import random

from django.conf import settings


class DistributedRouter:
    """ A base router for a distributed set-up """

    def db_for_read(self, model, **hints):
        # if the model is recently been updated then return the leader database, else return follower database
        if self.is_recently_updated(model):
            return self.leader_db

        return self.follower_db

    def db_for_write(self, model, **hints):
        # always return the leader database for write
        return self.leader_db

    def is_recently_updated(self, model):
        # to be implemented in base class
        raise NotImplementedError()

    @property
    def follower_db(self):
        """ Gets a random read database from the list, if not provided, return a default """
        if settings.REPLICA_DATABASES:
            return random.choice(settings.REPLICA_DATABASES)

        return 'replica'

    @property
    def leader_db(self):
        """ Gets a leader database from settings, if not provided, return default """
        if settings.LEADER_DATABASE:
            return settings.LEADER_DATABASE

        return 'default'

    def allow_relation(self):
        """ Whether to enable relations cross database """
        return True
