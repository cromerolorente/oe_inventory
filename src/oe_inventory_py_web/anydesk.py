"""Client for the AnyDesk REST API (my.anydesk II, API v2).

Used to find out whether the remote machines listed in oees_anydesk are online.
``GET /api/v2/clients`` returns every client (paginated) with its online
``state``, which we match against each row's ``code`` (the AnyDesk address /
client id, i.e. the API's ``cid``).

Auth is a single static token sent in the ``X-Api-Token`` header (the "API
password" generated in the my.anydesk II console). Credentials come from the
environment — see settings.ANYDESK_*. Standard library only (urllib).

NOTE: my.anydesk.com is fronted by Cloudflare's managed challenge, which blocks
non-browser clients from some IP ranges (you'll get an HTTP 403 "Just a
moment..." HTML page instead of JSON). We send a browser-like User-Agent, but if
the host keeps challenging from a given network the calls must run from an
allowed IP (e.g. the production server).
"""

import json
import logging
import ssl
import urllib.request

from django.conf import settings

logger = logging.getLogger(__name__)

# Cloudflare rejects urllib's default User-Agent; present a browser-like one.
_USER_AGENT = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
               'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36')
# Page size for the paginated /clients listing.
_PAGE_LIMIT = 200


def _ssl_context():
    # AnyDesk's API uses a valid public certificate, so verification works on the
    # server. The python.org build on macOS ships without a CA bundle, so set
    # ANYDESK_VERIFY_SSL=False locally to bypass verification.
    if getattr(settings, 'ANYDESK_VERIFY_SSL', True):
        return None
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    return ctx


class AnydeskError(Exception):
    """Raised when the AnyDesk API can't be reached or returns an error."""


def anydesk_configured():
    """True when the v2 token is set (license id is not needed for v2)."""
    return bool(getattr(settings, 'ANYDESK_API_TOKEN', ''))


def pick_column(columns, *names, prefix=None):
    """Return the first matching column name from `columns` (case-insensitive
    exact match against `names`, then an optional `prefix` match), or None.

    Tolerates schema naming variants — e.g. the live table spells the column
    `last_connetion` (sic), so we match `last_conn*`."""
    lower = {c.lower(): c for c in columns}
    for n in names:
        if n.lower() in lower:
            return lower[n.lower()]
    if prefix:
        for c in columns:
            if c.lower().startswith(prefix.lower()):
                return c
    return None


def _request(path):
    """GET an absolute API path (e.g. '/api/v2/clients?...') and return the
    decoded JSON. Raises on transport/HTTP errors."""
    url = settings.ANYDESK_API_URL.rstrip('/') + path
    req = urllib.request.Request(url, headers={
        'X-Api-Token': settings.ANYDESK_API_TOKEN,
        'Accept': 'application/json',
        'User-Agent': _USER_AGENT,
    })
    with urllib.request.urlopen(req, timeout=20, context=_ssl_context()) as resp:
        return json.loads(resp.read().decode('utf-8'))


def online_map():
    """Map AnyDesk client id (str) -> True/False (online) for every client in the
    account. Walks the paginated ``GET /api/v2/clients`` listing. Raises
    AnydeskError on connectivity/auth problems."""
    result = {}
    offset = 0
    try:
        while True:
            path = f"/api/v2/clients?limit={_PAGE_LIMIT}&offset={offset}"
            data = _request(path)
            items = data.get('items') or []
            for c in items:
                if isinstance(c, dict) and c.get('cid') is not None:
                    # v2 reports status via the `state` enum ("online"/"offline").
                    result[str(c['cid'])] = (str(c.get('state', '')).lower() == 'online')
            # Advance while the API says there are more pages and we got some.
            if not data.get('hasNextPage') or not items:
                break
            offset += len(items)
    except Exception as exc:
        # Logged at WARNING (no traceback) — this runs every few minutes and the
        # caller handles the failure with a fallback.
        logger.warning("AnyDesk clients request failed: %s", exc)
        raise AnydeskError(str(exc))

    return result
