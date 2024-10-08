# aiohttp-based wrapper for HTTPS interaction with the platform.
# Handles auth as well as GET and POST requests.
# This module is designed to be used by the Moobius service.
import json, os, io, hashlib, datetime, random, re
import aiohttp
from loguru import logger
from dacite import from_dict
from moobius import types
from moobius.types import Character, Group, UserInfo, MessageBody
# TODO: refresh
_URL2example_response = {} # Debug tool that allows inspecting example responses.


def summarize_html(html_str):
    """
    Creates a summary given an html_string.
    Converts HTML to an easier-for-a-human format by cutting out some of the more common tags. Far from perfect.
    Returns the summary as a string.
    """
    rs = [r'<div>\d+<\/div *>', r'<div class *= *"[a-zA-Z0-9]*">', r'<span class *= *"[a-zA-Z0-9]*">']
    for tag in ['div', 'li', 'head', 'body', 'pre', 'span']:
        rs.append(f'<{tag} *>')
        rs.append(f'</{tag} *>')
    for r in rs:
        html_str = re.sub(r, "", html_str)
    html_str = html_str.replace('\r\n','\n').replace('\t','  ')
    while '  ' in html_str or '\n\n' in html_str or '\n ' in html_str:
        html_str = html_str.replace('\n\n\n\n\n\n\n\n\n','\n').replace('\n\n','\n').replace('         ',' ').replace('  ',' ').replace('\n ','\n')
    return html_str.strip()


async def get_or_post(url, is_post, requests_kwargs=None, raise_json_decode_errors=True):
    """
    Sends a GET or POST request and awaits for the response.

    Parameters:
      url (str): https://...
      is_post (bool): False for GET, True for POST.
      requests_kwargs=None: These are fed into the requests/session get/post function.
      raise_json_decode_errors=True: Raise errors parsing the JSON that the request sends back, otherwise return the error as a dict.

    Returns: A dict which is the json.loads() of the return.
      Error condition if JSON decoding fails:
        dict['code'] contains the code
          10000 is "good" (but the JSON still failed).
          204 indicates no return but without error which is also fine.
          Many other codes exist.
        dict['blob'] is the response text in cases where the JSON fail and raise_json is False.

    Raises:
      An Exception if Json fails and raise_json is True. Not all non-error returns are JSON thus the "blob" option.
    """
    async with aiohttp.ClientSession() as session:
        async with (session.post if is_post else session.get)(url, **requests_kwargs) as resp:
            try:
                response_dict = await resp.json()
                return response_dict
            except aiohttp.client_exceptions.ContentTypeError:
                response_txt = await resp.text()
                if raise_json_decode_errors:
                    if not response_txt.strip():
                        raise Exception(f'Empty string.')
                    if len(response_txt)<384:
                        raise Exception(f'JSON cannot decode: {response_txt}')
                    elif '<div' in response_txt or 'div>' in response_txt: # HTML when it should be JSON.
                        summary_txt = summarize_html(response_txt)
                        raise Exception(f'JSON cannot decode long HTML stuff, here is a summary: {summary_txt}')
                    else:
                        raise Exception(f'JSON cannot decode long string: {response_txt[0:384]}...')
                else:
                    status_code = resp.status
                    if status_code is None:
                        raise Exception('Status code should be an int (after awaiting) but is None.')
                    return {'blob': str(response_txt), 'code':status_code}


class BadResponseException(Exception):
    """For when the network is not doing what it should."""
    pass


class HTTPAPIWrapper:
    """
    Helper class for interacting with the Moobius HTTP API.
    All methods except for authenticate() and refresh() require authentication headers. 
    When calling these methods, make sure to call authenticate() first and add headers=self.headers to the method call.

    This wrapper's methods are categorized as follows:
      Auth: Authentication and sign in/out.
      User: Dealing with real users.
      Service: Apps use this API to be a service.
      Channel: Dealing with threads/channels/chat-rooms etc.
      File: Upload files (automatically fetches the URL needed).
      Group: Combine users, services, or channels into groups which can be addressed by a single group_id.
    """
    def __init__(self, http_server_uri="", email="", password=""):
        """
        Initializes the HTTP API wrapper.

        Parameters:
          http_server_uri (str): The URI of the Moobius HTTP server.
          email (str): The email of the user.
          password (str): The password of the user.

        Example:
          >>> http_api_wrapper = HTTPAPIWrapper("http://localhost:8080", "test@test", "test")
        """
        self.http_server_uri = http_server_uri
        self.username = email
        self.password = password
        self.access_token = ""
        self.refresh_token = ""
        self.filehash2URL = {} # Avoid uploading the same file twice!

    async def _checked_get_or_post(self, url, the_request, is_post, requests_kwargs=None, good_message=None, bad_message="This HTTPs request failed", raise_errors=True):
        """
        Runs a GET or POST request returning the result as a JSON with optional logging and error raising.

           Parameters:
             url (str): The https://... url.
             the_request (dict): The "json" kwarg is set to this. Can be None in which no "json" will be set.
             is_post: True for post, False for get.
             requests_kwargs=None: Dict of extra arguments to send to requests/aiohttp. None is equivalent to {}
             good_message=None: The string-valued message to logger.debug. None means do not log.
             bad_message="...": The string-valued message to prepend to logger.error if the response isnt code 10000.
             raise_errors=True: Raise a BadResponseException if the request returns an error.

           Returns:
             The https response as a dict, using requests/aiohttp.post(...).json() to parse it.

           Raises:
             BadResponseException if raise_errors=True and the response is an error response.
        """
        if the_request is not None and type(the_request) is not dict:
            raise Exception(f'the_request must be None or a dict, not a {type(the_request)} because; dicts are turned into json.')
        if requests_kwargs is None:
            requests_kwargs = {}
        if the_request is not None:
            requests_kwargs['json'] = the_request
        kwarg_str = [] # Logging.
        for k in sorted(list(requests_kwargs.keys())):
            v = str(requests_kwargs[k])
            if 'token' in k.lower():
                v = "<token>"
            if 'password' in k.lower() or 'authorization' in k.lower():
                v = "*******"
            if x:= requests_kwargs.get('headers',{}).get('Authorization',{}):
                v = v.replace(x, "<Auth token>")
            if type(v) is bytes:
                v = f'<binary blob {len(v)} bytes>'
            sv = str(v)
            if len(sv)>256+16:
                sv = sv[0:256]+f'...<{len(sv)} chars total>'
            kwarg_str.append(k+'='+sv)
        kwarg_str = ' '.join(kwarg_str)
        req_info_str = f"{'POST' if is_post else 'GET'} URL={url} {kwarg_str.replace('<', '&lt;').replace('>', '&gt;')}"
        logger.opt(colors=True).info(f"<fg 160,0,240>{req_info_str}</>")

        response_dict = await get_or_post(url, is_post, requests_kwargs=requests_kwargs, raise_json_decode_errors=raise_errors)
        if response_dict.get('code') in [204, 10000]:
            if good_message is not None:
                logger.debug(good_message)
        else:
            error_code = response_dict.get('code')
            err_message = f"{bad_message+': ' if bad_message else ''}'code='{error_code} 'message='{response_dict.get('message')}"
            if bad_message is not None:
                logger.error(err_message)
            if raise_errors:
                raise BadResponseException(err_message)
        show_first_example = False # Turn off if too wordy.
        if (url not in _URL2example_response) and show_first_example:
            pretty_printed = json.dumps(response_dict, sort_keys=True, indent=2, ensure_ascii=False)
            logger.opt(colors=True).info(f"<fg 120,96,240>FIRST EXAMPLE OF: {req_info_str}\nRESULT:\n{pretty_printed.replace('<', '&lt;').replace('>', '&gt;')}</>") # Uncomment this line to see the callbacks of each GET and POST statement.
        _URL2example_response[url] = response_dict # Debug.
        return response_dict

    async def checked_get(self, url, the_request, requests_kwargs=None, good_message=None, bad_message="This HTTPs GET request failed", raise_errors=True):
        """
        Calls self._checked_get_or_post with is_post=False.
        Accepts the url, the request itself, the kwargs for the request, the message to print on a happy 200, the message to print on a sad non-200, and whether to raise errors if sad.
        Returns the response. Raises a BadResponseException if it fails and raise_errors is set.
        """
        url = url.replace('//','/').replace(':/','://') # May not be needed, but looks better in the printouts.
        return await self._checked_get_or_post(url, the_request, False, requests_kwargs=requests_kwargs, good_message=good_message, bad_message=bad_message, raise_errors=raise_errors)
    async def checked_post(self, url, the_request, requests_kwargs=None, good_message=None, bad_message="This HTTPs POST request failed", raise_errors=True):
        """
        Calls self._checked_get_or_post with is_post=True.
        Accepts the url, the request itself, the kwargs for the request, the message to print on a happy 200, the message to print on a sad non-200, and whether to raise errors if sad.
        Returns the response. Raises a BadResponseException if it fails and raise_errors is set.
        """
        url = url.replace('//','/').replace(':/','://') # May not be needed, but looks better in the printouts.
        return await self._checked_get_or_post(url, the_request, True, requests_kwargs=requests_kwargs, good_message=good_message, bad_message=bad_message, raise_errors=raise_errors)

    ############################ Auth ############################

    @property
    def headers(self):
        """
        Returns the authentication headers. Used for all API calls except for authenticate() and refresh().
        headers["Auth-Origin"] is the authentication service, such as "cognito".
        headers["Authorization"] is the access token, etc that proves authentication.
        """
        return {
            "Auth-Origin": "cognito",
            "Authorization": f"Bearer {self.access_token}"
        }

    @logger.catch
    async def authenticate(self):
        """
        Authenticates using self.username andself.password. Needs to be called before any other API calls.
        Returns (the access token, the refresh token).
        Raises an Exception if doesn't receive a valid response.
        Like most GET and POST functions it will raise any errors thrown by the http API.
        """
        response_dict = await self.checked_post(url=self.http_server_uri + "/auth/sign_in", the_request={"username": self.username, "password": self.password}, requests_kwargs=None, good_message=None, bad_message="Error during authentication", raise_errors=True)
        self.access_token = response_dict.get('data').get('AuthenticationResult').get('AccessToken')
        self.refresh_token = response_dict.get('data').get('AuthenticationResult').get('RefreshToken')
        logger.info(f"Authenticated. Access token: {self.access_token}")
        return self.access_token, self.refresh_token

    async def request_sign_up_code(self):
        """Signs up and sends the confirmation code to the email. Returns None. After confirming the account, self.authenticate() can be used to retrieve access and refresh tokens."""
        response_dict = await self.checked_post(url=self.http_server_uri + "/auth/sign_up", the_request={"username": self.username, "password": self.password}, requests_kwargs=None, good_message=None, bad_message="Error during signup", raise_errors=True)
        logger.info(f"Made a sign up request for {self.username}.")

    async def request_sign_up_code_again(self):
        """Resends the confimation code. Returns None. After confirming the account, self.authenticate() can be used to retrieve access and refresh tokens."""
        response_dict = await self.checked_post(url=self.http_server_uri + "/auth/resend_confirmation", the_request={"username": self.username}, requests_kwargs=None, good_message=None, bad_message="Error during signup code resend", raise_errors=True)
        logger.info(f"Made a sign up request for {self.username}.")

    async def sign_up_with_code(self, the_code):
        """Sends the confirmation code confirming the signup itself. Accepts the sign up code that was emailed. Returns None. After confirming the account, self.authenticate() can be used to retrieve access and refresh tokens."""
        response_dict = await self.checked_post(url=self.http_server_uri + "/auth/confirm_sign_up", the_request={"username": self.username, "confirmation_code": the_code}, requests_kwargs=None, good_message=None, bad_message="Error during signup confirm", raise_errors=True)
        logger.info(f"Made a sign up request for {self.username}.")

    async def get_password_reset_code(self):
        """Sends a reset-password request to the platform. After such a request is sent it will be necessary to check the email. Returns None"""
        response_dict = await self.checked_post(url=self.http_server_uri + "/auth/forgot_password", the_request={"username": self.username}, requests_kwargs=None, good_message=None, bad_message="Error during reset password code request", raise_errors=True)
        logger.info(f"Requesting a new password for {self.username}.")

    async def reset_password(self, the_code):
        """Updates the password with a new one. Returns None. Accepts the code that was emailed to the user (use get_password_reset_code)."""
        response_dict = await self.checked_post(url=self.http_server_uri + "/auth/confirm_reset_password", the_request={"username": self.username, "password":self.password, "confirmation_code":the_code}, requests_kwargs=None, good_message=None, bad_message="Error during reset password", raise_errors=True)
        logger.info(f"Reset the password for {self.username}.")

    async def delete_account(self):
        """Deletes the currently signed in account. Mainly used for testing. Returns None."""
        response_dict = await self.checked_post(url=self.http_server_uri + "/auth/delete_account", the_request={}, requests_kwargs=None, good_message=None, bad_message="Error during signup", raise_errors=True)
        logger.info(f"Deleted account for username: {self.username}, response={response_dict}")
        return None

    async def sign_out(self):
        """Signs out using the access token obtained from signing in. Returns None."""
        await self.checked_post(url=self.http_server_uri + "/auth/sign_out", the_request={"access_token": self.access_token}, requests_kwargs={'headers':self.headers}, good_message=None, bad_message="Error during signout", raise_errors=True)
        logger.info(f"Signed out.")

    async def refresh(self):
        """Refreshes the access token. Returns the new token."""
        response_dict = await self.checked_post(url=self.http_server_uri + "/auth/refresh", the_request={"username": self.username, "refresh_token": self.refresh_token}, requests_kwargs=None, good_message=None, bad_message="Error during refresh", raise_errors=True)
        self.access_token = response_dict.get('data').get('AuthenticationResult').get('AccessToken')
        logger.info(f"Refreshed access token: {self.access_token}")
        return self.access_token

    ######################## User #########################

    def _xtract_character(self, resp_data):
        """Given the JSON response data, returns a Character object."""
        c_data = {}
        c_data['character_id'] = resp_data['character_id']
        c_data['name'] = resp_data['character_context']['name']
        c_data['character_context'] = resp_data['character_context']
        c_data['avatar'] = resp_data['character_context']['avatar']
        c_data['description'] = resp_data['character_context']['description']
        return from_dict(data_class=Character, data=c_data)

    async def fetch_character_profile(self, character):
        """Given a string-valued (or list-valued) character_id/character returns a Character object (or list therof).
        It works for both member_ids and agent_ids."""
        is_list = type(character) not in [str, Character]
        character = types.to_char_id_list(character)
        types.assert_strs(*character)
        response_dict = await self.checked_post(url=self.http_server_uri + "/character/fetch_profile", the_request={"character_list": character}, requests_kwargs={'headers':self.headers}, good_message=None, bad_message="Error fetching user profile", raise_errors=True)
        characters = [self._xtract_character(d) for d in response_dict['data']]
        return characters if is_list else characters[0]

    async def fetch_member_ids(self, channel_id, service_id, raise_empty_list_err=False):
        """
        Fetches the member ids of a channel which coorespond to real users.

        Parameters:
          channel_id (str): The channel ID.
          service_id (str): The service/client/user ID.
          raise_empty_list_err=False: Raises an Exception if the list is empty.

        Returns:
         A list of character_id strings.

        Raises:
          An Exception (empty list) if raise_empty_list_err is True and the list is empty.
        """
        types.assert_strs(channel_id, service_id)
        params = {"channel_id": channel_id, "service_id": service_id}
        rkwargs = {'params':params, 'headers':self.headers}

        use_groups = False
        if use_groups:
            response_dict = await self.checked_get(url=self.http_server_uri + "/user/group/list", the_request=None, requests_kwargs=rkwargs, good_message="Successfully fetched channel character list", bad_message="Error fetching channel character list", raise_errors=True)
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
            response_dict = await self.checked_get(url=self.http_server_uri + "/channel/character_list", the_request=None, requests_kwargs=rkwargs, good_message="Successfully fetched channel character list", bad_message="Error fetching channel character list", raise_errors=True)
            character_list = response_dict['data']['character_list']

        if type(character_list) is not list:
            raise Exception('Got a character list which actually was not a list.')
        if character_list or not raise_empty_list_err:
            if character_list and type(character_list) is list and character_list[0] and type(character_list[0]) is list:
                raise Exception('Nested list bug (HTTP return).')
            return character_list
        else:
            raise Exception(f"Empty character_list error, channel_id: {channel_id}, service_id: {service_id}.")

    async def fetch_agents(self, service_id):
        """Given the service ID returns a list of non-user Character objects bound to this service."""
        types.assert_strs(service_id)
        m0 = "Successfully fetched character list"
        mr = "Error fetching character list"
        worked = False
        if not worked:
            try:
                response_dict = await self.checked_get(url=self.http_server_uri + f"/service/character/list?service_id={service_id}", the_request=None, requests_kwargs={'headers':self.headers}, good_message=m0, bad_message=mr, raise_errors=True)
                worked = True
            except Exception as e:
                logger.warning(f'Version 0 fetch_characters failed: {e}')
        if not worked:
            try:
                params = {"service_id": service_id}
                rkwargs = {'params':params, 'headers':self.headers}
                response_dict = await self.checked_get(url=self.http_server_uri + f"/service/character/list", the_request=None, requests_kwargs=rkwargs, good_message=m0, bad_message=mr, raise_errors=True)
                worked = True
            except Exception as e:
                logger.warning(f'Version 1 fetch_characters failed: {e}')
        if not worked:
            try:
                response_dict = await self.checked_get(url=self.http_server_uri + f"/service/character/list", the_request={"service_id": service_id}, requests_kwargs={'headers':self.headers}, good_message=m0, bad_message=mr, raise_errors=True)
                worked = True
            except Exception as e:
                logger.error(f'All three versions failed: {e}')
                raise e
        charlist = response_dict["data"]
        return [self._xtract_character(d) for d in charlist]

    async def fetch_user_info(self):
        """Returns the UserInfo of the user logged in as, containing thier name, avatar, etc. Used by user mode."""
        response_dict = await self.checked_get(url=self.http_server_uri + f"/user/info", the_request=None, requests_kwargs={'headers':self.headers}, good_message="Successfully fetched user info", bad_message="Error getting user info", raise_errors=True)
        idict = response_dict.get('data')
        email_verified = idict.get('email_verified') # Sometimes this is unfilled.
        return UserInfo(avatar=idict['context']['avatar'], description=idict['context']['description'], name=idict['context']['name'],
                        email=idict['email'], email_verified=email_verified, user_id=idict['user_id'], system_context=idict['system_context'])

    async def update_current_user(self, avatar, description, name):
        """Updates the user info. Used by user mode.

           Parameters:
             avatar: Link to image or local file_path to upload.
             description: Of the user.
             name: The name that shows in chat.

           Returns None.
        """
        avatar = await self.convert_to_url(avatar)
        the_request={"avatar": avatar, 'description':description, 'name':name}
        types.assert_strs(avatar, description, name)
        response_dict = await self.checked_post(url=self.http_server_uri + f"/user/info", the_request=the_request, requests_kwargs={'headers':self.headers}, good_message="Successfully updated user info", bad_message="Error updating user info", raise_errors=True)
        return response_dict.get('data')

    ############################# Service ############################

    async def create_service(self, description):
        """Accepts the description string. Creates and returns the string-valued service_id.
        Called once by the Moobius class if there is no service specified."""
        types.assert_strs(description)
        response_dict = await self.checked_post(url=self.http_server_uri + "/service/create", the_request={"description": description}, requests_kwargs={'headers':self.headers}, good_message="Successfully created service!", bad_message="Error creating service", raise_errors=True)
        return response_dict.get('data').get('service_id')

    async def fetch_service_id_list(self):
        """Returns a list of service_id strings of the user."""
        response_dict = await self.checked_get(url=self.http_server_uri + "/service/list", the_request=None, requests_kwargs={'headers':self.headers}, good_message=None, bad_message='Error getting service list', raise_errors=True)
        return response_dict.get('data')

    async def create_agent(self, service_id, name, avatar, description):
        """
        Creates a character with a given name, avatar, and description.
        The created user will be bound to the given service.

        Parameters:
          service_id (str): The service_id/client_id.
          name (str): The name of the user.
          avatar (str): The image URL of the user's picture OR a local file path.
          description (str): The description of the user.

        Returns: A Character object representing the created user.
        """
        avatar = await self.convert_to_url(avatar)

        jsonr = {"service_id": service_id,
                 "context": {
                   "name": name,
                   "avatar": avatar,
                   "description": description}}
        types.assert_strs(service_id, avatar, description, name)
        response_dict = await self.checked_post(url=self.http_server_uri + "/service/character/create", the_request=jsonr, requests_kwargs={'headers':self.headers}, good_message="Successfully created character", bad_message="Error creating character", raise_errors=True)
        character = self._xtract_character(response_dict['data'])
        return character

    async def update_agent(self, service_id, character, avatar, description, name):
        """Updates the characters name, avatar, etc for a FAKE user, for real users use update_current_user.

           Parameters:
             service_id (str): The service_id/client_id.
             character (str): Who to update. Can also be a Character object or character_id. Cannot be a list.
             avatar (str): A link to user's image or a local file_path to upload.
             description (str): The description of user.
             name (str): The name that will show in chat.

           Returns:
            Data about the user as a dict.
        """
        avatar = await self.convert_to_url(avatar)

        if type(character) is Character:
            character = character.character_id
        types.assert_strs(service_id, character, description, name, avatar)
        the_request = {"service_id": service_id, 'character_id':character, 'context': {'avatar':avatar, 'description':description, 'name':name}}
        response_dict = await self.checked_post(url=self.http_server_uri + f"/service/character/update", the_request=the_request, requests_kwargs={'headers':self.headers}, good_message="Successfully updated character info", bad_message="Error updating character info", raise_errors=True)
        return response_dict.get('data')

    ############################# Channel ############################

    async def create_channel(self, channel_name, channel_desc):
        """Creates a channel given a string-valued channel name and description. Returns the channel_id.
        Example ID: "13e44ea3-b559-45af-9106-6aa92501d4ed"."""
        types.assert_strs(channel_name, channel_desc)
        jsonr = {"channel_name": channel_name, 'context':{'channel_description':channel_desc}}
        response_dict = await self.checked_post(url=self.http_server_uri + "/channel/create", the_request=jsonr, requests_kwargs={'headers':self.headers}, good_message=f"Successfully created channel {channel_name}.", bad_message=f"Error creating channel {channel_name}", raise_errors=True)
        return response_dict['data']['channel_id']

    async def bind_service_to_channel(self, service_id, channel_id):
        """Binds a service to a channel given the service and channel IDs.
        This function is unusual in that it returns whether it was sucessful rather than raising errors if it fails."""
        types.assert_strs(service_id, channel_id)
        jsonr = {"channel_id": channel_id, "service_id": service_id}
        response_dict = await self.checked_post(url=self.http_server_uri + "/service/bind", the_request=jsonr, requests_kwargs={'headers':self.headers}, good_message=f"Successfully binded service {service_id} to channel {channel_id}.", bad_message=f"Error binding service {service_id} to channel {channel_id}", raise_errors=False)

        logger.debug(f"bind_service_to_channel response {response_dict}")
        if response_dict['code'] == 10000: # This means no error.
            return True
        else:
            return False

    async def unbind_service_from_channel(self, service_id, channel_id):
        """Unbinds a service to a channel given the service and channel IDs. Returns None."""
        types.assert_strs(service_id, channel_id)
        jsonr = {"channel_id": channel_id,"service_id": service_id}
        await self.checked_post(url=self.http_server_uri + "/service/unbind", the_request=jsonr, requests_kwargs={'headers':self.headers}, good_message=f"Successfully unbound service {service_id} from channel {channel_id}", bad_message=f"Error unbinding service {service_id} from channel {channel_id}", raise_errors=True)

    async def update_channel(self, channel_id, channel_name, channel_desc):
        """
        Updates the name and desc of a channel.

        Parameters:
          channel_id (str): Which channel to update.
          channel_name (str): The new channel name.
          channel_desc (str): The new channel description.

        Returns None.
        """
        types.assert_strs(channel_name, channel_id, channel_desc)
        jsonr = {"channel_id": channel_id, "channel_name": channel_name, "context":{"channel_description":channel_desc}}
        await self.checked_post(url=self.http_server_uri + "/channel/update", the_request=jsonr, requests_kwargs={'headers':self.headers}, good_message=f"Successfully updated channel {channel_id}", bad_message=f"Error updating channel {channel_id}", raise_errors=True)

    async def fetch_popular_channels(self):
        """Fetches the popular channels, returning a list of channel_id strings."""
        response_dict = await self.checked_get(url=self.http_server_uri + "/channel/popular", the_request=None, requests_kwargs={'headers':self.headers}, good_message=f"Successfully fetched popular channels", bad_message=f"Error fetching popular channels", raise_errors=True)
        out = []
        for ch in response_dict['data']:
            if type(ch) is not str:
                ch = ch['channel_id']
            out.append(ch)
        return out

    async def fetch_channel_list(self):
        """Fetches all? channels, returning a list of channel_id strings."""
        response_dict = await self.checked_get(url=self.http_server_uri + "/channel/list", the_request=None, requests_kwargs={'headers':self.headers}, good_message=f"Successfully fetched channels", bad_message=f"Error fetching channels", raise_errors=True)
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

        Returns a list of dicts.
        """
        if type(limit) is not str:
            limit = str(limit)
        types.assert_strs(channel_id, limit, before)
        params = {'channel_id':channel_id, 'limit':limit, 'before':before}
        rkwargs = {'params':params, 'headers':self.headers}
        jsonr = {"limit": limit} # Not where to put the limit, so it is put in both places.

        the_response = await self.checked_get(url=self.http_server_uri + "/channel/history_message", the_request=jsonr, requests_kwargs=rkwargs, good_message=f"Successfully fetched message history for channel {channel_id}", bad_message=f"Error fetching message history for channel {channel_id}", raise_errors=False)
        if 'blob' in the_response: # HTML style.
            return the_response['blob']
        return the_response

    async def this_user_channels(self):
        """Returns the list of channel_ids this user is in."""
        the_response = await self.checked_get(url=self.http_server_uri + "/channel/list", the_request=None, requests_kwargs={'headers':self.headers}, good_message=f"Successfully listed channels current user is in.", bad_message=f"Error listing channels current user is in.", raise_errors=False)
        return [x['channel_id'] for x in the_response['data']]
 
    ############################# File ############################

    async def _upload_extension(self, extension):
        """Gets the upload URL and needed fields for uploading a file given a string-valued extension.
        Returns (upload_url or None, upload_fields)."""
        types.assert_strs(extension)
        requests_kwargs = {'params':{"extension": extension}, 'headers':self.headers}
        response_dict = await self.checked_get(url=self.http_server_uri + "/file/upload", the_request=None, requests_kwargs=requests_kwargs, good_message="Successfully fetched upload url!", bad_message="Error fetching upload url", raise_errors=True)

        upload_url = response_dict.get('data').get('url')
        upload_fields = response_dict.get('data').get('fields')
        return upload_url, upload_fields

    async def _do_upload(self, upload_url, upload_fields, file_path):
        """
        Uploads a file to the given upload URL with the given upload fields.

        Parameters:
          upload_url (str): obtained with _upload_extension.
          upload_fields (dict): obtained with _upload_extension.
          file_path (str): The path of the file.

        Returns:
          The full URL string of the uploaded file. None if doesn't receive a valid response (error condition).

        Raises:
          Exception: If the file upload fails, this function will raise an exception detailing the error.
        """
        if type(upload_fields) is not dict:
            raise Exception('Upload fields must be a dict, and one that comes from _upload_extension')
        types.assert_strs(upload_url, file_path)
        with open(file_path, 'rb') as f:
            files = {'file': (file_path, f)}
            full_url = upload_url + upload_fields.get("key")
            logger.opt(colors=True).info(f"<fg 160,0,240>{('file upload: '+upload_url+' '+str(files)).replace('<', '&lt;').replace('>', '&gt;')}</>")

            #SECOND answer on: https://stackoverflow.com/questions/57553738/how-to-aiohttp-request-post-files-list-python-requests-module
            upload_fields['file'] = f.read()
            _ = await self._checked_get_or_post(upload_url, the_request=None, is_post=True, requests_kwargs={'data':upload_fields}, good_message=f'Successfully uploaded {file_path} to {full_url}', bad_message=f'failed to upload {file_path}', raise_errors=False)
            return full_url

    async def upload(self, file_path):
        """Accepts a file_path. Uploads the file at local path file_path to the Moobius server. Automatically calculates the upload URL and upload fields.
        Returns the uploaded URL. Raises an Exception if the upload fails.
        """
        if not os.path.exists(file_path):
            raise Exception(f'Local file not found: {os.path.realpath(file_path)}')
        extension = file_path.split(".")[-1]
        upload_url, upload_fields = await self._upload_extension(extension)
        if upload_url and upload_fields:
            # Exception will be raised in _do_upload(), no need to raise here
            full_url = await self._do_upload(upload_url, upload_fields, file_path)
            return full_url
        else:
            logger.error(f"Error getting upload url and upload fields! file_path: {file_path}")
            raise Exception(f"Error getting upload url and upload fields! file_path: {file_path}")

    async def convert_to_url(self, file_path):
        """Accepts a file_path. Uploads and returns the bucket's url. Idempotent: If given a URL will just return the URL.
        Empty, False, or None strings are converted to a default URL."""
        if not file_path:
            return f"https://{types.S3BUCKET}.amazonaws.com/LogoLight.jpg"
        if 'https://' in file_path or 'http://' in file_path or 'ftp://' in file_path or 'ftps://' in file_path:
            return file_path
        elif not os.path.exists(file_path):
            raise Exception(f'Cannot find this local file to upload: {os.path.realpath(file_path)}')
        else:
            with open(file_path, 'rb') as f:
                the_bytes = f.read()
            the_hash = hashlib.sha256(the_bytes).hexdigest()
            if the_hash not in self.filehash2URL:
                self.filehash2URL[the_hash] = await self.upload(file_path)
            return self.filehash2URL[the_hash]

    async def download_size(self, url, headers=None):
        """Gets the download size in bytes given a url and optional headers. Queries for the header and does not download the file. Returns the number of bytes."""
        if headers is None: # These buckets are public so no need to upload.
            headers = {}
        if headers == 'self':
            headers={'headers':self.headers} # Auth allows downloading form buckets we authed for.
        try:
            async with aiohttp.ClientSession() as session:
                async with session.head(url, **headers) as response:
                    if 'Content-Length' in response.headers:
                        file_size = int(response.headers['Content-Length'])
                        return file_size
                    else:
                        logger.warning("Content-Length not found in headers.")
                        return None
        except aiohttp.ClientError as e:
            return None

    async def download(self, source, file_path=None, auto_dir=None, overwrite=None, bytes=None, headers=None):
        """
        Downloads a file from a url or other source to a local filename, automatically creating dirs if need be.

        Parameters:
          source: The url to download the file from. OR a MessageBody which has a .content.path in it.
          file_path=None: The file_path to download to.
            None will create a file based on the timestamp + random numbers.
            If no extension is specified, will infer the extension from the url if one exists.
          auto_dir=None: If no file_path is specified, a folder must be choosen.
            Defaults to './downloads'.
          overwrite=None:
            Allow overwriting pre-existing files. If False, will raise an Exception on name collision.
          bytes=None:
            If True, will return bytes instead of saving a file.
          headers=None:
            Optional headers. Use these for downloads that require auth.
            Can set to "self" to use the same auth headers that this instance is using.

        Returns:
          The full filepath if bytes if false, otherwise the file's content bytes if bytes=True.
        """
        full_path = file_path
        if headers is None: # These buckets are public so no need to upload.
            headers = {}
        if headers == 'self':
            headers={'headers':self.headers} # Auth allows downloading form buckets we authed for.
        if not full_path:
            if not auto_dir:
                auto_dir = './downloads'
            full_path = auto_dir+'/'+datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f") + '_' + str(random.randint(1000, 9999))
        if type(source) is str:
            url = source
        elif type(source) is MessageBody:
            if hasattr(source.content, 'path') and source.content.path:
                url = source.content.path
            else:
                raise Exception("This message does not have a path in it's content.")
        else:
            raise Exception(f"Source must be a str or MessageBody, not a {type(source)}")
        full_path = os.path.realpath(full_path).replace('\\','/')
        if not '.' in full_path.split('/')[-1]:
            url_leaf = url.split('/')[-1]
            if '.' in url_leaf: # Infer the extension from the url.
                full_path = full_path+'.'+url_leaf.split('.')[-1]

        # https://stackoverflow.com/questions/35388332/how-to-download-images-with-aiohttp
        async with aiohttp.ClientSession() as session:
            async with session.get(url, **headers) as resp:
                if resp.status == 200:
                    if bytes:
                        buffer = io.BytesIO()
                        async for chunk in resp.content.iter_chunked(10):
                            buffer.write(chunk)
                        buffer.seek(0)
                        return buffer.getvalue()
                    else:
                        os.makedirs(os.path.dirname(full_path), exist_ok=True)
                        if os.path.exists(full_path) and not overwrite:
                            raise Exception(f'Assert no overwrite to pre-existing file: {full_path}')
                        with open(full_path, 'wb') as fd:
                            async for chunk in resp.content.iter_chunked(10):
                                fd.write(chunk)
                else:
                    raise Exception(f'Cannot download file: {resp}')
        return full_path

    ############################# Groups ############################

    async def fetch_channel_group_dict(self, channel_id, service_id):
        """Similar to fetch_member_ids. Accepts the channel_id and service_id. returns a dict from each group_id to all characters."""
        types.assert_strs(channel_id, service_id)
        params = {"channel_id": channel_id, "service_id": service_id}
        rkwargs = {'params':params, 'headers':self.headers}

        response_dict = await self.checked_get(url=self.http_server_uri + "/user/group/list", the_request=None, requests_kwargs=rkwargs, good_message="Successfully fetched channel group dict", bad_message="Error fetching channel group dict", raise_errors=True)
        id2members = {}
        for x in response_dict['data']:
            if type(x['characters']) is not list:
                raise Exception('The characters field of data for /user/group/list should be a list.')
            id2members[x['group_id']] = x['characters']
        return id2members

    async def fetch_channel_group_list(self, channel_id, service_id):
        """Similar to fetch_channel_group_dict. Accepts the channel_id and service_id. Returns the raw data."""
        types.assert_strs(channel_id, service_id)
        params = {"channel_id": channel_id, "service_id": service_id}
        rkwargs = {'params':params, 'headers':self.headers}

        response_dict = await self.checked_get(url=self.http_server_uri + "/user/group/list", the_request=None, requests_kwargs=rkwargs, good_message="Successfully fetched channel group list", bad_message="Error fetching channel group list", raise_errors=True)
        return response_dict['data']

    async def create_channel_group(self, channel_id, group_name, characters):
        """
        Creates a channel group.

        Parameters:
          channel_id (str): The id of the group leader?
          group_name (str): What to call it.
          characters (list): A list of characters or character_id strings that will be inside the group.

        Returns:
          The group_id string.
        """
        characters = types.to_char_id_list(characters) # Should not be necessary since this function is an internal function.
        types.assert_strs(*([channel_id, group_name]+characters))
        jsonr = {"channel_id": channel_id, "group_name":group_name, "characters": characters}
        response_dict = await self.checked_post(url=self.http_server_uri + "/user/group/create", the_request=jsonr, requests_kwargs={'headers':self.headers}, good_message="Successfully created channel group {group_name}!", bad_message="Error creating channel group {group_name}", raise_errors=True)
        return from_dict(data_class=Group, data={'group_id': response_dict['data']['group_id'], 'character_ids':characters})

    async def character_ids_of_service_group(self, group_id):
        """
        Given a group_id, returns a list of character ids belonging to a service group.
        Note that the 'recipients' in 'on message up' might be None:
          To avoid requiring checks for None this function will return an empty list given Falsey inputs or Falsey string literals.
        """
        if not group_id or group_id in ['None', 'null', 'none', 'Null', 'false', 'False']:
            return []
        types.assert_strs(group_id)
        use_questionmark = True
        if use_questionmark:
            response_dict = await self.checked_get(url=self.http_server_uri + f"/service/group?group_id={group_id}", the_request=None, requests_kwargs={'headers':self.headers}, good_message="Successfully fetched service group roster!", bad_message="Error fetching service group roster", raise_errors=True)
        else:
            the_json = {'group_id':group_id}
            response_dict = await self.checked_get(url=self.http_server_uri + f"/service/group", the_request=the_json, requests_kwargs={'headers':self.headers}, good_message="Successfully fetched service group roster!", bad_message="Error fetching service group roster", raise_errors=True)
        if len(response_dict['data']) == 0:
            logger.warning(f'This group, if service group, seems to have no character ids in it: {group_id}')
            return []
        logger.info(f'Character id, service group HTTP response: {response_dict}')
        return response_dict['data']['characters']

    async def character_ids_of_channel_group(self, sender_id, channel_id, group_id):
        """
        Gets a list of character ids belonging to a channel group.
        Websocket payloads contain these channel_groups which are shorthand for a list of characters.

        Parameters:
          sender_id: The message's sender.
          channel_id: The message specified that it was sent in this channel.
          group_id: The messages recipients.

        Returns the character_id list.
        """
        types.assert_strs(channel_id, sender_id, group_id)
        use_questionmark = True
        if use_questionmark:
            response_dict = await self.checked_get(url=self.http_server_uri + f"/user/group?group_id={group_id}&channel_id={channel_id}&user_id={sender_id}", the_request=None, requests_kwargs={'headers':self.headers}, good_message="Successfully fetched channel group roster!", bad_message="Error fetching channel group roster", raise_errors=True)
        else:
            the_json = {'user_id':sender_id, 'group_id':group_id, 'channel_id':channel_id}
            response_dict = await self.checked_get(url=self.http_server_uri + f"/user/group", the_request=the_json, requests_kwargs={'headers':self.headers}, good_message="Successfully fetched channel group roster!", bad_message="Error fetching channel group roster", raise_errors=True)
        logger.info(f'List character IDs of channel group HTTP response: {response_dict}')
        if len(response_dict['data']) == 0:
            logger.warning(f'This group, if channel group, seems to have no character ids in it: {group_id}')
            return []
        return response_dict['data']['characters']

    async def create_service_group(self, characters):
        """
        Creates a group containing the list of characters_ids and returns this Group object.
        This group can then be used in send_message_down payloads.

        Parameters:
          characters (list): A list of character_id strings or Characters that will be inside the group.

        Returns:
          A Group object.
        """
        characters = types.to_char_id_list(characters) # Should not be necessary since this function is an internal function.
        types.assert_strs(*characters)
        jsonr = {"group_id": "", "characters": characters}
        response_dict = await self.checked_post(url=self.http_server_uri + "/service/group/create", the_request=jsonr, requests_kwargs={'headers':self.headers}, good_message="Successfully created service group!", bad_message="Error creating service group", raise_errors=True)
        group_id = response_dict['data']
        if type(group_id) is not str:
            raise Exception('The group id returned was not a string.')
        group = from_dict(data_class=Group, data={'group_id': group_id, 'character_ids':characters})
        return group

    async def update_channel_group(self, channel_id, group_id, characters):
        """
        Updates a channel group.

        Parameters:
          channel_id (str): The id of the group leader?
          group_name (str): What to call it.
          characters (list): A list of character_id strings that will be inside the group.

        Returns None.

        Raises:
            An Exception because it is unused, unimplemented, and may be removed.
        """
        raise Exception('Unknown if this function is needed.')

    async def update_temp_channel_group(self, channel_id, characters):
        """
        Updates a channel TEMP group.

        Parameters:
          channel_id (str): The id of the group leader?
          characters (list): A list of character_id strings that will be inside the group.

        Returns None.

        Raises:
            An Exception because it is unused, unimplemented, and may be removed.
        """
        raise Exception('Unknown if this function is needed.')

    async def fetch_channel_temp_group(self, channel_id, service_id):
        """Like fetch_channel_group_list but for TEMP groups. Given the channel_id and service_id, returns the list of groups."""
        types.assert_strs(channel_id, service_id)
        params = {"channel_id": channel_id, "service_id": service_id}
        rkwargs = {'params':params, 'headers':self.headers}

        response_dict = await self.checked_get(url=self.http_server_uri + "/user/group/temp", the_request=None, requests_kwargs=rkwargs, good_message="Successfully fetched channel temp group list", bad_message="Error fetching channel temp group list", raise_errors=True)
        return response_dict['data']

    async def fetch_user_from_group(self, user_id, channel_id, group_id):
        """
        Not yet implemented!
        Fetches the user profile of a user from a group.

        Parameters:
            user_id (str): The user ID.
            channel_id (str): The channel ID. (TODO: of what?)
            group_id (str): The group ID.

        Returns:
            The user profile Character object.

        Raises:
            An Exception because it is unused, unimplemented, and may be removed.
        """
        raise Exception('http_api_wrapper.fetch_user_from_group has not yet been implemented.')

    async def fetch_target_group(self, user_id, channel_id, group_id):
        """
        Not yet implemented!
        Fetches info about the group.

        Parameters:
            user_id (str): The user id of the user bieng fetched (is this needed?)
            channel_id (str): The channel_id of the channel bieng fetched.
            group_id (str): Which group to fetch.

        Returns:
            The data-dict data.

        Raises:
            An Exception because it is unused, unimplemented, and may be removed.
        """
        raise Exception('http_api_wrapper.fetch_target_group has not yet been implemented.')

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
