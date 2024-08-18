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

* Signature

    * RedisDatabase.__init__(self, domain, host, port, db, password, kwargs)

* Parameters

    * domain: Domain.
    
    * host='': The host.
    
    * port='localhost': The port.
    
    * db=6379: The db.
    
    * password=None: The password.
    
    * kwargs='': Ignores the extra kwargs.

* Returns

  * (Class constructors have no explicit return value)

* Raises

  * (this function does not raise any notable errors)

.. _moobius.database.redis_database.RedisDatabase.get_value:

RedisDatabase.get_value
---------------------------------------------------------------------------------------------------------------------

* Signature

    * RedisDatabase.get_value(self, key)

* Parameters

    * key: Key.

* Returns

  * (sucess, the value).

* Raises

  * (this function does not raise any notable errors)

.. _moobius.database.redis_database.RedisDatabase.set_value:

RedisDatabase.set_value
---------------------------------------------------------------------------------------------------------------------

* Signature

    * RedisDatabase.set_value(self, key, value)

* Parameters

    * key: Key.
    
    * value: Value.

* Returns

  * (sucess, the key).

* Raises

  * (this function does not raise any notable errors)

.. _moobius.database.redis_database.RedisDatabase.delete_key:

RedisDatabase.delete_key
---------------------------------------------------------------------------------------------------------------------

* Signature

    * RedisDatabase.delete_key(self, key)

* Parameters

    * key: Key.

* Returns

  * (True, the key).

* Raises

  * (this function does not raise any notable errors)

.. _moobius.database.redis_database.RedisDatabase.all_keys:

RedisDatabase.all_keys
---------------------------------------------------------------------------------------------------------------------

* Signature

    * RedisDatabase.all_keys(self)

* Parameters

    * (this class constructor accepts no arguments)

* Returns

  * The list of keys.

* Raises

  * (this function does not raise any notable errors)

.. _moobius.database.redis_database.RedisDatabase.__str__:

RedisDatabase.__str__
---------------------------------------------------------------------------------------------------------------------

The string output function for debugging.

* Signature

    * RedisDatabase.__str__(self)

* Parameters

    * (this class constructor accepts no arguments)

* Returns

  * The  easy-to-read string summary.

* Raises

  * (this function does not raise any notable errors)

.. _moobius.database.redis_database.RedisDatabase.__repr__:

RedisDatabase.__repr__
---------------------------------------------------------------------------------------------------------------------

The string output function for debugging.

* Signature

    * RedisDatabase.__repr__(self)

* Parameters

    * (this class constructor accepts no arguments)

* Returns

  * The  easy-to-read string summary.

* Raises

  * (this function does not raise any notable errors)

Class attributes
--------------------

RedisDatabase.DatabaseInterface
