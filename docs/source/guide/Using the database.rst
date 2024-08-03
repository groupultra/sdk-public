.. _database-tut:

###################################################################################
Dicts for the disk
###################################################################################

Moobius offers built-in database engines to get you started.

A dict-like storage
==========================================

Databases allow dict-like interaction with datastructures that persist on the disk.

This is accompleshed by overriding __getitem__, __setitem__ and other Python magic methods that are used as operator overloads.


MoobiusStorage objects
==========================================

Data is stored in MoobiusStorage objects.

The constructor is:

.. code-block:: Python

    storage = MoobiusStorage(client_id, channel_id, db_config=self.db_config)

Note that "client_id" and "channel_id" need not coorespond to an actual client and channel, any string will do.

The value "db_config" is a list of dicts, for example:

`
[{
    "implementation": "json",
    "name": "stats",
    "load": true,
    "clear": false,
    "settings": {
        "root_dir": "json_db"
    }
},
{
    "implementation": "redis",
    "name": "profiles",
    ...
},
]
`

The "json" implementation is easier to work with. The "redis" implementation has higher performance.
Each "name" attribute becomes one attribute of the MoobiusStorage instance, and it is interacted with as if it is a dict:


.. code-block:: Python

    x = storage.stats['HP']
    storage.profiles['John'] = "Profile." # This autosaves to disk or the DB engine.

There is a *slight* difference between using this and using a dict. In-place modifications to the dict should be saved:

.. code-block:: Python

    x.storage["ShyGuy"]["Happiness"] += 1 # The DB cannot detect that an in-place change was made.
    x.storage.save("ShyGuy")

These databases support nested lists, dicts, sets, and also custom dataclasses.


Per-channel storage convention
==========================================

It's common to make one MoobiusStorage per channel.

To do so, a db conf file such as "config/db.json" can be created and passed in as the "db_config" kwarg for the Moobius constructor.

If such a config is specified, "service.channel_storages" is automatically populated during "initialize_channel".

Setting the storages up this way moves configuration parameters outside of the core service Python code and can make the code cleaner.

JSON vs Redis
==========================================

The "json" implementation is easier to set up but is not considered to have high performance when the number of users grows large.

A redis implemetnation is also supported as well. It requires a running Redis server
that is refrenced in the db_config. For example:

```
"settings": {
    "root_dir": "redis_db",
    "host":"localhost",
    "port":6379
}
```

Demo code
================================
The demo code is available on

`the public repo <https://github.com/groupultra/sdk-public/tree/main/projects/Database>`.
