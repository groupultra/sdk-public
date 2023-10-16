# http_api_wrapper.py
import requests

# todo: refresh
# todo: return code
class HTTPAPIWrapper:
    def __init__(self, http_server_uri=""):
        self.headers = {"Auth-Origin": "cognito"}
        self.http_server_uri = http_server_uri
        
    def authenticate(self, email, password):
        url = self.http_server_uri + "/auth/sign_in"
        data = {"username": email, "password": password}
        response = requests.post(url, json=data)
        
        if response.json().get('code') == 10000:
            self.headers["Authorization"] = f"Bearer {response.json().get('data').get('AuthenticationResult').get('AccessToken')}"
            
            access_token = response.json().get('data').get('AuthenticationResult').get('AccessToken')
            refresh_token = response.json().get('data').get('AuthenticationResult').get('RefreshToken')
            
            return access_token, refresh_token
        else:
            print("Error during authentication:", response.json().get('msg'))
            return None
        
    
    def get_channel_userlist(self, channel_id, service_id):
        params = {
            "channel_id": channel_id,
            "service_id": service_id
        }

        url = self.http_server_uri + "/channel/userlist"
        response = requests.get(url, params=params, headers=self.headers)
        print(response)
        # Check response
        if response.json().get('code') == 10000:
            print("Successfully fetched channel userlist!")
            return response.json()
        else:
            print("Error fetching channel userlist:", response.json().get('msg'))
            return None
    
    
    def fetch_user_profile(self, userlist):
        data = {
            "userlist": userlist
        }
        url = self.http_server_uri + "/user/fetch_profile"
        response = requests.post(url, json=data, headers=self.headers)
        
        # Check response
        if response.json().get('code') == 10000:
            print("Successfully fetched user profile!")
            return response.json()
        else:
            print("Error fetching user profile:", response.json().get('msg'))
            return None
        
    
    def create_service(self, description):
        data = {
            "description": description
        }
        url = self.http_server_uri + "/service/create"
        response = requests.post(url, json=data, headers=self.headers)
        
        # Check response
        if response.json().get('code') == 10000:
            print("Successfully created service!")
            return response.json().get('data').get('service_id')
        else:
            print("Error creating service:", response.json().get('msg'))
            return None
    
    def bind_service_to_channel(self, service_id, channel_id):
        data = {
            "channel_id": channel_id,
            "service_id": service_id
        }
        url = self.http_server_uri + "/service/bind"
        response = requests.post(url, json=data, headers=self.headers)
        
        # Check response
        if response.json().get('code') == 10000:
            print(f"Successfully binded service {service_id} with channel {channel_id}!")
            return True
        else:
            print("Error binding service with channel:", response.json().get('msg'))
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
            print(f"Successfully unbinded service {service_id} with channel {channel_id}!")
        else:
            print("Error unbinding service with channel:", response.json().get('msg'))
            
    def get_service_list(self):
        url = self.http_server_uri + "/service/list"
        response = requests.get(url, headers=self.headers)
        
        # Check response
        if response.json().get('code') == 10000:
            print(f"Successfully get service list!")
            return response.json().get('data')
        else:
            print("Error getting service list:", response.json().get('msg'))
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
        
        print("create_service_user data:", data)
        print("create_service_user headers:", self.headers)
        response = requests.post(url, json=data, headers=self.headers)
        print("create_service_user response:", response.json())
               
        if response.json().get('code') == 10000:
            print(f"Successfully created service user!")
            return response.json().get('data')
        else:
            print("Error creating service user:", response.json().get('msg'))
            return None
        
    def create_service_group(self, group_id, user_uuids):
        url = self.http_server_uri + "/service/group/create"
        data = {
            "group_id": group_id,
            "members": user_uuids
        }
        print("create_service_group data:", data)
        response = requests.post(url, json=data, headers=self.headers)
        print("create_service_group response:", response.json())
        # create_service_group response: {'code': 10000, 'data': '158929e8-808d-403f-b491-10de98206103', 'msg': 'Create success'}
        # Check response
        if response.json().get('code') == 10000:
            print(f"Successfully created service group!")
            return response.json().get('data')
        else:
            print("Error creating service group:", response.json().get('msg'))
            return None
        
    def get_service_user_list(self, service_id):
        url = self.http_server_uri + f"/service/user/list?service_id={service_id}"
        
        response = requests.get(url, headers=self.headers)
        print("get_service_user_list response:", response.json())
        # Check response
        if response.json().get('code') == 10000:
            print(f"Successfully got service user!")
            return response.json().get('data')
        else:
            print("Error creating service user:", response.json().get('msg'))
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
                print("Successfully fetched user profile!")
                return response_data
            else:
                print("Error fetching user profile:", response_data.get('msg'))
                return None
        except requests.RequestException as e:
            print("Network error:", e)
            return None
        except Exception as e:
            print("Unexpected error:", e)
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
                print("Successfully fetched upload url!")
                upload_url = response_data.get('data').get('url')
                upload_fields = response_data.get('data').get('fields')
                return upload_url, upload_fields
            else:
                print("Error fetching upload url:", response_data.get('msg'))
                return None
        except requests.RequestException as e:
            print("Network error:", e)
            return None
        except Exception as e:
            print("Unexpected error:", e)
            return None
        
    def do_upload_file(self, upload_url, upload_fields, file_path):
        try:
            with open(file_path, 'rb') as f:
                files = {'file': (file_path, f)}
                response = requests.post(upload_url, data=upload_fields, files=files)
                print(response)
                print(upload_url)
                print(upload_fields)
                full_url = upload_url + upload_fields.get("key")
                if response.status_code == 204:
                    return full_url
                return response
        except requests.RequestException as e:
            print("Network error:", e)
            return None
        except Exception as e:
            print("Unexpected error:", e)
            return None
        
    def upload_file(self, file_path):
        extension = file_path.split(".")[-1]
        upload_url, upload_fields = self.upload_with_extension(extension)
        if upload_url and upload_fields:
            full_url = self.do_upload_file(upload_url, upload_fields, file_path)
            if full_url:
                print(f"Successfully uploaded file! {full_url}")
                return full_url
            else:
                print("Error uploading file!")
                return None
        else:
            print("Error uploading file!")
            return None
        