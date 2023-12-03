# http_api_wrapper.py
import requests
from moobius.basic.logging_config import log_error, log_info
from dacite import from_dict
from moobius.basic._types import Character, Group
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
            log_error(f"Error during authentication: {response.json().get('msg')}")
            return None
        
    def refresh(self):
        url = self.http_server_uri + "/auth/refresh"
        data = {"username": self.username, "refresh_token": self.refresh_token}
        response = requests.post(url, json=data)
        
        if response.json().get('code') == 10000:
            self.access_token = response.json().get('data').get('AuthenticationResult').get('AccessToken')
            
            return self.access_token
        else:
            log_error(f"Error during refresh: {response.json().get('msg')}")
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
            log_info("Successfully fetched channel userlist!")
            userlist = response.json()["data"]["userlist"]

            return [from_dict(data_class=Character, data=d) for d in userlist]
        else:
            log_error(f"Error fetching channel userlist: {response.json().get('msg')}")
            return None
    
    
    def fetch_user_profile(self, user_id):
        data = {
            "userlist": [user_id]
        }
        url = self.http_server_uri + "/user/fetch_profile"
        response = requests.post(url, json=data, headers=self.headers)
        
        # Check response
        if response.json().get('code') == 10000:
            log_info("Successfully fetched user profile!")
            data=response.json()['data'][user_id]
            data['user_id'] = user_id
            character = from_dict(data_class=Character, data=data)
            return character
        else:
            log_error(f"Error fetching user profile: {response.json().get('msg')}")
            return None
    
    def fetch_real_characters(self, channel_id, service_id):
        channel_userlist = self.get_channel_userlist(channel_id, service_id)
        if channel_userlist:
            return channel_userlist
        else:
            return []
        
    
    def create_service(self, description):
        data = {
            "description": description
        }
        url = self.http_server_uri + "/service/create"
        response = requests.post(url, json=data, headers=self.headers)
        log_info(f"create_service response{response.json()}")
        # Check response
        if response.json().get('code') == 10000:
            log_info("Successfully created service!")
            return response.json().get('data').get('service_id')
        else:
            log_error(f"Error creating service: {response.json().get('msg')}")
            return None
    
    def bind_service_to_channel(self, service_id, channel_id):
        data = {
            "channel_id": channel_id,
            "service_id": service_id
        }
        url = self.http_server_uri + "/service/bind"
        response = requests.post(url, json=data, headers=self.headers)
        log_info(f"bind_service_to_channel response {response.json()}")
        # Check response
        if response.json().get('code') == 10000:
            log_info(f"Successfully binded service {service_id} with channel {channel_id}!")
            return True
        else:
            log_error(f"Error binding service with channel: {response.json().get('msg')}")
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
            log_info(f"Successfully unbinded service {service_id} with channel {channel_id}!")
        else:
            log_error(f"Error unbinding service with channel: {response.json().get('msg')}")
            
    def get_service_list(self):
        url = self.http_server_uri + "/service/list"
        response = requests.get(url, headers=self.headers)
        # Check response
        if response.json().get('code') == 10000:
            log_info(f"Successfully get service list!")
            return response.json().get('data')
        else:
            log_error(f"Error getting service list: {response.json().get('msg')}")
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
            log_info(f"Successfully created service user!")
            character = from_dict(data_class=Character, data=response.json()['data'])
            return character
        else:
            log_error(f"Error creating service user: {response.json().get('msg')}")
            
            return None
        
    def create_service_user_with_local_image(self, service_id, username, nickname, image_path, description):
        avatar = self.upload_file(image_path)
        return self.create_service_user(service_id, username, nickname, avatar, description)
        
    def create_service_group(self, group_id, user_uuids):
        url = self.http_server_uri + "/service/group/create"
        data = {
            "group_id": group_id,
            "members": user_uuids
        }
        response = requests.post(url, json=data, headers=self.headers)
        # Check response
        if response.json().get('code') == 10000:
            log_info(f"Successfully created service group!")
            group = from_dict(data_class=Group, data=response.json()['data'])
            return group
        else:
            log_error(f"Error creating service group: {response.json().get('msg')}")
            return None
        
    def get_service_user_list(self, service_id):
        url = self.http_server_uri + f"/service/user/list?service_id={service_id}"
        
        response = requests.get(url, headers=self.headers)
        log_info(f"get_service_user_list response: {response.json()}")
        # Check response
        if response.json().get('code') == 10000:
            log_info(f"Successfully got service user!")
            userlist = response.json()["data"]
            return [from_dict(data_class=Character, data=d) for d in userlist]
        else:
            log_error(f"Error creating service user: {response.json().get('msg')}")
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
                log_info("Successfully fetched user profile!")
                character = from_dict(data_class=Character, data=response_data['data'])
                return character
            else:
                log_error(f"Error fetching user profile: {response_data.get('msg')}")
                return None
        except requests.RequestException as e:
            log_error(f"Network error: {e}")
            return None
        except Exception as e:
            log_error(f"Unexpected error: {e}")
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
                log_info("Successfully fetched upload url!")
                upload_url = response_data.get('data').get('url')
                upload_fields = response_data.get('data').get('fields')
                return upload_url, upload_fields
            else:
                log_error(f"Error fetching upload url: {response_data.get('msg')}")
                return None
        except requests.RequestException as e:
            log_error(f"Network error: {e}")
            return None
        except Exception as e:
            log_error(f"Unexpected error: {e}")
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
            log_error(f"Network error: {e}")
            return None
        except Exception as e:
            log_error(f"Unexpected error: {e}")
            return None
        
    def upload_file(self, file_path):
        extension = file_path.split(".")[-1]
        upload_url, upload_fields = self.upload_with_extension(extension)
        if upload_url and upload_fields:
            full_url = self.do_upload_file(upload_url, upload_fields, file_path)
            if full_url:
                log_info(f"Successfully uploaded file! {full_url}")
                return full_url
            else:
                log_error("Error uploading file!")
                return None
        else:
            log_error("Error uploading file!")
            return None
        