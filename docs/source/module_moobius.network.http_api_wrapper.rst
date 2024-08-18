.. _moobius_network_http_api_wrapper:

###################################################################################
moobius.network.http_api_wrapper
###################################################################################

******************************
Module-level functions
******************************

.. _moobius.network.http_api_wrapper.get_or_post:

get_or_post
---------------------------------------------------------------------------------------------------------------------

Sends a GET or POST request and awaits for the response.

* Signature

    * get_or_post(url, is_post, requests_kwargs, raise_json_decode_errors)

* Parameters

    * url: Https://...
    
    * is_post: False for GET, True for POST.
    
    * requests_kwargs=None: These are fed into the requests/session get/post function.
    
    * raise_json_decode_errors=True: Raise errors parsing the JSON that the request sends back, otherwise return the error as a dict.

* Returns

  * The  dict which is the json.loads() of the return.
    Error condition if JSON decoding fails:
      dict['code'] contains the code
        10000 is "good" (but the JSON still failed).
        204 indicates no return but without error which is also fine.
        Many other codes exist.
      dict['blob'] is the response text in cases where the JSON fail and raise_json is False.

* Raises

  * An Exception if Json fails and raise_json is True. Not all non-error returns are JSON thus the "blob" option.

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

Initializes the HTTP API wrapper.

* Signature

    * HTTPAPIWrapper.__init__(self, http_server_uri, email, password)

* Parameters

    * http_server_uri='': The URI of the Moobius HTTP server.
    
    * email='': The email of the user.
    
    * password='': The password of the user.

* Returns

  * (Class constructors have no explicit return value)

* Raises

  * (this function does not raise any notable errors)

* Example

    >>> http_api_wrapper = HTTPAPIWrapper("http://localhost:8080", "test@test", "test")

.. _moobius.network.http_api_wrapper.HTTPAPIWrapper._checked_get_or_post:

HTTPAPIWrapper._checked_get_or_post
---------------------------------------------------------------------------------------------------------------------

Runs a GET or POST request returning the result as a JSON with optional logging and error raising.

* Signature

    * HTTPAPIWrapper._checked_get_or_post(self, url, the_request, is_post, requests_kwargs, good_message, bad_message, raise_errors)

* Parameters

    * url: The https://... url.
    
    * the_request: The "json" kwarg is set to this. Can be None in which no "json" will be set.
    
    * is_post: True for post, False for get.
    
    * requests_kwargs=None: Dict of extra arguments to send to requests/aiohttp. None is equivalent to {}.
    
    * good_message=None: The string-valued message to logger.debug. None means do not log.
    
    * bad_message='This HTTPs request failed': The string-valued message to prepend to logger.error if the response isnt code 10000.
    
    * raise_errors=True: Raise a BadResponseException if the request returns an error.

* Returns

  * The https response as a dict, using requests/aiohttp.post(...).json() to parse it.

* Raises

  * BadResponseException if raise_errors=True and the response is an error response.

.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.checked_get:

HTTPAPIWrapper.checked_get
---------------------------------------------------------------------------------------------------------------------

Calls self._checked_get_or_post with is_post=False..

* Signature

    * HTTPAPIWrapper.checked_get(self, url, the_request, requests_kwargs, good_message, bad_message, raise_errors)

* Parameters

    * url: Url.
    
    * the_request: The request itself.
    
    * requests_kwargs=None: The kwargs for the request.
    
    * good_message=None: The message to print on a happy 200.
    
    * bad_message='This HTTPs GET request failed': The message to print on a sad non-200.
    
    * raise_errors=True: Whether to raise errors if sad.

* Returns

  * The response. Raises a BadResponseException if it fails and raise_errors is set.

* Raises

  * (this function does not raise any notable errors)

.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.checked_post:

HTTPAPIWrapper.checked_post
---------------------------------------------------------------------------------------------------------------------

Calls self._checked_get_or_post with is_post=True..

* Signature

    * HTTPAPIWrapper.checked_post(self, url, the_request, requests_kwargs, good_message, bad_message, raise_errors)

* Parameters

    * url: Url.
    
    * the_request: The request itself.
    
    * requests_kwargs=None: The kwargs for the request.
    
    * good_message=None: The message to print on a happy 200.
    
    * bad_message='This HTTPs POST request failed': The message to print on a sad non-200.
    
    * raise_errors=True: Whether to raise errors if sad.

* Returns

  * The response. Raises a BadResponseException if it fails and raise_errors is set.

* Raises

  * (this function does not raise any notable errors)

.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.headers:

HTTPAPIWrapper.headers
---------------------------------------------------------------------------------------------------------------------

* Signature

    * HTTPAPIWrapper.headers(self)

* Parameters

    * (this class constructor accepts no arguments)

* Returns

  * The authentication headers. Used for all API calls except for authenticate() and refresh().
  headers["Auth-Origin"] is the authentication service, such as "cognito".
  headers["Authorization"] is the access token, etc that proves authentication.

* Raises

  * (this function does not raise any notable errors)

.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.authenticate:

HTTPAPIWrapper.authenticate
---------------------------------------------------------------------------------------------------------------------

Authenticates using self.username andself.password. Needs to be called before any other API calls.

* Signature

    * HTTPAPIWrapper.authenticate(self)

* Parameters

    * (this class constructor accepts no arguments)

* Returns

  * (the access token, the refresh token).
  Raises an Exception if doesn't receive a valid response.
  Like most GET and POST functions it will raise any errors thrown by the http API.

* Raises

  * (this function does not raise any notable errors)

.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.sign_up:

HTTPAPIWrapper.sign_up
---------------------------------------------------------------------------------------------------------------------

Signs up.

* Signature

    * HTTPAPIWrapper.sign_up(self)

* Parameters

    * (this class constructor accepts no arguments)

* Returns

  * (the access token, the refresh token).

* Raises

  * (this function does not raise any notable errors)

.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.sign_out:

HTTPAPIWrapper.sign_out
---------------------------------------------------------------------------------------------------------------------

Signs out using the access token obtained from signing in.

* Signature

    * HTTPAPIWrapper.sign_out(self)

* Parameters

    * (this class constructor accepts no arguments)

* Returns

  * The None.

* Raises

  * (this function does not raise any notable errors)

.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.refresh:

HTTPAPIWrapper.refresh
---------------------------------------------------------------------------------------------------------------------

Refreshes the access token.

* Signature

    * HTTPAPIWrapper.refresh(self)

* Parameters

    * (this class constructor accepts no arguments)

* Returns

  * The new token.

* Raises

  * (this function does not raise any notable errors)

.. _moobius.network.http_api_wrapper.HTTPAPIWrapper._xtract_character:

HTTPAPIWrapper._xtract_character
---------------------------------------------------------------------------------------------------------------------

* Signature

    * HTTPAPIWrapper._xtract_character(self, resp_data)

* Parameters

    * resp_data: JSON response data.

* Returns

  * The  Character object.

* Raises

  * (this function does not raise any notable errors)

.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.fetch_character_profile:

HTTPAPIWrapper.fetch_character_profile
---------------------------------------------------------------------------------------------------------------------

* Signature

    * HTTPAPIWrapper.fetch_character_profile(self, character_id)

* Parameters

    * character_id: String-valued (or list-valued) character_id.

* Returns

  * The  Character object (or list therof),
  It works for both member_ids and agent_ids.

* Raises

  * (this function does not raise any notable errors)

.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.fetch_member_ids:

HTTPAPIWrapper.fetch_member_ids
---------------------------------------------------------------------------------------------------------------------

Fetches the member ids of a channel which coorespond to real users.

* Signature

    * HTTPAPIWrapper.fetch_member_ids(self, channel_id, service_id, raise_empty_list_err)

* Parameters

    * channel_id: The channel ID.
    
    * service_id: The service/client/user ID.
    
    * raise_empty_list_err=False: Raises an Exception if the list is empty.

* Returns

  * The  list of character_id strings.

* Raises

  * An Exception (empty list) if raise_empty_list_err is True and the list is empty.

.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.fetch_agents:

HTTPAPIWrapper.fetch_agents
---------------------------------------------------------------------------------------------------------------------

* Signature

    * HTTPAPIWrapper.fetch_agents(self, service_id)

* Parameters

    * service_id: Service ID.

* Returns

  * The  list of non-user Character objects bound to this service.

* Raises

  * (this function does not raise any notable errors)

.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.fetch_user_info:

HTTPAPIWrapper.fetch_user_info
---------------------------------------------------------------------------------------------------------------------

* Signature

    * HTTPAPIWrapper.fetch_user_info(self)

* Parameters

    * (this class constructor accepts no arguments)

* Returns

  * The UserInfo of the user logged in as, containing thier name, avatar, etc. Used by user mode.

* Raises

  * (this function does not raise any notable errors)

.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.update_current_user:

HTTPAPIWrapper.update_current_user
---------------------------------------------------------------------------------------------------------------------

Updates the user info. Used by user mode.

* Signature

    * HTTPAPIWrapper.update_current_user(self, avatar, description, name)

* Parameters

    * avatar: Link to image or local file_path to upload.
    
    * description: Of the user.
    
    * name: The name that shows in chat.

* Returns

  * The None.

* Raises

  * (this function does not raise any notable errors)

.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.create_service:

HTTPAPIWrapper.create_service
---------------------------------------------------------------------------------------------------------------------

Creates and.

* Signature

    * HTTPAPIWrapper.create_service(self, description)

* Parameters

    * description: Description string.

* Returns

  * The string-valued service_id.
  Called once by the Moobius class if there is no service specified.

* Raises

  * (this function does not raise any notable errors)

.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.fetch_service_id_list:

HTTPAPIWrapper.fetch_service_id_list
---------------------------------------------------------------------------------------------------------------------

* Signature

    * HTTPAPIWrapper.fetch_service_id_list(self)

* Parameters

    * (this class constructor accepts no arguments)

* Returns

  * The  list of service_id strings of the user.

* Raises

  * (this function does not raise any notable errors)

.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.create_agent:

HTTPAPIWrapper.create_agent
---------------------------------------------------------------------------------------------------------------------

Creates a character with a given name, avatar, and description.
The created user will be bound to the given service.

* Signature

    * HTTPAPIWrapper.create_agent(self, service_id, name, avatar, description)

* Parameters

    * service_id: The service_id/client_id.
    
    * name: The name of the user.
    
    * avatar: The image URL of the user's picture OR a local file path.
    
    * description: The description of the user.

* Returns

  * The  Character object representing the created user.

* Raises

  * (this function does not raise any notable errors)

.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.update_agent:

HTTPAPIWrapper.update_agent
---------------------------------------------------------------------------------------------------------------------

Updates the characters name, avatar, etc for a FAKE user, for real users use update_current_user.

* Signature

    * HTTPAPIWrapper.update_agent(self, service_id, agent_id, avatar, description, name)

* Parameters

    * service_id: Which service holds the user.
    
    * agent_id: Who to update. Can also be a Character object. Cannot be a list.
    
    * avatar: A link to user's image or a local file_path to upload.
    
    * description: The description of user.
    
    * name: The name that will show in chat.

* Returns

  * The Data about the user as a dict.

* Raises

  * (this function does not raise any notable errors)

.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.create_channel:

HTTPAPIWrapper.create_channel
---------------------------------------------------------------------------------------------------------------------

Creates a channel.

* Signature

    * HTTPAPIWrapper.create_channel(self, channel_name, channel_desc)

* Parameters

    * channel_name: String-valued channel name.
    
    * channel_desc: Description.

* Returns

  * The channel_id.
  Example ID: "13e44ea3-b559-45af-9106-6aa92501d4ed".

* Raises

  * (this function does not raise any notable errors)

.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.bind_service_to_channel:

HTTPAPIWrapper.bind_service_to_channel
---------------------------------------------------------------------------------------------------------------------

Binds a service to a channel.
This function is unusual in that it.

* Signature

    * HTTPAPIWrapper.bind_service_to_channel(self, service_id, channel_id)

* Parameters

    * service_id: Service.
    
    * channel_id: Channel IDs.

* Returns

  * Whether it was sucessful rather than raising errors if it fails.

* Raises

  * (this function does not raise any notable errors)

.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.unbind_service_from_channel:

HTTPAPIWrapper.unbind_service_from_channel
---------------------------------------------------------------------------------------------------------------------

Unbinds a service to a channel.

* Signature

    * HTTPAPIWrapper.unbind_service_from_channel(self, service_id, channel_id)

* Parameters

    * service_id: Service.
    
    * channel_id: Channel IDs.

* Returns

  * The None.

* Raises

  * (this function does not raise any notable errors)

.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.update_channel:

HTTPAPIWrapper.update_channel
---------------------------------------------------------------------------------------------------------------------

Updates the name and desc of a channel.

* Signature

    * HTTPAPIWrapper.update_channel(self, channel_id, channel_name, channel_desc)

* Parameters

    * channel_id: Which channel to update.
    
    * channel_name: The new channel name.
    
    * channel_desc: The new channel description.

* Returns

  * The None.

* Raises

  * (this function does not raise any notable errors)

.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.fetch_popular_channels:

HTTPAPIWrapper.fetch_popular_channels
---------------------------------------------------------------------------------------------------------------------

Fetches the popular channels,.

* Signature

    * HTTPAPIWrapper.fetch_popular_channels(self)

* Parameters

    * (this class constructor accepts no arguments)

* Returns

  * The  list of channel_id strings.

* Raises

  * (this function does not raise any notable errors)

.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.fetch_channel_list:

HTTPAPIWrapper.fetch_channel_list
---------------------------------------------------------------------------------------------------------------------

Fetches all? channels,.

* Signature

    * HTTPAPIWrapper.fetch_channel_list(self)

* Parameters

    * (this class constructor accepts no arguments)

* Returns

  * The  list of channel_id strings.

* Raises

  * (this function does not raise any notable errors)

.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.fetch_message_history:

HTTPAPIWrapper.fetch_message_history
---------------------------------------------------------------------------------------------------------------------

Returns the message chat history.

* Signature

    * HTTPAPIWrapper.fetch_message_history(self, channel_id, limit, before)

* Parameters

    * channel_id: Channel with the messages inside of it.
    
    * limit=64: Max number of messages to return (messages further back in time, if any, will not be returned).
    
    * before='null': Only return messages older than this.

* Returns

  * The  list of dicts.

* Raises

  * (this function does not raise any notable errors)

.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.this_user_channels:

HTTPAPIWrapper.this_user_channels
---------------------------------------------------------------------------------------------------------------------

* Signature

    * HTTPAPIWrapper.this_user_channels(self)

* Parameters

    * (this class constructor accepts no arguments)

* Returns

  * The list of channel_ids this user is in.

* Raises

  * (this function does not raise any notable errors)

.. _moobius.network.http_api_wrapper.HTTPAPIWrapper._upload_extension:

HTTPAPIWrapper._upload_extension
---------------------------------------------------------------------------------------------------------------------

Gets the upload URL and needed fields for uploading a file.

* Signature

    * HTTPAPIWrapper._upload_extension(self, extension)

* Parameters

    * extension: String-valued extension.

* Returns

  * (upload_url or None, upload_fields).

* Raises

  * (this function does not raise any notable errors)

.. _moobius.network.http_api_wrapper.HTTPAPIWrapper._do_upload:

HTTPAPIWrapper._do_upload
---------------------------------------------------------------------------------------------------------------------

Uploads a file to the given upload URL with the given upload fields.

* Signature

    * HTTPAPIWrapper._do_upload(self, upload_url, upload_fields, file_path)

* Parameters

    * upload_url: Obtained with _upload_extension.
    
    * upload_fields: Obtained with _upload_extension.
    
    * file_path: The path of the file.

* Returns

  * The full URL string of the uploaded file. None if doesn't receive a valid response (error condition).

* Raises

  * Exception: If the file upload fails, this function will raise an exception detailing the error.

.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.upload:

HTTPAPIWrapper.upload
---------------------------------------------------------------------------------------------------------------------

Uploads the file at local path file_path to the Moobius server. Automatically calculates the upload URL and upload fields.

* Signature

    * HTTPAPIWrapper.upload(self, file_path)

* Parameters

    * file_path: File_path.

* Returns

  * The uploaded URL. Raises an Exception if the upload fails.

* Raises

  * (this function does not raise any notable errors)

.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.convert_to_url:

HTTPAPIWrapper.convert_to_url
---------------------------------------------------------------------------------------------------------------------

Uploads and.

* Signature

    * HTTPAPIWrapper.convert_to_url(self, file_path)

* Parameters

    * file_path: File_path.

* Returns

  * The bucket's url. Idempotent: If given a URL will just return the URL.
  Empty, False, or None strings are converted to a default URL.

* Raises

  * (this function does not raise any notable errors)

.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.download:

HTTPAPIWrapper.download
---------------------------------------------------------------------------------------------------------------------

Downloads a file from a url or other source to a local filename, automatically creating dirs if need be.

* Signature

    * HTTPAPIWrapper.download(self, source, full_path, auto_dir, overwrite, bytes, headers)

* Parameters

    * source: The url to download the file from.
    
    * full_path=None: The file_path to download to.
        None will create a file based on the timestamp + random numbers.
        If no extension is specified, will infer the extension from the url if one exists.
    
    * auto_dir=None: If no full_path is specified, a folder must be choosen.
        Defaults to './downloads'.
    
    * overwrite=None: Allow overwriting pre-existing files. If False, will raise an Exception on name collision.
    
    * bytes=None: If True, will return bytes instead of saving a file.
    
    * headers=None: Optional headers. Use these for downloads that require auth.
        Can set to "self" to use the same auth headers that this instance is using.

* Returns

  * The bytes if bytes=True.

* Raises

  * (this function does not raise any notable errors)

.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.fetch_channel_group_dict:

HTTPAPIWrapper.fetch_channel_group_dict
---------------------------------------------------------------------------------------------------------------------

Similar to fetch_member_ids..

* Signature

    * HTTPAPIWrapper.fetch_channel_group_dict(self, channel_id, service_id)

* Parameters

    * channel_id: Channel_id.
    
    * service_id: Service_id.

* Returns

  * The  dict from each group_id to all characters.

* Raises

  * (this function does not raise any notable errors)

.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.fetch_channel_group_list:

HTTPAPIWrapper.fetch_channel_group_list
---------------------------------------------------------------------------------------------------------------------

Similar to fetch_channel_group_dict..

* Signature

    * HTTPAPIWrapper.fetch_channel_group_list(self, channel_id, service_id)

* Parameters

    * channel_id: Channel_id.
    
    * service_id: Service_id.

* Returns

  * The raw data.

* Raises

  * (this function does not raise any notable errors)

.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.create_channel_group:

HTTPAPIWrapper.create_channel_group
---------------------------------------------------------------------------------------------------------------------

Creates a channel group.

* Signature

    * HTTPAPIWrapper.create_channel_group(self, channel_id, group_name, members)

* Parameters

    * channel_id: The id of the group leader?.
    
    * group_name: What to call it.
    
    * members: A list of character_id strings that will be inside the group.

* Returns

  * The group_id string.

* Raises

  * (this function does not raise any notable errors)

.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.character_ids_of_service_group:

HTTPAPIWrapper.character_ids_of_service_group
---------------------------------------------------------------------------------------------------------------------

* Signature

    * HTTPAPIWrapper.character_ids_of_service_group(self, group_id)

* Parameters

    * group_id: Group_id.

* Returns

  * The  list of character ids belonging to a service group.
  Note that the 'recipients' in 'on message up' might be None:
    To avoid requiring checks for None this function will return an empty list given Falsey inputs or Falsey string literals.

* Raises

  * (this function does not raise any notable errors)

.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.character_ids_of_channel_group:

HTTPAPIWrapper.character_ids_of_channel_group
---------------------------------------------------------------------------------------------------------------------

Gets a list of character ids belonging to a channel group.
Websocket payloads contain these channel_groups which are shorthand for a list of characters.

* Signature

    * HTTPAPIWrapper.character_ids_of_channel_group(self, sender_id, channel_id, group_id)

* Parameters

    * sender_id: The message's sender.
    
    * channel_id: The message specified that it was sent in this channel.
    
    * group_id: The messages recipients.

* Returns

  * The character_id list.

* Raises

  * (this function does not raise any notable errors)

.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.create_service_group:

HTTPAPIWrapper.create_service_group
---------------------------------------------------------------------------------------------------------------------

Creates a group containing the list of characters_ids and returns this Group object.
This group can then be used in send_message_down payloads.

* Signature

    * HTTPAPIWrapper.create_service_group(self, members)

* Parameters

    * members: A list of character_id strings or Characters that will be inside the group.

* Returns

  * The  Group object.

* Raises

  * (this function does not raise any notable errors)

.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.update_channel_group:

HTTPAPIWrapper.update_channel_group
---------------------------------------------------------------------------------------------------------------------

Updates a channel group.

* Signature

    * HTTPAPIWrapper.update_channel_group(self, channel_id, group_id, members)

* Parameters

    * channel_id: The id of the group leader?.
    
    * group_id: What to call it.
    
    * members: A list of character_id strings that will be inside the group.

* Returns

  * The None.

* Raises

  * An Exception because it is unused, unimplemented, and may be removed.

.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.update_temp_channel_group:

HTTPAPIWrapper.update_temp_channel_group
---------------------------------------------------------------------------------------------------------------------

Updates a channel TEMP group.

* Signature

    * HTTPAPIWrapper.update_temp_channel_group(self, channel_id, members)

* Parameters

    * channel_id: The id of the group leader?.
    
    * members: A list of character_id strings that will be inside the group.

* Returns

  * The None.

* Raises

  * An Exception because it is unused, unimplemented, and may be removed.

.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.fetch_channel_temp_group:

HTTPAPIWrapper.fetch_channel_temp_group
---------------------------------------------------------------------------------------------------------------------

Like fetch_channel_group_list but for TEMP groups..

* Signature

    * HTTPAPIWrapper.fetch_channel_temp_group(self, channel_id, service_id)

* Parameters

    * channel_id: Channel_id.
    
    * service_id: Service_id,.

* Returns

  * The list of groups.

* Raises

  * (this function does not raise any notable errors)

.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.fetch_user_from_group:

HTTPAPIWrapper.fetch_user_from_group
---------------------------------------------------------------------------------------------------------------------

Not yet implemented!
Fetches the user profile of a user from a group.

* Signature

    * HTTPAPIWrapper.fetch_user_from_group(self, user_id, channel_id, group_id)

* Parameters

    * user_id: The user ID.
    
    * channel_id: The channel ID. (TODO: of what?).
    
    * group_id: The group ID.

* Returns

  * The user profile Character object.

* Raises

  * An Exception because it is unused, unimplemented, and may be removed.

.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.fetch_target_group:

HTTPAPIWrapper.fetch_target_group
---------------------------------------------------------------------------------------------------------------------

Not yet implemented!
Fetches info about the group.

* Signature

    * HTTPAPIWrapper.fetch_target_group(self, user_id, channel_id, group_id)

* Parameters

    * user_id: The user id of the user bieng fetched (is this needed?).
    
    * channel_id: The channel_id of the channel bieng fetched.
    
    * group_id: Which group to fetch.

* Returns

  * The data-dict data.

* Raises

  * An Exception because it is unused, unimplemented, and may be removed.

.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.__str__:

HTTPAPIWrapper.__str__
---------------------------------------------------------------------------------------------------------------------

The string output function for debugging.

* Signature

    * HTTPAPIWrapper.__str__(self)

* Parameters

    * (this class constructor accepts no arguments)

* Returns

  * The  easy-to-read string summary.

* Raises

  * (this function does not raise any notable errors)

.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.__repr__:

HTTPAPIWrapper.__repr__
---------------------------------------------------------------------------------------------------------------------

The string output function for debugging.

* Signature

    * HTTPAPIWrapper.__repr__(self)

* Parameters

    * (this class constructor accepts no arguments)

* Returns

  * The  easy-to-read string summary.

* Raises

  * (this function does not raise any notable errors)

Class attributes
--------------------


