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
        return 'replica'

    @property
    def leader_db(self):
        return 'default'

    def allow_relation(self):
        """ Whether to enable relations cross database """
        return True
