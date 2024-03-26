.. _moobius_core_sdk:

moobius.core.sdk
===================================



===================


Class ServiceGroupLib
===================

Converts a list of character_ids into a service or channel group id, creating one if need be.
The lookup is O(n) so performance issues at extremly large list sizes are a theoretical possibility.

.. _moobius.core.sdk.ServiceGroupLib.__init__:
ServiceGroupLib.__init__
-----------------------------------
**ServiceGroupLib.__init__(self)**

<No doc string>

.. _moobius.core.sdk.ServiceGroupLib.convert_list:
ServiceGroupLib.convert_list
-----------------------------------
**ServiceGroupLib.convert_list(self, http_api, character_ids, is_message_down, channel_id)**

Converts a list to single group id unless it is already a group id.

Parameters:
  http_api: The http_api client in Moobius
  character_ids: List of ids. If a string, treated as a one element list.
  is_message_down: True = message_down (Service sends message), False = message_up (Agent sends message).
  channel_id=None: If None and the conversion still needs to happen it will raise an Exception.

Returns: The group id.



Class Moobius
===================

(No doc string)

.. _moobius.core.sdk.Moobius.__init__:
Moobius.__init__
-----------------------------------
**Moobius.__init__(self, config_path, db_config_path, is_agent, \*kwargs)**

Initialize a service or agent object.

Parameters:
  config_path: The path of the agent or service config file. Can also be a dict.
  db_config_path: The path of the database config file.
    Can also be a dict in which case no file will be loaded.
  is_agent=False: True for an agent, False for a service.
    Agents and services have slight differences in auth and how the platform reacts to them, etc.

No return value.

Example:
  >>> service = SDK(config_path="./config/service.json", db_config_path="./config/database.json", is_agent=False)

.. _moobius.core.sdk.Moobius.start:
Moobius.start
-----------------------------------
**Moobius.start(self)**

Start the Service/Agent. start() fns are called with wand.run. There are 6 steps:
  1. Authenticate.
  2. Connect to the websocket server.
  3. (if a Service) Bind the Service to the channels. If there is no service_id in the config file, create a new service and update the config file.
  4. Start the scheduler, run refresh(), authenticate(), send_heartbeat() periodically.
  5. Call the on_start() callback (override this method to perform your own initialization tasks).
  6. Start listening to the websocket and the Wand.

No parameters or return value.

.. _moobius.core.sdk.Moobius.agent_join_service_channels:
Moobius.agent_join_service_channels
-----------------------------------
**Moobius.agent_join_service_channels(self, service_config_fname)**

Joins service channels given by service config filename.

.. _moobius.core.sdk.Moobius.fetch_service_id_each_channel:
Moobius.fetch_service_id_each_channel
-----------------------------------
**Moobius.fetch_service_id_each_channel(self)**

Returns a dict of which service_id is each channel_id bound to. Channels can only be bound to a single service.
Channels not bound to any service will not be in the dict.

.. _moobius.core.sdk.Moobius.fetch_bound_channels:
Moobius.fetch_bound_channels
-----------------------------------
**Moobius.fetch_bound_channels(self)**

Returns a list of channels this Service is bound to.

.. _moobius.core.sdk.Moobius.fetch_characters:
Moobius.fetch_characters
-----------------------------------
**Moobius.fetch_characters(self, channel_id)**

Returns a list (or Character objects) with both the real caracters bound to channel_id
as well as fake virtual characters bound to, not a channel, but to service self.client_id.

.. _moobius.core.sdk.Moobius._convert_message_content:
Moobius._convert_message_content
-----------------------------------
**Moobius._convert_message_content(self, subtype, content)**

Converts message content, which can be a string (for text messages), to a MessageContent object.

.. _moobius.core.sdk.Moobius.initialize_channel:
Moobius.initialize_channel
-----------------------------------
**Moobius.initialize_channel(self, channel_id)**

Creates a MoobiusStorage object for a channel given by channel_id. Commonly overridden. Returns None.

.. _moobius.core.sdk.Moobius.upload_avatar_and_create_character:
Moobius.upload_avatar_and_create_character
-----------------------------------
**Moobius.upload_avatar_and_create_character(self, name, image_path, description)**

Upload an avatar image and create a character. Service function.

Parameters:
  name: str
    The name of the character.
  image_path: str
    The local path of the avatar image.
  description: str
    The description of the character.

Returns:
  The created character (Character object).

.. _moobius.core.sdk.Moobius.create_message:
Moobius.create_message
-----------------------------------
**Moobius.create_message(self, channel_id, message_content, recipients, subtype, sender, filename, size)**

Create a message_down (for Service) or message_up (for Agent) request and sends it to the channel.

Parameters:
  channel_id (str): The id of the channel.
  message_content (str or MessageContent): The text of the message such as "Hello everyone on this channel!" or file information.
    String-valued content is best for the text in a text message or a URI for an image file. It will be converted to a dict.
  recipients (list or string): The recipients character_id list or group_id string of the message.
    This choice of list vs string is the case whenever there is a "recipients" argument in a Moobius method.
  subtype=types.TEXT: The subtype of the message.
  sender=None: The sender of the message. None for Agents.
  filename=None: Optional, name to display files as.
  size=None: Optional, number of bytes in file.

No return value.

.. _moobius.core.sdk.Moobius.upload_file_in_message:
Moobius.upload_file_in_message
-----------------------------------
**Moobius.upload_file_in_message(self, channel_id, local_path, recipients, sender, file_display_name)**

Uploads a file and sends the uploaded file as a message.
Recognized image or audio extensions will render as the image or sound, other files will have to be downloaded to see.

Parameters:
  channel_id: The id of the channel.
  local_path: The local path to the file.
  recipients (list or string): The recipients character_id list or group_id string of the message.
  sender: The sender of the message. None for Agents.
  file_display_name=None: Optional, will use

.. _moobius.core.sdk.Moobius.convert_and_send_message:
Moobius.convert_and_send_message
-----------------------------------
**Moobius.convert_and_send_message(self, message_body)**

Converts the message body into a message down or message up object and sends it.
Agents send message_up and Services send message_down.

.. _moobius.core.sdk.Moobius.send:
Moobius.send
-----------------------------------
**Moobius.send(self, payload_type, payload_body)**

Send any kind of payload, including message_down, update, update_characters, update_channel_info, update_canvas, update_buttons, update_style, and heartbeat.

Parameters:
  payload_type (str): The type of the payload.
  payload_body (dict or str): The body of the payload.
    Strings will be converted into a Payload object.

No return value.

.. _moobius.core.sdk.Moobius.send_button_click:
Moobius.send_button_click
-----------------------------------
**Moobius.send_button_click(self, channel_id, button_id, button_args)**

Use to send a request to ask for a button call.

Parameters:
  channel_id (str): Which channel.
  button_id (str): Which button.
  button_args (list of k-v pairs, not a dict): What about said button should be fetched?

No return value.

.. _moobius.core.sdk.Moobius.send_heartbeat:
Moobius.send_heartbeat
-----------------------------------
**Moobius.send_heartbeat(self)**

Sends a heartbeat to the server. Return None

.. _moobius.core.sdk.Moobius.create_and_bind_channel:
Moobius.create_and_bind_channel
-----------------------------------
**Moobius.create_and_bind_channel(self, channel_name, channel_desc)**

Create a channel with the provided name and description and binds self.client_id (the service_id) to it.
(I think) a Service function. Returns the channel id.

.. _moobius.core.sdk.Moobius._update_rec:
Moobius._update_rec
-----------------------------------
**Moobius._update_rec(self, recipients, is_m_down, channel_id)**

Pass in await self._update_rec(recipients) into "recipients".
Converts lists into group_id strings, creating a group if need be.

.. _moobius.core.sdk.Moobius.refresh:
Moobius.refresh
-----------------------------------
**Moobius.refresh(self)**

Calls self.http_api.refresh.

.. _moobius.core.sdk.Moobius.authenticate:
Moobius.authenticate
-----------------------------------
**Moobius.authenticate(self)**

Calls self.http_api.authenticate.

.. _moobius.core.sdk.Moobius.sign_up:
Moobius.sign_up
-----------------------------------
**Moobius.sign_up(self)**

Calls self.http_api.sign_up.

.. _moobius.core.sdk.Moobius.sign_out:
Moobius.sign_out
-----------------------------------
**Moobius.sign_out(self)**

Calls self.http_api.sign_out.

.. _moobius.core.sdk.Moobius.update_current_user:
Moobius.update_current_user
-----------------------------------
**Moobius.update_current_user(self, avatar, description, name)**

Calls self.http_api.update_current_user.

.. _moobius.core.sdk.Moobius.update_character:
Moobius.update_character
-----------------------------------
**Moobius.update_character(self, character_id, avatar, description, name)**

Calls self.http_api.update_character using self.client_id.

.. _moobius.core.sdk.Moobius.update_channel:
Moobius.update_channel
-----------------------------------
**Moobius.update_channel(self, channel_id, channel_name, channel_desc)**

Calls self.http_api.update_channel.

.. _moobius.core.sdk.Moobius.create_channel:
Moobius.create_channel
-----------------------------------
**Moobius.create_channel(self, channel_name, channel_desc)**

Calls self.http_api.create_channel

.. _moobius.core.sdk.Moobius.bind_service_to_channel:
Moobius.bind_service_to_channel
-----------------------------------
**Moobius.bind_service_to_channel(self, channel_id)**

Calls self.http_api.bind_service_to_channel

.. _moobius.core.sdk.Moobius.unbind_service_from_channel:
Moobius.unbind_service_from_channel
-----------------------------------
**Moobius.unbind_service_from_channel(self, channel_id)**

Calls self.http_api.unbind_service_from_channel

.. _moobius.core.sdk.Moobius.create_character:
Moobius.create_character
-----------------------------------
**Moobius.create_character(self, name, avatar, description)**

Calls self.http_api.create_character using self.create_character.

.. _moobius.core.sdk.Moobius.fetch_popular_channels:
Moobius.fetch_popular_channels
-----------------------------------
**Moobius.fetch_popular_channels(self)**

Calls self.http_api.fetch_popular_channels.

.. _moobius.core.sdk.Moobius.fetch_channel_list:
Moobius.fetch_channel_list
-----------------------------------
**Moobius.fetch_channel_list(self)**

Calls self.http_api.fetch_channel_list.

.. _moobius.core.sdk.Moobius.fetch_real_character_ids:
Moobius.fetch_real_character_ids
-----------------------------------
**Moobius.fetch_real_character_ids(self, channel_id, raise_empty_list_err)**

Calls self.http_api.fetch_real_character_ids using self.client_id.

.. _moobius.core.sdk.Moobius.fetch_character_profile:
Moobius.fetch_character_profile
-----------------------------------
**Moobius.fetch_character_profile(self, character_id)**

Calls self.http_api.fetch_character_profile

.. _moobius.core.sdk.Moobius.fetch_service_id_list:
Moobius.fetch_service_id_list
-----------------------------------
**Moobius.fetch_service_id_list(self)**

Calls self.http_api.fetch_service_id_list

.. _moobius.core.sdk.Moobius.fetch_service_characters:
Moobius.fetch_service_characters
-----------------------------------
**Moobius.fetch_service_characters(self)**

Calls self.http_api.fetch_service_characters using self.client_id.

.. _moobius.core.sdk.Moobius.upload_file:
Moobius.upload_file
-----------------------------------
**Moobius.upload_file(self, filepath)**

Calls self.http_api.upload_file.

.. _moobius.core.sdk.Moobius.fetch_message_history:
Moobius.fetch_message_history
-----------------------------------
**Moobius.fetch_message_history(self, channel_id, limit, before)**

Calls self.http_api.fetch_message_history.

.. _moobius.core.sdk.Moobius.create_channel_group:
Moobius.create_channel_group
-----------------------------------
**Moobius.create_channel_group(self, channel_id, group_name, members)**

Calls self.http_api.create_channel_group.

.. _moobius.core.sdk.Moobius.create_service_group:
Moobius.create_service_group
-----------------------------------
**Moobius.create_service_group(self, group_id, members)**

Calls self.http_api.create_service_group.

.. _moobius.core.sdk.Moobius.character_ids_of_channel_group:
Moobius.character_ids_of_channel_group
-----------------------------------
**Moobius.character_ids_of_channel_group(self, sender_id, channel_id, group_id)**

Calls self.http_api.character_ids_of_channel_group

.. _moobius.core.sdk.Moobius.character_ids_of_service_group:
Moobius.character_ids_of_service_group
-----------------------------------
**Moobius.character_ids_of_service_group(self, group_id)**

Calls self.http_api.character_ids_of_service_group

.. _moobius.core.sdk.Moobius.update_channel_group:
Moobius.update_channel_group
-----------------------------------
**Moobius.update_channel_group(self, channel_id, group_id, members)**

Calls self.http_api.update_channel_group.

.. _moobius.core.sdk.Moobius.update_temp_channel_group:
Moobius.update_temp_channel_group
-----------------------------------
**Moobius.update_temp_channel_group(self, channel_id, members)**

Calls self.http_api.update_temp_channel_group.

.. _moobius.core.sdk.Moobius.fetch_channel_temp_group:
Moobius.fetch_channel_temp_group
-----------------------------------
**Moobius.fetch_channel_temp_group(self, channel_id)**

Calls self.http_api.fetch_channel_temp_group.

.. _moobius.core.sdk.Moobius.fetch_channel_group_list:
Moobius.fetch_channel_group_list
-----------------------------------
**Moobius.fetch_channel_group_list(self, channel_id)**

Calls self.http_api.fetch_target_group.

.. _moobius.core.sdk.Moobius.fetch_user_from_group:
Moobius.fetch_user_from_group
-----------------------------------
**Moobius.fetch_user_from_group(self, user_id, channel_id, group_id)**

Calls self.http_api.fetch_user_from_group.

.. _moobius.core.sdk.Moobius.fetch_target_group:
Moobius.fetch_target_group
-----------------------------------
**Moobius.fetch_target_group(self, user_id, channel_id, group_id)**

Calls self.http_api.fetch_target_group.

.. _moobius.core.sdk.Moobius.send_agent_login:
Moobius.send_agent_login
-----------------------------------
**Moobius.send_agent_login(self)**

Calls self.ws_client.agent_login using self.http_api.access_token; one of the agent vs service differences.

.. _moobius.core.sdk.Moobius.send_service_login:
Moobius.send_service_login
-----------------------------------
**Moobius.send_service_login(self)**

Calls self.ws_client.service_login using self.client_id and self.http_api.access_token; one of the agent vs service differences.

.. _moobius.core.sdk.Moobius.send_message_up:
Moobius.send_message_up
-----------------------------------
**Moobius.send_message_up(self, channel_id, recipients, subtype, message_content)**

Calls self.ws_client.message_up using self.client_id. Converts recipients to a group_id if a list.

.. _moobius.core.sdk.Moobius.send_message_down:
Moobius.send_message_down
-----------------------------------
**Moobius.send_message_down(self, channel_id, recipients, subtype, message_content, sender)**

Calls self.ws_client using self.client_id. Converts recipients to a group_id if a list.

.. _moobius.core.sdk.Moobius.send_update:
Moobius.send_update
-----------------------------------
**Moobius.send_update(self, target_client_id, data)**

Calls self.ws_client.TODO

.. _moobius.core.sdk.Moobius.send_update_character_list:
Moobius.send_update_character_list
-----------------------------------
**Moobius.send_update_character_list(self, channel_id, character_list, recipients)**

Calls self.ws_client.update_character_list using self.client_id. Converts recipients to a group_id if a list.

.. _moobius.core.sdk.Moobius.send_update_channel_info:
Moobius.send_update_channel_info
-----------------------------------
**Moobius.send_update_channel_info(self, channel_id, channel_info)**

Calls self.ws_client.update_channel_info using self.client_id.

.. _moobius.core.sdk.Moobius.send_update_canvas:
Moobius.send_update_canvas
-----------------------------------
**Moobius.send_update_canvas(self, channel_id, canvas_elements, recipients)**

Calls self.ws_client.update_canvas using self.client_id. Converts recipients to a group_id if a list.

.. _moobius.core.sdk.Moobius.send_update_buttons:
Moobius.send_update_buttons
-----------------------------------
**Moobius.send_update_buttons(self, channel_id, buttons, recipients)**

Calls self.ws_client.update_buttons using self.client_id. Converts recipients to a group_id if a list.

.. _moobius.core.sdk.Moobius.send_update_context_menu:
Moobius.send_update_context_menu
-----------------------------------
**Moobius.send_update_context_menu(self, channel_id, menu_elements, recipients)**

Calls self.ws_client.update_context_menu using self.client_id. Converts recipients to a group_id if a list.

.. _moobius.core.sdk.Moobius.send_update_style:
Moobius.send_update_style
-----------------------------------
**Moobius.send_update_style(self, channel_id, style_content, recipients)**

Calls self.ws_client.update_style using self.client_id. Converts recipients to a group_id if a list.

.. _moobius.core.sdk.Moobius.send_fetch_characters:
Moobius.send_fetch_characters
-----------------------------------
**Moobius.send_fetch_characters(self, channel_id)**

Calls self.ws_client.fetch_characters using self.client_id.

.. _moobius.core.sdk.Moobius.send_fetch_buttons:
Moobius.send_fetch_buttons
-----------------------------------
**Moobius.send_fetch_buttons(self, channel_id)**

Calls self.ws_client.fetch_buttons using self.client_id.

.. _moobius.core.sdk.Moobius.send_fetch_style:
Moobius.send_fetch_style
-----------------------------------
**Moobius.send_fetch_style(self, channel_id)**

Calls self.ws_client.fetch_style using self.client_id.

.. _moobius.core.sdk.Moobius.send_fetch_canvas:
Moobius.send_fetch_canvas
-----------------------------------
**Moobius.send_fetch_canvas(self, channel_id)**

Calls self.ws_client.fetch_canvas using self.client_id.

.. _moobius.core.sdk.Moobius.send_fetch_channel_info:
Moobius.send_fetch_channel_info
-----------------------------------
**Moobius.send_fetch_channel_info(self, channel_id)**

Calls self.ws_client.fetch_channel_info using self.client_id.

.. _moobius.core.sdk.Moobius.send_join_channel:
Moobius.send_join_channel
-----------------------------------
**Moobius.send_join_channel(self, channel_id)**

Calls self.ws_client.join_channel using self.client_id.

.. _moobius.core.sdk.Moobius.send_leave_channel:
Moobius.send_leave_channel
-----------------------------------
**Moobius.send_leave_channel(self, channel_id)**

Calls self.ws_client.leave_channel using self.client_id. The Agent version of self.unbind_service_from_channel.

.. _moobius.core.sdk.Moobius.listen_loop:
Moobius.listen_loop
-----------------------------------
**Moobius.listen_loop(self)**

Listens to the wand (in an infinite loop so) that the wand could send spells to the service at any time (not only before the service is started).
Uses asyncio.Queue.

.. _moobius.core.sdk.Moobius.handle_received_payload:
Moobius.handle_received_payload
-----------------------------------
**Moobius.handle_received_payload(self, payload)**

Decode the received (websocket) payload, a JSON string, and call the handler based on p['type']. Returns None.
Example methods called:
  on_message_up(), on_action(), on_button_click(), on_copy_client(), on_unknown_payload()

Example use-case:
  >>> self.ws_client = WSClient(ws_server_uri, on_connect=self.send_service_login, handle=self.handle_received_payload)

.. _moobius.core.sdk.Moobius.on_action:
Moobius.on_action
-----------------------------------
**Moobius.on_action(self, action)**

Handles an action (Action object) from a user. Returns None.
Calls the corresponding method to handle different subtypes of action.
Example methods called:
  on_fetch_service_characters(), on_fetch_buttons(), on_fetch_canvas(), on_join_channel(), on_leave_channel(), on_fetch_channel_info()
Service function.

.. _moobius.core.sdk.Moobius.on_update:
Moobius.on_update
-----------------------------------
**Moobius.on_update(self, update)**

Dispatches an Update instance to one of various callbacks. Agent function.
It is recommended to overload the invididual callbacks instead of this function.

.. _moobius.core.sdk.Moobius.on_spell:
Moobius.on_spell
-----------------------------------
**Moobius.on_spell(self, obj)**

Called when a spell is received, which can be any object but is often a string. Returns None.

.. _moobius.core.sdk.Moobius.on_start:
Moobius.on_start
-----------------------------------
**Moobius.on_start(self)**

Called when the service is initialized. Returns None

.. _moobius.core.sdk.Moobius.on_message_up:
Moobius.on_message_up
-----------------------------------
**Moobius.on_message_up(self, message_up)**

Handles a payload from a user. Service function. Returns None.
Example MessageBody object:
  moobius.MessageBody(subtype=text, channel_id=<channel id>, content=MessageContent(...), timestamp=1707254706635,
                      recipients=[<user id 1>, <user id 2>], sender=<user id>, message_id=<message-id>,
                      context={'group_id': <group-id>, 'channel_type': 'ccs'})

.. _moobius.core.sdk.Moobius.on_message_down:
Moobius.on_message_down
-----------------------------------
**Moobius.on_message_down(self, message_down)**

Callback when a message is recieved (a MessageBody object similar to what on_message_up gets).
Agent function. Returns None.

.. _moobius.core.sdk.Moobius.on_update_characters:
Moobius.on_update_characters
-----------------------------------
**Moobius.on_update_characters(self, update)**

Handles changes to the character list. One of the multiple update callbacks. Returns None.
Agent function. Update is an Update instance.

.. _moobius.core.sdk.Moobius.on_update_channel_info:
Moobius.on_update_channel_info
-----------------------------------
**Moobius.on_update_channel_info(self, update)**

Handles changes to the channel info. One of the multiple update callbacks. Returns None.
Agent function. Update is an Update instance.

.. _moobius.core.sdk.Moobius.on_update_canvas:
Moobius.on_update_canvas
-----------------------------------
**Moobius.on_update_canvas(self, update)**

Handles changes to the canvas. One of the multiple update callbacks. Returns None.
Agent function. Update is an Update instance.

.. _moobius.core.sdk.Moobius.on_update_buttons:
Moobius.on_update_buttons
-----------------------------------
**Moobius.on_update_buttons(self, update)**

Handles changes to the buttons. One of the multiple update callbacks. Returns None.
Agent function. Update is an Update instance.

.. _moobius.core.sdk.Moobius.on_update_style:
Moobius.on_update_style
-----------------------------------
**Moobius.on_update_style(self, update)**

Handles changes to the style (look and feel). One of the multiple update callbacks. Returns None.
Agent function. Update is an Update instance.

.. _moobius.core.sdk.Moobius.on_update_context_menu:
Moobius.on_update_context_menu
-----------------------------------
**Moobius.on_update_context_menu(self, update)**

Handles changes to the context menu. One of the multiple update callbacks. Returns None.
Agent function. Update is an Update instance.

.. _moobius.core.sdk.Moobius.on_fetch_service_characters:
Moobius.on_fetch_service_characters
-----------------------------------
**Moobius.on_fetch_service_characters(self, action)**

Handles the received action of fetching a character_list. One of the multiple Action object callbacks. Returns None.
Example Action object: moobius.Action(subtype="fetch_characters", channel_id=<channel id>, sender=<user id>, context={}).

.. _moobius.core.sdk.Moobius.on_fetch_buttons:
Moobius.on_fetch_buttons
-----------------------------------
**Moobius.on_fetch_buttons(self, action)**

Handles the received action of fetching buttons. One of the multiple Action object callbacks. Returns None.
Example Action object: moobius.Action(subtype="fetch_buttons", channel_id=<channel id>, sender=<user id>, context={})

.. _moobius.core.sdk.Moobius.on_fetch_canvas:
Moobius.on_fetch_canvas
-----------------------------------
**Moobius.on_fetch_canvas(self, action)**

Handles the received action (Action object) of fetching canvas. One of the multiple Action object callbacks. Returns None.

.. _moobius.core.sdk.Moobius.on_fetch_context_menu:
Moobius.on_fetch_context_menu
-----------------------------------
**Moobius.on_fetch_context_menu(self, action)**

Handles the received action (Action object) of fetching the right-click context menu. One of the multiple Action object callbacks. Returns None.

.. _moobius.core.sdk.Moobius.on_fetch_channel_info:
Moobius.on_fetch_channel_info
-----------------------------------
**Moobius.on_fetch_channel_info(self, action)**

Handle the received action of fetching channel info. One of the multiple Action object callbacks. Returns None.
Example Action object: moobius.Action(subtype="fetch_channel_info", channel_id=<channel id>, sender=<user id>, context={}).

.. _moobius.core.sdk.Moobius.on_join_channel:
Moobius.on_join_channel
-----------------------------------
**Moobius.on_join_channel(self, action)**

Handles the received action of joining a channel. One of the multiple Action object callbacks. Returns None.
Example Action object: moobius.Action(subtype="join_channel", channel_id=<channel id>, sender=<user id>, context={}).

.. _moobius.core.sdk.Moobius.on_leave_channel:
Moobius.on_leave_channel
-----------------------------------
**Moobius.on_leave_channel(self, action)**

Handles the received action of leaving a channel. One of the multiple Action object callbacks. Returns None.
Example Action object: moobius.Action(subtype="leave_channel", channel_id=<channel id>, sender=<user id>, context={}).

.. _moobius.core.sdk.Moobius.on_button_click:
Moobius.on_button_click
-----------------------------------
**Moobius.on_button_click(self, button_click)**

Handles a button call from a user. Returns None.
Example ButtonClick object: moobius.ButtonClick(button_id="the_big_red_button", channel_id=<channel id>, sender=<user id>, arguments=[], context={})

.. _moobius.core.sdk.Moobius.on_context_menu_click:
Moobius.on_context_menu_click
-----------------------------------
**Moobius.on_context_menu_click(self, context_click)**

Handles a context menu right click from a user. Returns None. Example MenuClick object:
MenuClick(item_id=1, message_id=<id>, message_subtype=text, message_content={'text': 'Click on this message.'}, channel_id=<channel_id>, context={}, recipients=[])

.. _moobius.core.sdk.Moobius.on_copy_client:
Moobius.on_copy_client
-----------------------------------
**Moobius.on_copy_client(self, copy)**

Handles a "Copy" of a message. Returns None.
Example Copy object: moobius.Copy(request_id=<id>, origin_type=message_down, status=True, context={'message': 'Message received'})

.. _moobius.core.sdk.Moobius.on_unknown_payload:
Moobius.on_unknown_payload
-----------------------------------
**Moobius.on_unknown_payload(self, payload)**

Catch-all for handling unknown Payload objects. Returns None.

.. _moobius.core.sdk.Moobius.__str__:
Moobius.__str__
-----------------------------------
**Moobius.__str__(self)**

<No doc string>

.. _moobius.core.sdk.Moobius.__repr__:
Moobius.__repr__
-----------------------------------
**Moobius.__repr__(self)**

<No doc string>

.. _moobius.core.sdk.Moobius.handle_received_payload._group2ids:
Moobius.handle_received_payload._group2ids
-----------------------------------
**Moobius.handle_received_payload._group2ids(g_id)**

<No doc string>

.. _moobius.core.sdk.Moobius.start._get_agent_info:
Moobius.start._get_agent_info
-----------------------------------
**Moobius.start._get_agent_info()**

<No doc string>

.. _moobius.core.sdk.Moobius.handle_received_payload._make_elem:
Moobius.handle_received_payload._make_elem
-----------------------------------
**Moobius.handle_received_payload._make_elem(d)**

<No doc string>