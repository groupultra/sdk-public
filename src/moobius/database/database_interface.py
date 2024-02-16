from abc import ABC, abstractmethod


class DatabaseInterface(ABC):
    """
    Various database backends need to inherit this interface.
    Currently available as of Jan 2024: JSONDatabase, NullDatabase, and RedisDatabase.
    Each demo's on_start() function passes calls MoobiusStorage(self.client_id, channel_id, db_config=self.db_config)
    Instead of hardcoding self.db_config each demo it stores it as a JSON list, each element of the form:
        {"implementation": "json", "name": "buttons", "load": true, "clear": false,
         "settings": {"root_dir": "json_db"}}
         Where different elements in the list have different "name" values.
    To use a config file, pass db_config_path="my/db_config/file.json" into wand.run()
      Wand will pass this kwarg to the MoobiusService object bieng ran.
      The service will load the JSON into self.db_config
    Then, in the on_start() function each demo will call MoobiusStorage(self.client_id, channel_id, db_config=self.db_config)
      TODO: This is clumsy and on_start is repetative between demos, refactor this part and maybe others into service functions?
      For each element in db_config the MoobiusStorage will call self.add_container(**config) and use the implementation kwarg as a switchyard.
    """
    @abstractmethod
    def __init__(self, domain='', **kwargs):
        """
        The concrete methods should expect a `domain` parameter as a `str`.
        It is used to separate different domains in the same database.
        Like different tables in the same database.
        Or different folders in the same file system.
        The keys inside different domains may overlap, but they are different entries.
        For example, two channels may have entries with the same button id.
        domains are '.' separated strings, like '<channel_id>.<character_id>'
        """
        super().__init__()

    @abstractmethod
    def get_value(self, key) -> (bool, any):
        """Returns a tuple of (is_success, value)"""
        pass

    @abstractmethod
    def set_value(self, key, value) -> (bool, any):
        """Returns a tuple of (is_success=True, key) or (is_success=False, err_msg)"""
        pass

    @abstractmethod
    def delete_key(self, key) -> (bool, any):
        """Returns a tuple of (is_success=True, key) or (is_success=False, err_msg)"""
        pass

    @abstractmethod
    def all_keys(self) -> any:
        """Returns an iterable of all keys, the details of which depend on the implementation."""
        pass

    def __str__(self):
        return f'moobius.DatabaseInterface()'
    def __repr__(self):
        return self.__str__()
