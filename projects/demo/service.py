# service.py
import json

from loguru import logger
from moobius import MoobiusService, MoobiusStorage


class DemoService(MoobiusService):
    def __init__(self, log_file="logs/service.log", error_log_file="logs/error.log", **kwargs):
        super().__init__(**kwargs)
        logger.add(log_file, rotation="1 day", retention="7 days", level="DEBUG")
        logger.add(error_log_file, rotation="1 day", retention="7 days", level="ERROR")
        self.default_features = {}
        self.bands = {}

        self.LIGHT = "light"
        self.DARK = "dark"
        self.MICKEY = "Mickey"
        self.WAND = "Wand"
        self.MICKEY_LIMIT = 5
        
        self.default_status = {
            'stage': self.LIGHT,
            'mickey_num': 0
        }

        self.images = {
            self.LIGHT: "resources/light.png",
            self.DARK: "resources/dark.png",
            self.MICKEY: "resources/mickey.jpg",
            self.WAND: "resources/wand.png"
        }

    async def on_start(self):
        """
        Called after successful connection to websocket server and service login success.
        """
        # ==================== load features ====================
        
        with open('resources/features.json', 'r') as f:
            self.default_features = json.load(f)

        for channel_id in self.channels:
            self.bands[channel_id] = MoobiusStorage(self.service_id, channel_id, db_config=self.db_config)
            real_characters = self.http_api.fetch_real_characters(channel_id, self.service_id)

            for character in real_characters:
                character_id = character.user_id
                self.bands[channel_id].real_characters[character_id] = character

                if character_id not in self.bands[channel_id].features:
                    self.bands[channel_id].features[character_id] = self.default_features
                else:
                    pass
                
                if character_id not in self.bands[channel_id].states:
                    self.bands[channel_id].states[character_id] = self.default_status
                else:
                    pass

            # DEMO: upload image
            for name in self.images:
                if name not in self.bands[channel_id].image_paths:
                    self.bands[channel_id].image_paths[name] = self.http_api.upload_file(self.images[name])
                else:
                    pass

            for sn in range(self.MICKEY_LIMIT):
                key = f"{self.MICKEY}_{sn}"

                if key not in self.bands[channel_id].virtual_characters:
                    image_path = self.bands[channel_id].image_paths[self.MICKEY]

                    self.bands[channel_id].virtual_characters[key] = self.http_api.create_service_user(
                        self.service_id, self.MICKEY, f'{self.MICKEY} {sn}', image_path, f'I am {self.MICKEY} {sn}!'
                    )
                else:
                    continue
            
            self.bands[channel_id].virtual_characters[self.WAND] = self.http_api.create_service_user(
                self.service_id, self.WAND, self.WAND, self.bands[channel_id].image_paths[self.WAND], f'I am {self.WAND}!'
            )

            self.stage_dict = {
                self.LIGHT: {
                    "path": self.bands[channel_id].image_paths[self.LIGHT],
                    "text": "Let There Be Light!"
                },

                self.DARK: {
                    "path": self.bands[channel_id].image_paths[self.DARK],
                    "text": "Let There Be Dark!"
                }
            }

    async def on_msg_up(self, msg_up):
        if msg_up.subtype == "text":
            txt = msg_up.content['text']
            channel_id = msg_up.channel_id
            sender = msg_up.context.sender
            recipients = msg_up.recipients
            
            if recipients:
                # DEMO: text modification
                if txt.lower() == "moobius":
                    await self.create_message(channel_id, "Moobius is Great!", recipients, sender=sender)
                else:
                    msg_down = self.msg_up_to_msg_down(msg_up)
                    await self.send(payload_type='msg_down', payload_body=msg_down)
            
            # DEMO: Infinity
            else:   # send to Service(Infinity)
                if txt.lower() == "hide":
                    self.bands[channel_id].features[sender] = []
                    await self.send_features_from_database(channel_id, sender)
                elif txt.lower() == "show":
                    self.bands[channel_id].features[sender] = self.default_features
                    await self.send_features_from_database(channel_id, sender)
                elif txt.lower() == "reset":
                    self.bands[channel_id].states[sender]['mickey_num'] = 0
                    await self.calculate_and_update_user_list_from_database(channel_id, sender)
                else:
                    pass
        
        # DEMO: other message types. TODO: save to your disk
        else:   
            msg_down = self.msg_up_to_msg_down(msg_up)
            await self.send(payload_type='msg_down', payload_body=msg_down)

    async def on_fetch_userlist(self, action):
        await self.calculate_and_update_user_list_from_database(action.channel_id, action.sender)
    
    async def on_fetch_features(self, action):
        await self.send_features_from_database(action.channel_id, action.sender)

    async def on_fetch_playground(self, action):
        channel_id = action.channel_id
        sender = action.sender

        state = self.bands[channel_id].states[sender]['stage']
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
        character_id = action.sender
        channel_id = action.channel_id
        character = self.http_api.fetch_user_profile(character_id)
        nickname = character.user_context.nickname

        self.bands[action.channel_id].real_characters[character_id] = character
        self.features[character_id] = self.default_features
        self.bands[action.channel_id].states[character_id] = self.default_status
        real_characters = self.bands[action.channel_id].real_characters

        user_list = list(real_characters.values())
        character_ids = list(real_characters.keys())
        
        await self.send_update_userlist(channel_id, user_list, character_ids)
        await self.create_message(channel_id, f'{nickname} joined the band! Special Commands (to ∞): show|hide|reset', character_ids, sender=character_id)

    # DEMO: a typical leave channel handler
    async def on_leave_channel(self, action):
        character_id = action.sender
        channel_id = action.channel_id
        character = self.bands[action.channel_id].real_characters.pop(character_id, None)
        self.bands[action.channel_id].states.pop(character_id, None)
        self.bands[action.channel_id].features.pop(character_id, None)
        nickname = character.user_context.nickname

        real_characters = self.bands[action.channel_id].real_characters
        user_list = list(real_characters.values())
        character_ids = list(real_characters.keys())

        await self.send_update_userlist(channel_id, user_list, character_ids)
        await self.create_message(channel_id, f'{nickname} left the band!', character_ids, sender=character_id)
    
    async def on_feature_call(self, feature_call):
        channel_id = feature_call.channel_id
        feature_id = feature_call.feature_id
        sender = feature_call.sender

        character = self.bands[channel_id].real_characters[sender]
        nickname = character.user_context.nickname
        recipients = list(self.bands[channel_id].real_characters.keys())
        
        if feature_id == "key1":
            value = feature_call.arguments[0].value

            if value == 'Mickey':
                if self.bands[channel_id].states[sender]['mickey_num'] >= self.MICKEY_LIMIT:
                    await self.create_message(channel_id, "You have reached the limit of Mickey!", [sender], sender=sender)
                else:
                    self.bands[channel_id].states[sender]['mickey_num'] += 1
                    await self.calculate_and_update_user_list_from_database(channel_id, sender)
            elif value == 'Talk':
                if self.bands[channel_id].states[sender]['mickey_num'] == 0:
                    await self.create_message(channel_id, "Please Create Mickey First!", [sender], sender=sender)
                else:
                    sn = self.bands[channel_id].states[sender]['mickey_num'] - 1
                    talker = self.bands[channel_id].virtual_characters[f"{self.MICKEY}_{sn}"].user_id
                    await self.create_message(channel_id, f"Mickey {sn} Here!", [sender], sender=talker)
            else:
                logger.warning(f"Unknown value: {value}")

        elif feature_id == "key2":
            if self.bands[channel_id].states[sender]['stage'] == self.LIGHT:
                self.bands[channel_id].states[sender]['stage'] = self.DARK
            else:
                self.bands[channel_id].states[sender]['stage'] = self.LIGHT
            
            state = self.bands[channel_id].states[sender]['stage']
            await self.send_update_playground(channel_id, self.stage_dict[state], [sender])

            image_uri = self.bands[channel_id].image_paths[state]
            await self.create_message(channel_id, image_uri, [sender], subtype='image', sender=sender)
        else:
            logger.warning(f"Unknown feature_id: {feature_id}")

    async def on_unknown_message(self, message_data):
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
            recipients = list(self.bands[channel_id].real_characters.keys())
            talker = self.bands[channel_id].virtual_characters[f"{self.WAND}"].user_id
            await self.create_message(channel_id, text, recipients, sender=talker)

    # ==================== helper functions ====================
    async def create_message(self, channel_id, content, recipients, subtype='text', sender=None):
        await self.send_msg_down(
            channel_id=channel_id,
            recipients=recipients,
            subtype=subtype,
            message_content=content,
            sender=sender or 'no_sender'
        )

    async def send_features_from_database(self, channel_id, character_id):
        feature_data_list = self.bands[channel_id].features.get(character_id, [])
        await self.send_update_features(channel_id, feature_data_list, [character_id])

    async def calculate_and_update_user_list_from_database(self, channel_id, character_id):
        real_characters = self.bands[channel_id].real_characters
        user_list = list(real_characters.values())
        
        mickey_num = self.bands[channel_id].states[character_id]['mickey_num']
        
        for sn in range(mickey_num):
            key = f"{self.MICKEY}_{sn}"
            user_list.append(self.bands[channel_id].virtual_characters[key])
        
        await self.send_update_userlist(channel_id, user_list, [character_id])