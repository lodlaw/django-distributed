from django.conf import settings

from django_distributed.distributed_router import DistributedRouter
from crum import get_current_request
from datetime import datetime
from django.core.cache import cache

KEY_PREFIX = 'django_distributed.distributed_router.'


class CachedRouter(DistributedRouter):

    def db_for_write(self, model, **hints):
        if model not in settings.IGNORED_REPLICA_MODELS:
            self.update_cache(model)

        super().db_for_write(model, **hints)

    def update_cache(self, model):
        cache_key = self.get_cache_key(model)
        if cache_key:
            cache.set(cache_key, datetime.utcnow())

    def is_recently_updated(self, model):
        if model in settings.IGNORED_REPLICA_MODELS:
            return False

        cache_key = self.get_cache_key(model)
        if cache_key:
            time_before = cache.get(cache_key)
            if time_before and (datetime.utcnow() - time_before).total_seconds() < settings.MULTIDB_PINNING_SECONDS:
                return True

        return False

    def get_cache_key(self, model):
        raise NotImplementedError()


class SessionCachedRouter(CachedRouter):
    cache_key_prefix = KEY_PREFIX

    def get_cache_key(self, model):
        request = get_current_request()

        if request and request.session:
            return self.cache_key_prefix + str(request.session.session_key) + '_' + model.__name__

        return None
