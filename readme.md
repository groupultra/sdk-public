# Welcome to Moobius Python SDK (Version 1.x.y)!

This readme provides a condensed tutorial. A much more complete reference can be found on [the Read The Docs](https://moobius.readthedocs.io/en/stable/).

## Quick Start

**Setup your account**

Register an account on [Moobius](http://www.moobius.ai). You have to enter an email and password to use this SDK. Third-party logins are not supported.

**Install Python and Moobius**

Make sure you are at least at Python 3.10 with `python --version`. If not, install it from [Python.org](https://www.python.org/downloads/). Also make sure `pip` is isntalled.

Install with `pip install moobius`

Note: It may be "python3" and "pip3" instead of "python" and "pip" if you are not aliasing "python" to python3.

**Create a simple service**

`cd` into a folder of your choice.

Type in `moobius` or `moobius gui`. Enter your email and password (these are the only fields you absolutely need to get a correct configuration). If you are getting a command not found error, you can alternatively use `python -m moobius`.

**Test Moobius**

Start the service with `python service.py` within your folder. Go back to your browser and you should see a new channel in the list of channels. The service is currently running on this channel.

**Experiment!**

Congratulations! Now you have your first Moobius Service. It functions by overriding the base `Moobius` class. The code is driven by async callbacks which can in turn send commands up to the service to i.e. send particular messages to particular users.

Several demos that showcase simple features [are a good starting point](https://github.com/groupultra/Public-CCS-demos).

## Glossary / Reference

Again, a more detailed version of this is available in the read-the-docs.

1. **Tutorials:** In `projects/demo` there are `DemoServiceTutorial.md` and `DemoAgentTutorial.md` walkthroughs.

2. **Service:** The Service handles most of the interaction with the platform SDK. This includes sending and responding to messages, controlling the look and feel, and uploading assets. Callbacks have the format `on_xyz` and actuators have the format `send_xyz`. JSON is automatically converted to and from *dataclasses* within `types.py`. A *CCS* is our term for your custom service that overrides the base Moobius class.

3. **Databases:** Moobius provides a client-side database engine with the `MoobiusStorage` class. The structure is determined by a configuration file (usually `./config/db.json`) or can be hard-coded in your CCS app. Each element has a `name` that *created a dynamic attribute on the MoobiusStorage instance*. Each element also contains an `implementation` which determines the database engine; currently "json" and "redis" are supported.

4. **Logging:** Logging uses [Loguru](https://loguru.readthedocs.io/en/stable/), a colorful, comprehensive logging system. Simply replace `print` with `logging.info()`, `logging.warning()`, or `logging.error()` for a thread-safe logging that also saves to the disk. It has plenty of other features as well.

5. **Wand:** The `MoobiusWand` class launches and manages one or more services. The services can either run on the Wand's process (recommended for simple tasks) or on a seperate process with `background=True`. Using a background service requires moving initialization of unpickable objects to `self.on_start()`. Use `wand.spell()` or `await wand.aspell()` to have the wand interact with the service by calling the `self.on_spell()` callback.

6. **Usermode:** *Usermode is an advanced feature with niche use-cases.* This is a service running with `service_mode` set to False. Instead of a service, it acts as a user who can interact with a service much like a user would. It responds to messages recieved *down* from the serivce (instead of *up* from a user) and sends messages *up* instead of *down*. Instead of *sending* buttons, wigits, and other menus and *recieving* clicks and other interaction, it *recieves* changes to these components and *sends* clicks. **Only use usermode if you need to automate a pre-existing account.** If all you need to do is create AI characters and have them talk, it is much easier to do so using the `service.create_character` function.

## Dict-like databases for easier persistent data manipulation

As mentioned before, databases allow persistant storage and support redis. Each custom attribute of a `MoobiusStorage` instance is a `CachedDict` which in turn implements `__getitem__`, `__setitem__`, and `__delitem__`. This means that it can be used as a dict and will automatically save whenever it is modified. However, the value itself may be in turn a mutable data structure. In which case `CachedDict` will not be aware of this change and a call to `cached_dict.save(key)` is needed to serialize and save the value to the database.

Custom database engines can be implemented by following these steps:
1. Inherit the `DatabaseInterface` class and specifying the engine.
2. Choose a name.
3. Add the name to the `get_engine` function in storage.py.
4. Use the name in the database config file.

In addition to `name` and `implementation`, each database field defined in the configuration has `load` and `clear` booleans. Usually `load` is True and `clear` is False. (Experimental) `load` can be False to not load everything at once for optimization. If `clear` is True, the database will be cleared from the disk on init and `load` does not matter.

## File and Class Organization Details

The code is divided into the core logic, the database, and the network. All the Python code is in the `src/moobius` folder. Again, an exhaustive list is on read-the-docs.

- `core/`: The core logic of the SDK including Services and databases.
   - `sdk.py`: Defines the `Moobius` class which is the main class that aggregates all functions a CCS needs to interact with the Moobius platform. It is the base class of a Service.
   - `storage.py`: Defines `MoobiusStorage` which acts as a container of disk-stored "dictionaries" (`CachedDict` instances). This feature can be used independently of the Moobius class.
   - `wand.py`: Defines `MoobiusWand` which handles all the multiprocessing magic. This can be used independently of the Moobius class.
- `database/`: The infrastructure of `MoobiusStorage`.
   - `database_interface.py`: Defines `DatabaseInterface`, an abstract base class used by each of the below implementations.
   - `null_database.py`: Defines `NullDatabase` which is like `dev/null`.
   - `json_database.py`: Defines `JSONDatabase` which uses json files and stores plaintext.
   - `redis_database.py`: Defines `RedisDatabase` which requires a running Redis server to function.
   - `magical_storage.py`: Defines several classes. `CachedDict` is used like a dictionary but has a database under the hood. `MagicalStorage` is built on `CachedDict` and supports customized on-the-fly `CachedDict` containers.
- `network/`: Network communication with the Platform.
   - `http_api_wrapper.py`: Defines `HTTPAPIWrapper` which mirrors the Platform's low-level HTTP API. Used by `Moobius` instances. Handels HTTPS auth among other tasks.
   - `ws_client.py`: Defines `WSClient` which mirrors the Platform's low-level Socket API. Used by `Moobius` instances. Handles most communication for a running service.
- `types.py`: Defines many dataclasses`Button`, `Canvas`, `View`, `Message`, `MessageBody`, `ButtonClick`, etc. Each class encodes a very simple data-structure and is easily converted to/from a dict.
- `json_utils.py`: Extends JSON read/write functionality.
- `quickstart.py`: This is called when `moobius` is typed into the terminal and sets up a basic service.
