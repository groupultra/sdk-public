.. _moobius_database_null_database:

###################################################################################
moobius.database.null_database
###################################################################################

******************************
Module-level functions
******************************

(No module-level functions)

************************************
Class NullDatabase
************************************

The NullDatabase is like /dev/null; nothing is ever stored.
Get returns (True, None) and set/delete return (True, "").

.. _moobius.database.null_database.NullDatabase.__init__:

NullDatabase.__init__
---------------------------------------------------------------------------------------------------------------------

* Signature

    * NullDatabase.__init__(self, domain, kwargs)

* Parameters

    * domain: Domain.
    
    * kwargs='': Optional kwargs.

* Returns

  * (Class constructors have no explicit return value)

* Raises

  * (this function does not raise any notable errors)

.. _moobius.database.null_database.NullDatabase.get_value:

NullDatabase.get_value
---------------------------------------------------------------------------------------------------------------------

* Signature

    * NullDatabase.get_value(self, key)

* Parameters

    * key: Key.

* Returns

  * (True, None).

* Raises

  * (this function does not raise any notable errors)

.. _moobius.database.null_database.NullDatabase.set_value:

NullDatabase.set_value
---------------------------------------------------------------------------------------------------------------------

* Signature

    * NullDatabase.set_value(self, key, value)

* Parameters

    * key: Key.
    
    * value: Value.

* Returns

  * (True, '').

* Raises

  * (this function does not raise any notable errors)

.. _moobius.database.null_database.NullDatabase.delete_key:

NullDatabase.delete_key
---------------------------------------------------------------------------------------------------------------------

* Signature

    * NullDatabase.delete_key(self, key)

* Parameters

    * key: Key.

* Returns

  * (True, '').

* Raises

  * (this function does not raise any notable errors)

.. _moobius.database.null_database.NullDatabase.all_keys:

NullDatabase.all_keys
---------------------------------------------------------------------------------------------------------------------

* Signature

    * NullDatabase.all_keys(self)

* Parameters

    * (this class constructor accepts no arguments)

* Returns

  * The [].

* Raises

  * (this function does not raise any notable errors)

.. _moobius.database.null_database.NullDatabase.__str__:

NullDatabase.__str__
---------------------------------------------------------------------------------------------------------------------

The string output function for debugging.

* Signature

    * NullDatabase.__str__(self)

* Parameters

    * (this class constructor accepts no arguments)

* Returns

  * The  easy-to-read string summary.

* Raises

  * (this function does not raise any notable errors)

.. _moobius.database.null_database.NullDatabase.__repr__:

NullDatabase.__repr__
---------------------------------------------------------------------------------------------------------------------

The string output function for debugging.

* Signature

    * NullDatabase.__repr__(self)

* Parameters

    * (this class constructor accepts no arguments)

* Returns

  * The  easy-to-read string summary.

* Raises

  * (this function does not raise any notable errors)

Class attributes
--------------------

NullDatabase.DatabaseInterface
