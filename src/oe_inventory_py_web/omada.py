"""Minimal client for the TP-Link Omada Open API (Cloud-Based Controller).

Uses the OAuth2 *client credentials* grant to obtain an access token and then
queries the controller. Credentials come from the environment (never hardcoded)
— see settings.OMADA_*. Standard library only (urllib), matching the project's
no-extra-dependency style.

Docs: the controller exposes the Open API once an application is created under
Settings -> Platform Integration -> Open API (gives a Client ID / Secret).
"""

import collections
import json
import logging
import ssl
import urllib.parse
import urllib.request

from django.conf import settings

logger = logging.getLogger(__name__)

# Omada device status: 1 = CONNECTED (online). Anything else (0 disconnected,
# pending, isolated…) counts as offline. Kept as a set so it's easy to widen if
# a controller reports other "connected" sub-states.
_ONLINE_STATUS = {1}


class OmadaError(Exception):
    """Raised when the Omada API can't be reached or returns an error."""


def _primary_creds():
    """Credentials for the first/legacy controller, from settings.OMADA_*."""
    return {
        'base_url': getattr(settings, 'OMADA_BASE_URL', ''),
        'omadac_id': getattr(settings, 'OMADA_OMADAC_ID', ''),
        'client_id': getattr(settings, 'OMADA_CLIENT_ID', ''),
        'client_secret': getattr(settings, 'OMADA_CLIENT_SECRET', ''),
        'verify_ssl': getattr(settings, 'OMADA_VERIFY_SSL', False),
    }


def controllers():
    """All configured Omada controllers (one creds dict each). Defined in
    settings.OMADA_CONTROLLERS (built from OMADA_*, OMADA_*2, …); falls back to
    the single primary controller for backward compatibility."""
    configured = getattr(settings, 'OMADA_CONTROLLERS', None)
    if configured:
        return list(configured)
    c = _primary_creds()
    return [c] if omada_configured() else []


def omada_configured():
    """True when the primary controller's credentials/URL are all set."""
    c = _primary_creds()
    return all([c['base_url'], c['omadac_id'], c['client_id'], c['client_secret']])


def _ssl_context(creds):
    """Controllers use a self-signed cert; skip verification unless the creds
    enable it. Returns None to use the default (verified) context."""
    if creds.get('verify_ssl'):
        return None
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    return ctx


def _request(url, creds, method='GET', data=None, headers=None, timeout=15):
    body = json.dumps(data).encode('utf-8') if data is not None else None
    req = urllib.request.Request(
        url, data=body, method=method,
        headers={'Content-Type': 'application/json', **(headers or {})},
    )
    with urllib.request.urlopen(req, timeout=timeout, context=_ssl_context(creds)) as resp:
        return json.loads(resp.read().decode('utf-8'))


def get_access_token(creds):
    base = creds['base_url'].rstrip('/')
    url = f"{base}/openapi/authorize/token?grant_type=client_credentials"
    payload = {
        'omadacId': creds['omadac_id'],
        'client_id': creds['client_id'],
        'client_secret': creds['client_secret'],
    }
    resp = _request(url, creds, method='POST', data=payload)
    if resp.get('errorCode') not in (0, '0'):
        raise OmadaError(f"[{resp.get('errorCode')}] {resp.get('msg') or 'Omada authentication failed.'}")
    token = (resp.get('result') or {}).get('accessToken')
    if not token:
        raise OmadaError('Omada did not return an access token.')
    return token


def _api_get(path, token, creds, params=None):
    base = creds['base_url'].rstrip('/')
    qs = ('?' + urllib.parse.urlencode(params)) if params else ''
    url = f"{base}/openapi/v1/{creds['omadac_id']}{path}{qs}"
    return _request(url, creds, headers={'Authorization': f'AccessToken={token}'})


def _total_rows(path, token, creds):
    """Total count for a paginated endpoint (asks for a single row)."""
    try:
        resp = _api_get(path, token, creds, {'page': 1, 'pageSize': 1})
        return (resp.get('result') or {}).get('totalRows')
    except Exception:
        logger.exception("Omada count failed for %s", path)
        return None


def site_overview(creds=None):
    """One row per site: name, device count and connected-client count.

    Raises OmadaError on auth/connectivity problems so the view can show a
    friendly message. Per-site counts degrade to None on individual failures.
    """
    creds = creds or _primary_creds()
    try:
        token = get_access_token(creds)
        sites_resp = _api_get('/sites', token, creds, {'page': 1, 'pageSize': 100})
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
            'devices': _total_rows(f'/sites/{site_id}/devices', token, creds),
            'clients': _total_rows(f'/sites/{site_id}/clients', token, creds),
        })
    return rows


def _norm_mac(mac):
    return (mac or '').upper().replace(':', '-').strip()


def _all_rows(path, token, creds, page_size=100):
    """Walk a paginated Open API listing and return (all_rows, total)."""
    rows, page, total = [], 1, None
    while True:
        resp = _api_get(path, token, creds, {'page': page, 'pageSize': page_size})
        result = resp.get('result') or {}
        data = result.get('data') or []
        if total is None:
            total = result.get('totalRows')
        rows.extend(data)
        if len(data) < page_size or (total is not None and len(rows) >= total):
            break
        page += 1
    return rows, (total if total is not None else len(rows))


def _firmware_outdated(token, site_id, mac, creds):
    """Whether a device has a newer firmware available, via the Open API
    ``latest-firmware-info`` (``lastFwVer`` differs from ``curFwVer``). Returns
    ``(outdated, current, latest)``; any error/odd response -> (False, '', '')."""
    try:
        resp = _api_get(f'/sites/{site_id}/devices/{mac}/latest-firmware-info', token, creds)
        if resp.get('errorCode') not in (0, '0'):
            return False, '', ''
        r = resp.get('result') or {}
        cur, last = r.get('curFwVer') or '', r.get('lastFwVer') or ''
        return (bool(last) and last != cur), cur, last
    except Exception:
        return False, '', ''


def site_details(creds=None):
    """Per Omada site, the figures needed to fold into the Net Overview cards:

    ``{name, site_id, switches{total,online,offline,outdated}, aps{...},
       clients{total,wifi,wired}, offline_devices[], outdated_devices[],
       topology{switches[],aps[]}}``

    Online = device status in ``_ONLINE_STATUS``. Per-node client counts in the
    topology are the wired clients on each switch (by ``switchMac``) and the
    wireless clients on each AP (by ``apMac``). Raises OmadaError on
    auth/connectivity problems."""
    creds = creds or _primary_creds()
    try:
        token = get_access_token(creds)
        sites_resp = _api_get('/sites', token, creds, {'page': 1, 'pageSize': 100})
    except OmadaError:
        raise
    except Exception as exc:
        logger.exception("Omada site_details failed")
        raise OmadaError(str(exc))

    sites = (sites_resp.get('result') or {}).get('data') or []
    out = []
    for s in sites:
        site_id = s.get('siteId') or s.get('id') or ''
        name = s.get('name') or site_id
        devices, _ = _all_rows(f'/sites/{site_id}/devices', token, creds)
        clients, total_clients = _all_rows(f'/sites/{site_id}/clients', token, creds)

        # Firmware status is a per-device call (latest-firmware-info); cache the
        # "newer firmware available" verdict and the version detail by MAC.
        firmware = {}
        for d in devices:
            mac = d.get('mac')
            if not mac:
                continue
            outdated, cur, last = _firmware_outdated(token, site_id, mac, creds)
            firmware[_norm_mac(mac)] = {'outdated': outdated, 'cur': cur, 'last': last}

        def is_outdated(d):
            return firmware.get(_norm_mac(d.get('mac')), {}).get('outdated', False)

        wifi = sum(1 for c in clients if c.get('wireless'))
        wired = sum(1 for c in clients if not c.get('wireless'))
        # Per-device client counts: wired clients by their switch MAC, wireless
        # clients by the AP MAC they're associated with (both exposed per client).
        wired_by_switch = collections.Counter(
            _norm_mac(c.get('switchMac')) for c in clients
            if not c.get('wireless') and c.get('switchMac'))
        wireless_by_ap = collections.Counter(
            _norm_mac(c.get('apMac')) for c in clients
            if c.get('wireless') and c.get('apMac'))

        def is_online(d):
            return d.get('status') in _ONLINE_STATUS

        def family(kind):
            items = [d for d in devices if d.get('type') == kind]
            on = sum(1 for d in items if is_online(d))
            od = sum(1 for d in items if is_outdated(d))
            return {'total': len(items), 'online': on,
                    'offline': len(items) - on, 'outdated': od}, items

        sw_stats, sw_items = family('switch')
        ap_stats, ap_items = family('ap')

        offline_devices = [{
            'name': d.get('name') or d.get('mac') or '?',
            'type': (d.get('type') or '').upper(),
            'model': d.get('model') or '',
            'mac': d.get('mac') or '',
            'issue': 'Offline',
            'detail': '',
        } for d in devices if not is_online(d)]

        outdated_devices = [{
            'name': d.get('name') or d.get('mac') or '?',
            'type': (d.get('type') or '').upper(),
            'model': d.get('model') or '',
            'mac': d.get('mac') or '',
            'issue': 'Outdated firmware',
            'detail': '{} → {}'.format(
                firmware.get(_norm_mac(d.get('mac')), {}).get('cur') or '?',
                firmware.get(_norm_mac(d.get('mac')), {}).get('last') or '?'),
        } for d in devices if is_outdated(d)]

        def topo_entry(d, clients_n):
            # CPU/memory utilisation per device (only meaningful while online),
            # same shape the map uses for Nebula firewalls: {label, value%}.
            metrics = []
            if is_online(d):
                cpu, mem = d.get('cpuUtil'), d.get('memUtil')
                if cpu is not None:
                    metrics.append({'label': 'CPU', 'value': round(cpu)})
                if mem is not None:
                    metrics.append({'label': 'Memory', 'value': round(mem)})
            return {
                'name': d.get('name') or d.get('mac') or '?',
                'model': d.get('model') or '',
                'online': is_online(d),
                'clients': clients_n,
                'metrics': metrics,
                'outdated': is_outdated(d),
            }

        topo_switches = sorted(
            [topo_entry(d, wired_by_switch.get(_norm_mac(d.get('mac')), 0)) for d in sw_items],
            key=lambda x: x['name'])
        topo_aps = sorted(
            [topo_entry(d, wireless_by_ap.get(_norm_mac(d.get('mac')), 0)) for d in ap_items],
            key=lambda x: x['name'])

        out.append({
            'name': name,
            'site_id': site_id,
            'switches': sw_stats,
            'aps': ap_stats,
            'clients': {'total': total_clients, 'wifi': wifi, 'wired': wired},
            'offline_devices': offline_devices,
            'outdated_devices': outdated_devices,
            'topology': {'switches': topo_switches, 'aps': topo_aps},
        })
    return out
