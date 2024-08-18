# Set up a simple demo using moobius

This tutorial sets up a basic demo which showcases the essential usage of Moobius. Almost all of the code is in ./service.py

## Configuration and "channels"

Once Moobius is installed (see the quickstart guide) you need to create a *channels* and link the app to the channels. Each backend SDK app is associated with one more channels.

To create a channel, log into Moobius via the browser and create a new channel (click the + next to My channels).
Enter a nice *name* and *description*, such as "Demo" and "This-is-my-test". Doing so will see the *channel ID* (example: "2c76aba1-73f4-4834-55f5-7ac8431640b1"). Alternativlty, the channel ID of the currently selected channel is shown in the URL. It is also possible to join channels by entering an ID.

To delete a channel that you created, click the ... and select "Leave channel".

Create config/service.json with this format to link it to your account:
```
{
    "http_server_uri": "https://api.sociyoo.com/",
    "ws_server_uri": "wss://ws.sociyoo.com/",
    "email": "<Moobius login email>",
    "password": "<Moobius login password>",
    "service_id": "",
    "channels": [
        "<channel id>"
    ],
    "others": "ignore"
}
```
Since it contains credentials the folder should be in secured and this file .gitignore'ed.
Service_id will be filled out when the program first runs and is used internally. There is also config/db.json, which sets the database engine rules. For now it should not be changed.

## Database engines "implementations"

This demo tests both internal Moobius JSON and Redis db engines. See RedisTutorial.md for setting up Redis.
As Redis is Linux software by default Redis is disabled on Windows, this behavior can be changed by changing "avoid_redis" at the top of ./service.py.
RedisTutorial.md provides instructions as to how to set up a localhost-based Redis server.

The database configuration in our case is stores in *config/db.json*. It is a list of configurations. Here is one element of the list:
```
{
    "implementation": "json",
    "load": true,
    "clear": true,
    "name": "real_characters",

    "settings": {
        "root_dir": "json_db"
    }
}
```
To create a moobius storage object, call it's constructor with this configuration:
**channel = MoobiusStorage(self.client_id, channel_id, db_config=json.load("./config/db.json"))**
channel.service_id and channel.channel_id are set to the client_id and channel_id respectivly.
Each element's "implementation", in this case "json", determines the engine to use.
Each element's "name", in this case "real_characters", creates an attribute of channel dynamically.
This means that channel.real_characters is set to an initally empty **CachedDict**. Modifications to the dict will automatically keep the database up-to-date, there is no need to manually call save().
The "settings" stores engine-dependent parameters.

## Platform GUI structure

All created and joined channels will be shown in the list at the left panel.

Each channel has it's own GUI independent of the others. There is a chat history, a collapsable *canvas* to show images and text, and a *character list*. On the right there is a list of characters who may be real users or AI bots.

**The GUI state can be set independently per-user**. This means one user could see characters Alice and Bob while another sees Charlie and Dave. This provides flexibility for a wide variety of social deduction games, study groups, etc.

## Launching

Launching uses the *MoobiusWand* class to run your custom class:
```
from moobius import MoobiusWand
if __name__ == "__main__":
    wand = MoobiusWand()
    
    handle = wand.run(
        <YourCustomClassType>,
        config_path="config/service.json",
        db_config_path="config/db.json",
        background=True
    )
```
In our example, YourCustomClassType = service.DemoService, as defined in service.py.
TODO: refactor the wand.run code so that you pass in the class itself and not the type.

Running the main.py will open a terminal. The demo also includes tests that run via "python main.py test".

## The MoobiusService class

The MoobiusService class is full of async callback methods that respond to specific types of events and requests. Most of these methods do nothing by default and have a doc-string describing how to use them and what they do.

To build your app, you extend this class and overload some or all of these methods.

For simple apps such as this Demo it makes sense to store the application state as custom properties in our new DemoService class. Various callbacks will use these properties. Note the call to **super().__init__()**. The self.images should point to the images folder:

```
class DemoService(MoobiusService):
    def __init__(self, log_file="logs/service.log", error_log_file="logs/error.log", **kwargs):
        super().__init__(**kwargs)
        self.log_file = log_file
        self.error_log_file = error_log_file

        self._default_buttons = {}
        self.channels = {}
        self.image_show_dict = {}

        self.LIGHT = "light"
        self.DARK = "dark"
        self.MICKEY = "Mickey"
        self.WAND = "Wand"
        self.MICKEY_LIMIT = 5

        self._default_status = {
            'canvas_mode': self.LIGHT,
            'mickey_num': 0
        }

        self.images = {
            self.LIGHT: "resources/light.png",
            self.DARK: "resources/dark.png",
            self.MICKEY: "resources/mickey.jpg",
            self.WAND: "resources/wand.png"
        }
```

On launch the base class calls **self.start()**. This function authenticates, connects, sets the config's service_id, schedules repeating tasks, and more. After it is done with all of this it calls self.on_start(). This means that *the service is already set up and running by the time self.on_start() is called*.

## Overriding service.on_start() and creating a MoobiusStorage class

The goal of **on_start()** is primarily to query and modify the client configuration. self.rate_task is scheduled here instead of at self.__init__ so that it will not run before self.start() has finished:
```
self.scheduler.add_job(self.rate_task, 'interval', minutes=1)

async def rate_task(self):
    for channel_id in self.channels:
        channel = self.channels[channel_id]
        recipients = list(channel.real_characters.keys())
        talker = channel.virtual_characters[self.WAND].character_id
        txt = f"Check in every minute! {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        await self.send_message(channel_id, txt, talker, recipients)
```

On startup MoobiusService populates self.channels() with a list of channel_id values. It searches over all the channels and selects those for which service_id == self.client_id.

Each channel is a **MoobiusStorage** object as described earlier.

Each channel's moobius chat can have both real users as well as chatbots or other computer-controlled characters.
Demo uses the attributes *channel.real_characters* and *channel.virtual_characters* respectivly.

Populate the real characters:
```
    channel = MoobiusStorage(self.client_id, channel_id, db_config=self.db_config)
    self.channels[channel_id] = channel
    real_characters = await self.fetch_real_character_ids(channel_id)

    for character in real_characters:
        character_id = character.character_id
        channel.real_characters[character_id] = character

        if character_id not in channel.buttons:
            channel.buttons[character_id] = self.default_buttons
        else:
            pass

        if character_id not in channel.states:
            channel.states[character_id] = self.default_status
        else:
            pass
```

In this demo the bots are mickey-mouses which talk when a button is pressed. They can be initalized given a name and avatar:
create_character():

```
    for sn in range(self.MICKEY_LIMIT):
        key = f"{self.MICKEY}_{sn}"

        if key not in channel.virtual_characters:
            image_path = channel.image_paths[self.MICKEY]

            channel.virtual_characters[key] = await self.create_character(
                f'{self.MICKEY} {sn}', image_path, f'I am {self.MICKEY} {sn}!'
            )
        else:
            continue
```

Then upload the local images to it:
```
    for name in self.images:
        if name not in channel.image_paths:
            channel.image_paths[name] = await self.upload_file(self.images[name])
        else:
            pass
```

There are other, less important odds-and-ends in this function.
**TODO:** self.image_show_dict setup has a bug which will break if there is more than one channel.

## Overriding self.on_message_up(message_up)

This callback triggers when users send messages "up" to the backend server.
Here are some important properties of a messageUp object:
```
txt = message_up.content.text
channel_id = message_up.channel_id
sender = message_up.sender
recipients = message_up.recipients
```

Lets replace messages of "moobius" sent to ALL with "Moobius is Great!". Note that self.send_message is quite polymorphic and can handle string messages as well as MessageBody messages:
```
if recipients:
    # DEMO: text modification
    if txt.lower() == "moobius":
        await self.send_message(channel_id, "Moobius is Great!", sender, recipients)
    else:
        await self.send_message(message_up)
```

## Overriding self.on_refresh(action)

It is important to keep the database up-to-date with the buttons.
First define the function that does so:
```
async def calculate_and_update_character_list_from_database(self, channel_id, character_id):
    channel = self.channels[channel_id]
    real_characters = channel.real_characters
    character_list = [rc.character_id for rc in list(real_characters.values())]
    character_list = list(real_characters.keys()) # Equivalent to previous line for real_characters in these demo examples, but NOT for virtual_characters
    mickey_num = channel.states[character_id]['mickey_num']

    for sn in range(mickey_num):
        key = f"{self.MICKEY}_{sn}"
        character_list.append(channel.virtual_characters[key])

    await self.send_update_character_list(channel_id, character_list, [character_id])
```

Then keeping up to date when fetching the buttons and user list is easy. The **Action** dataclass has *channel_id* and *sender* attributes as well as *subtype* and an optional *context* attribute.

```
async def send_buttons_from_database(self, channel_id, character_id): # Doesn't overloading any method.
    button_list = self.channels[channel_id].buttons.get(character_id, self._default_buttons)
    await self.send_update_buttons(channel_id, button_list, [character_id])

async def on_refresh(self, action):
    await self.calculate_and_update_character_list_from_database(action.channel_id, action.sender)
    await self.send_buttons_from_database(action.channel_id, action.sender)

    channel_id = action.channel_id
    sender = action.sender
    channel = self.channels[channel_id]

    state = channel.states[sender]['canvas_mode']
    await self.send_update_canvas(channel_id, self.image_show_dict[state], [sender])

    await self.send_update_style(channel_id, [StyleElement(widget="canvas", display="visible", expand="true")], [sender])
```

## Overriding self.on_join_channel(action) and self.on_leave_channel(action)
When users join or leave channels it's time to update the channel.real_characters() list.
Lets also send a message to let people know:

```
async def on_join_channel(self, action):
    sender = action.sender
    channel_id = action.channel_id
    character = await self.fetch_character_profile(sender)
    name = character.name
    channel = self.channels[channel_id]

    channel.real_characters[sender] = character
    channel.buttons[sender] = self.default_buttons
    channel.states[sender] = self.default_status

    character_list = list(channel.real_characters.keys()) # Keys are character_ids for real characters generally.
    character_ids = list(channel.real_characters.keys()) # In this example character_list is the same as character_ids; every user gets to see the update.

    await self.send_update_character_list(channel_id, character_list, character_ids)
    await self.send_message(channel_id, f'{name} joined the channel!', sender, character_ids)

async def on_leave_channel(self, action):
    sender = action.sender
    channel_id = action.channel_id
    character = self.channels[action.channel_id].real_characters.pop(sender, None)
    self.channels[channel_id].states.pop(sender, None)
    self.channels[channel_id].buttons.pop(sender, None)
    name = character.name

    real_characters = self.channels[channel_id].real_characters
    character_list = list(real_characters.keys())
    character_ids = list(real_characters.keys())

    await self.send_update_character_list(channel_id, character_list, character_ids)
    await self.send_message(channel_id, f'{name} left the channel!', sender, character_ids)
```

## Overriding **self.on_spell(spell)**
This is how to respond to wand-dispatched methods. Lets print a message depending on how many times the wand is used:

```
async def on_spell(self, spell):
    try:
        content, times = spell
        content = str(content)
        times = int(times)
    except:
        content = 'DEFAULT'
        times = 1

    text = f"WAND: {content * times}"

    for channel_id in self.channels:
        channel = self.channels[channel_id]
        recipients = list(channel.real_characters.keys())
        talker = channel.virtual_characters[self.WAND].character_id
        await self.send_message(channel_id, text, sender, recipients)
```

## Overriding self.on_button_click(button_click)
*Button calls* encode button presses, etc and dispatched when a given client-side wigit is used used.
button_click.button_id gives the id of the wigit.
button_click.Arguments is a list of arguments, an example argument, which happens when the user selects the "create new Mickey" character option is: "ClickArgument(name='magic_type', value='Mickey')". Arguments encode which choice of a drop-down menu was used.

The resulting function is a siwthyard that handels different buttons:
```
async def on_button_click(self, button_click):
    channel_id = button_click.channel_id
    button_id = button_click.button_id
    sender = button_click.sender
    channel = self.channels[channel_id]

    character = channel.real_characters[sender]
    name = character.name
    recipients = list(channel.real_characters.keys())

    if button_id == "key1":
        value = button_click.arguments[0].value
        # Various actions.

    elif button_id == "key2":
        # various actions.
    elif button_id = "key3":
        # ... multible other button_ids ...
    else:
        logger.error(f"Unknown button_id: {button_id}")
```

## Callback Service Methods with a default behavior:
Most callbacks do nothing and are designed to be overriden. However, a few have default effects. None of these are used in the demo.

@logger.catch
**async def handle_received_payload(self, payload)**
This is a switchyard method that calls other callbacks such as "on_message_up" dependent on the type of the payload. It rarely needs to be overriden.

**async def on_action(self, action: Action)**
This is another switchyard method but it can be useful to override, such is in the *mahjong* demo. It calls functions such as "on_refresh", "on_join_channel" dependent on *action.subtype*.

**async def on_copy_client(self, copy: Copy)**
Will call self.send_service_login() if copy.status is invalid. Generally not useful to override.

## Other service methods not overriden nor used by Demo (except for debug info):

**async def on_unknown_payload(self, payload: Payload)**
This is used as a catchall in the handle_received_payload switchyard and is uncommon to override.

**async def send_service_login(self)**
Used internally in the Service class.

**async def send_update(self, target_client_id, data)**
Generaic send_update. It is generally not used, more specific functions such as send_update_character_list are used instead.

**async def send_update_channel_info(self, channel_id, channel_data)**
Generally not used.

**async def send_heartbeat(self)**
Used internally by Service and Agent.
