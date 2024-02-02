# json_database.py

import json
import os
from pydoc import locate

from dacite import from_dict
from loguru import logger

from moobius.utils import EnhancedJSONEncoder
from moobius import types
from .database_interface import DatabaseInterface


# TODO: 
# 1. validity check for key (must be str)
# 2. json serializable check
# 3. rolling back when error occurs
class JSONDatabase(DatabaseInterface):
    # key: name of the database json file
    # file content: {key: value}
    '''
    JSONDatabase simply stores information as JSON strings in a list of files.
    '''
    def __init__(self, domain='', root_dir='', **kwargs):
        '''
        Initialize a JSONDatabase object.

        Parameters:
            domain: str
                The name of the database directory. Will be automatically added in the add_container() function in MoobiusStorage.
            root_dir: str
                The root directory of the all the database files.

        Returns:
            None

        Example:
            Note: This should not be called directly. Users should config the database in the config file, and call MoobiusStorage to initialize the database.
            >>> database = JSONDatabase(domain='service_1.band_1', root_dir='data')
        '''

        super().__init__()

        self.path = os.path.join(root_dir, domain.replace('.', os.sep))
        self.ref_module = types
        os.makedirs(self.path, exist_ok=True)

    @logger.catch
    def get_value(self, key):
        '''
        Get the value of a key.

        Parameters:
            key: str
                Here key is the name of the json file.

        Returns:
            A tuple of (is_success, value) or (is_success, None)

        Example:
            Note: This is a hidden function, you don't need to call it directly.
            >>> is_success, value = database.get_value('character_1')

        Raises:
            TypeError: If the type of the value is unknown, so we can't construct the object.
        '''
        filename = os.path.join(self.path, key + '.json')
        logger.debug(f'Loading {filename}')

        with open(filename, 'r') as f:
            data = json.load(f)

            if data['_type'] == 'NoneType':
                return True, None   # You can't use NoneType(None) to construct a NoneType object, so we have to return None directly
            else:
                class_name = data['_type']
                data_type = locate(f'{self.ref_module.__name__}.{class_name}')

                if data_type:   # dataclass
                    return True, from_dict(data_class=data_type, data=data[key])

                else:   # possible built-in type, attempt to construct the object from the value
                    data_type = locate(class_name)
                    
                    if data_type:
                        return True, data_type(data[key])
                        
                    else:
                        raise TypeError(f'Unknown type: {class_name}')

    @logger.catch
    def set_value(self, key, value):    # the value has to be dict!
        '''
        Set the value of a key. Here key is the name of the json file.

        Parameters:
            key: str
                Here key is the name of the json file, not the key inside the json file.
            value: dict
                Content of the json file, in dict format.

        Returns:
            A tuple of (is_success, key)

        Example:
            Note: This is a hidden function, you don't need to call it directly.
            >>> is_success, key = database.set_value('character_1', {'name': 'Alice', 'age': 18})
        '''
        filename = os.path.join(self.path, key + '.json')

        with open(filename, 'w') as f:
            data = {key: value, '_type': type(value).__name__}
            json.dump(data, f, indent=4, cls=EnhancedJSONEncoder)
            return True, key

    @logger.catch
    def delete_key(self, key):
        '''
        Delete a key.

        Parameters:
            key: str
                Here key is the name of the json file, not the key inside the json file.

        Returns:
            A tuple of (is_success, key)

        Example:
            Note: This is a hidden function, you don't need to call it directly.
            >>> is_success, key = database.delete_key('character_1')
        '''
        filename = os.path.join(self.path, key + '.json')
        os.remove(filename)

        return True, key

    @logger.catch
    def all_keys(self):
        '''
        Get all keys in the database, return an iterable.

        Parameters:
            None

        Returns:
            An iterable of all keys

        Example:
            Note: This is a hidden function, you don't need to call it directly.
            >>> for key in self.database.all_keys():
            >>>     logger.info(key)
        '''
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