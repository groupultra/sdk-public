.. _moobius_database_database_interface:

moobius.database.database_interface
===================================



===================


Class DatabaseInterface
===================

Various database backends need to inherit this interface.
Currently available as of Jan 2024: JSONDatabase, NullDatabase, and RedisDatabase.
Each demo's on_start() function passes calls MoobiusStorage(self.client_id, channel_id, db_config=self.db_config)
Instead of hardcoding self.db_config each demo it stores it as a JSON list, each element of the form:
    {"implementation": "json", "name": "buttons", "load": true, "clear": false,
     "settings": {"root_dir": "json_db"}}
     Where different elements in the list have different "name" values.
To use a config file, pass db_config_path="my/db_config/file.json" into wand.run()
  Wand will pass this kwarg to the MoobiusService object bieng ran.
  The service will load the JSON into self.db_config
Then, in the on_start() function each demo will call MoobiusStorage(self.client_id, channel_id, db_config=self.db_config)
  TODO: This is clumsy and on_start is repetative between demos, refactor this part and maybe others into service functions?
  For each element in db_config the MoobiusStorage will call self.add_container(**config) and use the implementation kwarg as a switchyard.

.. _moobius.database.database_interface.DatabaseInterface.__init__:
DatabaseInterface.__init__
-----------------------------------
**DatabaseInterface.__init__(self, domain, \*kwargs)**

The concrete methods should expect a `domain` parameter as a `str`.
It is used to separate different domains in the same database.
Like different tables in the same database.
Or different folders in the same file system.
The keys inside different domains may overlap, but they are different entries.
For example, two channels may have entries with the same button id.
domains are '.' separated strings, like '<channel_id>.<character_id>'

.. _moobius.database.database_interface.DatabaseInterface.get_value:
DatabaseInterface.get_value
-----------------------------------
**DatabaseInterface.get_value(self, key)**

Returns a tuple of (is_success, value)

.. _moobius.database.database_interface.DatabaseInterface.set_value:
DatabaseInterface.set_value
-----------------------------------
**DatabaseInterface.set_value(self, key, value)**

Returns a tuple of (is_success=True, key) or (is_success=False, err_message)

.. _moobius.database.database_interface.DatabaseInterface.delete_key:
DatabaseInterface.delete_key
-----------------------------------
**DatabaseInterface.delete_key(self, key)**

Returns a tuple of (is_success=True, key) or (is_success=False, err_message)

.. _moobius.database.database_interface.DatabaseInterface.all_keys:
DatabaseInterface.all_keys
-----------------------------------
**DatabaseInterface.all_keys(self)**

Returns an iterable of all keys, the details of which depend on the implementation.

.. _moobius.database.database_interface.DatabaseInterface.__str__:
DatabaseInterface.__str__
-----------------------------------
**DatabaseInterface.__str__(self)**

<No doc string>

.. _moobius.database.database_interface.DatabaseInterface.__repr__:
DatabaseInterface.__repr__
-----------------------------------
**DatabaseInterface.__repr__(self)**

<No doc string>