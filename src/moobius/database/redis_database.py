import json, redis
from .database_interface import DatabaseInterface

from moobius.utils import EnhancedJSONEncoder
from loguru import logger

autosave = False # Only set True for debugging, saving is O(N)!


class RedisDatabase(DatabaseInterface):
    """The redis database make use of a redis.Redis(...) server (Redis servers are set to localhost:6379 by default)."""
    def __init__(self, domain='', host="localhost", port=6379, db=0, password="", **kwargs):
        super().__init__(domain, **kwargs)
        logger.info(f'Redis initialized on {host} port {port}')
        self.redis = redis.Redis(host=host, port=port, db=db, password=password)

    def get_value(self, key) -> (bool, any):
        if self.redis.exists(key):
            balue = self.redis.get(key)
            return True, json.loads(balue.decode())
        return False, f'Key {key} does not exist'

    def set_value(self, key, value) -> (bool, any):
        balue = json.dumps(value, cls=EnhancedJSONEncoder).encode()
        self.redis.set(key, balue)
        if autosave:
            self.redis.save()
        return True, key

    def delete_key(self, key) -> (bool, any):
        self.redis.delete(key)
        if autosave:
            self.redis.save()
        return True, key

    def all_keys(self) -> any:
        out = self.redis.keys()
        return [k.decode() for k in out]

    def __str__(self):
        return f'moobius.RedisDatabase({self.redis})'
    def __repr__(self):
        return self.__str__()
