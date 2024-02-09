# http_api_wrapper.py
import json
from loguru import logger
from dacite import from_dict
from moobius.types import Character, Group
# TODO: refresh
# TODO: return code

use_async_http = True
URL2example = {} # Shows the most recent value of each GET and POST returned dict.
if use_async_http:
    import aiohttp
else:
    import requests


async def get_or_post(url, is_post, requests_kwargs=None, raise_json_decode_errors=True):
    """Get or post, will use requests.get/post or aiohttp.session.get/post depending on which one has been choosen.

    Parameters:
      url (str): https://...
      is_post (bool): False for GET, True for POST.
      requests_kwargs=None: These are fed into the requests/session get/post function.
      raise_json_decode_errors=True

    Returns: A dict which is json.loads() of the return.
      dict['code'] has the code, 10000 is good and 204 indicates no return but without error which is also fine.
      dict['blob'] is the response text in cases where the JSON fail and raise_json is False.

    Raises:
      Exception if Json fails and raise_json is True. Not all non-error returns are JSON thus the "blob" option."""
    if use_async_http:
        async with aiohttp.ClientSession() as session:
            async with (session.post if is_post else session.get)(url, **requests_kwargs) as resp:
                try:
                    response_dict = await resp.json()
                except aiohttp.client_exceptions.ContentTypeError:
                    response_txt = await resp.text()
                    if raise_json_decode_errors:
                        raise Exception(f'JSON cannot decode: {response_txt}')
                    else:
                        status_code = resp.status
                        if status_code is None:
                            raise Exception('Status code should be an int (after awaiting) but is None.')
                        return {'blob': str(response_txt), 'code':status_code}
    else:
        response_object = (requests.post if is_post else requests.get)(url, **requests_kwargs)
        if str(response_object).strip() == '<Response [204]>':
            return {'code':204} # Not an error condition, just a message indicating an empty response.
        try:
            response_dict = response_object.json()
        except Exception as e:
            if raise_json_decode_errors:
                raise Exception(f'Cannot JSON this string: {repr(response_object)}\nError message: {e}')
            else:
                return {'blob': str(response_object.text()), 'code':response_object.status_code}
    return response_dict


class BadResponseException(Exception):
    """For when the network is not doing what it should."""
    pass


class HTTPAPIWrapper:
    """
    Helper class for interacting with the Moobius HTTP API.
    All methods except for authenticate() and refresh() require authentication headers. 
    When calling these methods, make sure to call authenticate() first and add headers=self.headers to the method call.

    This Wrapper's methods are categorized as follows:
      Auth: Authentication and sign in/out.
      User: Dealing with real users.
      Service: Apps use this API to be a service.
      Channel: Dealing with bands/channels/chat-rooms etc.
      File: Upload files (automatically fetches the URL needed).
      Group: Combine users, services, or channels into groups which can be addressed by a single group_id.
    """
    def __init__(self, http_server_uri="", email="", password=""):
        """
        Initialize the HTTP API wrapper.

        Parameters:
          http_server_uri (str): The URI of the Moobius HTTP server.
          email (str): The email of the user.
          password (str): The password of the user.

        No return value.

        Example:
          >>> http_api_wrapper = HTTPAPIWrapper("http://localhost:8080", "test@test", "test")
        """
        self.http_server_uri = http_server_uri
        self.username = email
        self.password = password
        self.access_token = ""
        self.refresh_token = ""

    async def _checked_get_or_post(self, url, the_request, is_post, requests_kwargs=None, good_msg=None, bad_msg="This HTTPs request failed", raise_errors=True):
        """Runs a GET or POST request returning the result as a JSON with optional logging and error raising.

           Parameters:
             url (str): The https://... url.
             the_request (dict): The "json" kwarg is set to this. Can be None in which no "json" will be set.
             is_post: True for post, False for get.
             requests_kwargs=None: Dict of extra arguments to send to requests/aiohttp. None is equivalent to {}
             good_msg=None: The string-valued message to logger.debug. None means do not log.
             bad_msg="...": The string-valued to prepend to logger.error if the response isnt code 10000.
             raise_errors=True: Raise a BadResponseException if the request returns an error.

           Returns:
             The https response as a dict, using requests/aiohttp.post(...).json() to parse it.

           Raises:
             BadResponseException if raise_errors=True and the response is an error response."""
        if the_request is not None and type(the_request) is not dict:
            raise Exception(f'the_request must be None or a dict, not a {type(the_request)} because; dicts are turned into json.')
        if requests_kwargs is None:
            requests_kwargs = {}
        if the_request is not None:
            requests_kwargs['json'] = the_request
        kwarg_str = [] # Debug.
        for k in sorted(list(requests_kwargs.keys())):
            v = str(requests_kwargs[k])
            if 'token' in k.lower():
                v = "<token>"
            if 'password' in k.lower() or 'authorization' in k.lower():
                v = "*******"
            if x:= requests_kwargs.get('headers',{}).get('Authorization',{}):
                v = v.replace(x, "<Auth token>")
            kwarg_str.append(k+'='+str(v))
        kwarg_str = ' '.join(kwarg_str)
        req_info_str = f"{'POST' if is_post else 'GET'} URL={url} {kwarg_str.replace('<', '&lt;').replace('>', '&gt;')}"
        logger.opt(colors=True).info(f"<fg 160,0,240>{req_info_str}</>")

        response_dict = await get_or_post(url, is_post, requests_kwargs=requests_kwargs, raise_json_decode_errors=raise_errors)
        if response_dict.get('code') in [204, 10000]:
            if good_msg is not None:
                logger.debug(good_msg)
        else:
            error_code = response_dict.get('code')
            err_msg = f"{bad_msg+': ' if bad_msg else ''}'code='{error_code} 'msg='{response_dict.get('msg')}"
            if bad_msg is not None:
                logger.error(err_msg)
            if raise_errors:
                raise BadResponseException(err_msg)
        show_first_example = False # Turn off if too wordy.
        if (url not in URL2example) and show_first_example:
            pretty_printed = json.dumps(response_dict, sort_keys=True, indent=2)
            logger.opt(colors=True).info(f"<fg 120,96,240>FIRST EXAMPLE OF: {req_info_str}\nRESULT:\n{pretty_printed.replace('<', '&lt;').replace('>', '&gt;')}</>") # Uncomment this line to see the callbacks of each GET and POST statement.
        URL2example[url] = response_dict # Debug feature.
        return response_dict

    async def checked_get(self, url, the_request, requests_kwargs=None, good_msg=None, bad_msg="This HTTPs GET request failed", raise_errors=True):
        """Calls self._checked_get_or_post with is_post=False"""
        return await self._checked_get_or_post(url, the_request, False, requests_kwargs=requests_kwargs, good_msg=good_msg, bad_msg=bad_msg, raise_errors=raise_errors)
    async def checked_post(self, url, the_request, requests_kwargs=None, good_msg=None, bad_msg="This HTTPs POST request failed", raise_errors=True):
        """Calls self._checked_get_or_post with is_post=True"""
        return await self._checked_get_or_post(url, the_request, True, requests_kwargs=requests_kwargs, good_msg=good_msg, bad_msg=bad_msg, raise_errors=raise_errors)

    ############################ Auth ############################

    @property
    def headers(self):
        """Returns the authentication headers. Used for all API calls except for authenticate() and refresh().
        headers["Auth-Origin"] is the authentication service, such as "cognito".
        headers["Authorization"] is the access token, etc that proves authentication."""
        return {
            "Auth-Origin": "cognito",
            "Authorization": f"Bearer {self.access_token}"
        }

    @logger.catch
    async def authenticate(self):
        """Authenticates the user. Needs to be called before any other API calls.
           Returns (the access token, the refresh token). Exception if doesn't receive a valid response.
           Like most GET and POST functions it will raise any errors thrown by the http API."""
        response_dict = await self.checked_post(url=self.http_server_uri + "/auth/sign_in", the_request={"username": self.username, "password": self.password}, requests_kwargs=None, good_msg=None, bad_msg="Error during authentication", raise_errors=True)
        self.access_token = response_dict.get('data').get('AuthenticationResult').get('AccessToken')
        self.refresh_token = response_dict.get('data').get('AuthenticationResult').get('RefreshToken')
        logger.info(f"Authenticated. Access token: {self.access_token}")
        return self.access_token, self.refresh_token

    async def sign_up(self):
        """Signs up. Returns (the access token, the refresh token).
        Exception if doesn't receive a valid response."""
        response_dict = await self.checked_post(url=self.http_server_uri + "/auth/sign_up", the_request={"username": self.username, "password": self.password}, requests_kwargs=None, good_msg=None, bad_msg="Error during signup", raise_errors=True)
        self.access_token = response_dict.get('data').get('AuthenticationResult').get('AccessToken')
        self.refresh_token = response_dict.get('data').get('AuthenticationResult').get('RefreshToken')
        logger.info(f"Signed up! Access token: {self.access_token}")
        return self.access_token, self.refresh_token

    async def sign_out(self):
        """Signs out using the access token obtained from signing in. Returns None."""
        await self.checked_post(url=self.http_server_uri + "/auth/sign_out", the_request={"access_token": self.access_token}, requests_kwargs={'headers':self.headers}, good_msg=None, bad_msg="Error during signout", raise_errors=True)
        logger.info(f"Signed out.")

    async def refresh(self):
        """Refreshes the access token, returning it."""
        response_dict = await self.checked_post(url=self.http_server_uri + "/auth/refresh", the_request={"username": self.username, "refresh_token": self.refresh_token}, requests_kwargs=None, good_msg=None, bad_msg="Error during refresh", raise_errors=True)
        self.access_token = response_dict.get('data').get('AuthenticationResult').get('AccessToken')
        logger.info(f"Refreshed access token: {self.access_token}")
        return self.access_token

    ######################## User #########################

    async def fetch_user_profile(self, user_id):
        """Returns a Character object that contains user profile of (string-valued) user_id."""
        response_dict = await self.checked_post(url=self.http_server_uri + "/user/fetch_profile", the_request={"userlist": [user_id]}, requests_kwargs={'headers':self.headers}, good_msg=None, bad_msg="Error fetching user profile", raise_errors=True)
        data=response_dict['data'][user_id]
        data['user_id'] = user_id
        character = from_dict(data_class=Character, data=data)
        return character

    async def fetch_real_characters(self, channel_id, service_id, raise_empty_list_err=True):
        """
        Fetches the real characters of a channel. More of a service than an Agent function.

        Parameters:
          channel_id (str): The channel ID.
          service_id (str): The service/client/agent ID.
          raise_empty_list_err=True: Raises an Exception if the list is empty.

        Returns:
         A list of user_ids strings.

        Raises:
          Exception (empty list) if raise_empty_list_err is True and the list is empty.
        """
        params = {"channel_id": channel_id, "service_id": service_id}
        rkwargs = {'params':params, 'headers':self.headers}

        response_dict = await self.checked_get(url=self.http_server_uri + "/channel/userlist", the_request=None, requests_kwargs=rkwargs, good_msg="Successfully fetched channel userlist!", bad_msg="Error fetching channel userlist", raise_errors=True)

        userlist = response_dict["data"]["userlist"]
        channel_userlist = [u['user_id'] if type(u) is dict else u for u in userlist] # Convert to user_id if and only if given a user dict.

        if channel_userlist or not raise_empty_list_err:
            return channel_userlist
        else:
            raise Exception(f"Empty user_list error, channel_id: {channel_id}, service_id: {service_id}.")

    async def fetch_service_user_list(self, service_id):
        """Get the user list (a list of Character objects), of a service given the string-valued service_id."""
        response_dict = await self.checked_get(url=self.http_server_uri + f"/service/user/list?service_id={service_id}", the_request=None, requests_kwargs={'headers':self.headers}, good_msg="Successfully got service user", bad_msg="Error creating service user", raise_errors=True)
        userlist = response_dict["data"]
        return [from_dict(data_class=Character, data=d) for d in userlist]

    async def fetch_user_info(self):
        """Used by the agent to get the agent info as a dict."""
        response_dict = await self.checked_get(url=self.http_server_uri + f"/user/info", the_request=None, requests_kwargs={'headers':self.headers}, good_msg="Successfully got user info", bad_msg="Error getting user info", raise_errors=True)
        return response_dict.get('data')

    async def update_real_user(self, user_id, avatar, description, nickname):
        """Updates the user info.

           Parameters:
             avatar: Link to image.
             description: Of the user.
             nickname: The name that shows in chat, differen than username.

           No return value.
        """
        the_request={"avatar": avatar, 'description':description, 'nickname':nickname, 'user_id':user_id}
        response_dict = await self.checked_post(url=self.http_server_uri + f"/user/info", the_request=the_request, requests_kwargs={'headers':self.headers}, good_msg="Successfully updated user info", bad_msg="Error updating user info", raise_errors=True)
        return response_dict.get('data')

    ############################# Service ############################

    async def create_service(self, description):
        """Creates a service with the given description string and returns the string-valued service_id."""
        response_dict = await self.checked_post(url=self.http_server_uri + "/service/create", the_request={"description": description}, requests_kwargs={'headers':self.headers}, good_msg="Successfully created service!", bad_msg="Error creating service", raise_errors=True)
        return response_dict.get('data').get('service_id')

    async def fetch_service_list(self):
        """Returns a list of service ID strings of the user, or None if doesn't receive a valid response or one without any 'data' (error condition)."""
        response_dict = await self.checked_get(url=self.http_server_uri + "/service/list", the_request=None, requests_kwargs={'headers':self.headers}, good_msg=None, bad_msg='Error getting service list', raise_errors=True)
        return response_dict.get('data')

    async def create_service_user(self, service_id, username, nickname, avatar, description):
        """
        Creates a service user with given username, nickname, avatar, and description.
        The created user will be bound to the given service.

        Parameters:
          service_id (str): The service_id/client_id.
          username (str): The username of the user.
          nickname (str): The nickname of the user.
          avatar (str): The image URL of the user's picture/
          description (str): The description of the user.

        Returns: A Character object representing the created user, None if doesn't receive a valid response (error condition). TODO: Should these error conditions jsut raise Exceptions instead?
        """
        jsonr = {"service_id": service_id,
                 "username": username,
                 "context": {
                   "nickname": nickname,
                   "avatar": avatar,
                   "description": description}}
        response_dict = await self.checked_post(url=self.http_server_uri + "/service/user/create", the_request=jsonr, requests_kwargs={'headers':self.headers}, good_msg="Successfully created service user", bad_msg="Error creating service user", raise_errors=True)
        character = from_dict(data_class=Character, data=response_dict['data'])
        return character

    async def update_service_user(self, service_id, user_id, username, avatar, description, nickname):
        """Updates the user info for a FAKE user, for real users use update_real_user.

           Parameters:
             service_id (str): Which service holds the user.
             user_id (str): Of the user.
             username (str): User name, different than nickname.
             avatar (str): Link to user's image.
             description (str): Description of user.
             nickname (str): The name that shows in chat, differen than username.

           Returns:
            Data about the user as a dict.
        """
        the_request = {"service_id": service_id, 'user_id':user_id, 'username': username, 'context': {'avatar':avatar, 'description':description, 'nickname':nickname}}
        response_dict = await self.checked_post(url=self.http_server_uri + f"/service/user/update", the_request=the_request, requests_kwargs={'headers':self.headers}, good_msg="Successfully updated service user info", bad_msg="Error updating service user info", raise_errors=True)
        return response_dict.get('data')

    ############################# Channel ############################

    async def create_channel(self, channel_name, channel_desc):
        """Creates a channel given a string-valued channel name and description. Returns the channel_id.
        Example ID: "13e44ea3-b559-45af-9106-6aa92501d4ed"."""
        jsonr = {"channel_name": channel_name, 'context':{'channel_description':channel_desc}}
        response_dict = await self.checked_post(url=self.http_server_uri + "/channel/create", the_request=jsonr, requests_kwargs={'headers':self.headers}, good_msg=f"Successfully created channel {channel_name}.", bad_msg=f"Error creating channel {channel_name}", raise_errors=True)
        return response_dict['data']['channel_id']

    async def bind_service_to_channel(self, service_id, channel_id):
        """Binds a service to a channel given the service and channel IDs. Returns whether sucessful."""
        jsonr = {"channel_id": channel_id, "service_id": service_id}
        response_dict = await self.checked_post(url=self.http_server_uri + "/service/bind", the_request=jsonr, requests_kwargs={'headers':self.headers}, good_msg=f"Successfully binded service {service_id} to channel {channel_id}.", bad_msg=f"Error binding service {service_id} to channel {channel_id}", raise_errors=False)

        logger.debug(f"bind_service_to_channel response {response_dict}")
        if response_dict['code'] == 10000: # This means no error.
            return True
        else:
            return False

    async def unbind_service_from_channel(self, service_id, channel_id):
        """Unbinds a service to a channel given the service and channel IDs. Returns None."""
        jsonr = {"channel_id": channel_id,"service_id": service_id}
        await self.checked_post(url=self.http_server_uri + "/service/unbind", the_request=jsonr, requests_kwargs={'headers':self.headers}, good_msg=f"Successfully unbound service {service_id} from channel {channel_id}", bad_msg=f"Error unbinding service {service_id} from channel {channel_id}", raise_errors=True)

    async def update_channel(self, channel_id, channel_name, channel_desc):
        """
        Updates the name and desc of a channel.

        Parameters:
          channel_id (str): Which channel to update.
          channel_name (str): The new channel name.
          channel_desc (str): The new channel description.

        No return value.
        """
        jsonr = {"channel_id": channel_id, "channel_name": channel_name, "context":{"channel_description":channel_desc}}
        await self.checked_post(url=self.http_server_uri + "/channel/update", the_request=jsonr, requests_kwargs={'headers':self.headers}, good_msg=f"Successfully updated channel {channel_id}", bad_msg=f"Error updating channel {channel_id}", raise_errors=True)

    async def fetch_popular_chanels(self):
        """Fetches the popular channels, returning a list of channel_id strings."""
        response_dict = await self.checked_get(url=self.http_server_uri + "/channel/popular", the_request=None, requests_kwargs={'headers':self.headers}, good_msg=f"Successfully fetched popular channels", bad_msg=f"Error fetching popular channels", raise_errors=True)
        out = []
        for ch in response_dict['data']:
            if type(ch) is not str:
                ch = ch['channel_id']
            out.append(ch)
        return out

    async def fetch_channel_list(self):
        """Fetches all? channels, returning a list of channel_id strings."""
        response_dict = await self.checked_get(url=self.http_server_uri + "/channel/list", the_request=None, requests_kwargs={'headers':self.headers}, good_msg=f"Successfully fetched channels", bad_msg=f"Error fetching channels", raise_errors=True)
        out = []
        for ch in response_dict['data']:
            if type(ch) is not str:
                ch = ch['channel_id']
            out.append(ch)
        return out

    async def fetch_history_message(self, channel_id, limit=1024, before="null"):
        """
        Returns the message history. TODO: May not be working yet.

        Parameters:
          channel_id (str): Channel with the messages inside of it.
          limit=1024: Max number of messages to return (messages further back in time, if any, will not be returned).
          before="null": Only return messages older than this.

        Returns a list of dicts, each dict has this structure:
          "FromUserID", "MessageContent" (example {"text": "..."}), "MessageContext" (example {"is_dcs": true})
          "MessageID", "MessageType", "Status", "Timestamp"
        """
        if type(limit) is not str:
            limit = str(limit)
        jsonr = {'channel_id':channel_id, 'limit':limit, 'before':before}
        the_response = await self.checked_get(url=self.http_server_uri + "/channel/history_message", the_request=jsonr, requests_kwargs={'headers':self.headers}, good_msg=f"Successfully fetched messages for channel {channel_id}", bad_msg=f"Error fetching messages for channel {channel_id}", raise_errors=False)
        return the_response

    ############################# File ############################

    async def upload_extension(self, extension):
        """Get the upload URL and upload fields for uploading a file with the given string-valued extension.
        Returns (upload_url or None, upload_fields)."""
        requests_kwargs = {'params':{"extension": extension}, 'headers':self.headers}
        response_dict = await self.checked_get(url=self.http_server_uri + "/file/upload", the_request=None, requests_kwargs=requests_kwargs, good_msg="Successfully fetched upload url!", bad_msg="Error fetching upload url", raise_errors=True)

        upload_url = response_dict.get('data').get('url')
        upload_fields = response_dict.get('data').get('fields')
        return upload_url, upload_fields

    async def do_upload_file(self, upload_url, upload_fields, file_path):
        """
        Upload a file to the given upload URL with the given upload fields.

        Parameters:
          upload_url (str): obtained with upload_extension.
          upload_fields (dict): obtained with upload_extension.
          file_path (str): The path of the file.

        Returns:
          The full URL string of the uploaded file. None if doesn't receive a valid response (error condition).

        Raises:
          Exception: If the file upload fails, this function will raise an exception about the error.
        """
        with open(file_path, 'rb') as f:
            files = {'file': (file_path, f)}
            full_url = upload_url + upload_fields.get("key")
            logger.opt(colors=True).info(f"<fg 160,0,240>{('file upload: '+upload_url+' '+str(files)).replace('<', '&lt;').replace('>', '&gt;')}</>")

            #async with aiohttp.ClientSession() as session:
            #    async with session.post(upload_url, data=upload_fields, files=files) as resp: #TypeError: ClientSession._request() got an unexpected keyword argument 'files'
            #        response_dict = await resp.json()
            #return full_url
            old_way = True # The aiohttp cannot handle the kword "files" even though it handles other keywords just fine. This is a common bug in aiohttp.
            if old_way:
                import requests
                response = requests.post(upload_url, data=upload_fields, files=files)
                if response.status_code == 204:
                    return full_url
                else:
                    raise Exception(f'Upload file error: {upload_url}; {full_url}.')
            else:
                err_msg = f"Error uploading file upload_url: {upload_url}, upload_fields: {upload_fields}, file_path: {file_path}"
                response = await self._checked_get_or_post(upload_url, the_request=None, is_post=True, requests_kwargs={'data':upload_fields, 'files':files}, good_msg=None, bad_msg=err_msg, raise_errors=True)
                return full_url

    async def upload_file(self, file_path):
        """Upload the file at file_path to the Moobius server. Automatically gets the upload URL and upload fields.
        Returns the full upload URL. Raises Exception if the upload fails.
        """
        extension = file_path.split(".")[-1]
        upload_url, upload_fields = await self.upload_extension(extension)
        if upload_url and upload_fields:
            # Exception will be raised in do_upload_file(), no need to raise here
            full_url = await self.do_upload_file(upload_url, upload_fields, file_path)
            return full_url
        else:
            logger.error(f"Error getting upload url and upload fields! file_path: {file_path}")
            raise Exception(f"Error getting upload url and upload fields! file_path: {file_path}")

    ############################# Groups ############################

    async def create_channel_group(self, channel_id, group_name, members):
        """
        Creates a channel group.

        Parameters:
          channel_id (str): The id of the group leader?
          group_name (str): What to call it.
          members (list): A list of channel_id strings that will be inside the group.

        Returns:
          The group id string.
        """
        raise Exception('Group functions are not yet fully supported in the platform. Once supported remove this and all other group-not-supported exceptions in http_api_wrapper.py')
        jsonr = {"channel_id": channel_id, "group_name":group_name, "members": members}
        response_dict = await self.checked_post(url=self.http_server_uri + "/user/group/create", the_request=jsonr, requests_kwargs={'headers':self.headers}, good_msg="Successfully created channel group {group_name}!", bad_msg="Error creating channel group {group_name}", raise_errors=True)
        return response_dict['data']['channel_group_id']

    async def create_service_group(self, group_id, members):
        """
        Create a user group. The group will be created with the given group ID and user UUIDs.

        Parameters:
          group_name (str): What to call it.
          members (list): A list of channel_id strings that will be inside the group.

        Returns:
          A Group object."""
        raise Exception('Group functions are not yet fully supported in the platform. Once supported remove this and all other group-not-supported exceptions in http_api_wrapper.py')
        jsonr = {"group_id": group_id, "members": members}
        response_dict = await self.checked_post(url=self.http_server_uri + "/service/group/create", the_request=jsonr, requests_kwargs={'headers':self.headers}, good_msg="Successfully created service group!", bad_msg="Error creating service group", raise_errors=True)
        group = from_dict(data_class=Group, data=response_dict['data'])
        return group

    async def update_channel_group(self, channel_id, group_id, members):
        """
        Updates a channel group.

        Parameters:
          channel_id (str): The id of the group leader?
          group_name (str): What to call it.
          members (list): A list of channel_id strings that will be inside the group.

        No return value.
        """
        raise Exception('Group functions are not yet fully supported in the platform. Once supported remove this and all other group-not-supported exceptions in http_api_wrapper.py')
        jsonr = {"channel_id": channel_id, "group_id":group_id, "members": members}
        await self.checked_post(url=self.http_server_uri + "/user/group/update", the_request=jsonr, requests_kwargs={'headers':self.headers}, good_msg="Successfully updated channel group {group_name}!", bad_msg="Error updating channel group {group_name}", raise_errors=True)

    async def update_temp_channel_group(self, channel_id, members):
        """
        Updates a channel TEMP group.

        Parameters:
          channel_id (str): The id of the group leader?
          members (list): A list of channel_id strings that will be inside the group.

        No return value.
        """
        raise Exception('Group functions are not yet fully supported in the platform. Once supported remove this and all other group-not-supported exceptions in http_api_wrapper.py')
        jsonr = {"channel_id": channel_id, "members": members}
        await self.checked_post(url=self.http_server_uri + "/user/group/temp", the_request=jsonr, requests_kwargs={'headers':self.headers}, good_msg="Successfully updated channel group {group_name}!", bad_msg="Error updating channel group {group_name}", raise_errors=True)

    async def fetch_channel_group(self, channel_id):
        """Returns the group_id that the given channel_id string is in."""
        raise Exception('Group functions are not yet fully supported in the platform. Once supported remove this and all other group-not-supported exceptions in http_api_wrapper.py')
        jsonr = {'channel_id':channel_id}
        response_dict = await self.checked_get(url=self.http_server_uri + "/user/group/list", the_request=jsonr, requests_kwargs={'headers':self.headers}, good_msg=f"Successfully fetched group for channel {channel_id}", bad_msg=f"Error fetching group for channel {channel_id}", raise_errors=True)
        return response_dict['data']['group_id']

    async def fetch_channel_temp_group(self, channel_id):
        """Returns the TEMP group data that the given channel_id string is in."""
        raise Exception('Group functions are not yet fully supported in the platform. Once supported remove this and all other group-not-supported exceptions in http_api_wrapper.py')
        jsonr = {'channel_id':channel_id}
        response_dict = await self.checked_get(url=self.http_server_uri + "/user/group/temp", the_request=jsonr, requests_kwargs={'headers':self.headers}, good_msg=f"Successfully fetched group for channel {channel_id}", bad_msg=f"Error fetching group for channel {channel_id}", raise_errors=True)
        return response_dict['data']

    async def fetch_user_from_group(self, user_id, channel_id, group_id):
        """
        Fetch the user profile of a user from a group.

        Parameters:
            user_id (str): The user ID.
            channel_id (str): The channel ID. (TODO: of what?)
            group_id (str): The group ID.

        Returns:
            The user profile Character object.
        """
        raise Exception('Group functions are not yet fully supported in the platform. Once supported remove this and all other group-not-supported exceptions in http_api_wrapper.py')
        params = {"user_id": user_id,
                  "channel_id": channel_id,
                  "group_id": group_id}
        rkwargs = {'params':params, 'headers':self.headers}
        response_dict = await self.checked_get(url=self.http_server_uri + "/user/group", the_request=None, requests_kwargs=rkwargs, good_msg="Successfully fetched user profile!", bad_msg="Error fetching user profile", raise_errors=True)

        character = from_dict(data_class=Character, data=response_dict['data'])
        return character

    async def fetch_target_group(self, user_id, channel_id, group_id):
        """
        Fetches info about the group.

          Parameters:
            user_id (str), channel_id (str): why needed?
            group_id (str): Which group to fetch.

          Returns:
            The data-dict data.
        """
        raise Exception('Group functions are not yet fully supported in the platform. Once supported remove this and all other group-not-supported exceptions in http_api_wrapper.py')
        jsonr = {'user_id':user_id, 'channel_id':channel_id, 'group_id':group_id}
        response_dict = await self.checked_get(url=self.http_server_uri + "/user/group", the_request=jsonr, requests_kwargs={'headers':self.headers}, good_msg=f"Successfully fetched group for channel {channel_id}", bad_msg=f"Error fetching group for channel {channel_id}", raise_errors=True)
        return response_dict['data']

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
