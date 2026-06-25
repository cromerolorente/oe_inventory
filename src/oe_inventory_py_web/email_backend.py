"""Django email backend that sends through the Resend API.

This replaces the previous SMTP backend. Both places the app sends mail — the
staff inventory report (frmStaff) and the password-reset flow (login) — go
through Django's standard email API, so routing everything through Resend is
just a matter of swapping EMAIL_BACKEND; no call site needs to change.

Implemented with the standard library only (urllib), matching the project's
existing no-extra-dependency style (same as the Nominatim geocoding helper).
"""

import base64
import json
import logging
import ssl
import urllib.error
import urllib.request

from django.conf import settings
from django.core.mail.backends.base import BaseEmailBackend

logger = logging.getLogger(__name__)

RESEND_API_URL = 'https://api.resend.com/emails'


def _ssl_context():
    # Resend uses a valid public certificate, so verification works on the
    # server. The python.org build on macOS ships without a CA bundle, so set
    # RESEND_VERIFY_SSL=False locally to bypass verification.
    if getattr(settings, 'RESEND_VERIFY_SSL', True):
        return None
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    return ctx


def build_resend_payload(message):
    """Translate a Django EmailMessage into the JSON payload Resend expects."""
    payload = {
        'from': message.from_email or settings.DEFAULT_FROM_EMAIL,
        'to': list(message.to),
        'subject': message.subject or '',
    }
    if message.cc:
        payload['cc'] = list(message.cc)
    if message.bcc:
        payload['bcc'] = list(message.bcc)
    if getattr(message, 'reply_to', None):
        payload['reply_to'] = list(message.reply_to)

    # Body: an html message goes in `html`, anything else as plain `text`.
    if message.content_subtype == 'html':
        payload['html'] = message.body or ''
    else:
        payload['text'] = message.body or ''

    # EmailMultiAlternatives html part (if any) wins as the html body.
    for content, mimetype in getattr(message, 'alternatives', None) or []:
        if mimetype == 'text/html':
            payload['html'] = content

    # Attachments (e.g. the staff inventory PDF). Resend takes the raw bytes as
    # an array of integers, matching the official Resend SDK's behaviour.
    attachments = []
    for attachment in message.attachments:
        if isinstance(attachment, tuple):
            filename, content, _mimetype = attachment
            if isinstance(content, str):
                content = content.encode('utf-8')
            attachments.append({
                'filename': filename or 'attachment',
                'content': list(content),
            })
    if attachments:
        payload['attachments'] = attachments

    return payload


class ResendEmailBackend(BaseEmailBackend):
    """Sends Django emails via the Resend HTTP API."""

    def __init__(self, fail_silently=False, **kwargs):
        super().__init__(fail_silently=fail_silently, **kwargs)
        self.api_key = getattr(settings, 'RESEND_API_KEY', '') or ''

    def send_messages(self, email_messages):
        if not email_messages:
            return 0
        if not self.api_key:
            if not self.fail_silently:
                raise ValueError("RESEND_API_KEY is not configured.")
            return 0

        sent = 0
        for message in email_messages:
            try:
                self._send(message)
                sent += 1
            except Exception:
                logger.exception("Resend: failed to send email to %s", getattr(message, 'to', None))
                if not self.fail_silently:
                    raise
        return sent

    def _send(self, message):
        data = json.dumps(build_resend_payload(message)).encode('utf-8')
        request = urllib.request.Request(
            RESEND_API_URL,
            data=data,
            method='POST',
            headers={
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json',
                # Resend's API is behind Cloudflare, which blocks urllib's default
                # User-Agent (Python-urllib/x.y) with error 1010. Send a normal UA.
                'User-Agent': 'Mozilla/5.0 (compatible; OE-Inventory/1.0; +https://octoenergy.com)',
            },
        )
        try:
            with urllib.request.urlopen(request, timeout=15, context=_ssl_context()) as response:
                response.read()
        except urllib.error.HTTPError as exc:
            # Surface Resend's error body (reason for 4xx, e.g. unverified domain
            # or a recipient not allowed in testing mode) so it's actionable.
            try:
                body = exc.read().decode('utf-8', 'replace')
            except Exception:
                body = ''
            logger.error("Resend API %s: %s", exc.code, body)
            raise
