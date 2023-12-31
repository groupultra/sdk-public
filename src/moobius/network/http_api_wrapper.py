# http_api_wrapper.py
import requests
from loguru import logger
from dacite import from_dict
from moobius.types import Character, Group
# todo: refresh
# todo: return code


class HTTPAPIWrapper:
    '''
    Helper class for interacting with the Moobius HTTP API.
    All methods except for authenticate() and refresh() require authentication headers. 
    When calling these methods, make sure to call authenticate() first and add headers=self.headers to the method call.
    
    Auth:
        - headers()
        - authenticate()
        - refresh()
        
    User:
        - get_channel_user_list(channel_id, service_id)
        - fetch_user_profile(user_id)
        - fetch_real_characters(channel_id, service_id)
        - fetch_user_from_group(user_id, channel_id, group_id)
        - get_service_user_list(service_id)
        
    Service:
        - create_service(description)
        - bind_service_to_channel(service_id, channel_id)
        - unbind_service_from_channel(service_id, channel_id)
        - get_service_list()
        - create_service_user(service_id, username, nickname, avatar, description)
        - create_service_group(group_id, user_uuids)
    
    File:
        - upload_with_extension(extension)
        - do_upload_file(upload_url, upload_fields, file_path)
        - upload_file(file_path)    
    '''
    def __init__(self, http_server_uri="", email="", password=""):
        '''
        Initialize the HTTP API wrapper.
        
        Parameters:
            http_server_uri: str
                The URI of the Moobius HTTP server.
            email: str
                The email of the user.
            password: str
                The password of the user.
        
        Returns:
            None
        
        Example:
            >>> http_api_wrapper = HTTPAPIWrapper("http://localhost:8080", "test@test", "test")
        '''
        self.http_server_uri = http_server_uri
        self.username = email
        self.password = password
        self.access_token = ""
        self.refresh_token = ""

    # ==================== Auth ====================
    
    @property
    def headers(self):
        '''
        Returns the authentication headers. Used for all API calls except for authenticate() and refresh().
        
        Parameters:
            None
        
        Returns:
            dict
                The authentication headers.
        
        Example:
            >>> response = requests.get(url, params=params, headers=self.headers)
        '''
        return {
            "Auth-Origin": "cognito",
            "Authorization": f"Bearer {self.access_token}"
        }

    @logger.catch
    def authenticate(self):
        '''
        Authenticate the user. Needs to be called before any other API calls.
        
        Parameters:
            None
        
        Returns:
            tuple
                The access token and refresh token. Exception if doesn't receive a valid response.
            
        Example:
            >>> access_token, refresh_token = http_api_wrapper.authenticate()
            
        Raises:
            Exception: If the authentication fails, this function will raise an exception about the error during authentication.
        '''
        url = self.http_server_uri + "/auth/sign_in"
        data = {"username": self.username, "password": self.password}
        response = requests.post(url, json=data)
        
        if response.json().get('code') == 10000:
            self.access_token = response.json().get('data').get('AuthenticationResult').get('AccessToken')
            self.refresh_token = response.json().get('data').get('AuthenticationResult').get('RefreshToken')
            
            return self.access_token, self.refresh_token
        else:
            raise Exception(f"Error during authentication: {response.json()}")
    
    
    def refresh(self):
        '''
        Refresh the access token.
        
        Parameters:
            None
        
        Returns:
            str
                The new access token. None if doesn't receive a valid response, please check the logs for more information.
        
        Example:
            >>> access_token = http_api_wrapper.refresh()
        
        Raises:
            Exception: If the refresh fails, this function will raise an exception about the error during refresh.
        '''
        url = self.http_server_uri + "/auth/refresh"
        data = {"username": self.username, "refresh_token": self.refresh_token}
        response = requests.post(url, json=data)
        
        if response.json().get('code') == 10000:
            self.access_token = response.json().get('data').get('AuthenticationResult').get('AccessToken')
            
            return self.access_token
        else:
            logger.error(f"Error during refresh: {response.json().get('msg')}")
            raise Exception(f"Error during refresh: {response.json().get('msg')}")
        
    # ==================== User ====================
    
    def get_channel_user_list(self, channel_id, service_id):
        '''
        Get the user list of a channel.
        
        Parameters:
            channel_id: str
                The channel ID.
            service_id: str
                The service ID.
            
        Returns:
            list
                A list of Character objects. Empty list if doesn't receive a valid response, please check the logs for more information.
        
        Example:
            >>> user_list = http_api_wrapper.get_channel_user_list(channel_id, service_id)
        
        Raises:
            Exception: If the channel user list fetch fails, this function will raise an exception about the error.
        '''
        params = {
            "channel_id": channel_id,
            "service_id": service_id
        }

        url = self.http_server_uri + "/channel/userlist"
        response = requests.get(url, params=params, headers=self.headers)
        # Check response
        if response.json().get('code') == 10000:
            logger.debug("Successfully fetched channel userlist!")
            userlist = response.json()["data"]["userlist"]

            return [from_dict(data_class=Character, data=d) for d in userlist]
        else:
            logger.error(f"Error fetching channel userlist: {response.json().get('msg')}, channel_id: {channel_id}, service_id: {service_id}")
            raise Exception(f"Error fetching channel userlist: {response.json().get('msg')}, channel_id: {channel_id}, service_id: {service_id}")
    
    def fetch_user_profile(self, user_id):
        '''
        Fetch the user profile of a user. 
        
        Parameters:
            user_id: str
                The user ID.
        
        Returns:
            Character
                The user profile. None if doen't receive a valid response, please check the logs for more information.
        
        Example:
            >>> character = http_api_wrapper.fetch_user_profile(user_id)
            
        Raises:
            Exception: If the user profile fetch fails, this function will raise an exception about the error.
        '''
        data = {
            "userlist": [user_id]
        }
        url = self.http_server_uri + "/user/fetch_profile"
        response = requests.post(url, json=data, headers=self.headers)
        
        # Check response
        if response.json().get('code') == 10000:
            logger.debug("Successfully fetched user profile!")
            data=response.json()['data'][user_id]
            data['user_id'] = user_id
            character = from_dict(data_class=Character, data=data)
            return character
        else:
            logger.error(f"Error fetching user profile: {response.json().get('msg')}, user_id: {user_id}")
            raise Exception(f"Error fetching user profile: {response.json().get('msg')}, user_id: {user_id}")
    
    def fetch_real_characters(self, channel_id, service_id):
        '''
        Fetch the real characters of a channel.
        
        Parameters:
            channel_id: str
                The channel ID.
            service_id: str
                The service ID.
            
        Returns:
            list
                A list of Character objects. Empty list if doesn't receive a valid response, please check the logs for more information.
        
        Example:
            >>> real_characters = http_api_wrapper.fetch_real_characters(channel_id, service_id)
            
        Raises:
            Exception: If the real characters fetch fails, this function will raise an exception about the error.
        '''
        channel_userlist = self.get_channel_user_list(channel_id, service_id)
        if channel_userlist:
            return channel_userlist
        else:
            raise Exception(f"Error fetching real characters: {response.json().get('msg')}, channel_id: {channel_id}, service_id: {service_id}")
        
    def fetch_user_from_group(self, user_id, channel_id, group_id):
        '''
        Fetch the user profile of a user from a group.
        
        Parameters:
            user_id: str
                The user ID.
            channel_id: str
                The channel ID.
            group_id: str
                The group ID.
                
        Returns:
            Character
                The user profile. None if doen't receive a valid response, please check the logs for more information.
        
        Example:
            >>> character = http_api_wrapper.fetch_user_from_group(user_id, channel_id, group_id)
        
        Raises:
            Exception: If the user profile fetch fails, this function will raise an exception about the error.
        '''
        params = {
            "user_id": user_id,
            "channel_id": channel_id,
            "group_id": group_id
        }
        url = self.http_server_uri + "/user/group"
        response = requests.get(url, params=params, headers=self.headers)
        response_data = response.json()
        
        # Check response
        if response_data.get('code') == 10000:
            logger.debug("Successfully fetched user profile!")
            character = from_dict(data_class=Character, data=response_data['data'])
            return character
        else:
            logger.error(f"Error fetching user profile: {response_data.get('msg')}, user_id: {user_id}, channel_id: {channel_id}, group_id: {group_id}")
            raise Exception(f"Error fetching user profile: {response_data.get('msg')}, user_id: {user_id}, channel_id: {channel_id}, group_id: {group_id}")

    def get_service_user_list(self, service_id):
        '''
        Get the user list of a service.
        
        Parameters:
            service_id: str
                The service ID.
                
        Returns:
            list
                A list of Character objects. None if doesn't receive a valid response, please check the logs for more information.

        Example:
            >>> user_list = http_api_wrapper.get_service_user_list(service_id)
        
        Raises:
            Exception: If the service user list fetch fails, this function will raise an exception about the error.
        '''
        url = self.http_server_uri + f"/service/user/list?service_id={service_id}"
        
        response = requests.get(url, headers=self.headers)
        logger.debug(f"get_service_user_list response: {response.json()}")
        # Check response
        if response.json().get('code') == 10000:
            logger.debug(f"Successfully got service user!")
            userlist = response.json()["data"]
            return [from_dict(data_class=Character, data=d) for d in userlist]
        else:
            logger.error(f"Error creating service user: {response.json().get('msg')}, service_id: {service_id}")
            raise Exception(f"Error creating service user: {response.json().get('msg')}, service_id: {service_id}")
    
    # ==================== Service ====================
    
    def create_service(self, description):
        '''
        Create a service with the given description.
        
        Parameters:
            description: str
                The description of the service.
        
        Returns:
            str
                The service ID. None if doesn't receive a valid response, please check the logs for more information.
        
        Example:
            >>> service_id = http_api_wrapper.create_service(description)
            
        Raises:
            Exception: If the service creation fails, this function will raise an exception about the error.
        '''
        data = {
            "description": description
        }
        url = self.http_server_uri + "/service/create"
        response = requests.post(url, json=data, headers=self.headers)
        logger.debug(f"create_service response{response.json()}")
        # Check response
        if response.json().get('code') == 10000:
            logger.debug("Successfully created service!")
            return response.json().get('data').get('service_id')
        else:
            logger.error(f"Error creating service: {response.json().get('msg')}, description: {description}")
            raise Exception(f"Error creating service: {response.json().get('msg')}, description: {description}")
    
    def bind_service_to_channel(self, service_id, channel_id):
        '''
        Bind a service to a channel.
        
        Parameters:
            service_id: str
                The service ID.
            channel_id: str
                The channel ID.
        
        Returns:
            bool
                True if successfully binded, False otherwise. Please check the logs for more information.
        
        Example:
            >>> success = http_api_wrapper.bind_service_to_channel(service_id, channel_id)
        '''
        data = {
            "channel_id": channel_id,
            "service_id": service_id
        }
        url = self.http_server_uri + "/service/bind"
        response = requests.post(url, json=data, headers=self.headers)
        logger.debug(f"bind_service_to_channel response {response.json()}")
        # Check response
        if response.json().get('code') == 10000:
            logger.debug(f"Successfully binded service {service_id} to channel {channel_id}!")
            return True
        else:
            logger.error(f"Error binding service to channel: {response.json().get('msg')}, service_id: {service_id}, channel_id: {channel_id}")
            return False
    
    def unbind_service_from_channel(self, service_id, channel_id):
        '''
        Unbind a service from a channel.
        
        Parameters:
            service_id: str
                The service ID.
            channel_id: str
                The channel ID.
            
        Returns:
            None
                We report the unbinding result in the logs.

        Example:
            >>> http_api_wrapper.unbind_service_from_channel(service_id, channel_id)
        
        Raises:
            Exception: If the service unbinding fails, this function will raise an exception about the error.
        '''
        data = {
            "channel_id": channel_id,
            "service_id": service_id
        }
        url = self.http_server_uri + "/service/unbind"
        response = requests.post(url, json=data, headers=self.headers)
        
        # Check response
        if response.json().get('code') == 10000:
            logger.debug(f"Successfully unbinded service {service_id} from channel {channel_id}!")
        else:
            logger.error(f"Error unbinding service from channel: {response.json().get('msg')}, service_id: {service_id}, channel_id: {channel_id}")
            raise Exception(f"Error unbinding service from channel: {response.json().get('msg')}, service_id: {service_id}, channel_id: {channel_id}")
            
    def get_service_list(self):
        '''
        Get the service list of the user.
        
        Parameters:
            None
        
        Returns:
            list
                A list of service IDs of the user. None if doesn't receive a valid response, please check the logs for more information.
        
        Example:
            >>> service_list = http_api_wrapper.get_service_list()
        
        Raises:
            Exception: If the service list fetch fails, this function will raise an exception about the error.
        '''
        url = self.http_server_uri + "/service/list"
        response = requests.get(url, headers=self.headers)
        
        if response.json().get('code') == 10000:
            return response.json().get('data')
        else:
            logger.error(f"Error getting service list: {response.json().get('msg')}")
            raise Exception(f"Error getting service list: {response.json().get('msg')}")
    
    def create_service_user(self, service_id, username, nickname, avatar, description):
        '''
        Create a service user. The user will be created with the given username, nickname, avatar, and description.
        The created user will be bound to the given service.
        
        Parameters:
            service_id: str
                The service ID.
            username: str
                The username of the user.
            nickname: str
                The nickname of the user.
            avatar: str
                The avatar of the user. Should be a URL.
            description: str
                The description of the user.
        
        Returns:
            Character
                The created user. None if doesn't receive a valid response, please check the logs for more information.
        
        Example:
            >>> character = http_api_wrapper.create_service_user(service_id, username, nickname, avatar, description)
        
        Raises:
            Exception: If the service user creation fails, this function will raise an exception about the error.
        '''
        url = self.http_server_uri + "/service/user/create"
        data = {
            "service_id": service_id,
            "username": username,
            "context": {
                "nickname": nickname,
                "avatar": avatar,
                "description": description
            }
        }
        
        response = requests.post(url, json=data, headers=self.headers)
               
        if response.json().get('code') == 10000:
            logger.debug(f"Successfully created service user!")
            character = from_dict(data_class=Character, data=response.json()['data'])
            return character
        else:
            logger.error(f"Error creating service user: {response.json().get('msg')}, service_id: {service_id}, username: {username}, nickname: {nickname}, avatar: {avatar}, description: {description}")
            raise Exception(f"Error creating service user: {response.json().get('msg')}, service_id: {service_id}, username: {username}, nickname: {nickname}, avatar: {avatar}, description: {description}")
        
    def create_service_group(self, group_id, user_uuids):
        '''
        Create a user group. The group will be created with the given group ID and user UUIDs.
        
        Parameters:
            group_id: str
                The group ID.
            user_uuids: list
                A list of user UUIDs.
        
        Returns:
            Group
                The created group. None if doesn't receive a valid response, please check the logs for more information.
        
        Example:
            >>> group = http_api_wrapper.create_service_group(group_id, user_uuids)
        
        Raises:
            Exception: If the service group creation fails, this function will raise an exception about the error.
        '''
        url = self.http_server_uri + "/service/group/create"
        data = {
            "group_id": group_id,
            "members": user_uuids
        }
        response = requests.post(url, json=data, headers=self.headers)
        # Check response
        if response.json().get('code') == 10000:
            logger.debug(f"Successfully created service group!")
            group = from_dict(data_class=Group, data=response.json()['data'])
            return group
        else:
            logger.error(f"Error creating service group: {response.json().get('msg')}, group_id: {group_id}, user_uuids: {user_uuids}")
            raise Exception(f"Error creating service group: {response.json().get('msg')}, group_id: {group_id}, user_uuids: {user_uuids}")
    
    # ==================== File ====================
    
    def upload_with_extension(self, extension):
        '''
        Get the upload URL and upload fields for uploading a file with the given extension.
        
        Parameters:
            extension: str
                The extension of the file.
        
        Returns:
            tuple
                The upload URL and upload fields. None if doesn't receive a valid response, please check the logs for more information.
        
        Example:
            >>> upload_url, upload_fields = http_api_wrapper.upload_with_extension(extension)
        
        Raises:
            Exception: If the upload URL fetch fails, this function will raise an exception about the error.
        '''
        params = {
            "extension": extension
        }

        url = self.http_server_uri + "/file/upload"
        
        response = requests.get(url, params=params, headers=self.headers)
        response_data = response.json()
        
        # Check response
        if response_data.get('code') == 10000:
            logger.debug("Successfully fetched upload url!")
            upload_url = response_data.get('data').get('url')
            upload_fields = response_data.get('data').get('fields')
            return upload_url, upload_fields
        else:
            logger.error(f"Error fetching upload url: {response_data.get('msg')}")
            raise Exception(f"Error fetching upload url: {response_data.get('msg')}")

    def do_upload_file(self, upload_url, upload_fields, file_path):
        '''
        Upload a file to the given upload URL with the given upload fields.
        
        Parameters:
            upload_url: str
                The upload URL.
            upload_fields: dict
                The upload fields.
            file_path: str
                The path of the file.
        
        Returns:
            str
                The full URL of the uploaded file. None if doesn't receive a valid response, please check the logs for more information.
        
        Example:
            >>> full_url = http_api_wrapper.do_upload_file(upload_url, upload_fields, file_path)
        
        Raises:
            Exception: If the file upload fails, this function will raise an exception about the error.
        '''
        
        with open(file_path, 'rb') as f:
            files = {'file': (file_path, f)}
            response = requests.post(upload_url, data=upload_fields, files=files)
            full_url = upload_url + upload_fields.get("key")
            if response.status_code == 204:
                return full_url
            else:
                logger.error(f"Error uploading file: {response.json().get('msg')}, upload_url: {upload_url}, upload_fields: {upload_fields}, file_path: {file_path}")
                raise Exception(f"Error uploading file: {response.json().get('msg')}, upload_url: {upload_url}, upload_fields: {upload_fields}, file_path: {file_path}")
        
    def upload_file(self, file_path):
        '''
        Upload a file to the Moobius server. This method will automatically get the upload URL and upload fields.

        Parameters:
            file_path: str
                The path of the file. This should be a local file path.
        
        Returns:
            str
                The full URL of the uploaded file. None if doesn't receive a valid response, please check the logs for more information.
        
        Example:
            >>> full_url = http_api_wrapper.upload_file(file_path)
            
        Raises:
            Exception: If the file upload fails, this function will raise an exception about the error.
        '''
        extension = file_path.split(".")[-1]
        upload_url, upload_fields = self.upload_with_extension(extension)
        if upload_url and upload_fields:
            # Exception will be raised in do_upload_file(), no need to raise here
            full_url = self.do_upload_file(upload_url, upload_fields, file_path)
            return full_url
        else:
            logger.error(f"Error getting upload url and upload fields! file_path: {file_path}")
            raise Exception(f"Error getting upload url and upload fields! file_path: {file_path}")
        
    def get_user_info(self):
        url = self.http_server_uri + f"/user/info"
        response = requests.get(url, headers=self.headers)
        # Check response
        if response.json().get('code') == 10000:
            logger.info(f"Successfully got user info!")
            return response.json().get('data')
        else:
            logger.error(f"Error getting user info: {response.json().get('msg')}")
            raise Exception(f"Error getting user info: {response.json().get('msg')}")