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

from django.conf import settings
from django.core.cache import cache

logger = logging.getLogger(__name__)

DATA_KEY = 'mdi_status_data'
TS_KEY = 'mdi_status_ts'
LOCK_KEY = 'mdi_status_lock'

# Returned while the first background compute is still running (cold start).
PLACEHOLDER = {'total_orders': 0, 'total_cards': 0, 'net_alerts': None}


def _refresh_seconds():
    return getattr(settings, 'MDI_STATUS_REFRESH_SECONDS', 300)


def _store(data):
    cache.set(DATA_KEY, data, None)
    cache.set(TS_KEY, time.time(), None)


def compute_and_store():
    """Recompute the counters and store them in the cache. Returns the data.

    The cheap DB counts (pending orders/cards) are published first so the footer
    isn't stuck at zero during the slow Nebula call on a cold start; the network
    alerts figure is filled in once Nebula responds."""
    from .context_processors import pending_counts
    from . import nebula

    prev = cache.get(DATA_KEY) or {}
    total_orders, total_cards = pending_counts()

    # Publish the cheap counts straight away (keep any known alerts figure).
    data = {'total_orders': total_orders, 'total_cards': total_cards,
            'net_alerts': prev.get('net_alerts')}
    _store(data)

    if nebula.nebula_configured():
        net_alerts = prev.get('net_alerts')  # keep last known if Nebula fails
        try:
            net_alerts = sum(int(r.get('alerts') or 0) for r in nebula.site_overview())
        except Exception:
            logger.exception("Net alerts background compute failed")
        data = {'total_orders': total_orders, 'total_cards': total_cards, 'net_alerts': net_alerts}
    else:
        data = {'total_orders': total_orders, 'total_cards': total_cards, 'net_alerts': None}

    _store(data)
    return data


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
