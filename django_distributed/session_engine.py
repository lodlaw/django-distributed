import threading

from django.contrib.sessions.backends.base import UpdateError
from django.contrib.sessions.backends.cached_db import SessionStore as DBStore


class SessionStore(DBStore):
    """ Session store for follower replica """

    def save(self, must_create=False):
        if not self.session_key:
            must_create = True

        # set the cache first in order to get a session key
        self._cache.set(self.cache_key, self._session, self.get_expiry_age())

        # offload database-session save to another thread
        threading.Thread(target=self._save_db, args=(must_create,)).start()

    def _save_db(self, must_create):
        try:
            super().save(must_create)
        except UpdateError:
            # another retry in case the leader database hasn't been updated
            # if there is an error, then remove the session and rethrow the error
            max_retries = 7
            for i in range(max_retries):
                try:
                    super().save(must_create)
                    return
                except UpdateError:
                    pass

                self.flush()
                raise
