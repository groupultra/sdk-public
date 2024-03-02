# Welcome to Moobius Python SDK (Version 1.0.0)!

## Quick Start (Requires Python 3.10+)

**Setup your account**

Register an account on [Moobius](http://www.moobius.net). You have to enter an email and password to use this SDK. Third-party logins are not supported.

**Install Moobius**

If you just want to *use* the platform `pip install moobius` is suffficient. However, the SDK is in Beta so it may be desirable to install it in *editable* mode:

1. `git clone` or manually download the sdk-public source code.
2. `cd` into the the src directory (`./src` with respect to this file).
3. `pip install -e .`. Note the lack of a "moobius" argument!

The `e` indicates "editable" and it will install the local package in the given folder to the `PYTHONPATH` instead of pulling from the PyPy site. The file `src/setup.py` tells pip that the name is "Moobius".

**Test Moobius**

Test Moobius by creating a channel, running a Demo feature-suite servicing, and testing the features.

1. In the browser, create a *channel* on Moobius. It will tell you it's unique `channel_id`.
2. `cd` into `projects/demo` (or a copy of this folder).
2. Rename `./config/(example service).json` to `service.json` and  `./config/(example agent).json` to `agent.json`
3. Enter your credentials and the `channel_id` you obtained into `service.json`.
4. (Optional) create an alt-account and enter those credentials into `agent.json`.
5. Add the lines `*/config/service.json` and `*/config/agent.json` to your `.gitignore` to keep these secrets safe!
6. `cd` into the folde and `python main.py`. Make sure it continues to run and does not spew excessive amounts of errors.
7. In the browser, navigate to the channel you created. Hit refresh a few times until you see a list of buttons ("Swap Stage", "Channels", "Commands", etc). It should take around 30 seconds to fully load.
8. Test the various buttons to make sure the button options either work (or give a warning message that they are expiremental).
9. Press "Commands" to see a message with commands to run. Test these commands. Some need to be sent to the "service" instead of the "all" to work. Note that Agent features will only work if the Agent has been setup.

**Expriement!**

Congratulations! Now you have your first Moobius Service. The demo contains `service.py` and `agent.py` which together test most SDK features. Each one overrides the base `MoobiusClient` class. The code is driven by async callbacks which can in turn send commands up to the service to i.e. send particular messages to particular users.

## Glossery / Reference

1. **Tutorials:** In `projects/demo` there are `DemoServiceTutorial.md` and `DemoAgentTutorial.md` walkthroughs.

2. **Service:** The Service handles most of the interaction with the platform SDK. This includes sending and responding to messages, controlling the look and feel, and uploading assets. Callbacks have the format `on_xyz` and actuators have the format `send_xyz`. JSON is automatically converted to and from *dataclasses* within `types.py`.

3. **Agent:** Like *service*, the agent overrides the `MoobiusClient` class and is constructed with `is_agent` set to True. However, the agent is more limited in it's functionality: it cannot do much besides sending and recieving messages and modifying itself. Most other functions will generate an error. To use an agent under a given account requires knowing the secret credentials. Services call `send_message_down` while users and agents call `send_message_up`.

4. **Databases:** Databases are client-side and represented as `MoobiusStorage` instances. The structure is determined by a configuration file (usually `./config/db.json`). Each element has a `name` that is *directly written instance's attributes*. Each element also contains an `implementation` which determines the database engine; currently "json" and "redis" is supported. The Demo by default will only run "redis" on Linux and Mac.

5. **Logging:** Logging uses [Loguru](https://loguru.readthedocs.io/en/stable/), a colorful, comprehensive logging system. Simply replace `print` with `logging.info()`, `logging.error()`, or `logging.error()` for a thread-safe logging that also saves to the disk. It has plenty of other [features](https://loguru.readthedocs.io/en/stable/) as well.

6. **Wand:** The `MoobiusWand` class launches and manages one or more services. The services can either run on the Wand's process (recommended for simple tasks) or on a seperate process with `background=True`. Using a background service requires moving initialization of unpickable objects to `on_start()`. Use `wand.spell()` or `await wand.aspell()` to have the wand interact with the service by calling the `on_spell()` callback.

## Database Details

As mentioned before, databases allow persistant storage and support redis. Each custom attribute of a `MoobiusStorage` instance is a `CachedDict` which in turn implements `__getitem__`, `__setitem__`, and `__delitem__`. This means that it can be used as a dict and will automatically save whenever it is modified. However, the value itself may be in turn a mutable data structure. In which case `CachedDict` will not be aware of this change and a call to `cached_dict.save(key)` is needed to serialize and save the value to the database.

Custom database engines can be implemented by following these steps:
1. Inherit the `DatabaseInterface` class and specifying the engine.
2. Choose a name.
3. Add the name to the `get_engine` function in storage.py.
4. Use the name in the database config file.

In addition to `name` and `implementation`, each database field defined in the configuration has `load` and `clear` booleans. Usually `load` is True and `clear` is False. (Experimental) `load` can be False to not load everything at once for optimization. If `clear` is True, the databasse will be cleared from the disk on init and `load` does not matter.

## File and Class Organization Details

The code is divided into the core logic, the database, and the network.

`projects/demo`: The Demo example Service and Agent. If desired, other Services and/or agents can be put into the projects folder.

`src/moobius`: The source code itself.

- `core/`: The core logic of the SDK including Services, Agents, and databases.
   - `sdk.py`: Defines `MoobiusClient` which integrates database and high-level commonly used helper methods. It is the base class of a Service or Agent.
   - `storage.py`: Defines `MoobiusStorage` which acts as a container of backed-up dictionaries (`CachedDict` instances)
   - `wand.py`: Defines `MoobiusWand` which handles all the multiprocessing and remote control magic. 
- `database/`: The infrastructure of `MoobiusStorage`.
   - `database_interface.py`: Defines `DatabaseInterface`, an abstract base class used by each of the below implementations.
   - `null_database.py`: Defines `NullDatabase` which is like `dev/null`.
   - `json_database.py`: Defines `JSONDatabase` which uses json files and stores plaintext.
   - `redis_database.py`: Defines `RedisDatabase` which requires a running Redis server to function.
   - `magical_storage.py`: Defines several classes. `CachedDict` is used like a dictionary but has a database under the hood. `MagicalStorage` is built on `CachedDict` and supports customized on-the-fly `CachedDict` containers.
- `network/`: Network communication with the Platform.
   - `http_api_wrapper.py`: Defines `HTTPAPIWrapper` which mirrors the Platform's low-level HTTP API. Used by `MoobiusClient` instances.
   - `ws_client.py`: Defines `WSClient` which mirrors the Platform's low-level Socket API. Used by `MoobiusClient` instances.
- `types.py`: Defines the dataclasses: `ButtonArgument` and `Button`, `ButtonClickArgument` and `ButtonClick`, `Stage`, `View`, `Group`, `MessageContext` and `MessageBody`, `Action`, `ChannelInfo`, `Copy` and `Payload` and `CharacterContext` and `Character`. Each class is a very simple data-structure and is easily converted to/from a dict.
- `utils.py`: Defines`EnhancedJSONEncoder` which allows certain classes to be JSON encoded.
