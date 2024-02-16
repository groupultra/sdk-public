# Defines class MoobiusStorage

from loguru import logger

from collections.abc import MutableMapping
from loguru import logger


def get_engine(implementation):
    """Only import the database engine that is needed. Returns a Class object given a string."""

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
    """
    CachedDict is a custom dictionary-like class that inherits from the built-in dict class.
    The MagicalStorage class manages the creation of CachedDict instances with different attribute names, allowing users to cache and retrieve data in a structured way, with optional database interaction.
    """

    def __init__(self, database, strict_mode=False):
        """
        Initialize a CachedDict object.

        Parameters:
          database (DatabaseInterface): The database to be used, currently supports JSONDatabase and RedisDatabase.
          strict_mode=False: Whether to use strict mode.
            In strict mode, set value will raise exception if database save fails, but the value will still be set in the dict.

        No return value.

        Example:
          Note: This should not be called directly. Users should call MoobiusStorage to initialize the database.
          >>> cached_dict = CachedDict(database=database, strict_mode=True)
        """
        super().__init__()
        self.database = database
        self.strict_mode = strict_mode  

    def load(self):
        """Load all keys from the database to the cache. Returns None."""
        for key in self.database.all_keys():
            self.__getitem__(key)

    def save(self, key):
        """Save a key to the database. given a string-valued key. Returns None.
        For JSONDatabase, this will create a new json file named after the key."""
        self.__setitem__(key, self.__getitem__(key))

    def __getitem__(self, key):
        """
        Override the __getitem__, __setitem__, and __delitem__ methods of the CachedDict class to support database interaction.
        These methods are called when accessing elements using index notation and square brackets.
        Raises a KeyError if strict_mode is True and the key is not found.
        """
        if dict.__contains__(self, key):
            return dict.__getitem__(self, key)
        else:
            try:
                is_success, value = self.database.get_value(key)
            except Exception as e:
                raise Exception(f'Error with extracting {key} from database {self.database}: {e}')

            if is_success:
                self.__setitem__(key, value)
                return dict.__getitem__(self, key)
            else:
                raise KeyError(f'Key {key} not found in database')

    def __setitem__(self, key, value):
        """Allows i.e. "my_cached_dict["foo"] = some_dict" to access the underlying database, much like __getitem__.
           Raises an Exception if in strict_mode and the database cannot set the value for whatever reason."""
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
        """Allows i.e. "del my_cached_dict["foo"]" to access the underlying database, much like __getitem__.
           Raises an Exception if in strict_mode and the database cannot delete the key for whatever reason (or does not have the key)."""
        is_success, err_msg = self.database.delete_key(key)

        if is_success:
            dict.__delitem__(self, key)
        else:
            if self.strict_mode:
                raise Exception(f'Failed to delete key {key} from database. {err_msg}')
            else:
                logger.error(f'Failed to delete key {key} from database: {err_msg}. Inconsistency may occur.')
                dict.__delitem__(self,key)

    def __str__(self):
        kys = list(self.keys())
        vs = [self.get(k) for k in kys]
        return f'moobius.CachedDict({dict(zip(kys, vs))})'
    def __repr__(self):
        return self.__str__()


class MoobiusStorage():
    """
    MoobiusStorage combines multiple databases into a single interface.

    The config file to specify this database should be a list of dicts. The dict parameters are:
      implementation (str): The type of the database.
      load (bool): Whether to load the database when initializing the database.
      clear (bool): Whether to clear the database when initializing the database.
      name (str): The name of the json database.
      settings (dict): Misc settings such as Redis port, etc.
      root_dir (str): The root directory of the all the json files.
    """
    def __init__(self, service_id, channel_id, db_config=()):
        """
        Initialize a MoobiusStorage object.

        Parameters:
          service_id (str): The id of the service.
          channel_id (str): The id of the channel.
          db_config(list): The config of the databases, should be a list of config dicts.
            Each dict's 'implemetation' selects the engine. (TODO? use the field 'engine' instead of 'implementation'?)

        No return value.

        Example:
          >>> storage = MoobiusStorage(service_id='1', channel_id='1', db_config=[{'implementation': 'json', 'load': True, 'clear': False, 'name': 'character', 'settings': {'root_dir': 'data'}}])
          >>> storage.get('character').set_value('1', {'name': 'Alice'})
        """
        super().__init__()

        self.service_id = service_id
        self.channel_id = channel_id

        for config in db_config:
            self.add_container(**config)

    def put(self, attr_name, database, load=True, clear=False):
        """Sets self.attr_name to database (a DatabaseInterface object) for later retrieval.
           load (default True) to load the dict, clear (default False) to clear the dict and skip loading it."""
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
        """
        Add a database using the config dict.

        Parameters:
          implementation (str): The engine of the database.
          settings (dict): Contains "root_dir" of the json files, for example
          name (str): The attribute that will be added to self for later use.
          load=True: Whether to load the database when initializing the database.
          clear=False: Whether to clear the database when initializing the database.

        No return value.

        Example:
          Note: This is a hidden function, you don't need to call it directly.
          >>> storage = MoobiusStorage(service_id='1', channel_id='1')
          >>> storage.add_container(implementation='json', settings={'root_dir': 'data'}, name='character', load=True, clear=False)
        """
        domain = f'service_{self.service_id}.channel_{self.channel_id}.{name}'

        database_class = get_engine(implementation)

        database = database_class(domain=domain, **settings)
        self.put(name, database, load=load, clear=clear)

    def __str__(self):
        if hasattr(self, 'database'):
            db = self.database
        else:
            db = '<Not init yet>'
        if hasattr(self, 'strict_mode'):
            stm = self.strict_mode
        else:
            stm = '<Not set yet>'
        return f'moobius.MoobiusStorage(service_id={self.service_id}, channel_id={self.channel_id}, database={db}, strict={stm})'
    def __repr__(self):
        return self.__str__()
