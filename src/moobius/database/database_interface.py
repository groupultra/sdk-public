# All databases imeplement the abstract DatabaseInterface class.
from abc import ABC, abstractmethod


class DatabaseInterface(ABC):
    """
    An bstract base class that is to be inherited by different database backends.
    Currently available as of July 2024: JSONDatabase, NullDatabase, and RedisDatabase.

    When a MoobiusStorage object is constructed:
    >>> MoobiusStorage(self.client_id, channel_id, db_config=self.db_config)
    An internal DatabaseInterface is constructed.

    Each demo's on_start() function passes calls MoobiusStorage(self.client_id, channel_id, db_config=self.db_config)
    The db_config can be a dict or a .json file name. An example:
    >>>    [{"implementation": "json", "name": "health_bars", "load": true, "clear": false,
    >>>     "settings": {"root_dir": "json_db"}}
    >>>    {"implementation": "redis", "name": "mana_bars", "load": true, "clear": false,
    >>>     "settings": {"root_dir": "json_db"}}]

    The Moobius (service) class, on initialization, create one MoobiusStorage object per channel, unless initalize_channel() is overridden.
    Each MoobiusStorage object creates one CachedDict per element in the db-config list, using the "name" to dynamically generate an attribute.
    The "implementation" sets the engine to be used by CachedDict.
    """
    @abstractmethod
    def __init__(self, domain='', **kwargs):
        """
        Creates the database itself.

        The string-valued `domain` parameteras is used to prevent collisions: different domains with the same key are different database entries.
        Internally, differnt domains become different tables in the same database or different folders in the same file system.
        Currently, the MoobiusStorage names it's domains in a dot-seperated way:
        >>> <service_id>.channel_<channel_id>.<name in db_config>.
        """
        super().__init__()

    @abstractmethod
    def get_value(self, key) -> (bool, any):
        """Returns a tuple of (is_success, value)."""
        pass

    @abstractmethod
    def set_value(self, key, value) -> (bool, any):
        """Returns a tuple of (is_success=True, key) or (is_success=False, err_message)."""
        pass

    @abstractmethod
    def delete_key(self, key) -> (bool, any):
        """Returns a tuple of (is_success=True, key) or (is_success=False, err_message)."""
        pass

    @abstractmethod
    def all_keys(self) -> any:
        """Returns an iterable of all keys, the details of which depend on the implementation."""
        pass

    def __str__(self):
        return f'moobius.DatabaseInterface()'
    def __repr__(self):
        return self.__str__()
