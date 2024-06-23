.. _database-tut:

The DB config
==========================================

It is preferable (although not manditory) to use a JSON file to store the database config. This makes it easier.

The main.py sets the db conf file to "config/db.json". Note: config/service.json is .gitignored but db.json is *not*.
In this db file, create a single-element config with the "name" set to "stats". All the other fields are left as default:

`
[{
    "implementation": "json",
    "name": "stats",
    "load": true,
    "clear": false,
    "settings": {
        "root_dir": "json_db"
    }
}]
`

Using it in the CCS
=======================

A common pattern is to create a "channels" field that is initially empty:

.. code-block:: Python
    self.channels = {} # One MoobiusStorage object per channel.

Then to use the initialize_channel callback:

.. code-block:: Python
    async def initialize_channel(self, channel_id):
        self.channels[channel_id] = MoobiusStorage(self.client_id, channel_id, self.db_config)

The "name" was set to "stats", which becomes an attribute (dynamic attribute setting):

.. code-block:: Python
    default_stats = {'str':1, 'dex':1, 'int':1}
    stats = self.channels[c_id].stats.get(sender, default_stats)

stats.get(sender) itself is a dictionary, and when modified in-place there is no way that the stats can tell.
Thus another assignment call is needed to update the disk. This line of code would not be necessary for vanilla dicts:

.. code-block:: Python
    self.channels[c_id].stats[sender] = stats

The stats are persistent (for each player, on each channel) on app restart.

They are stored in jsondb/service_1234.../channel_1234.../stats/1234....json

JSON vs Redis
==========================================

JSON DB is much easier to set up, but is not considered to have high performance when the number of users grows large.

Redis DB is also supported, and can be used by changing the "implementation" to "redis".

Doing so requires a running Redis server on the correct port; the config can be 

```
"settings": {
    "root_dir": "json_db",
    "host":"localhost",
    "port":1234
}
```