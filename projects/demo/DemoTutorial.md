# Set up a simple demo using moobius

This tutorial sets up a basic demo which showcases the essential features of Moobius. Almost all of the code is in ./service.py

## Configuration and "bands"

Once Moobius is installed (see the quickstart guide) you need to create a *band* and link the app to the band. Each backend SDK app is associated with one more bands.

To create a band, log into Moobius via the browser and create a new band (click the + next to My Bands).
Enter a nice *name* and *description*, such as "Demo" and "This-is-my-test". Doing so will see the *band ID* (example: "2c76aba1-73f4-4834-55f5-7ac8431640b1"). Alternativlty, the band ID of the currently selected band is shown in the URL. It is also possible to join bands by entering an ID.

To delete a band that you created, click the ... and select "Leave Band".

Create config/service.json with this format to link it to your account:
```
{
    "http_server_uri": "https://api.sociyoo.com/",
    "ws_server_uri": "wss://ws.sociyoo.com/",
    "email": "<Moobius login email>",
    "password": "<Moobius login password>",
    "service_id": "",
    "channels": [
        "<Band id>"
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
**band = MoobiusStorage(self.service_id, channel_id, db_config=json.load("./config/db.json"))**
band.service_id and band.band_id are set to the service_id and channel_id respectivly.
Each element's "implementation", in this case "json", determines the engine to use.
Each element's "name", in this case "real_characters", creates an attribute of band dynamically.
This means that band.real_characters is set to an initally empty **CachedDict**. Modifications to the dict will automatically keep the database up-to-date, there is no need to manually call save().
The "settings" stores engine-dependent parameters.

## Platform GUI structure

All created and joined bands will be shown in the list at the left panel.

Each band has it's own GUI independent of the others. There is a chat history, a collapsable *playground* (stage) to show images and text, and a *character list*. On the right there is a list of characters who may be real users or AI bots.

**The GUI state can be set independently per-user**. This means one user could see characters Alice and Bob while another sees Charlie and Dave. This provides flexibility for a wide variety of social deduction games, study groups, etc.

## Launching

Launching uses the *MoobiusWand* class to run your custom class:
```
from moobius import MoobiusWand
if __name__ == "__main__":
    wand = MoobiusWand()
    
    handle = wand.run(
        <YourCustomClassType>,
        service_config_path="config/service.json",
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

        self._default_features = {}
        self.bands = {}
        self.stage_dict = {}

        self.LIGHT = "light"
        self.DARK = "dark"
        self.MICKEY = "Mickey"
        self.WAND = "Wand"
        self.MICKEY_LIMIT = 5

        self._default_status = {
            'stage': self.LIGHT,
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

The goal of **on_start()** is primarily to query and modify the client configuration. self.cron_task is scheduled here instead of at self.__init__ so that it will not run before self.start() has finished:
```
self.scheduler.add_job(self.cron_task, 'interval', minutes=1)

async def cron_task(self):
    for channel_id in self.channels:
        band = self.bands[channel_id]
        recipients = list(band.real_characters.keys())
        talker = band.virtual_characters[self.WAND].user_id
        txt = f"Check in every minute! {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        await self.create_message(channel_id, txt, recipients, sender=talker)
```

On startup MoobiusService populates self.channels() with a list of band_id values. It searches over all the channels and selects those for which service_id == self.service_id.

Each band is a **MoobiusStorage** object as described earlier.

Each band's moobius chat can have both real users as well as chatbots or other computer-controlled characters.
Demo uses the attributes *band.real_characters* and *band.virtual_characters* respectivly.

Populate the real characters:
```
    band = MoobiusStorage(self.service_id, channel_id, db_config=self.db_config)
    self.bands[channel_id] = band
    real_characters = self.http_api.fetch_real_characters(channel_id, self.service_id)

    for character in real_characters:
        character_id = character.user_id
        band.real_characters[character_id] = character

        if character_id not in band.features:
            band.features[character_id] = self.default_features
        else:
            pass

        if character_id not in band.states:
            band.states[character_id] = self.default_status
        else:
            pass
```

In this demo the bots are mickey-mouses which talk when a button is pressed. They can be initalized with self.http_api.create_service_user():

```
    for sn in range(self.MICKEY_LIMIT):
        key = f"{self.MICKEY}_{sn}"

        if key not in band.virtual_characters:
            image_path = band.image_paths[self.MICKEY]

            band.virtual_characters[key] = self.http_api.create_service_user(
                self.service_id, self.MICKEY, f'{self.MICKEY} {sn}', image_path, f'I am {self.MICKEY} {sn}!'
            )
        else:
            continue
```

Then upload the local images to it:
```
    for name in self.images:
        if name not in band.image_paths:
            band.image_paths[name] = self.http_api.upload_file(self.images[name])
        else:
            pass
```

There are other, less important odds-and-ends in this function.
**TODO:** self.stage_dict setup has a bug which will break if there is more than one band.

## Overriding self.on_message_up(msg_up)

This callback triggers when users send messages "up" to the backend server.
Here are some important properties of a messageUp object:
```
txt = msg_up.content['text']
channel_id = msg_up.channel_id
sender = msg_up.context.sender
recipients = msg_up.context.recipients
```

Lets replace messages of "moobius" sent to ALL with "Moobius is Great!":
```
if recipients:
    # DEMO: text modification
    if txt.lower() == "moobius":
        await self.create_message(channel_id, "Moobius is Great!", recipients, sender=sender)
    else:
        await self.send(payload_type='msg_down', payload_body=msg_up)
```

## Overriding self.on_fetch_user_list(action) and self.on_fetch_features(action)

It is important to keep the database up-to-date with the features.
First define the function that does so:
```
async def calculate_and_update_user_list_from_database(self, channel_id, character_id):
    band = self.bands[channel_id]
    real_characters = band.real_characters
    user_list = [rc.user_id for rc in list(real_characters.values())]
    user_list = list(real_characters.keys()) # Equivalent to previous line for real_characters in these demo examples, but NOT for virtual_characters
    mickey_num = band.states[character_id]['mickey_num']

    for sn in range(mickey_num):
        key = f"{self.MICKEY}_{sn}"
        user_list.append(band.virtual_characters[key])

    await self.send_update_user_list(channel_id, user_list, [character_id])
```

Then keeping up to date when fetching the features and user list is easy. The **Action** dataclass has *channel_id* and *sender* attributes as well as *subtype* and an optional *context* attribute.

```
async def send_features_from_database(self, channel_id, character_id): # Doesn't overloading any method.
    feature_data_list = self.bands[channel_id].features.get(character_id, [])
    await self.send_update_features(channel_id, feature_data_list, [character_id])

async def on_fetch_user_list(self, action):
    await self.calculate_and_update_user_list_from_database(action.channel_id, action.sender)

async def on_fetch_features(self, action):
    await self.send_features_from_database(action.channel_id, action.sender)
```

## Overriding self.on_fetch_playground(action)
This is an excellent time to set up the widgets by using the parent **self.send_update_style()**

```
async def on_fetch_playground(self, action):
    channel_id = action.channel_id
    sender = action.sender
    band = self.bands[channel_id]

    state = band.states[sender]['stage']
    await self.send_update_playground(channel_id, self.stage_dict[state], [sender])

    content = [
        {
            "widget": "playground",
            "display": "visible",
            "expand": "true"
        }
    ]
    await self.send_update_style(channel_id, content, [sender])
```

## Overriding self.on_join_channel(action) and self.on_leave_channel(action)
When users join or leave channels it's time to update the band.real_characters() list.
Lets also send a message to let people know:

```
async def on_join_channel(self, action):
    sender = action.sender
    channel_id = action.channel_id
    character = self.http_api.fetch_user_profile(sender)
    nickname = character.user_context.nickname
    band = self.bands[channel_id]

    band.real_characters[sender] = character
    band.features[sender] = self.default_features
    band.states[sender] = self.default_status

    user_list = list(band.real_characters.keys()) # Keys are user_ids for real characters generally.
    character_ids = list(band.real_characters.keys()) # In this example user_list is the same as character_ids; every user gets to see the update.

    await self.send_update_user_list(channel_id, user_list, character_ids)
    await self.create_message(channel_id, f'{nickname} joined the band!', character_ids, sender=sender)

async def on_leave_channel(self, action):
    sender = action.sender
    channel_id = action.channel_id
    character = self.bands[action.channel_id].real_characters.pop(sender, None)
    self.bands[channel_id].states.pop(sender, None)
    self.bands[channel_id].features.pop(sender, None)
    nickname = character.user_context.nickname

    real_characters = self.bands[channel_id].real_characters
    user_list = list(real_characters.keys())
    character_ids = list(real_characters.keys())

    await self.send_update_user_list(channel_id, user_list, character_ids)
    await self.create_message(channel_id, f'{nickname} left the band!', character_ids, sender=sender)
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
        band = self.bands[channel_id]
        recipients = list(band.real_characters.keys())
        talker = band.virtual_characters[self.WAND].user_id
        await self.create_message(channel_id, text, recipients, sender=talker)
```

## Overriding self.on_feature_call(feature_call)
*Feature calls* encode button presses, etc and dispatched when a given client-side wigit is used used.
feature_call.feature_id gives the id of the wigit.
feature_call.Arguments is a list of arguments, an example argument, which happens when the user selects the "create new Mickey" character option is: "FeatureCallArgument(name='magic_type', value='Mickey')". Arguments encode which choice of a drop-down menu was used.

The resulting function is a siwthyard that handels different features:
```
async def on_feature_call(self, feature_call):
    channel_id = feature_call.channel_id
    feature_id = feature_call.feature_id
    sender = feature_call.sender
    band = self.bands[channel_id]

    character = band.real_characters[sender]
    nickname = character.user_context.nickname
    recipients = list(band.real_characters.keys())

    if feature_id == "key1":
        value = feature_call.arguments[0].value

        if value == 'Mickey':
            if band.states[sender]['mickey_num'] >= self.MICKEY_LIMIT:
                await self.create_message(channel_id, "You have reached the limit of Mickey!", [sender], sender=sender)
            else:
                band.states[sender]['mickey_num'] += 1
                band.states.save(sender)

                await self.calculate_and_update_user_list_from_database(channel_id, sender)
        elif value == 'Talk':
            if band.states[sender]['mickey_num'] == 0:
                await self.create_message(channel_id, "Please Create Mickey First!", [sender], sender=sender)
            else:
                sn = band.states[sender]['mickey_num'] - 1
                talker = band.virtual_characters[f"{self.MICKEY}_{sn}"].user_id
                await self.create_message(channel_id, f"Mickey {sn} Here!", [sender], sender=talker)
        else:
            dtrack.log_warning(f"Unknown value: {value}")

    elif feature_id == "key2":
        if band.states[sender]['stage'] == self.LIGHT: 
                band.states[sender]['stage'] = self.DARK
        else:
                band.states[sender]['stage'] = self.LIGHT

        band.states.save(sender)
        state = band.states[sender]['stage']
        await self.send_update_playground(channel_id, self.stage_dict[state], [sender])

        image_uri = band.image_paths[state]
        await self.create_message(channel_id, image_uri, [sender], subtype='image', sender=sender)
    else:
        dtrack.log_warning(f"Unknown feature_id: {feature_id}")
```

## Callback Service Methods with a default behavior:
Most callbacks do nothing and are designed to be overriden. However, a few have default effects. None of these are used in the demo.

@logger.catch
**async def handle_received_payload(self, payload)**
This is a switchyard method that calls other callbacks such as "on_msg_up" dependent on the type of the payload. It rarely needs to be overriden.

**async def on_action(self, action: Action)**
This is another switchyard method but it can be useful to override, such is in the *mahjong* demo. It calls functions such as "on_fetch_features", "on_join_playground" dependent on *action.subtype*.

**async def on_copy_client(self, copy: Copy)**
Will call self.send_service_login() if copy.status is invalid. Generally not useful to override.

## Other service methods not overriden nor used by Demo (except for debug info):

**async def on_fetch_channel_info(self, action)**
This method is uncommon to override.

**async def upload_avatar_and_create_character(self, service_id, username, nickname, image_path, description)**
Uses HTTPS to uploade an image and assign it to a new character. Used by the demos *neko* and *script_cinema*.


**async def on_unknown_payload(self, payload: Payload)**
This is used as a catchall in the handle_received_payload switchyard and is uncommon to override.

**async def send_service_login(self)**
Used internally in the Service class.

**async def send_msg_down(self, channel_id, recipients, subtype, message_content, sender)**
Used by virtual characters to send messages to users. Used many times in the demo *mouse*.

**async def send_update(self, target_client_id, data)**
Generaic send_update. It is generally not used, more specific functions such as send_update_user_list are used instead.

**async def send_update_channel_info(self, channel_id, channel_data)**
Generally not used.

**async def send_heartbeat(self)**
Used internally by Service and Agent.
