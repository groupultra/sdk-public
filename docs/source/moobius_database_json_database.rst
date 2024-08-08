.. _moobius_database_json_database:

###################################################################################
moobius.database.json_database
###################################################################################

******************************
Module-level functions
******************************

(No module-level functions)

************************************
Class JSONDatabase
************************************

JSONDatabase simply stores information as JSON strings in a list of files.
Each domain, key combination is stored as one file.
Dataclass objects can be seralized as wll.

.. _moobius.database.json_database.JSONDatabase.__init__:

JSONDatabase.__init__
---------------------------------------------------------------------------------------------------------------------
JSONDatabase.__init__(self, domain, root_dir, \*kwargs)


Initialize a JSONDatabase object.
  Parameters:
    domain: The str
        The name of the database directory. Will be automatically added in the add_container() function in MoobiusStorage.
    
    root_dir: The str
        The root directory of the all the database files.
    
    Example: 
    
    Note: The This should not be called directly. Users should config the database in the config file, and call MoobiusStorage to initialize the database.
      >>> database = JSONDatabase(domain='service_1.channel_1', root_dir='data').
  Returns:
    (Class constructors have no explicit return value)
  Raises:
    (this function does not raise any errors of its own)


.. _moobius.database.json_database.JSONDatabase.get_value:

JSONDatabase.get_value
---------------------------------------------------------------------------------------------------------------------
JSONDatabase.get_value(self, key)


Gets the value (which is a dict).
Note: This "key" is different from a key to look up a CachedDict file.
Note: This function should not be called directly.
  Parameters:
    key: The string-valued key.
  Returns:
    The is_sucessful, the_value.
  Raises:
    TypeError: If the type of the value is unknown, so we can't construct the object.


.. _moobius.database.json_database.JSONDatabase.set_value:

JSONDatabase.set_value
---------------------------------------------------------------------------------------------------------------------
JSONDatabase.set_value(self, key, value)


Updates and saves a cached dict,.
  Parameters:
    key: The string-valued key.
    
    value: The  dict-valued value.
  Returns:
    (is_success, the key).
    Note: This function should not be called directly.
  Raises:
    (this function does not raise any errors of its own)


.. _moobius.database.json_database.JSONDatabase.delete_key:

JSONDatabase.delete_key
---------------------------------------------------------------------------------------------------------------------
JSONDatabase.delete_key(self, key)


Deletes a cached dict.
  Parameters:
    key: The key.
  Returns:
    (True, the key)
    Note: This function should not be called directly.
  Raises:
    (this function does not raise any errors of its own)


.. _moobius.database.json_database.JSONDatabase.all_keys:

JSONDatabase.all_keys
---------------------------------------------------------------------------------------------------------------------
JSONDatabase.all_keys(self)


Gets all the cached dicts in the database.
  Parameters:
    (No parameters in this class constructor)
  Returns:
    The dicts as an iterable which internally uses yield().
  Raises:
    (this function does not raise any errors of its own)


.. _moobius.database.json_database.JSONDatabase.__str__:

JSONDatabase.__str__
---------------------------------------------------------------------------------------------------------------------
JSONDatabase.__str__(self)


The string output function for debugging.
  Parameters:
    (No parameters in this class constructor)
  Returns:
    The  easy-to-read string summary.
  Raises:
    (this function does not raise any errors of its own)


.. _moobius.database.json_database.JSONDatabase.__repr__:

JSONDatabase.__repr__
---------------------------------------------------------------------------------------------------------------------
JSONDatabase.__repr__(self)


The string output function for debugging.
  Parameters:
    (No parameters in this class constructor)
  Returns:
    The  easy-to-read string summary.
  Raises:
    (this function does not raise any errors of its own)


Class attributes
--------------------

JSONDatabase.DatabaseInterface
