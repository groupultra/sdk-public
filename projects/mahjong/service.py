# service.py

import asyncio
import requests
import random
from datetime import datetime
import os
import base64
import io

from loguru import logger
from PIL import Image

from moobius import MoobiusService, MoobiusStorage


class MahjongService(MoobiusService):
    def __init__(self, log_file="logs/service.log", error_log_file="logs/error.log", **kwargs):
        super().__init__(**kwargs)
        logger.add(log_file, rotation="1 day", retention="7 days", level="DEBUG")
        logger.add(error_log_file, rotation="1 day", retention="7 days", level="ERROR")

        self.image_dir = kwargs.get('image_dir', 'temp/images')

        os.makedirs(self.image_dir, exist_ok=True)

    async def on_start(self):
        """
        Called after successful connection to websocket server and service login success.
        """
        for channel_id in self.channels:
            self.bands[channel_id] = MoobiusStorage(self.service_id, channel_id, db_config=self.db_config)

            real_characters = await self.fetch_real_characters(channel_id)

            for character in real_characters:
                character_id = character.user_id
                self.bands[channel_id].real_characters[character_id] = character

    def base64_to_image(self, b64_str):
        b64_str = b64_str.split(',')[1]   # data:image/png;base64,
        img = base64.b64decode(b64_str)
        img = Image.open(io.BytesIO(img))
        file_name = f'{datetime.now().strftime("%Y%m%d%H%M%S%f")}_{random.randint(1000, 9999)}.png'
        path = os.path.join(self.image_dir, file_name)
        img.save(path)

        return path

    async def on_msg_up(self, msg_up):
        """
        Handle the received message.
        """
        channel_id = msg_up.channel_id
        sender = msg_up.context.sender

        recipients = msg_up.context.recipients

        if msg_up.subtype == "text":
            txt = msg_up.content['text'].strip()
            
            if txt.startswith('river'):
                river = True
                content = txt[5:].strip()
            else:
                river = False
                content = txt

            res = requests.post('http://localhost:3001/mahgen', json={'content': content, 'river': river})

            if res.status_code == 200:
                b64_str = res.text
                path = self.base64_to_image(b64_str)
                image_url = self.http_api.upload_file(path)

                await self._send_msg(channel_id, image_url, recipients, subtype='image', sent_by=sender, virtual=False)

            else:
                msg_down = self.msg_up_to_msg_down(msg_up, remove_self=True)

                print("msg_down", msg_down)
                await self.send(payload_type='msg_down', payload_body=msg_down)
        else:
            msg_down = self.msg_up_to_msg_down(msg_up, remove_self=True)
            await self.send(payload_type='msg_down', payload_body=msg_down)

    async def _send_msg(self, channel_id, message_content, recipients, subtype='text', sent_by='Painter', virtual=True):
        """
        Send system message.
        """

        if virtual:
            sender = self.bands[channel_id].virtual_characters[sent_by].user_id
        else:
            sender = sent_by

        await self.send_msg_down(
            channel_id=channel_id,
            recipients=recipients,
            subtype=subtype,
            message_content=message_content,
            sender=sender
        )

    async def _send_playground_image(self, channel_id, image_path, recipients):
        """
        Send playground image.
        """
        content = {"path": image_path}
        await self.send_update_playground(channel_id, content, recipients)

    async def _send_playground_text(self, channel_id, text, recipients):
        """
        Send playground image.
        """
        content = {"text": text}
        await self.send_update_playground(channel_id, content, recipients)

    async def on_action(self, action):
        """
        Handle the received action.
        """
        sender = action.sender
        channel_id = action.channel_id

        if action.subtype == "fetch_userlist":
            real_characters = list(self.bands[channel_id].real_characters.values())
            virtual_characters = list(self.bands[channel_id].virtual_characters.values())
            user_list = virtual_characters + real_characters

            await self.send_update_userlist(channel_id, user_list, [sender])

        elif action.subtype == "fetch_features":
            await self.send_update_features(action.channel_id, [], [action.sender])

        elif action.subtype == "fetch_playground":
            text = "This project is inspired by https://github.com/eric200203/mahgen. Try sending one of the following:<br/><br/>"
            text += "123m456p789s1267z<br/><br/>"
            text += '_123m5_50p||||12345s||6s<br/><br/>'
            text += '6^66z||v555m||55v0s||0z89s0z||8z9z<br/><br/>'
            text += "river 123456m123456v789p123s<br/><br/>"
            text += "river 123^456_7m^8^9s"

            await self._send_playground_text(channel_id, text, [sender])

            content = [
                {
                    "widget": "playground",
                    "display": "visible",
                    "expand": "true"
                }
            ]
            
            await self.send_update_style(channel_id, content, [sender])

        elif action.subtype == "join_channel":
            character = self.http_api.fetch_user_profile([sender])
            self.bands[channel_id].real_characters[sender] = character

            real_characters = list(self.bands[channel_id].real_characters.values())
            virtual_characters = list(self.bands[channel_id].virtual_characters.values())
            user_list = virtual_characters + real_characters

            character_ids = list(self.bands[channel_id].real_characters.keys())

            await self.send_update_userlist(channel_id, user_list, character_ids)
            await self._send_msg(channel_id, f'{character.user_context.nickname} joined the band!', character_ids, sent_by=sender, virtual=False)

            await asyncio.sleep(0.5)
        
        elif action.subtype == "leave_channel":
            character = self.bands[channel_id].real_characters.pop(sender, None)

            real_characters = self.bands[channel_id].real_characters
            virtual_characters = self.bands[channel_id].virtual_characters
            user_list = list(virtual_characters.values()) + list(real_characters.values())
            character_ids = list(real_characters.keys())
            
            await self._send_msg(channel_id, f'{character.user_context.nickname} left the band!', character_ids, sent_by=sender, virtual=False)
            await self.send_update_userlist(channel_id, user_list, character_ids)

        elif action.subtype == "fetch_channel_info":
            logger.info("fetch_channel_info")
            """
            await self.send_update_channel_info(channel_id, self.db_helper.get_channel_info(channel_id))
            """
        else:
            logger.warning("Unknown action subtype:", action.subtype)

    async def on_feature_call(self, feature_call):
        """
        Handle the received feature call.
        """

    async def on_unknown_message(self, message_data):
        """
        Handle the received unknown message.
        """
        logger.warning("Received unknown message:", message_data)
