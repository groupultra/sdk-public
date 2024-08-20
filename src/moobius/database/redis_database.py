# Uses Redis, an in-memory database, to improve performance. Requires a running Redis server.
import json, redis
from .database_interface import DatabaseInterface

from moobius import json_utils

from loguru import logger

autosave = False # Only set True for debugging, saving is O(N)!


class RedisDatabase(DatabaseInterface):
    """The redis database make use of a redis.Redis(...) server (Redis servers are set to localhost:6379 by default).
    By default uses the domains's hash code to differentiate different domains, unless a user-supplied "db" value is given."""
    def __init__(self, domain='', host="localhost", port=6379, db=None, password="", **kwargs):
        """Accepts the domain, the host, the port, the db, the password, and ignores the extra kwargs."""
        super().__init__(domain, **kwargs)
        logger.info(f'Redis initialized on {host} port {port}')
        if db is None:
            db = abs(hash(domain))
        self.redis = redis.Redis(host=host, port=port, db=db, password=password)

    def get_value(self, key) -> (bool, any):
        """Accepts a key. Returns (sucess, the value)."""
        if self.redis.exists(key):
            balue = self.redis.get(key)
            return True, json_utils.enhanced_json_load(balue)
        return False, f'Key {key} does not exist'

    def set_value(self, key, value) -> (bool, any):
        """Accepts the key and value. Returns (sucess, the key)."""
        balue = utils.enhanced_json_save(None, value).encode()
        self.redis.set(key, balue)
        if autosave:
            self.redis.save()
        return True, key

    def delete_key(self, key) -> (bool, any):
        """Accepts the key. Returns (True, the key)."""
        self.redis.delete(key)
        if autosave:
            self.redis.save()
        return True, key

    def all_keys(self) -> any:
        """Returns the list of keys."""
        out = self.redis.keys()
        return [k.decode() for k in out]

    def __str__(self):
        return f'moobius.RedisDatabase({self.redis})'
    def __repr__(self):
        return self.__str__()
