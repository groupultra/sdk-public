## Agents are accounts

To make a user first create an account. Put these credentials into config/agent.json and .gitignore the file:
```
{
    "http_server_uri": "https://api.sociyoo.com/",
    "ws_server_uri": "wss://ws.sociyoo.com/",
    "email": "<agent email>",
    "password": "<agent password>"
}
```

To run a user it is first necessary to log in and join a channel (TODO: automatic way to do this). Do so by clicking on "Join Channel" (if it isn't already selected) and pasting in the channel ID. **If the agent is not showing up at all make sure it is joined to this channel and not used by any other app**.

It's also fun to customize the profile pic. Click the user icon at the top left and click on "settings". Click on "profile picture" and a filebrowser should open. Ideally the pictures are square. 256x256 resolution is sufficient.

## Using a user

Agents, like Services, inherit from the SDK base class. There is a lot of similarity between these two objects: Both have HTTP and Socket APIs to interact with the platform. Both have a client_id and authenticate against it.
Once the agent is all set up it needs to be ran alongside the service. Note the "is_agent=True" which makes the SDK base class run slightly different code on construction and set self.is_agent to True.
```
agent_handle = wand.run(
    DemoAgent,
    log_file="logs/agent.log",
    error_log_file="logs/error.log",
    config_path="config/agent.json",
    db_config_path="config/agent_db.json",
    is_agent=True,
    background=True)
```

## Agents vs Services

Although there is a lot in common, agents have some functions that are different than services. Most notabaly:
1. The login API is slighly different:
```
message = {
    "type": "user_login", # Instead of "service_login"
    "request_id": str(uuid.uuid4()),
    "auth_origin": "cognito" or "oauth2",
    "access_token": access_token
}
```
The SDK provides seperate agent self.send_agent_login() and self.send_service_login()

2. Some SDK actuator functions are specific to use as a user (and conversly, service-specific functions will not be used). For example agents cannot "send_update_buttons".

3. The set of callbacks that are generally used is quite different. `on_update` functions such as `on_update_canvas` are dispatched when the service updates the canvas, for example.

There are also fetch callbacks such as `send_fetch_channel_info`.

TODO more comprehensive tested list of what fns work with or without the agent.
