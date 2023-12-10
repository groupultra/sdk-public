# Welcome to Moobius Python SDK (Version 0.0.1)!

## Quick Start

+ Install, Service Config and Test Run

Steps: 
- Preparation
1. Register an account on http://www.moobius.app (you have to have an email and password to use this SDK. Third-party login not supported).
2. Create a band with your account and copy the `band_id` (referred below as `channel_id`).

- Install the SDK on your computer/server
3. Use `git clone` or download the source code from this repository (and unzip it)
4. Change current directory to `src/` on your terminal
5. Run `pip install -e .` (for Mac OS, it could be `pip3 install -e .`). This command will install the package `moobius` to your `PYTHONPATH`.
   + Note: `-e` means editable mode. With this option your changes to the source code will take effect immediately.

- Run a demo (test) service
6. Change current directory on your terminal to `projects/demo/`
7. Copy `projects/service.json` to `projects/demo/`, and edit the copied json file. Fill in your `email`, `password` and a list of `channels` you want to run on. If you have a `service_id`, just fill in the field, otherwise please use `"service_id": ""` and the SDK will create a new `service_id` for you and write back to `service.json` for future use.
   + Note: A channel previously binded to a `service_id` could not be binded again to a different `service_id`, unless the original service unbinds first. 
8. Run `python main.py` (For Mac OS, it could be `python3 main.py`). The config file will automatically update so that you don't need to configure it the next time you start the program. You can see from your browser (after refresh) and expect an actively functional service in your band, that
- Would begin to "SYNC", "ASYNC", "BOMB" and "SURVIVE" messages in order automatically (after 10 seconds).
- Has two Keys ("Do Some Magic" and "Swap Stage"). The band would respond when you click them.
- Will respond a "Moobius is Great!" to a "moobius" message, and repeat other messages. If you use another account and join the same band, you will observe a functional group chat service, but any "moobius" sent would become "Moobius is Great!" on the recipients' side.
- If you send the following commands to Service(∞), the band would respond in some way.
  + `hide`: the keys (buttons) would disappear
  + `show`: the keys would reappear
  + `reset`: clear all Mickeys in your character list.

Congratulations! Now you have your first Moobius Service.

## Core Features
1. Tutorial
- Writing a service can be fun and challenging, and we are trying to write tutorials for it to be easy and smooth. Right now we don't have that kind of detailed documentation, and we suggest you read (and modify) the code of the demo service as a starting point. You can use some of the code and "template" for your own service (for example, the `on_join_channel` and `on_leave_channel` methods).

2. Service
- To be brief, your own service should be a subclass of `MoobiusService` and you should implement all the `on_xxx()` methods defined in `MoobiusBasicService` that would be triggered by user-generated events (`msg_up`, `join_channel`, `feature_call`, etc). There are a bunch of helper methods like `send_xxx()` for you to use in your handler methods.

3. Database
- A service could be quiet simple, or dazzlingly complicated. You have the power to control every user's experience in your band -- everything they see on the stage and character list, and every consequence of their messages and key clicks. Each user's view could be independent (for example, each user would see different number of Mickeys), so that it is vital to have a database doing this. We have implemented a `MoobiusStorage` class for you to use with minimum extra effort. It magically turns a key-value pair database into a python `dict` that automatically synchronizes with the database under the hood (could be json file or redis service now, but new implementations are welcome!). See below for details.

4. Logging
- We use loguru for a colorful, comprehensive logging system. You can see the logs on your console and in the log files. All you need to do is to use functions like `logging.info()` or `logging.error()` instead of `print()` in your code. For advanced usage, please see the documentation of loguru.

5. Wand
- Here comes the most delicious part. The `MoobiusWand` is not only a loader of your service, but a remote controller of your services that allows you to "manually" control your service *AFTER* it starts. A wand can controll more than one background services (`background=True`) and you can call `wand.spell()` or `await wand.aspell()` in another (independent) script to use you service as an platform of output (say, you wrote another weather forecast program and notify your bands whenever it seems to start raining besides the original service logic). You just need to implement `on_spell()` and write a protocol between your band and the wand.

- If you use background service, please avoid initializing of complex data types (such as a scheduler or an OpenAI client) in `__init__()`, which may cause pickling issues. In most cases, these attributes could be initialized in `on_start()` method instead.

- You may need to Press `Ctrl + C` multiple times if you want to stop your service (it could have multiple process plus `asyncio` loops and tasks). In some cases you may see a latent `KeyboardInterrupt` Error with stacktrace printed even after you already started your service again. That's normal! It's just the aftermath of your last `Ctrl + C` (and we are working on fixing this).

## Database

+ Database Config: `config/db.json` in `projects/<your_project>`. You can put any `name` that is a valid python identifier as the name the attribute of a `MoobiusStorage` instance to store your data (in case your program need to restart). Currently two types of configurations are supported: json and redis. For json you need to specify `implementation: "json"` and `root_dir` as your root directory to save the database files. For redis you need to specify `implementation: "redis"` and `password` for your redis password (you should have a redis service already running on your machine, of course). See the Database part for more info. Each database can be configured independently. If `clear` is set, everything in the database would be erased during the initialization of the service. If `load` is set, the service will load a copy from the database to the memory during initialization.
1. Data types supported are built-in types (list, dict, int, str, etc) and all dataclass types defined in `types.py`
2. PITFALL! Be careful when you modify a mutable object in your database record, the memory wouldn't be updated. You have to reassign it to the band or call `save()` method explicitly. (all abstractions are leaky!)

For example:
```python
self.bands[channel_id].data = {'key': 1}   # memory: 1, disk: 1
self.bands[channel_id].data = {'key': 2}   # memory: 2, disk: 2
```

But
```python
self.bands[channel_id].data = {'key': 1}   # memory: 1, disk: 1
self.bands[channel_id].data['key'] = 2   # memory: 2, disk: 1
# Not saved!
# The change will not be detected as the id of the dict did not change
```

Hence you should
```python
self.bands[channel_id].data = {'key': 1}   # memory: 1, disk: 1
self.bands[channel_id].data['key'] = 2   # memory: 2, disk: 1 (not saved!)
self.bands[channel_id].data = self.bands[channel_id].data   # Weird, right? Know about setState() in React.js?
```
or, alternatively
```python
self.bands[channel_id].data = {'key': 1}   # memory: 1, disk: 1
self.bands[channel_id].data['key'] = 2   # memory: 2, disk: 1 (not saved!)
self.bands[channel_id].save('data')   # A more graceful way to do this.
```

## File Structures

1. If you want to modify the code and start your own service, please refer to the source code of `projects/demo/service.py`.  Basically, you need to write a subclass of `MoobiusService` and implement all the `on_xxx()` methods. There is a trivial noop implementation in `moobius_service.py` which does nothing but printing the messages to the console, and the code in `demo_service.py` could help you understand how it works.

2. There are a bunch of helper methods for you to use. For an instance `service` of `MoobiusService` class, you can use the following methods:

   - `service.send_xxx()`. These are higher level methods for you to send payloads through websockets. These are defined in its parent class `MoobiusBasicService`. Please see `moobius/moobius_basic_service.py`.
   - `service.http_api.*()`. These are wrapped HTTP APIs you may occasionally use. Please see `moobius/basic/http_api_wrapper.py`.
   - `service._ws_client.*()`. These are low-level websocket APIs. You are not recommended to call them directly. The methods are defined in `moobius/basic/ws_client.py`.
   - `service.*()` defined in `MoobiusService`. These are high-level complex operations that could involve multiple API calls or database operations. There could be more! Please see `moobius/moobius_service.py`.

## File structures

`moobius/basic`: Basic utilites

- `http_api_wrapper.py`: a pure implementation of low-level HTTP APIs.
- `ws_payload_builder.py`: a pure builder of websocket API payloads.
- `ws_client.py`: a websocket client based on `websockets` that facilitates automatic reconnection, exception handling and `asyncio.create_task()` wrapper (so that you can simply use `await` in higher methods.)
- `_types.py`: definition of all datatypes.
- `logging_config.py`: all things about console logs.

`moobius/moobius_basic_service.py`: The Base class of a Service. It has a minimal but complete implementation of a fully functional Moobius Service instance (so that it is runnable!), including authentication, automatic heartbeat and a trivial handler to payloads (print and noops).

`moobius/moobius_service.py`: A Service with a built-in database helper (you can set it `None`), and some high level methods. It is highly recommended that your custom class inherit `MoobiusService` defined here.

## Database

On JSON-based file db, it involves some trick to build a dict-like `MagicalStorage` with automatic DB sync (including sync after restart) independent of database implementation, and customizable domains (you can add custom attributes as needed).

1. `moobius/basic/_types.py`

- Dataclasses are defined(`Character`, `Stage`, etc).

2. `moobius/dbtools`

- `CachedDict` is a dictionary with a database under the hood, and the changes in the dict will be automatically synchronized to the database.
- An abstract class `DatabaseInterface` is defined in `database_interface.py`. As long as the methods defined in the interface are implemented (for a key-value pair), the instance of the concrete class can be used to initialize a `CachedDict` instance.
- A functional JSON implementation is defined in `simple_json_database.py`, so as `simple_redis_database.py`. You are welcome to make MySQL, SQLite or other implementations.
- `magical_storage.py` has a class `MagicalStorage` built on `CachedDict`, which supports customized on-the-fly `CachedDict` containers (`put()`) which can automatically load (`load=True`) from a database on initialization, or automatically clear the database (`clear=True`) to clean out garbage records.

3. How to use:

- An instance of class `MoobiusBand` contains all dbs defined in the `db_settings` file; when initiating the service instance, you shall pass a `db_config` argument explicitly.
- The initialization makes the `MoobiusBand` contain all db interface. For a `MoobiusBand` instance called `band` and a db called `foo`, you can refer to `band.foo`; codes like `band.foo['bar'] = 'some_value'` can access to the db and update values. `del` keyword removes KV pair in db.
- If json is used, `root_dir` indicates where to save these json files.

# Dataclasses

Define them!

## Todo
1. Async http and database
2. HTTP Data Types
3. Ctrl + C multiple times, why
4. Documentation
5. Tutorials and better examples
6. Unbind `others`
