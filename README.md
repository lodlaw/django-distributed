# django-distributed
A multi database setup for Django.

Tested with www.lodlaw.com, our setup consists of:
- one write database based in Australia corresponding to an Australian kubernetes cluser
- one read database based in Europe corresponding to an European kubernetes cluster

## Installing
`pip install django-distributed`

## Requirements

### Required configs
In `settings.py` of Django, you need to define the following variables for the slave configuration:

| Variable         | Type      | Description                                                   |
|------------------|-----------|---------------------------------------------------------------|
| LEADER_DATABASE  | str       | The name of the leader database (i.e. `default`)                |
| FOLLOWER_DATABASES | list[str] | A list of follower databases (i.e. `['replica1', 'replica2']`) |

In addition, you need to use our custom `DistributedRouter` database router. In `settings.py`, add in:

`DATABASE_ROUTERS = ('django_distributed.SessionCachedRouter',)`

### Optional configs

