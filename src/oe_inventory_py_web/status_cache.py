"""Cached footer status counters (pending orders, pending cards, network
alerts), refreshed in the background.

The footer of every page shows these figures. Computing them on each request
is slow — the network-alerts figure calls the Nebula API (several seconds) —
and made the badge blank out and the app feel sluggish on every navigation.

Instead we compute once and cache the result in-process, then refresh it in a
daemon thread at most every ``MDI_STATUS_REFRESH_SECONDS``. Requests always read
the cached value instantly (stale-while-revalidate): when the cache is missing
or stale a background refresh is kicked off, but the request never waits for it.
"""

import logging
import threading
import time
from datetime import datetime

from django.conf import settings
from django.core.cache import cache
from django.db import connection

logger = logging.getLogger(__name__)

DATA_KEY = 'mdi_status_data'
ROWS_KEY = 'mdi_net_overview_rows'    # full site_overview() result (list) or None
ERR_KEY = 'mdi_net_overview_error'    # error message when the last fetch failed
ANYDESK_STATUS_KEY = 'mdi_anydesk_status'   # code(str) -> online(bool) from last check
TS_KEY = 'mdi_status_ts'
LOCK_KEY = 'mdi_status_lock'

NEBULA_ERROR = ("Could not reach the Nebula API. Check the API key, "
                "organization id and base URL.")

# Returned while the first background compute is still running (cold start).
PLACEHOLDER = {'total_orders': 0, 'total_cards': 0, 'net_alerts': None, 'anydesk_alerts': None}


def _refresh_seconds():
    return getattr(settings, 'MDI_STATUS_REFRESH_SECONDS', 300)


def _store(data):
    cache.set(DATA_KEY, data, None)
    cache.set(TS_KEY, time.time(), None)


def compute_and_store():
    """Recompute the counters (and the full Net Overview rows) and cache them.

    The cheap DB counts (pending orders/cards) are published first so the footer
    isn't stuck at zero during the slow Nebula call on a cold start. The Nebula
    site overview is fetched once and reused both for the alerts figure and for
    the Net Overview screen (served from cache so its AJAX request never waits
    on the slow API and never times out)."""
    from .context_processors import pending_counts
    from . import nebula

    prev = cache.get(DATA_KEY) or {}
    total_orders, total_cards = pending_counts()

    # AnyDesk check first — it's cheap, so its alert count is published before the
    # slow Nebula call below (no waiting for the badge to appear).
    anydesk_alerts, anydesk_status = _anydesk_check(prev)
    cache.set(ANYDESK_STATUS_KEY, anydesk_status, None)

    # Publish the cheap figures straight away (keep any known net_alerts).
    _store({'total_orders': total_orders, 'total_cards': total_cards,
            'net_alerts': prev.get('net_alerts'), 'anydesk_alerts': anydesk_alerts})

    net_alerts = None
    if nebula.nebula_configured():
        net_alerts = prev.get('net_alerts')  # keep last known if Nebula fails
        try:
            rows = nebula.site_overview()
            net_alerts = sum(int(r.get('alerts') or 0) for r in rows)
            cache.set(ROWS_KEY, rows, None)
            cache.set(ERR_KEY, None, None)
        except Exception:
            logger.exception("Nebula site overview background compute failed")
            cache.set(ERR_KEY, NEBULA_ERROR, None)
    else:
        cache.set(ROWS_KEY, None, None)
        cache.set(ERR_KEY, None, None)

    data = {'total_orders': total_orders, 'total_cards': total_cards,
            'net_alerts': net_alerts, 'anydesk_alerts': anydesk_alerts}
    _store(data)
    return data


def _anydesk_check(prev=None):
    """Check the AnyDesk machines in oees_anydesk. Returns ``(alerts, status_map)``
    where alerts is the number of unreachable machines and status_map is
    ``code(str) -> online(bool)``.

    * With the API configured: the real online status; reachable machines get
      their ``last_connection`` stamped.
    * Without a working API (not configured, or the call failed / bad key): a
      fallback where a machine counts as online only if it has a
      ``last_connection`` — so the footer count and the green/red dots still
      reflect the machines and the design can be tuned meanwhile.
    * Returns ``(None, {})`` only when the table itself isn't available.
    """
    from . import anydesk
    prev = prev or {}

    online = None
    if anydesk.anydesk_configured():
        try:
            online = anydesk.online_map()   # one call returns every client's status
        except Exception:
            # API unreachable / bad credentials: fall through to the
            # last_connection fallback so the footer still reflects the machines
            # (otherwise a configured-but-failing key would hide the badge).
            logger.warning("AnyDesk background check failed; using last_connection fallback")
            online = None

    from . import anydesk as _ad
    status_map, offline = {}, 0
    now = datetime.now()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM oees_anydesk ORDER BY 1")
            cols = [c[0] for c in cursor.description]
            code_col = _ad.pick_column(cols, 'code')
            lc_col = _ad.pick_column(cols, 'last_connection', prefix='last_conn')
            ci = cols.index(code_col)
            li = cols.index(lc_col) if lc_col else None
            for r in cursor.fetchall():
                key = str(r[ci]).strip()
                last = r[li] if li is not None else None
                if online is not None:               # real check
                    up = bool(online.get(key))
                    if up and lc_col:                # stamp the reachable ones
                        cursor.execute(
                            f"UPDATE oees_anydesk SET {lc_col} = %s WHERE {code_col} = %s",
                            [now, r[ci]])
                else:                                # fallback (no API key yet)
                    up = last is not None
                status_map[key] = up
                if not up:
                    offline += 1
    except Exception:
        logger.warning("oees_anydesk table not available for the AnyDesk check")
        return None, {}
    return offline, status_map


def get_anydesk_status():
    """code(str) -> online(bool) from the last background check ({} if none)."""
    return cache.get(ANYDESK_STATUS_KEY) or {}


def _refresh_locked():
    # Single-flight: only one refresh runs at a time. The lock also has a TTL so
    # a crashed compute can't block refreshes forever.
    if not cache.add(LOCK_KEY, 1, 120):
        return
    try:
        compute_and_store()
    finally:
        cache.delete(LOCK_KEY)


def _trigger_refresh():
    if getattr(settings, 'MDI_STATUS_REFRESH_IN_BACKGROUND', True):
        threading.Thread(target=_refresh_locked, name='mdi-status-refresh', daemon=True).start()
    else:
        # Synchronous path (tests / management): keep it simple and blocking.
        _refresh_locked()


def get_status(trigger=True):
    """Return the cached counters instantly. If the cache is missing or older
    than the refresh cadence, kick off a background refresh (non-blocking).

    When background refresh is disabled (tests / management commands) it computes
    synchronously so callers always see current data."""
    if not getattr(settings, 'MDI_STATUS_REFRESH_IN_BACKGROUND', True):
        return compute_and_store()

    data = cache.get(DATA_KEY)
    ts = cache.get(TS_KEY) or 0
    if data is None:
        if trigger:
            _trigger_refresh()
        return dict(PLACEHOLDER)
    if trigger and (time.time() - ts) > _refresh_seconds():
        _trigger_refresh()
    return data


def get_net_overview(trigger=True):
    """Return ``(rows, error)`` for the Net Overview screen from the cache.

    * ``rows`` is the cached ``site_overview()`` list when available, else None.
    * ``error`` is a message when the last fetch failed and no rows are cached.
    * ``(None, None)`` means a compute is in flight / not done yet (cold start):
      the caller should tell the client to retry shortly.

    A background refresh is kicked off when the data is missing or stale; the
    request never waits for it. In synchronous mode (tests / management) it
    computes inline so callers always see current data."""
    if not getattr(settings, 'MDI_STATUS_REFRESH_IN_BACKGROUND', True):
        compute_and_store()
        return cache.get(ROWS_KEY), cache.get(ERR_KEY)

    ts = cache.get(TS_KEY) or 0
    if trigger and (ts == 0 or (time.time() - ts) > _refresh_seconds()):
        _trigger_refresh()
    return cache.get(ROWS_KEY), cache.get(ERR_KEY)
