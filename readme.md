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
8. Run `python main.py test` (For Mac OS, it could be `python3 main.py test`). The config file will automatically update with a `service_id` so that you can just use it next time you start the program. You can see from your browser (after refresh) and expect an actively functional service in your band, that
- A Character named "Wand" (not in the character list) would begin to send "SYNC", "ASYNC", "BOMB" and "SURVIVE" messages in order automatically (after 10 seconds).
- The "Wand" will send "Check in every minute" with a timestamp every minute (as it is).
- Has two Keys ("Do Some Magic" and "Swap Stage"). Something obvious will happen in the band when you click them.
- If you type "moobius" in the text input area in your browser, recipients will receive "Moobius is Great!" instead. You can see this when your intended recipients include yourself, and you can also check this with another account joining the same band (be sure to use different browsers if you try multiple accounts on the same machine).
- If you type other text messages, all your intended recipients would receive your messages. You will hear an "echo" from yourself if your intended recipients include yourself (which is the default option of our Web UI where the intended recipients is "All").
- If you send an image, all your intended recipients EXCEPT YOURSELF would receive the image, even if your intended recipients include yourself (you may already be used to this behavior and did not even think it is a thing!).
- If you send the following commands to Service(∞), the band would respond in some way.
  + `hide`: the keys (buttons) would disappear
  + `show`: the keys would reappear
  + `reset`: clear all Mickeys in your character list.
9. Next time you can run `python main.py` or `python3 main.py` without the `test` argument. The test messages beginning with "WAND: " won't be sent on start.

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

## File Organization Structure
`projects/`: Example services. Each subfolder contains a separate service.

`src/moobius`: The source code of the `moobius` package, which includes:

- `core/`: All core features and logic of a Moobius Serivce.
   - `basic_service.py`: `MoobiusBasicService` that defines all `on_xxx()` triggers and `send_xxx()` helper methods (for you to send payloads through websockets.)
   - `service.py`: `MoobiusService` that integrates database and high-level commonly used helper methods. It is the base class of a Service. It has a minimal but complete implementation of a fully functional Moobius Service instance (so that it is runnable!), including authentication, automatic heartbeat and a trivial handler to payloads (print and noops). It is highly recommended that your custom class inherit `MoobiusService` defined here.
   - `storage.py`: `MoobiusStorage` that acts as a container of backed-up dictionaries (`CachedDict` instances)
   - `wand.py`: `MoobiusWand` class that handles all the multiprocessing and remote control magic. 

- `database/`: The infrastructure of `MoobiusStorage`.
   - `database_interface.py`: An abstract class definition of database implementations. As long as the methods defined in the interface are implemented (for a key-value pair), the instance of the concrete class can be used to initialize a `CachedDict` instance.
   - `null_database.py`: A trivial implementation.
   - `json_database.py`: A json file based implementation (simple but useful and intuitive -- you can see the data records easily!)
   - `redis_database.py`: A redis implementation (which requires a redis service on your machine). You are welcome to make MySQL, SQLite or other implementations.
   - `magical_storage.py`: `CachedDict` is a dictionary with a database under the hood, and the changes in the dict will be automatically synchronized to the database. `MagicalStorage` is built on `CachedDict`, which supports customized on-the-fly `CachedDict` containers (`put()`) which can automatically load (`load=True`) from a database on initialization, or automatically clear the database (`clear=True`) to clean out garbage records.

- `network/`: All basic network communications
   - `http_api_wrapper.py`: a pure implementation of low-level HTTP APIs. `MoobiusService` instances have an attribute `self.http_api` of this class.
   - `ws_payload_builder.py`: a pure builder of websocket API payloads.
   - `ws_client.py`: a websocket client based on `websockets` that facilitates exception handling, asynchronous event handling and automatic reconnection attempts on error. `MoobiusService` instances have an attribute `self._ws_client` of this class.

- `types.py`: All relevant dataclasses of a Moobius event (websocket package) payload.
- `utils.py`: Basic utilities like `EnhancedJSONEncoder` which can recognize dataclasses.

## Todo
1. Async http and database
2. HTTP Data Types refactor
3. Documentation
4. Tutorials and better examples
