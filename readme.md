# Welcome to Moobius SDK!

## Quick Start

1. Config

- change the values of `config.json`
  - If you don't have a `service_id` or prefer to use a new `service_id`, delete this item. Please notice that the new service_id won't be written to the config file, so you need to copy it manually from the console.
- For `db_config`, currently two types of configurations are supported: json and redis. For json you need to specify `type`: "json" and `root_dir` as your root directory to save the database files. For redis you need to specify `type`: redis and `password` for your redis password. See the Database part for more info.

2. Run `python demo.py`. It creates a `DemoService` object and run the service. It is a simple forwarding service with two test buttons. If the service run successfully, you will find two buttons on the "keyboard" panel and every message you send will be repeated, except that if you send 'ping', you will get 'pong'.

## Build Your Own Service

1. If you want to modify the code and start your own service, please refer to the source code of `demo_service.py`. Basically, you need to write a subclass of `MoobiusService` and implement all the `on_xxx()` methods. There is a trivial noop implementation in `moobius_service.py` which does nothing but printing the messages to the console, and the code in `demo_service.py` could help you understand how it works.

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
- `_logging_config.py`: all things about console logs.

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

1. Database related refactoring, documentations, etc
2. Detailed websocket payloads (channel_info, etc)
3. Non-blocking operations after `start()` (multiprocessing)
4. Async http and database
5. Auto refresh tokens!
6. Tutorials
7. Database safety (lots of work)
8. Data Types!
