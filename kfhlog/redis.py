import redis
import pickle


class Redis_store(object):
    def __init__(self):
        self._r = redis.StrictRedis(host='localhost', port=6379, db=0)

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
    return Redis_store()


def includeme(config):
    config.add_request_method(get_redis, 'redis', reify=True)
