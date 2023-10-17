# simple_json_database.py

import json
import os
import dataclasses
import traceback
from moobius.dbtools.database_interface import DatabaseInterface

def safe_operate(func):
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except Exception as e:
            traceback.print_exc()
            return False, repr(e)
    return wrapper


class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        else:
            return super().default(o)




# todo: 
# 1. validity check for key (must be str)
# 2. json serializable check
# 3. rolling back when error occurs
class SimpleJSONDatabase(DatabaseInterface):
    # root_dir: root directory of the all the database files
    # domain: name of the database dir
    # key: name of the database json file
    # file content: {key: value}
    def __init__(self, root_dir='.', domain=''):
        super().__init__()
        
        self.path = os.path.join(root_dir, domain)
        os.makedirs(self.path, exist_ok=True)

    
    @safe_operate
    def get_value(self, key):
        filename = os.path.join(self.path, key + '.json')
        print('SimpleJSONDatabase: Loading key {k}'.format(k=key))
        
        with open(filename, 'r') as f:
            data = json.load(f)
            return True, data[key]

    @safe_operate
    def set_value(self, key, value):
        filename = os.path.join(self.path, key + '.json')
        print('SimpleJSONDatabase: Saving key {k} with value {v}'.format(k=key, v=value))
        with open(filename, 'w') as f:
            data = {key: value}
            json.dump(data, f, indent=4, cls=EnhancedJSONEncoder)
            return True, key

    @safe_operate
    def delete_key(self, key):
        filename = os.path.join(self.path, key + '.json')
        print('SimpleJSONDatabase: Deleting key {k}'.format(k=key))
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
    