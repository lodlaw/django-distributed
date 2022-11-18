import random

from django.conf import settings


class DistributedRouter:

    def db_for_read(self, model, **hints):
        if self.is_recently_updated(model):
            return self.leader_db

        return self.follower_db

    def db_for_write(self, model, **hints):
        return self.leader_db

    def is_recently_updated(self, model):
        raise NotImplementedError()

    @property
    def follower_db(self):
        if settings.REPLICA_DATABASES:
            return random.choice(settings.REPLICA_DATABASES)

        return 'replica'

    @property
    def leader_db(self):
        if settings.LEADER_DATABASE:
            return settings.LEADER_DATABASE

        return 'default'

    def allow_relation(self):
        """ Whether to enable relations cross database """
        return True
