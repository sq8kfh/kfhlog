from pyramid_celery import celery_app
from ..models import (
    get_engine,
    get_session_factory,
)
from .. import redis

class BaseTask(celery_app.Task):
    def on_success(self, retval, task_id, args, kwargs):
        print("succes " + task_id)
        super(BaseTask, self).on_success(retval, task_id, args, kwargs)

    def on_retry(self, exc, task_id, args, kwargs, einfo):
        print('retry ' + task_id)
        super(BaseTask, self).on_retry(exc, task_id, args, kwargs, einfo)

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        print('failure ' + task_id)
        super(BaseTask, self).on_failure(exc, task_id, args, kwargs, einfo)

    def get_db(self):
        #return celery_app.conf['PYRAMID_REGISTRY'].dbsession_factory
        settings = celery_app.conf['PYRAMID_REGISTRY'].settings
        engine = get_engine(settings)
        session_factory = get_session_factory(engine)
        #with transaction.manager:
        #    dbsession = get_tm_session(session_factory, transaction.manager)
        #    #fun(self, dbsession, None, *arg, **karg)
        return session_factory

    def get_redis(self):
        print("get redis")
        settings = celery_app.conf['PYRAMID_REGISTRY'].settings

        tmp = redis._get_raw_redis_factory(settings['redis.host'], settings['redis.port'], settings['redis.db'])
        return redis.RedisStore(tmp)
