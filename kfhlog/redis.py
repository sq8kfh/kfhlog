import redis
import pickle


# for redis sessions
def get_redis_client(request, **redis_options):
    return request.raw_redis


class RedisStore(object):
    def __init__(self, raw_redis):
        self._r = raw_redis

    def __len__(self):
        return 0

    def __getitem__(self, key):
        tmp = self._r.get(key)
        if not tmp:
            raise KeyError(key)
        return pickle.loads(tmp)

    def __setitem__(self, key, value):
        self._r.set(key, pickle.dumps(value))

    def __delitem__(self, key):
        if self.__contains__(key):
            self._r.delete(key)
        else:
            raise KeyError(key)

    def __contains__(self, item):
        return self._r.exists(item)


def get_redis(request):
    return RedisStore(request.raw_redis)


def _get_raw_redis_factory(host, port, db):
    return lambda x: redis.StrictRedis(host=host, port=port, db=db)


def includeme(config):
    settings = config.get_settings()

    tmp = _get_raw_redis_factory(settings['redis.host'], settings['redis.port'], settings['redis.db'])
    config.add_request_method(tmp, 'raw_redis', reify=True)
    config.add_request_method(get_redis, 'redis', reify=True)
