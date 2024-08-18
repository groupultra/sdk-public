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
Dataclass objects can be seralized as well.

.. _moobius.database.json_database.JSONDatabase.__init__:

JSONDatabase.__init__
---------------------------------------------------------------------------------------------------------------------

Initialize a JSONDatabase object.

* Signature

    * JSONDatabase.__init__(self, domain, root_dir, kwargs)

* Parameters

    * domain: Str
        The name of the database directory. Will be automatically added in the add_container() function in MoobiusStorage.
    
    * root_dir='': Str
        The root directory of the all the database files.
    
    * kwargs='': Ignored for this implementation.

* Returns

  * (Class constructors have no explicit return value)

* Raises

  * (this function does not raise any notable errors)

* Example

    Note: This should not be called directly. Users should config the database in the config file, and call MoobiusStorage to initialize the database.
      >>> database = JSONDatabase(domain='service_1.channel_1', root_dir='data')

.. _moobius.database.json_database.JSONDatabase.get_value:

JSONDatabase.get_value
---------------------------------------------------------------------------------------------------------------------

Gets the value (which is a dict).
Note: This "key" is different from a key to look up a CachedDict file.
Note: This function should not be called directly.

* Signature

    * JSONDatabase.get_value(self, key)

* Parameters

    * key: String-valued key.

* Returns

  * The is_sucessful, the_value.

* Raises

  * TypeError: If the type of the value is unknown, so we can't construct the object.

.. _moobius.database.json_database.JSONDatabase.set_value:

JSONDatabase.set_value
---------------------------------------------------------------------------------------------------------------------

Updates and saves a cached dict,.

* Signature

    * JSONDatabase.set_value(self, key, value)

* Parameters

    * key: String-valued key.
    
    * value: A dict-valued value.

* Returns

  * (is_success, the key).
  Note: This function should not be called directly.

* Raises

  * (this function does not raise any notable errors)

.. _moobius.database.json_database.JSONDatabase.delete_key:

JSONDatabase.delete_key
---------------------------------------------------------------------------------------------------------------------

Deletes a cached dict.

* Signature

    * JSONDatabase.delete_key(self, key)

* Parameters

    * key: Key.

* Returns

  * (True, the key)
  Note: This function should not be called directly.

* Raises

  * (this function does not raise any notable errors)

.. _moobius.database.json_database.JSONDatabase.all_keys:

JSONDatabase.all_keys
---------------------------------------------------------------------------------------------------------------------

Gets all the cached dicts in the database.

* Signature

    * JSONDatabase.all_keys(self)

* Parameters

    * (this class constructor accepts no arguments)

* Returns

  * The dicts as an iterable which internally uses yield().

* Raises

  * (this function does not raise any notable errors)

.. _moobius.database.json_database.JSONDatabase.__str__:

JSONDatabase.__str__
---------------------------------------------------------------------------------------------------------------------

The string output function for debugging.

* Signature

    * JSONDatabase.__str__(self)

* Parameters

    * (this class constructor accepts no arguments)

* Returns

  * The  easy-to-read string summary.

* Raises

  * (this function does not raise any notable errors)

.. _moobius.database.json_database.JSONDatabase.__repr__:

JSONDatabase.__repr__
---------------------------------------------------------------------------------------------------------------------

The string output function for debugging.

* Signature

    * JSONDatabase.__repr__(self)

* Parameters

    * (this class constructor accepts no arguments)

* Returns

  * The  easy-to-read string summary.

* Raises

  * (this function does not raise any notable errors)

Class attributes
--------------------

JSONDatabase.DatabaseInterface
