.. _moobius_database_redis_database:

###################################################################################
moobius.database.redis_database
###################################################################################

******************************
Module-level functions
******************************

(No module-level functions)

************************************
Class RedisDatabase
************************************

The redis database make use of a redis.Redis(...) server (Redis servers are set to localhost:6379 by default).
By default uses the domains's hash code to differentiate different domains, unless a user-supplied "db" value is given.

.. _moobius.database.redis_database.RedisDatabase.__init__:

RedisDatabase.__init__
---------------------------------------------------------------------------------------------------------------------
RedisDatabase.__init__(self, domain, host, port, db, password, \*kwargs)

Also optional kwargs.
  Parameters:
    domain: The domain.
    host: The host.
    port: The port.
    db: The db.
    password: The password.
  Returns:
    (Class constructors have no explicit return value)
  Raises:
    (this function does not raise any notable errors)

.. _moobius.database.redis_database.RedisDatabase.get_value:

RedisDatabase.get_value
---------------------------------------------------------------------------------------------------------------------
RedisDatabase.get_value(self, key)

  Parameters:
    key: The key.
  Returns:
    (sucess, the value).
  Raises:
    (this function does not raise any notable errors)

.. _moobius.database.redis_database.RedisDatabase.set_value:

RedisDatabase.set_value
---------------------------------------------------------------------------------------------------------------------
RedisDatabase.set_value(self, key, value)

  Parameters:
    key: The key.
    value: The value.
  Returns:
    (sucess, the key).
  Raises:
    (this function does not raise any notable errors)

.. _moobius.database.redis_database.RedisDatabase.delete_key:

RedisDatabase.delete_key
---------------------------------------------------------------------------------------------------------------------
RedisDatabase.delete_key(self, key)

  Parameters:
    key: The key.
  Returns:
    (True, the key).
  Raises:
    (this function does not raise any notable errors)

.. _moobius.database.redis_database.RedisDatabase.all_keys:

RedisDatabase.all_keys
---------------------------------------------------------------------------------------------------------------------
RedisDatabase.all_keys(self)

  Parameters:
    (No parameters in this class constructor)
  Returns:
    The list of keys.
  Raises:
    (this function does not raise any notable errors)

.. _moobius.database.redis_database.RedisDatabase.__str__:

RedisDatabase.__str__
---------------------------------------------------------------------------------------------------------------------
RedisDatabase.__str__(self)

The string output function for debugging.
  Parameters:
    (No parameters in this class constructor)
  Returns:
    The  easy-to-read string summary.
  Raises:
    (this function does not raise any notable errors)

.. _moobius.database.redis_database.RedisDatabase.__repr__:

RedisDatabase.__repr__
---------------------------------------------------------------------------------------------------------------------
RedisDatabase.__repr__(self)

The string output function for debugging.
  Parameters:
    (No parameters in this class constructor)
  Returns:
    The  easy-to-read string summary.
  Raises:
    (this function does not raise any notable errors)

Class attributes
--------------------

RedisDatabase.DatabaseInterface
