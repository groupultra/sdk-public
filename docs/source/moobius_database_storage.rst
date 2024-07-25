.. _moobius_database_storage:

moobius.database.storage
===================================

Module-level functions
===================

.. _moobius.database.storage.get_engine:
get_engine
-----------------------------------
get_engine(implementation)

Returns the engine's Class. Last-minute-imports the module so that no pip package is needed for unused engines.

.. _moobius.database.storage.get_engine._hit:
get_engine._hit
-----------------------------------
get_engine._hit(matches)

<No doc string>

===================

Class CachedDict
===================

CachedDict is a custom dictionary-like class that inherits from the built-in dict class.
The MagicalStorage class manages the creation of CachedDict instances with different attribute names, allowing users to cache and retrieve data in a structured way, with optional database interaction.

.. _moobius.database.storage.CachedDict.__init__:
CachedDict.__init__
-----------------------------------
CachedDict.__init__(self, database, strict_mode)

Initialize a CachedDict object.

Parameters:
  database (DatabaseInterface): The database to be used, currently supports JSONDatabase and RedisDatabase.
  strict_mode=False: Whether to use strict mode.
    In strict mode, set value will raise exception if database save fails, but the value will still be set in the dict.

No return value.

Example:
  Note: This should not be called directly. Users should call MoobiusStorage to initialize the database.
  >>> cached_dict = CachedDict(database=database, strict_mode=True)

.. _moobius.database.storage.CachedDict.load:
CachedDict.load
-----------------------------------
CachedDict.load(self)

Loads all keys from the database to the cache. Returns None.

.. _moobius.database.storage.CachedDict.save:
CachedDict.save
-----------------------------------
CachedDict.save(self, key)

Saves a key to the database. given a string-valued key. Returns None.
For a JSONDatabase, this will create a new json file named after the database's domain and key.

.. _moobius.database.storage.CachedDict.__getitem__:
CachedDict.__getitem__
-----------------------------------
CachedDict.__getitem__(self, key)

Overrides dict-like usages of the form: "v = d['my_key']" to query from the database.
Raises a KeyError if strict_mode is True and the key is not found.

.. _moobius.database.storage.CachedDict.__setitem__:
CachedDict.__setitem__
-----------------------------------
CachedDict.__setitem__(self, key, value)

Overrides dict-like usages of the form: "d['my_key'] = v" to save to the database.
For a JSONDatabase, this will save the updated json to a file.

.. _moobius.database.storage.CachedDict.__delitem__:
CachedDict.__delitem__
-----------------------------------
CachedDict.__delitem__(self, key)

Overrides dict-like usages of the form: "del d['my_key']" to delete a key from the database.
For a JSONDatabase, this will save the updated json to a file.

.. _moobius.database.storage.CachedDict.pop:
CachedDict.pop
-----------------------------------
CachedDict.pop(self, key, default)

Overrides "v = d.pop(k)" to get and delete k from the database.

.. _moobius.database.storage.CachedDict.clear:
CachedDict.clear
-----------------------------------
CachedDict.clear(self)

Overrides "d.clear()" to clear the database.

.. _moobius.database.storage.CachedDict.__str__:
CachedDict.__str__
-----------------------------------
CachedDict.__str__(self)

<No doc string>

.. _moobius.database.storage.CachedDict.__repr__:
CachedDict.__repr__
-----------------------------------
CachedDict.__repr__(self)

<No doc string>

Class MoobiusStorage
===================

MoobiusStorage combines multiple databases together.
Each database becomes one attribute using dynamic attribute creation.

.. _moobius.database.storage.MoobiusStorage.__init__:
MoobiusStorage.__init__
-----------------------------------
MoobiusStorage.__init__(self, service_id, channel_id, db_config)

Initialize a MoobiusStorage object.

Parameters:
  service_id (str): The id of the service.
  channel_id (str): The id of the channel.
  db_config(list): The config of the databases, should be a list of config dicts.
    Dict keys of each element:
      implementation (str): The type of the database.
      load (bool): Whether to load the database when initializing the database.
      clear (bool): Whether to clear the database when initializing the database.
      name (str): The name of the json database.
      settings (dict): Misc settings such as Redis port, etc.
      root_dir (str): The root directory of the all the json files.

Example:
  >>> storage = MoobiusStorage(service_id='1', channel_id='1', db_config=[{'implementation': 'json', 'load': True, 'clear': False, 'name': 'character', 'settings': {'root_dir': 'data'}}])
  >>> storage.get('character').set_value('1', {'name': 'Alice'})

.. _moobius.database.storage.MoobiusStorage.put:
MoobiusStorage.put
-----------------------------------
MoobiusStorage.put(self, attr_name, database, load, clear)

Sets self.attr_name to database (a DatabaseInterface object) for later retrieval.
load (default True) to load the dict immediatly, clear (default False) to clear the dict and skip loading it.

.. _moobius.database.storage.MoobiusStorage.add_container:
MoobiusStorage.add_container
-----------------------------------
MoobiusStorage.add_container(self, implementation, settings, name, load, clear)

Adds a database using the config dict.

Parameters:
  implementation (str): The engine of the database.
  settings (dict): Contains "root_dir" of the json files, for example
  name (str): The attribute that will be added to self for later use.
  load=True: Whether to load the database when initializing the database.
  clear=False: Whether to clear the database when initializing the database.

No return value.

Example:
  Note: This is a hidden function, you don't need to call it directly.
  >>> storage = MoobiusStorage(service_id='1', channel_id='1')
  >>> storage.add_container(implementation='json', settings={'root_dir': 'data'}, name='character', load=True, clear=False)

.. _moobius.database.storage.MoobiusStorage.__str__:
MoobiusStorage.__str__
-----------------------------------
MoobiusStorage.__str__(self)

<No doc string>

.. _moobius.database.storage.MoobiusStorage.__repr__:
MoobiusStorage.__repr__
-----------------------------------
MoobiusStorage.__repr__(self)

<No doc string>
