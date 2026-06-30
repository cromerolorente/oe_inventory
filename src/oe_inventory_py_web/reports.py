"""PDF report generation for the Staff screen.

Web port of reports_design.staff_devices.StaffReportDevices: same layout, but it
returns the PDF as bytes (in memory) instead of writing to a local Windows path.
"""

import datetime
import io
import os
from xml.sax.saxutils import escape

from django.conf import settings
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.utils import ImageReader
from reportlab.platypus import Image, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


def _logo_path():
    """Optional report logo, served from the app's static folder if present."""
    path = os.path.join(
        settings.BASE_DIR, 'oe_inventory_py_web', 'static', 'images', 'report_logo.png'
    )
    return path if os.path.exists(path) else None


def build_staff_inventory_pdf(staff_data, devices_list, generated_by='', show_returned=False):
    """Return the staff inventory report as PDF bytes.

    staff_data:   dict with {'name', 'dep', 'comp', 'deleg', 'fecha_i'}
    devices_list: list of dicts [{'id', 'serial', 'type', 'brand', 'model', 'value', 'obs'}]
    generated_by: name shown in the audit footer line.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=landscape(A4),
        rightMargin=1 * cm, leftMargin=1 * cm,
        topMargin=1.5 * cm, bottomMargin=1 * cm,
    )
    elements = []
    styles = getSampleStyleSheet()
    style_h1 = ParagraphStyle('H1', parent=styles['Normal'], fontSize=18, leading=22, fontName='Helvetica-Bold')
    style_bold = ParagraphStyle('Bold', parent=styles['Normal'], fontSize=8, fontName='Helvetica-Bold', leading=10)
    style_normal = ParagraphStyle('Body', parent=styles['Normal'], fontSize=8, leading=9)
    style_red = ParagraphStyle('Red', parent=styles['Normal'], fontSize=8, textColor=colors.red, leading=10)
    style_audit = ParagraphStyle('Audit', parent=styles['Normal'], fontSize=7, textColor=colors.grey)

    # --- 1. Header (title + optional logo) ---
    logo = _logo_path()
    logo_cell = Paragraph('', style_bold)
    if logo:
        try:
            # Preserve the logo's real aspect ratio: scale it to fit within a
            # max box instead of forcing fixed width/height (which distorted it).
            iw, ih = ImageReader(logo).getSize()
            max_w, max_h = 5.0 * cm, 1.6 * cm
            scale = min(max_w / iw, max_h / ih)
            logo_cell = Image(logo, width=iw * scale, height=ih * scale, hAlign='RIGHT')
        except Exception:
            logo_cell = Paragraph('', style_bold)

    header_table = Table(
        [[Paragraph("Personal Inventory", style_h1), logo_cell]],
        colWidths=[21 * cm, 6 * cm], hAlign='LEFT',
    )
    header_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
    ]))
    elements.append(header_table)
    elements.append(Spacer(1, 0.3 * cm))

    # --- 2. Employee data ---
    data_user = [
        [Paragraph("Name", style_bold), Paragraph(staff_data.get('name', ''), style_normal)],
        [Paragraph("Department", style_bold), Paragraph(staff_data.get('dep', ''), style_normal)],
        [Paragraph("Company", style_bold), Paragraph(staff_data.get('comp', ''), style_normal)],
        [Paragraph("Delegation", style_bold), Paragraph(staff_data.get('deleg', ''), style_normal)],
        [Paragraph("Date of Incorporation", style_bold), Paragraph(staff_data.get('fecha_i', ''), style_normal)],
    ]
    user_table = Table(data_user, colWidths=[4.5 * cm, 14 * cm], hAlign='LEFT')
    user_table.setStyle(TableStyle([
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
    ]))
    elements.append(user_table)
    elements.append(Spacer(1, 0.5 * cm))

    # --- 3. Inventory table ---
    header = ["ID", "Serial Number", "Type", "Brand", "Model", "Value", "Obs"]
    if show_returned:
        header.append("Returned")
    table_data = [header]
    for eq in devices_list:
        # Currency formatting: 2250 -> 2.250,00 (European style).
        val = eq.get('value')
        try:
            val_num = float(val)
            val_str = f"{val_num:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".") if val_num > 0 else "0"
        except (TypeError, ValueError):
            val_str = val if val is not None else ""
        row = [
            eq.get('id', ''), eq.get('serial', ''), eq.get('type', ''),
            eq.get('brand', ''), eq.get('model', ''), val_str, eq.get('obs', ''),
        ]
        if show_returned:
            row.append("RETURNED" if eq.get('returned') else "")
        table_data.append(row)

    if show_returned:
        widths = [1.3 * cm, 4.5 * cm, 3.2 * cm, 2.8 * cm, 5.5 * cm, 2.2 * cm, 5.2 * cm, 3.0 * cm]
    else:
        widths = [1.5 * cm, 5.0 * cm, 3.5 * cm, 3.0 * cm, 7.5 * cm, 2.5 * cm, 4.5 * cm]
    inv_table = Table(table_data, colWidths=widths)
    style = [
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('LINEBELOW', (0, 0), (-1, 0), 1, colors.black),
        ('ALIGN', (0, 0), (0, -1), 'CENTER'),   # ID centered
        ('ALIGN', (5, 0), (5, -1), 'RIGHT'),    # Value right-aligned
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]
    if show_returned:
        # "Returned" column centered and highlighted in red.
        style.append(('ALIGN', (7, 0), (7, -1), 'CENTER'))
        style.append(('FONTNAME', (7, 1), (7, -1), 'Helvetica-Bold'))
        style.append(('TEXTCOLOR', (7, 1), (7, -1), colors.red))
    inv_table.setStyle(TableStyle(style))
    elements.append(inv_table)

    # --- 4. Footer (legal notice + signature/audit) ---
    elements.append(Spacer(1, 2 * cm))
    elements.append(Paragraph(
        "PLEASE NOTE: All devices must be handed in and collected with their corresponding cables and chargers.",
        style_red,
    ))
    elements.append(Paragraph(
        "When collecting the equipment, please request the login and password details so that it can be formatted.",
        style_red,
    ))
    elements.append(Spacer(1, 1 * cm))

    fecha_gen = datetime.datetime.now().strftime("%d-%m-%Y at %H:%M")
    elements.append(Paragraph("Acceptance Delivery", style_normal))
    elements.append(Spacer(1, 1.8 * cm))  # room for the handwritten signature

    footer_table = Table(
        [[Paragraph(staff_data.get('name', ''), style_normal),
          Paragraph(f"Document generated by {generated_by} on {fecha_gen}", style_audit)]],
        colWidths=[6 * cm, 13 * cm], hAlign='LEFT',
    )
    footer_table.setStyle(TableStyle([
        ('LINEABOVE', (0, 0), (-1, 0), 0.5, colors.black),  # signature / audit line
        ('VALIGN', (0, 0), (-1, -1), 'BOTTOM'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
    ]))
    elements.append(footer_table)

    doc.build(elements)
    return buffer.getvalue()


def _metric_value(entry, label):
    """(text, numeric) for a topology node metric (e.g. CPU/Memory), or ('—', None)."""
    for m in (entry.get('metrics') or []):
        if m.get('label') == label:
            v = m.get('value')
            return (f'{v}%', v if isinstance(v, (int, float)) else None)
    return ('—', None)


def _usage_hex(v):
    """Colour for a CPU/memory % (green <50, orange 50-80, red >80), or None."""
    if v is None:
        return None
    return '#dc3545' if v > 80 else ('#fd7e14' if v >= 50 else '#16a34a')


def build_net_topology_pdf(site_name, topology):
    """Return one site's Net Overview topology (firewalls -> switches -> APs) as
    PDF bytes: a table per tier with status, clients, CPU/memory and firmware."""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=landscape(A4),
        rightMargin=1 * cm, leftMargin=1 * cm, topMargin=1.5 * cm, bottomMargin=1 * cm,
    )
    elements = []
    styles = getSampleStyleSheet()
    style_h1 = ParagraphStyle('TH1', parent=styles['Normal'], fontSize=16, leading=20, fontName='Helvetica-Bold')
    style_bold = ParagraphStyle('TBold', parent=styles['Normal'], fontSize=8, fontName='Helvetica-Bold', leading=10)
    style_meta = ParagraphStyle('TMeta', parent=styles['Normal'], fontSize=9, textColor=colors.grey, leading=12)
    style_audit = ParagraphStyle('TAudit', parent=styles['Normal'], fontSize=7, textColor=colors.grey)

    topology = topology or {}
    gws = topology.get('gateways') or []
    sws = topology.get('switches') or []
    aps = topology.get('aps') or []
    total = len(gws) + len(sws) + len(aps)
    online = sum(1 for d in (gws + sws + aps) if d.get('online'))

    # --- Header (title + optional logo) ---
    logo = _logo_path()
    logo_cell = Paragraph('', style_bold)
    if logo:
        try:
            iw, ih = ImageReader(logo).getSize()
            scale = min(5.0 * cm / iw, 1.6 * cm / ih)
            logo_cell = Image(logo, width=iw * scale, height=ih * scale, hAlign='RIGHT')
        except Exception:
            logo_cell = Paragraph('', style_bold)
    header_table = Table(
        [[Paragraph(f"Network Topology — {site_name or ''}", style_h1), logo_cell]],
        colWidths=[21 * cm, 6 * cm], hAlign='LEFT',
    )
    header_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'), ('ALIGN', (1, 0), (1, 0), 'RIGHT')]))
    elements.append(header_table)
    elements.append(Spacer(1, 0.2 * cm))
    elements.append(Paragraph(
        f"{len(sws)} switches · {len(aps)} APs · {len(gws)} firewalls · {online}/{total} online",
        style_meta))
    elements.append(Spacer(1, 0.4 * cm))

    # Card styles that mirror the on-screen device cards.
    st_name = ParagraphStyle('cN', parent=styles['Normal'], fontSize=8, leading=10, fontName='Helvetica-Bold')
    st_model = ParagraphStyle('cM', parent=styles['Normal'], fontSize=6.5, leading=8, textColor=colors.HexColor('#6b7280'))
    st_foot = ParagraphStyle('cF', parent=styles['Normal'], fontSize=6.5, leading=9)
    st_metric = ParagraphStyle('cMet', parent=styles['Normal'], fontSize=6.5, leading=9)
    st_out = ParagraphStyle('cO', parent=styles['Normal'], fontSize=6.5, leading=8,
                            textColor=colors.HexColor('#fd7e14'), alignment=TA_CENTER)
    st_tier = ParagraphStyle('cTier', parent=styles['Normal'], fontSize=10, leading=14,
                             fontName='Helvetica-Bold', alignment=TA_CENTER, textColor=colors.HexColor('#6b7280'))
    st_site = ParagraphStyle('cSite', parent=styles['Normal'], fontSize=11, leading=14,
                             fontName='Helvetica-Bold', alignment=TA_CENTER)
    st_sitemeta = ParagraphStyle('cSiteM', parent=styles['Normal'], fontSize=7.5, leading=10,
                                 alignment=TA_CENTER, textColor=colors.HexColor('#6b7280'))

    CARD_W = 4.3 * cm
    PER_ROW = 5

    def make_card(d):
        online = d.get('online')
        border = (colors.HexColor('#fd7e14') if d.get('outdated')
                  else (colors.HexColor('#e5e7eb') if online else colors.HexColor('#f0a8a8')))
        status_hex = '#16a34a' if online else '#dc3545'
        rows = [
            [Paragraph(escape(d.get('name') or ''), st_name)],
            [Paragraph(escape(d.get('model') or '') or '&nbsp;', st_model)],
            [Paragraph('<font color="%s">%s</font> &nbsp;|&nbsp; %d clients'
                       % (status_hex, 'Online' if online else 'Offline', d.get('clients') or 0), st_foot)],
        ]
        spans = []
        for label in ('CPU', 'Memory'):
            txt, val = _metric_value(d, label)
            if val is not None:
                spans.append('<font color="%s">%s %s</font>' % (_usage_hex(val), label, txt))
        if spans:
            rows.append([Paragraph(' &nbsp; '.join(spans), st_metric)])
        if d.get('outdated'):
            rows.append([Paragraph('firmware outdated', st_out)])
        card = Table(rows, colWidths=[CARD_W])
        card.setStyle(TableStyle([
            ('BOX', (0, 0), (-1, -1), 0.8, border),
            ('BACKGROUND', (0, 0), (-1, -1), colors.white),
            ('LEFTPADDING', (0, 0), (-1, -1), 5), ('RIGHTPADDING', (0, 0), (-1, -1), 5),
            ('TOPPADDING', (0, 0), (-1, -1), 2), ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))
        return card

    def add_tier(title, items):
        if not items:
            return
        elements.append(Paragraph(title, st_tier))
        elements.append(Spacer(1, 0.15 * cm))
        cards = [make_card(d) for d in items]
        # Centered rows of up to PER_ROW cards, like the on-screen tiers.
        for r in range(0, len(cards), PER_ROW):
            chunk = cards[r:r + PER_ROW]
            grid = Table([chunk], colWidths=[CARD_W] * len(chunk), hAlign='CENTER')
            grid.setStyle(TableStyle([
                ('LEFTPADDING', (0, 0), (-1, -1), 5), ('RIGHTPADDING', (0, 0), (-1, -1), 5),
                ('TOPPADDING', (0, 0), (-1, -1), 5), ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ]))
            elements.append(grid)
        elements.append(Spacer(1, 0.35 * cm))

    if not total:
        elements.append(Paragraph('No devices in this site.', style_meta))
    else:
        # Site node on top, then the tiers (same layout/order as on screen).
        site_box = Table(
            [[Paragraph(escape(site_name or ''), st_site)],
             [Paragraph('%d switches | %d APs | %d firewalls | %d/%d online'
                        % (len(sws), len(aps), len(gws), online, total), st_sitemeta)]],
            colWidths=[10 * cm], hAlign='CENTER')
        site_box.setStyle(TableStyle([
            ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#FF48D8')),
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#fff0fb')),
            ('TOPPADDING', (0, 0), (-1, -1), 4), ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ]))
        elements.append(site_box)
        elements.append(Spacer(1, 0.35 * cm))
        add_tier('Firewalls / Gateways', gws)
        add_tier('Switches', sws)
        add_tier('Access Points', aps)

    elements.append(Spacer(1, 0.2 * cm))
    elements.append(Paragraph('Note: links are shown by tier (not port-to-port). '
                              'Client counts reflect devices connected at the time of generation.', style_audit))

    doc.build(elements)
    return buffer.getvalue()
