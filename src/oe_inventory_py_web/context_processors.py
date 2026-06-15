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


def mdi_status_counters(request):
    # If the user is not logged in, skip the calculation.
    if not request.user.is_authenticated:
        return {}

    total_orders = 0
    total_cards = 0

    with connection.cursor() as cursor:
        try:
            # 1. Pending orders: not processed and not cancelled.
            cursor.execute("SELECT count(*) FROM oees_orders WHERE tramitado = 0 AND cancelado = 0")
            total_orders = cursor.fetchone()[0]

            # 2. Pending access cards (staff + visitors) whose state is PENDING.
            #    The PENDING state id is looked up by description, not hardcoded.
            cursor.execute(
                "SELECT id_state FROM oees_access_cards_states WHERE UPPER(TRIM(description)) = 'PENDING'")
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

    # Count online users from the persisted sessions, but always include the
    # user making this request: they are online by definition, and their own
    # `last_activity` stamp isn't flushed to the DB until this response ends, so
    # without this they'd see "0" on their own footer until the next page load.
    ids = online_user_ids()
    ids.add(str(request.user.pk))

    # Whatever is returned here is available in ALL HTML templates.
    return {
        'total_orders': total_orders,
        'total_cards': total_cards,
        'online_users': len(ids),
    }
