.. _moobius_network_http_api_wrapper:

moobius.network.http_api_wrapper
===================================


Module-level functions
===================

.. _moobius.network.http_api_wrapper.get_or_post:
get_or_post
-----------------------------------
**get_or_post(url, is_post, requests_kwargs, raise_json_decode_errors)**

Get or post, will use requests.get/post or aiohttp.session.get/post depending on which one has been choosen.

Parameters:
  url (str): https://...
  is_post (bool): False for GET, True for POST.
  requests_kwargs=None: These are fed into the requests/session get/post function.
  raise_json_decode_errors=True

Returns: A dict which is json.loads() of the return.
  dict['code'] has the code, 10000 is good and 204 indicates no return but without error which is also fine.
  dict['blob'] is the response text in cases where the JSON fail and raise_json is False.

Raises:
  Exception if Json fails and raise_json is True. Not all non-error returns are JSON thus the "blob" option.


===================


Class BadResponseException
===================

For when the network is not doing what it should.





Class HTTPAPIWrapper
===================

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

.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.__init__:
HTTPAPIWrapper.__init__
-----------------------------------
**HTTPAPIWrapper.__init__(self, http_server_uri, email, password)**

Initialize the HTTP API wrapper.

Parameters:
  http_server_uri (str): The URI of the Moobius HTTP server.
  email (str): The email of the user.
  password (str): The password of the user.

No return value.

Example:
  >>> http_api_wrapper = HTTPAPIWrapper("http://localhost:8080", "test@test", "test")

.. _moobius.network.http_api_wrapper.HTTPAPIWrapper._checked_get_or_post:
HTTPAPIWrapper._checked_get_or_post
-----------------------------------
**HTTPAPIWrapper._checked_get_or_post(self, url, the_request, is_post, requests_kwargs, good_message, bad_message, raise_errors)**

Runs a GET or POST request returning the result as a JSON with optional logging and error raising.

Parameters:
  url (str): The https://... url.
  the_request (dict): The "json" kwarg is set to this. Can be None in which no "json" will be set.
  is_post: True for post, False for get.
  requests_kwargs=None: Dict of extra arguments to send to requests/aiohttp. None is equivalent to {}
  good_message=None: The string-valued message to logger.debug. None means do not log.
  bad_message="...": The string-valued to prepend to logger.error if the response isnt code 10000.
  raise_errors=True: Raise a BadResponseException if the request returns an error.

Returns:
  The https response as a dict, using requests/aiohttp.post(...).json() to parse it.

Raises:
  BadResponseException if raise_errors=True and the response is an error response.

.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.checked_get:
HTTPAPIWrapper.checked_get
-----------------------------------
**HTTPAPIWrapper.checked_get(self, url, the_request, requests_kwargs, good_message, bad_message, raise_errors)**

Calls self._checked_get_or_post with is_post=False

.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.checked_post:
HTTPAPIWrapper.checked_post
-----------------------------------
**HTTPAPIWrapper.checked_post(self, url, the_request, requests_kwargs, good_message, bad_message, raise_errors)**

Calls self._checked_get_or_post with is_post=True

.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.headers:
HTTPAPIWrapper.headers
-----------------------------------
**HTTPAPIWrapper.headers(self)**

Returns the authentication headers. Used for all API calls except for authenticate() and refresh().
headers["Auth-Origin"] is the authentication service, such as "cognito".
headers["Authorization"] is the access token, etc that proves authentication.

.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.authenticate:
HTTPAPIWrapper.authenticate
-----------------------------------
**HTTPAPIWrapper.authenticate(self)**

Authenticates the user. Needs to be called before any other API calls.
Returns (the access token, the refresh token). Exception if doesn't receive a valid response.
Like most GET and POST functions it will raise any errors thrown by the http API.

.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.sign_up:
HTTPAPIWrapper.sign_up
-----------------------------------
**HTTPAPIWrapper.sign_up(self)**

Signs up. Returns (the access token, the refresh token).
Exception if doesn't receive a valid response.

.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.sign_out:
HTTPAPIWrapper.sign_out
-----------------------------------
**HTTPAPIWrapper.sign_out(self)**

Signs out using the access token obtained from signing in. Returns None.

.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.refresh:
HTTPAPIWrapper.refresh
-----------------------------------
**HTTPAPIWrapper.refresh(self)**

Refreshes the access token, returning it.

.. _moobius.network.http_api_wrapper.HTTPAPIWrapper._xtract_character:
HTTPAPIWrapper._xtract_character
-----------------------------------
**HTTPAPIWrapper._xtract_character(self, resp_data)**

<No doc string>

.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.fetch_character_profile:
HTTPAPIWrapper.fetch_character_profile
-----------------------------------
**HTTPAPIWrapper.fetch_character_profile(self, character_id)**

Returns a Character object (or list) given a string-valued (or list-valued) character_id.

.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.fetch_real_character_ids:
HTTPAPIWrapper.fetch_real_character_ids
-----------------------------------
**HTTPAPIWrapper.fetch_real_character_ids(self, channel_id, service_id, raise_empty_list_err)**

Fetches the real user ids of a channel. A service function, will not work as an Agent function.

Parameters:
  channel_id (str): The channel ID.
  service_id (str): The service/client/agent ID.
  raise_empty_list_err=True: Raises an Exception if the list is empty.

Returns:
 A list of character_id strings.

Raises:
  Exception (empty list) if raise_empty_list_err is True and the list is empty.

.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.fetch_service_characters:
HTTPAPIWrapper.fetch_service_characters
-----------------------------------
**HTTPAPIWrapper.fetch_service_characters(self, service_id)**

Get the user list (a list of Character objects), of a service given the string-valued service_id.

.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.fetch_user_info:
HTTPAPIWrapper.fetch_user_info
-----------------------------------
**HTTPAPIWrapper.fetch_user_info(self)**

Used by the Agent to get their info as a UserInfo object.

.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.update_current_user:
HTTPAPIWrapper.update_current_user
-----------------------------------
**HTTPAPIWrapper.update_current_user(self, avatar, description, name)**

Updates the user info. Will only be an Agent function in the .net version.

Parameters:
  avatar: Link to image.
  description: Of the user.
  name: The name that shows in chat.

No return value.

.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.create_service:
HTTPAPIWrapper.create_service
-----------------------------------
**HTTPAPIWrapper.create_service(self, description)**

Creates a service with the given description string and returns the string-valued service_id.

.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.fetch_service_id_list:
HTTPAPIWrapper.fetch_service_id_list
-----------------------------------
**HTTPAPIWrapper.fetch_service_id_list(self)**

Returns a list of service ID strings of the user, or None if doesn't receive a valid response or one without any 'data' (error condition).

.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.create_character:
HTTPAPIWrapper.create_character
-----------------------------------
**HTTPAPIWrapper.create_character(self, service_id, name, avatar, description)**

Creates a character with given name, avatar, and description.
The created user will be bound to the given service.

Parameters:
  service_id (str): The service_id/client_id.
  name (str): The name of the user.
  avatar (str): The image URL of the user's picture/
  description (str): The description of the user.

Returns: A Character object representing the created user, None if doesn't receive a valid response (error condition). TODO: Should these error conditions jsut raise Exceptions instead?

.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.update_character:
HTTPAPIWrapper.update_character
-----------------------------------
**HTTPAPIWrapper.update_character(self, service_id, character_id, avatar, description, name)**

Updates the user info for a FAKE user, for real users use update_current_user.

Parameters:
  service_id (str): Which service holds the user.
  character_id (str): Of the user.
  avatar (str): Link to user's image.
  description (str): Description of user.
  name (str): The name that shows in chat.

Returns:
 Data about the user as a dict.

.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.create_channel:
HTTPAPIWrapper.create_channel
-----------------------------------
**HTTPAPIWrapper.create_channel(self, channel_name, channel_desc)**

Creates a channel given a string-valued channel name and description. Returns the channel_id.
Example ID: "13e44ea3-b559-45af-9106-6aa92501d4ed".

.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.bind_service_to_channel:
HTTPAPIWrapper.bind_service_to_channel
-----------------------------------
**HTTPAPIWrapper.bind_service_to_channel(self, service_id, channel_id)**

Binds a service to a channel given the service and channel IDs. Returns whether sucessful.

.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.unbind_service_from_channel:
HTTPAPIWrapper.unbind_service_from_channel
-----------------------------------
**HTTPAPIWrapper.unbind_service_from_channel(self, service_id, channel_id)**

Unbinds a service to a channel given the service and channel IDs. Returns None.

.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.update_channel:
HTTPAPIWrapper.update_channel
-----------------------------------
**HTTPAPIWrapper.update_channel(self, channel_id, channel_name, channel_desc)**

Updates the name and desc of a channel.

Parameters:
  channel_id (str): Which channel to update.
  channel_name (str): The new channel name.
  channel_desc (str): The new channel description.

No return value.

.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.fetch_popular_chanels:
HTTPAPIWrapper.fetch_popular_chanels
-----------------------------------
**HTTPAPIWrapper.fetch_popular_chanels(self)**

Fetches the popular channels, returning a list of channel_id strings.

.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.fetch_channel_list:
HTTPAPIWrapper.fetch_channel_list
-----------------------------------
**HTTPAPIWrapper.fetch_channel_list(self)**

Fetches all? channels, returning a list of channel_id strings.

.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.fetch_message_history:
HTTPAPIWrapper.fetch_message_history
-----------------------------------
**HTTPAPIWrapper.fetch_message_history(self, channel_id, limit, before)**

Returns the message chat history.

Parameters:
  channel_id (str): Channel with the messages inside of it.
  limit=64: Max number of messages to return (messages further back in time, if any, will not be returned).
  before="null": Only return messages older than this.

Should return a list of dicts, but has not been tested.

.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.this_user_channels:
HTTPAPIWrapper.this_user_channels
-----------------------------------
**HTTPAPIWrapper.this_user_channels(self)**

What channels this user is joined to?

.. _moobius.network.http_api_wrapper.HTTPAPIWrapper._upload_extension:
HTTPAPIWrapper._upload_extension
-----------------------------------
**HTTPAPIWrapper._upload_extension(self, extension)**

Get the upload URL and upload fields for uploading a file with the given string-valued extension.
Returns (upload_url or None, upload_fields).

.. _moobius.network.http_api_wrapper.HTTPAPIWrapper._do_upload_file:
HTTPAPIWrapper._do_upload_file
-----------------------------------
**HTTPAPIWrapper._do_upload_file(self, upload_url, upload_fields, file_path)**

Upload a file to the given upload URL with the given upload fields.

Parameters:
  upload_url (str): obtained with _upload_extension.
  upload_fields (dict): obtained with _upload_extension.
  file_path (str): The path of the file.

Returns:
  The full URL string of the uploaded file. None if doesn't receive a valid response (error condition).

Raises:
  Exception: If the file upload fails, this function will raise an exception about the error.

.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.upload_file:
HTTPAPIWrapper.upload_file
-----------------------------------
**HTTPAPIWrapper.upload_file(self, file_path)**

Upload the file at local path file_path to the Moobius server. Automatically gets the upload URL and upload fields.
Returns the full upload URL. Raises Exception if the upload fails.

.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.fetch_channel_group_dict:
HTTPAPIWrapper.fetch_channel_group_dict
-----------------------------------
**HTTPAPIWrapper.fetch_channel_group_dict(self, channel_id, service_id)**

Like fetch_real_character_ids but returns a dict from group_id to all characters.

.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.fetch_channel_group_list:
HTTPAPIWrapper.fetch_channel_group_list
-----------------------------------
**HTTPAPIWrapper.fetch_channel_group_list(self, channel_id, service_id)**

Like fetch_channel_group_dict but returns the raw data.

.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.create_channel_group:
HTTPAPIWrapper.create_channel_group
-----------------------------------
**HTTPAPIWrapper.create_channel_group(self, channel_id, group_name, characters)**

Creates a channel group.

Parameters:
  channel_id (str): The id of the group leader?
  group_name (str): What to call it.
  characters (list): A list of channel_id strings that will be inside the group.

Returns:
  The group id string.

.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.character_ids_of_service_group:
HTTPAPIWrapper.character_ids_of_service_group
-----------------------------------
**HTTPAPIWrapper.character_ids_of_service_group(self, group_id)**

Gets a list of character ids belonging to a service group.
Note that the 'recipients' in 'on message up' might be None:
  This function will return an empty list given Falsey inputs or Falsey string literals.

.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.character_ids_of_channel_group:
HTTPAPIWrapper.character_ids_of_channel_group
-----------------------------------
**HTTPAPIWrapper.character_ids_of_channel_group(self, sender_id, channel_id, group_id)**

Gets a list of character ids belonging to a channel group that is returned by a message.

Parameters:
  sender_id: The message's sender.
  channel_id: The message specified that it was sent in this channel.
  group_id: The messages recipients.

.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.create_service_group:
HTTPAPIWrapper.create_service_group
-----------------------------------
**HTTPAPIWrapper.create_service_group(self, characters)**

Create a group containing characters id list, returning a Group object.
Sending messages down for the new .net API requires giving myGroup.group_id instead of a list of character_ids.

Parameters:
  group_name (str): What to call it.
  characters (list): A list of character_id strings that will be inside the group.

Returns:
  A Group object.

.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.update_channel_group:
HTTPAPIWrapper.update_channel_group
-----------------------------------
**HTTPAPIWrapper.update_channel_group(self, channel_id, group_id, members)**

Updates a channel group.

Parameters:
  channel_id (str): The id of the group leader?
  group_name (str): What to call it.
  members (list): A list of channel_id strings that will be inside the group.

No return value.

.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.update_temp_channel_group:
HTTPAPIWrapper.update_temp_channel_group
-----------------------------------
**HTTPAPIWrapper.update_temp_channel_group(self, channel_id, members)**

Updates a channel TEMP group.

Parameters:
  channel_id (str): The id of the group leader?
  members (list): A list of channel_id strings that will be inside the group.

No return value.

.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.fetch_channel_temp_group:
HTTPAPIWrapper.fetch_channel_temp_group
-----------------------------------
**HTTPAPIWrapper.fetch_channel_temp_group(self, channel_id, service_id)**

Like fetch_channel_group_list but for Temp groups.

.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.fetch_user_from_group:
HTTPAPIWrapper.fetch_user_from_group
-----------------------------------
**HTTPAPIWrapper.fetch_user_from_group(self, user_id, channel_id, group_id)**

Fetch the user profile of a user from a group.

Parameters:
    user_id (str): The user ID.
    channel_id (str): The channel ID. (TODO: of what?)
    group_id (str): The group ID.

Returns:
    The user profile Character object.

.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.fetch_target_group:
HTTPAPIWrapper.fetch_target_group
-----------------------------------
**HTTPAPIWrapper.fetch_target_group(self, user_id, channel_id, group_id)**

Fetches info about the group.

  Parameters:
    user_id (str), channel_id (str): why needed?
    group_id (str): Which group to fetch.

  Returns:
    The data-dict data.

.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.__str__:
HTTPAPIWrapper.__str__
-----------------------------------
**HTTPAPIWrapper.__str__(self)**

<No doc string>

.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.__repr__:
HTTPAPIWrapper.__repr__
-----------------------------------
**HTTPAPIWrapper.__repr__(self)**

<No doc string>