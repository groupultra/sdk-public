from dataclasses import dataclass, asdict
from collections.abc import MutableMapping

@dataclass
class Character:
    character_id: str
    username: str
    nickname: str
    avatar: str
    description: str


@dataclass
class Feature:
    feature_id: str
    feature_name: str
    button_text: str
    new_window: bool
    arguments: list


@dataclass
class Stage:
    stage_id: str
    stage_args: dict


@dataclass
class View:
    character_ids: list[str]
    feature_ids: list[str]
    stage_id: str


@dataclass
class Group:
    group_id: str
    character_ids: list[str]


class CachedDict(MutableMapping, dict):
    def __init__(self, database=None, strict_mode=False):
        super().__init__()
        self.database = database or NullDatabase()
        self.strict_mode = strict_mode  
        # in strict mode, set value will raise exception if database save fails
        # but the value will still be set in the dict

    def load(self):
        print('Loading cached dict')
        
        for key in self.database.all_keys():
            self.__getitem__(key)

    def __getitem__(self, key):
        if dict.__contains__(self, key):
            return dict.__getitem__(self, key)
        else:
            is_success, value = self.database.get_value(key)

            if is_success:
                self.__setitem__(key, value)
                return dict.__getitem__(self, key)
            else:
                return dict.__getitem__(self, key)
    
    def __setitem__(self, key, value):
        print('Setting key {k} to {v}'.format(k=key, v=value))
        is_success, err_msg = self.database.set_value(key, value)

        if is_success:
            dict.__setitem__(self, key, value)
        else:
            if self.strict_mode:
                raise Exception(f'Failed to save key {key} to database. {err_msg}')
            else:
                print(f'Failed to save key {key} to database: {err_msg}. Inconsistency may occur.')
                dict.__setitem__(self, key, value)    
    
    def __delitem__(self, key):
        is_success, err_msg = self.database.delete_key(key)

        if is_success:
            dict.__delitem__(self, key)
        else:
            if self.strict_mode:
                raise Exception(f'Failed to delete key {key} from database. {err_msg}')
            else:
                print(f'Failed to delete key {key} from database: {err_msg}. Inconsistency may occur.')
                dict.__delitem__(self,key)
    
    def __iter__(self):
        return dict.__iter__(self)
    
    def __len__(self):
        return dict.__len__(self)
    
    def __contains__(self, x):
        return dict.__contains__(self, x)