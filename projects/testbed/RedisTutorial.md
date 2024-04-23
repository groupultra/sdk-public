## Setting up Redis "vanilla" and/or Redis-om on Linux/Bash

Redis is a simple apt-get call. But if redis-stack (an extension to Redis) is desiered it must be manually added to the apt library as shown in the block below (see https://redis.io/docs/install/install-stack/linux/).

This demo does not use docker, for instructions on how to do so see https://redis.io/docs/install/install-stack/docker/.

```
sudo apt-get install redis-server
curl -fsSL https://packages.redis.io/gpg | sudo gpg --dearmor -o /usr/share/keyrings/redis-archive-keyring.gpg
sudo chmod 644 /usr/share/keyrings/redis-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/redis-archive-keyring.gpg] https://packages.redis.io/deb $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/redis.list
sudo apt-get update
sudo apt-get install redis-stack-server
```

Note: 6379 is the default Redis port. (I think) by default the non-stack redis runs on this port and will keep restarting if killed. And shouldn't a tutorial explain how to set the port? Lets use 8984.

## Starting redis

Once that is installed the server can be started (using an & symbol so the shell doesn't block):
```
redis-server --port 8984 --bind localhost &
```
OR
```
redis-stack-server --port 8984 --bind localhost &
```

## Vanilla Redis configuration

Moobius/database/redis.py makes use of the "vanilla" version of redis. Database interfaces are interchangable. The Redis database has the same API as JSON or any other database.

The demo Redis to store how many paychecks are in each currency:
Here is the db.json snippit that configures the Redis:
```
{
    "implementation": "redis",
    "load": true,
    "clear": false,
    "name": "currency",

    "settings": {
        "host":"localhost",
        "port":8984
    }
}
```

If AUTH is configured on localhost (off by default in EC2 instances) a "username" and/or "password" would be required in the settings as well as .gitignoring the file because it would have secrets.

Unfortunatly, this config cannot (I don't think so at least).

## Vanilla Redis use

Under the hood Moobius's use of Redis is very simple, just a dict with a little JSON and string-binary conversion:

```
autosave = False # True would be slow O(N)

def __init__(self, domain='', host="localhost", port=6379, db=0, password="", **kwargs):
    super().__init__(domain, **kwargs)
    logger.info(f'Redis initialized on {host} port {port}')
    self.redis = redis.Redis(host=host, port=port, db=db, password=password)

def get_value(self, key) -> (bool, any):
    if self.redis.exists(key):
        balue = self.redis.get(key)
        return True, json.loads(balue.decode())
    return False, f'Key {key} does not exist'

def set_value(self, key, value) -> (bool, any):
    balue = json.dumps(value, ensure_ascii=False).encode()
    self.redis.set(key, balue)
    if autosave:
        self.redis.save()
    return True, key

def delete_key(self, key) -> (bool, any):
    self.redis.delete(key)
    if autosave:
        self.redis.save()
    return True, key

def all_keys(self) -> any:
    out = self.redis.keys()
    return [k.decode() for k in out]
```

Note: Redis is supposed to save automaticly before exiting when a "kill" command is sent to the process. However, only redis-stack-server, not redis-server, seems to autosave on exit. A single call to channel.database.redis.save() will save *all* changes to the dict.

## Redis OM Setup

**Redis OM requires redis-stack** and provides greater functionality, most notably better integration with object-oriented programming.

```
os.environ['REDIS_OM_URL'] = 'redis://localhost:8984'
```

If there is an AUTH configured on localhost the URL will be formatted like 'redis://:MyPassword@localhost:8984'  or 'redis://MyUsername:MyPassword@localhost:8984'. By default new EC2 instances don't have such an AUTH and so can use the simplier localhost URL. **Be careful to avoid hardcoding secrets!**.

As Redis is an *in-memory* database it is used locally on a machine and when exiting dumps the data into ./dump.rdb

Finally, install the lightweight redis-om wrapper:
```
pip install redis-om
```

## Using redis-om

The redis-om library is very slick to use. It's heavy use of dynamic Python code makes it counter-intuitivie to newcommers; looking at it's source is a like watching 5D chess. However, the querying code is easy to read and write for more familiar users. 

The following defines a simplified enemy class for i.e. a D&D game. Because HashModel is used all fields must be primitives (bools, numbers, and strings). However, JsonModel would allow list and dict-valued fields. Only Fields with index=True can be queried.
```
class Monster(HashModel):
    hp: int
    attk: int = 5 # Default value.
    loot: str = Field(default='{"gold":50, "exp":8}')
```
Note the use of a string for the "collection" attribute. JsonModel would allow more complex, non-flat datastructures. However, Genshin only uses the simpler HashModel given that there is no need to query on thier detailed structure. 

Instances of Model classes behave much like dataclasses and are constructed by supplying key-value pairs. They have a .save() function which saves them back to the database. They also have a unique "pk" which behaves as a disk-savable version of Pythons id().

Redis-om gets very fun and creative when you consider the attributes of Model *classes* instead of Model *instances*. Here is an example query:
```
monsters = Monster.find(Monster.attk > 12 & Monster.hp >= 25 & Monster.hp <= 50).all()
```
This returns a list of monsters with moderate health and a string attack. The all() turns the query into a list; replace all() with delete() to instead remove elements.

Under the hood redis_om gave the Monster class both class-level attributes *and* a constructer that populates instance-level attributes. On top of that it has to overload operators and keep track of complex boolean expressions (which are evaluated when all() is called)!

This is possible because Python is a *very* dynamic language. Functions, class instances, the classes themselves, modules, special forms such __init__ and more are all *first-class objects* and can all be changed at runtime.

## Common errors

Hopefully this section can be skipped!

If the port is already in use, by Redis or another service, this error will appear:
```
#32504:M 25 Jan 2024 03:20:31.429 # Warning: Could not create server TCP listening socket localhost:8984: bind: Address already in use
#32504:M 25 Jan 2024 03:20:31.429 # Failed listening on port 8984 (tcp), aborting.
```

It's easy to query what is on the port (and maybe "sudo kill" unwanted processes):
```
sudo lsof -i :8984 # See what is on this port.
```

If the server is not set up on the port this kind of error will appear:
```
redis.exceptions.ConnectionError: Error 111 connecting to localhost:8984. Connection refused.
```

If the url mismatches the localhost AUTH setting this kind of error will appear when starting Genshins:
```
redis.exceptions.AuthenticationError: AUTH <password> called without any password configured for the default user. Are you sure your configuration is correct?
```
