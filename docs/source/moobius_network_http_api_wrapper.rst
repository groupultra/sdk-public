.. _moobius_network_http_api_wrapper:

###################################################################################
Module moobius.network.http_api_wrapper
###################################################################################

******************************
Module-level functions
******************************

.. _moobius.network.http_api_wrapper.get_or_post:

get_or_post
---------------------------------------------------------------------------------------------------------------------
get_or_post(url, is_post, requests_kwargs, raise_json_decode_errors)


Sends a GET or POST request and awaits for the response.
  Parameters:
    url (str): The https://...
    
    is_post (bool): The False for GET, True for POST.
    
    requests_kwargs=None: These are fed into the requests/session get/post function.
      raise_json_decode_errors=True.
  Returns:
    The  dict which is the json.loads() of the return.
      Error condition if JSON decoding fails:
        dict['code'] contains the code
          10000 is "good" (but the JSON still failed).
          204 indicates no return but without error which is also fine.
          Many other codes exist.
        dict['blob'] is the response text in cases where the JSON fail and raise_json is False.
  Raises:
    An Exception if Json fails and raise_json is True. Not all non-error returns are JSON thus the "blob" option.


************************************
Class BadResponseException
************************************

For when the network is not doing what it should.



Class attributes
--------------------

BadResponseException.Exception

************************************
Class HTTPAPIWrapper
************************************

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

.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.__init__:

HTTPAPIWrapper.__init__
---------------------------------------------------------------------------------------------------------------------
HTTPAPIWrapper.__init__(self, http_server_uri, email, password)


Initializes the HTTP API wrapper.
  Parameters:
    http_server_uri (str): The URI of the Moobius HTTP server.
    
    email (str): The email of the user.
    
    password (str): The password of the user.
    
    Example: 
    
    >>> http_api_wrapper = HTTPAPIWrapper("http: The //localhost:8080", "test@test", "test").
  Returns:
    (Class constructors have no explicit return value)
  Raises:
    (this function does not raise any errors of its own)


.. _moobius.network.http_api_wrapper.HTTPAPIWrapper._checked_get_or_post:

HTTPAPIWrapper._checked_get_or_post
---------------------------------------------------------------------------------------------------------------------
HTTPAPIWrapper._checked_get_or_post(self, url, the_request, is_post, requests_kwargs, good_message, bad_message, raise_errors)


Runs a GET or POST request returning the result as a JSON with optional logging and error raising.
  Parameters:
    url (str): The https://... url.
    
    the_request (dict): The "json" kwarg is set to this. Can be None in which no "json" will be set.
    
    is_post: The True for post, False for get.
    
    requests_kwargs=None: The Dict of extra arguments to send to requests/aiohttp. None is equivalent to {}.
    
    good_message=None: The string-valued message to logger.debug. None means do not log.
    
    bad_message="...": The string-valued message to prepend to logger.error if the response isnt code 10000.
    
    raise_errors=True: The Raise a BadResponseException if the request returns an error.
  Returns:
    The https response as a dict, using requests/aiohttp.post(...).json() to parse it.
  Raises:
    BadResponseException if raise_errors=True and the response is an error response.


.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.checked_get:

HTTPAPIWrapper.checked_get
---------------------------------------------------------------------------------------------------------------------
HTTPAPIWrapper.checked_get(self, url, the_request, requests_kwargs, good_message, bad_message, raise_errors)


Calls self._checked_get_or_post with is_post=False..
  Parameters:
    url: The url.
    
    the_request: The request itself.
    
    requests_kwargs: The kwargs for the request.
    
    good_message: The message to print on a happy 200.
    
    bad_message: The message to print on a sad non-200.
    
    raise_errors: Whether to raise errors if sad.
  Returns:
    The response. Raises a BadResponseException if it fails and raise_errors is set.
  Raises:
    (this function does not raise any errors of its own)


.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.checked_post:

HTTPAPIWrapper.checked_post
---------------------------------------------------------------------------------------------------------------------
HTTPAPIWrapper.checked_post(self, url, the_request, requests_kwargs, good_message, bad_message, raise_errors)


Calls self._checked_get_or_post with is_post=True..
  Parameters:
    url: The url.
    
    the_request: The request itself.
    
    requests_kwargs: The kwargs for the request.
    
    good_message: The message to print on a happy 200.
    
    bad_message: The message to print on a sad non-200.
    
    raise_errors: Whether to raise errors if sad.
  Returns:
    The response. Raises a BadResponseException if it fails and raise_errors is set.
  Raises:
    (this function does not raise any errors of its own)


.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.headers:

HTTPAPIWrapper.headers
---------------------------------------------------------------------------------------------------------------------
HTTPAPIWrapper.headers(self)



  Parameters:
    (No parameters in this class constructor)
  Returns:
    The authentication headers. Used for all API calls except for authenticate() and refresh().
    headers["Auth-Origin"] is the authentication service, such as "cognito".
    headers["Authorization"] is the access token, etc that proves authentication.
  Raises:
    (this function does not raise any errors of its own)


.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.authenticate:

HTTPAPIWrapper.authenticate
---------------------------------------------------------------------------------------------------------------------
HTTPAPIWrapper.authenticate(self)


Authenticates using self.username andself.password. Needs to be called before any other API calls.
  Parameters:
    (No parameters in this class constructor)
  Returns:
    (the access token, the refresh token).
    Raises an Exception if doesn't receive a valid response.
    Like most GET and POST functions it will raise any errors thrown by the http API.
  Raises:
    (this function does not raise any errors of its own)


.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.sign_up:

HTTPAPIWrapper.sign_up
---------------------------------------------------------------------------------------------------------------------
HTTPAPIWrapper.sign_up(self)


Signs up.
  Parameters:
    (No parameters in this class constructor)
  Returns:
    (the access token, the refresh token).
  Raises:
    (this function does not raise any errors of its own)


.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.sign_out:

HTTPAPIWrapper.sign_out
---------------------------------------------------------------------------------------------------------------------
HTTPAPIWrapper.sign_out(self)


Signs out using the access token obtained from signing in.
  Parameters:
    (No parameters in this class constructor)
  Returns:
    The None.
  Raises:
    (this function does not raise any errors of its own)


.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.refresh:

HTTPAPIWrapper.refresh
---------------------------------------------------------------------------------------------------------------------
HTTPAPIWrapper.refresh(self)


Refreshes the access token,.
  Parameters:
    (No parameters in this class constructor)
  Returns:
    The it.
  Raises:
    (this function does not raise any errors of its own)


.. _moobius.network.http_api_wrapper.HTTPAPIWrapper._xtract_character:

HTTPAPIWrapper._xtract_character
---------------------------------------------------------------------------------------------------------------------
HTTPAPIWrapper._xtract_character(self, resp_data)



  Parameters:
    resp_data: The JSON response data.
  Returns:
    The  Character object.
  Raises:
    (this function does not raise any errors of its own)


.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.fetch_character_profile:

HTTPAPIWrapper.fetch_character_profile
---------------------------------------------------------------------------------------------------------------------
HTTPAPIWrapper.fetch_character_profile(self, character_id)



  Parameters:
    character_id: The string-valued (or list-valued) character_id.
  Returns:
    The  Character object (or list therof),
    It works for both member_ids and puppet_ids.
  Raises:
    (this function does not raise any errors of its own)


.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.fetch_member_ids:

HTTPAPIWrapper.fetch_member_ids
---------------------------------------------------------------------------------------------------------------------
HTTPAPIWrapper.fetch_member_ids(self, channel_id, service_id, raise_empty_list_err)


Fetches the member ids of a channel which coorespond to real users.
  Parameters:
    channel_id (str): The channel ID.
    
    service_id (str): The service/client/agent ID.
    
    raise_empty_list_err=False: The Raises an Exception if the list is empty.
  Returns:
    The  list of character_id strings.
  Raises:
    An Exception (empty list) if raise_empty_list_err is True and the list is empty.


.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.fetch_puppets:

HTTPAPIWrapper.fetch_puppets
---------------------------------------------------------------------------------------------------------------------
HTTPAPIWrapper.fetch_puppets(self, service_id)



  Parameters:
    service_id: The service ID.
  Returns:
    The  list of Character objects bound to this service.
  Raises:
    (this function does not raise any errors of its own)


.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.fetch_user_info:

HTTPAPIWrapper.fetch_user_info
---------------------------------------------------------------------------------------------------------------------
HTTPAPIWrapper.fetch_user_info(self)



  Parameters:
    (No parameters in this class constructor)
  Returns:
    The UserInfo of the user logged in as, containing thier name, avatar, etc. Used by agents.
  Raises:
    (this function does not raise any errors of its own)


.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.update_current_user:

HTTPAPIWrapper.update_current_user
---------------------------------------------------------------------------------------------------------------------
HTTPAPIWrapper.update_current_user(self, avatar, description, name)


Updates the user info. Used by agents.
  Parameters:
    avatar: The Link to image or local filepath to upload.
    
    description: The Of the user.
    
    name: The name that shows in chat.
  Returns:
    The None.
  Raises:
    (this function does not raise any errors of its own)


.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.create_service:

HTTPAPIWrapper.create_service
---------------------------------------------------------------------------------------------------------------------
HTTPAPIWrapper.create_service(self, description)


Creates and.
  Parameters:
    description: The description string.
  Returns:
    The string-valued service_id.
    Called once by the Moobius class if there is no service specified.
  Raises:
    (this function does not raise any errors of its own)


.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.fetch_service_id_list:

HTTPAPIWrapper.fetch_service_id_list
---------------------------------------------------------------------------------------------------------------------
HTTPAPIWrapper.fetch_service_id_list(self)



  Parameters:
    (No parameters in this class constructor)
  Returns:
    The  list of service_id strings of the user.
  Raises:
    (this function does not raise any errors of its own)


.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.create_puppet:

HTTPAPIWrapper.create_puppet
---------------------------------------------------------------------------------------------------------------------
HTTPAPIWrapper.create_puppet(self, service_id, name, avatar, description)


Creates a character with a given name, avatar, and description.
The created user will be bound to the given service.
  Parameters:
    service_id (str): The service_id/client_id.
    
    name (str): The name of the user.
    
    avatar (str): The image URL of the user's picture OR a local file path.
    
    description (str): The description of the user.
  Returns:
    The  Character object representing the created user.
  Raises:
    (this function does not raise any errors of its own)


.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.update_puppet:

HTTPAPIWrapper.update_puppet
---------------------------------------------------------------------------------------------------------------------
HTTPAPIWrapper.update_puppet(self, service_id, character_id, avatar, description, name)


Updates the characters name, avatar, etc for a FAKE user, for real users use update_current_user.
  Parameters:
    service_id (str): The Which service holds the user.
    
    character_id (str): The Who to update. Can also be a Character object. Cannot be a list.
    
    avatar (str): The  link to user's image or a local filepath to upload.
    
    description (str): The description of user.
    
    name (str): The name that will show in chat.
  Returns:
    The Data about the user as a dict.
  Raises:
    (this function does not raise any errors of its own)


.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.create_channel:

HTTPAPIWrapper.create_channel
---------------------------------------------------------------------------------------------------------------------
HTTPAPIWrapper.create_channel(self, channel_name, channel_desc)


Creates a channel.
  Parameters:
    channel_name: The string-valued channel name.
    
    channel_desc: The description.
  Returns:
    The channel_id.
    Example ID: "13e44ea3-b559-45af-9106-6aa92501d4ed".
  Raises:
    (this function does not raise any errors of its own)


.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.bind_service_to_channel:

HTTPAPIWrapper.bind_service_to_channel
---------------------------------------------------------------------------------------------------------------------
HTTPAPIWrapper.bind_service_to_channel(self, service_id, channel_id)


Binds a service to a channel.
This function is unusual in that it.
  Parameters:
    service_id: The service.
    
    channel_id: The channel IDs.
  Returns:
    Whether it was sucessful rather than raising errors if it fails.
  Raises:
    (this function does not raise any errors of its own)


.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.unbind_service_from_channel:

HTTPAPIWrapper.unbind_service_from_channel
---------------------------------------------------------------------------------------------------------------------
HTTPAPIWrapper.unbind_service_from_channel(self, service_id, channel_id)


Unbinds a service to a channel.
  Parameters:
    service_id: The service.
    
    channel_id: The channel IDs.
  Returns:
    The None.
  Raises:
    (this function does not raise any errors of its own)


.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.update_channel:

HTTPAPIWrapper.update_channel
---------------------------------------------------------------------------------------------------------------------
HTTPAPIWrapper.update_channel(self, channel_id, channel_name, channel_desc)


Updates the name and desc of a channel.
  Parameters:
    channel_id (str): The Which channel to update.
    
    channel_name (str): The new channel name.
    
    channel_desc (str): The new channel description.
  Returns:
    The None.
  Raises:
    (this function does not raise any errors of its own)


.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.fetch_popular_channels:

HTTPAPIWrapper.fetch_popular_channels
---------------------------------------------------------------------------------------------------------------------
HTTPAPIWrapper.fetch_popular_channels(self)


Fetches the popular channels,.
  Parameters:
    (No parameters in this class constructor)
  Returns:
    The  list of channel_id strings.
  Raises:
    (this function does not raise any errors of its own)


.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.fetch_channel_list:

HTTPAPIWrapper.fetch_channel_list
---------------------------------------------------------------------------------------------------------------------
HTTPAPIWrapper.fetch_channel_list(self)


Fetches all? channels,.
  Parameters:
    (No parameters in this class constructor)
  Returns:
    The  list of channel_id strings.
  Raises:
    (this function does not raise any errors of its own)


.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.fetch_message_history:

HTTPAPIWrapper.fetch_message_history
---------------------------------------------------------------------------------------------------------------------
HTTPAPIWrapper.fetch_message_history(self, channel_id, limit, before)


Returns the message chat history.
  Parameters:
    channel_id (str): The Channel with the messages inside of it.
    
    limit=64: The Max number of messages to return (messages further back in time, if any, will not be returned).
    
    before="null": The Only return messages older than this.
  Returns:
    The  list of dicts.
  Raises:
    (this function does not raise any errors of its own)


.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.this_user_channels:

HTTPAPIWrapper.this_user_channels
---------------------------------------------------------------------------------------------------------------------
HTTPAPIWrapper.this_user_channels(self)



  Parameters:
    (No parameters in this class constructor)
  Returns:
    The list of channel_ids this user is in.
  Raises:
    (this function does not raise any errors of its own)


.. _moobius.network.http_api_wrapper.HTTPAPIWrapper._upload_extension:

HTTPAPIWrapper._upload_extension
---------------------------------------------------------------------------------------------------------------------
HTTPAPIWrapper._upload_extension(self, extension)


Gets the upload URL and needed fields for uploading a file.
  Parameters:
    extension: The string-valued extension.
  Returns:
    (upload_url or None, upload_fields).
  Raises:
    (this function does not raise any errors of its own)


.. _moobius.network.http_api_wrapper.HTTPAPIWrapper._do_upload:

HTTPAPIWrapper._do_upload
---------------------------------------------------------------------------------------------------------------------
HTTPAPIWrapper._do_upload(self, upload_url, upload_fields, file_path)


Uploads a file to the given upload URL with the given upload fields.
  Parameters:
    upload_url (str): The obtained with _upload_extension.
    
    upload_fields (dict): The obtained with _upload_extension.
    
    file_path (str): The path of the file.
  Returns:
    The full URL string of the uploaded file. None if doesn't receive a valid response (error condition).
  Raises:
    Exception: If the file upload fails, this function will raise an exception detailing the error.


.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.upload:

HTTPAPIWrapper.upload
---------------------------------------------------------------------------------------------------------------------
HTTPAPIWrapper.upload(self, file_path)


Uploads the file at local path file_path to the Moobius server. Automatically calculates the upload URL and upload fields.
  Parameters:
    file_path: The file_path.
  Returns:
    The uploaded URL. Raises an Exception if the upload fails.
  Raises:
    (this function does not raise any errors of its own)


.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.convert_to_url:

HTTPAPIWrapper.convert_to_url
---------------------------------------------------------------------------------------------------------------------
HTTPAPIWrapper.convert_to_url(self, file_path)


Uploads and.
  Parameters:
    file_path: The file_path.
  Returns:
    The bucket's url. Idempotent: If given a URL will just return the URL.
    Empty, False, or None strings are converted to a default URL.
  Raises:
    (this function does not raise any errors of its own)


.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.download:

HTTPAPIWrapper.download
---------------------------------------------------------------------------------------------------------------------
HTTPAPIWrapper.download(self, source, fullpath, auto_dir, overwrite, bytes, headers)


Downloads a file from a url or other source to a local filename, automatically creating dirs if need be.
  Parameters:
    url: The url to download the file from.
    
    fullpath=None: The filepath to download to.
        None will create a file based on the timestamp + random numbers.
        If no extension is specified, will infer the extension from the url if one exists.
    
    auto_dir=None: The If no fullpath is specified, a folder must be choosen.
        Defaults to './downloads'.
    
    overwrite=None: The llow overwriting pre-existing files. If False, will raise an Exception on name collision.
    
    bytes=None: The If True, will return bytes instead of saving a file.
    
    headers=None: The Optional headers. Use these for downloads that require auth.
        Can set to "self" to use the same auth headers that this instance is using.
  Returns:
    The bytes if bytes=True.
  Raises:
    (this function does not raise any errors of its own)


.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.fetch_channel_group_dict:

HTTPAPIWrapper.fetch_channel_group_dict
---------------------------------------------------------------------------------------------------------------------
HTTPAPIWrapper.fetch_channel_group_dict(self, channel_id, service_id)


Similar to fetch_member_ids..
  Parameters:
    channel_id: The channel_id.
    
    service_id: The service_id.
  Returns:
    The  dict from each group_id to all characters.
  Raises:
    (this function does not raise any errors of its own)


.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.fetch_channel_group_list:

HTTPAPIWrapper.fetch_channel_group_list
---------------------------------------------------------------------------------------------------------------------
HTTPAPIWrapper.fetch_channel_group_list(self, channel_id, service_id)


Similar to fetch_channel_group_dict..
  Parameters:
    channel_id: The channel_id.
    
    service_id: The service_id.
  Returns:
    The raw data.
  Raises:
    (this function does not raise any errors of its own)


.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.create_channel_group:

HTTPAPIWrapper.create_channel_group
---------------------------------------------------------------------------------------------------------------------
HTTPAPIWrapper.create_channel_group(self, channel_id, group_name, character_ids)


Creates a channel group.
  Parameters:
    channel_id (str): The id of the group leader?.
    
    group_name (str): The What to call it.
    
    characters (list): The  list of channel_id strings that will be inside the group.
  Returns:
    The group_id string.
  Raises:
    (this function does not raise any errors of its own)


.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.character_ids_of_service_group:

HTTPAPIWrapper.character_ids_of_service_group
---------------------------------------------------------------------------------------------------------------------
HTTPAPIWrapper.character_ids_of_service_group(self, group_id)



  Parameters:
    group_id: The group_id.
  Returns:
    The  list of character ids belonging to a service group.
    Note that the 'recipients' in 'on message up' might be None:
      To avoid requiring checks for None this function will return an empty list given Falsey inputs or Falsey string literals.
  Raises:
    (this function does not raise any errors of its own)


.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.character_ids_of_channel_group:

HTTPAPIWrapper.character_ids_of_channel_group
---------------------------------------------------------------------------------------------------------------------
HTTPAPIWrapper.character_ids_of_channel_group(self, sender_id, channel_id, group_id)


Gets a list of character ids belonging to a channel group.
Websocket payloads contain these channel_groups which are shorthand for a list of characters.
  Parameters:
    sender_id: The message's sender.
    
    channel_id: The message specified that it was sent in this channel.
    
    group_id: The messages recipients.
  Returns:
    The character_id list.
  Raises:
    (this function does not raise any errors of its own)


.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.create_service_group:

HTTPAPIWrapper.create_service_group
---------------------------------------------------------------------------------------------------------------------
HTTPAPIWrapper.create_service_group(self, character_ids)


Creates a group containing the list of characters_ids and returns this Group object.
This group can then be used in send_message_down payloads.
  Parameters:
    group_name (str): The What to call it.
    
    character_ids (list): The  list of character_id strings or Characters that will be inside the group.
  Returns:
    The  Group object.
  Raises:
    (this function does not raise any errors of its own)


.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.update_channel_group:

HTTPAPIWrapper.update_channel_group
---------------------------------------------------------------------------------------------------------------------
HTTPAPIWrapper.update_channel_group(self, channel_id, group_id, members)


Updates a channel group.
  Parameters:
    channel_id (str): The id of the group leader?.
    
    group_name (str): The What to call it.
    
    members (list): The  list of character_id strings that will be inside the group.
  Returns:
    The None.
  Raises:
    (this function does not raise any errors of its own)


.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.update_temp_channel_group:

HTTPAPIWrapper.update_temp_channel_group
---------------------------------------------------------------------------------------------------------------------
HTTPAPIWrapper.update_temp_channel_group(self, channel_id, members)


Updates a channel TEMP group.
  Parameters:
    channel_id (str): The id of the group leader?.
    
    members (list): The  list of character_id strings that will be inside the group.
  Returns:
    The None.
  Raises:
    (this function does not raise any errors of its own)


.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.fetch_channel_temp_group:

HTTPAPIWrapper.fetch_channel_temp_group
---------------------------------------------------------------------------------------------------------------------
HTTPAPIWrapper.fetch_channel_temp_group(self, channel_id, service_id)


Like fetch_channel_group_list but for TEMP groups..
  Parameters:
    channel_id: The channel_id.
    
    service_id: The service_id,.
  Returns:
    The list of groups.
  Raises:
    (this function does not raise any errors of its own)


.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.fetch_user_from_group:

HTTPAPIWrapper.fetch_user_from_group
---------------------------------------------------------------------------------------------------------------------
HTTPAPIWrapper.fetch_user_from_group(self, user_id, channel_id, group_id)


Not yet implemented!
Fetches the user profile of a user from a group.
  Parameters:
    user_id (str): The user ID.
    
    channel_id (str): The channel ID. (TODO: of what?).
    
    group_id (str): The group ID.
  Returns:
    The user profile Character object.
  Raises:
    (this function does not raise any errors of its own)


.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.fetch_target_group:

HTTPAPIWrapper.fetch_target_group
---------------------------------------------------------------------------------------------------------------------
HTTPAPIWrapper.fetch_target_group(self, user_id, channel_id, group_id)


Not yet implemented!
Fetches info about the group.
  Parameters:
    user_id (str), channel_id (str): The why needed?.
    
    group_id (str): The Which group to fetch.
  Returns:
    The data-dict data.
  Raises:
    (this function does not raise any errors of its own)


.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.__str__:

HTTPAPIWrapper.__str__
---------------------------------------------------------------------------------------------------------------------
HTTPAPIWrapper.__str__(self)


The string output function for debugging.
  Parameters:
    (No parameters in this class constructor)
  Returns:
    The  easy-to-read string summary.
  Raises:
    (this function does not raise any errors of its own)


.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.__repr__:

HTTPAPIWrapper.__repr__
---------------------------------------------------------------------------------------------------------------------
HTTPAPIWrapper.__repr__(self)


The string output function for debugging.
  Parameters:
    (No parameters in this class constructor)
  Returns:
    The  easy-to-read string summary.
  Raises:
    (this function does not raise any errors of its own)


Class attributes
--------------------


