.. _moobius_database_json_database:

moobius.database.json_database
===================================



===================


Class JSONDatabase
===================

JSONDatabase simply stores information as JSON strings in a list of files.

.. _moobius.database.json_database.JSONDatabase.__init__:
JSONDatabase.__init__
-----------------------------------
**JSONDatabase.__init__(self, domain, root_dir, \*kwargs)**

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

.. _moobius.database.json_database.JSONDatabase.get_value:
JSONDatabase.get_value
-----------------------------------
**JSONDatabase.get_value(self, key)**

Gets the value (which is a dict) of a string-valued key. Returns (is_success, the_value).
Note: This function should not be called directly.

Raises:
  TypeError: If the type of the value is unknown, so we can't construct the object.

.. _moobius.database.json_database.JSONDatabase.set_value:
JSONDatabase.set_value
-----------------------------------
**JSONDatabase.set_value(self, key, value)**

Set the value (a dict) of a key (a string). Returns (is_success, the_key).
Note: This function should not be called directly.

.. _moobius.database.json_database.JSONDatabase.delete_key:
JSONDatabase.delete_key
-----------------------------------
**JSONDatabase.delete_key(self, key)**

Delete a (string-valued) key. Returns (is_success, key)
Note: This function should not be called directly.

.. _moobius.database.json_database.JSONDatabase.all_keys:
JSONDatabase.all_keys
-----------------------------------
**JSONDatabase.all_keys(self)**

Gets all keys in the database. Returns an iterable which internally uses yield().

.. _moobius.database.json_database.JSONDatabase.__str__:
JSONDatabase.__str__
-----------------------------------
**JSONDatabase.__str__(self)**

<No doc string>

.. _moobius.database.json_database.JSONDatabase.__repr__:
JSONDatabase.__repr__
-----------------------------------
**JSONDatabase.__repr__(self)**

<No doc string>

.. _moobius.database.json_database.JSONDatabase.all_keys.key_iterator:
JSONDatabase.all_keys.key_iterator
-----------------------------------
**JSONDatabase.all_keys.key_iterator()**

<No doc string>