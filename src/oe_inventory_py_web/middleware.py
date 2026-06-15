"""Custom middleware for the OE Inventory app."""

import time

from django.contrib import messages
from django.shortcuts import redirect

# How recently a user must have made a request to be counted as "online".
ACTIVE_USER_WINDOW_SECONDS = 5 * 60
# Don't rewrite the session on every single request: refresh the timestamp at
# most once per this interval to keep the per-request DB write off the hot path.
_ACTIVE_USER_THROTTLE_SECONDS = 60


class TrackActiveUserMiddleware:
    """Stamp the current time on the session so we can count online users.

    We store a `last_activity` epoch on each authenticated user's session. The
    session backend is the database (`django_session`), so the stamp is shared
    across all gunicorn workers — unlike the per-process local-memory cache.
    Counting online users is then a matter of scanning non-expired sessions for
    a recent `last_activity` (see context_processors.count_online_users).
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = getattr(request, 'user', None)
        if user is not None and user.is_authenticated:
            now = time.time()
            last = request.session.get('last_activity', 0)
            if now - last > _ACTIVE_USER_THROTTLE_SECONDS:
                request.session['last_activity'] = now
        return self.get_response(request)


class BlockReaderExportMiddleware:
    """Readers can view data but must not download the Excel exports.

    Every screen triggers its export with a GET `?export=excel` request, so this
    is a single enforcement point that blocks the download for users with a
    reader profile, regardless of which form it came from. It complements the
    CSS that hides the export buttons for readers in the UI.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # The `export` GET param is only ever used to trigger a download
        # (export=excel on most screens, export=incidences on Fiber Lines), so
        # any value of it is blocked for readers.
        if request.method == 'GET' and request.GET.get('export'):
            user = getattr(request, 'user', None)
            if user is not None and user.is_authenticated and getattr(user, 'reader', 0) == 1:
                messages.error(request, "You have a reader profile and can't download Excel files.")
                # Redirect back to the same screen without the export parameter,
                # preserving any other query string (filters, tab, etc.).
                params = request.GET.copy()
                params.pop('export', None)
                qs = params.urlencode()
                return redirect(f"{request.path}?{qs}" if qs else request.path)
        return self.get_response(request)
