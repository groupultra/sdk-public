.. _src_moobius_database_redis_database:

src.moobius.database.redis_database
===================================

Module-level functions
==================



==================


Class RedisDatabase
==================

The redis database make use of a redis.Redis(...) server (Redis servers are set to localhost:6379 by default).

RedisDatabase.__init__
----------------------
RedisDatabase.__init__(self, domain, host, port, db, password, \*kwargs)
<No doc string>

RedisDatabase.get_value
----------------------
RedisDatabase.get_value(self, key)
<No doc string>

RedisDatabase.set_value
----------------------
RedisDatabase.set_value(self, key, value)
<No doc string>

RedisDatabase.delete_key
----------------------
RedisDatabase.delete_key(self, key)
<No doc string>

RedisDatabase.all_keys
----------------------
RedisDatabase.all_keys(self)
<No doc string>

RedisDatabase.__str__
----------------------
RedisDatabase.__str__(self)
<No doc string>

RedisDatabase.__repr__
----------------------
RedisDatabase.__repr__(self)
<No doc string>