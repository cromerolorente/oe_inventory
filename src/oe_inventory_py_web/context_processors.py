import logging
import time

from django.contrib.sessions.models import Session
from django.db import connection
from django.utils import timezone

from .middleware import ACTIVE_USER_WINDOW_SECONDS

logger = logging.getLogger(__name__)


def online_user_ids(window_seconds=ACTIVE_USER_WINDOW_SECONDS):
    """Set of user ids with activity in the last `window_seconds`.

    Scans non-expired sessions for the `last_activity` stamp written by
    TrackActiveUserMiddleware and returns the unique authenticated user ids.
    """
    cutoff = time.time() - window_seconds
    active_user_ids = set()
    try:
        sessions = Session.objects.filter(expire_date__gte=timezone.now())
        for session in sessions.iterator():
            data = session.get_decoded()
            user_id = data.get('_auth_user_id')
            last_activity = data.get('last_activity')
            if user_id and last_activity and last_activity >= cutoff:
                active_user_ids.add(user_id)
    except Exception:
        logger.exception("Error scanning online users")
    return active_user_ids


def count_online_users(window_seconds=ACTIVE_USER_WINDOW_SECONDS):
    """Number of distinct users with activity in the last `window_seconds`."""
    return len(online_user_ids(window_seconds))


# Maps each screen (URL name) to the manual anchor that explains it, so the
# navbar help button can deep-link straight to the relevant chapter.
MANUAL_ANCHORS = {
    'login': 'login',
    'mdi_home': 'home',
    'frm_staff': 'staff',
    'frm_allocations': 'allocations',
    'frm_incorporations': 'incorporations',
    'frm_devices': 'devices',
    'frm_licenses': 'licenses',
    'frm_phones': 'phones',
    'frm_mobile_lines': 'mobile-lines',
    'frm_fiber': 'fiber-lines',
    'frm_printers': 'printers',
    'frm_access_cards': 'access-cards',
    'frm_visitor_cards': 'visitor-cards',
    'frm_access_keys': 'access-keys',
    'frm_orders': 'orders',
    'frm_availability': 'availability',
    'frm_under_repair': 'under-repair',
    'frm_dist_invoices': 'distribution-invoices',
    'frm_net_overview': 'net-overview',
    'frm_remote_machines': 'remote-machines',
    'frm_video_rooms': 'video-rooms',
    'frm_delegations': 'delegations',
    'frm_users': 'users',
    'frm_password_change': 'password-change',
}


def manual_help(request):
    """Expose the manual anchor for the current screen (for the help button)."""
    match = getattr(request, 'resolver_match', None)
    url_name = match.url_name if match else None
    return {'manual_anchor': MANUAL_ANCHORS.get(url_name, '')}


def pending_counts():
    """(total_orders, total_cards): pending orders and pending access cards.

    Shared by the page context processor and the footer-refresh API endpoint so
    both report identical figures.
    """
    total_orders = 0
    total_cards = 0

    with connection.cursor() as cursor:
        try:
            # 1. Pending orders: not processed and not cancelled.
            cursor.execute("SELECT count(*) FROM oees_orders WHERE tramitado = 0 AND cancelado = 0")
            total_orders = cursor.fetchone()[0]

            # 2. Pending access cards (staff + visitors). There can be several
            #    "pending" states (e.g. "PENDING ACTIVATION"), so we match any
            #    state whose description contains the word PENDING, by id.
            cursor.execute(
                "SELECT id_state FROM oees_access_cards_states WHERE UPPER(TRIM(description)) LIKE '%PENDING%'")
            pending_ids = [r[0] for r in cursor.fetchall()]
            if pending_ids:
                ph = ",".join(["%s"] * len(pending_ids))
                cursor.execute(
                    f"SELECT count(*) FROM oees_access_cards WHERE state_card IN ({ph})", pending_ids)
                total_cards = cursor.fetchone()[0]
                cursor.execute(
                    f"SELECT count(*) FROM oees_access_cards_visitors WHERE state_card IN ({ph})", pending_ids)
                total_cards += cursor.fetchone()[0]
        except Exception:
            logger.exception("Error computing MDI status counters")

    return total_orders, total_cards


def mdi_status_counters(request):
    # If the user is not logged in, skip the calculation.
    if not request.user.is_authenticated:
        return {}

    # Pending orders/cards and network alerts come from a background-refreshed
    # cache, so navigating between forms never waits on these (the network
    # alerts figure in particular calls the slow Nebula API). See status_cache.
    from . import status_cache
    status = status_cache.get_status()

    # Count online users from the persisted sessions, but always include the
    # user making this request: they are online by definition, and their own
    # `last_activity` stamp isn't flushed to the DB until this response ends, so
    # without this they'd see "0" on their own footer until the next page load.
    ids = online_user_ids()
    ids.add(str(request.user.pk))

    # Whatever is returned here is available in ALL HTML templates.
    return {
        'total_orders': status.get('total_orders') or 0,
        'total_cards': status.get('total_cards') or 0,
        'net_alerts': status.get('net_alerts'),
        'anydesk_alerts': status.get('anydesk_alerts'),
        'video_rooms_alerts': status.get('video_rooms_alerts'),
        'online_users': len(ids),
        'last_update': status_cache.last_update_str(),
    }
