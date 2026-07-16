"""Read incorporation-preference replies from the incorporations@oees.app
mailbox over IMAP, extract the returned editable PDF form, and update the
matching incorporation record from its editable fields (keyed by the read-only
``id`` field written by reports.build_incorporation_form_pdf).

Invoked best-effort from the 5-minute background refresh
(status_cache.compute_and_store). Processed messages are flagged ``\\Seen`` so
they are not handled again. Config comes from settings.INCORP_IMAP_* (env only).
"""

import email
import imaplib
import io
import logging
from datetime import datetime
from email.utils import parseaddr

from django.conf import settings

logger = logging.getLogger(__name__)

# Editable PDF checkbox field -> OeesIncorporations attribute. Only the fields
# that are editable in the PDF are written back; Phone/Screen were removed from
# the form, so those DB columns are left untouched.
_CHECKBOX_FIELDS = {
    'chk_usbchub': 'usbchub',
    'chk_pdf': 'pdf',
    'chk_acad': 'acad',
    'chk_keyboard': 'keyboard',
}
_VALID_SIZES = {'XS', 'S', 'M', 'L', 'XL', 'XXL', 'XXXL'}


def imap_configured():
    """True when the IMAP host and credentials are all set."""
    return bool(getattr(settings, 'INCORP_IMAP_HOST', '')
                and getattr(settings, 'INCORP_IMAP_USER', '')
                and getattr(settings, 'INCORP_IMAP_PASSWORD', ''))


def _connect():
    host = settings.INCORP_IMAP_HOST
    port = int(getattr(settings, 'INCORP_IMAP_PORT', 993) or 993)
    conn = imaplib.IMAP4_SSL(host, port)
    conn.login(settings.INCORP_IMAP_USER, settings.INCORP_IMAP_PASSWORD)
    return conn


def _checkbox_on(value):
    """AcroForm checkbox state -> bool. Our PDFs use '/Yes' (on) / '/Off' (off);
    treat anything that isn't an explicit off/empty state as checked."""
    v = ('' if value is None else str(value)).strip().lower()
    return v not in ('', 'off', '/off', 'no', '0', 'false')


def _read_pdf(pdf_bytes):
    """Return (fields_dict, PdfReader). fields_dict is {name: /V}."""
    from pypdf import PdfReader
    reader = PdfReader(io.BytesIO(pdf_bytes))
    fields = reader.get_fields() or {}
    return {name: f.get('/V') for name, f in fields.items()}, reader


def _mouse_selection(reader):
    """Return 'right' / 'left' / '' for the mouse_hand radio group.

    Reads the selection by WIDGET POSITION, not by the export value name: some
    PDF readers rewrite radio export names to /0,/1 on save, which would break a
    name-based lookup. The form draws Right first (kid 0) and Left second (kid 1);
    we find the kid whose on-state (or /AS) equals the field value /V. Falls back
    to the literal name when the reader preserved it."""
    try:
        acro = reader.trailer['/Root'].get('/AcroForm')
        if not acro:
            return ''
        for f in acro.get('/Fields', []):
            obj = f.get_object()
            if obj.get('/T') != 'mouse_hand':
                continue
            v = obj.get('/V')
            if v in (None, '', '/Off'):
                return ''
            vs = str(v).lstrip('/').lower()
            if vs in ('right', 'left'):
                return vs
            kids = obj.get('/Kids') or []
            for idx, kid in enumerate(kids):
                ko = kid.get_object()
                apn = (ko.get('/AP') or {}).get('/N') or {}
                onstates = [k for k in apn.keys() if k != '/Off']
                if v in onstates or ko.get('/AS') == v:
                    return 'right' if idx == 0 else 'left'
        return ''
    except Exception:
        logger.exception("Could not read mouse_hand selection")
        return ''


def _iter_pdf_attachments(msg):
    for part in msg.walk():
        if part.get_content_maintype() == 'multipart':
            continue
        filename = part.get_filename() or ''
        if part.get_content_type() == 'application/pdf' or filename.lower().endswith('.pdf'):
            payload = part.get_payload(decode=True)
            if payload:
                yield payload


def apply_pdf(pdf_bytes, sender):
    """Update the incorporation identified by the PDF's ``id`` field from its
    editable fields, and prepend an audit line to notes. Returns True on update.

    We only act on our *editable* form PDFs: a PDF with no AcroForm fields (a
    photo/scan/printout of the document, exactly what the email asks candidates
    not to send) is ignored. The caller marks the email read regardless."""
    from .models import OeesIncorporations

    fields, reader = _read_pdf(pdf_bytes)
    if not fields:
        logger.info("PDF from %s is not an editable form (no fields); ignoring", sender)
        return False
    raw_id = fields.get('id')
    id_str = str(raw_id).strip() if raw_id is not None else ''
    if not id_str.isdigit():
        logger.warning("Incorporation PDF from %s has no usable ID (%r)", sender, raw_id)
        return False

    rec = OeesIncorporations.objects.filter(id=int(id_str)).first()
    if not rec:
        logger.warning("Incorporation id %s (from %s) not found", id_str, sender)
        return False

    for pdf_name, attr in _CHECKBOX_FIELDS.items():
        setattr(rec, attr, 1 if _checkbox_on(fields.get(pdf_name)) else 0)

    # Mouse is a radio group (exclusive by construction); read by widget position.
    hand = _mouse_selection(reader)
    rec.mouse = 1 if hand == 'right' else 0
    rec.left_mouse = 1 if hand == 'left' else 0

    size = str(fields.get('sweatshirt_size') or '').strip().upper()
    rec.sweatshirt_size = size if size in _VALID_SIZES else None

    # Address is only present in the PDF for remote delegations.
    addr = fields.get('address')
    if addr is not None:
        rec.direccion = str(addr).strip()

    now = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    note = f"{now} - Received preferences from {sender} automatically"
    rec.notes = f"{note}\n{rec.notes or ''}".strip()
    rec.email_processed = 2  # returned PDF processed
    rec.save()
    logger.info("Incorporation %s updated from preferences PDF sent by %s", id_str, sender)
    return True


def process_inbox():
    """Process all UNSEEN messages with a PDF attachment. Returns the number of
    incorporation records updated. Best-effort: a bad attachment is logged and
    the message is still marked read so it isn't retried forever."""
    mailbox = getattr(settings, 'INCORP_IMAP_MAILBOX', 'INBOX')
    conn = _connect()
    updated = 0
    try:
        conn.select(mailbox)
        typ, data = conn.search(None, 'UNSEEN')
        if typ != 'OK' or not data or not data[0]:
            return 0
        for num in data[0].split():
            typ, msg_data = conn.fetch(num, '(RFC822)')
            if typ != 'OK' or not msg_data or not msg_data[0]:
                continue
            msg = email.message_from_bytes(msg_data[0][1])
            sender = parseaddr(msg.get('From', ''))[1]
            for pdf_bytes in _iter_pdf_attachments(msg):
                try:
                    if apply_pdf(pdf_bytes, sender):
                        updated += 1
                except Exception:
                    logger.exception("Failed to apply incorporation PDF from %s", sender)
            # Mark read whether or not it matched, so a malformed/duplicate email
            # is not reprocessed on every cycle.
            conn.store(num, '+FLAGS', '\\Seen')
    finally:
        try:
            conn.close()
        except Exception:
            pass
        try:
            conn.logout()
        except Exception:
            pass
    return updated
