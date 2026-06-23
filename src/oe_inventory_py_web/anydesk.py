"""Client for the AnyDesk REST API (my.anydesk management console, v1).

Used to find out whether the remote machines listed in oees_anydesk are online.
A single ``GET /clients`` call returns every client with its online status, which
we then match against each row's ``code`` (the AnyDesk address / client id).

Auth is a per-request HMAC-SHA1 token built from the license id and API key
(``AD <license>:<timestamp>:<token>``), exactly as the official AnyDesk Python
library does. Credentials come from the environment — see settings.ANYDESK_*.
Standard library only (urllib).
"""

import base64
import hashlib
import hmac
import json
import logging
import ssl
import time
import urllib.request

from django.conf import settings

logger = logging.getLogger(__name__)


def _ssl_context():
    # AnyDesk's API uses a valid public (DigiCert) certificate, so verification
    # works on the server. The python.org build on macOS ships without a CA
    # bundle, so set ANYDESK_VERIFY_SSL=False locally to bypass verification.
    if getattr(settings, 'ANYDESK_VERIFY_SSL', True):
        return None
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    return ctx


class AnydeskError(Exception):
    """Raised when the AnyDesk API can't be reached or returns an error."""


def anydesk_configured():
    return bool(getattr(settings, 'ANYDESK_API_LICENSE', '')) and \
        bool(getattr(settings, 'ANYDESK_API_KEY', ''))


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


def _auth(resource, content='', method='GET'):
    """Build the 'AD <license>:<timestamp>:<token>' Authorization header."""
    content_hash = base64.b64encode(hashlib.sha1(content.encode('utf-8')).digest()).decode('utf-8')
    timestamp = str(int(time.time()))
    request_string = f"{method}\n{resource}\n{timestamp}\n{content_hash}"
    token = base64.b64encode(hmac.new(
        settings.ANYDESK_API_KEY.encode('utf-8'),
        request_string.encode('utf-8'),
        hashlib.sha1,
    ).digest()).decode('utf-8')
    return f"AD {settings.ANYDESK_API_LICENSE}:{timestamp}:{token}"


def _request(resource):
    url = settings.ANYDESK_API_URL.rstrip('/') + '/' + resource
    req = urllib.request.Request(url, headers={'Authorization': _auth('/' + resource)})
    with urllib.request.urlopen(req, timeout=20, context=_ssl_context()) as resp:
        return json.loads(resp.read().decode('utf-8'))


def online_map():
    """Map AnyDesk client id (str) -> True/False (online) for every client in the
    account. Raises AnydeskError on connectivity/auth problems."""
    try:
        data = _request('clients')
    except Exception as exc:
        logger.exception("AnyDesk clients request failed")
        raise AnydeskError(str(exc))

    result = {}
    for c in (data.get('list') or []):
        if isinstance(c, dict) and c.get('cid') is not None:
            result[str(c['cid'])] = bool(c.get('online'))
    return result
