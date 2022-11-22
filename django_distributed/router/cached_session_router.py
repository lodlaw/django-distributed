from datetime import datetime

from crum import get_current_request
from django.conf import settings
from django.core.cache import cache

from django_distributed.router.distributed_router import DistributedRouter

KEY_PREFIX = 'django_distributed.distributed_router.'


class CachedRouter(DistributedRouter):
    """ A base database router that uses caching strategy """

    def update_cache(self, model):
        """ Updates the cache store based on a cache key and current date """
        cache_key = self.get_cache_key(model)
        if cache_key:
            cache.set(cache_key, datetime.utcnow())

    def is_recently_updated(self, model):
        """ Returns true if the cache store is recently updated based on a key, else false """
        cache_key = self.get_cache_key(model)

        if cache_key:
            time_before = cache.get(cache_key)
            if time_before and (datetime.utcnow() - time_before).total_seconds() < settings.REPLICATION_LAG:
                return True

    def get_cache_key(self, model):
        """" Gets the cache key from a model """
        raise NotImplementedError()


class SessionCachedRouter(CachedRouter):
    """ A router for distributed database using the caching strategy with user session """
    cache_key_prefix = KEY_PREFIX

    def get_cache_key(self, model):
        """ Gets the cache key based on user session and model """
        request = get_current_request()

        if request and request.session:
            return self.cache_key_prefix + str(request.session.session_key) + '_' + model.__name__
