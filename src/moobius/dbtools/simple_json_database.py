# simple_json_database.py

import json
import os
import dataclasses
import traceback
from dataclasses import asdict

from moobius.utils import EnhancedJSONEncoder
from moobius.dbtools.database_interface import DatabaseInterface

def safe_operate(func):
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except Exception as e:
            traceback.print_exc()
            return False, repr(e)
    return wrapper


# todo: 
# 1. validity check for key (must be str)
# 2. json serializable check
# 3. rolling back when error occurs
class SimpleJSONDatabase(DatabaseInterface):
    # root_dir: root directory of the all the database files
    # domain: name of the database dir
    # key: name of the database json file
    # file content: {key: value}
    def __init__(self, domain='', root_dir='', **kwargs):
        super().__init__()
        
        self.path = os.path.join(root_dir, domain.replace('.', os.sep))
        os.makedirs(self.path, exist_ok=True)

    
    @safe_operate
    def get_value(self, key):
        filename = os.path.join(self.path, key + '.json')
        
        with open(filename, 'r') as f:
            data = json.load(f)
            return True, dict(data[key])  # todo: add a field to indicate the type of the value

    @safe_operate
    def set_value(self, key, value):    # the value has to be dict!
        filename = os.path.join(self.path, key + '.json')
        
        with open(filename, 'w') as f:
            data = {key: dict(value)}
            json.dump(data, f, indent=4, cls=EnhancedJSONEncoder)
            return True, key

    @safe_operate
    def delete_key(self, key):
        filename = os.path.join(self.path, key + '.json')
        os.remove(filename)
        
        return True, key

    def all_keys(self):
        def key_iterator():
            for filename in os.listdir(self.path):
                if filename.endswith('.json'):
                    yield filename[:-5]
                else:
                    continue

        return key_iterator()
    