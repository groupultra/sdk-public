# json_database.py

import json
import os
from pydoc import locate

from dacite import from_dict
from loguru import logger

from moobius.utils import EnhancedJSONEncoder
from moobius import types
from .database_interface import DatabaseInterface


# todo: 
# 1. validity check for key (must be str)
# 2. json serializable check
# 3. rolling back when error occurs
class JSONDatabase(DatabaseInterface):
    # root_dir: root directory of the all the database files
    # domain: name of the database dir
    # key: name of the database json file
    # file content: {key: value}
    def __init__(self, domain='', root_dir='', **kwargs):
        super().__init__()
        
        self.path = os.path.join(root_dir, domain.replace('.', os.sep))
        self.ref_module = types
        os.makedirs(self.path, exist_ok=True)

    @logger.catch
    def get_value(self, key):
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
        filename = os.path.join(self.path, key + '.json')
        
        with open(filename, 'w') as f:
            data = {key: value, '_type': type(value).__name__}
            json.dump(data, f, indent=4, cls=EnhancedJSONEncoder)
            return True, key

    @logger.catch
    def delete_key(self, key):
        filename = os.path.join(self.path, key + '.json')
        os.remove(filename)
        
        return True, key

    @logger.catch
    def all_keys(self):
        def key_iterator():
            for filename in os.listdir(self.path):
                if filename.endswith('.json'):
                    yield filename[:-5]
                else:
                    continue

        return key_iterator()
    