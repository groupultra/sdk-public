import redis
import traceback
from src.moobius.dbtools.database_interface import DatabaseInterface

def safe_operate(func):
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except Exception as e:
            traceback.print_exc()
            return False, repr(e)
    return wrapper

class SimpleRedisDatabase(DatabaseInterface):
    def __init__(self, domain='', host="localhost", port=6379, db=0, password="", **kwargs):
        super().__init__(domain, **kwargs)

        self.redis = redis.Redis(host=host, port=port, db=db, password=password)

    @safe_operate
    def get_value(self, key) -> (bool, any):
        if self.redis.exists(key):
            return True, self.redis.get(key)
        return False, f'Key {key} does not exist'
    
    @safe_operate
    def set_value(self, key, value) -> (bool, any):
        self.redis.set(key, value)
        return True, key
    
    @safe_operate
    def delete_key(self, key) -> (bool, any):
        self.redis.delete(key)
        return True, key
    
    @safe_operate
    def all_keys(self) -> any:
        return self.redis.keys()
    
