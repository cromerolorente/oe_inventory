"""Client for the AnyDesk REST API (my.anydesk II, API v2).

Used to find out whether the remote machines listed in oees_anydesk are online.
``GET /v2/api/v2/clients`` returns every client (paginated) with its online
``state``, which we match against each row's ``code`` (the AnyDesk address /
client id, i.e. the API's ``cid``). Endpoint path per AnyDesk support (2026-07).

Auth is a single static token sent in the ``X-Api-Token`` header (the "API
password" generated in the my.anydesk II console). Credentials come from the
environment — see settings.ANYDESK_*.

NOTE: my.anydesk.com is fronted by Cloudflare. AnyDesk support (2026-07) said
IP whitelisting is not possible and that the HTTP 403 comes from using a
browser-like/curl client; automation must send a proper User-Agent and they
recommend Python's ``requests``. We therefore use ``requests`` (its default
header set/order reads as an API client, unlike urllib's minimal headers) with
a plain automation User-Agent. If Cloudflare still serves its "Just a moment"
challenge, the call is reported as such so the caller falls back gracefully.
"""

import logging

import requests

from django.conf import settings

logger = logging.getLogger(__name__)

# Plain, non-browser User-Agent (per AnyDesk support: a browser UA triggers
# Cloudflare's interactive JS challenge; automation should identify itself).
_USER_AGENT = 'OE-Inventory/1.0 (automation)'
# Page size for the paginated /clients listing.
_PAGE_LIMIT = 200


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
    decoded JSON, via ``requests``. Raises AnydeskError on transport/HTTP errors.

    AnyDesk's cert is public/valid, so verification stays on in production; set
    ANYDESK_VERIFY_SSL=False only for local dev (python.org macOS lacks a CA
    bundle)."""
    url = settings.ANYDESK_API_URL.rstrip('/') + path
    verify = getattr(settings, 'ANYDESK_VERIFY_SSL', True)
    try:
        resp = requests.get(url, headers={
            'X-Api-Token': settings.ANYDESK_API_TOKEN,
            'Accept': 'application/json',
            'User-Agent': _USER_AGENT,
        }, timeout=20, verify=verify)
    except requests.RequestException as exc:
        raise AnydeskError(str(exc))

    if resp.status_code != 200:
        # Tell apart a Cloudflare edge challenge (an HTML "Just a moment..." page
        # — the request never reached the API) from a genuine API error (JSON),
        # so the logs say which it is.
        body = resp.text or ''
        if 'Just a moment' in body or 'cf-browser-verification' in body or '/cdn-cgi/' in body:
            raise AnydeskError(
                f"HTTP {resp.status_code}: blocked by Cloudflare challenge (request "
                f"did not reach the API) at {settings.ANYDESK_API_URL}")
        raise AnydeskError(f"HTTP {resp.status_code} from API: {body[:200]}")
    try:
        return resp.json()
    except ValueError:
        raise AnydeskError("AnyDesk returned a non-JSON response")


def online_map():
    """Map AnyDesk client id (str) -> True/False (online) for every client in the
    account. Walks the paginated ``GET /v2/api/v2/clients`` listing. Raises
    AnydeskError on connectivity/auth problems."""
    result = {}
    offset = 0
    try:
        while True:
            path = f"/v2/api/v2/clients?limit={_PAGE_LIMIT}&offset={offset}"
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
