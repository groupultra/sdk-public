# json_database.py

import json, dataclasses
import os
from pydoc import locate

from dacite import from_dict
from loguru import logger

from moobius.utils import EnhancedJSONEncoder
from moobius import types
from .database_interface import DatabaseInterface

DTYPE = '_type' # Used to indicate the class name.

# TODO: 
# 1. validity check for key (must be str)
# 2. json serializable check
# 3. rolling back when error occurs
class JSONDatabase(DatabaseInterface):
    # key: name of the database json file
    # file content: {key: value}
    """
    JSONDatabase simply stores information as JSON strings in a list of files.
    """
    def __init__(self, domain='', root_dir='', **kwargs):
        """
        Initialize a JSONDatabase object.

        Parameters:
          domain: str
            The name of the database directory. Will be automatically added in the add_container() function in MoobiusStorage.
          root_dir: str
            The root directory of the all the database files.

        No return value.

        Example:
          Note: This should not be called directly. Users should config the database in the config file, and call MoobiusStorage to initialize the database.
          >>> database = JSONDatabase(domain='service_1.channel_1', root_dir='data')
        """

        super().__init__()

        self.path = os.path.join(root_dir, domain.replace('.', os.sep))
        os.makedirs(self.path, exist_ok=True)

    def get_value(self, key):
        """
        Gets the value (which is a dict) of a string-valued key. Returns (is_success, the_value).
        Note: This function should not be called directly.

        Raises:
          TypeError: If the type of the value is unknown, so we can't construct the object.
        """
        filename = os.path.join(self.path, key + '.json')

        if not os.path.exists(filename):
            return False, f'No json file found for {key}.'
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)

            if data[DTYPE] == 'NoneType':
                return True, None   # You can't use NoneType(None) to construct a NoneType object, so we have to return None directly
            else:
                class_name_fullpath = data[DTYPE]
                data_type = locate(class_name_fullpath)

                if not data_type: # Legacy backwards compat. Remove this if block after enough time has passed.
                    data_type = locate(f'{types.__name__}.{class_name_fullpath}')
                    if data_type:
                        logger.warning('Legacy compat JSONDatabase type system. This warning should disappear on save+load of the database.')

                if data_type:
                    if dataclasses.is_dataclass(data_type):
                        return True, from_dict(data_class=data_type, data=data[key])
                    else:
                        return True, data_type(data[key])
                else:
                    raise TypeError(f'Unknown type: {class_name_fullpath}')

    def set_value(self, key, value):
        """Set the value (a dict) of a key (a string). Returns (is_success, the_key).
           Note: This function should not be called directly."""
        filename = os.path.join(self.path, key + '.json')

        with open(filename, 'w', encoding='utf-8') as f:
            data = {key: value, DTYPE: type(value).__module__+'.'+type(value).__name__} # Fullpath is package.module.name.
            json.dump(data, f, indent=4, cls=EnhancedJSONEncoder, ensure_ascii=False)
            return True, key

    def delete_key(self, key):
        """Delete a (string-valued) key. Returns (is_success, key)
           Note: This function should not be called directly."""
        filename = os.path.join(self.path, key + '.json')
        os.remove(filename)

        return True, key

    def all_keys(self):
        """Gets all keys in the database. Returns an iterable which internally uses yield()."""
        def key_iterator():
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
