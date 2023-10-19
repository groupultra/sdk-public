from moobius.dbtools.magical_storage import MagicalStorage
from moobius.dbtools.simple_json_database import SimpleJSONDatabase
from moobius.basic.types import Character, CharacterContext


if __name__ == '__main__':
    database = SimpleJSONDatabase(domain='test_db', root_dir='.', clear=True)

    storage = MagicalStorage()

    storage.put('test', database=database)

    print(storage.test)
    character = Character(user_id='test', user_context=CharacterContext(nickname='test', description='test', avatar='test'))

    storage.test['a'] = character
    storage.test['b'] = 123
    storage.test['c'] = 'test'
    storage.test['d'] = None
    storage.test['e'] = {'a': 'b', 'c': (1, 2, 3)}  # tuple would be converted to list

    print(storage.test)

