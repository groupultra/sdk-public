# Welcome to Moobius SDK!

## Quick Start

1. Config
- change the values of `config.json`
    - If you don't have a `service_id` or prefer to use a new `service_id`, make it empty.
    - For `db_config`, currently two types of configurations are supported: json and redis. For json you need to specify `type`: "json" and `root_dir` as your root directory to save the database files. For redis you need to specify `type`: redis and `password` for your redis password.

2. Run `python src/demo.py`. It creates a `DemoAgent` object and run the service. It is a simple forwarding service with one test button. If the service run successfully, you will find a button on the "keyboard" panel and every message you send will be repeated.

## Build Your Own Service

1. If you want to modify the code and start your own agent, please refer to the source code of `demo_agent.py`. Basically, you need to write a subclass of `MoobiusAgent` and implement all the `on_xxx()` methods. There is a trivial noop implementation in `moobius_agent.py` with does nothing but printing the messages to the console, and the code in `demo_agent.py` could help you understand how it works.

2. There are a bunch of helper methods for you to use. For an instance `agent` of `MoobiusAgent` class, you can use the following methods:
    - `agent.send_xxx()`. These are higher level methods for you to send messages through websockets. These are defined in its parent class `MoobiusBasicAgent`. Please see `src/moobius/moobius_basic_agent.py`
    - `agent.http_api.*()`. These are wrapped HTTP APIs you may occasionally use. Please see `src/moobius/basic/http_api_wrapper.py`.
    - `agent.db_helper.*()`. These are database-related operations commonly used.
    - `agent._ws_client.*()`. These are low-level websocket APIs. You are not recommended to call them directly. The methods are defined in `src/moobius/basic/ws_client.py`.
    - `agent.*()` defined in `MoobiusAgent`. These are high-level complex operations that could involve multiple API calls or database operations. There could be more! Please see `src/moobius/moobius_agent.py`

## File structures
`moobius/basic`: Basic utilites
- `http_api_wrapper.py`: a pure implementation of low-level HTTP APIs.
- `ws_message_builder.py`: a pure builder of websocket API messages.
- `ws_client.py`: a websocket client based on `websockets` that facilitates automatic reconnection, exception handling and `asyncio.create_task()` wrapper (so that you can simply use `await` in higher methods.)

`moobius/database`: Database interface with commonly used operations
- `database_helper.py`: The parent class that defines high-level methods (implemented) and low-level methods (not implemented) of database operations. All subclasses should implement all the low-level methods.
- `json_helper.py`: JSON implementation
- `redis_helper.py`: redis implementation

`moobius/moobius_basic_agent.py`: The Base class of a Service. It has a minimal but complete implementation of a fully functional Moobius Service instance (so that it is runnable!), including authentication, automatic heartbeat and a trivial handler to messages (print and noops).

`moobius/moobius_agent.py`: A Service with a built-in database helper (you can set it `None`), and some high level methods. It is highly recommended that your custom class inherit `MoobiusAgent` defined here.


## Todo
1. Database related refactoring, documentations, etc
2. Detailed websocket messages (channel_info, etc)
3. Non-blocking operations after `start()` (multiprocessing)
4. Async http and database
5. Auto refresh!
6. Tutorials


================================ OLD VERSION ====================================


# How to start the server:
Run start_tmux_session.sh, which start redis server and run main.py. If something goes wrong, you could tmux attach -t to the session and check the error log.

# How to clean the database:
Run scourgify.sh, which will delete all the keys except service_id in the database.

# How to setup config:
Please copy sample_config.py and name it as config.py, then fill up the data fields.

# How to customize your channel:
If it is the first time you are running main.py, you need to create a service and bind it with a channel. 
Please uncomment the following lines in main.py and run it once:

```python
# service_id = api_handler.create_service(CHANNEL_DESCRIPTION)
# bind_result = api_handler.bind_service_with_channel(service_id, CHANNEL_ID)
# if bind_result:
#     redis_instance.connection.set("service_id", service_id)
```

To initialize the channel, set visible features and user list, please modify the initialize_data() method in ws_handler.py.
If you create a singleton user with singleton_local_id 'fortune', you could append it in your initialize_data() method.

To create a singleton user, please uncomment the following lines in ws_handler.py and run it once:
```python
# avatar = api_handler.upload_file("fortune.jpg")
# avatar = "https://social-public-bucket-1.s3.amazonaws.com/46fae16b-c72c-455f-aa51-0875d6187019.jpg"
# singleton_local_id = "fortune3"
# username = "fortune"
# nickname = "Ms Fortune"
# description = "I'm Ms Fortune"
# create_singleton_user_result = api_handler.try_create_singleton_service_user(service_id, singleton_local_id, username, nickname, avatar, description)
``` 