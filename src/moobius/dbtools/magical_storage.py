# storage.py

from moobius.types import CachedDict

class MagicalStorage:
    def __init__(self):
        pass
    
    def put(self, attr_name, database=None, load=True, clear=False):
        if attr_name in self.__dict__:
            raise Exception('Domain {n} already exists'.format(n=attr_name))
        else:
            cached_dict = CachedDict(database=database)

            if clear:
                cached_dict.clear()
            elif load:
                cached_dict.load()
            else:
                pass
            
            self.__setattr__(attr_name, cached_dict)
