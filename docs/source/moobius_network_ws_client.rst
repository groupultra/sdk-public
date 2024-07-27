.. _moobius_network_ws_client:

moobius.network.ws_client
====================================================================================

Module-level functions
===================================================================================

.. _moobius.network.ws_client.send_tweak:

send_tweak
---------------------------------------------------------------------------------------------------------------------
send_tweak(the_message)

A slight modification of messages.

.. _moobius.network.ws_client.time_out_wrap:

time_out_wrap
---------------------------------------------------------------------------------------------------------------------
time_out_wrap(co_routine, timeout)

Sometimes the connection can hang forever.
Returns a co-routine that is the same as the given co_routine except that
await will raise an asyncio.TimeoutError if it takes too long.

===================================================================================

Class WSClient
===========================================================================================

WSClient is a websocket client that has a wide variety of Moobius-specific functions for sending payloads specific to the Moobius platform.
It contains the standard socket functions such as on_connect(), send(), and receive() and is more robust:
it has a queuing system and will automatically reconnect.

.. _moobius.network.ws_client.WSClient.__init__:

WSClient.__init__
---------------------------------------------------------------------------------------------------------------------
WSClient.__init__(self, ws_server_uri, on_connect, handle)

Initializes a WSClient object.

Parameters:
  ws_server_uri: str
    The URI of the websocket server.
  on_connect: function
    The function to be called when the websocket is connected.
  handle: function
    The function to be called when a message is received.

Example:
  >>> ws_client = WSClient("ws://localhost:8765", on_connect=on_connect, handle=handle)
  >>> await self.authenticate()
  >>> await self.ws_client.connect()

.. _moobius.network.ws_client.WSClient.connect:

WSClient.connect
---------------------------------------------------------------------------------------------------------------------
WSClient.connect(self)

Connects to the websocket server. Call after self.authenticate(). Returns None.
Keeps trying if it fails!

.. _moobius.network.ws_client.WSClient._queue_consume:

WSClient._queue_consume
---------------------------------------------------------------------------------------------------------------------
WSClient._queue_consume(self)

Consumes tasks from an internal asyncio queue.

.. _moobius.network.ws_client.WSClient.send:

WSClient.send
---------------------------------------------------------------------------------------------------------------------
WSClient.send(self, message)

Sends a dict-valued message (or JSON string) to the websocket server.
  Adds the message to self.outbound_queue.
Note: Call this and other socket functions after self.authenticate()
Returns None, but if the server responds to the message it will be detected in the self.recieve() loop.

.. _moobius.network.ws_client.WSClient.receive:

WSClient.receive
---------------------------------------------------------------------------------------------------------------------
WSClient.receive(self)

Waits in a loop for messages from the websocket server or from the wand queue. Never returns.
Reconnectes if the connection fails or self.websocket.recv() stops getting anything (no heartbeats nor messages).

.. _moobius.network.ws_client.WSClient.safe_handle:

WSClient.safe_handle
---------------------------------------------------------------------------------------------------------------------
WSClient.safe_handle(self, message)

Handles a string-valued message from the websocket server. Returns None.
The handle() function is defined by the user.

.. _moobius.network.ws_client.WSClient.heartbeat:

WSClient.heartbeat
---------------------------------------------------------------------------------------------------------------------
WSClient.heartbeat(self)

Sends a heartbeat unless dry_run is True. Returns the message dict.

.. _moobius.network.ws_client.WSClient.dumps:

WSClient.dumps
---------------------------------------------------------------------------------------------------------------------
WSClient.dumps(data)

A slightly better json.dumps. Takes in data and returns a JSON string.

.. _moobius.network.ws_client.WSClient.service_login:

WSClient.service_login
---------------------------------------------------------------------------------------------------------------------
WSClient.service_login(self, service_id, access_token)

Logs in. Much like the HTTP api, this needs to be sent before any other messages.

Parameters:
  service_id (str): The client_id of a Moobius service object, which is the ID of the running service.
    Used in almost every function.
  access_token (str):
    TODO: This is the access token from http_api_wrapper; for clean code decouple access_token here!
  dry_run=False: Don't acually send anything (must functions offer a dry-run option)

Returns:
  The message as a dict.

.. _moobius.network.ws_client.WSClient.agent_login:

WSClient.agent_login
---------------------------------------------------------------------------------------------------------------------
WSClient.agent_login(self, access_token)

Logs-in agents.
Every 2h AWS will force-disconnect, so it is a good idea to send agent_login on connect.

Parameters:
  access_token: Used in the user_login message that is sent.
    This is the access token from http_api_wrapper.
  dry_run=False: Don't acually send anything if True.

Returns: The message as a dict.

.. _moobius.network.ws_client.WSClient.leave_channel:

WSClient.leave_channel
---------------------------------------------------------------------------------------------------------------------
WSClient.leave_channel(self, user_id, channel_id)

Leaves the channel with channel_id, unless dry_run is True. Used by agents. Returns the message dict.

.. _moobius.network.ws_client.WSClient.join_channel:

WSClient.join_channel
---------------------------------------------------------------------------------------------------------------------
WSClient.join_channel(self, user_id, channel_id)

Joins the channel with channel_id, unless dry_run is True. Used by agents. Returns the message dict.

.. _moobius.network.ws_client.WSClient.update_character_list:

WSClient.update_character_list
---------------------------------------------------------------------------------------------------------------------
WSClient.update_character_list(self, service_id, channel_id, characters, recipients)

Updates the characters that the recipients see.

Parameters:
  service_id (str): As always.
  channel_id (str): The channel id.
  characters (str): The group id to represent the characters who are updated.
  recipients (str): The group id to send to.
  dry_run=False: if True don't acually send the message (messages are sent in thier JSON-strin format).

Returns:
  The message as a dict.

.. _moobius.network.ws_client.WSClient.update_buttons:

WSClient.update_buttons
---------------------------------------------------------------------------------------------------------------------
WSClient.update_buttons(self, service_id, channel_id, buttons, recipients)

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

.. _moobius.network.ws_client.WSClient.update_context_menu:

WSClient.update_context_menu
---------------------------------------------------------------------------------------------------------------------
WSClient.update_context_menu(self, service_id, channel_id, menu_items, recipients)

Updates the right-click menu that the recipients can open on various messages.

Parameters:
  service_id (str): As always.
  channel_id (str): The channel id.
  menu_items (list): List of ContextMenuElement dataclasses.

Returns:
  The message as a dict.

.. _moobius.network.ws_client.WSClient.update_style:

WSClient.update_style
---------------------------------------------------------------------------------------------------------------------
WSClient.update_style(self, service_id, channel_id, style_content, recipients)

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

.. _moobius.network.ws_client.WSClient.update_channel_info:

WSClient.update_channel_info
---------------------------------------------------------------------------------------------------------------------
WSClient.update_channel_info(self, service_id, channel_id, channel_info)

Updates the channel name, description, etc for a given channel.

Parameters:
  service_id (str): As always.
  channel_id (str): The channel id.
  channel_info (ChannelInfo or dict): The data of the update.
  dry_run=False: Don't acually send anything if True.

Returns: The message as a dict.

Example:
  >>> ws_client.update_channel_info("service_id", "channel_id", {"name": "new_channel_name"})

.. _moobius.network.ws_client.WSClient.update_canvas:

WSClient.update_canvas
---------------------------------------------------------------------------------------------------------------------
WSClient.update_canvas(self, service_id, channel_id, canvas_elements, recipients)

Updates the canvas that the recipients see.

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

.. _moobius.network.ws_client.WSClient.update:

WSClient.update
---------------------------------------------------------------------------------------------------------------------
WSClient.update(self, service_id, target_client_id, data)

A generic update function that is rarely used.

Parameters:
  service_id (str): As always.
  target_client_id (str): The target client id (TODO: not currently used)
  data (dict): The content of the update.
  dry_run=False: Don't acually send anything if True.

Returns: The message as a dict.

.. _moobius.network.ws_client.WSClient.message_up:

WSClient.message_up
---------------------------------------------------------------------------------------------------------------------
WSClient.message_up(self, user_id, service_id, channel_id, recipients, subtype, content)

Used by agents to send messages.

Parameters:
  user_id (str): An agent id generally.
  channel_id (str): Which channel to broadcast the message in.
  recipients (str): The group id to send to.
  subtype (str): The subtype of message to send (text, etc). Goes into message['body'] JSON.
  content (MessageContent or dict): What is inside the message['body']['content'] JSON.
  dry_run=False: Don't acually send anything if True.

Returns: The message as a dict.

.. _moobius.network.ws_client.WSClient.message_down:

WSClient.message_down
---------------------------------------------------------------------------------------------------------------------
WSClient.message_down(self, user_id, service_id, channel_id, recipients, subtype, content, sender)

Sends a message to the recipients.

Parameters:
  user_id (str): An agent id generally.
  channel_id (str): Which channel to broadcast the message in.
  recipients (str): The group id to send to.
  subtype (str): The subtype of message to send (text, etc). Goes into message['body'] JSON.
  content (MessageContent or dict): What is inside the message['body']['content'] JSON.
  sender (str): The sender ID of the message, which determines who the chat shows the message as sent by.
  dry_run=False: Don't acually send anything if True.

Returns:
  The message as a dict.

.. _moobius.network.ws_client.WSClient.fetch_characters:

WSClient.fetch_characters
---------------------------------------------------------------------------------------------------------------------
WSClient.fetch_characters(self, user_id, channel_id)

Asks for the list of characters. The socket will send back a message with the information later.

Parameters (these are common to most fetch messages):
  user_id (str): Used in the "action" message that is sent.
  channel_id (str): Used in the body of said message.
  dry_run=False: Don't acually send anything if True.

Returns:
  The message that was sent as a dict.

.. _moobius.network.ws_client.WSClient.fetch_buttons:

WSClient.fetch_buttons
---------------------------------------------------------------------------------------------------------------------
WSClient.fetch_buttons(self, user_id, channel_id)

Same usage as fetch_characters but for the buttons.
These functions return the sent message, the actual response will come later.

.. _moobius.network.ws_client.WSClient.fetch_style:

WSClient.fetch_style
---------------------------------------------------------------------------------------------------------------------
WSClient.fetch_style(self, user_id, channel_id)

Same usage as fetch_characters but for the style.
These functions return the sent message, the actual response will come later.

.. _moobius.network.ws_client.WSClient.fetch_canvas:

WSClient.fetch_canvas
---------------------------------------------------------------------------------------------------------------------
WSClient.fetch_canvas(self, user_id, channel_id)

Same usage as fetch_characters but for the canvas.
These functions return the sent message, the actual response will come later.

.. _moobius.network.ws_client.WSClient.fetch_channel_info:

WSClient.fetch_channel_info
---------------------------------------------------------------------------------------------------------------------
WSClient.fetch_channel_info(self, user_id, channel_id)

Same usage as fetch_characters but for the channel_info.
These functions return the sent message, the actual response will come later.

.. _moobius.network.ws_client.WSClient.__str__:

WSClient.__str__
---------------------------------------------------------------------------------------------------------------------
WSClient.__str__(self)

<No doc string>

.. _moobius.network.ws_client.WSClient.__repr__:

WSClient.__repr__
---------------------------------------------------------------------------------------------------------------------
WSClient.__repr__(self)

<No doc string>

.. _moobius.network.ws_client.WSClient.__init__._default_on_connect:

WSClient.__init__._default_on_connect
---------------------------------------------------------------------------------------------------------------------
WSClient.__init__._default_on_connect(self)

<No doc string>

.. _moobius.network.ws_client.WSClient.__init__._default_handle:

WSClient.__init__._default_handle
---------------------------------------------------------------------------------------------------------------------
WSClient.__init__._default_handle(self, message)

<No doc string>

Class attributes
--------------------


