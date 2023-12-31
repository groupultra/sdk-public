# translate_service.py

import asyncio
import json

from moobius import MoobiusService, MoobiusStorage, Moobius

from dacite import from_dict
from loguru import logger

import aiohttp

DeepL_Key = "Your DeepL API Key"

class TranslateService(MoobiusService):
    def __init__(self, log_file="logs/service.logger.info", error_log_file="logs/error.logger.info", **kwargs):
        super().__init__(**kwargs)
        logger.add("logs/service.logger.info", rotation="1 day", retention="7 days", level="DEBUG")
        logger.add("logs/error.logger.info", rotation="1 day", retention="7 days", level="ERROR")
        

    async def on_start(self):
        """
        Called after successful connection to websocket server and service login success.
        """
        li = self.http_api.get_service_list()
        self.channel_ids = []

        for d in li:
            if d.get('service_id', None) == self.service_id:
                self.channel_ids = d.get('channel_ids', [])
                break

        logger.info(f"channel_ids: {self.channel_ids}")
        
        # ==================== load features ====================
        with open('config/features.json', 'r', encoding='utf-8') as f:
            features = json.load(f)

        for channel_id in self.channel_ids:
            cur_band = MoobiusStorage(self.service_id, channel_id, db_config=self.db_config)
            self.bands[channel_id] = cur_band
            real_characters = await self.fetch_real_characters(channel_id)

            for character in real_characters:
                character_id = character.user_id
                cur_band.real_characters[character_id] = character
                if character_id not in cur_band.user_languages:
                    cur_band.user_languages[character_id] = "English"

            for feature in features:
                feature_id = feature["feature_id"]
                cur_band.features[feature_id] = feature
        
        self.deepl_map = {"English": "EN", "中文": "ZH", "日本語": "JA",
                          "Русский": "RU", "Español": "ES", "Français": "FR",
                          "Deutsch": "DE", "한국인": "KO", "Dansk": "DA"}
    

    def split_recipients_by_language(self, channel_id, recipients):
        cur_band = self.bands[channel_id]
        ret = {}
        for user in recipients:
            if user in cur_band.user_languages:
                lang = cur_band.user_languages[user]
                if lang not in ret:
                    ret[lang] = []
                ret[lang].append(user)
            else:
                logger.info(f"User {user} not in band {channel_id}!", error=True)
        return ret

    async def process_text_by_lang(self, text, lang):
        ret_text = ''
        async with aiohttp.ClientSession() as session:
            header = {"Authorization": f"DeepL-Auth-Key {DeepL_Key}", "Content-Type": "application/json"}
            data = {
                "text": [
                    text
                ],
                "target_lang": self.deepl_map[lang]
            }
            async with session.post('https://api-free.deepl.com/v2/translate', json=data, headers=header) as resp:
                try:
                    ret_json = await resp.json()
                    ret_text = ret_json['translations'][0]['text']
                except Exception as e:
                    ret_text = "Something wrong happened! Maybe limit exceeded!" + str(e) + await resp.text()
        return ret_text


    # on_xxx, default implementation, to be override
    async def on_msg_up(self, msg_up):
        """
        Handle the received message.
        """
        logger.info(f"on_msg_up: {msg_up}")
        recipients = msg_up.recipients
        if msg_up.sender in recipients:
            recipients.remove(msg_up.sender)
        if msg_up.subtype == "text":
            text = msg_up.content["text"]
            recipient_by_lang = self.split_recipients_by_language(msg_up.channel_id, recipients)
            for lang in recipient_by_lang.keys():
                result_text = await self.process_text_by_lang(text, lang)
                cur_recipients = recipient_by_lang[lang]
                await self.send_msg_down(
                    channel_id=msg_up.channel_id,
                    recipients=cur_recipients,
                    subtype="text",
                    message_content=result_text,
                    sender=msg_up.sender
                )
        else:
            await self.send(payload_type='msg_down', payload_body=msg_up)

    async def on_fetch_user_list(self, action):
        logger.info("fetch_userlist")
        real_characters = self.bands[action.channel_id].real_characters
        user_list = list(real_characters.values())

        await self.send_update_user_list(action.channel_id, user_list, [action.sender])
    
    async def on_fetch_features(self, action):
        logger.info("fetch_features")
        features = self.bands[action.channel_id].features
        if "key2" in features:
            del features["key2"]
        feature_data_list = list(features.values())

        await self.send_update_features(action.channel_id, feature_data_list, [action.sender])

    
    async def on_fetch_playground(self, action):
        logger.info("fetch_playground")
        """
        content = self.db_helper.get_playground_info(client_id)
        await self.send_update_playground(channel_id, content, [client_id])
        """
    
    async def on_join_channel(self, action):
        logger.info("join_channel")
        character_id = action.sender
        channel_id = action.channel_id
        character = self.http_api.fetch_user_profile(character_id)

        if character:
            self.bands[action.channel_id].real_characters[character_id] = character

            real_characters = self.bands[action.channel_id].real_characters
            user_list = list(real_characters.values())
            character_ids = list(real_characters.keys())

            if character_id not in self.bands[action.channel_id].user_languages:
                self.bands[action.channel_id].user_languages[character_id] = "English"

            await self.send_update_userlist(action.channel_id, user_list, character_ids)

            await self.send_msg_down(
                channel_id=channel_id,
                recipients=character_ids,
                subtype="text",
                message_content=f'{character.user_context.nickname} joined the band!',
                sender=character_id
            )
        
        else:
            logger.info(f"Error fetching user profile: {character_id}", error=True)

    async def on_leave_channel(self, action):
        logger.info("leave_channel")
        character_id = action.sender
        channel_id = action.channel_id
        character = self.bands[action.channel_id].real_characters.pop(character_id, None)

        real_characters = self.bands[action.channel_id].real_characters
        user_list = list(real_characters.values())
        character_ids = list(real_characters.keys())

        await self.send_update_userlist(action.channel_id, user_list, character_ids)

        await self.send_msg_down(
            channel_id=channel_id,
            recipients=character_ids,
            subtype="text",
            message_content=f'{character.user_context.nickname} left the band (but still talks~)!',
            sender=character_id
        )
        
    async def on_fetch_channel_info(self, action):
        logger.info("fetch_channel_info")
        """
        await self.send_update_channel_info(channel_id, self.db_helper.get_channel_info(channel_id))
        """

    async def on_feature_call(self, feature_call):
        """
        Handle the received feature call.
        """
        logger.info("Feature call received:", feature_call)
        channel_id = feature_call.channel_id
        feature_id = feature_call.feature_id

        cur_band = self.bands[channel_id]

        character = cur_band.real_characters[feature_call.sender]
        nickname = character.user_context.nickname
        # recipients = list(cur_band.real_characters.keys())
        
        if feature_id == "key1":
            language = feature_call.arguments[0].value
            await self.send_msg_down(
                channel_id=channel_id,
                recipients=[feature_call.sender],
                subtype="text",
                message_content=f'{nickname} choosed to use {language}!',
                sender=feature_call.sender
            )

            cur_band.user_languages[feature_call.sender] = language
        
        if feature_id == "key2":
            await self.send_msg_down(
                channel_id=channel_id,
                recipients=[feature_call.sender],
                subtype="text",
                message_content=f'{nickname} is using {cur_band.user_languages[feature_call.sender]}!',
                sender=feature_call.sender
            )

    async def on_unknown_message(self, message_data):
        """
        Handle the received unknown message.
        """
        logger.info(f"Received unknown message: {message_data}")
