# http_api_wrapper.py
import requests, json
from loguru import logger
from dacite import from_dict
from moobius.types import Character, Group
# TODO: refresh
# TODO: return code

class BadResponseException(Exception):
    '''For when the network is not doing what it should.'''
    pass

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
        - fetch_user_profile(user_id)
        - fetch_real_characters(channel_id, service_id)
        - fetch_user_from_group(user_id, channel_id, group_id)
        - fetch_service_user_list(service_id)

    Service:
        - create_service(description)
        - bind_service_to_channel(service_id, channel_id)
        - unbind_service_from_channel(service_id, channel_id)
        - fetch_service_list()
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

    def _checked_get_or_post(self, url, the_request, is_post, requests_kwargs=None, good_msg=None, bad_msg="This HTTPs request failed", raise_errors=True):
        '''Runs a GET or POST request returning the result as a JSON with optional logging and error raising.

           Parameters:
             url: The https url.
             the_request: In dictionary form; the "json" kwarg is set to this. Can be None
             is_post: True for post, False for get.
             requests_kwargs=None: Extra argument dict to send to requests. None is equivalent to {}
             good_msg=None: The message to logger.debug. None means do not log.
             bad_msg="...": The message to prepend to logger.error if the response isnt code 10000.
             raise_errors=True: Raise a BadResponseException if POST returns an error.

           Returns:
             The https response as a dict, using requests.post(...).json() to parse it.

           Raises:
             BadResponseException if raise_errors=True and the response is an error response.'''
        if the_request is not None and type(the_request) is not dict:
            raise Exception(f'the_request must be None or a dict, not a {type(the_request)} because; dicts are turned into json.')
        if requests_kwargs is None:
            requests_kwargs = {}
        if the_request is not None:
            requests_kwargs['json'] = the_request
        logger.opt(colors=True).info(f"<fg 160,0,240>{'POST' if is_post else 'GET'} URL={url} json={(json.dumps(the_request) if the_request is not None else 'None').replace('<', '&lt;').replace('>', '&gt;')}</>")
        response_txt = (requests.post if is_post else requests.get)(url, **requests_kwargs)
        try:
            response_dict = response_txt.json()
        except Exception as e:
            raise Exception(f'Cannot JSON this string: {repr(response_txt)}\nError message: {e}')
        if response_dict.get('code') == 10000:
            if good_msg is not None:
                logger.debug(good_msg)
        else:
            error_code = response_dict.get('code')
            err_msg = f"{bad_msg+': ' if bad_msg else ''}'code='{error_code} 'msg='{response_dict.get('msg')}"
            if bad_msg is not None:
                logger.error(err_msg)
            if raise_errors:
                raise BadResponseException(err_msg)
        return response_dict

    def checked_get(self, url, the_request, requests_kwargs=None, good_msg=None, bad_msg="This HTTPs GET request failed", raise_errors=True):
        '''Same as self._checked_get_or_post but makes only for GET requests and of course no is_post parameter.'''
        return self._checked_get_or_post(url, the_request, False, requests_kwargs=requests_kwargs, good_msg=good_msg, bad_msg=bad_msg, raise_errors=raise_errors)
    def checked_post(self, url, the_request, requests_kwargs=None, good_msg=None, bad_msg="This HTTPs POST request failed", raise_errors=True):
        '''Same as self._checked_get_or_post but makes only for POST requests and of course no is_post parameter.'''
        return self._checked_get_or_post(url, the_request, True, requests_kwargs=requests_kwargs, good_msg=good_msg, bad_msg=bad_msg, raise_errors=raise_errors)

    ############################ Auth ############################

    @property
    def headers(self):
        '''
        Returns the authentication headers. Used for all API calls except for authenticate() and refresh().

        Parameters:
            None

        Returns:
            A dict equalt to {"Auth-Origin": "cognito", "Authorization": f"Bearer {self.access_token}"}

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
        Authenticates the user. Needs to be called before any other API calls.

        Parameters:
            None

        Returns:
            tuple
                The access token and refresh token. Exception if doesn't receive a valid response. None if not in the response.

        Example:
            >>> access_token, refresh_token = http_api_wrapper.authenticate()

        Raises:
            Exception: If the authentication fails, this function will raise an exception about the error during authentication.
        '''
        response_dict = self.checked_post(url=self.http_server_uri + "/auth/sign_in", the_request={"username": self.username, "password": self.password}, requests_kwargs=None, good_msg=None, bad_msg="Error during authentication", raise_errors=True)
        self.access_token = response_dict.get('data').get('AuthenticationResult').get('AccessToken')
        self.refresh_token = response_dict.get('data').get('AuthenticationResult').get('RefreshToken')
        logger.info(f"Authenticated. Access token: {self.access_token}")
        return self.access_token, self.refresh_token

    def refresh(self):
        '''
        Refreshes the access token. This method will automatically set http_api headers

        Parameters:
            None

        Returns:
            str
                The new access token. None if doesn't receive a valid response, please check the logs for more information. None if it cannot find the access token.

        Example:
            >>> access_token = http_api_wrapper.refresh()

        Raises:
            Exception: If the refresh fails, this function will raise an exception containing the response.json()['msg'] error.
        '''
        response_dict = self.checked_post(url=self.http_server_uri + "/auth/refresh", the_request={"username": self.username, "refresh_token": self.refresh_token}, requests_kwargs=None, good_msg=None, bad_msg="Error during refresh", raise_errors=True)
        self.access_token = response_dict.get('data').get('AuthenticationResult').get('AccessToken')
        logger.info(f"Refreshed access token: {self.access_token}")
        return self.access_token

    ######################## User #########################

    def fetch_user_profile(self, user_id):
        '''
        Fetch the user profile of a user. 

        Parameters:
            user_id: str
                The user ID.

        Returns:
            Character
                The user profile. None if doen't receive a valid response or cannot find the character in the response, please check the logs for more information.

        Example:
            >>> character = http_api_wrapper.fetch_user_profile(user_id)

        Raises:
            Exception: If the user profile fetch fails, this function will raise an exception about the error.
        '''
        response_dict = self.checked_post(url=self.http_server_uri + "/user/fetch_profile", the_request={"userlist": [user_id]}, requests_kwargs={'headers':self.headers}, good_msg=None, bad_msg="Error fetching user profile", raise_errors=True)
        data=response_dict['data'][user_id]
        data['user_id'] = user_id
        character = from_dict(data_class=Character, data=data)
        return character

    def fetch_real_characters(self, channel_id, service_id, raise_empty_list_err=True):
        '''
        Fetch the real characters of a channel. More of a service than an Agent function.

        Parameters:
            channel_id: str
                The channel ID.
            service_id: str
                The service ID.

        Returns:
            list
                A list of user_ids. Empty list if doesn't receive a valid response, please check the logs for more information.

        Example:
            >>> real_character_ids = http_api_wrapper.fetch_real_characters(channel_id, service_id)

        Raises:
            Empty list error if raise_empty_list_err is True and the list is empty.
        '''

        params = {"channel_id": channel_id, "service_id": service_id}
        rkwargs = {'params':params, 'headers':self.headers}

        response_dict = self.checked_get(url=self.http_server_uri + "/channel/userlist", the_request=None, requests_kwargs=rkwargs, good_msg="Successfully fetched channel userlist!", bad_msg="Error fetching channel userlist", raise_errors=True)

        userlist = response_dict["data"]["userlist"]
        channel_userlist = [u['user_id'] if type(u) is dict else u for u in userlist] # Convert to user_id if and only if given a user dict.

        if channel_userlist or not raise_empty_list_err:
            return channel_userlist
        else:
            raise Exception(f"Empty user_list error, channel_id: {channel_id}, service_id: {service_id}.")

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
        params = {"user_id": user_id,
                  "channel_id": channel_id,
                  "group_id": group_id}
        rkwargs = {'params':params, 'headers':self.headers}
        response_dict = self.checked_get(url=self.http_server_uri + "/user/group", the_request=None, requests_kwargs=rkwargs, good_msg="Successfully fetched user profile!", bad_msg="Error fetching user profile", raise_errors=True)

        character = from_dict(data_class=Character, data=response_dict['data'])
        return character

    def fetch_service_user_list(self, service_id):
        '''
        Get the user list of a service.

        Parameters:
            service_id: str
                The service ID.

        Returns:
            list
                A list of Character objects. None if doesn't receive a valid response, please check the logs for more information.

        Example:
            >>> user_list = http_api_wrapper.fetch_service_user_list(service_id)

        Raises:
            Exception: If the service user list fetch fails, this function will raise an exception about the error.
        '''
        response_dict = self.checked_get(url=self.http_server_uri + f"/service/user/list?service_id={service_id}", the_request=None, requests_kwargs={'headers':self.headers}, good_msg="Successfully got service user", bad_msg="Error creating service user", raise_errors=True)
        userlist = response_dict["data"]
        return [from_dict(data_class=Character, data=d) for d in userlist]

    def fetch_user_info(self):
        '''Used by the agent to get the agent info.'''
        response_dict = self.checked_get(url=self.http_server_uri + f"/user/info", the_request=None, requests_kwargs={'headers':self.headers}, good_msg="Successfully got user info", bad_msg="Error getting user info", raise_errors=True)
        return response_dict.get('data')

    ############################# Service ############################

    def create_service(self, description):
        '''
        Create a service with the given description.

        Parameters:
            description: str
                The description of the service.

        Returns:
            str
                The service ID. None if doesn't receive a valid response or cannot find the service id, please check the logs for more information.

        Example:
            >>> service_id = http_api_wrapper.create_service(description)

        Raises:
            Exception: If the service creation fails, this function will raise an exception about the error.
        '''
        response_dict = self.checked_post(url=self.http_server_uri + "/service/create", the_request={"description": description}, requests_kwargs={'headers':self.headers}, good_msg="Successfully created service!", bad_msg="Error creating service", raise_errors=True)
        return response_dict.get('data').get('service_id')

    def fetch_service_list(self):
        '''
        Get the service list of the user.

        Parameters:
            None

        Returns:
            list
                A list of service IDs of the user. None if doesn't receive a valid response or one without any 'data', please check the logs for more information.

        Example:
            >>> service_list = http_api_wrapper.fetch_service_list()

        Raises:
            Exception: If the service list fetch fails, this function will raise an exception about the error.
        '''
        response_dict = self.checked_get(url=self.http_server_uri + "/service/list", the_request=None, requests_kwargs={'headers':self.headers}, good_msg=None, bad_msg='Error getting service list', raise_errors=True)
        return response_dict.get('data')

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
        jsonr = {"service_id": service_id,
                 "username": username,
                 "context": {
                   "nickname": nickname,
                   "avatar": avatar,
                   "description": description}}
        response_dict = self.checked_post(url=self.http_server_uri + "/service/user/create", the_request=jsonr, requests_kwargs={'headers':self.headers}, good_msg="Successfully created service user", bad_msg="Error creating service user", raise_errors=True)
        character = from_dict(data_class=Character, data=response_dict['data'])
        return character

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
        jsonr = {"group_id": group_id, "members": user_uuids}
        response_dict = self.checked_post(url=self.http_server_uri + "/service/group/create", the_request=jsonr, requests_kwargs={'headers':self.headers}, good_msg="Successfully created service group!", bad_msg="Error creating service group", raise_errors=True)
        group = from_dict(data_class=Group, data=response_dict['data'])
        return group

    ############################# Channel ############################

    def create_channel(self, channel_name, channel_desc):
        '''
        Creates a channel.

        Parameters:
          channel_name: The name will appear on the list on the lefthandside in the browser.
          channel_desc: Appears in the description text of popular bands.

        Returns:
          channel_id: An ID such as 13e44ea3-b559-45af-9106-6aa92501d4ed.

        Raises:
          Exception: If the service group creation fails, this function will raise an exception about the error.
        '''
        jsonr = {"channel_name": channel_name, 'context':{'channel_description':channel_desc}}
        response_dict = self.checked_post(url=self.http_server_uri + "/channel/create", the_request=jsonr, requests_kwargs={'headers':self.headers}, good_msg=f"Successfully created channel {channel_name}.", bad_msg=f"Error creating channel {channel_name}", raise_errors=True)
        return response_dict['data']['channel_id']

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
                (does not raise an Exception if it fails)

        Example:
            >>> success = http_api_wrapper.bind_service_to_channel(service_id, channel_id)
        '''
        jsonr = {"channel_id": channel_id, "service_id": service_id}
        response_dict = self.checked_post(url=self.http_server_uri + "/service/bind", the_request=jsonr, requests_kwargs={'headers':self.headers}, good_msg=f"Successfully binded service {service_id} to channel {channel_id}.", bad_msg=f"Error binding service {service_id} to channel {channel_id}", raise_errors=False)

        logger.debug(f"bind_service_to_channel response {response_dict}")
        if response_dict['code'] == 10000: # This means no error.
            return True
        else:
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
        jsonr = {"channel_id": channel_id,"service_id": service_id}
        self.checked_post(url=self.http_server_uri + "/service/unbind", the_request=jsonr, requests_kwargs={'headers':self.headers}, good_msg=f"Successfully unbinded service {service_id} from channel {channel_id}", bad_msg=f"Error unbinding service {service_id} from channel {channel_id}", raise_errors=True)

    ############################# File ############################

    def upload_with_extension(self, extension):
        '''
        Get the upload URL and upload fields for uploading a file with the given extension.

        Parameters:
            extension: str
                The extension of the file.

        Returns:
            tuple
                The upload URL and upload fields. None, None if doesn't receive a valid response or cannot find the url and fields, please check the logs for more information.

        Example:
            >>> upload_url, upload_fields = http_api_wrapper.upload_with_extension(extension)

        Raises:
            Exception: If the upload URL fetch fails, this function will raise an exception about the error.
        '''
        requests_kwargs = {'params':{"extension": extension}, 'headers':self.headers}
        response_dict = self.checked_get(url=self.http_server_uri + "/file/upload", the_request=None, requests_kwargs=requests_kwargs, good_msg="Successfully fetched upload url!", bad_msg="Error fetching upload url", raise_errors=True)

        upload_url = response_dict.get('data').get('url')
        upload_fields = response_dict.get('data').get('fields')
        return upload_url, upload_fields

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
            logger.opt(colors=True).info(f"<fg 160,0,240>{('file upload: '+upload_url+' '+str(files)).replace('<', '&lt;').replace('>', '&gt;')}</>")
            response = requests.post(upload_url, data=upload_fields, files=files) # Using checked_post here is not helpful
            full_url = upload_url + upload_fields.get("key")
            if response.status_code == 204:
                return full_url
            else:
                err_msg = f"Error uploading file: {response.json().get('msg')}, upload_url: {upload_url}, upload_fields: {upload_fields}, file_path: {file_path}"
                logger.error(err_msg); raise Exception(err_msg)

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

    def __str__(self):
        access = self.access_token
        if len(access)>16:
            access = access[0:8]+'...'+access[-8:]
        refresh = self.refresh_token
        if len(refresh)>16:
            refresh = refresh[0:8]+'...'+refresh[-8:]
        return f'moobius.HTTPAPIWrapper(http_server_uri={self.http_server_uri}, username={self.username}, password=***, access_token={access}, refresh_token={refresh})'
    def __repr__(self):
        return self.__str__()
