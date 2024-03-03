# http_api_wrapper.py
import json
from loguru import logger
from dacite import from_dict
from moobius import utils
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
                        if len(response_txt)<384:
                            raise Exception(f'JSON cannot decode: {response_txt}')
                        elif '<div' in response_txt or 'div>' in response_txt: # HTML when it should be JSON.
                            summary_txt = utils.summarize_html(response_txt)
                            raise Exception(f'JSON cannot decode long HTML stuff, here is a summary: {summary_txt}')
                        else:
                            raise Exception(f'JSON cannot decode long string: {response_txt[0:384]}...')
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
      Channel: Dealing with threads/channels/chat-rooms etc.
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
        URL2example[url] = response_dict # Debug.
        return response_dict

    async def checked_get(self, url, the_request, requests_kwargs=None, good_msg=None, bad_msg="This HTTPs GET request failed", raise_errors=True):
        """Calls self._checked_get_or_post with is_post=False"""
        url = url.replace('//','/').replace(':/','://') # May not be needed, but looks better in the printouts.
        return await self._checked_get_or_post(url, the_request, False, requests_kwargs=requests_kwargs, good_msg=good_msg, bad_msg=bad_msg, raise_errors=raise_errors)
    async def checked_post(self, url, the_request, requests_kwargs=None, good_msg=None, bad_msg="This HTTPs POST request failed", raise_errors=True):
        """Calls self._checked_get_or_post with is_post=True"""
        url = url.replace('//','/').replace(':/','://') # May not be needed, but looks better in the printouts.
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

    def _xtract_character(self, resp_data):
        c_data = {}
        c_data['character_id'] = resp_data['character_id']
        c_data['name'] = resp_data['character_context']['name']
        c_data['character_context'] = resp_data['character_context']
        return from_dict(data_class=Character, data=c_data)

    async def fetch_character_profile(self, character_id):
        """Returns a Character object (or list) given a string-valued (or list-valued) character_id."""
        is_list = True
        if type(character_id) is str:
            is_list = False
            character_id = [character_id]
        response_dict = await self.checked_post(url=self.http_server_uri + "/character/fetch_profile", the_request={"character_list": character_id}, requests_kwargs={'headers':self.headers}, good_msg=None, bad_msg="Error fetching user profile", raise_errors=True)
        characters = [self._xtract_character(d) for d in response_dict['data']]
        return characters if is_list else characters[0]

    async def fetch_real_character_ids(self, channel_id, service_id, raise_empty_list_err=True):
        """
        Fetches the real user ids of a channel. A service function, will not work as an Agent function.

        Parameters:
          channel_id (str): The channel ID.
          service_id (str): The service/client/agent ID.
          raise_empty_list_err=True: Raises an Exception if the list is empty.

        Returns:
         A list of character_id strings.

        Raises:
          Exception (empty list) if raise_empty_list_err is True and the list is empty.
        """
        params = {"channel_id": channel_id, "service_id": service_id}
        rkwargs = {'params':params, 'headers':self.headers}

        use_groups = False
        if use_groups:
            response_dict = await self.checked_get(url=self.http_server_uri + "/user/group/list", the_request=None, requests_kwargs=rkwargs, good_msg="Successfully fetched channel character list", bad_msg="Error fetching channel character list", raise_errors=True)
            character_list = []
            logger.info(f'Who is on this channel? {channel_id}:\n{response_dict}')
            for x in response_dict['data']:
                if 'characters' in x:
                    character_list.extend(x['characters'])
                elif 'character_ids' in x: # I don't think this key is used.
                    character_list.extend(x['character_ids'])
                else:
                    raise Exception('The /user/group/list fetch did not return the characters as well, so maybe it should be extract-from-group time?')
        else:
            response_dict = await self.checked_get(url=self.http_server_uri + "/channel/character_list", the_request=None, requests_kwargs=rkwargs, good_msg="Successfully fetched channel character list", bad_msg="Error fetching channel character list", raise_errors=True)
            character_list = response_dict['data']['character_list']

        if type(character_list) is not list:
            raise Exception('Got a character list which actually was not a list.')
        if character_list or not raise_empty_list_err:
            return character_list
        else:
            raise Exception(f"Empty character_list error, channel_id: {channel_id}, service_id: {service_id}.")

    async def fetch_service_characters(self, service_id):
        """Get the user list (a list of Character objects), of a service given the string-valued service_id."""
        m0 = "Successfully fetched character list"
        mr = "Error fetching character list"
        worked = False
        if not worked:
            try:
                response_dict = await self.checked_get(url=self.http_server_uri + f"/service/character/list?service_id={service_id}", the_request=None, requests_kwargs={'headers':self.headers}, good_msg=m0, bad_msg=mr, raise_errors=True)
                worked = True
            except Exception as e:
                logger.warning(f'Version 0 fetch_characters failed: {e}')
        if not worked:
            try:
                params = {"service_id": service_id}
                rkwargs = {'params':params, 'headers':self.headers}
                response_dict = await self.checked_get(url=self.http_server_uri + f"/service/character/list", the_request=None, requests_kwargs=rkwargs, good_msg=m0, bad_msg=mr, raise_errors=True)
                worked = True
            except Exception as e:
                logger.warning(f'Version 1 fetch_characters failed: {e}')
        if not worked:
            try:
                response_dict = await self.checked_get(url=self.http_server_uri + f"/service/character/list", the_request={"service_id": service_id}, requests_kwargs={'headers':self.headers}, good_msg=m0, bad_msg=mr, raise_errors=True)
                worked = True
            except Exception as e:
                logger.error(f'All three versions failed: {e}')
                raise e
        charlist = response_dict["data"]
        return [self._xtract_character(d) for d in charlist]

    async def fetch_user_info(self):
        """Used by the agent to get the agent info as a dict."""
        response_dict = await self.checked_get(url=self.http_server_uri + f"/user/info", the_request=None, requests_kwargs={'headers':self.headers}, good_msg="Successfully fetched user info", bad_msg="Error getting user info", raise_errors=True)
        return response_dict.get('data')

    async def update_current_user(self, avatar, description, name):
        """Updates the user info. Will only be an Agent function in the .net version.

           Parameters:
             avatar: Link to image.
             description: Of the user.
             name: The name that shows in chat.

           No return value.
        """
        the_request={"avatar": avatar, 'description':description, 'name':name}
        response_dict = await self.checked_post(url=self.http_server_uri + f"/user/info", the_request=the_request, requests_kwargs={'headers':self.headers}, good_msg="Successfully updated user info", bad_msg="Error updating user info", raise_errors=True)
        return response_dict.get('data')

    ############################# Service ############################

    async def create_service(self, description):
        """Creates a service with the given description string and returns the string-valued service_id."""
        response_dict = await self.checked_post(url=self.http_server_uri + "/service/create", the_request={"description": description}, requests_kwargs={'headers':self.headers}, good_msg="Successfully created service!", bad_msg="Error creating service", raise_errors=True)
        return response_dict.get('data').get('service_id')

    async def fetch_service_id_list(self):
        """Returns a list of service ID strings of the user, or None if doesn't receive a valid response or one without any 'data' (error condition)."""
        response_dict = await self.checked_get(url=self.http_server_uri + "/service/list", the_request=None, requests_kwargs={'headers':self.headers}, good_msg=None, bad_msg='Error getting service list', raise_errors=True)
        return response_dict.get('data')

    async def create_character(self, service_id, name, avatar, description):
        """
        Creates a character with given name, avatar, and description.
        The created user will be bound to the given service.

        Parameters:
          service_id (str): The service_id/client_id.
          name (str): The name of the user.
          avatar (str): The image URL of the user's picture/
          description (str): The description of the user.

        Returns: A Character object representing the created user, None if doesn't receive a valid response (error condition). TODO: Should these error conditions jsut raise Exceptions instead?
        """
        jsonr = {"service_id": service_id,
                 "context": {
                   "name": name,
                   "avatar": avatar,
                   "description": description}}
        response_dict = await self.checked_post(url=self.http_server_uri + "/service/character/create", the_request=jsonr, requests_kwargs={'headers':self.headers}, good_msg="Successfully created character", bad_msg="Error creating character", raise_errors=True)
        character = self._xtract_character(response_dict['data'])
        return character

    async def update_character(self, service_id, character_id, avatar, description, name):
        """Updates the user info for a FAKE user, for real users use update_current_user.

           Parameters:
             service_id (str): Which service holds the user.
             character_id (str): Of the user.
             avatar (str): Link to user's image.
             description (str): Description of user.
             name (str): The name that shows in chat.

           Returns:
            Data about the user as a dict.
        """
        the_request = {"service_id": service_id, 'character_id':character_id, 'context': {'avatar':avatar, 'description':description, 'name':name}}
        response_dict = await self.checked_post(url=self.http_server_uri + f"/service/character/update", the_request=the_request, requests_kwargs={'headers':self.headers}, good_msg="Successfully updated character info", bad_msg="Error updating character info", raise_errors=True)
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

    async def fetch_message_history(self, channel_id, limit=64, before="null"):
        """
        Returns the message chat history.

        Parameters:
          channel_id (str): Channel with the messages inside of it.
          limit=64: Max number of messages to return (messages further back in time, if any, will not be returned).
          before="null": Only return messages older than this.

        Returns a list of dicts, each dict has this structure:
          "FromUserID", "MessageContent" (example {"text": "..."}), "MessageContext" (example {"is_dcs": true})
          "MessageID", "MessageType", "Status", "Timestamp"
        """
        if type(limit) is not str:
            limit = str(limit)
        params = {'channel_id':channel_id, 'limit':limit, 'before':before}
        rkwargs = {'params':params, 'headers':self.headers}
        jsonr = {"limit": limit} # Not where to put the limit, so it is put in both places.

        the_response = await self.checked_get(url=self.http_server_uri + "/channel/history_message", the_request=jsonr, requests_kwargs=rkwargs, good_msg=f"Successfully fetched message history for channel {channel_id}", bad_msg=f"Error fetching message history for channel {channel_id}", raise_errors=False)
        if 'blob' in the_response: # HTML style.
            return the_response['blob']
        return the_response

    async def this_user_channels(self):
        """What channels this user is joined to?"""
        the_response = await self.checked_get(url=self.http_server_uri + "/channel/list", the_request=None, requests_kwargs={'headers':self.headers}, good_msg=f"Successfully listed channels current user is in.", bad_msg=f"Error listing channels current user is in.", raise_errors=False)
        return [x['channel_id'] for x in the_response['data']]

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

    async def fetch_channel_group_dict(self, channel_id, service_id):
        """Like fetch_real_character_ids but returns a dict from group_id to all characters."""
        params = {"channel_id": channel_id, "service_id": service_id}
        rkwargs = {'params':params, 'headers':self.headers}

        response_dict = await self.checked_get(url=self.http_server_uri + "/user/group/list", the_request=None, requests_kwargs=rkwargs, good_msg="Successfully fetched channel group dict", bad_msg="Error fetching channel group dict", raise_errors=True)
        id2members = {}
        for x in response_dict['data']:
            if type(x['characters']) is not list:
                raise Exception('The characters field of data for /user/group/list should be a list.')
            id2members[x['group_id']] = x['characters']
        return id2members

    async def fetch_channel_group_list(self, channel_id, service_id):
        """Like fetch_channel_group_dict but returns the raw data."""
        params = {"channel_id": channel_id, "service_id": service_id}
        rkwargs = {'params':params, 'headers':self.headers}

        response_dict = await self.checked_get(url=self.http_server_uri + "/user/group/list", the_request=None, requests_kwargs=rkwargs, good_msg="Successfully fetched channel group list", bad_msg="Error fetching channel group list", raise_errors=True)
        return response_dict['data']

    async def create_channel_group(self, channel_id, group_name, characters):
        """
        Creates a channel group.

        Parameters:
          channel_id (str): The id of the group leader?
          group_name (str): What to call it.
          characters (list): A list of channel_id strings that will be inside the group.

        Returns:
          The group id string.
        """
        jsonr = {"channel_id": channel_id, "group_name":group_name, "characters": characters}
        response_dict = await self.checked_post(url=self.http_server_uri + "/user/group/create", the_request=jsonr, requests_kwargs={'headers':self.headers}, good_msg="Successfully created channel group {group_name}!", bad_msg="Error creating channel group {group_name}", raise_errors=True)
        return from_dict(data_class=Group, data={'group_id': response_dict['data']['group_id'], 'character_ids':characters})

    async def character_ids_of_service_group(self, group_id):
        """Gets a list of character ids belonging to a service group."""

        use_questionmark = True
        if use_questionmark:
            response_dict = await self.checked_get(url=self.http_server_uri + f"/service/group?group_id={group_id}", the_request=None, requests_kwargs={'headers':self.headers}, good_msg="Successfully fetched service group roster!", bad_msg="Error fetching service group roster", raise_errors=True)
        else:
            the_json = {'group_id':group_id}
            response_dict = await self.checked_get(url=self.http_server_uri + f"/service/group", the_request=the_json, requests_kwargs={'headers':self.headers}, good_msg="Successfully fetched service group roster!", bad_msg="Error fetching service group roster", raise_errors=True)
        if len(response_dict['data']) == 0:
            logger.warning(f'This group, if service group, seems to have no character ids in it: {group_id}')
            return []
        logger.info(f'Character id, service group HTTP response: {response_dict}')
        return response_dict['data']['characters']

    async def character_ids_of_channel_group(self, sender_id, channel_id, group_id):
        """
        Gets a list of character ids belonging to a channel group that is returned by a message.

        Parameters:
          sender_id: The message's sender.
          channel_id: The message specified that it was sent in this channel.
          group_id: The messages recipients.
        """

        use_questionmark = True
        if use_questionmark:
            response_dict = await self.checked_get(url=self.http_server_uri + f"/user/group?group_id={group_id}&channel_id={channel_id}&user_id={sender_id}", the_request=None, requests_kwargs={'headers':self.headers}, good_msg="Successfully fetched channel group roster!", bad_msg="Error fetching channel group roster", raise_errors=True)
        else:
            the_json = {'user_id':sender_id, 'group_id':group_id, 'channel_id':channel_id}
            response_dict = await self.checked_get(url=self.http_server_uri + f"/user/group", the_request=the_json, requests_kwargs={'headers':self.headers}, good_msg="Successfully fetched channel group roster!", bad_msg="Error fetching channel group roster", raise_errors=True)
        logger.info(f'List character IDs of channel group HTTP response: {response_dict}')
        if len(response_dict['data']) == 0:
            logger.warning(f'This group, if channel group, seems to have no character ids in it: {group_id}')
            return []
        return response_dict['data']['characters']

    async def create_service_group(self, characters):
        """
        Create a group containing characters id list, returning a Group object.
        Sending messages down for the new .net API requires giving myGroup.group_id instead of a list of character_ids.

        Parameters:
          group_name (str): What to call it.
          characters (list): A list of character_id strings that will be inside the group.

        Returns:
          A Group object."""
        if type(characters) is not list:
            raise Exception('Create service group expects a list of strings.')
        jsonr = {"group_id": "", "characters": characters}
        response_dict = await self.checked_post(url=self.http_server_uri + "/service/group/create", the_request=jsonr, requests_kwargs={'headers':self.headers}, good_msg="Successfully created service group!", bad_msg="Error creating service group", raise_errors=True)
        group_id = response_dict['data']
        if type(group_id) is not str:
            raise Exception('The group id returned was not a string.')
        group = from_dict(data_class=Group, data={'group_id': group_id, 'character_ids':characters})
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

    async def fetch_channel_temp_group(self, channel_id, service_id):
        """Like fetch_channel_group_list but for Temp groups."""
        params = {"channel_id": channel_id, "service_id": service_id}
        rkwargs = {'params':params, 'headers':self.headers}

        response_dict = await self.checked_get(url=self.http_server_uri + "/user/group/temp", the_request=None, requests_kwargs=rkwargs, good_msg="Successfully fetched channel temp group list", bad_msg="Error fetching channel temp group list", raise_errors=True)
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
