# magical_storage.py.py

from collections.abc import MutableMapping
from .null_database import NullDatabase
from loguru import logger


class CachedDict(MutableMapping, dict):
    def __init__(self, database=None, strict_mode=False):
        super().__init__()
        self.database = database or NullDatabase()
        self.strict_mode = strict_mode  
        # in strict mode, set value will raise exception if database save fails
        # but the value will still be set in the dict

    def load(self):
        for key in self.database.all_keys():
            self.__getitem__(key)

    def __getitem__(self, key):
        if dict.__contains__(self, key):
            return dict.__getitem__(self, key)
        else:
            is_success, value = self.database.get_value(key)

            if is_success:
                self.__setitem__(key, value)
                return dict.__getitem__(self, key)
            else:
                raise KeyError(f'Key {key} not found in database')
    
    def __setitem__(self, key, value):
        is_success, err_msg = self.database.set_value(key, value)

        if is_success:
            dict.__setitem__(self, key, value)
        else:
            if self.strict_mode:
                raise Exception(f'Failed to save key {key} to database. {err_msg}')
            else:
                logger.error(f'Failed to save key {key} to database: {err_msg}. Inconsistency may occur.')
                dict.__setitem__(self, key, value)    
    
    def __delitem__(self, key):
        is_success, err_msg = self.database.delete_key(key)

        if is_success:
            dict.__delitem__(self, key)
        else:
            if self.strict_mode:
                raise Exception(f'Failed to delete key {key} from database. {err_msg}')
            else:
                logger.error(f'Failed to delete key {key} from database: {err_msg}. Inconsistency may occur.')
                dict.__delitem__(self,key)
    
    def __iter__(self):
        return dict.__iter__(self)
    
    def __len__(self):
        return dict.__len__(self)
    
    def __contains__(self, x):
        return dict.__contains__(self, x)


class MagicalStorage:
    def __init__(self):
        pass
    
    def put(self, attr_name, database=None, load=True, clear=False):
        if attr_name in self.__dict__:
            raise Exception('Domain {n} already exists'.format(n=attr_name))
        else:
            cached_dict = CachedDict(database=database)

            if clear:
                cached_dict.clear()
            elif load:
                cached_dict.load()
            else:
                pass
            
            self.__setattr__(attr_name, cached_dict)
