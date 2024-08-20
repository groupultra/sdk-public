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

Class attributes
--------------------

RedisDatabase.DatabaseInterface 

**********************
Internals
**********************
.. toctree::
   :maxdepth: 2

   moobius.database.redis_database_internal_attrs <moobius.database.redis_database_internal_attrs>
