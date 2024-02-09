# service.py
import json, sys, asyncio
import copy
from datetime import datetime

from loguru import logger
from moobius import SDK, MoobiusStorage
from moobius.types import Feature

avoid_redis_on_windoze = True # Redis requires WSL2 to run on windows since it is Linux-only.
avoid_redis = (avoid_redis_on_windoze and (sys.platform.lower() in ['win', 'win32', 'win64', 'windows', 'windoze'])) or avoid_redis_on_windoze == 'also linux'
load_xtra_bands_on_start = True

example_socket_callback_payloads = {} # Print these out when the AI is done.

class DemoService(SDK):
    def __init__(self, log_file="logs/service.log", error_log_file="logs/error.log", **kwargs):
        super().__init__(**kwargs)
        self.log_file = log_file
        self.error_log_file = error_log_file

        self._default_features = []
        self.bands = {}
        self.stage_dict = {}

        self.LIGHT = "light"
        self.DARK = "dark"
        self.MICKEY = "Mickey"
        self.WAND = "Wand"
        self.MICKEY_LIMIT = 5

        self.image_paths = {}

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

    @property
    def default_status(self):
        return copy.deepcopy(self._default_status)

    @property
    def default_features(self):
        return copy.deepcopy(self._default_features)

    async def initialize_band(self, channel_id):
        """Initalizes the band (given by channel_id) with the images and real and virtual characters.
           All of this is stored in a MoobiusStorage object."""
        band = MoobiusStorage(self.client_id, channel_id, db_config=self.db_config)
        self.bands[channel_id] = band

        real_character_ids = await self.fetch_real_characters(channel_id, raise_empty_list_err=False)

        for character_id in real_character_ids:
            band.real_characters[character_id] = await self.fetch_user_profile(character_id)

            if character_id not in band.features:
                band.features[character_id] = self.default_features

            if character_id not in band.states:
                band.states[character_id] = self.default_status

        for name in self.images: # Once per startup upload images.
            if name not in self.image_paths:
                self.image_paths[name] = await self.upload_file(self.images[name])

        for sn in range(self.MICKEY_LIMIT):
            key = f"{self.MICKEY}_{sn}"

            if key not in band.virtual_characters:
                image_path = self.image_paths[self.MICKEY]

                band.virtual_characters[key] = await self.create_service_user(
                    self.MICKEY, f'{self.MICKEY} {sn}', image_path, f'I am {self.MICKEY} {sn}!'
                )

        band.virtual_characters[self.WAND] = await self.create_service_user(
            self.WAND, self.WAND, self.image_paths[self.WAND], f'I am {self.WAND}!'
        )

        self.stage_dict = {
            self.LIGHT: {
                "path": self.image_paths[self.LIGHT],
                "text": "Let There Be Light!"
            },

            self.DARK: {
                "path": self.image_paths[self.DARK],
                "text": "Let There Be Dark!"
            }
        }
        return band

    async def get_band(self, channel_id):
        """Prevents KeyErrors by creating new band databases if they don't exist yet."""
        if channel_id not in self.bands:
            await self.initialize_band(channel_id)
        return self.bands[channel_id]

    async def on_start(self):
        """Called after successful connection to websocket server and service login success.
           Launches the chron check-in task and searches for extra bands bound to this service."""
        # ==================== load features ====================
        logger.add(self.log_file, rotation="1 day", retention="7 days", level="DEBUG")
        logger.add(self.error_log_file, rotation="1 day", retention="7 days", level="ERROR")

        for c in self.db_config: # Windoze!
            if 'redis' in c['implementation'].lower():
                if avoid_redis:
                    logger.warning('WARNING: No Redis this demo b/c avoid_redis is True, using JSON instead for: '+ str(c))
                    c['implementation'] = 'json'

        with open('resources/features.json', 'r') as f:
            self._default_features = [Feature(**f) for f in json.load(f)]

        self.scheduler.add_job(self.cron_task, 'interval', minutes=1)

        channel2service = await self.fetch_bound_channels()
        for c_id, s_id in channel2service.items():
            if s_id == self.client_id and c_id not in self.bands:
                if load_xtra_bands_on_start:
                    logger.info(f'EXTRA band bound to this service on startup will be added: {c_id}')
                    await self.initialize_band(c_id)
                else:
                    logger.info(f'EXTRA band bound to this service on startup will NOT be added b/c load_xtra_bands_on_start is False: {c_id}')

    async def cron_task(self):
        """Sends a check-in message to each band."""
        for channel_id in self.channels:
            band = await self.get_band(channel_id)
            recipients = list(band.real_characters.keys())
            talker = band.virtual_characters[self.WAND].user_id
            txt = f"Check in every minute! {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            await self.create_message(channel_id, txt, recipients, sender=talker)

    async def on_msg_down(self, msg_down):
        """This and several other callbacks only exist to record the API calls."""
        example_socket_callback_payloads['on_msg_down'] = msg_down

    async def on_update(self, the_update):
        """This and several other callbacks only exist to record the API calls."""
        example_socket_callback_payloads['on_update'] = the_update

    async def on_msg_up(self, msg_up):
        """Runs various commands, such as resetting when the user types in "reset".
           (Agent-related commands are found in the agent.py instead of here)."""
        example_socket_callback_payloads['on_msg_up'] = msg_up
        if msg_up.subtype == "text":
            txt = msg_up.content['text']
            channel_id = msg_up.channel_id
            sender = msg_up.sender
            if type(sender) is not str:
                raise Exception(f'Sender must be a string, instead it is: {sender}')
            recipients = msg_up.recipients
            band = await self.get_band(channel_id)

            if recipients: # DEMO: text modification
                if txt.lower() == "moobius":
                    await self.create_message(channel_id, "Moobius is Great!", recipients, sender=sender)
                elif txt.lower() == "api":
                    lines = []
                    for k,v in example_socket_callback_payloads.items():
                        lines.append(k+': '+str(v))
                    txt = '\n\n'.join(lines)
                    await self.create_message(channel_id, 'Socket api call examples recorded:\n'+txt, recipients, sender=sender)
                else:
                    await self.create_message(channel_id, txt, recipients, sender=sender)
                    #await self.send(payload_type='msg_down', payload_body=msg_up) # equivalent.
            else: # DEMO: commands to Service(Infinity)
                if txt.lower() == "hide":
                    band.features[sender] = []
                    await self.send_features_from_database(channel_id, sender)
                elif txt.lower() == "show":
                    band.features[sender] = self.default_features
                    await self.send_features_from_database(channel_id, sender)
                elif txt.lower() == "reset":

                    for sn in range(self.MICKEY_LIMIT):
                        the_user_id = band.virtual_characters[f"{self.MICKEY}_{sn}"].user_id
                        await self.update_service_user(user_id=the_user_id, username=f'Mickey {sn} uname', avatar=self.image_paths[self.MICKEY], description='Mickey restet!', nickname=f'Mickey {sn}')

                    band.states[sender]['mickey_num'] = 0
                    band.states.save(sender)

                    await self.calculate_and_update_user_list_from_database(channel_id, sender)
                    the_band = await self.get_band(channel_id)
                    the_band.features[sender] = self.default_features # Reset buttons etc.
                    await self.send_update_features(channel_id, self.default_features, [sender])
                else:
                    pass

        # DEMO: other message types.
        else:
            await self.create_message(channel_id, str(msg_up), recipients, sender=sender) # Not sure if this works or the generic next line is needed?
            #await self.send(payload_type='msg_down', payload_body=msg_up)

    async def on_fetch_user_list(self, action):
        example_socket_callback_payloads['on_fetch_user_list'] = action
        await self.calculate_and_update_user_list_from_database(action.channel_id, action.sender)

    async def on_fetch_features(self, action):
        example_socket_callback_payloads['on_fetch_features'] = action
        if hasattr(self, 'TMP_print_buttons') and getattr(self, 'TMP_print_buttons'): # Set to True to indicate an extra call to print the buttons.
            self.TMP_print_buttons = False
            channel_id = action.channel_id
            sender = action.sender
            await self.create_message(channel_id, f"Fetch feature action\n: {action}.", [sender], sender=sender)
        else:
            await self.send_features_from_database(action.channel_id, action.sender)

    async def on_fetch_channel_info(self, action):
        example_socket_callback_payloads['on_fetch_channel_info'] = action

    async def on_fetch_playground(self, action):
        """Pipes self.stage_dict from band.states into self.send_update_playground."""
        example_socket_callback_payloads['on_fetch_playground'] = action
        channel_id = action.channel_id
        sender = action.sender
        band = await self.get_band(channel_id)

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

    async def on_join_channel(self, action):
        """Most join handlers, as this one does, will send_update_user_list with the new character added and send a "user joined!" message."""
        example_socket_callback_payloads['on_join_channel'] = action
        sender_id = action.sender
        channel_id = action.channel_id
        character = await self.fetch_user_profile(sender_id)
        nickname = character.user_context.nickname
        band = await self.get_band(channel_id)

        band.real_characters[sender_id] = character
        band.features[sender_id] = self.default_features
        band.states[sender_id] = self.default_status

        character_ids = list(band.real_characters.keys())
        await self.send_update_user_list(channel_id, character_ids, character_ids)
        await self.create_message(channel_id, f'{nickname} joined the band!', character_ids, sender=sender_id)

    async def on_leave_channel(self, action):
        """Most leave handlers, as this one does, will send_update_user_list with the character removed and maybe send a "user left!" message."""
        example_socket_callback_payloads['on_leave_channel'] = action
        sender = action.sender
        channel_id = action.channel_id
        character = (await self.get_band(action.channel_id)).real_characters.pop(sender, None)
        (await self.get_band(channel_id)).states.pop(sender, None)
        (await self.get_band(channel_id)).features.pop(sender, None)
        nickname = character.user_context.nickname

        real_characters = (await self.get_band(channel_id)).real_characters
        character_ids = list(real_characters.keys())

        await self.send_update_user_list(channel_id, character_ids, character_ids)
        await self.create_message(channel_id, f'{nickname} left the band!', character_ids, sender=sender)

    async def on_copy_client(self, the_copy):
        await super().on_copy_client(the_copy) # One of the few callbacks to have an action.
        example_socket_callback_payloads['on_copy_client'] = the_copy

    async def on_unknown_payload(self, x):
        example_socket_callback_payloads['on_unknown_payload'] = x

    async def on_update_style(self, x):
        example_socket_callback_payloads['on_update_style'] = x

    async def on_update_features(self, x):
        example_socket_callback_payloads['on_update_features'] = x

    async def on_update_playground(self, x):
        example_socket_callback_payloads['on_update_playground'] = x

    async def on_update_userlist(self, x):
        example_socket_callback_payloads['on_update_userlist'] = x

    async def on_feature_call(self, feature_call):
        """Called when the user presses a button (and selecting an option of a list appears). feature_call is a Feature object.
           This is a major switchyard which handles most of the different features in the demo."""
        example_socket_callback_payloads['on_feature_call'] = feature_call
        channel_id = feature_call.channel_id
        feature_id = feature_call.feature_id
        sender = feature_call.sender
        band = await self.get_band(channel_id)

        character = band.real_characters[sender]
        nickname = character.user_context.nickname
        recipients = list(band.real_characters.keys())

        redis_txt = 'not-the-Redis' if avoid_redis else 'Redis'

        if feature_id == "stage_feat":
            if band.states[sender]['stage'] == self.LIGHT: 
                 band.states[sender]['stage'] = self.DARK
            else:
                 band.states[sender]['stage'] = self.LIGHT

            band.states.save(sender)
            state = band.states[sender]['stage']
            await self.send_update_playground(channel_id, self.stage_dict[state], [sender])

            image_uri = self.image_paths[state]
            await self.create_message(channel_id, image_uri, [sender], subtype='image', sender=sender)
        elif feature_id == "money_feat":
            value = feature_call.arguments[0].value
            if value == '(Print Savings)' or value == '(Donate all)':
                if value == '(Donate all)':
                    tot = 0
                    for k in band.currency.keys():
                        tot += band.currency[k]
                        band.currency[k] = 0
                    await self.create_message(channel_id, f"{tot} weeks of savings donated to mysterious unknown charities.", [sender], sender=sender)
                desc = []
                unicode_map = {'Naira':'₦', 'Dollar':'$', 'Peso':'₱', 'Yuan':'¥', 'Euro': '€', 'Kina':'K', 'Penguin':'🐧'}
                for k in band.currency.keys():
                    desc.append(f'{unicode_map[k]}={band.currency[k]}')
                desc = '['+', '.join(desc)+']'
                await self.create_message(channel_id, f"{redis_txt} query; number of weeks of living expenses saved in each currency:\n {desc}", [sender], sender=sender)
            else:
                msg_map = {'Naira':'Nigerian', 'Dollar':'American', 'Peso':'Chilean', 'Yuan':'Chinese', 'Euro': 'West European', 'Kina':'Papua New Guinean', 'Penguin':'Antarctican'}

                await self.create_message(channel_id, f"You earn two weeks salary of {msg_map[value]}. Your bank account will be stored in {redis_txt}!", [sender], sender=sender)

                if value not in band.currency:
                    band.currency[value] = 0
                band.currency[value] += 2 # Number of weeks.
        elif feature_id == "band_feat":
            value = feature_call.arguments[0].value
            if not hasattr(self, 'xtra_bands'): # One time on startup.
                self.xtra_bands = {} # Created by clicking on the "band!" button.
                self.left_bands = []
            #channel2service = self.fetch_bound_channels() TODO
            extra_band_ids = list(self.xtra_bands.keys())
            if value == "New band":
                band_name = '>>Demo TEMP band'+str(len(extra_band_ids))
                new_band_id = await self.create_and_bind_channel(band_name, 'Band created by the GUI.')
                await self.initialize_band(new_band_id) # Prevents KeyErrors.
                self.xtra_bands[new_band_id] = 'A band'
                await self.create_message(channel_id, f"New band created, refresh and it should appear on the left bar: {band_name} ({new_band_id})", [sender], sender=sender)
            elif value == "Ping Bands":
                tasks = [self.create_message(channel_id, f"Pinging Band ids: {extra_band_ids} (one ping message should show up in each band)", [sender], sender=sender)]
                for extra_band_id in extra_band_ids + self.left_bands: # Ideally the left out bands should no longer respond.
                    tasks.append(self.create_message(extra_band_id, f"Ping from band {channel_id} to band {extra_band_id}!", [sender], sender=sender))
                await asyncio.wait(tasks)
            elif value == "Reset extra bands":
                await self.create_message(channel_id, f"Leaving Band ids: {extra_band_ids}", [sender], sender=sender)
                tasks = []
                for band_id in extra_band_ids:
                    tasks.append(self.send_leave_channel(band_id))
                    if band_id in self.bands: # Should always be.
                        del self.bands[band_id]
                self.xtra_bands = {}
                await asyncio.wait(tasks)
                self.left_bands += extra_band_ids
            elif value == "Fetch channel list":
                x = await self.fetch_channel_list()
                await self.create_message(channel_id, f"Channel list:\n{str(x)}", [sender], sender=sender)
                x = await self.fetch_popular_channels()
                await self.create_message(channel_id, f"Popular channel list:\n{str(x)}", [sender], sender=sender)
            elif value == "Update extra channels":
                extra_band_ids = list(self.xtra_bands.keys())
                ix = 0
                for bid in extra_band_ids:
                    await self.update_channel(bid, f'<>DemoTmpChannel{ix}<>', 'Pressed the update extra channels button.')
                    ix = ix+1
                await self.create_message(channel_id, f"Updated these band names (refresh to see changes):\n{extra_band_ids}", [sender], sender=sender)
            elif value == "Fetch chat history":
                history = await self.fetch_history_message(channel_id, limit=6, before="null")
                await self.create_message(channel_id, f"Recent chat history of this channel:\n{history}", [sender], sender=sender)
            elif value == "Fetch features":
                print('Asking for Features (will have to wait for the WS to get back).')
                self.TMP_print_buttons = True
                await self.send_fetch_features(channel_id)
            else:
                raise Exception(f'Strange value for feature band_feat: {value}')
        elif feature_id == "user_feat":
            value = feature_call.arguments[0].value
            if not hasattr(self, 'n_usr_update'):
                self.n_usr_update = -1
            self.n_usr_update += 1
            image_list = [self.image_paths[x] for x in [self.LIGHT, self.DARK, self.WAND]]
            image_path = image_list[self.n_usr_update%len(image_list)] # Cycle through non-mickey images.

            #with open('config/agent.json','r') as f_obj:
            #    agent_config = json.load(f_obj)
            if value == 'Make Mickey':
                if band.states[sender]['mickey_num'] >= self.MICKEY_LIMIT:
                    await self.create_message(channel_id, "You have reached the limit of Mickey!", [sender], sender=sender)
                else:
                    band.states[sender]['mickey_num'] += 1
                    band.states.save(sender)

                    await self.calculate_and_update_user_list_from_database(channel_id, sender)
            elif value == 'Mickey Talk':
                if band.states[sender]['mickey_num'] == 0:
                    await self.create_message(channel_id, "Please Create Mickey First!", [sender], sender=sender)
                else:
                    sn = band.states[sender]['mickey_num'] - 1
                    talker = band.virtual_characters[f"{self.MICKEY}_{sn}"].user_id
                    await self.create_message(channel_id, f"Mickey {sn} Here! Mickeys are stored in JSON db.", [sender], sender=talker)
            elif value == "Update Mickey (not agent) name":
                if band.states[sender]['mickey_num'] == 0:
                    await self.create_message(channel_id, "Please Create Mickey First!", [sender], sender=sender)
                else:
                    sn = band.states[sender]['mickey_num'] - 1
                    the_user_id = band.virtual_characters[f"{self.MICKEY}_{sn}"].user_id
                    await self.update_service_user(user_id=the_user_id, username='Updated Mickey Nickname', avatar=image_path, description='Mickey updated name!', nickname=f'Update Mickey Nick {self.n_usr_update}')
                    await self.create_message(channel_id, f"Updated Mickey name and image (refresh to see).", [sender], sender=sender)
            else:
                raise Exception(f'Strange value for feature user_feat: {value}')
        elif feature_id == "command_feat":
            cmds = '"moobius": Print Moobius is Great msg.\n\n"meow": Have Agent print nya.\n\n"reset": Reset mickeys and refresh buttons.\n\n"API": Print special socket API doc.\n\n"log agent out": Log out agent, will re-auth next session.\n\n"agent info": See printout of agent info.\n\n"rename agent foo": Set agent nickname to foo.'
            await self.create_message(channel_id, f"Commands (some get sent to all 'all' some to 'service'):\n{cmds}", [sender], sender=sender)
        else:
            logger.warning(f"Unknown feature_id: {feature_id}")

    async def on_unknown_message(self, message_data):
        example_socket_callback_payloads['on_feature_call'] = message_data
        logger.warning(f"Received unknown message: {message_data}")

    async def on_spell(self, spell):
        """Just send the content of the spell to the message."""
        try:
            content, times = spell
            content = str(content)
            times = int(times)
        except:
            content = 'DEFAULT'
            times = 1

        text = f"WAND: {content * times}"

        for channel_id in self.channels:
            band = await self.get_band(channel_id)
            recipients = list(band.real_characters.keys())
            talker = band.virtual_characters[self.WAND].user_id
            await self.create_message(channel_id, text, recipients, sender=talker)

    ########################### helper functions #####################################

    async def send_features_from_database(self, channel_id, character_id):
        """Pipes the features (loaded from the JSON) to self.send_update_features."""
        feature_data_list = (await self.get_band(channel_id)).features.get(character_id, []) # Contents of features.json.
        await self.send_update_features(channel_id, feature_data_list, [character_id])

    async def calculate_and_update_user_list_from_database(self, channel_id, character_id):
        """Pipes all real users + the correct number of Mickeys to self.send_update_user_list."""
        band = await self.get_band(channel_id)
        real_characters = band.real_characters
        user_list = list(real_characters.keys())

        mickey_num = band.states[character_id]['mickey_num']

        for sn in range(mickey_num):
            key = f"{self.MICKEY}_{sn}"
            user_list.append(band.virtual_characters[key].user_id)

        await self.send_update_user_list(channel_id, user_list, [character_id])
