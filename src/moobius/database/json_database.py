# A simple-to-use database that dumps all it's data into nested JSON files.

import json, dataclasses
import os

from loguru import logger

from moobius import types, json_utils
from .database_interface import DatabaseInterface


class JSONDatabase(DatabaseInterface):
    """
    JSONDatabase simply stores information as JSON strings in a list of files.
    Each domain, key combination is stored as one file.
    Dataclass objects can be seralized as well.
    """
    def __init__(self, domain='', root_dir='', **kwargs):
        """
        Initialize a JSONDatabase object.

        Parameters:
          domain: str
            The name of the database directory. Will be automatically added in the add_container() function in MoobiusStorage.
          root_dir: str
            The root directory of the all the database files.
          **kwargs: Ignored for this implementation.

        Example:
          Note: This should not be called directly. Users should config the database in the config file, and call MoobiusStorage to initialize the database.
          >>> database = JSONDatabase(domain='service_1.channel_1', root_dir='data')
        """

        super().__init__()

        self.path = os.path.join(root_dir, domain.replace('.', os.sep))
        os.makedirs(self.path, exist_ok=True)

    def get_value(self, key):
        """
        Gets the value (which is a dict) given a string-valued key.
        Note: This "key" is different from a key to look up a CachedDict file.
        Note: This function should not be called directly.

        Raises:
          TypeError: If the type of the value is unknown, so we can't construct the object.

        Returns: is_sucessful, the_value
        """
        filename = os.path.join(self.path, key + '.json')

        if not os.path.exists(filename):
            return False, f'No json file found for {key}.'
        return True, json_utils.enhanced_json_load(filename)

    def set_value(self, key, value):
        """Updates and saves a cached dict, given a string-valued key and a dict-valued value. Returns (is_success, the key).
           Note: This function should not be called directly."""
        filename = os.path.join(self.path, key + '.json')
        json_utils.enhanced_json_save(filename, value)
        return True, key

    def delete_key(self, key):
        """Deletes a cached dict given a key. Returns (True, the key)
           Note: This function should not be called directly."""
        filename = os.path.join(self.path, key + '.json')
        os.remove(filename)
        return True, key

    def all_keys(self):
        """Gets all the cached dicts in the database. Returns the dicts as an iterable which internally uses yield()."""
        def key_iterator():
            """Returns an iterater with a yield."""
            for filename in os.listdir(self.path):
                if filename.endswith('.json'):
                    yield filename[:-5]
                else:
                    continue
        return key_iterator()

    def __str__(self):
        the_path = os.path.realpath(self.path).replace('\\','/')
        return f'moobius.JSONDatabase(path={the_path})'
    def __repr__(self):
        return self.__str__()
