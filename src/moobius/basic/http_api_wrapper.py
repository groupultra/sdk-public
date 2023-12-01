# http_api_wrapper.py
import requests
from moobius.basic._logging_config import logger
# todo: refresh
# todo: return code
class HTTPAPIWrapper:
    def __init__(self, http_server_uri="", email="", password=""):
        self.http_server_uri = http_server_uri
        self.username = email
        self.password = password
        self.access_token = ""
        self.refresh_token = ""

    @property
    def headers(self):
        return {
            "Auth-Origin": "cognito",
            "Authorization": f"Bearer {self.access_token}"
        }
        
    def authenticate(self):
        url = self.http_server_uri + "/auth/sign_in"
        data = {"username": self.username, "password": self.password}
        response = requests.post(url, json=data)
        
        if response.json().get('code') == 10000:
            self.access_token = response.json().get('data').get('AuthenticationResult').get('AccessToken')
            self.refresh_token = response.json().get('data').get('AuthenticationResult').get('RefreshToken')
            
            return self.access_token, self.refresh_token
        else:
            logger.error(f"Error during authentication: {response.json().get('msg')}")
            return None
        
    def refresh(self):
        url = self.http_server_uri + "/auth/refresh"
        data = {"username": self.username, "refresh_token": self.refresh_token}
        response = requests.post(url, json=data)
        
        if response.json().get('code') == 10000:
            self.access_token = response.json().get('data').get('AuthenticationResult').get('AccessToken')
            
            return self.access_token
        else:
            logger.error(f"Error during refresh: {response.json().get('msg')}")
            return None


    def get_channel_userlist(self, channel_id, service_id):
        params = {
            "channel_id": channel_id,
            "service_id": service_id
        }

        url = self.http_server_uri + "/channel/userlist"
        response = requests.get(url, params=params, headers=self.headers)
        # Check response
        if response.json().get('code') == 10000:
            logger.info("Successfully fetched channel userlist!")
            return response.json()
        else:
            logger.error(f"Error fetching channel userlist: {response.json().get('msg')}")
            return None
    
    
    def fetch_user_profile(self, userlist):
        data = {
            "userlist": userlist
        }
        url = self.http_server_uri + "/user/fetch_profile"
        response = requests.post(url, json=data, headers=self.headers)
        
        # Check response
        if response.json().get('code') == 10000:
            logger.info("Successfully fetched user profile!")
            return response.json()
        else:
            logger.error(f"Error fetching user profile: {response.json().get('msg')}")
            return None
        
    
    def create_service(self, description):
        data = {
            "description": description
        }
        url = self.http_server_uri + "/service/create"
        response = requests.post(url, json=data, headers=self.headers)
        logger.info("create_service response", response.json())
        # Check response
        if response.json().get('code') == 10000:
            logger.info("Successfully created service!")
            return response.json().get('data').get('service_id')
        else:
            logger.error(f"Error creating service: {response.json().get('msg')}")
            return None
    
    def bind_service_to_channel(self, service_id, channel_id):
        data = {
            "channel_id": channel_id,
            "service_id": service_id
        }
        url = self.http_server_uri + "/service/bind"
        response = requests.post(url, json=data, headers=self.headers)
        logger.info(f"bind_service_to_channel response {response.json()}")
        # Check response
        if response.json().get('code') == 10000:
            logger.info(f"Successfully binded service {service_id} with channel {channel_id}!")
            return True
        else:
            logger.error(f"Error binding service with channel: {response.json().get('msg')}")
            return False
    
    def unbind_service_from_channel(self, service_id, channel_id):
        data = {
            "channel_id": channel_id,
            "service_id": service_id
        }
        url = self.http_server_uri + "/service/unbind"
        response = requests.post(url, json=data, headers=self.headers)
        
        # Check response
        if response.json().get('code') == 10000:
            logger.info(f"Successfully unbinded service {service_id} with channel {channel_id}!")
        else:
            logger.error(f"Error unbinding service with channel: {response.json().get('msg')}")
            
    def get_service_list(self):
        url = self.http_server_uri + "/service/list"
        response = requests.get(url, headers=self.headers)
        # Check response
        if response.json().get('code') == 10000:
            logger.info(f"Successfully get service list!")
            return response.json().get('data')
        else:
            logger.error(f"Error getting service list: {response.json().get('msg')}")
            return None
    
    def create_service_user(self, service_id, username, nickname, avatar, description):
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
            logger.info(f"Successfully created service user!")
            return response.json().get('data')
        else:
            logger.error(f"Error creating service user: {response.json().get('msg')}")
            
            return None
        
    def create_service_user_with_local_image(self, service_id, username, nickname, avatar, description, image_path):
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
        
        files = {
            "image": open(image_path, "rb")
        }
        
        response = requests.post(url, data=data, files=files, headers=self.headers)
               
        if response.json().get('code') == 10000:
            logger.info(f"Successfully created service user!")
            return response.json().get('data')
        else:
            logger.error(f"Error creating service user: {response.json().get('msg')}")
            
            return None
        
    def create_service_group(self, group_id, user_uuids):
        url = self.http_server_uri + "/service/group/create"
        data = {
            "group_id": group_id,
            "members": user_uuids
        }
        response = requests.post(url, json=data, headers=self.headers)
        # create_service_group response: {'code': 10000, 'data': '158929e8-808d-403f-b491-10de98206103', 'msg': 'Create success'}
        # Check response
        if response.json().get('code') == 10000:
            logger.info(f"Successfully created service group!")
            return response.json().get('data')
        else:
            logger.error(f"Error creating service group: {response.json().get('msg')}")
            return None
        
    def get_service_user_list(self, service_id):
        url = self.http_server_uri + f"/service/user/list?service_id={service_id}"
        
        response = requests.get(url, headers=self.headers)
        logger.info(f"get_service_user_list response: {response.json()}")
        # Check response
        if response.json().get('code') == 10000:
            logger.info(f"Successfully got service user!")
            return response.json().get('data')
        else:
            logger.error(f"Error creating service user: {response.json().get('msg')}")
            return None
    
    def fetch_user_from_group(self, user_id, channel_id, group_id):
        params = {
            "user_id": user_id,
            "channel_id": channel_id,
            "group_id": group_id
        }
        url = self.http_server_uri + "/user/group"
        try:
            response = requests.get(url, params=params, headers=self.headers)
            response_data = response.json()
            
            # Check response
            if response_data.get('code') == 10000:
                logger.info("Successfully fetched user profile!")
                return response_data
            else:
                logger.error(f"Error fetching user profile: {response_data.get('msg')}")
                return None
        except requests.RequestException as e:
            logger.error(f"Network error: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return None


    def upload_with_extension(self, extension):
        params = {
            "extension": extension
        }

        url = self.http_server_uri + "/file/upload"
        try:
            response = requests.get(url, params=params, headers=self.headers)
            response_data = response.json()
            
            # Check response
            if response_data.get('code') == 10000:
                logger.info("Successfully fetched upload url!")
                upload_url = response_data.get('data').get('url')
                upload_fields = response_data.get('data').get('fields')
                return upload_url, upload_fields
            else:
                logger.error(f"Error fetching upload url: {response_data.get('msg')}")
                return None
        except requests.RequestException as e:
            logger.error(f"Network error: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return None
        
    def do_upload_file(self, upload_url, upload_fields, file_path):
        try:
            with open(file_path, 'rb') as f:
                files = {'file': (file_path, f)}
                response = requests.post(upload_url, data=upload_fields, files=files)
                full_url = upload_url + upload_fields.get("key")
                if response.status_code == 204:
                    return full_url
                return response
        except requests.RequestException as e:
            logger.error(f"Network error: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return None
        
    def upload_file(self, file_path):
        extension = file_path.split(".")[-1]
        upload_url, upload_fields = self.upload_with_extension(extension)
        if upload_url and upload_fields:
            full_url = self.do_upload_file(upload_url, upload_fields, file_path)
            if full_url:
                logger.info(f"Successfully uploaded file! {full_url}")
                return full_url
            else:
                logger.error("Error uploading file!")
                return None
        else:
            logger.error("Error uploading file!")
            return None
        