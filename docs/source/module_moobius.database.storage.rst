.. _moobius_database_storage:

###################################################################################
moobius.database.storage
###################################################################################

******************************
Module-level functions
******************************

.. _moobius.database.storage.get_engine:

get_engine
---------------------------------------------------------------------------------------------------------------------

* Signature

    * get_engine(implementation)

* Parameters

    * implementation: N implementation string.

* Returns

  * The engine's Class. 
  Last-minute-imports the module so that no pip package is needed for unused engines.

* Raises

  * (this function does not raise any notable errors)

************************************
Class CachedDict
************************************

CachedDict is a custom dictionary-like class that inherits from the built-in dict class.
The MagicalStorage class manages the creation of CachedDict instances with different attribute names, allowing users to cache and retrieve data in a structured way, with optional database interaction.

.. _moobius.database.storage.CachedDict.__init__:

CachedDict.__init__
---------------------------------------------------------------------------------------------------------------------

Initialize a CachedDict object.

* Signature

    * CachedDict.__init__(self, database, strict_mode)

* Parameters

    * database: The database to be used, currently supports JSONDatabase and RedisDatabase.
    
    * strict_mode=False: Whether to use strict mode.
        In strict mode, set value will raise exception if database save fails, but the value will still be set in the dict.

* Returns

  * The None.

* Raises

  * (this function does not raise any notable errors)

* Example

    Note: This should not be called directly. Users should call MoobiusStorage to initialize the database.
      >>> cached_dict = CachedDict(database=database, strict_mode=True)

.. _moobius.database.storage.CachedDict.load:

CachedDict.load
---------------------------------------------------------------------------------------------------------------------

Loads all keys from the database to the cache.

* Signature

    * CachedDict.load(self)

* Parameters

    * (this class constructor accepts no arguments)

* Returns

  * The None.

* Raises

  * (this function does not raise any notable errors)

.. _moobius.database.storage.CachedDict.save:

CachedDict.save
---------------------------------------------------------------------------------------------------------------------

Saves a key to the database.. 
For a JSONDatabase, this will create a new json file named after the database's domain and key.

* Signature

    * CachedDict.save(self, key)

* Parameters

    * key: String-valued key.

* Returns

  * The None.

* Raises

  * (this function does not raise any notable errors)

.. _moobius.database.storage.CachedDict.__getitem__:

CachedDict.__getitem__
---------------------------------------------------------------------------------------------------------------------

Overrides dict-like usages of the form: "v = d['my_key']" to query from the database...

* Signature

    * CachedDict.__getitem__(self, key)

* Parameters

    * key: Key and.

* Returns

  * The value.

* Raises

  * A KeyError if strict_mode is True and the key is not found.

.. _moobius.database.storage.CachedDict.__setitem__:

CachedDict.__setitem__
---------------------------------------------------------------------------------------------------------------------

Overrides dict-like usages of the form: "d['my_key'] = v" to save to the database.
For a JSONDatabase, this will save the updated json to a file..

* Signature

    * CachedDict.__setitem__(self, key, value)

* Parameters

    * key: Key.
    
    * value: Value.

* Returns

  * The None.

* Raises

  * (this function does not raise any notable errors)

.. _moobius.database.storage.CachedDict.__delitem__:

CachedDict.__delitem__
---------------------------------------------------------------------------------------------------------------------

Overrides dict-like usages of the form: "del d['my_key']" to delete a key from the database.
For a JSONDatabase, this will save the updated json to a file..

* Signature

    * CachedDict.__delitem__(self, key)

* Parameters

    * key: Key.

* Returns

  * The None.

* Raises

  * (this function does not raise any notable errors)

.. _moobius.database.storage.CachedDict.pop:

CachedDict.pop
---------------------------------------------------------------------------------------------------------------------

Overrides "v = d.pop(k)" to get and delete k from the database..

* Signature

    * CachedDict.pop(self, key, default)

* Parameters

    * key: Key.
    
    * default='__unspecified__': An optional default value.

* Returns

  * The value.

* Raises

  * (this function does not raise any notable errors)

.. _moobius.database.storage.CachedDict.clear:

CachedDict.clear
---------------------------------------------------------------------------------------------------------------------

Overrides "d.clear()" to clear the database.

* Signature

    * CachedDict.clear(self)

* Parameters

    * (this class constructor accepts no arguments)

* Returns

  * The None.

* Raises

  * (this function does not raise any notable errors)

.. _moobius.database.storage.CachedDict.__str__:

CachedDict.__str__
---------------------------------------------------------------------------------------------------------------------

The string output function for debugging.

* Signature

    * CachedDict.__str__(self)

* Parameters

    * (this class constructor accepts no arguments)

* Returns

  * The  easy-to-read string summary.

* Raises

  * (this function does not raise any notable errors)

.. _moobius.database.storage.CachedDict.__repr__:

CachedDict.__repr__
---------------------------------------------------------------------------------------------------------------------

The string output function for debugging.

* Signature

    * CachedDict.__repr__(self)

* Parameters

    * (this class constructor accepts no arguments)

* Returns

  * The  easy-to-read string summary.

* Raises

  * (this function does not raise any notable errors)

Class attributes
--------------------

CachedDict.dict

************************************
Class MoobiusStorage
************************************

MoobiusStorage combines multiple databases together.
Each database becomes one attribute using dynamic attribute creation.

.. _moobius.database.storage.MoobiusStorage.__init__:

MoobiusStorage.__init__
---------------------------------------------------------------------------------------------------------------------

Initialize a MoobiusStorage object.

* Signature

    * MoobiusStorage.__init__(self, service_id, channel_id, db_config)

* Parameters

    * service_id: The id of the service.
    
    * channel_id: The id of the channel.
    
    * db_config=(): The config of the databases, should be a list of config dicts.
          implementation (str) = the type of the database.
          load (bool) = whether to load the database when initializing the database.
          clear (bool) = whether to clear the database when initializing the database.
          name (str) = the name of the json database.
          settings (dict) = misc settings such as Redis port, etc.
          root_dir (str) = the root directory of the all the json files.

* Returns

  * (Class constructors have no explicit return value)

* Raises

  * (this function does not raise any notable errors)

* Example

    >>> storage = MoobiusStorage(service_id='1', channel_id='1', db_config=[{'implementation': 'json', 'load': True, 'clear': False, 'name': 'character', 'settings': {'root_dir': 'data'}}])
      >>> storage.get('character').set_value('1', {'name': 'Alice'})

.. _moobius.database.storage.MoobiusStorage.put:

MoobiusStorage.put
---------------------------------------------------------------------------------------------------------------------

Sets self.attr_name to database (a DatabaseInterface object) for later retrieval. 
load (default True) to load the dict immediatly, clear (default False) to clear the dict and skip loading it.

* Signature

    * MoobiusStorage.put(self, attr_name, database, load, clear)

* Parameters

    * attr_name: The attr name to add dynamically to self, setting it to a CachedDict.
    
    * database: The database.
    
    * load=True: Whether to load the dict in full at startup instead of gradually.
    
    * clear=False: Whether to clear the dict (which deletes the files).

* Returns

  * The None.

* Raises

  * (this function does not raise any notable errors)

.. _moobius.database.storage.MoobiusStorage.add_container:

MoobiusStorage.add_container
---------------------------------------------------------------------------------------------------------------------

Adds a database using the config dict.

* Signature

    * MoobiusStorage.add_container(self, implementation, settings, name, load, clear)

* Parameters

    * implementation: The engine of the database.
    
    * settings: Contains "root_dir" of the json files, for example.
    
    * name: The attribute that will be added to self for later use.
    
    * load=True: Whether to load the database when initializing the database.
    
    * clear=False: Whether to clear the database when initializing the database.

* Returns

  * The None.

* Raises

  * (this function does not raise any notable errors)

* Example

    Note: This is a hidden function, you don't need to call it directly.
      >>> storage = MoobiusStorage(service_id='1', channel_id='1')
      >>> storage.add_container(implementation='json', settings={'root_dir': 'data'}, name='character', load=True, clear=False)

.. _moobius.database.storage.MoobiusStorage.__str__:

MoobiusStorage.__str__
---------------------------------------------------------------------------------------------------------------------

The string output function for debugging.

* Signature

    * MoobiusStorage.__str__(self)

* Parameters

    * (this class constructor accepts no arguments)

* Returns

  * The  easy-to-read string summary.

* Raises

  * (this function does not raise any notable errors)

.. _moobius.database.storage.MoobiusStorage.__repr__:

MoobiusStorage.__repr__
---------------------------------------------------------------------------------------------------------------------

The string output function for debugging.

* Signature

    * MoobiusStorage.__repr__(self)

* Parameters

    * (this class constructor accepts no arguments)

* Returns

  * The  easy-to-read string summary.

* Raises

  * (this function does not raise any notable errors)

Class attributes
--------------------


