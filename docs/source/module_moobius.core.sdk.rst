.. _moobius_core_sdk:

###################################################################################
moobius.core.sdk
###################################################################################

******************************
Module-level functions
******************************

.. _moobius.core.sdk._deprecated_wrap:

_deprecated_wrap
---------------------------------------------------------------------------------------------------------------------
_deprecated_wrap(f, old_name, new_name)

  Parameters:
    f: The function.
    old_name: The  deprecated old name.
    new_name: The  new name.
  Returns:
    The function with a deprecation logger warning.
  Raises:
    (this function does not raise any notable errors)

************************************
Class ServiceGroupLib
************************************

(This class is for internal use)
Converts a list of character_ids into a service or channel group id, creating one if need be.
   The lookup is O(n) so performance at extremly large list sizes may require optimizations.

.. _moobius.core.sdk.ServiceGroupLib.__init__:

ServiceGroupLib.__init__
---------------------------------------------------------------------------------------------------------------------
ServiceGroupLib.__init__(self)

Creates an empty ServiceGroupLib instance.
  Parameters:
    (No parameters in this class constructor)
  Returns:
    (Class constructors have no explicit return value)
  Raises:
    (this function does not raise any notable errors)

.. _moobius.core.sdk.ServiceGroupLib.convert_list:

ServiceGroupLib.convert_list
---------------------------------------------------------------------------------------------------------------------
ServiceGroupLib.convert_list(self, http_api, character_ids, is_message_down, channel_id)

Converts a list to single group id, unless it is already a group id.
  Parameters:
    http_api: The http_api client in Moobius.
    character_ids: The List of ids. If a string, treated as a one element list.
    is_message_down: The True = message_down (a message sent from the service), False = message_up (a message sent from a user).
    channel_id=None: The If None and the conversion still needs to happen it will raise an Exception.
  Returns:
    The group id.
  Raises:
    (this function does not raise any notable errors)

Class attributes
--------------------



************************************
Class Moobius
************************************

<no class docstring>

.. _moobius.core.sdk.Moobius.__init__:

Moobius.__init__
---------------------------------------------------------------------------------------------------------------------
Moobius.__init__(self, config_path, db_config_path, service_mode, \*kwargs)

Initializes a service object, can do so in "user mode" where it acts like a user.
  Parameters:
    config_path: The path of the service config file.
        Can instead be a dict of the actual config, so that no file is loaded.
    db_config_path=None: The optional path of the database config file.
        Can also be a dict instead of a file.
    service_mode=True: The True is the default for services. False is "user_mode" where we can simulate bieng an end-user.
    Example: The >>> service = SDK(config_path="./config/service.json", db_config_path="./config/database.json", service_mode=True).
  Returns:
    (Class constructors have no explicit return value)
  Raises:
    (this function does not raise any notable errors)

.. _moobius.core.sdk.Moobius.start:

Moobius.start
---------------------------------------------------------------------------------------------------------------------
Moobius.start(self)

Starts the service and calls start() fns are called with wand.run. There are 6 steps:
  1. Authenticate.
  2. Connect to the websocket server.
  3. Bind the service to the channels, if a service. If there is no service_id in the config file, create a new service and update the config file.
  4. Start the scheduler and run refresh(), authenticate(), and send_heartbeat() periodically.
  5. Call the on_start() callback (override this method to perform your own initialization tasks).
  6. Start listening to the websocket and the Wand.
  Parameters:
    (No parameters in this class constructor)
  Returns:
    The None.
  Raises:
    (this function does not raise any notable errors)

.. _moobius.core.sdk.Moobius.user_join_service_channels:

Moobius.user_join_service_channels
---------------------------------------------------------------------------------------------------------------------
Moobius.user_join_service_channels(self, service_config_fname)

Joins service channels.
  Parameters:
    service_config_fname: The service config dict or JSON filename (use in user mode).
  Returns:
    The None.
  Raises:
    (this function does not raise any notable errors)

.. _moobius.core.sdk.Moobius.fetch_service_id_each_channel:

Moobius.fetch_service_id_each_channel
---------------------------------------------------------------------------------------------------------------------
Moobius.fetch_service_id_each_channel(self)

  Parameters:
    (No parameters in this class constructor)
  Returns:
    The  dict describing which service_id each channel_id is bound to. 
    Channels can only be bound to a single service.
    Channels not bound to any service will not be in the dict.
  Raises:
    (this function does not raise any notable errors)

.. _moobius.core.sdk.Moobius.fetch_bound_channels:

Moobius.fetch_bound_channels
---------------------------------------------------------------------------------------------------------------------
Moobius.fetch_bound_channels(self)

  Parameters:
    (No parameters in this class constructor)
  Returns:
    The  list of channels that are bound to this service.
  Raises:
    (this function does not raise any notable errors)

.. _moobius.core.sdk.Moobius.fetch_characters:

Moobius.fetch_characters
---------------------------------------------------------------------------------------------------------------------
Moobius.fetch_characters(self, channel_id)

  Parameters:
    channel_id: The channel id.
  Returns:
    The  list (of Character objects).
    This list includes:
      Real members (ids for a particular user-channel combination) who joined the channel with the given channel_id.
      Agent characters that have been created by this service; agent characters are not bound to any channel.
  Raises:
    (this function does not raise any notable errors)

.. _moobius.core.sdk.Moobius.limit_len:

Moobius.limit_len
---------------------------------------------------------------------------------------------------------------------
Moobius.limit_len(self, txt, n)

  Parameters:
    txt: The text.
    n: The maximum length,.
  Returns:
    The  string with a limited length.
    If the string is shortened "...<number of> chars" will be shown at the end.
  Raises:
    (this function does not raise any notable errors)

.. _moobius.core.sdk.Moobius._convert_message_content:

Moobius._convert_message_content
---------------------------------------------------------------------------------------------------------------------
Moobius._convert_message_content(self, subtype, content)

  Parameters:
    subtype: The subtype.
    content: The string or dict-valued content,.
  Returns:
    The  MessageContent object.
  Raises:
    (this function does not raise any notable errors)

.. _moobius.core.sdk.Moobius.send_message:

Moobius.send_message
---------------------------------------------------------------------------------------------------------------------
Moobius.send_message(self, message, channel_id, sender, recipients, subtype, len_limit, file_display_name)

Sends a message down (or up if in user-mode). This function is very flexible.
  Parameters:
    message: The message to send.
        If a string, the message will be a text message unless subtype is set.
          If not a text message, the string must either be a local filepath or an http(s) filepath.
        If a MessageBody or dict, the message sent will depend on it's fields/attributes as well as the overrides specified.
        If a pathlib.Path, will be a file/audio/image message by default.
    channel_id=None: The channel ids, if None message must be a MessageBody with the channel_id.
        Overrides message if not None.
    sender=None: The character/user who's avatar appears to "speak" this message.
        Overrides message if not None.
    recipients=None: The List of character_ids.
        Overrides message if not None.
    subtype=None: The Can be set to types.TEXT, types.IMAGE, types.AUDIO, types.FILE, or types.CARD
        If None, the subtype will be inferred.
    len_limit=None: The Limit the length of large text messages.
    file_display_name: The name shown for downloadable files can be set to a value different than the filename.
        Sets the subtype to "types.FILE" if subtype is not specified.
  Returns:
    The None.
  Raises:
    (this function does not raise any notable errors)

.. _moobius.core.sdk.Moobius.send:

Moobius.send
---------------------------------------------------------------------------------------------------------------------
Moobius.send(self, payload_type, payload_body)

Sends any kind of payload. Example payload types:
  message_down, update, update_characters, update_channel_info, update_canvas, update_buttons, update_style, and heartbeat.
Rarely used except internally, but provides the most flexibility for those special occasions.
  Parameters:
    payload_type (str): The type of the payload.
    payload_body (dict or str): The body of the payload.
        Strings will be converted into a Payload object.
  Returns:
    The None.
  Raises:
    (this function does not raise any notable errors)

.. _moobius.core.sdk.Moobius.send_button_click:

Moobius.send_button_click
---------------------------------------------------------------------------------------------------------------------
Moobius.send_button_click(self, button_id, button_args, channel_id)

Used in user-mode to send a button click.
  Parameters:
    button_id (str): The Which button.
    button_args (list of str): The What about said button should be fetched?.
    channel_id (str): The Which channel.
  Returns:
    The None.
  Raises:
    (this function does not raise any notable errors)

.. _moobius.core.sdk.Moobius.send_heartbeat:

Moobius.send_heartbeat
---------------------------------------------------------------------------------------------------------------------
Moobius.send_heartbeat(self)

Sends a heartbeat to the server.
  Parameters:
    (No parameters in this class constructor)
  Returns:
    The None.
  Raises:
    (this function does not raise any notable errors)

.. _moobius.core.sdk.Moobius.create_channel:

Moobius.create_channel
---------------------------------------------------------------------------------------------------------------------
Moobius.create_channel(self, channel_name, channel_desc, bind)

Creates a channel.
By default bind is True, which means the service connects itself to the channel.
  Parameters:
    channel_name: The channel name.
    channel_desc: The channel description.
    bind: Whether to bind to the new channel.
  Returns:
    The channel id.
  Raises:
    (this function does not raise any notable errors)

.. _moobius.core.sdk.Moobius.send_canvas:

Moobius.send_canvas
---------------------------------------------------------------------------------------------------------------------
Moobius.send_canvas(self, canvas_items, channel_id, recipients)

Updates the canvas.
  Parameters:
    canvas_items: The list of CanvasItems (which have text and/or images).
    channel_id: The  channel_id.
    recipients: The recipients.
  Returns:
    The message.
  Raises:
    (this function does not raise any notable errors)

.. _moobius.core.sdk.Moobius._update_rec:

Moobius._update_rec
---------------------------------------------------------------------------------------------------------------------
Moobius._update_rec(self, recipients, is_m_down, channel_id)

Use this function in the in the "recipients" fields of the websocket.
Converts lists into group_id strings, creating a group if need be, when.
  Parameters:
    recipients: The recipients.
    is_m_down: The True if a message down.
    channel_id: The channel_id.
  Returns:
    The converted list.
  Raises:
    (this function does not raise any notable errors)

.. _moobius.core.sdk.Moobius.refresh_http:

Moobius.refresh_http
---------------------------------------------------------------------------------------------------------------------
Moobius.refresh_http(self)

Calls self.http_api.refresh.
Doc for the called function:
Refreshes the access token,.
  Parameters:
    (No parameters in this class constructor)
  Returns:
    The it.
  Raises:
    (this function does not raise any notable errors)

.. _moobius.core.sdk.Moobius.authenticate:

Moobius.authenticate
---------------------------------------------------------------------------------------------------------------------
Moobius.authenticate(self)

Calls self.http_api.authenticate.
Doc for the called function:
Authenticates using self.username andself.password. Needs to be called before any other API calls.
  Parameters:
    (No parameters in this class constructor)
  Returns:
    (the access token, the refresh token).
    Raises an Exception if doesn't receive a valid response.
    Like most GET and POST functions it will raise any errors thrown by the http API.
  Raises:
    (this function does not raise any notable errors)

.. _moobius.core.sdk.Moobius.sign_up:

Moobius.sign_up
---------------------------------------------------------------------------------------------------------------------
Moobius.sign_up(self)

Calls self.http_api.sign_up.
Doc for the called function:
Signs up.
  Parameters:
    (No parameters in this class constructor)
  Returns:
    (the access token, the refresh token).
  Raises:
    (this function does not raise any notable errors)

.. _moobius.core.sdk.Moobius.sign_out:

Moobius.sign_out
---------------------------------------------------------------------------------------------------------------------
Moobius.sign_out(self)

Calls self.http_api.sign_out.
Doc for the called function:
Signs out using the access token obtained from signing in.
  Parameters:
    (No parameters in this class constructor)
  Returns:
    The None.
  Raises:
    (this function does not raise any notable errors)

.. _moobius.core.sdk.Moobius.update_current_user:

Moobius.update_current_user
---------------------------------------------------------------------------------------------------------------------
Moobius.update_current_user(self, avatar, description, name)

Calls self.http_api.update_current_user.
Doc for the called function:
Updates the user info. Used by user mode.
  Parameters:
    avatar: The Link to image or local filepath to upload.
    description: The Of the user.
    name: The name that shows in chat.
  Returns:
    The None.
  Raises:
    (this function does not raise any notable errors)

.. _moobius.core.sdk.Moobius.update_agent:

Moobius.update_agent
---------------------------------------------------------------------------------------------------------------------
Moobius.update_agent(self, agent_id, avatar, description, name)

Calls self.http_api.update_agent using self.client_id.
Doc for the called function:
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
    (this function does not raise any notable errors)

.. _moobius.core.sdk.Moobius.update_channel:

Moobius.update_channel
---------------------------------------------------------------------------------------------------------------------
Moobius.update_channel(self, channel_id, channel_name, channel_desc)

Calls self.http_api.update_channel.
Doc for the called function:
Updates a channel group.
  Parameters:
    channel_id (str): The id of the group leader?.
    group_name (str): The What to call it.
    members (list): The  list of character_id strings that will be inside the group.
  Returns:
    The None.
  Raises:
    (this function does not raise any notable errors)

.. _moobius.core.sdk.Moobius.bind_service_to_channel:

Moobius.bind_service_to_channel
---------------------------------------------------------------------------------------------------------------------
Moobius.bind_service_to_channel(self, channel_id)

Calls self.http_api.bind_service_to_channel
Doc for the called function:
Binds a service to a channel.
This function is unusual in that it.
  Parameters:
    service_id: The service.
    channel_id: The channel IDs.
  Returns:
    Whether it was sucessful rather than raising errors if it fails.
  Raises:
    (this function does not raise any notable errors)

.. _moobius.core.sdk.Moobius.unbind_service_from_channel:

Moobius.unbind_service_from_channel
---------------------------------------------------------------------------------------------------------------------
Moobius.unbind_service_from_channel(self, channel_id)

Calls self.http_api.unbind_service_from_channel
Doc for the called function:
Unbinds a service to a channel.
  Parameters:
    service_id: The service.
    channel_id: The channel IDs.
  Returns:
    The None.
  Raises:
    (this function does not raise any notable errors)

.. _moobius.core.sdk.Moobius.create_agent:

Moobius.create_agent
---------------------------------------------------------------------------------------------------------------------
Moobius.create_agent(self, name, avatar, description)

Calls self.http_api.create_agent using self.create_agent.
Doc for the called function:
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
    (this function does not raise any notable errors)

.. _moobius.core.sdk.Moobius.fetch_popular_channels:

Moobius.fetch_popular_channels
---------------------------------------------------------------------------------------------------------------------
Moobius.fetch_popular_channels(self)

Calls self.http_api.fetch_popular_channels.
Doc for the called function:
Fetches the popular channels,.
  Parameters:
    (No parameters in this class constructor)
  Returns:
    The  list of channel_id strings.
  Raises:
    (this function does not raise any notable errors)

.. _moobius.core.sdk.Moobius.fetch_channel_list:

Moobius.fetch_channel_list
---------------------------------------------------------------------------------------------------------------------
Moobius.fetch_channel_list(self)

Calls self.http_api.fetch_channel_list.
Doc for the called function:
Fetches all? channels,.
  Parameters:
    (No parameters in this class constructor)
  Returns:
    The  list of channel_id strings.
  Raises:
    (this function does not raise any notable errors)

.. _moobius.core.sdk.Moobius.fetch_member_ids:

Moobius.fetch_member_ids
---------------------------------------------------------------------------------------------------------------------
Moobius.fetch_member_ids(self, channel_id, raise_empty_list_err)

Calls self.http_api.fetch_member_ids using self.client_id.
Doc for the called function:
Fetches the member ids of a channel which coorespond to real users.
  Parameters:
    channel_id (str): The channel ID.
    service_id (str): The service/client/user ID.
    raise_empty_list_err=False: The Raises an Exception if the list is empty.
  Returns:
    The  list of character_id strings.
  Raises:
    An Exception (empty list) if raise_empty_list_err is True and the list is empty.

.. _moobius.core.sdk.Moobius.fetch_character_profile:

Moobius.fetch_character_profile
---------------------------------------------------------------------------------------------------------------------
Moobius.fetch_character_profile(self, character_id)

Calls self.http_api.fetch_character_profile
Doc for the called function:
  Parameters:
    character_id: The string-valued (or list-valued) character_id.
  Returns:
    The  Character object (or list therof),
    It works for both member_ids and agent_ids.
  Raises:
    (this function does not raise any notable errors)

.. _moobius.core.sdk.Moobius.fetch_service_id_list:

Moobius.fetch_service_id_list
---------------------------------------------------------------------------------------------------------------------
Moobius.fetch_service_id_list(self)

Calls self.http_api.fetch_service_id_list
Doc for the called function:
  Parameters:
    (No parameters in this class constructor)
  Returns:
    The  list of service_id strings of the user.
  Raises:
    (this function does not raise any notable errors)

.. _moobius.core.sdk.Moobius.fetch_agents:

Moobius.fetch_agents
---------------------------------------------------------------------------------------------------------------------
Moobius.fetch_agents(self)

Calls self.http_api.fetch_agents using self.client_id.
Doc for the called function:
  Parameters:
    service_id: The service ID.
  Returns:
    The  list of non-user Character objects bound to this service.
  Raises:
    (this function does not raise any notable errors)

.. _moobius.core.sdk.Moobius.upload:

Moobius.upload
---------------------------------------------------------------------------------------------------------------------
Moobius.upload(self, filepath)

Calls self.http_api.upload. Note that uploads happen automatically for any function that accepts a filepath/url when given a local path.
Doc for the called function:
Uploads the file at local path file_path to the Moobius server. Automatically calculates the upload URL and upload fields.
  Parameters:
    file_path: The file_path.
  Returns:
    The uploaded URL. Raises an Exception if the upload fails.
  Raises:
    (this function does not raise any notable errors)

.. _moobius.core.sdk.Moobius.download:

Moobius.download
---------------------------------------------------------------------------------------------------------------------
Moobius.download(self, source, full_path, auto_dir, overwrite, bytes, headers)

Calls self.http_api.download.
Doc for the called function:
Downloads a file from a url or other source to a local filename, automatically creating dirs if need be.
  Parameters:
    url: The url to download the file from.
    full_path=None: The filepath to download to.
        None will create a file based on the timestamp + random numbers.
        If no extension is specified, will infer the extension from the url if one exists.
    auto_dir=None: The If no full_path is specified, a folder must be choosen.
        Defaults to './downloads'.
    overwrite=None: The llow overwriting pre-existing files. If False, will raise an Exception on name collision.
    bytes=None: The If True, will return bytes instead of saving a file.
    headers=None: The Optional headers. Use these for downloads that require auth.
        Can set to "self" to use the same auth headers that this instance is using.
  Returns:
    The bytes if bytes=True.
  Raises:
    (this function does not raise any notable errors)

.. _moobius.core.sdk.Moobius.fetch_message_history:

Moobius.fetch_message_history
---------------------------------------------------------------------------------------------------------------------
Moobius.fetch_message_history(self, channel_id, limit, before)

Calls self.http_api.fetch_message_history.
Doc for the called function:
Returns the message chat history.
  Parameters:
    channel_id (str): The Channel with the messages inside of it.
    limit=64: The Max number of messages to return (messages further back in time, if any, will not be returned).
    before="null": The Only return messages older than this.
  Returns:
    The  list of dicts.
  Raises:
    (this function does not raise any notable errors)

.. _moobius.core.sdk.Moobius.create_channel_group:

Moobius.create_channel_group
---------------------------------------------------------------------------------------------------------------------
Moobius.create_channel_group(self, channel_id, group_name, members)

Calls self.http_api.create_channel_group.
Doc for the called function:
Creates a channel group.
  Parameters:
    channel_id (str): The id of the group leader?.
    group_name (str): The What to call it.
    characters (list): The  list of channel_id strings that will be inside the group.
  Returns:
    The group_id string.
  Raises:
    (this function does not raise any notable errors)

.. _moobius.core.sdk.Moobius.create_service_group:

Moobius.create_service_group
---------------------------------------------------------------------------------------------------------------------
Moobius.create_service_group(self, group_id, members)

Calls self.http_api.create_service_group.
Doc for the called function:
Creates a group containing the list of characters_ids and returns this Group object.
This group can then be used in send_message_down payloads.
  Parameters:
    group_name (str): The What to call it.
    character_ids (list): The  list of character_id strings or Characters that will be inside the group.
  Returns:
    The  Group object.
  Raises:
    (this function does not raise any notable errors)

.. _moobius.core.sdk.Moobius.character_ids_of_channel_group:

Moobius.character_ids_of_channel_group
---------------------------------------------------------------------------------------------------------------------
Moobius.character_ids_of_channel_group(self, sender_id, channel_id, group_id)

Calls self.http_api.character_ids_of_channel_group
Doc for the called function:
Gets a list of character ids belonging to a channel group.
Websocket payloads contain these channel_groups which are shorthand for a list of characters.
  Parameters:
    sender_id: The message's sender.
    channel_id: The message specified that it was sent in this channel.
    group_id: The messages recipients.
  Returns:
    The character_id list.
  Raises:
    (this function does not raise any notable errors)

.. _moobius.core.sdk.Moobius.character_ids_of_service_group:

Moobius.character_ids_of_service_group
---------------------------------------------------------------------------------------------------------------------
Moobius.character_ids_of_service_group(self, group_id)

Calls self.http_api.character_ids_of_service_group
Doc for the called function:
  Parameters:
    group_id: The group_id.
  Returns:
    The  list of character ids belonging to a service group.
    Note that the 'recipients' in 'on message up' might be None:
      To avoid requiring checks for None this function will return an empty list given Falsey inputs or Falsey string literals.
  Raises:
    (this function does not raise any notable errors)

.. _moobius.core.sdk.Moobius.update_channel_group:

Moobius.update_channel_group
---------------------------------------------------------------------------------------------------------------------
Moobius.update_channel_group(self, channel_id, group_id, members)

Calls self.http_api.update_channel_group.
Doc for the called function:
Updates a channel group.
  Parameters:
    channel_id (str): The id of the group leader?.
    group_name (str): The What to call it.
    members (list): The  list of character_id strings that will be inside the group.
  Returns:
    The None.
  Raises:
    (this function does not raise any notable errors)

.. _moobius.core.sdk.Moobius.update_temp_channel_group:

Moobius.update_temp_channel_group
---------------------------------------------------------------------------------------------------------------------
Moobius.update_temp_channel_group(self, channel_id, members)

Calls self.http_api.update_temp_channel_group.
Doc for the called function:
Updates a channel TEMP group.
  Parameters:
    channel_id (str): The id of the group leader?.
    members (list): The  list of character_id strings that will be inside the group.
  Returns:
    The None.
  Raises:
    (this function does not raise any notable errors)

.. _moobius.core.sdk.Moobius.fetch_channel_temp_group:

Moobius.fetch_channel_temp_group
---------------------------------------------------------------------------------------------------------------------
Moobius.fetch_channel_temp_group(self, channel_id)

Calls self.http_api.fetch_channel_temp_group.
Doc for the called function:
Like fetch_channel_group_list but for TEMP groups..
  Parameters:
    channel_id: The channel_id.
    service_id: The service_id,.
  Returns:
    The list of groups.
  Raises:
    (this function does not raise any notable errors)

.. _moobius.core.sdk.Moobius.fetch_channel_group_list:

Moobius.fetch_channel_group_list
---------------------------------------------------------------------------------------------------------------------
Moobius.fetch_channel_group_list(self, channel_id)

Calls self.http_api.fetch_target_group.
Doc for the called function:
Not yet implemented!
Fetches info about the group.
  Parameters:
    user_id (str), channel_id (str): The why needed?.
    group_id (str): The Which group to fetch.
  Returns:
    The data-dict data.
  Raises:
    (this function does not raise any notable errors)

.. _moobius.core.sdk.Moobius.fetch_user_from_group:

Moobius.fetch_user_from_group
---------------------------------------------------------------------------------------------------------------------
Moobius.fetch_user_from_group(self, user_id, channel_id, group_id)

Calls self.http_api.fetch_user_from_group.
Doc for the called function:
Not yet implemented!
Fetches the user profile of a user from a group.
  Parameters:
    user_id (str): The user ID.
    channel_id (str): The channel ID. (TODO: of what?).
    group_id (str): The group ID.
  Returns:
    The user profile Character object.
  Raises:
    (this function does not raise any notable errors)

.. _moobius.core.sdk.Moobius.fetch_target_group:

Moobius.fetch_target_group
---------------------------------------------------------------------------------------------------------------------
Moobius.fetch_target_group(self, user_id, channel_id, group_id)

Calls self.http_api.fetch_target_group.
Doc for the called function:
Not yet implemented!
Fetches info about the group.
  Parameters:
    user_id (str), channel_id (str): The why needed?.
    group_id (str): The Which group to fetch.
  Returns:
    The data-dict data.
  Raises:
    (this function does not raise any notable errors)

.. _moobius.core.sdk.Moobius.send_user_login:

Moobius.send_user_login
---------------------------------------------------------------------------------------------------------------------
Moobius.send_user_login(self)

Calls self.ws_client.user_login using self.http_api.access_token; Use for user mode.
Doc for the called function:
Logs-in a user.
Every 2h AWS will force-disconnect, so it is a good idea to send this on connect.
  Parameters:
    access_token: The Used in the user_login message that is sent.
        This is the access token from http_api_wrapper.
    dry_run=False: The Don't acually send anything if True.
  Returns:
    The message as a dict.
  Raises:
    (this function does not raise any notable errors)

.. _moobius.core.sdk.Moobius.send_service_login:

Moobius.send_service_login
---------------------------------------------------------------------------------------------------------------------
Moobius.send_service_login(self)

Calls self.ws_client.service_login using self.client_id and self.http_api.access_token.
Doc for the called function:
Logs in. Much like the HTTP api, this needs to be sent before any other messages.
  Parameters:
    service_id (str): The client_id of a Moobius service object, which is the ID of the running service.
        Used in almost every function.
    access_token (str): 
    TODO: The This is the access token from http_api_wrapper; for clean code decouple access_token here!.
    dry_run=False: The Don't acually send anything (must functions offer a dry-run option).
  Returns:
    The message as a dict.
  Raises:
    (this function does not raise any notable errors)

.. _moobius.core.sdk.Moobius.send_update:

Moobius.send_update
---------------------------------------------------------------------------------------------------------------------
Moobius.send_update(self, data, target_client_id)

Calls self.ws_client.update
Doc for the called function:
A generic update function that is rarely used.
  Parameters:
    service_id (str): The s always.
    target_client_id (str): The target client id (TODO: not currently used).
    data (dict): The content of the update.
    dry_run=False: The Don't acually send anything if True.
  Returns:
    The message as a dict.
  Raises:
    (this function does not raise any notable errors)

.. _moobius.core.sdk.Moobius.send_characters:

Moobius.send_characters
---------------------------------------------------------------------------------------------------------------------
Moobius.send_characters(self, character_ids, channel_id, recipients)

Calls self.ws_client.update_character_list using self.client_id. Converts recipients to a group_id if a list.
Doc for the called function:
Updates the characters that the recipients see.
  Parameters:
    characters (str): The group id to represent the characters who are updated.
    service_id (str): The s always.
    channel_id (str): The channel id.
    recipients (str): The group id to send to.
    dry_run=False: The if True don't acually send the message (messages are sent in thier JSON-strin format).
  Returns:
    The message as a dict.
  Raises:
    (this function does not raise any notable errors)

.. _moobius.core.sdk.Moobius.send_channel_info:

Moobius.send_channel_info
---------------------------------------------------------------------------------------------------------------------
Moobius.send_channel_info(self, channel_info, channel_id)

Calls self.ws_client.update_channel_info using self.client_id.
Doc for the called function:
Updates the channel name, description, etc for a given channel.
  Parameters:
    channel_info (ChannelInfo or dict): The data of the update.
    service_id (str): The s always.
    channel_id (str): The channel id.
    dry_run=False: The Don't acually send anything if True.
  Returns:
    The message as a dict.
    Example:
      >>> ws_client.update_channel_info("service_id", "channel_id", {"name": "new_channel_name"}).
  Raises:
    (this function does not raise any notable errors)

.. _moobius.core.sdk.Moobius.send_buttons:

Moobius.send_buttons
---------------------------------------------------------------------------------------------------------------------
Moobius.send_buttons(self, buttons, channel_id, recipients)

Calls self.ws_client.update_buttons using self.client_id. Converts recipients to a group_id if a list.
Doc for the called function:
Updates the buttons that the recipients see.
  Parameters:
    buttons (list of Buttons): The buttons list to be updated.
    service_id (str): The s always.
    channel_id (str): The channel id.
    recipients (str): The group id to send to.
    dry_run=False: The Don't acually send anything if True.
  Returns:
    The message as a dict.
    Example:
      >>> continue_button =
      >>>   {"button_name": "Continue Playing", "button_id": "play",
      >>>    "button_name": "Continue Playing", "new_window": False,
      >>>    "arguments": []}
      >>> ws_client.update_buttons("service_id", "channel_id", [continue_button], ["user1", "user2"]).
  Raises:
    (this function does not raise any notable errors)

.. _moobius.core.sdk.Moobius.send_menu:

Moobius.send_menu
---------------------------------------------------------------------------------------------------------------------
Moobius.send_menu(self, menu_items, channel_id, recipients)

Calls self.ws_client.update_menu using self.client_id. Converts recipients to a group_id if a list.
Doc for the called function:
Updates the right-click menu that the recipients can open on various messages.
  Parameters:
    menu_items (list): The List of MenuItem dataclasses.
    service_id (str): The s always.
    channel_id (str): The channel id.
  Returns:
    The message as a dict.
  Raises:
    (this function does not raise any notable errors)

.. _moobius.core.sdk.Moobius.send_style:

Moobius.send_style
---------------------------------------------------------------------------------------------------------------------
Moobius.send_style(self, style_items, channel_id, recipients)

Calls self.ws_client.update_style using self.client_id. Converts recipients to a group_id if a list.
Doc for the called function:
Updates the style (whether the canvas is expanded, other look-and-feel aspects) that the recipients see.
  Parameters:
    style_items (list of dicts or StyleItem objects): The style content to be updated. Dicts are converted into 1-elemnt lists.
    service_id (str): The s always.
    channel_id (str): The channel id.
    recipients (str): The group id to send to.
    dry_run=False: The Don't acually send anything if True.
  Returns:
    The message as a dict.
    Example:
        >>> style_items = [
        >>>   {
        >>>     "widget": "channel",
        >>>     "display": "invisible",
        >>>   },
        >>>   {
        >>>     "widget": "button",
        >>>     "display": "highlight",
        >>>     "button_hook": {
        >>>       "button_id": "button_id",
        >>>       "button_name": "done",
        >>>       "arguments": []
        >>>       },
        >>>     "text": "<h1>Start from here.</h1><p>This is a Button, which most channels have</p>"
        >>>   }]
        >>> ws_client.update_style("service_id", "channel_id", style_items, ["user1", "user2"]).
  Raises:
    (this function does not raise any notable errors)

.. _moobius.core.sdk.Moobius.refresh_socket:

Moobius.refresh_socket
---------------------------------------------------------------------------------------------------------------------
Moobius.refresh_socket(self, channel_id)

Calls self.ws_client.refresh using self.client_id.
Doc for the called function:
Refreshes everything the user can see. The socket will send back messages with the information later.
  Parameters:
    user_id (str): The Used in the "action" message that is sent.
    channel_id (str): The Used in the body of said message.
    dry_run=False: The Don't acually send anything if True.
        These three parameters are common to most fetch messages.
  Returns:
    The message that was sent as a dict.
  Raises:
    (this function does not raise any notable errors)

.. _moobius.core.sdk.Moobius.send_join_channel:

Moobius.send_join_channel
---------------------------------------------------------------------------------------------------------------------
Moobius.send_join_channel(self, channel_id)

Calls self.ws_client.join_channel using self.client_id. Use for user mode.
Doc for the called function:
A user joins the channel with channel_id, unless dry_run is True..
  Parameters:
    user_id: The user_id, the channel_id,.
    channel_id: Whether to dry_run.
  Returns:
    The message sent.
  Raises:
    (this function does not raise any notable errors)

.. _moobius.core.sdk.Moobius.send_leave_channel:

Moobius.send_leave_channel
---------------------------------------------------------------------------------------------------------------------
Moobius.send_leave_channel(self, channel_id)

Calls self.ws_client.leave_channel using self.client_id. Used for user mode.
Doc for the called function:
A user leaves the channel with channel_id, unless dry_run is True..
  Parameters:
    user_id: The user_id, the channel_id,.
    channel_id: Whether to dry_run.
  Returns:
    The message sent.
  Raises:
    (this function does not raise any notable errors)

.. _moobius.core.sdk.Moobius.checkin:

Moobius.checkin
---------------------------------------------------------------------------------------------------------------------
Moobius.checkin(self)

Called as a rate task, used to resync users, etc. Only called after on_start().
  Parameters:
    (No parameters in this class constructor)
  Returns:
    The None.
  Raises:
    (this function does not raise any notable errors)

.. _moobius.core.sdk.Moobius.listen_loop:

Moobius.listen_loop
---------------------------------------------------------------------------------------------------------------------
Moobius.listen_loop(self)

Listens to the wand in an infinite loop, polling self.queue (which is an aioprocessing.AioQueue).
This allows the wand to send "spells" (messages) to the services at any time.
  Parameters:
    (No parameters in this class constructor)
  Returns:
    The Never.
  Raises:
    (this function does not raise any notable errors)

.. _moobius.core.sdk.Moobius.handle_received_payload:

Moobius.handle_received_payload
---------------------------------------------------------------------------------------------------------------------
Moobius.handle_received_payload(self, payload)

Decodes the received websocket payload JSON and calls the handler based on p['type'],. 
Example methods called:
  on_message_up(), on_action(), on_button_click(), on_copy_client(), on_unknown_payload()
Example use-case:
  >>> self.ws_client = WSClient(ws_server_uri, on_connect=self.send_service_login, handle=self.handle_received_payload).
  Parameters:
    payload: The payload string.
  Returns:
    The None.
  Raises:
    (this function does not raise any notable errors)

.. _moobius.core.sdk.Moobius.on_action:

Moobius.on_action
---------------------------------------------------------------------------------------------------------------------
Moobius.on_action(self, action)

Calls the corresponding method to handle different subtypes of action.
Example methods called:
  on_fetch_characters(), on_fetch_buttons(), on_fetch_canvas(), on_join_channel(), on_leave_channel(), on_fetch_channel_info().
  Parameters:
    action: The n Action object from a user.
  Returns:
    The None.
  Raises:
    (this function does not raise any notable errors)

.. _moobius.core.sdk.Moobius.on_update:

Moobius.on_update
---------------------------------------------------------------------------------------------------------------------
Moobius.on_update(self, update)

Dispatches it to one of various callbacks. Use for user mode.
It is recommended to overload the invididual callbacks instead of this function.
  Parameters:
    update: The n Update object from the socket.
  Returns:
    The None.
  Raises:
    (this function does not raise any notable errors)

.. _moobius.core.sdk.Moobius.on_start:

Moobius.on_start
---------------------------------------------------------------------------------------------------------------------
Moobius.on_start(self)

Called when the service is initialized.
  Parameters:
    (No parameters in this class constructor)
  Returns:
    The None.
  Raises:
    (this function does not raise any notable errors)

.. _moobius.core.sdk.Moobius.initialize_channel:

Moobius.initialize_channel
---------------------------------------------------------------------------------------------------------------------
Moobius.initialize_channel(self, channel_id)

Called once per channel on startup.. 
By default, if self.db_config has been set, a MoobiusStorage is created in self.channel_storages.
  Parameters:
    channel_id: The channel ID.
  Returns:
    The None.
  Raises:
    (this function does not raise any notable errors)

.. _moobius.core.sdk.Moobius.checkin_channel:

Moobius.checkin_channel
---------------------------------------------------------------------------------------------------------------------
Moobius.checkin_channel(self, channel_id)

A "wellness check" which is called on startup, on reconnect, and as a periodic "check-in"..
  Parameters:
    channel_id: The channel ID.
  Returns:
    The None.
  Raises:
    (this function does not raise any notable errors)

.. _moobius.core.sdk.Moobius.on_spell:

Moobius.on_spell
---------------------------------------------------------------------------------------------------------------------
Moobius.on_spell(self, obj)

Called when a "spell" from the wand is received, which can be any object but is often a string..
  Parameters:
    obj: The wand sent this process.
  Returns:
    The None.
  Raises:
    (this function does not raise any notable errors)

.. _moobius.core.sdk.Moobius.on_message_up:

Moobius.on_message_up
---------------------------------------------------------------------------------------------------------------------
Moobius.on_message_up(self, message)

Example MessageBody object:
>>>  moobius.MessageBody(subtype="text", channel_id=<channel id>, content=MessageContent(...), timestamp=1707254706635,
>>>                      recipients=[<user id 1>, <user id 2>], sender=<user id>, message_id=<message-id>,
>>>                      context={'group_id': <group-id>, 'channel_type': 'ccs'}).
  Parameters:
    message: The  message from a user.
  Returns:
    The None.
  Raises:
    (this function does not raise any notable errors)

.. _moobius.core.sdk.Moobius.on_fetch_buttons:

Moobius.on_fetch_buttons
---------------------------------------------------------------------------------------------------------------------
Moobius.on_fetch_buttons(self, fetch)

This and other "on_fetch_xyz" functions are commonly overriden to call "send_xyz" with the needed material.
Example Action object:
>>> moobius.Action(subtype="fetch_buttons", channel_id=<channel id>, sender=<user id>, context={}).
  Parameters:
    fetch: The request for the list of buttons from the user.
  Returns:
    The None.
  Raises:
    (this function does not raise any notable errors)

.. _moobius.core.sdk.Moobius.on_fetch_style:

Moobius.on_fetch_style
---------------------------------------------------------------------------------------------------------------------
Moobius.on_fetch_style(self, fetch)

This and other "on_fetch_xyz" functions are commonly overriden to call "send_xyz" with the needed material.
Example Action object:
>>> moobius.Action(subtype="fetch_style", channel_id=<channel id>, sender=<user id>, context={}).
  Parameters:
    fetch: The request for the style from the user.
  Returns:
    The None.
  Raises:
    (this function does not raise any notable errors)

.. _moobius.core.sdk.Moobius.on_fetch_characters:

Moobius.on_fetch_characters
---------------------------------------------------------------------------------------------------------------------
Moobius.on_fetch_characters(self, fetch)

This tells them who they will be able to see and send messages to. 
Example Action object:
>>> moobius.Action(subtype="fetch_characters", channel_id=<channel id>, sender=<user id>, context={}).
  Parameters:
    fetch: The request for the list of characters from the user.
  Returns:
    The None.
  Raises:
    (this function does not raise any notable errors)

.. _moobius.core.sdk.Moobius.on_fetch_canvas:

Moobius.on_fetch_canvas
---------------------------------------------------------------------------------------------------------------------
Moobius.on_fetch_canvas(self, fetch)

Example Action object:
>>> moobius.Action(subtype="fetch_canvas", channel_id=<channel id>, sender=<user id>, context={}).
  Parameters:
    fetch: The request for the canvas from the user.
  Returns:
    The None.
  Raises:
    (this function does not raise any notable errors)

.. _moobius.core.sdk.Moobius.on_fetch_menu:

Moobius.on_fetch_menu
---------------------------------------------------------------------------------------------------------------------
Moobius.on_fetch_menu(self, fetch)

Example Action object:
>>> moobius.Action(subtype="fetch_menu", channel_id=<channel id>, sender=<user id>, context={}).
  Parameters:
    fetch: The request for the context menu from the user.
  Returns:
    The None.
  Raises:
    (this function does not raise any notable errors)

.. _moobius.core.sdk.Moobius.on_fetch_channel_info:

Moobius.on_fetch_channel_info
---------------------------------------------------------------------------------------------------------------------
Moobius.on_fetch_channel_info(self, fetch)

Example Action object:
>>> moobius.Action(subtype="fetch_channel_info", channel_id=<channel id>, sender=<user id>, context={}).
  Parameters:
    fetch: The request for channel's metadata from the user.
  Returns:
    The None.
  Raises:
    (this function does not raise any notable errors)

.. _moobius.core.sdk.Moobius.on_copy_client:

Moobius.on_copy_client
---------------------------------------------------------------------------------------------------------------------
Moobius.on_copy_client(self, copy)

Example Copy object:
>>> moobius.Copy(request_id=<id>, origin_type=message_down, status=True, context={'message': 'Message received'}).
  Parameters:
    copy: The  "Copy" request from the user.
  Returns:
    The None.
  Raises:
    (this function does not raise any notable errors)

.. _moobius.core.sdk.Moobius.on_join_channel:

Moobius.on_join_channel
---------------------------------------------------------------------------------------------------------------------
Moobius.on_join_channel(self, action)

This callback happens when the user joins a channel.. 
Commonly used to inform everyone about this new user and update everyone's character list.
Example Action object:
>>> moobius.Action(subtype="join_channel", channel_id=<channel id>, sender=<user id>, context={}).
  Parameters:
    action: The n Action object.
  Returns:
    The None.
  Raises:
    (this function does not raise any notable errors)

.. _moobius.core.sdk.Moobius.on_leave_channel:

Moobius.on_leave_channel
---------------------------------------------------------------------------------------------------------------------
Moobius.on_leave_channel(self, action)

Called when the user leaves a channel.. 
Commonly used to update everyone's character list.
Example Action object:
>>> moobius.Action(subtype="leave_channel", channel_id=<channel id>, sender=<user id>, context={}).
  Parameters:
    action: The n Action object.
  Returns:
    The None.
  Raises:
    (this function does not raise any notable errors)

.. _moobius.core.sdk.Moobius.on_button_click:

Moobius.on_button_click
---------------------------------------------------------------------------------------------------------------------
Moobius.on_button_click(self, action)

Handles a button click from a user.. 
Example ButtonClick object:
>>> moobius.ButtonClick(button_id="the_big_red_button", channel_id=<channel id>, sender=<user id>, components=[], context={}).
  Parameters:
    action: The user's ButtonClick.
  Returns:
    The None.
  Raises:
    (this function does not raise any notable errors)

.. _moobius.core.sdk.Moobius.on_menu_item_click:

Moobius.on_menu_item_click
---------------------------------------------------------------------------------------------------------------------
Moobius.on_menu_item_click(self, action)

Handles a context menu right click from a user.. 
Example MenuItemClick object:
>>> MenuItemClick(item_id=1, message_id=<id>, message_subtypes=text, message_content={'text': 'Click on this message.'}, channel_id=<channel_id>, context={}, recipients=[]).
  Parameters:
    action: The user's MenuItemClick.
  Returns:
    The None.
  Raises:
    (this function does not raise any notable errors)

.. _moobius.core.sdk.Moobius.on_unknown_payload:

Moobius.on_unknown_payload
---------------------------------------------------------------------------------------------------------------------
Moobius.on_unknown_payload(self, payload)

A catch-all for handling unknown Payloads..
  Parameters:
    payload: The Payload that has not been recognized by the other handlers.
  Returns:
    The None.
  Raises:
    (this function does not raise any notable errors)

.. _moobius.core.sdk.Moobius.on_message_down:

Moobius.on_message_down
---------------------------------------------------------------------------------------------------------------------
Moobius.on_message_down(self, message)

Callback when the user recieves a message..
Use for user mode.
  Parameters:
    message: The service's MessageBody.
  Returns:
    The None.
  Raises:
    (this function does not raise any notable errors)

.. _moobius.core.sdk.Moobius.on_update_characters:

Moobius.on_update_characters
---------------------------------------------------------------------------------------------------------------------
Moobius.on_update_characters(self, update)

Callback when the user recieves the character list.. One of the multiple update callbacks. 
Use for user mode.
  Parameters:
    update: The service's Update.
  Returns:
    The None.
  Raises:
    (this function does not raise any notable errors)

.. _moobius.core.sdk.Moobius.on_update_channel_info:

Moobius.on_update_channel_info
---------------------------------------------------------------------------------------------------------------------
Moobius.on_update_channel_info(self, update)

Callback when the user recieves the channel info.. One of the multiple update callbacks. 
Use for user mode.
  Parameters:
    update: The service's Update.
  Returns:
    The None.
  Raises:
    (this function does not raise any notable errors)

.. _moobius.core.sdk.Moobius.on_update_canvas:

Moobius.on_update_canvas
---------------------------------------------------------------------------------------------------------------------
Moobius.on_update_canvas(self, update)

Callback when the user recieves the canvas content.. One of the multiple update callbacks. 
Use for user mode.
  Parameters:
    update: The service's Update.
  Returns:
    The None.
  Raises:
    (this function does not raise any notable errors)

.. _moobius.core.sdk.Moobius.on_update_buttons:

Moobius.on_update_buttons
---------------------------------------------------------------------------------------------------------------------
Moobius.on_update_buttons(self, update)

Callback when the user recieves the buttons.. One of the multiple update callbacks. 
Use for user mode.
  Parameters:
    update: The service's Update.
  Returns:
    The None.
  Raises:
    (this function does not raise any notable errors)

.. _moobius.core.sdk.Moobius.on_update_style:

Moobius.on_update_style
---------------------------------------------------------------------------------------------------------------------
Moobius.on_update_style(self, update)

Callback when the user recieves the style info (look and feel).. One of the multiple update callbacks. 
Use for user mode.
  Parameters:
    update: The service's Update.
  Returns:
    The None.
  Raises:
    (this function does not raise any notable errors)

.. _moobius.core.sdk.Moobius.on_update_menu:

Moobius.on_update_menu
---------------------------------------------------------------------------------------------------------------------
Moobius.on_update_menu(self, update)

Callback when the user recieves the context menu info.. One of the multiple update callbacks. 
Use for user mode.
  Parameters:
    update: The service's Update.
  Returns:
    The None.
  Raises:
    (this function does not raise any notable errors)

.. _moobius.core.sdk.Moobius.__str__:

Moobius.__str__
---------------------------------------------------------------------------------------------------------------------
Moobius.__str__(self)

The string output function for debugging.
  Parameters:
    (No parameters in this class constructor)
  Returns:
    The  easy-to-read string summary.
  Raises:
    (this function does not raise any notable errors)

.. _moobius.core.sdk.Moobius.__repr__:

Moobius.__repr__
---------------------------------------------------------------------------------------------------------------------
Moobius.__repr__(self)

The string output function for debugging.
  Parameters:
    (No parameters in this class constructor)
  Returns:
    The  easy-to-read string summary.
  Raises:
    (this function does not raise any notable errors)

Class attributes
--------------------


