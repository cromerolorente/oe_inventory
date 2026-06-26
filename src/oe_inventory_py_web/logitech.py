"""Client for the Logitech Sync Cloud API (LogiSync Place / Insights).

Used to monitor the videoconference rooms (Logitech Rally Bar / Bar Mini).
Authentication is mutual TLS (mTLS): every request presents a client
certificate + private key issued by Logitech. We use the standard library
(urllib + ssl) — ``ssl_context.load_cert_chain(cert, key)`` is the stdlib
equivalent of requests' ``cert=(cert, key)``.

Paths and base URL come from settings.LOGITECH_* (env only).
"""

import datetime
import json
import logging
import os
import ssl
import urllib.request

from django.conf import settings
from django.utils.dateparse import parse_datetime

logger = logging.getLogger(__name__)


def _parse_dt(value):
    """Best-effort parse of a meeting start/end value into a datetime (or None).
    Accepts ISO-8601 strings or epoch seconds/milliseconds; adjust once we see
    the live Logitech format."""
    if not value:
        return None
    if isinstance(value, datetime.datetime):
        return value
    if isinstance(value, (int, float)):
        ts = value / 1000 if value > 1e12 else value  # ms vs s
        try:
            return datetime.datetime.fromtimestamp(ts, tz=datetime.timezone.utc)
        except (ValueError, OSError, OverflowError):
            return None
    return parse_datetime(str(value))


class LogitechError(Exception):
    """Raised when the Logitech Sync API can't be reached or returns an error."""


def logitech_configured():
    """True when the base URL and the client cert + key files are all present."""
    cert = getattr(settings, 'LOGITECH_CERT_PATH', '')
    key = getattr(settings, 'LOGITECH_KEY_PATH', '')
    return bool(getattr(settings, 'LOGITECH_API_BASE_URL', '')) and \
        bool(cert) and bool(key) and os.path.exists(cert) and os.path.exists(key)


def _ssl_context():
    """mTLS context: presents our client certificate + private key. Server-side
    verification stays on unless LOGITECH_VERIFY_SSL is False (local dev)."""
    ctx = ssl.create_default_context()
    if not getattr(settings, 'LOGITECH_VERIFY_SSL', True):
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
    ctx.load_cert_chain(certfile=settings.LOGITECH_CERT_PATH,
                        keyfile=settings.LOGITECH_KEY_PATH)
    return ctx


def _request(path):
    url = settings.LOGITECH_API_BASE_URL.rstrip('/') + path
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req, timeout=20, context=_ssl_context()) as resp:
        return json.loads(resp.read().decode('utf-8'))


def _is_occupied_but_empty(occupied, in_meeting, occupancy):
    """A room counts as an alert when it's occupied / in a meeting but no people
    are detected (occupancyCount == 0). Unknown occupancy (None) is NOT an alert."""
    return bool(occupied or in_meeting) and occupancy == 0


def _meeting_field(insights, *keys):
    """Best-effort read of a meeting attribute that may be a string or an object
    ({name|displayName|email}). Field names are guessed until we see the real
    payload; adjust here once Logitech returns live meeting data."""
    for k in keys:
        v = insights.get(k)
        if v:
            if isinstance(v, dict):
                return v.get('name') or v.get('displayName') or v.get('email') or ''
            return str(v)
    return ''


def future_bookings():
    """Upcoming room bookings (from now on). Each entry::

        {'room', 'organizer_email', 'organizer_name', 'title', 'start'}

    The endpoint and field names are a best-effort guess until we see the live
    Sync Cloud booking payload — adjust here when it's available. Raises
    LogitechError on connectivity/auth problems."""
    try:
        data = _request('/bookings') or {}
    except Exception as exc:
        logger.warning("Logitech bookings request failed: %s", exc)
        raise LogitechError(str(exc))

    items = data.get('bookings') or data.get('items') or []
    out = []
    for b in items:
        if not isinstance(b, dict):
            continue
        org = b.get('organizer') if isinstance(b.get('organizer'), dict) else {}
        out.append({
            'room': b.get('placeName') or b.get('room') or '',
            'organizer_email': (b.get('organizerEmail') or org.get('email') or '').strip(),
            'organizer_name': org.get('name') or b.get('organizerName') or '',
            'title': b.get('meetingTitle') or b.get('title') or b.get('subject') or '',
            'start': b.get('start') or b.get('startTime') or '',
        })
    return out


def demo_rooms():
    """Sample rooms (same shape as rooms_overview) shown when the integration
    isn't configured yet, so the screen design can be worked on meanwhile."""
    def _hm(h, m=0):
        return datetime.datetime(2026, 6, 26, h, m)

    def room(name, occupied, in_meeting, occupancy, model, status, organizer='', title='',
             start=None, end=None):
        connected = status == 'connected'
        return {
            'id': 'demo-' + name, 'name': name,
            'occupied': occupied, 'in_meeting': in_meeting, 'occupancy': occupancy,
            'connected': connected,
            'organizer': organizer, 'title': title,
            'start_time': start, 'end_time': end,
            'alert': _is_occupied_but_empty(occupied, in_meeting, occupancy) or not connected,
            'devices': [{'model': model, 'firmware': 'CollabOS 1.12.x', 'status': status}],
        }
    return [
        room('Sala de Juntas', True, True, 6, 'Rally Bar', 'connected',
             organizer='Ana García', title='Comité de Dirección', start=_hm(9), end=_hm(10)),
        room('Sala Picasso', True, True, 3, 'Rally Bar Mini', 'connected',
             organizer='Marta Ruiz', title='Sprint Review', start=_hm(11, 30), end=_hm(12)),
        room('Sala Dalí', True, False, 2, 'Rally Bar Mini', 'connected'),
        room('Sala Sorolla', True, True, 4, 'Rally Bar', 'connected',
             organizer='Javier Soler', title='Demo Cliente', start=_hm(13), end=_hm(14)),
        room('Sala Miró', False, False, 0, 'Rally Bar Mini', 'connected'),
        # Occupied / in meeting but nobody detected -> alert.
        room('Sala Formación', True, True, 0, 'Rally Bar', 'connected',
             organizer='Luis Pérez', title='Onboarding Q3', start=_hm(16), end=_hm(17)),
        room('Sala Goya', False, False, 0, 'Rally Bar Mini', 'disconnected'),
    ]


def rooms_overview():
    """One entry per place/room with its occupancy and device status.

    Shape of each row::

        {'id', 'name', 'occupied', 'in_meeting', 'occupancy', 'connected',
         'devices': [{'model', 'firmware', 'status'}, ...]}

    Raises LogitechError on connectivity/auth problems."""
    try:
        data = _request('/places') or {}
    except Exception as exc:
        logger.warning("Logitech Sync request failed: %s", exc)
        raise LogitechError(str(exc))

    rooms = []
    for p in (data.get('places') or []):
        if not isinstance(p, dict):
            continue
        insights = p.get('insights') or {}
        devices = [d for d in (p.get('devices') or []) if isinstance(d, dict)]
        occupied = bool(insights.get('isOccupied'))
        in_meeting = bool(insights.get('inMeeting'))
        occupancy = insights.get('occupancyCount')
        connected = any(d.get('status') == 'connected' for d in devices)
        org = insights.get('organizer') if isinstance(insights.get('organizer'), dict) else {}
        rooms.append({
            'id': p.get('id') or '',
            'name': p.get('name') or p.get('id') or '?',
            'occupied': occupied,
            'in_meeting': in_meeting,
            'occupancy': occupancy,
            # Best-effort meeting metadata (field names guessed; adjust when live).
            'meet_id': str(insights.get('meetingId') or insights.get('currentMeetingId')
                           or insights.get('sessionId') or ''),
            'organizer': _meeting_field(insights, 'organizer', 'meetingOrganizer',
                                        'organizerName', 'host'),
            'organizer_email': (insights.get('organizerEmail') or org.get('email') or ''),
            'title': _meeting_field(insights, 'meetingTitle', 'title', 'subject'),
            'start_time': _parse_dt(insights.get('startTime') or insights.get('meetingStart')
                                    or insights.get('scheduledStartTime') or insights.get('start')),
            'end_time': _parse_dt(insights.get('endTime') or insights.get('meetingEnd')
                                  or insights.get('scheduledEndTime') or insights.get('end')),
            # Alert when occupied/in-meeting but no people detected, OR disconnected.
            'alert': _is_occupied_but_empty(occupied, in_meeting, occupancy) or not connected,
            # A room is "connected" when at least one of its devices is connected.
            'connected': connected,
            'devices': [
                {'model': d.get('model') or '',
                 'firmware': d.get('firmwareVersion') or '',
                 'status': d.get('status') or ''}
                for d in devices
            ],
        })
    return rooms
