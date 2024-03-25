.. _src_moobius_database_storage:

src.moobius.database.storage
===================================


Module-level functions
==================

get_engine
----------------------
**get_engine(implementation)**

Only import the database engine that is needed. Returns a Class object given a string.

get_engine._hit
----------------------
**get_engine._hit(matches)**

<No doc string>


==================


Class MoobiusStorage
==================

MoobiusStorage combines multiple databases into a single interface.

The config file to specify this database should be a list of dicts. The dict parameters are:
  implementation (str): The type of the database.
  load (bool): Whether to load the database when initializing the database.
  clear (bool): Whether to clear the database when initializing the database.
  name (str): The name of the json database.
  settings (dict): Misc settings such as Redis port, etc.
  root_dir (str): The root directory of the all the json files.

MoobiusStorage.__init__
----------------------
**MoobiusStorage.__init__(self, service_id, channel_id, db_config)**

Initialize a MoobiusStorage object.

Parameters:
  service_id (str): The id of the service.
  channel_id (str): The id of the channel.
  db_config(list): The config of the databases, should be a list of config dicts.
    Each dict's 'implemetation' selects the engine. (TODO? use the field 'engine' instead of 'implementation'?)

No return value.

Example:
  >>> storage = MoobiusStorage(service_id='1', channel_id='1', db_config=[{'implementation': 'json', 'load': True, 'clear': False, 'name': 'character', 'settings': {'root_dir': 'data'}}])
  >>> storage.get('character').set_value('1', {'name': 'Alice'})

MoobiusStorage.put
----------------------
**MoobiusStorage.put(self, attr_name, database, load, clear)**

Sets self.attr_name to database (a DatabaseInterface object) for later retrieval.
load (default True) to load the dict, clear (default False) to clear the dict and skip loading it.

MoobiusStorage.add_container
----------------------
**MoobiusStorage.add_container(self, implementation, settings, name, load, clear)**

Add a database using the config dict.

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

MoobiusStorage.__str__
----------------------
**MoobiusStorage.__str__(self)**

<No doc string>

MoobiusStorage.__repr__
----------------------
**MoobiusStorage.__repr__(self)**

<No doc string>