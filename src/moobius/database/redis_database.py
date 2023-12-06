import redis
from .database_interface import DatabaseInterface
from loguru import logger


class RedisDatabase(DatabaseInterface):
    def __init__(self, domain='', host="localhost", port=6379, db=0, password="", **kwargs):
        super().__init__(domain, **kwargs)

        self.redis = redis.Redis(host=host, port=port, db=db, password=password)

    @logger.catch
    def get_value(self, key) -> (bool, any):
        if self.redis.exists(key):
            return True, self.redis.get(key)
        return False, f'Key {key} does not exist'
    
    @logger.catch
    def set_value(self, key, value) -> (bool, any):
        self.redis.set(key, value)
        return True, key
    
    @logger.catch
    def delete_key(self, key) -> (bool, any):
        self.redis.delete(key)
        return True, key
    
    @logger.catch
    def all_keys(self) -> any:
        return self.redis.keys()
    
