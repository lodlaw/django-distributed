import threading

from django.contrib.sessions.backends.base import UpdateError
from django.contrib.sessions.backends.cached_db import SessionStore as DBStore


class SessionStore(DBStore):
    """ Session store for follower replica """

    def save(self, must_create=False):
        # set the cache first in order to get a session key
        self._cache.set(self.cache_key, self._session, self.get_expiry_age())

        # offload database-session save to another thread
        threading.Thread(target=self._save, args=(must_create,)).start()

    def _save(self, must_create):
        try:
            super().save(must_create)
        except UpdateError:
            # if there is an error, then remove the session then propagate the error
            self.flush()
            raise
