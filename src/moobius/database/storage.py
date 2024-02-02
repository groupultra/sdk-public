# Defines class MoobiusStorage

from loguru import logger

from collections.abc import MutableMapping
from loguru import logger


def get_engine(implementation):
    '''Only import the database engine that is needed.'''

    def _hit(matches):
        for m in matches:
            if implementation.lower().strip()==m.lower().strip():
                return True

    # "Switch" is only avaialbe in Python 3.10+ and can be used once this code is reset:
    if _hit(['json', 'JSON', 'JSONdb', 'JSONDatabase']):
        from moobius.database.json_database import JSONDatabase
        database_class = JSONDatabase
    elif _hit(['redis','redi', 'RedisDB', 'ready', 'RedisDatabase', 'The Linux one']):
        from moobius.database.redis_database import RedisDatabase
        database_class = RedisDatabase
    elif _hit(['null', 'None', 'False', 'Nulldb''NullDatabase']):
        from moobius.database.null_database import NullDatabase
        logger.warning('Using NullDatabase, nothing will be stored.')
        database_class = NullDatabase
    else:
        raise Exception(f'Storage engine request unrecognized {implementation}, the above block of code may need to be updated.')
    return database_class


class CachedDict(dict):
    '''
    CachedDict is a custom dictionary-like class that inherits from MutableMapping and the built-in dict class.
    The MagicalStorage class manages the creation of CachedDict instances with different attribute names, allowing users to cache and retrieve data in a structured way, with optional database interaction.
    '''

    def __init__(self, database, strict_mode=False):
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
        self.database = database
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
            >>>     logger.info(key)
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
            >>> logger.info(len(cached_dict))
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
            >>> logger.info('character_1' in cached_dict)
        '''
        return dict.__contains__(self, x)

    def __str__(self):
        return f'moobius.CachedDict({repr(dict)})'
    def __repr__(self):
        return self.__str__()


class MoobiusStorage():
    '''
    MoobiusStorage combines multiple databases into a single interface.

    To use this class, you need to specify the database config in the config file.

    The config file should be a list of dicts. The dict parameters are:
        implementation: str
            The type of the database.
        load: bool
            Whether to load the database when initializing the database.
        clear: bool
            Whether to clear the database when initializing the database.
        name: str
            The name of the json database.
        settings: dict
            root_dir: str
                The root directory of the all the json files.
    '''
    def __init__(self, service_id, band_id, db_config=()):
        '''
        Initialize a MoobiusStorage object.

        Parameters:
            service_id: str
                The id of the service.
            band_id: str
                The id of the band.
            db_config: list
                The config of the databases, should be a list of config dicts.
                  Each dict's 'implemetation' selects the engine. (TODO? use the field 'engine' instead of 'implementation'?)
                  'settings' gives settings such as Redis port etc.

        Returns:
            None

        Example:
            >>> storage = MoobiusStorage(service_id='1', band_id='1', db_config=[{'implementation': 'json', 'load': True, 'clear': False, 'name': 'character', 'settings': {'root_dir': 'data'}}])
            >>> storage.get('character').set_value('1', {'name': 'Alice'})
        '''
        super().__init__()

        self.service_id = service_id
        self.band_id = band_id

        for config in db_config:
            self.add_container(**config)

    def put(self, attr_name, database, load=True, clear=False):
        '''Sets self.attr_name to the storage for later retrieval.'''
        if attr_name in self.__dict__:
            raise Exception('Domain {n} already exists'.format(n=attr_name))
        else:
            cached_dict = CachedDict(database)

            if clear:
                cached_dict.clear()
            elif load:
                cached_dict.load()
            else:
                pass

            self.__setattr__(attr_name, cached_dict)

    @logger.catch
    def add_container(self, implementation, settings, name, load=True, clear=False):
        '''
        Add a database using the config dict.

        Parameters:
            implementation: str
                The type of the database.
            settings: dict
                root_dir: str
                    The root directory of the all the json files.
            name: str
                The name of the json database.
            load=True: bool
                Whether to load the database when initializing the database.
            clear=False: bool
                Whether to clear the database when initializing the database.

        Returns:
            None

        Example:
            Note: This is a hidden function, you don't need to call it directly.
            >>> storage = MoobiusStorage(service_id='1', band_id='1')
            >>> storage.add_container(implementation='json', settings={'root_dir': 'data'}, name='character', load=True, clear=False)
        '''
        domain = f'service_{self.service_id}.band_{self.band_id}.{name}'

        database_class = get_engine(implementation)

        database = database_class(domain=domain, **settings)
        self.put(name, database, load=load, clear=clear)

    def __str__(self):
        return f'moobius.MoobiusStorage(service_id={self.service_id}, band_id={self.band_id}, database={self.database}, strict={self.strict_mode})'
    def __repr__(self):
        return self.__str__()
