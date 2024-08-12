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
NullDatabase.__init__(self, domain, \*kwargs)

  Parameters:
    domain: The domain and optional kwargs.
  Returns:
    (Class constructors have no explicit return value)
  Raises:
    (this function does not raise any notable errors)

.. _moobius.database.null_database.NullDatabase.get_value:

NullDatabase.get_value
---------------------------------------------------------------------------------------------------------------------
NullDatabase.get_value(self, key)

  Parameters:
    key: The key.
  Returns:
    (True, None).
  Raises:
    (this function does not raise any notable errors)

.. _moobius.database.null_database.NullDatabase.set_value:

NullDatabase.set_value
---------------------------------------------------------------------------------------------------------------------
NullDatabase.set_value(self, key, value)

  Parameters:
    key: The key.
    value: The value.
  Returns:
    (True, '').
  Raises:
    (this function does not raise any notable errors)

.. _moobius.database.null_database.NullDatabase.delete_key:

NullDatabase.delete_key
---------------------------------------------------------------------------------------------------------------------
NullDatabase.delete_key(self, key)

  Parameters:
    key: The key.
  Returns:
    (True, '').
  Raises:
    (this function does not raise any notable errors)

.. _moobius.database.null_database.NullDatabase.all_keys:

NullDatabase.all_keys
---------------------------------------------------------------------------------------------------------------------
NullDatabase.all_keys(self)

  Parameters:
    (No parameters in this class constructor)
  Returns:
    The [].
  Raises:
    (this function does not raise any notable errors)

.. _moobius.database.null_database.NullDatabase.__str__:

NullDatabase.__str__
---------------------------------------------------------------------------------------------------------------------
NullDatabase.__str__(self)

The string output function for debugging.
  Parameters:
    (No parameters in this class constructor)
  Returns:
    The  easy-to-read string summary.
  Raises:
    (this function does not raise any notable errors)

.. _moobius.database.null_database.NullDatabase.__repr__:

NullDatabase.__repr__
---------------------------------------------------------------------------------------------------------------------
NullDatabase.__repr__(self)

The string output function for debugging.
  Parameters:
    (No parameters in this class constructor)
  Returns:
    The  easy-to-read string summary.
  Raises:
    (this function does not raise any notable errors)

Class attributes
--------------------

NullDatabase.DatabaseInterface
