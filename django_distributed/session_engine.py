import threading
import time

from django.contrib.sessions.backends.base import UpdateError
from django.contrib.sessions.backends.cached_db import SessionStore as DBStore


class SessionStore(DBStore):

    def save_parallel(self, must_create):
        MAX_RETRIES = 5
        for i in range(MAX_RETRIES):
            try:
                super().save(must_create)
                break
            except UpdateError:
                if i == MAX_RETRIES - 1:
                    raise UpdateError()
                time.sleep(1)

    def save(self, must_create=False):
        self._cache.set(self.cache_key, self._session, self.get_expiry_age())

        threading.Thread(target=self.save_parallel, args=(must_create,)).start()
