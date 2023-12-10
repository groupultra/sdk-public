# service.py

import json

from dacite import from_dict
from loguru import logger

from moobius import MoobiusService, MoobiusStorage, Moobius


class NekoService(MoobiusService):
    def __init__(self, log_file="logs/service.log", error_log_file="logs/error.log", **kwargs):
        super().__init__(**kwargs)
        self.log_file = log_file
        self.error_log_file = error_log_file

    # todo: channels and channel_ids, unbind_first, write back channels
    async def on_start(self):
        """
        Called after successful connection to websocket server and service login success.
        """
        # ==================== load features ====================
        logger.add(self.log_file, rotation="1 day", retention="7 days", level="DEBUG")
        logger.add(self.error_log_file, rotation="1 day", retention="7 days", level="ERROR")

        with open('resources/test_features.json', 'r') as f:
            features = json.load(f)

        for channel_id in self.channels:
            self.bands[channel_id] = MoobiusStorage(self.service_id, channel_id, db_config=self.db_config)
            real_characters = self.http_api.fetch_real_characters(channel_id, self.service_id)

            for character in real_characters:
                character_id = character.user_id
                self.bands[channel_id].real_characters[character_id] = character

            for feature in features:
                feature_id = feature["feature_id"]
                self.bands[channel_id].features[feature_id] = from_dict(data_class=Moobius.Feature, data=feature)

    # on_xxx, default implementation, to be override
    async def on_msg_up(self, msg_up):
        """
        Handle the received message.
        """
        logger.debug(f"on_msg_up {msg_up}")
        
        if msg_up.subtype == "text":
            if msg_up.content['text'] == "ping":
                msg_up.content['text'] = "pong"
            else:
                pass
        else:
            pass
                
        msg_down = self.msg_up_to_msg_down(msg_up)
        
        await self.send(payload_type='msg_down', payload_body=msg_down)

    async def on_fetch_user_list(self, action):
        logger.debug("fetch_userlist")
        real_characters = self.bands[action.channel_id].real_characters
        user_list = list(real_characters.values())

        await self.send_update_user_list(action.channel_id, user_list, [action.sender])
    
    async def on_fetch_features(self, action):
        logger.debug("fetch_features")
        features = self.bands[action.channel_id].features
        feature_data_list = list(features.values())

        await self.send_update_features(action.channel_id, feature_data_list, [action.sender])

    async def on_fetch_playground(self, action):
        logger.debug("fetch_playground")
        """
        content = self.db_helper.get_playground_info(client_id)
        await self.send_update_playground(channel_id, content, [client_id])
        """
    
    async def on_join_channel(self, action):
        logger.debug("join_channel")
        character_id = action.sender
        channel_id = action.channel_id
        character = self.http_api.fetch_user_profile(character_id)

        if character:            
            self.bands[action.channel_id].real_characters[character_id] = character

            real_characters = self.bands[action.channel_id].real_characters
            user_list = list(real_characters.values())
            character_ids = list(real_characters.keys())
            
            await self.send_update_user_list(action.channel_id, user_list, character_ids)

            await self.send_msg_down(
                channel_id=channel_id,
                recipients=character_ids,
                subtype="text",
                message_content=f'{character.user_context.nickname} joined the band!',
                sender=character_id
            )
        
        else:
            logger.error(f"Error fetching user profile: {character_id}")

    async def on_leave_channel(self, action):
        logger.debug("leave_channel")
        character_id = action.sender
        channel_id = action.channel_id
        character = self.bands[action.channel_id].real_characters.pop(character_id, None)

        real_characters = self.bands[action.channel_id].real_characters
        user_list = list(real_characters.values())
        character_ids = list(real_characters.keys())

        await self.send_update_user_list(action.channel_id, user_list, character_ids)

        await self.send_msg_down(
            channel_id=channel_id,
            recipients=character_ids,
            subtype="text",
            message_content=f'{character.user_context.nickname} left the band (but still talks~)!',
            sender=character_id
        )
        
    async def on_fetch_channel_info(self, action):
        logger.debug("fetch_channel_info")
        """
        await self.send_update_channel_info(channel_id, self.db_helper.get_channel_info(channel_id))
        """
    
    async def on_feature_call(self, feature_call):
        """
        Handle the received feature call.
        """
        logger.debug(f"Feature call received: {feature_call}")
        channel_id = feature_call.channel_id
        feature_id = feature_call.feature_id
        feature_name = self.bands[channel_id].features[feature_id].feature_name
        character = self.bands[channel_id].real_characters[feature_call.sender]
        nickname = character.user_context.nickname
        recipients = list(self.bands[channel_id].real_characters.keys())
        
        if feature_name == "name1":
            if feature_call.arguments[0].value == "Meet Tubbs":
                def _make_character(band_id, local_id, nickname):
                    username = f'{nickname}'
                    description = f'I am {nickname}!'
                    
                    character = self.http_api.create_service_user_with_local_image(self.service_id, "tubbs", "tubbs", "resources/tubbs.png", "I'm tubbs!")
                    
                    return character
                
                tubbs = _make_character(channel_id, "tubbs", "tubbs")
                user_list = list(self.bands[channel_id].real_characters.values())
                user_list.append(tubbs)
                await self.send_update_user_list(channel_id, user_list, [feature_call.sender])
                await self.send_msg_down(
                    channel_id=channel_id,
                    recipients=recipients,
                    subtype="text",
                    message_content=f'{nickname} clicked {feature_name}! Check out the user list!',
                    sender=feature_call.sender
                )
            elif feature_call.arguments[0].value == "Meet Hermeowne":
                image_uri = self.http_api.upload_file("resources/hermeowne.png")
                playground_content = {
                    "path": image_uri,
                    "text": "I'm Hermeowne!"
                }
        
                await self.send_update_playground(channel_id, playground_content, [feature_call.sender])
                await self.send_msg_down(
                    channel_id=channel_id,
                    recipients=recipients,
                    subtype="text",
                    message_content=f'{nickname} clicked {feature_name}! Check out the playground!',
                    sender=feature_call.sender
                )
                
        elif feature_name == "name2":
            image_uri = self.http_api.upload_file("resources/ms_fortune.png")
            await self.send_msg_down(
                channel_id=channel_id,
                recipients=recipients,
                subtype="image",
                message_content=image_uri,
                sender=feature_call.sender
            )

    async def on_unknown_message(self, message_data):
        """
        Handle the received unknown message.
        """
        logger.debug(f"Received unknown message: {message_data}")
