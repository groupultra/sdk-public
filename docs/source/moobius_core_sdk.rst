.. _moobius_core_sdk:

moobius.core.sdk
====================================================================================

Module-level functions
===================================================================================

.. _moobius.core.sdk._deprecated_wrap:

_deprecated_wrap
---------------------------------------------------------------------------------------------------------------------
_deprecated_wrap(f, old_name, new_name)

<No doc string>

.. _moobius.core.sdk._deprecated_wrap.out:

_deprecated_wrap.out
---------------------------------------------------------------------------------------------------------------------
_deprecated_wrap.out(\*kwargs)

<No doc string>

===================================================================================

Class ServiceGroupLib
===========================================================================================

(This class is for internal use)
Converts a list of character_ids into a service or channel group id, creating one if need be.
   The lookup is O(n) so performance at extremly large list sizes may require optimizations.

.. _moobius.core.sdk.ServiceGroupLib.__init__:

ServiceGroupLib.__init__
---------------------------------------------------------------------------------------------------------------------
ServiceGroupLib.__init__(self)

Creates an empty ServiceGroupLib instance.

.. _moobius.core.sdk.ServiceGroupLib.convert_list:

ServiceGroupLib.convert_list
---------------------------------------------------------------------------------------------------------------------
ServiceGroupLib.convert_list(self, http_api, character_ids, is_message_down, channel_id)

Converts a list to single group id, unless it is already a group id.

Parameters:
  http_api: The http_api client in Moobius
  character_ids: List of ids. If a string, treated as a one element list.
  is_message_down: True = message_down (a message sent from the service), False = message_up (a message sent from an agent).
  channel_id=None: If None and the conversion still needs to happen it will raise an Exception.

Returns: The group id.

Class Moobius
===========================================================================================

<no class docstring>

.. _moobius.core.sdk.Moobius.__init__:

Moobius.__init__
---------------------------------------------------------------------------------------------------------------------
Moobius.__init__(self, config_path, db_config_path, is_agent, \*kwargs)

Initializes a service or agent object.

Parameters:
  config_path: The path of the agent or service config file.
    Can instead be a dict of the actual config, so that no file is loaded.
  db_config_path=None: The optional path of the database config file.
    Can also be a dict instead of a file.
  is_agent=False: True for an agent, False for a service.
    Agents are bots which simulate users and are limited to what a user can see.
    Both auth with user credentials, but there are slight differences under the hood.

Example:
  >>> service = SDK(config_path="./config/service.json", db_config_path="./config/database.json", is_agent=False)

.. _moobius.core.sdk.Moobius.start:

Moobius.start
---------------------------------------------------------------------------------------------------------------------
Moobius.start(self)

Starts the service/agent and calls start() fns are called with wand.run. There are 6 steps:
  1. Authenticate.
  2. Connect to the websocket server.
  3. Bind the service to the channels, if a service. If there is no service_id in the config file, create a new service and update the config file.
  4. Start the scheduler and run refresh(), authenticate(), and send_heartbeat() periodically.
  5. Call the on_start() callback (override this method to perform your own initialization tasks).
  6. Start listening to the websocket and the Wand.

No parameters or return value.

.. _moobius.core.sdk.Moobius.agent_join_service_channels:

Moobius.agent_join_service_channels
---------------------------------------------------------------------------------------------------------------------
Moobius.agent_join_service_channels(self, service_config_fname)

Joins service channels given by service config filename.

.. _moobius.core.sdk.Moobius.fetch_service_id_each_channel:

Moobius.fetch_service_id_each_channel
---------------------------------------------------------------------------------------------------------------------
Moobius.fetch_service_id_each_channel(self)

Returns a dict describing which service_id each channel_id is bound to. 
Channels can only be bound to a single service.
Channels not bound to any service will not be in the dict.

.. _moobius.core.sdk.Moobius.fetch_bound_channels:

Moobius.fetch_bound_channels
---------------------------------------------------------------------------------------------------------------------
Moobius.fetch_bound_channels(self)

Returns a list of channels that are bound to this service.

.. _moobius.core.sdk.Moobius.fetch_characters:

Moobius.fetch_characters
---------------------------------------------------------------------------------------------------------------------
Moobius.fetch_characters(self, channel_id)

Returns a list (of Character objects).
This list includes:
  Real members (ids for a particular user-channel combination) who joined the channel with the given channel_id.
  Puppet characters that have been created by this service; puppet characters are not bound to any channel.

.. _moobius.core.sdk.Moobius.limit_len:

Moobius.limit_len
---------------------------------------------------------------------------------------------------------------------
Moobius.limit_len(self, txt, n)

Returns a string with a limited length, appendin "...<number of> chars" if an abbreviation is necessary.

.. _moobius.core.sdk.Moobius._convert_message_content:

Moobius._convert_message_content
---------------------------------------------------------------------------------------------------------------------
Moobius._convert_message_content(self, subtype, content)

Creates a MessageContent object of the specified subtype, given the string or dict-valued content.

.. _moobius.core.sdk.Moobius.send_message:

Moobius.send_message
---------------------------------------------------------------------------------------------------------------------
Moobius.send_message(self, the_message, channel_id, sender, recipients, subtype, len_limit, file_display_name)

Sends a message. Used by both servies and agents. This function is very flexible.

Parameters:
  the_message:
    If a string, the message will be a text message unless subtype is set.
      If not a text message, the string must either be a local filepath or an http(s) filepath.
    If a MessageBody or dict, the message sent will depend on it's fields/attributes as well as the overrides specified.
    If a pathlib.Path, will be a file/audio/image message by default.
  channel_id=None: The channel ids, if None the_message must be a MessageBody with the channel_id.
    Overrides the_message if not None
  sender=None: The character/user who's avatar appears to "speak" this message.
    Overrides the_message if not None
  recipients=None: List of character_ids.
    Overrides the_message if not None.
  subtype=None: Can be set to types.TEXT, types.IMAGE, types.AUDIO, types.FILE, or types.CARD
    If None, the subtype will be inferred.
  len_limit=None: Limit the length of large text messages.
  file_display_name: The name shown for downloadable files can be set to a value different than the filename.
    Sets the subtype to "types.FILE" if subtype is not specified.

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

No return value.

.. _moobius.core.sdk.Moobius.send_button_click:

Moobius.send_button_click
---------------------------------------------------------------------------------------------------------------------
Moobius.send_button_click(self, channel_id, button_id, button_args)

Used by agents to send a button click.

Parameters:
  channel_id (str): Which channel.
  button_id (str): Which button.
  button_args (list of k-v pairs, not a dict): What about said button should be fetched?

No return value.

.. _moobius.core.sdk.Moobius.send_heartbeat:

Moobius.send_heartbeat
---------------------------------------------------------------------------------------------------------------------
Moobius.send_heartbeat(self)

Sends a heartbeat to the server. Return None

.. _moobius.core.sdk.Moobius.create_channel:

Moobius.create_channel
---------------------------------------------------------------------------------------------------------------------
Moobius.create_channel(self, channel_name, channel_desc, bind)

Creates a channel with the provided name and description.
By default bind is True, which means the service connects itself to the channel.
Returns the channel id.

.. _moobius.core.sdk.Moobius.send_update_canvas:

Moobius.send_update_canvas
---------------------------------------------------------------------------------------------------------------------
Moobius.send_update_canvas(self, channel_id, canvas_elements, recipients)

Updates the canvas given a channel_id, a list of CanvasElements (which have text and/or images), and recipients.

.. _moobius.core.sdk.Moobius._update_rec:

Moobius._update_rec
---------------------------------------------------------------------------------------------------------------------
Moobius._update_rec(self, recipients, is_m_down, channel_id)

Pass in await self._update_rec(recipients) into "recipients".
Converts lists into group_id strings, creating a group if need be.

.. _moobius.core.sdk.Moobius.refresh:

Moobius.refresh
---------------------------------------------------------------------------------------------------------------------
Moobius.refresh(self)

Calls self.http_api.refresh.
Doc for the called function:
Refreshes the access token, returning it.

.. _moobius.core.sdk.Moobius.authenticate:

Moobius.authenticate
---------------------------------------------------------------------------------------------------------------------
Moobius.authenticate(self)

Calls self.http_api.authenticate.
Doc for the called function:
Authenticates using self.username andself.password. Needs to be called before any other API calls.
Returns (the access token, the refresh token).
Raises an Exception if doesn't receive a valid response.
Like most GET and POST functions it will raise any errors thrown by the http API.

.. _moobius.core.sdk.Moobius.sign_up:

Moobius.sign_up
---------------------------------------------------------------------------------------------------------------------
Moobius.sign_up(self)

Calls self.http_api.sign_up.
Doc for the called function:
Signs up. Returns (the access token, the refresh token).

.. _moobius.core.sdk.Moobius.sign_out:

Moobius.sign_out
---------------------------------------------------------------------------------------------------------------------
Moobius.sign_out(self)

Calls self.http_api.sign_out.
Doc for the called function:
Signs out using the access token obtained from signing in. Returns None.

.. _moobius.core.sdk.Moobius.update_current_user:

Moobius.update_current_user
---------------------------------------------------------------------------------------------------------------------
Moobius.update_current_user(self, avatar, description, name)

Calls self.http_api.update_current_user.
Doc for the called function:
Updates the user info. Used by agents.

Parameters:
  avatar: Link to image or local filepath to upload.
  description: Of the user.
  name: The name that shows in chat.

No return value.

.. _moobius.core.sdk.Moobius.update_puppet:

Moobius.update_puppet
---------------------------------------------------------------------------------------------------------------------
Moobius.update_puppet(self, puppet_id, avatar, description, name)

Calls self.http_api.update_puppet using self.client_id.
Doc for the called function:
Updates the characters name, avatar, etc for a FAKE user, for real users use update_current_user.

Parameters:
  service_id (str): Which service holds the user.
  character_id (str): Who to update. Can also be a Character object. Cannot be a list.
  avatar (str): A link to user's image or a local filepath to upload.
  description (str): The description of user.
  name (str): The name that will show in chat.

Returns:
 Data about the user as a dict.

.. _moobius.core.sdk.Moobius.update_channel:

Moobius.update_channel
---------------------------------------------------------------------------------------------------------------------
Moobius.update_channel(self, channel_id, channel_name, channel_desc)

Calls self.http_api.update_channel.
Doc for the called function:
Updates a channel group.

Parameters:
  channel_id (str): The id of the group leader?
  group_name (str): What to call it.
  members (list): A list of character_id strings that will be inside the group.

No return value.

.. _moobius.core.sdk.Moobius.bind_service_to_channel:

Moobius.bind_service_to_channel
---------------------------------------------------------------------------------------------------------------------
Moobius.bind_service_to_channel(self, channel_id)

Calls self.http_api.bind_service_to_channel
Doc for the called function:
Binds a service to a channel given the service and channel IDs.
This function is unusual in that it returns whether it was sucessful rather than raising errors if it fails.

.. _moobius.core.sdk.Moobius.unbind_service_from_channel:

Moobius.unbind_service_from_channel
---------------------------------------------------------------------------------------------------------------------
Moobius.unbind_service_from_channel(self, channel_id)

Calls self.http_api.unbind_service_from_channel
Doc for the called function:
Unbinds a service to a channel given the service and channel IDs. Returns None.

.. _moobius.core.sdk.Moobius.create_puppet:

Moobius.create_puppet
---------------------------------------------------------------------------------------------------------------------
Moobius.create_puppet(self, name, avatar, description)

Calls self.http_api.create_puppet using self.create_puppet.
Doc for the called function:
Creates a character with a given name, avatar, and description.
The created user will be bound to the given service.

Parameters:
  service_id (str): The service_id/client_id.
  name (str): The name of the user.
  avatar (str): The image URL of the user's picture OR a local file path.
  description (str): The description of the user.

Returns: A Character object representing the created user.

.. _moobius.core.sdk.Moobius.fetch_popular_channels:

Moobius.fetch_popular_channels
---------------------------------------------------------------------------------------------------------------------
Moobius.fetch_popular_channels(self)

Calls self.http_api.fetch_popular_channels.
Doc for the called function:
Fetches the popular channels, returning a list of channel_id strings.

.. _moobius.core.sdk.Moobius.fetch_channel_list:

Moobius.fetch_channel_list
---------------------------------------------------------------------------------------------------------------------
Moobius.fetch_channel_list(self)

Calls self.http_api.fetch_channel_list.
Doc for the called function:
Fetches all? channels, returning a list of channel_id strings.

.. _moobius.core.sdk.Moobius.fetch_member_ids:

Moobius.fetch_member_ids
---------------------------------------------------------------------------------------------------------------------
Moobius.fetch_member_ids(self, channel_id, raise_empty_list_err)

Calls self.http_api.fetch_member_ids using self.client_id.
Doc for the called function:
Fetches the member ids of a channel which coorespond to real users.

Parameters:
  channel_id (str): The channel ID.
  service_id (str): The service/client/agent ID.
  raise_empty_list_err=False: Raises an Exception if the list is empty.

Returns:
 A list of character_id strings.

Raises:
  An Exception (empty list) if raise_empty_list_err is True and the list is empty.

.. _moobius.core.sdk.Moobius.fetch_character_profile:

Moobius.fetch_character_profile
---------------------------------------------------------------------------------------------------------------------
Moobius.fetch_character_profile(self, character_id)

Calls self.http_api.fetch_character_profile
Doc for the called function:
Returns a Character object (or list therof) given a string-valued (or list-valued) character_id.
It works for both member_ids and puppet_ids.

.. _moobius.core.sdk.Moobius.fetch_service_id_list:

Moobius.fetch_service_id_list
---------------------------------------------------------------------------------------------------------------------
Moobius.fetch_service_id_list(self)

Calls self.http_api.fetch_service_id_list
Doc for the called function:
Returns a list of service_id strings of the user.

.. _moobius.core.sdk.Moobius.fetch_puppets:

Moobius.fetch_puppets
---------------------------------------------------------------------------------------------------------------------
Moobius.fetch_puppets(self)

Calls self.http_api.fetch_puppets using self.client_id.
Doc for the called function:
Gets all the puppets defined for this service, returning a list of Character objects.

.. _moobius.core.sdk.Moobius.upload_file:

Moobius.upload_file
---------------------------------------------------------------------------------------------------------------------
Moobius.upload_file(self, filepath)

Calls self.http_api.upload_file. Note that uploads happen automatically for any function that accepts a filepath/url when given a local path.
Doc for the called function:
Uploads the file at local path file_path to the Moobius server. Automatically calculates the upload URL and upload fields.
Returns the uploaded URL. Raises an Exception if the upload fails.

.. _moobius.core.sdk.Moobius.download_file:

Moobius.download_file
---------------------------------------------------------------------------------------------------------------------
Moobius.download_file(self, url, filepath, assert_no_overwrite, headers)

Calls self.http_api.download_file
Doc for the called function:
Downloads a file from a url to a local filename, automatically creating dirs and overwriting pre-existing files.
If filename is None it will return the bytes and not save any file instead.

.. _moobius.core.sdk.Moobius.fetch_message_history:

Moobius.fetch_message_history
---------------------------------------------------------------------------------------------------------------------
Moobius.fetch_message_history(self, channel_id, limit, before)

Calls self.http_api.fetch_message_history.
Doc for the called function:
Returns the message chat history.

Parameters:
  channel_id (str): Channel with the messages inside of it.
  limit=64: Max number of messages to return (messages further back in time, if any, will not be returned).
  before="null": Only return messages older than this.

Returns a list of dicts.

.. _moobius.core.sdk.Moobius.create_channel_group:

Moobius.create_channel_group
---------------------------------------------------------------------------------------------------------------------
Moobius.create_channel_group(self, channel_id, group_name, members)

Calls self.http_api.create_channel_group.
Doc for the called function:
Creates a channel group.

Parameters:
  channel_id (str): The id of the group leader?
  group_name (str): What to call it.
  characters (list): A list of channel_id strings that will be inside the group.

Returns:
  The group_id string.

.. _moobius.core.sdk.Moobius.create_service_group:

Moobius.create_service_group
---------------------------------------------------------------------------------------------------------------------
Moobius.create_service_group(self, group_id, members)

Calls self.http_api.create_service_group.
Doc for the called function:
Creates a group containing the list of characters_ids and returns this Group object.
This group can then be used in send_message_down payloads.

Parameters:
  group_name (str): What to call it.
  character_ids (list): A list of character_id strings or Characters that will be inside the group.

Returns:
  A Group object.

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

Returns the character_id list.

.. _moobius.core.sdk.Moobius.character_ids_of_service_group:

Moobius.character_ids_of_service_group
---------------------------------------------------------------------------------------------------------------------
Moobius.character_ids_of_service_group(self, group_id)

Calls self.http_api.character_ids_of_service_group
Doc for the called function:
Gets a list of character ids belonging to a service group.
Note that the 'recipients' in 'on message up' might be None:
  To avoid requiring checks for None this function will return an empty list given Falsey inputs or Falsey string literals.

.. _moobius.core.sdk.Moobius.update_channel_group:

Moobius.update_channel_group
---------------------------------------------------------------------------------------------------------------------
Moobius.update_channel_group(self, channel_id, group_id, members)

Calls self.http_api.update_channel_group.
Doc for the called function:
Updates a channel group.

Parameters:
  channel_id (str): The id of the group leader?
  group_name (str): What to call it.
  members (list): A list of character_id strings that will be inside the group.

No return value.

.. _moobius.core.sdk.Moobius.update_temp_channel_group:

Moobius.update_temp_channel_group
---------------------------------------------------------------------------------------------------------------------
Moobius.update_temp_channel_group(self, channel_id, members)

Calls self.http_api.update_temp_channel_group.
Doc for the called function:
Updates a channel TEMP group.

Parameters:
  channel_id (str): The id of the group leader?
  members (list): A list of character_id strings that will be inside the group.

No return value.

.. _moobius.core.sdk.Moobius.fetch_channel_temp_group:

Moobius.fetch_channel_temp_group
---------------------------------------------------------------------------------------------------------------------
Moobius.fetch_channel_temp_group(self, channel_id)

Calls self.http_api.fetch_channel_temp_group.
Doc for the called function:
Like fetch_channel_group_list but for TEMP groups.

.. _moobius.core.sdk.Moobius.fetch_channel_group_list:

Moobius.fetch_channel_group_list
---------------------------------------------------------------------------------------------------------------------
Moobius.fetch_channel_group_list(self, channel_id)

Calls self.http_api.fetch_target_group.
Doc for the called function:
Not yet implemented!
Fetches info about the group.

  Parameters:
    user_id (str), channel_id (str): why needed?
    group_id (str): Which group to fetch.

  Returns:
    The data-dict data.

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
    channel_id (str): The channel ID. (TODO: of what?)
    group_id (str): The group ID.

Returns:
    The user profile Character object.

.. _moobius.core.sdk.Moobius.fetch_target_group:

Moobius.fetch_target_group
---------------------------------------------------------------------------------------------------------------------
Moobius.fetch_target_group(self, user_id, channel_id, group_id)

Calls self.http_api.fetch_target_group.
Doc for the called function:
Not yet implemented!
Fetches info about the group.

  Parameters:
    user_id (str), channel_id (str): why needed?
    group_id (str): Which group to fetch.

  Returns:
    The data-dict data.

.. _moobius.core.sdk.Moobius.send_agent_login:

Moobius.send_agent_login
---------------------------------------------------------------------------------------------------------------------
Moobius.send_agent_login(self)

Calls self.ws_client.agent_login using self.http_api.access_token; one of the agent vs service differences.
Doc for the called function:
Logs-in agents.
Every 2h AWS will force-disconnect, so it is a good idea to send agent_login on connect.

Parameters:
  access_token: Used in the user_login message that is sent.
    This is the access token from http_api_wrapper.
  dry_run=False: Don't acually send anything if True.

Returns: The message as a dict.

.. _moobius.core.sdk.Moobius.send_service_login:

Moobius.send_service_login
---------------------------------------------------------------------------------------------------------------------
Moobius.send_service_login(self)

Calls self.ws_client.service_login using self.client_id and self.http_api.access_token; one of the agent vs service differences.
Doc for the called function:
Logs in. Much like the HTTP api, this needs to be sent before any other messages.

Parameters:
  service_id (str): The client_id of a Moobius service object, which is the ID of the running service.
    Used in almost every function.
  access_token (str):
    TODO: This is the access token from http_api_wrapper; for clean code decouple access_token here!
  dry_run=False: Don't acually send anything (must functions offer a dry-run option)

Returns:
  The message as a dict.

.. _moobius.core.sdk.Moobius.send_update:

Moobius.send_update
---------------------------------------------------------------------------------------------------------------------
Moobius.send_update(self, target_client_id, data)

Calls self.ws_client.update
Doc for the called function:
A generic update function that is rarely used.

Parameters:
  service_id (str): As always.
  target_client_id (str): The target client id (TODO: not currently used)
  data (dict): The content of the update.
  dry_run=False: Don't acually send anything if True.

Returns: The message as a dict.

.. _moobius.core.sdk.Moobius.send_update_characters:

Moobius.send_update_characters
---------------------------------------------------------------------------------------------------------------------
Moobius.send_update_characters(self, channel_id, character_ids, recipients)

Calls self.ws_client.update_character_list using self.client_id. Converts recipients to a group_id if a list.
Doc for the called function:
Updates the characters that the recipients see.

Parameters:
  service_id (str): As always.
  channel_id (str): The channel id.
  characters (str): The group id to represent the characters who are updated.
  recipients (str): The group id to send to.
  dry_run=False: if True don't acually send the message (messages are sent in thier JSON-strin format).

Returns:
  The message as a dict.

.. _moobius.core.sdk.Moobius.send_update_channel_info:

Moobius.send_update_channel_info
---------------------------------------------------------------------------------------------------------------------
Moobius.send_update_channel_info(self, channel_id, channel_info)

Calls self.ws_client.update_channel_info using self.client_id.
Doc for the called function:
Updates the channel name, description, etc for a given channel.

Parameters:
  service_id (str): As always.
  channel_id (str): The channel id.
  channel_info (ChannelInfo or dict): The data of the update.
  dry_run=False: Don't acually send anything if True.

Returns: The message as a dict.

Example:
  >>> ws_client.update_channel_info("service_id", "channel_id", {"name": "new_channel_name"})

.. _moobius.core.sdk.Moobius.send_update_buttons:

Moobius.send_update_buttons
---------------------------------------------------------------------------------------------------------------------
Moobius.send_update_buttons(self, channel_id, buttons, recipients)

Calls self.ws_client.update_buttons using self.client_id. Converts recipients to a group_id if a list.
Doc for the called function:
Updates the buttons that the recipients see.

Parameters:
  service_id (str): As always.
  channel_id (str): The channel id.
  buttons (list of Buttons): The buttons list to be updated.
  recipients (str): The group id to send to.
  dry_run=False: Don't acually send anything if True.

Returns:
  The message as a dict.

Example:
  >>> continue_button =
  >>>   {"button_name": "Continue Playing", "button_id": "play",
  >>>    "button_name": "Continue Playing", "new_window": False,
  >>>    "arguments": []}
  >>> ws_client.update_buttons("service_id", "channel_id", [continue_button], ["user1", "user2"])

.. _moobius.core.sdk.Moobius.send_update_context_menu:

Moobius.send_update_context_menu
---------------------------------------------------------------------------------------------------------------------
Moobius.send_update_context_menu(self, channel_id, menu_elements, recipients)

Calls self.ws_client.update_context_menu using self.client_id. Converts recipients to a group_id if a list.
Doc for the called function:
Updates the right-click menu that the recipients can open on various messages.

Parameters:
  service_id (str): As always.
  channel_id (str): The channel id.
  menu_items (list): List of ContextMenuElement dataclasses.

Returns:
  The message as a dict.

.. _moobius.core.sdk.Moobius.send_update_style:

Moobius.send_update_style
---------------------------------------------------------------------------------------------------------------------
Moobius.send_update_style(self, channel_id, style_content, recipients)

Calls self.ws_client.update_style using self.client_id. Converts recipients to a group_id if a list.
Doc for the called function:
Updates the style (whehter the canvas is expanded, other look-and-feel aspects) that the recipients see.

Parameters:
  service_id (str): As always.
  channel_id (str): The channel id.
  style_content (list of dicts): The style content to be updated. TODO: List of Style classes.
  recipients (str): The group id to send to.
  dry_run=False: Don't acually send anything if True.

Returns:
  The message as a dict.

Example:
    >>> style_content = [
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
    >>> ws_client.update_style("service_id", "channel_id", style_content, ["user1", "user2"])

.. _moobius.core.sdk.Moobius.send_fetch_characters:

Moobius.send_fetch_characters
---------------------------------------------------------------------------------------------------------------------
Moobius.send_fetch_characters(self, channel_id)

Calls self.ws_client.fetch_characters using self.client_id.
Doc for the called function:
Asks for the list of characters. The socket will send back a message with the information later.

Parameters (these are common to most fetch messages):
  user_id (str): Used in the "action" message that is sent.
  channel_id (str): Used in the body of said message.
  dry_run=False: Don't acually send anything if True.

Returns:
  The message that was sent as a dict.

.. _moobius.core.sdk.Moobius.send_fetch_buttons:

Moobius.send_fetch_buttons
---------------------------------------------------------------------------------------------------------------------
Moobius.send_fetch_buttons(self, channel_id)

Calls self.ws_client.fetch_buttons using self.client_id.
Doc for the called function:
Same usage as fetch_characters but for the buttons.
These functions return the sent message, the actual response will come later.

.. _moobius.core.sdk.Moobius.send_fetch_style:

Moobius.send_fetch_style
---------------------------------------------------------------------------------------------------------------------
Moobius.send_fetch_style(self, channel_id)

Calls self.ws_client.fetch_style using self.client_id.
Doc for the called function:
Same usage as fetch_characters but for the style.
These functions return the sent message, the actual response will come later.

.. _moobius.core.sdk.Moobius.send_fetch_canvas:

Moobius.send_fetch_canvas
---------------------------------------------------------------------------------------------------------------------
Moobius.send_fetch_canvas(self, channel_id)

Calls self.ws_client.fetch_canvas using self.client_id.
Doc for the called function:
Same usage as fetch_characters but for the canvas.
These functions return the sent message, the actual response will come later.

.. _moobius.core.sdk.Moobius.send_fetch_channel_info:

Moobius.send_fetch_channel_info
---------------------------------------------------------------------------------------------------------------------
Moobius.send_fetch_channel_info(self, channel_id)

Calls self.ws_client.fetch_channel_info using self.client_id.
Doc for the called function:
Same usage as fetch_characters but for the channel_info.
These functions return the sent message, the actual response will come later.

.. _moobius.core.sdk.Moobius.send_join_channel:

Moobius.send_join_channel
---------------------------------------------------------------------------------------------------------------------
Moobius.send_join_channel(self, channel_id)

Calls self.ws_client.join_channel using self.client_id. Used by agents.
Doc for the called function:
Joins the channel with channel_id, unless dry_run is True. Used by agents. Returns the message dict.

.. _moobius.core.sdk.Moobius.send_leave_channel:

Moobius.send_leave_channel
---------------------------------------------------------------------------------------------------------------------
Moobius.send_leave_channel(self, channel_id)

Calls self.ws_client.leave_channel using self.client_id. Used by agents.
Doc for the called function:
Leaves the channel with channel_id, unless dry_run is True. Used by agents. Returns the message dict.

.. _moobius.core.sdk.Moobius.checkin:

Moobius.checkin
---------------------------------------------------------------------------------------------------------------------
Moobius.checkin(self)

Called as a rate task, used to resync users, etc. Only called after on_start()

.. _moobius.core.sdk.Moobius.listen_loop:

Moobius.listen_loop
---------------------------------------------------------------------------------------------------------------------
Moobius.listen_loop(self)

Listens to the wand in an infinite loop, polling self.queue (which is an aioprocessing.AioQueue).
This allows the wand to send "spells" (messages) to the services at any time.

.. _moobius.core.sdk.Moobius.handle_received_payload:

Moobius.handle_received_payload
---------------------------------------------------------------------------------------------------------------------
Moobius.handle_received_payload(self, payload)

Decodes the received websocket payload JSON and calls the handler based on p['type']. Returns None.
Example methods called:
  on_message_up(), on_action(), on_button_click(), on_copy_client(), on_unknown_payload()

Example use-case:
  >>> self.ws_client = WSClient(ws_server_uri, on_connect=self.send_service_login, handle=self.handle_received_payload)

.. _moobius.core.sdk.Moobius.on_action:

Moobius.on_action
---------------------------------------------------------------------------------------------------------------------
Moobius.on_action(self, action)

Handles an action (Action object) from a user. Returns None.
Calls the corresponding method to handle different subtypes of action.
Example methods called:
  on_fetch_characters(), on_fetch_buttons(), on_fetch_canvas(), on_join_channel(), on_leave_channel(), on_fetch_channel_info()

.. _moobius.core.sdk.Moobius.on_update:

Moobius.on_update
---------------------------------------------------------------------------------------------------------------------
Moobius.on_update(self, update)

Dispatches an Update object to one of various callbacks. Agent function.
It is recommended to overload the invididual callbacks instead of this function.

.. _moobius.core.sdk.Moobius.on_start:

Moobius.on_start
---------------------------------------------------------------------------------------------------------------------
Moobius.on_start(self)

Called when the service is initialized. Returns None

.. _moobius.core.sdk.Moobius.initialize_channel:

Moobius.initialize_channel
---------------------------------------------------------------------------------------------------------------------
Moobius.initialize_channel(self, channel_id)

Called once per channel on startup. Returns None.
By default, if self.db_config has been set, a MoobiusStorage is created in self.channel_storages

.. _moobius.core.sdk.Moobius.checkin_channel:

Moobius.checkin_channel
---------------------------------------------------------------------------------------------------------------------
Moobius.checkin_channel(self, channel_id)

A "wellness check" which is called on startup, on reconnect, and as a periodic "check-in". Returns None.

.. _moobius.core.sdk.Moobius.on_spell:

Moobius.on_spell
---------------------------------------------------------------------------------------------------------------------
Moobius.on_spell(self, obj)

Called when a "spell" from the wand is received, which can be any object but is often a string. Returns None.

.. _moobius.core.sdk.Moobius.on_message_up:

Moobius.on_message_up
---------------------------------------------------------------------------------------------------------------------
Moobius.on_message_up(self, message_up)

Called when a user sends a message. Returns None.
Example MessageBody object:
>>>  moobius.MessageBody(subtype="text", channel_id=<channel id>, content=MessageContent(...), timestamp=1707254706635,
>>>                      recipients=[<user id 1>, <user id 2>], sender=<user id>, message_id=<message-id>,
>>>                      context={'group_id': <group-id>, 'channel_type': 'ccs'})

.. _moobius.core.sdk.Moobius.on_fetch_buttons:

Moobius.on_fetch_buttons
---------------------------------------------------------------------------------------------------------------------
Moobius.on_fetch_buttons(self, action)

Called when the user's browser requests the list of buttons. Returns None.
This and other "on_fetch_xyz" functions are commonly overriden to call "send_update_xyz" with the needed material.
Example Action object:
>>> moobius.Action(subtype="fetch_buttons", channel_id=<channel id>, sender=<user id>, context={})

.. _moobius.core.sdk.Moobius.on_fetch_characters:

Moobius.on_fetch_characters
---------------------------------------------------------------------------------------------------------------------
Moobius.on_fetch_characters(self, action)

Called when the user's browser requests the list of characters that they will be able to see and send messages to. Returns None.
Example Action object:
>>> moobius.Action(subtype="fetch_characters", channel_id=<channel id>, sender=<user id>, context={}).

.. _moobius.core.sdk.Moobius.on_fetch_canvas:

Moobius.on_fetch_canvas
---------------------------------------------------------------------------------------------------------------------
Moobius.on_fetch_canvas(self, action)

Called when the user's browser requests the content of the canvas. Returns None.
Example Action object:
>>> moobius.Action(subtype="fetch_canvas", channel_id=<channel id>, sender=<user id>, context={})

.. _moobius.core.sdk.Moobius.on_fetch_context_menu:

Moobius.on_fetch_context_menu
---------------------------------------------------------------------------------------------------------------------
Moobius.on_fetch_context_menu(self, action)

Called when the user's browser requests the content of the right-click menu. Returns None.
Example Action object:
>>> moobius.Action(subtype="fetch_context_menu", channel_id=<channel id>, sender=<user id>, context={})

.. _moobius.core.sdk.Moobius.on_fetch_channel_info:

Moobius.on_fetch_channel_info
---------------------------------------------------------------------------------------------------------------------
Moobius.on_fetch_channel_info(self, action)

Called when the user's browser requests information about a channel. Returns None.
Example Action object:
>>> moobius.Action(subtype="fetch_channel_info", channel_id=<channel id>, sender=<user id>, context={})

.. _moobius.core.sdk.Moobius.on_copy_client:

Moobius.on_copy_client
---------------------------------------------------------------------------------------------------------------------
Moobius.on_copy_client(self, copy)

Handles a "Copy" request bade by the user's browser. Returns None.
Example Copy object:
>>> moobius.Copy(request_id=<id>, origin_type=message_down, status=True, context={'message': 'Message received'})

.. _moobius.core.sdk.Moobius.on_join_channel:

Moobius.on_join_channel
---------------------------------------------------------------------------------------------------------------------
Moobius.on_join_channel(self, action)

Called when the user joins a channel. Returns None.
Commonly used to inform everyone about this new user and update everyone's character list.
Example Action object:
>>> moobius.Action(subtype="join_channel", channel_id=<channel id>, sender=<user id>, context={})

.. _moobius.core.sdk.Moobius.on_leave_channel:

Moobius.on_leave_channel
---------------------------------------------------------------------------------------------------------------------
Moobius.on_leave_channel(self, action)

Called when the user leaves a channel. Returns None.
Commonly used to update everyone's character list.
Example Action object:
>>> moobius.Action(subtype="leave_channel", channel_id=<channel id>, sender=<user id>, context={})

.. _moobius.core.sdk.Moobius.on_button_click:

Moobius.on_button_click
---------------------------------------------------------------------------------------------------------------------
Moobius.on_button_click(self, button_click)

Handles a button click from a user, usually performing some action. Returns None.
Example ButtonClick object:
>>> moobius.ButtonClick(button_id="the_big_red_button", channel_id=<channel id>, sender=<user id>, arguments=[], context={})

.. _moobius.core.sdk.Moobius.on_context_menu_click:

Moobius.on_context_menu_click
---------------------------------------------------------------------------------------------------------------------
Moobius.on_context_menu_click(self, context_click)

Handles a context menu right click from a user, usually performing some action. Returns None.
Example MenuClick object:
>>> MenuClick(item_id=1, message_id=<id>, message_subtype=text, message_content={'text': 'Click on this message.'}, channel_id=<channel_id>, context={}, recipients=[])

.. _moobius.core.sdk.Moobius.on_unknown_payload:

Moobius.on_unknown_payload
---------------------------------------------------------------------------------------------------------------------
Moobius.on_unknown_payload(self, payload)

A catch-all for handling unknown Payload objects. Returns None.

.. _moobius.core.sdk.Moobius.on_message_down:

Moobius.on_message_down
---------------------------------------------------------------------------------------------------------------------
Moobius.on_message_down(self, message_down)

Callback when a message is recieved (a MessageBody object similar to what on_message_up gets).
Agent function. Returns None.

.. _moobius.core.sdk.Moobius.on_update_characters:

Moobius.on_update_characters
---------------------------------------------------------------------------------------------------------------------
Moobius.on_update_characters(self, update)

Responds to changes to the character list. One of the multiple update callbacks. Returns None.
Agent function. Update is an Update instance.

.. _moobius.core.sdk.Moobius.on_update_channel_info:

Moobius.on_update_channel_info
---------------------------------------------------------------------------------------------------------------------
Moobius.on_update_channel_info(self, update)

Responds to changes to the channel info. One of the multiple update callbacks. Returns None.
Agent function. Update is an Update instance.

.. _moobius.core.sdk.Moobius.on_update_canvas:

Moobius.on_update_canvas
---------------------------------------------------------------------------------------------------------------------
Moobius.on_update_canvas(self, update)

Responds to changes to the canvas. One of the multiple update callbacks. Returns None.
Agent function. Update is an Update instance.

.. _moobius.core.sdk.Moobius.on_update_buttons:

Moobius.on_update_buttons
---------------------------------------------------------------------------------------------------------------------
Moobius.on_update_buttons(self, update)

Responds to changes to the buttons. One of the multiple update callbacks. Returns None.
Agent function. Update is an Update instance.

.. _moobius.core.sdk.Moobius.on_update_style:

Moobius.on_update_style
---------------------------------------------------------------------------------------------------------------------
Moobius.on_update_style(self, update)

Responds to changes to the style (look and feel). One of the multiple update callbacks. Returns None.
Agent function. Update is an Update instance.

.. _moobius.core.sdk.Moobius.on_update_context_menu:

Moobius.on_update_context_menu
---------------------------------------------------------------------------------------------------------------------
Moobius.on_update_context_menu(self, update)

Responds to changes to the context menu. One of the multiple update callbacks. Returns None.
Agent function. Update is an Update instance.

.. _moobius.core.sdk.Moobius.__str__:

Moobius.__str__
---------------------------------------------------------------------------------------------------------------------
Moobius.__str__(self)

<No doc string>

.. _moobius.core.sdk.Moobius.__repr__:

Moobius.__repr__
---------------------------------------------------------------------------------------------------------------------
Moobius.__repr__(self)

<No doc string>

.. _moobius.core.sdk.Moobius.send_message._get_file_message_content:

Moobius.send_message._get_file_message_content
---------------------------------------------------------------------------------------------------------------------
Moobius.send_message._get_file_message_content(filepath, file_display_name, subtype)

Converts a filepath into a MessageContent object, uploading files if need be.

.. _moobius.core.sdk.Moobius.handle_received_payload._group2ids:

Moobius.handle_received_payload._group2ids
---------------------------------------------------------------------------------------------------------------------
Moobius.handle_received_payload._group2ids(g_id)

<No doc string>

.. _moobius.core.sdk.Moobius.start._get_agent_info:

Moobius.start._get_agent_info
---------------------------------------------------------------------------------------------------------------------
Moobius.start._get_agent_info()

<No doc string>

.. _moobius.core.sdk.Moobius.handle_received_payload._make_elem:

Moobius.handle_received_payload._make_elem
---------------------------------------------------------------------------------------------------------------------
Moobius.handle_received_payload._make_elem(d)

<No doc string>
