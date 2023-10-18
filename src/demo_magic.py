# demo_magic.py

from moobius.dbtools.magical_storage import MagicalStorage
from moobius.dbtools.simple_json_database import SimpleJSONDatabase
from moobius.basic.types import Feature

class Conductor:
    def __init__(self):
        self.band = MagicalStorage()

        domains = ['features', 'views', 'real_characters', 'virtual_characters']

        for domain in domains:
            self.band.put(domain, database=SimpleJSONDatabase(root_dir='demo_magic', domain=domain))

if __name__ == '__main__':
    conductor = Conductor()
    
    print(conductor.band.views)     # should be non-empty at the second time
    
    conductor.band.features['c'] = 2
    conductor.band.features['d'] = 4
    conductor.band.views['uuid-1234'] = {
        'features': [Feature('a', 'b', 'c', 'd', 'e'), Feature('a2', 'b2', 'c2', 'd2', 'e2')],
        'stage': 'stage-1',
        'characters': ['char-1', 'char-2', 'char-3']
    }

    print(conductor.band.views)
    # conductor.band.features.clear()
    print(conductor.band.features)
