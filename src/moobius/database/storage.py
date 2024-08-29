# Dict-like storage that is persistent across program restarts.

from loguru import logger

from collections.abc import MutableMapping
from loguru import logger


def get_engine(implementation):
    """Given an implementation string, returns the engine's Class. 
    Last-minute-imports the module so that no pip package is needed for unused engines."""

    def _hit(matches):
        """Accepts a list of matches. Returns if the engine is one of those matches."""
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

        Returns None.

        Example:
          Note: This should not be called directly. Users should call MoobiusStorage to initialize the database.
          >>> cached_dict = CachedDict(database=database, strict_mode=True)
        """
        super().__init__()
        self.database = database
        self.strict_mode = strict_mode  

    def load(self):
        """Loads all keys from the database to the cache. Returns None."""
        for key in self.database.all_keys():
            self.__getitem__(key)

    def save(self, key):
        """Saves a key to the database. given a string-valued key. Returns None.
        For a JSONDatabase, this will create a new json file named after the database's domain and key."""
        self.__setitem__(key, self.__getitem__(key))

    def __getitem__(self, key):
        """Overrides dict-like usages of the form: "v = d['my_key']" to query from the database.
        Raises a KeyError if strict_mode is True and the key is not found. Accepts the key and returns the value."""
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
        """Overrides dict-like usages of the form: "d['my_key'] = v" to save to the database.
        For a JSONDatabase, this will save the updated json to a file. Accepts the key and value. Returns None."""
        is_success, err_message = self.database.set_value(key, value)

        if is_success:
            dict.__setitem__(self, key, value)
        else:
            if self.strict_mode:
                raise Exception(f'Failed to save key {key} to database. {err_message}')
            else:
                logger.error(f'Failed to save key {key} to database: {err_message}. Inconsistency may occur.')
                dict.__setitem__(self, key, value)    

    def __delitem__(self, key):
        """Overrides dict-like usages of the form: "del d['my_key']" to delete a key from the database.
        For a JSONDatabase, this will save the updated json to a file. Accepts the key. Returns None."""
        is_success, err_message = self.database.delete_key(key)

        if is_success:
            dict.__delitem__(self, key)
        else:
            if self.strict_mode:
                raise Exception(f'Failed to delete key {key} from database. {err_message}')
            else:
                logger.error(f'Failed to delete key {key} from database: {err_message}. Inconsistency may occur.')
                dict.__delitem__(self,key)

    def pop(self, key, default="__unspecified__"):
        """Overrides "v = d.pop(k)" to get and delete k from the database. Accepts the key and an optional default value. Returns the value."""
        if default == "__unspecified__" and not dict.__contains__(self, key):
            raise KeyError(f'Key {key} not in dict.')
        if dict.__contains__(self, key):
            out = self.__getitem__(key)
            self.__delitem__(key)
            return out
        else:
            return default

    def clear(self):
        """Overrides "d.clear()" to clear the database. Returns None."""
        for k in list(self.keys()):
            self.pop(k)

    def __str__(self):
        kys = list(self.keys())
        vs = [self.get(k) for k in kys]
        return f'moobius.CachedDict({dict(zip(kys, vs))})'
    def __repr__(self):
        return self.__str__()


class MoobiusStorage():
    """
    MoobiusStorage combines multiple databases together.
    Each database becomes one attribute using dynamic attribute creation.
    """
    def __init__(self, service_id, channel_id, db_config=()):
        """
        Initialize a MoobiusStorage object.

        Parameters:
          service_id (str): The id of the service.
          channel_id (str): The id of the channel.
          db_config (list): The config of the databases, should be a list of config dicts.
              implementation (str) = the type of the database.
              load (bool) = whether to load the database when initializing the database.
              clear (bool) = whether to clear the database when initializing the database.
              name (str) = the name of the json database.
              settings (dict) = misc settings such as Redis port, etc.
              root_dir (str) = the root directory of the all the json files.

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
        """
        Sets self.attr_name to database (a DatabaseInterface object) for later retrieval. Returns None.
        load (default True) to load the dict immediatly, clear (default False) to clear the dict and skip loading it.

        Parameters:
           attr_name: The attr name to add dynamically to self, setting it to a CachedDict.
           database: The database.
           load=True: Whether to load the dict in full at startup instead of gradually.
           clear=False: Whether to clear the dict (which deletes the files).
        """
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
        Adds a database using the config dict.

        Parameters:
          implementation (str): The engine of the database.
          settings (dict): Contains "root_dir" of the json files, for example
          name (str): The attribute that will be added to self for later use.
          load=True: Whether to load the database when initializing the database.
          clear=False: Whether to clear the database when initializing the database.

        Returns None.

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
