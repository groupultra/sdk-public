# service.py
import json, sys, asyncio
import copy
from datetime import datetime

from loguru import logger
from moobius import SDK, MoobiusStorage

avoid_redis_on_windoze = True # Redis requires WSL2 to run on windows since it is Linux-only.
avoid_redis = (avoid_redis_on_windoze and (sys.platform.lower() in ['win', 'win32', 'win64', 'windows', 'windoze'])) or avoid_redis_on_windoze == 'also linux'
load_xtra_bands_on_start = True

example_socket_callback_payloads = {} # Print these out when the AI is done.

class DemoService(SDK):
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

    def initialize_band(self, channel_id):
        '''Initalize the band with the startup features.'''
        band = MoobiusStorage(self.client_id, channel_id, db_config=self.db_config)
        self.bands[channel_id] = band

        real_character_ids = self.http_api.fetch_real_characters(channel_id, self.client_id, raise_empty_list_err=False)

        for character_id in real_character_ids:
            band.real_characters[character_id] = self.http_api.fetch_user_profile(character_id)

            if character_id not in band.features:
                band.features[character_id] = self.default_features

            if character_id not in band.states:
                band.states[character_id] = self.default_status

        for name in self.images: # Once per startup upload images.
            if name not in self.image_paths:
                self.image_paths[name] = self.http_api.upload_file(self.images[name]) # This isn't async so to speed up maybe a (TODO) parallel map?

        for sn in range(self.MICKEY_LIMIT):
            key = f"{self.MICKEY}_{sn}"

            if key not in band.virtual_characters:
                image_path = self.image_paths[self.MICKEY]

                band.virtual_characters[key] = self.http_api.create_service_user(
                    self.client_id, self.MICKEY, f'{self.MICKEY} {sn}', image_path, f'I am {self.MICKEY} {sn}!'
                )

        band.virtual_characters[self.WAND] = self.http_api.create_service_user(
            self.client_id, self.WAND, self.WAND, self.image_paths[self.WAND], f'I am {self.WAND}!'
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

    def get_band(self, channel_id):
        '''Prevents KeyErrors by creating new band databases if they don't exist yet.'''
        if channel_id not in self.bands:
            self.initialize_band(channel_id)
        return self.bands[channel_id]

    async def on_start(self):
        """
        Called after successful connection to websocket server and service login success.
        """
        # ==================== load features ====================
        logger.add(self.log_file, rotation="1 day", retention="7 days", level="DEBUG")
        logger.add(self.error_log_file, rotation="1 day", retention="7 days", level="ERROR")

        for c in self.db_config: # Windoze!
            if 'redis' in c['implementation'].lower():
                if avoid_redis:
                    logger.warning('WARNING: No Redis this demo b/c avoid_redis is True, using JSON instead for: '+ str(c))
                    c['implementation'] = 'json'

        with open('resources/features.json', 'r') as f:
            self._default_features = json.load(f)

        self.scheduler.add_job(self.cron_task, 'interval', minutes=1)

        channel2service = await self.fetch_bound_channels()
        for c_id, s_id in channel2service.items():
            if s_id == self.client_id and c_id not in self.bands:
                if load_xtra_bands_on_start:
                    logger.info(f'EXTRA band bound to this service on startup will be added: {c_id}')
                    self.initialize_band(c_id)
                else:
                    logger.info(f'EXTRA band bound to this service on startup will NOT be added b/c load_xtra_bands_on_start is False: {c_id}')

    async def cron_task(self):
        for channel_id in self.channels:
            band = self.get_band(channel_id)
            recipients = list(band.real_characters.keys())
            talker = band.virtual_characters[self.WAND].user_id
            txt = f"Check in every minute! {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            await self.create_message(channel_id, txt, recipients, sender=talker)

    async def on_msg_down(self, msg_down):
        example_socket_callback_payloads['on_msg_down'] = msg_down

    async def on_update(self, the_update):
        example_socket_callback_payloads['on_update'] = the_update

    async def on_msg_up(self, msg_up):
        if msg_up.subtype == "text":
            txt = msg_up.content['text']
            channel_id = msg_up.channel_id
            sender = msg_up.sender
            if type(sender) is not str:
                raise Exception(f'Sender must be a string, instead it is: {sender}')
            recipients = msg_up.recipients
            band = self.get_band(channel_id)

            if recipients:
                # DEMO: text modification
                if txt.lower() == "moobius":
                    await self.create_message(channel_id, "Moobius is Great!", recipients, sender=sender)
                elif txt.lower() == "api":
                    lines = []
                    for k,v in example_socket_callback_payloads.items():
                        lines.append(k+': '+str(v))
                    txt = '\n'.join(lines)
                    await self.create_message(channel_id, 'Socket api call examples recorded:\n'+txt, recipients, sender=sender)
                else:
                    await self.create_message(channel_id, txt, recipients, sender=sender)
                    #await self.send(payload_type='msg_down', payload_body=msg_up) # equivalent.
            # DEMO: Infinity
            else:   # send to Service(Infinity)
                if txt.lower() == "hide":
                    band.features[sender] = []
                    await self.send_features_from_database(channel_id, sender)
                elif txt.lower() == "show":
                    band.features[sender] = self.default_features
                    await self.send_features_from_database(channel_id, sender)
                elif txt.lower() == "reset":
                    band.states[sender]['mickey_num'] = 0
                    band.states.save(sender)

                    await self.calculate_and_update_user_list_from_database(channel_id, sender)
                    the_band = self.get_band(channel_id)
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
        await self.send_features_from_database(action.channel_id, action.sender)

    async def on_fetch_channel_info(self, action):
        example_socket_callback_payloads['on_fetch_channel_info'] = action

    async def on_fetch_playground(self, action):
        example_socket_callback_payloads['on_fetch_features'] = action
        channel_id = action.channel_id
        sender = action.sender
        band = self.get_band(channel_id)

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

    # DEMO: a typical join channel handler
    async def on_join_channel(self, action):
        example_socket_callback_payloads['on_join_channel'] = action
        sender_id = action.sender
        channel_id = action.channel_id
        character = self.http_api.fetch_user_profile(sender_id)
        nickname = character.user_context.nickname
        band = self.get_band(channel_id)

        band.real_characters[sender_id] = character
        band.features[sender_id] = self.default_features
        band.states[sender_id] = self.default_status

        character_ids = list(band.real_characters.keys())
        await self.send_update_user_list(channel_id, character_ids, character_ids)
        await self.create_message(channel_id, f'{nickname} joined the band!', character_ids, sender=sender_id)

    # DEMO: a typical leave channel handler
    async def on_leave_channel(self, action):
        example_socket_callback_payloads['on_leave_channel'] = action
        sender = action.sender
        channel_id = action.channel_id
        character = self.get_band(action.channel_id).real_characters.pop(sender, None)
        self.get_band(channel_id).states.pop(sender, None)
        self.get_band(channel_id).features.pop(sender, None)
        nickname = character.user_context.nickname

        real_characters = self.get_band(channel_id).real_characters
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
        example_socket_callback_payloads['on_feature_call'] = feature_call
        channel_id = feature_call.channel_id
        feature_id = feature_call.feature_id
        sender = feature_call.sender
        band = self.get_band(channel_id)

        character = band.real_characters[sender]
        nickname = character.user_context.nickname
        recipients = list(band.real_characters.keys())

        redis_txt = 'not-the-Redis' if avoid_redis else 'Redis'

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
                    await self.create_message(channel_id, f"Mickey {sn} Here! Mickeys are stored in JSON db.", [sender], sender=talker)
            else:
                logger.warning(f"Unknown value: {value}")

        elif feature_id == "key2":
            if band.states[sender]['stage'] == self.LIGHT: 
                 band.states[sender]['stage'] = self.DARK
            else:
                 band.states[sender]['stage'] = self.LIGHT

            band.states.save(sender)
            state = band.states[sender]['stage']
            await self.send_update_playground(channel_id, self.stage_dict[state], [sender])

            image_uri = self.image_paths[state]
            await self.create_message(channel_id, image_uri, [sender], subtype='image', sender=sender)
        elif feature_id == "key3":
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
        elif feature_id == "key4":
            value = feature_call.arguments[0].value
            if not hasattr(self, 'xtra_bands'): # One time on startup.
                self.xtra_bands = {} # Created by clicking on the "band!" button.
                self.left_bands = []
            #channel2service = self.fetch_bound_channels() TODO
            extra_band_ids = list(self.xtra_bands.keys())
            if value == "New band":
                band_name = '>>Demo TEMP band'+str(len(extra_band_ids))
                new_band_id = await self.create_and_bind_channel(band_name, 'Band created by the GUI.')
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
            else:
                raise Exception(f'Strange value for feature key4: {value}')
        elif feature_id == "key5":
            cmds = '"moobius": Print Moobius is Great msg. "meow": Have Agent print nya. "reset": Reset mickeys and refresh buttons. "API": Print special socket API doc.'
            await self.create_message(channel_id, f"Commands (some get sent to all 'all' some to 'service'):\n{cmds}", [sender], sender=sender)
        else:
            logger.warning(f"Unknown feature_id: {feature_id}")

    async def on_unknown_message(self, message_data):
        example_socket_callback_payloads['on_feature_call'] = message_data
        logger.warning(f"Received unknown message: {message_data}")
    
    # ==================== DEMO: Wand Event Listener ====================
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
            band = self.get_band(channel_id)
            recipients = list(band.real_characters.keys())
            talker = band.virtual_characters[self.WAND].user_id
            await self.create_message(channel_id, text, recipients, sender=talker)

    # ==================== helper functions ====================
    async def send_features_from_database(self, channel_id, character_id):
        feature_data_list = self.get_band(channel_id).features.get(character_id, []) # Contents of features.json.
        await self.send_update_features(channel_id, feature_data_list, [character_id])

    async def calculate_and_update_user_list_from_database(self, channel_id, character_id):
        band = self.get_band(channel_id)
        real_characters = band.real_characters
        user_list = list(real_characters.keys())

        mickey_num = band.states[character_id]['mickey_num']

        for sn in range(mickey_num):
            key = f"{self.MICKEY}_{sn}"
            user_list.append(band.virtual_characters[key].user_id)

        await self.send_update_user_list(channel_id, user_list, [character_id])
