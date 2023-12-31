# demo_service.py

import asyncio
import json

from moobius import MoobiusService, MoobiusStorage, Moobius

from dacite import from_dict
from loguru import logger

from script_parser import *

class ScriptService(MoobiusService):
    def __init__(self, log_file="logs/service.logger.info", error_log_file="logs/error.logger.info", **kwargs):
        super().__init__(**kwargs)
        logger.add("logs/service.logger.info", rotation="1 day", retention="7 days", level="DEBUG")
        logger.add("logs/error.logger.info", rotation="1 day", retention="7 days", level="ERROR")
        

    @logger.catch
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

        logger.info(f"channel_ids {self.channel_ids}")
        
        # ==================== load features ====================
        # with open('demo_features.json', 'r') as f:
            # features = json.load(f)
        
        self.story = parse_story("mahjong.yaml")
        self.avatar_key_map = {}

        for channel_id in self.channel_ids:
            self.bands[channel_id] = MoobiusStorage(self.service_id, channel_id, db_config=self.db_config)
            real_characters = self.http_api.fetch_real_characters(channel_id, self.service_id)
            virtual_characters = self.http_api.get_service_user_list(self.service_id)

            for character in virtual_characters:
                character_id = character.user_id
                self.bands[channel_id].virtual_characters[character_id] = character

            for character in real_characters:
                character_id = character.user_id
                self.bands[channel_id].real_characters[character_id] = character
                # 初始化script_progress
                if character_id not in self.bands[channel_id].script_progress:
                    properties, global_properties = self.story.get_init_value()
                    self.bands[channel_id].script_progress[character_id] = {
                        'playing_script': False,
                        'can_use_feature': False,
                        'status': [{
                            'unit': self.story.start_unit, 
                            'property': properties
                        }],
                        'global': global_properties
                    }
                # 初始化features
                if character_id not in self.bands[channel_id].features:
                    self.bands[channel_id].features[character_id] = []
            
            # 初始化avatar_key_map和虚拟用户
            # map是从avatar的key到character_id(uuid)
            virtual_characters = self.bands[channel_id].virtual_characters
            for character_id, character in virtual_characters.items():
                self.avatar_key_map[character.username] = character_id
            for avatar_key, avatar in self.story.avatar.items():
                # 创建那些暂未被创建的avatar
                # key是avatar_id，name是nickname
                if avatar_key not in self.avatar_key_map:
                    character = await self.upload_avatar_and_create_character(
                        self.service_id, avatar_key, avatar.name, avatar.image, "")
                    self.avatar_key_map[avatar_key] = character.user_id
                    virtual_characters[character.user_id] = character
            
            # 把图片预上传
            for image in self.story.used_images:
                if image not in self.bands[channel_id].image_url:
                    url = self.http_api.upload_file(self.story.get_full_image_path(image))
                    self.bands[channel_id].image_url[image] = url

            # for feature in features:
                # feature_id = feature["feature_id"]
                # self.bands[channel_id].features[feature_id] = feature
        
        self.continue_feature = {
                        "feature_id": "play",
                        "feature_name": "Continue Playing",
                        "button_text": "Continue Playing",
                        "new_window": False,
                        "arguments": [
                        ]
                    }
        self.pause_feature = {
                        "feature_id": "pause",
                        "feature_name": "Pause Script",
                        "button_text": "Pause Script",
                        "new_window": False,
                        "arguments": [
                        ]
                    }
        self.revert_feature = {
                        "feature_id": "revert",
                        "feature_name": "Back to Previous Choice",
                        "button_text": "Back to Previous Choice",
                        "new_window": False,
                        "arguments": [
                        ]
                    }
        self.replay_feature = {
                        "feature_id": "replay",
                        "feature_name": "Replay this Unit",
                        "button_text": "Replay this Unit",
                        "new_window": False,
                        "arguments": [
                        ]
                    }
        self.default_next_feature = {
                        "feature_id": "next",
                        "feature_name": "Continue",
                        "button_text": "Continue",
                        "new_window": False,
                        "arguments": [
                        ]
                    }


    # on_xxx, default implementation, to be override
    async def on_msg_up(self, msg_up):
        """
        Handle the received message.
        """
        logger.info(f"on_msg_up {msg_up}")
        '''if msg_up.subtype == "text":
            if msg_up.content['text'] == "ping":
                msg_up.content['text'] = "pong"'''
        
        channel_id = msg_up.channel_id
        character_id = msg_up.sender
        # 如果他在玩，就直接忽略掉
        if self.bands[channel_id].script_progress[character_id]['playing_script']:
            return

        # 如果他不在玩，就过滤掉在玩的
        recipients = msg_up.recipients

        result_recipients = []

        for recipient in recipients:
            if not self.bands[channel_id].script_progress[recipient]['playing_script']:
                result_recipients.append(recipient)
        msg_down.recipients = result_recipients

        await self.send(payload_type='msg_down', payload_body=msg_up)
    

    async def on_fetch_user_list(self, action):
        logger.info("fetch_user_list")
        # 如果正在播放剧本，就只显示当前unit的人
        if self.bands[action.channel_id].script_progress[action.sender]['playing_script']:
            display_characters = []
            current_unit = self.bands[action.channel_id].script_progress[action.sender]['status'][-1]['unit']
            current_unit_members = self.story.story[current_unit].member
            for avatar in current_unit_members:
                character_id = self.avatar_key_map[avatar.key]
                display_characters.append(self.bands[action.channel_id].virtual_characters[character_id])

            await self.send_update_user_list(action.channel_id, display_characters, [action.sender])
            return
        # 如果不在播放剧本，就显示所有人
        real_characters = self.bands[action.channel_id].real_characters
        user_list = list(real_characters.values())

        await self.send_update_user_list(action.channel_id, user_list, [action.sender])
    
    async def on_fetch_features(self, action):
        logger.info("fetch_features")
        # 如果在播放剧本并且不能用feature，就给一个空的
        if self.bands[action.channel_id].script_progress[action.sender]['playing_script'] \
            and not self.bands[action.channel_id].script_progress[action.sender]['can_use_feature']:
            await self.send_update_features(action.channel_id, [], [action.sender])
            return
        # 如果不在播放剧本，就给一个继续播放的按钮
        if not self.bands[action.channel_id].script_progress[action.sender]['playing_script']:
            features = [
                    self.continue_feature
                ]
            await self.send_update_features(action.channel_id, features, [action.sender])
            return
        # 在播放剧本且可以用feature，从数据库里拿一下现在可以用啥
        features = self.bands[action.channel_id].features[action.sender]

        await self.send_update_features(action.channel_id, features, [action.sender])

    
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

            if character_id not in self.bands[action.channel_id].script_progress:
                properties, global_properties = self.story.get_init_value()
                self.bands[action.channel_id].script_progress[character_id] = {
                            'playing_script': False,
                            'can_use_feature': False,
                            'status': [{
                                'unit': self.story.start_unit, 
                                'property': properties
                            }],
                            'global': global_properties
                        }
            
            if character_id not in self.bands[channel_id].features:
                self.bands[channel_id].features[character_id] = []
            
            real_characters = self.bands[action.channel_id].real_characters
            user_list = list(real_characters.values())
            character_ids = list(real_characters.keys())
            character_ids_not_playing = [character_id for character_id in character_ids if not self.bands[action.channel_id].script_progress[character_id]['playing_script']]

            await self.send_update_user_list(action.channel_id, user_list, character_ids_not_playing)

            await self.send_msg_down(
                channel_id=channel_id,
                recipients=character_ids_not_playing,
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

        character_ids_not_playing = [character_id for character_id in character_ids if not self.bands[action.channel_id].script_progress[character_id]['playing_script']]

        await self.send_update_user_list(action.channel_id, user_list, character_ids_not_playing)

        await self.send_msg_down(
            channel_id=channel_id,
            recipients=character_ids_not_playing,
            subtype="text",
            message_content=f'{character.user_context.nickname} left the band! How sad!',
            sender=character_id
        )
        
    async def on_fetch_channel_info(self, action):
        logger.info("fetch_channel_info")
        """
        await self.send_update_channel_info(channel_id, self.db_helper.get_channel_info(channel_id))
        """
    
    def update_script_progress(self, channel_id, character_id, field, value):
        new_dict = dict(self.bands[channel_id].script_progress[character_id])
        new_dict[field] = value
        self.bands[channel_id].script_progress[character_id] = new_dict
    
    async def play_script_unit(self, channel_id, recipient, unit: StoryUnit, ignore_delay=False):
        self.update_script_progress(channel_id, recipient, 'playing_script', True)
        self.update_script_progress(channel_id, recipient, 'can_use_feature', False)

        properties = self.bands[channel_id].script_progress[recipient]['status'][-1]['property']
        global_properties = self.bands[channel_id].script_progress[recipient]['global']

        await self.send_update_features(channel_id, [], [recipient])

        display_characters = []
        current_unit_members = unit.member
        for avatar in current_unit_members:
            character_id = self.avatar_key_map[avatar.key]
            display_characters.append(self.bands[channel_id].virtual_characters[character_id])

        await self.send_update_user_list(channel_id, display_characters, [recipient])

        for dialog in unit.dialog:
            sender_id = self.avatar_key_map[dialog.speaker]
            if dialog.type == "image":
                url = self.bands[channel_id].image_url[dialog.content]
                await self.send_msg_down(
                    channel_id=channel_id,
                    recipients=[recipient],
                    subtype="image",
                    message_content=url,
                    sender=sender_id
                )
            else:
                await self.send_msg_down(
                    channel_id=channel_id,
                    recipients=[recipient],
                    subtype="text",
                    message_content=dialog.content,
                    sender=sender_id
                )
            if not ignore_delay:
                await asyncio.sleep(dialog.delay / 1000)
            else:
                await asyncio.sleep(0.1)
    
        self.update_script_progress(channel_id, recipient, 'can_use_feature', True)

        features = []
        features.append(self.pause_feature)
        if len(self.bands[channel_id].script_progress[recipient]['status']) > 1:
            features.append(self.revert_feature)
        features.append(self.replay_feature)
        has_choice = False
        for choice_number, choice in enumerate(unit.choice):
            if choice.check_constraint(properties) and choice.check_constraint(global_properties):
                feature = self.generate_feature_from_choice(choice, choice_number)
                features.append(feature)
                has_choice = True
        if (not has_choice) and (not unit.is_end):
            features.append(self.default_next_feature)

        self.bands[channel_id].features[recipient] = features
        
        await self.send_update_features(channel_id, features, [recipient])
    
    def generate_feature_from_choice(self, choice: SingleChoice, choice_number: int):
        feature = {
            "feature_id": f"choice_{choice_number}",
            "feature_name": choice.name,
            "button_text": choice.name,
            "new_window": False,
            "arguments": [
            ]
        }
        return feature
    
    async def on_feature_call(self, feature_call):
        """
        Handle the received feature call.
        """
        logger.info(f"Feature call received: {feature_call}")
        channel_id = feature_call.channel_id
        feature_id = feature_call.feature_id
        sender = feature_call.sender
        # character = self.bands[channel_id].real_characters[sender]
        # nickname = character.user_context.nickname
        # recipients = list(self.bands[channel_id].real_characters.keys())

        # 如果在播片，且不能用feature，就直接忽略掉
        if self.bands[channel_id].script_progress[sender]['playing_script'] \
            and not self.bands[channel_id].script_progress[sender]['can_use_feature']:
            return
    
        if not self.bands[channel_id].script_progress[sender]['playing_script']:
            if feature_id == "play":
                current_unit = self.bands[channel_id].script_progress[sender]['status'][-1]['unit']
                if self.bands[channel_id].script_progress[sender]['can_use_feature']:
                    self.update_script_progress(channel_id, sender, 'playing_script', True)
                    display_characters = []
                    current_unit_members = self.story.story[current_unit].member
                    for avatar in current_unit_members:
                        character_id = self.avatar_key_map[avatar.key]
                        display_characters.append(self.bands[channel_id].virtual_characters[character_id])

                    await self.send_update_user_list(channel_id, display_characters, [sender])
                    await self.send_update_features(channel_id, self.bands[channel_id].features[sender], [sender])
                else:
                    await self.play_script_unit(channel_id, sender, self.story.story[current_unit])
                return
        
        if self.bands[channel_id].script_progress[sender]['playing_script']:
            status = self.bands[channel_id].script_progress[sender]['status']
            current_unit = status[-1]['unit']
            if feature_id == "pause":
                self.update_script_progress(channel_id, sender, 'playing_script', False)
                real_characters = self.bands[channel_id].real_characters
                real_characters = list(real_characters.values())
                await self.send_update_features(channel_id, [self.continue_feature], [sender])
                await self.send_update_user_list(channel_id, real_characters, [sender])
                return
            if feature_id == "revert":
                if len(status) == 1:
                    return
                previous_unit = status[-2]['unit']
                status.pop()
                self.update_script_progress(channel_id, sender, 'status', status)
                await self.play_script_unit(channel_id, sender, self.story.story[previous_unit], ignore_delay=True)
                return
            if feature_id.startswith("choice_"):
                choice_number = int(feature_id.split("_")[1])
                choice = self.story.story[current_unit].choice[choice_number]
                if not (choice.check_constraint(status[-1]['property']) \
                        and choice.check_constraint(self.bands[channel_id].script_progress[sender]['global'])):
                    return
                status.append({
                    'unit': choice.goto,
                    'property': choice.apply_value_change(status[-1]['property'])
                })
                self.update_script_progress(channel_id, sender, 'status', status)

                global_properties = self.bands[channel_id].script_progress[sender]['global']
                global_properties = choice.apply_value_change(global_properties)
                self.update_script_progress(channel_id, sender, 'global', global_properties)

                await self.play_script_unit(channel_id, sender, self.story.story[choice.goto])
                return
            if feature_id == "replay":
                await self.play_script_unit(channel_id, sender, self.story.story[current_unit], ignore_delay=True)
                return
            # 理论上需要校验是否没有其他选择可用，但是我不想做了
            if feature_id == "next":
                next_unit = self.story.story[current_unit].default_next
                if next_unit and next_unit != '':
                    await self.play_script_unit(channel_id, sender, self.story.story[next_unit])
                return

    async def on_unknown_message(self, message_data):
        """
        Handle the received unknown message.
        """
        logger.info(f"Received unknown message: {message_data}")
