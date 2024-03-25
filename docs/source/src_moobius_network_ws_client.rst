.. _src_moobius_network_ws_client:

src.moobius.network.ws_client
===================================


Module-level functions
==================

send_tweak
----------------------
**send_tweak(the_message)**

<No doc string>


==================


Class WSClient
==================

WSClient is a websocket client that automatically reconnects when the connection is closed.
It contains the standard socket functions such as on_connect(), send(), receive().
Custom on_connect() and handle() functions are also supported.
Finally, there is a wide variety of Moobius-specific functions that send payloads recognized by the platform.
Users should call all websocket APIs through this class just as they should call all HTTP APIs through HTTPAPIWrapper.

WSClient.__init__
----------------------
**WSClient.__init__(self, ws_server_uri, on_connect, handle)**

Initialize a WSClient object.

Parameters:
  ws_server_uri: str
    The URI of the websocket server.
  on_connect: function
    The function to be called when the websocket is connected.
  handle: function
    The function to be called when a message is received.

No return value.

Example:
  >>> ws_client = WSClient("ws://localhost:8765", on_connect=on_connect, handle=handle)
  >>> await self.authenticate()
  >>> await self.ws_client.connect()

WSClient.connect
----------------------
**WSClient.connect(self)**

Connects to the websocket server. Call after self.authenticate(). Returns None.

WSClient.send
----------------------
**WSClient.send(self, message)**

Sends a dict-valued message (or JSON string) to the websocket server. Call this and other socket functions after self.authenticate()
If the connection is closed, reconnect and send again.
If an exception is raised, reconnect and send again.
Returns None, but if the server responds to the message it will be detected in the self.recieve() loop.

WSClient.receive
----------------------
**WSClient.receive(self)**

Waits in a loop for messages from the websocket server or from the wand queue. Never returns.
If the connection is closed, reconnect and keep going.
If an exception is raised, reconnect and keep going.

WSClient.safe_handle
----------------------
**WSClient.safe_handle(self, message)**

Handles a string-valued message from the websocket server. Returns None.
The handle() function is defined by the user.
If an exception is raised, reconnect and handle again.

WSClient.heartbeat
----------------------
**WSClient.heartbeat(self)**

Sends a heartbeat unless dry_run is True. Returns the message dict.

WSClient.dumps
----------------------
**WSClient.dumps(data)**

A slightly better json.dumps. Takes in data and returns a JSON string.

WSClient.service_login
----------------------
**WSClient.service_login(self, service_id, access_token)**

Constructs and sends a message that logs the service in. Need to be sent before any other messages.
Of course it is an service function not an agent function.

Parameters:
  service_id (str): The client_id of a Moobius service object, which is the ID of the running service.
    Used in almost every function.
  access_token (str):
    TODO: This is the access token from http_api_wrapper; for clean code decouple access_token here!
  dry_run=False: Don't acually send anything (must functions offer a dry-run option)

Returns:
  The message as a dict.

WSClient.agent_login
----------------------
**WSClient.agent_login(self, access_token)**

Constructs the agent_login message. Of course it is an agent function not a service function.
Every 2h AWS will force-disconnect, so it is a good idea to send agent_login on connect.

Parameters:
  access_token: Used in the user_login message that is sent.
    TODO: This is the access token from http_api_wrapper; for clean code decouple access_token here!
  dry_run=False: Don't acually send anything if True.

Returns: The message as a dict.

WSClient.leave_channel
----------------------
**WSClient.leave_channel(self, user_id, channel_id)**

Makes the character with user_id leave the channel with channel_id, unless dry_run is True. Returns the message dict.

WSClient.join_channel
----------------------
**WSClient.join_channel(self, user_id, channel_id)**

Makes the character with user_id join the channel with channel_id, unless dry_run is True. Returns the message dict.

WSClient.update_character_list
----------------------
**WSClient.update_character_list(self, service_id, channel_id, character_list, recipients)**

Constructs and sends the update message for user list.

Parameters:
  service_id (str): As always.
  channel_id (str): The channel id.
  character_list (list): The list of character_id strings to be updated.
  recipients (str): The group id to send to.
  dry_run=False: if True don't acually send the message (messages are sent in thier JSON-strin format).

Returns:
  The message as a dict.

WSClient.update_buttons
----------------------
**WSClient.update_buttons(self, service_id, channel_id, buttons, recipients)**

Constructs and sends the update message for buttons list.

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
  >>>    "button_text": "Continue Playing", "new_window": False,
  >>>    "arguments": []}
  >>> ws_client.update_buttons("service_id", "channel_id", [continue_button], ["user1", "user2"])

WSClient.update_context_menu
----------------------
**WSClient.update_context_menu(self, service_id, channel_id, menu_items, recipients)**

Updates the right click context menu.

Parameters:
  service_id (str): As always.
  channel_id (str): The channel id.
  menu_items (list): List of ContextMenuElement dataclasses.

Returns:
  The message as a dict.

WSClient.update_style
----------------------
**WSClient.update_style(self, service_id, channel_id, style_content, recipients)**

Constructs and sends the update message for style update.

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
    >>>       "button_text": "done",
    >>>       "arguments": []
    >>>       },
    >>>     "text": "<h1>Start from here.</h1><p>This is a Button, which most channels have</p>"
    >>>   }]
    >>> ws_client.update_style("service_id", "channel_id", style_content, ["user1", "user2"])

WSClient.update_channel_info
----------------------
**WSClient.update_channel_info(self, service_id, channel_id, channel_info)**

Constructs and sends the update message for channel info.

Parameters:
  service_id (str): As always.
  channel_id (str): The channel id.
  channel_info (ChannelInfo or dict): The data of the update.
  dry_run=False: Don't acually send anything if True.

Returns: The message as a dict.

Example:
  >>> ws_client.update_channel_info("service_id", "channel_id", {"name": "new_channel_name"})

WSClient.update_canvas
----------------------
**WSClient.update_canvas(self, service_id, channel_id, canvas_elements, recipients)**

Constructs and sends the update message for the canvas.

Parameters:
  service_id (str): As always.
  channel_id (str): The channel id.
  canvas_elements (dict or CanvasElement; or a list therof): The elements to push to the canvas.
  recipients(list): The recipients character_ids who see the update.
  dry_run=False: Don't acually send anything if True.

Returns:
  The message as a dict.

Example:
  >>> canvas1 = CanvasElement(path="image/url", text="the_text")
  >>> canvas2 = CanvasElement(text="the_text2")
  >>> ws_client.update_canvas("service_id", "channel_id", [canvas1, canvas2], ["user1", "user2"])

WSClient.update
----------------------
**WSClient.update(self, service_id, target_client_id, data)**

Constructs the update message. (I think) more of a Service than Agent function.

Parameters:
  service_id (str): As always.
  target_client_id (str): The target client id (TODO: not currently used)
  data (dict): The content of the update.
  dry_run=False: Don't acually send anything if True.

Returns: The message as a dict.

WSClient.message_up
----------------------
**WSClient.message_up(self, user_id, service_id, channel_id, recipients, subtype, message_content)**

Constructs and sends a message_up message. The same parameters as self.message_down, except that no sender is needed.

Parameters:
  user_id (str): An agent id generally.
  channel_id (str): Which channel to broadcast the message in.
  recipients (str): The group id to send to.
  subtype (str): The subtype of message to send (text, etc). Goes into message['body'] JSON.
  message_content (MessageContent): What is inside the message['body']['content'] JSON.
  dry_run=False: Don't acually send anything if True.

Returns: The message as a dict.

WSClient.message_down
----------------------
**WSClient.message_down(self, user_id, service_id, channel_id, recipients, subtype, message_content, sender)**

Constructs and sends the message_down message.
Currently, only text message is supported, so the subtype is always "text".

Parameters:
  user_id (str): An agent id generally.
  channel_id (str): Which channel to broadcast the message in.
  recipients (str): The group id to send to.
  subtype (str): The subtype of message to send (text, etc). Goes into message['body'] JSON.
  message_content (MessageContent): What is inside the message['body']['content'] JSON.
  sender (str): The sender ID of the message, which determines who the chat shows the message as sent by.
  dry_run=False: Don't acually send anything if True.

Returns:
  The message as a dict.

WSClient.fetch_characters
----------------------
**WSClient.fetch_characters(self, user_id, channel_id)**

Constructs and sends the fetch_service_characters message.
If everything works the server will send back a message with the information later.

Parameters (these are common to most fetch messages):
  user_id (str): Used in the "action" message that is sent.
  channel_id (str): Used in the body of said message.
  dry_run=False: Don't acually send anything if True.

Returns:
  The message as a dict.

WSClient.fetch_buttons
----------------------
**WSClient.fetch_buttons(self, user_id, channel_id)**

Same usage as fetch_characters but for the buttons. Returns the message dict.

WSClient.fetch_style
----------------------
**WSClient.fetch_style(self, user_id, channel_id)**

Same usage as fetch_characters but for the style. Returns the message dict.

WSClient.fetch_canvas
----------------------
**WSClient.fetch_canvas(self, user_id, channel_id)**

Same usage as fetch_characters but for the canvas. Returns the message dict.

WSClient.fetch_channel_info
----------------------
**WSClient.fetch_channel_info(self, user_id, channel_id)**

Same usage as fetch_characters but for the channel_info. Returns the message dict.

WSClient.__str__
----------------------
**WSClient.__str__(self)**

<No doc string>

WSClient.__repr__
----------------------
**WSClient.__repr__(self)**

<No doc string>

WSClient.__init__._on_connect
----------------------
**WSClient.__init__._on_connect(self)**

<No doc string>

WSClient.__init__._default_handle
----------------------
**WSClient.__init__._default_handle(self, message)**

<No doc string>