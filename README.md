# django-distributed
A multi database setup for Django.

Tested with www.lodlaw.com, our setup consists of:
- one write database based in Australia corresponding to an Australian cluser
- one read database based in Europe corresponding to an European cluster

## Installing
`pip install django-distributed`

## Requirements

### Required configs
In `settings.py` of Django, you need to define the following variables for the follower configuration:

| Variable         | Type      | Description                                                   |
|------------------|-----------|---------------------------------------------------------------|
| `LEADER_DATABASE`  | str       | The name of the leader database (i.e. `default`)                |
| `FOLLOWER_DATABASES` | list[str] | A list of follower databases (i.e. `['replica1', 'replica2']`) |
| `REPLICATION_LAG`  | number    | The replication lag in seconds between the read and write instances. |

#### Database router
In addition, you need to use our custom `DistributedRouter` database router. In `settings.py`, add in:

```py
DATABASE_ROUTERS = ('django_distributed.SessionCachedRouter',)
MIDDLEWARE = ('crum.CurrentRequestUserMiddleware',) + MIDDLEWARE
```

##### Customize database router
Our database router is session-based. It means that we decide to which database to read from or write to based on the user session.

However, if you want to use another session back end, you have two options with our setup:

1. Extend the class `CachedRouter` and implement the method `get_cache_key`. Define your custom cache key there; or
2. Extend the class `DistributedRouter` and implement the method `is_recently_updated`. Our distributed router logic will read from the write database if it is recently updated else replica database.

### Optional configs

If you want to use our own session engine, you can do so by specifying in `settings.py`

```py
SESSION_ENGINE = 'django_distributed.session_engine'
```

#### Session engine explanation
This session engine is using both cache store and database store. 

Because replication is not fast enough, a session written in the leader database will not appear in the replicas right away. Hence the user might get kicked out after logging in because the session is there in the read replica. Of course, we could do R/W all on the master database, but it would be slow as our R and W databases are located far away from each other.

Hence we have created this session engine, it will first add the session to the cache first, in our case, memcached. Then it will update the database. Same for reading session, cache store goes first then database store. Nevertheless, what is different here from the Django `cached_db` is the write operation, it is offloaded to another thread.

