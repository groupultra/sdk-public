.. _moobius_database_redis_database:

moobius.database.redis_database
====================================================================================

Module-level functions
===================================================================================

(No module-level functions)

===================================================================================

Class RedisDatabase
===========================================================================================

The redis database make use of a redis.Redis(...) server (Redis servers are set to localhost:6379 by default).
By default uses the domains's hash code to differentiate different domains, unless a user-supplied "db" value is given.

.. _moobius.database.redis_database.RedisDatabase.__init__:

RedisDatabase.__init__
---------------------------------------------------------------------------------------------------------------------
RedisDatabase.__init__(self, domain, host, port, db, password, \*kwargs)

<No doc string>

.. _moobius.database.redis_database.RedisDatabase.get_value:

RedisDatabase.get_value
---------------------------------------------------------------------------------------------------------------------
RedisDatabase.get_value(self, key)

<No doc string>

.. _moobius.database.redis_database.RedisDatabase.set_value:

RedisDatabase.set_value
---------------------------------------------------------------------------------------------------------------------
RedisDatabase.set_value(self, key, value)

<No doc string>

.. _moobius.database.redis_database.RedisDatabase.delete_key:

RedisDatabase.delete_key
---------------------------------------------------------------------------------------------------------------------
RedisDatabase.delete_key(self, key)

<No doc string>

.. _moobius.database.redis_database.RedisDatabase.all_keys:

RedisDatabase.all_keys
---------------------------------------------------------------------------------------------------------------------
RedisDatabase.all_keys(self)

<No doc string>

.. _moobius.database.redis_database.RedisDatabase.__str__:

RedisDatabase.__str__
---------------------------------------------------------------------------------------------------------------------
RedisDatabase.__str__(self)

<No doc string>

.. _moobius.database.redis_database.RedisDatabase.__repr__:

RedisDatabase.__repr__
---------------------------------------------------------------------------------------------------------------------
RedisDatabase.__repr__(self)

<No doc string>
