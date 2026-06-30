"""Client for the Zyxel Nebula OpenAPI (https://api.nebula.zyxel.com).

Auth is a single API key sent in the `X-ZyxelNebula-API-Key` header (no token
exchange). Credentials come from the environment — see settings.NEBULA_*.
Standard library only (urllib).

Per site we build a small dashboard: switch/AP counts (online/offline), client
counts (wifi vs wired) and an "alerts" figure (offline devices).
"""

import collections
import json
import logging
import re
import ssl
import urllib.parse
import urllib.request

from django.conf import settings

logger = logging.getLogger(__name__)


class NebulaError(Exception):
    """Raised when the Nebula API can't be reached or returns an error."""


def nebula_configured():
    # Org id is optional: if omitted we discover the organizations from the key.
    return bool(getattr(settings, 'NEBULA_BASE_URL', '')) and bool(getattr(settings, 'NEBULA_API_KEY', ''))


def _ssl_context():
    if getattr(settings, 'NEBULA_VERIFY_SSL', True):
        return None
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    return ctx


def _request(path, method='GET', body=None):
    url = settings.NEBULA_BASE_URL.rstrip('/') + path
    data = json.dumps(body).encode('utf-8') if body is not None else None
    req = urllib.request.Request(url, data=data, method=method, headers={
        'X-ZyxelNebula-API-Key': settings.NEBULA_API_KEY,
        'Content-Type': 'application/json',
    })
    with urllib.request.urlopen(req, timeout=20, context=_ssl_context()) as resp:
        raw = resp.read().decode('utf-8')
    return json.loads(raw) if raw else None


def _q(value):
    return urllib.parse.quote(str(value))


def _org_ids():
    """The configured org, or all organizations reachable with the key."""
    if getattr(settings, 'NEBULA_ORG_ID', ''):
        return [settings.NEBULA_ORG_ID]
    orgs = _request('/v1/nebula/organizations') or []
    return [o['orgId'] for o in orgs if isinstance(o, dict) and o.get('orgId')]


def _devices_by_site(org_id):
    """Map siteId -> list of devices (each with type AP/SW/GW...)."""
    result = {}
    data = _request(f'/v1/nebula/organizations/{_q(org_id)}/sites/devices') or []
    for entry in data:
        if entry and entry.get('siteId'):
            result[entry['siteId']] = entry.get('devices') or []
    return result


def _online_map(site_id):
    """Map devId -> True/False (online) for a site."""
    statuses = _request(f'/v1/nebula/{_q(site_id)}/online-status') or []
    return {s['devId']: (s.get('currentStatus') == 'ONLINE')
            for s in statuses if isinstance(s, dict) and s.get('devId')}


def _firmware_status(site_id):
    """Map devId -> firmware info {'status', 'current', 'latest'} for a site.
    `status` is one of N/A, UP_TO_DATE, NOT_UP_TO_DATE, DEDICATED."""
    data = _request(f'/v1/nebula/{_q(site_id)}/firmware-status') or []
    result = {}
    for d in data:
        if isinstance(d, dict) and d.get('devId'):
            result[d['devId']] = {
                'status': d.get('status'),
                'current': d.get('currentVersion'),
                'latest': d.get('latestVersion'),
            }
    return result


def _online_clients(site_id):
    """List of clients that are ONLINE right now (each with its `connectedTo`
    device id). Returns None if the endpoint is unavailable.

    The clients endpoint reports over a period (min 2h), so each client carries
    a `status` of ONLINE/OFFLINE; we keep only the ONLINE ones.
    """
    try:
        body = {'period': '2h',
                'featrues': ['mac_address', 'status', 'connected_device_id']}
        resp = _request(f'/v2/nebula/{_q(site_id)}/clients', method='POST', body=body)
    except Exception:
        logger.warning("Nebula clients unavailable for site %s", site_id)
        return None
    rows = resp.get('data') if isinstance(resp, dict) else resp
    return [c for c in (rows or [])
            if isinstance(c, dict) and c.get('status') == 'ONLINE']


def _client_counts(online_clients, devices_by_id):
    """Aggregate online-client counts, by distinct device (MAC), split wifi vs
    wired by the device each one is connected to (AP -> wifi, else wired).

    Deduplicated per equipment: a device with several connections of the same
    type counts once for that type; one with both a wireless and a wired
    connection counts once in each (so wifi + wired may exceed total, which is
    the number of distinct devices). ``online_clients`` is the list from
    `_online_clients` (None when unavailable -> unknown counts)."""
    if online_clients is None:
        return {'wifi': None, 'wired': None, 'total': None}
    wifi_macs, wired_macs, all_macs = set(), set(), set()
    for c in online_clients:
        mac = c.get('macAddress') or c.get('mac') or c.get('connectedTo')
        all_macs.add(mac)
        dev = devices_by_id.get(c.get('connectedTo'))
        if (dev or {}).get('type') == 'AP':
            wifi_macs.add(mac)
        else:
            wired_macs.add(mac)
    return {'wifi': len(wifi_macs), 'wired': len(wired_macs), 'total': len(all_macs)}


def _build_topology(site_name, devices, online, online_clients, gw_metrics=None,
                    outdated_ids=frozenset()):
    """A tiered map of the site: gateways/firewalls -> switches -> access points.
    Each node carries name, model, online state, the number of clients connected
    to it right now and (for firewalls) CPU/memory usage metrics.

    Note: the Nebula OpenAPI only exposes CPU/memory for gateways/firewalls
    (system-status); it has no equivalent for switches or AP channel utilisation,
    so those nodes carry no metrics."""
    gw_metrics = gw_metrics or {}
    # Distinct devices (MACs) connected to each network device.
    per_dev = collections.defaultdict(set)
    for c in (online_clients or []):
        mac = c.get('macAddress') or c.get('mac') or id(c)
        per_dev[c.get('connectedTo')].add(mac)

    def entry(d, metrics=None):
        return {
            'name': d.get('name') or d.get('mac') or '?',
            'model': d.get('model') or '',
            'online': bool(online.get(d.get('devId'))),
            'clients': len(per_dev.get(d.get('devId'), ())),
            'metrics': metrics or [],
            'outdated': d.get('devId') in outdated_ids,
        }

    def gw_entry(d):
        m = gw_metrics.get(d.get('devId')) or {}
        metrics = []
        if m.get('cpu') is not None:
            metrics.append({'label': 'CPU', 'value': round(m['cpu'])})
        if m.get('mem') is not None:
            metrics.append({'label': 'Memory', 'value': round(m['mem'])})
        return entry(d, metrics)

    gateways = sorted([gw_entry(d) for d in devices if d and d.get('type') in FIREWALL_TYPES],
                      key=lambda x: x['name'])
    switches = sorted([entry(d) for d in devices if d and d.get('type') == 'SW'],
                      key=lambda x: x['name'])
    aps = sorted([entry(d) for d in devices if d and d.get('type') == 'AP'],
                 key=lambda x: x['name'])
    return {'site': site_name, 'gateways': gateways, 'switches': switches, 'aps': aps}


# Types that count as a "firewall" / security gateway in the Nebula data.
FIREWALL_TYPES = {'FIREWALL', 'GW', 'GWH', 'SCR'}


def _device_stats(devices, online, outdated_ids=frozenset()):
    """Counters by device family (incl. how many have outdated firmware) plus
    the list of offline devices for a site."""
    def stat(matches):
        items = [d for d in devices if matches((d or {}).get('type'))]
        total = len(items)
        on = sum(1 for d in items if online.get(d.get('devId')))
        od = sum(1 for d in items if d.get('devId') in outdated_ids)
        return {'total': total, 'online': on, 'offline': total - on, 'outdated': od}

    offline_devices = [
        {
            'name': d.get('name') or d.get('mac') or d.get('devId') or '?',
            'type': d.get('type') or '',
            'model': d.get('model') or '',
            'mac': d.get('mac') or '',
            'issue': 'Offline',
            'detail': '',
        }
        for d in devices if d and not online.get(d.get('devId'))
    ]
    sw = stat(lambda t: t == 'SW')
    ap = stat(lambda t: t == 'AP')
    fw = stat(lambda t: t in FIREWALL_TYPES)
    return sw, ap, fw, offline_devices


def _gateway_wan(site_id, dev_id):
    """WAN summary for one gateway: how many WAN interfaces are enabled, and how
    many are operational (have a live physical link).

    * ``enabled`` comes from interface-settings (the configured WAN interfaces).
    * ``operational`` comes from ports-status (a WAN port with a link speed).
      That endpoint currently returns HTTP 500 on the USG FLEX 700H, so when it
      is unavailable ``operational`` is ``None`` (unknown), distinct from 0.
    """
    enabled = 0
    wan_ifaces = []
    try:
        data = _request(f'/v1/nebula/{_q(site_id)}/gw/{_q(dev_id)}/interface-settings') or {}
        for w in (data.get('wan') or []):
            if w and w.get('enabled'):
                enabled += 1
                if w.get('interface'):
                    wan_ifaces.append(w['interface'])
    except Exception:
        logger.warning("Nebula WAN interface-settings unavailable for gw %s", dev_id)

    operational = None
    try:
        ports = _request(f'/v1/nebula/{_q(site_id)}/gw/{_q(dev_id)}/ports-status') or []
        # WAN interfaces are named like 'ge1'; ports-status keys ports by number.
        wan_nums = {re.sub(r'\D', '', i) for i in wan_ifaces if i}
        up = 0
        for p in ports:
            if not isinstance(p, dict):
                continue
            num = re.sub(r'\D', '', str(p.get('portNumber') or ''))
            speed = str(p.get('linkSpeed') or '').strip().lower()
            if num in wan_nums and speed and speed not in ('down', 'disabled', 'none'):
                up += 1
        operational = up
    except Exception:
        # Expected for the USG FLEX 700H today (endpoint returns 500).
        logger.info("Nebula gateway ports-status unavailable for gw %s", dev_id)

    return {'enabled': enabled, 'operational': operational}


def _gateway_system(site_id, dev_id):
    """CPU and memory usage (%) for a gateway/firewall (system-status), or an
    empty dict if unavailable."""
    try:
        data = _request(f'/v1/nebula/{_q(site_id)}/gw/{_q(dev_id)}/system-status') or {}
        return {'cpu': data.get('cpuUsage'), 'mem': data.get('memUsage')}
    except Exception:
        logger.info("Nebula gateway system-status unavailable for gw %s", dev_id)
        return {}


# CPU/memory usage strictly above this (%) is reported as an alert.
METRIC_ALERT_THRESHOLD = 80


def site_overview():
    """One entry per site with switch/AP/client/alert summaries. Raises
    NebulaError only on auth/connectivity problems; orgs that deny access
    (BASE-mode ones return 403) are skipped, not fatal."""
    try:
        org_ids = _org_ids()
    except Exception as exc:
        logger.exception("Nebula organization discovery failed")
        raise NebulaError(str(exc))

    sites = []
    for org_id in org_ids:
        try:
            site_list = _request(f'/v1/nebula/organizations/{_q(org_id)}/sites') or []
            devices_map = _devices_by_site(org_id)
        except Exception:
            logger.warning("Nebula data unavailable for org %s (skipped)", org_id)
            continue

        for s in site_list:
            if not s:
                continue
            site_id = s.get('siteId') or ''
            devices = devices_map.get(site_id, [])
            by_id = {d.get('devId'): d for d in devices if d}
            try:
                online = _online_map(site_id)
            except Exception:
                online = {}
            try:
                fw_info = _firmware_status(site_id)
            except Exception:
                logger.warning("Nebula firmware-status unavailable for site %s", site_id)
                fw_info = {}
            outdated_ids = {devid for devid, i in fw_info.items()
                            if (i.get('status') == 'NOT_UP_TO_DATE')}

            sw, ap, fw, offline_devices = _device_stats(devices, online, outdated_ids)

            # Outdated-firmware devices are also alerts (with version detail).
            outdated_devices = []
            for devid in outdated_ids:
                d = by_id.get(devid, {})
                info = fw_info.get(devid, {})
                cur, latest = info.get('current') or '?', info.get('latest') or '?'
                outdated_devices.append({
                    'name': d.get('name') or d.get('mac') or devid,
                    'type': d.get('type') or '',
                    'model': d.get('model') or '',
                    'mac': d.get('mac') or '',
                    'issue': 'Outdated firmware',
                    'detail': f'{cur} → {latest}',
                })

            # WAN summary + CPU/memory metrics across the site's gateway(s).
            gw_devices = [d for d in devices
                          if d and (d.get('type') in FIREWALL_TYPES) and d.get('devId')]
            wan_enabled, wan_operational, wan_op_known = 0, 0, False
            gw_metrics = {}
            for gw in gw_devices:
                w = _gateway_wan(site_id, gw['devId'])
                wan_enabled += w['enabled']
                if w['operational'] is not None:
                    wan_operational += w['operational']
                    wan_op_known = True
                gw_metrics[gw['devId']] = _gateway_system(site_id, gw['devId'])
            wan = {'enabled': wan_enabled,
                   'operational': (wan_operational if wan_op_known else None)}

            # A device metric above the threshold (e.g. CPU/memory > 80%) is an alert.
            metric_alerts = []
            for gw in gw_devices:
                d = by_id.get(gw['devId'], {})
                m = gw_metrics.get(gw['devId']) or {}
                for label, val in (('CPU', m.get('cpu')), ('memory', m.get('mem'))):
                    if val is not None and val > METRIC_ALERT_THRESHOLD:
                        metric_alerts.append({
                            'name': d.get('name') or d.get('mac') or gw['devId'],
                            'type': d.get('type') or '',
                            'model': d.get('model') or '',
                            'mac': d.get('mac') or '',
                            'issue': f'High {label} usage',
                            'detail': f'{round(val)}%',
                        })

            online_clients = _online_clients(site_id)
            clients = _client_counts(online_clients, by_id)
            topology = _build_topology(s.get('name') or site_id, devices, online,
                                       online_clients, gw_metrics, outdated_ids)

            # All alerts: offline + outdated-firmware + over-threshold metrics.
            alert_list = offline_devices + outdated_devices + metric_alerts

            sites.append({
                'site': s.get('name') or site_id,
                'wan': wan,
                'switches': sw,
                'aps': ap,
                'firewalls': fw,
                'clients': clients,
                'outdated': len(outdated_devices),
                'alerts': len(alert_list),
                'alert_list': alert_list,
                'topology': topology,
            })
    return sites
