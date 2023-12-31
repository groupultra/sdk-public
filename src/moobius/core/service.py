# service.py

import json
import time

from dataclasses import asdict
from dacite import from_dict

from moobius.types import MessageBody
from .basic_service import MoobiusBasicService


# with database
class MoobiusService(MoobiusBasicService):
    '''
    MoobiusService provides a basic service class containing higher-level interfaces for users, e.g., self.bands.
    Users can use self.bands to access the data of different bands.
    These interfaces are built on top of the basic interfaces provided by MoobiusBasicService, and can be used to build more complex services.
    '''
    def __init__(self, service_config_path="", db_config_path="", **kwargs):
        '''
        Initialize a MoobiusService object.
        
        Parameters:
            service_config_path: str
                The path of the service config file.
            db_config_path: str
                The path of the database config file.
        
        Returns:
            None
        
        Example:
            >>> service = MoobiusService(service_config_path="config/service.json", db_config_path="config/database.json")
        '''
        super().__init__(config_path=service_config_path)

        with open(db_config_path, "r") as f:
            self.db_config = json.load(f)

        self.bands = {}

    async def upload_avatar_and_create_character(self, service_id, username, nickname, image_path, description):
        '''
        Upload an avatar image and create a character.
        
        Parameters:
            service_id: str
                The id of the service.
            username: str
                The username of the character.
            nickname: str
                The nickname of the character.
            image_path: str
                The path of the avatar image. This should be the local path of the image.
            description: str
                The description of the character.
        
        Returns:
            The Character object of the created character.
    
        Example:
            >>> character = await self.upload_avatar_and_create_character(service_id, username, nickname, image_path, description)
        '''
        avatar = self.http_api.upload_file(image_path)
        return self.http_api.create_service_user(service_id, username, nickname, avatar, description)

    async def fetch_real_characters(self, channel_id):
        '''
        Fetch all real characters in a channel.
        
        Parameters:
            channel_id: str
                The id of the channel.
            
        Returns:
            A list of Character objects.
        
        Example:
            >>> characters = await self.fetch_real_characters(channel_id)
        '''
        return self.http_api.fetch_real_characters(channel_id, self.service_id)

    async def create_message(self, channel_id, content, recipients, subtype='text', sender=None):
        '''
        Create a MessageDown object and send it to the channel.
        
        Parameters:
            channel_id: str
                The id of the channel.
            content: str
                The content of the message.
            recipients: list
                The recipients of the message.
            subtype: str
                The subtype of the message.
            sender: str
                The sender of the message.
        
        Returns:
            None
        
        Example:
            >>> await self.create_message(channel_id, content, recipients, subtype='text', sender=None)
        '''
        await self.send_msg_down(
            channel_id=channel_id,
            recipients=recipients,
            subtype=subtype,
            message_content=content,
            sender=sender or 'no_sender'
        )
