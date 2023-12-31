# magical_storage.py.py

from collections.abc import MutableMapping
from .null_database import NullDatabase
from loguru import logger


class CachedDict(MutableMapping, dict):
    '''
    CachedDict is a custom dictionary-like class that inherits from MutableMapping and the built-in dict class.
    The MagicalStorage class manages the creation of CachedDict instances with different attribute names, allowing users to cache and retrieve data in a structured way, with optional database interaction.
    '''
    
    def __init__(self, database=None, strict_mode=False):
        '''
        Initialize a CachedDict object.
        
        Parameters:
            database: DatabaseInterface
                The database to be used, currently supports JSONDatabase and NullDatabase.
            strict_mode: bool
                Whether to use strict mode. In strict mode, set value will raise exception if database save fails, but the value will still be set in the dict.
        
        Returns:
            None
        
        Example:
            Note: This should not be called directly. Users should call MoobiusStorage to initialize the database.
            >>> cached_dict = CachedDict(database=database, strict_mode=True)
        '''
        super().__init__()
        self.database = database or NullDatabase()
        self.strict_mode = strict_mode  

    def load(self):
        '''
        Load all keys from the database to the cache.
        
        Parameters:
            None
        
        Returns:
            None
        
        Example:
            Note: This is a hidden function, you don't need to call it directly.
            >>> cached_dict = CachedDict(database=database, strict_mode=True)
            >>> cached_dict.load()
        '''
        for key in self.database.all_keys():
            self.__getitem__(key)

    def save(self, key):
        '''
        Save a key to the database. For JSONDatabase, this will create a new json file named after the key.
        
        Parameters:
            key: str
                The key to be saved.
        
        Returns:
            None
        
        Example:
            Note: This is a hidden function, you don't need to call it directly.
            >>> cached_dict = CachedDict(database=database, strict_mode=True)
            >>> cached_dict.save('character_1')
        '''
        self.__setitem__(key, self.__getitem__(key))

    def __getitem__(self, key):
        '''
        Override the __getitem__ method of the CachedDict class to support database interaction.
        This function enables accessing elements using index notation and square brackets.
        
        Parameters:
            key: str
                The key to be retrieved.
        
        Returns:
            The value of the key.
        
        Example:
            Note: This is a hidden function, you don't need to call it directly.
            >>> cached_dict = CachedDict(database=database, strict_mode=True)
            >>> cached_dict['character_1']
            
        Raises:
            KeyError: If the key is not found in the database and strict_mode is True, this function will raise a KeyError.
        '''
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
        '''
        Override the __setitem__ method of the CachedDict class to support database interaction.
        This function enables assigning elements using index notation and square brackets.
        
        Parameters:
            key: str
                The key to be set.
            value: dict
                The value to be set. Should be a dict.
        
        Returns:
            None
        
        Example:
            Note: This is a hidden function, you don't need to call it directly.
            >>> cached_dict = CachedDict(database=database, strict_mode=True)
            >>> cached_dict['character_1'] = {'name': 'Alice', 'age': 18}
            
        Raises:
            Exception: If the database save fails and strict_mode is True, this function will raise an exception about the failure.
        '''
                
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
        '''
        Enable deleting elements from CachedDict using index notation and square brackets.
        
        Parameters:
            key: str
                The key to be deleted.
            
        Returns:
            None
        
        Example:
            Note: This is a hidden function, you don't need to call it directly.
            >>> cached_dict = CachedDict(database=database, strict_mode=True)
            >>> del cached_dict['character_1']
        
        Raises:
            Exception: If the database delete fails and strict_mode is True, this function will raise an exception about the failure.
        '''
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
        '''
        Enable iteration over the CachedDict.
        
        Parameters:
            None
        
        Returns:
            None
            
        Example:
            Note: This is a hidden function, you don't need to call it directly.
            >>> cached_dict = CachedDict(database=database, strict_mode=True)
            >>> for key in cached_dict:
            >>>     print(key)
        '''
        return dict.__iter__(self)
    
    def __len__(self):
        '''
        Enable getting the length of the CachedDict.
        
        Parameters:
            None
        
        Returns:
            None
        
        Example:
            Note: This is a hidden function, you don't need to call it directly.
            >>> cached_dict = CachedDict(database=database, strict_mode=True)
            >>> print(len(cached_dict))
        '''
        return dict.__len__(self)
    
    def __contains__(self, x):
        '''
        Enable checking if a key exists in the CachedDict.
        
        Parameters:
            x: str
                The key to be checked.
            
        Returns:
            None
    
        Example:
            Note: This is a hidden function, you don't need to call it directly.
            >>> cached_dict = CachedDict(database=database, strict_mode=True)
            >>> print('character_1' in cached_dict)
        '''
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
