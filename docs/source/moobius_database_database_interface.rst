.. _moobius_database_database_interface:

moobius.database.database_interface
====================================================================================

Module-level functions
===================================================================================

(No module-level functions)

===================================================================================

Class DatabaseInterface
===========================================================================================

An bstract base class that is to be inherited by different database backends.
Currently available as of July 2024: JSONDatabase, NullDatabase, and RedisDatabase.

When a MoobiusStorage object is constructed:
>>> MoobiusStorage(self.client_id, channel_id, db_config=self.db_config)
An internal DatabaseInterface is constructed.

Each demo's on_start() function passes calls MoobiusStorage(self.client_id, channel_id, db_config=self.db_config)
The db_config can be a dict or a .json file name. An example:
>>>    [{"implementation": "json", "name": "health_bars", "load": true, "clear": false,
>>>     "settings": {"root_dir": "json_db"}}
>>>    {"implementation": "redis", "name": "mana_bars", "load": true, "clear": false,
>>>     "settings": {"root_dir": "json_db"}}]

The Moobius (service) class, on initialization, create one MoobiusStorage object per channel, unless initalize_channel() is overridden.
Each MoobiusStorage object creates one CachedDict per element in the db-config list, using the "name" to dynamically generate an attribute.
The "implementation" sets the engine to be used by CachedDict.

.. _moobius.database.database_interface.DatabaseInterface.__init__:

DatabaseInterface.__init__
---------------------------------------------------------------------------------------------------------------------
DatabaseInterface.__init__(self, domain, \*kwargs)

Creates the database itself.

The string-valued `domain` parameteras is used to prevent collisions: different domains with the same key are different database entries.
Internally, differnt domains become different tables in the same database or different folders in the same file system.
Currently, the MoobiusStorage names it's domains in a dot-seperated way:
>>> <service_id>.channel_<channel_id>.<name in db_config>.

.. _moobius.database.database_interface.DatabaseInterface.get_value:

DatabaseInterface.get_value
---------------------------------------------------------------------------------------------------------------------
DatabaseInterface.get_value(self, key)

Returns a tuple of (is_success, value).

.. _moobius.database.database_interface.DatabaseInterface.set_value:

DatabaseInterface.set_value
---------------------------------------------------------------------------------------------------------------------
DatabaseInterface.set_value(self, key, value)

Returns a tuple of (is_success=True, key) or (is_success=False, err_message).

.. _moobius.database.database_interface.DatabaseInterface.delete_key:

DatabaseInterface.delete_key
---------------------------------------------------------------------------------------------------------------------
DatabaseInterface.delete_key(self, key)

Returns a tuple of (is_success=True, key) or (is_success=False, err_message).

.. _moobius.database.database_interface.DatabaseInterface.all_keys:

DatabaseInterface.all_keys
---------------------------------------------------------------------------------------------------------------------
DatabaseInterface.all_keys(self)

Returns an iterable of all keys, the details of which depend on the implementation.

.. _moobius.database.database_interface.DatabaseInterface.__str__:

DatabaseInterface.__str__
---------------------------------------------------------------------------------------------------------------------
DatabaseInterface.__str__(self)

<No doc string>

.. _moobius.database.database_interface.DatabaseInterface.__repr__:

DatabaseInterface.__repr__
---------------------------------------------------------------------------------------------------------------------
DatabaseInterface.__repr__(self)

<No doc string>
