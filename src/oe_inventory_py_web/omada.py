"""Minimal client for the TP-Link Omada Open API (Cloud-Based Controller).

Uses the OAuth2 *client credentials* grant to obtain an access token and then
queries the controller. Credentials come from the environment (never hardcoded)
— see settings.OMADA_*. Standard library only (urllib), matching the project's
no-extra-dependency style.

Docs: the controller exposes the Open API once an application is created under
Settings -> Platform Integration -> Open API (gives a Client ID / Secret).
"""

import json
import logging
import ssl
import urllib.parse
import urllib.request

from django.conf import settings

logger = logging.getLogger(__name__)


class OmadaError(Exception):
    """Raised when the Omada API can't be reached or returns an error."""


def omada_configured():
    """True when all the required credentials/URLs are set."""
    return all([
        getattr(settings, 'OMADA_BASE_URL', ''),
        getattr(settings, 'OMADA_OMADAC_ID', ''),
        getattr(settings, 'OMADA_CLIENT_ID', ''),
        getattr(settings, 'OMADA_CLIENT_SECRET', ''),
    ])


def _ssl_context():
    """Local controllers use a self-signed cert; skip verification unless
    OMADA_VERIFY_SSL is enabled. Returns None to use the default (verified)."""
    if getattr(settings, 'OMADA_VERIFY_SSL', False):
        return None
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    return ctx


def _request(url, method='GET', data=None, headers=None, timeout=15):
    body = json.dumps(data).encode('utf-8') if data is not None else None
    req = urllib.request.Request(
        url, data=body, method=method,
        headers={'Content-Type': 'application/json', **(headers or {})},
    )
    with urllib.request.urlopen(req, timeout=timeout, context=_ssl_context()) as resp:
        return json.loads(resp.read().decode('utf-8'))


def get_access_token():
    base = settings.OMADA_BASE_URL.rstrip('/')
    url = f"{base}/openapi/authorize/token?grant_type=client_credentials"
    payload = {
        'omadacId': settings.OMADA_OMADAC_ID,
        'client_id': settings.OMADA_CLIENT_ID,
        'client_secret': settings.OMADA_CLIENT_SECRET,
    }
    resp = _request(url, method='POST', data=payload)
    if resp.get('errorCode') not in (0, '0'):
        raise OmadaError(f"[{resp.get('errorCode')}] {resp.get('msg') or 'Omada authentication failed.'}")
    token = (resp.get('result') or {}).get('accessToken')
    if not token:
        raise OmadaError('Omada did not return an access token.')
    return token


def _api_get(path, token, params=None):
    base = settings.OMADA_BASE_URL.rstrip('/')
    qs = ('?' + urllib.parse.urlencode(params)) if params else ''
    url = f"{base}/openapi/v1/{settings.OMADA_OMADAC_ID}{path}{qs}"
    return _request(url, headers={'Authorization': f'AccessToken={token}'})


def _total_rows(path, token):
    """Total count for a paginated endpoint (asks for a single row)."""
    try:
        resp = _api_get(path, token, {'page': 1, 'pageSize': 1})
        return (resp.get('result') or {}).get('totalRows')
    except Exception:
        logger.exception("Omada count failed for %s", path)
        return None


def site_overview():
    """One row per site: name, device count and connected-client count.

    Raises OmadaError on auth/connectivity problems so the view can show a
    friendly message. Per-site counts degrade to None on individual failures.
    """
    try:
        token = get_access_token()
        sites_resp = _api_get('/sites', token, {'page': 1, 'pageSize': 100})
    except OmadaError:
        raise
    except Exception as exc:
        logger.exception("Omada site_overview failed")
        raise OmadaError(str(exc))

    sites = (sites_resp.get('result') or {}).get('data') or []
    rows = []
    for s in sites:
        site_id = s.get('siteId') or s.get('id') or ''
        rows.append({
            'site': s.get('name') or site_id,
            'devices': _total_rows(f'/sites/{site_id}/devices', token),
            'clients': _total_rows(f'/sites/{site_id}/clients', token),
        })
    return rows
