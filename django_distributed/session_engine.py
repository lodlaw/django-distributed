import threading

from django.contrib.sessions.backends.base import UpdateError
from django.contrib.sessions.backends.cached_db import SessionStore as DBStore


class SessionStore(DBStore):

    def save_parallel(self, must_create):
        try:
            super().save(must_create)
        except UpdateError:
            self.flush()
            raise

    def save(self, must_create=False):
        self._cache.set(self.cache_key, self._session, self.get_expiry_age())

        threading.Thread(target=self.save_parallel, args=(must_create,)).start()
