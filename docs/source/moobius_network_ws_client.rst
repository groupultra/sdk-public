.. _moobius_network_ws_client:

###################################################################################
moobius.network.ws_client
###################################################################################

******************************
Module-level functions
******************************

.. _moobius.network.ws_client.send_tweak:

send_tweak
---------------------------------------------------------------------------------------------------------------------
send_tweak(the_message)


A slight modification of messages..
  Parameters:
    the_message: The message.
  Returns:
    The  slightly modified message.
  Raises:
    (this function does not raise any errors of its own)


.. _moobius.network.ws_client.time_out_wrap:

time_out_wrap
---------------------------------------------------------------------------------------------------------------------
time_out_wrap(co_routine, timeout)


Sometimes the connection can hang forever. Adds a timeout that will make await raise an asyncio.TimeoutError if the function takes too long..
  Parameters:
    co_routine: The co-routine.
    
    timeout: The  timeout.
  Returns:
    The co-routine with a timeout.
  Raises:
    (this function does not raise any errors of its own)


************************************
Class WSClient
************************************

WSClient is a websocket client that has a wide variety of Moobius-specific functions for sending payloads specific to the Moobius platform.
It contains the standard socket functions such as on_connect(), send(), and receive() and is more robust:
it has a queuing system and will automatically reconnect.

.. _moobius.network.ws_client.WSClient.__init__:

WSClient.__init__
---------------------------------------------------------------------------------------------------------------------
WSClient.__init__(self, ws_server_uri, on_connect, handle)


Initializes a WSClient object.
  Parameters:
    ws_server_uri: The str
        The URI of the websocket server.
    
    on_connect: The function
        The function to be called when the websocket is connected.
    
    handle: The function
        The function to be called when a message is received.
    
    Example: 
    
    >>> ws_client = WSClient("ws: The //localhost:8765", on_connect=on_connect, handle=handle)
      >>> await self.authenticate()
      >>> await self.ws_client.connect().
  Returns:
    (Class constructors have no explicit return value)
  Raises:
    (this function does not raise any errors of its own)


.. _moobius.network.ws_client.WSClient.connect:

WSClient.connect
---------------------------------------------------------------------------------------------------------------------
WSClient.connect(self)


Connects to the websocket server. Call after self.authenticate(). 
Keeps trying if it fails!.
  Parameters:
    (No parameters in this class constructor)
  Returns:
    The None.
  Raises:
    (this function does not raise any errors of its own)


.. _moobius.network.ws_client.WSClient._queue_consume:

WSClient._queue_consume
---------------------------------------------------------------------------------------------------------------------
WSClient._queue_consume(self)


Consumes tasks from an internal asyncio queue.
  Parameters:
    (No parameters in this class constructor)
  Returns:
    The Never.
  Raises:
    (this function does not raise any errors of its own)


.. _moobius.network.ws_client.WSClient.send:

WSClient.send
---------------------------------------------------------------------------------------------------------------------
WSClient.send(self, message)


Adds the message to self.outbound_queue for sending to the server.
Note: Call this and other socket functions after self.authenticate()
 If the server responds to the message it will be detected in the self.recieve() loop.
  Parameters:
    message: The dict-valued message (or JSON string).
  Returns:
    The None.
  Raises:
    (this function does not raise any errors of its own)


.. _moobius.network.ws_client.WSClient.receive:

WSClient.receive
---------------------------------------------------------------------------------------------------------------------
WSClient.receive(self)


Waits in a loop for messages from the websocket server or from the wand queue. Never.
  Parameters:
    (No parameters in this class constructor)
  Returns:
    The 
    Reconnectes if the connection fails or self.websocket.recv() stops getting anything (no heartbeats nor messages).
  Raises:
    (this function does not raise any errors of its own)


.. _moobius.network.ws_client.WSClient.safe_handle:

WSClient.safe_handle
---------------------------------------------------------------------------------------------------------------------
WSClient.safe_handle(self, message)


Handles it with self.handle, which is specified on construction, catching errors.
  Parameters:
    message: The string-valued message from the websocket server.
  Returns:
    The None.
  Raises:
    (this function does not raise any errors of its own)


.. _moobius.network.ws_client.WSClient.heartbeat:

WSClient.heartbeat
---------------------------------------------------------------------------------------------------------------------
WSClient.heartbeat(self)


Sends a heartbeat unless dry_run is True.
  Parameters:
    (No parameters in this class constructor)
  Returns:
    The message dict.
  Raises:
    (this function does not raise any errors of its own)


.. _moobius.network.ws_client.WSClient.dumps:

WSClient.dumps
---------------------------------------------------------------------------------------------------------------------
WSClient.dumps(data)


A slightly better json.dumps..
  Parameters:
    data: The datastructure or dataclass and.
  Returns:
    The  JSON string.
  Raises:
    (this function does not raise any errors of its own)


.. _moobius.network.ws_client.WSClient.service_login:

WSClient.service_login
---------------------------------------------------------------------------------------------------------------------
WSClient.service_login(self, service_id, access_token)


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
    (this function does not raise any errors of its own)


.. _moobius.network.ws_client.WSClient.agent_login:

WSClient.agent_login
---------------------------------------------------------------------------------------------------------------------
WSClient.agent_login(self, access_token)


Logs-in agents.
Every 2h AWS will force-disconnect, so it is a good idea to send agent_login on connect.
  Parameters:
    access_token: The Used in the user_login message that is sent.
        This is the access token from http_api_wrapper.
    
    dry_run=False: The Don't acually send anything if True.
  Returns:
    The message as a dict.
  Raises:
    (this function does not raise any errors of its own)


.. _moobius.network.ws_client.WSClient.leave_channel:

WSClient.leave_channel
---------------------------------------------------------------------------------------------------------------------
WSClient.leave_channel(self, user_id, channel_id)


Leaves the channel with channel_id, unless dry_run is True. Used by agents..
  Parameters:
    user_id: The user_id, the channel_id,.
    
    channel_id: Whether to dry_run.
  Returns:
    The message sent.
  Raises:
    (this function does not raise any errors of its own)


.. _moobius.network.ws_client.WSClient.join_channel:

WSClient.join_channel
---------------------------------------------------------------------------------------------------------------------
WSClient.join_channel(self, user_id, channel_id)


Joins the channel with channel_id, unless dry_run is True. Used by agents..
  Parameters:
    user_id: The user_id, the channel_id,.
    
    channel_id: Whether to dry_run.
  Returns:
    The message sent.
  Raises:
    (this function does not raise any errors of its own)


.. _moobius.network.ws_client.WSClient.update_character_list:

WSClient.update_character_list
---------------------------------------------------------------------------------------------------------------------
WSClient.update_character_list(self, characters, service_id, channel_id, recipients)


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
    (this function does not raise any errors of its own)


.. _moobius.network.ws_client.WSClient.update_buttons:

WSClient.update_buttons
---------------------------------------------------------------------------------------------------------------------
WSClient.update_buttons(self, buttons, service_id, channel_id, recipients)


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
    (this function does not raise any errors of its own)


.. _moobius.network.ws_client.WSClient.update_context_menu:

WSClient.update_context_menu
---------------------------------------------------------------------------------------------------------------------
WSClient.update_context_menu(self, menu_items, service_id, channel_id, recipients)


Updates the right-click menu that the recipients can open on various messages.
  Parameters:
    menu_items (list): The List of ContextMenuElement dataclasses.
    
    service_id (str): The s always.
    
    channel_id (str): The channel id.
  Returns:
    The message as a dict.
  Raises:
    (this function does not raise any errors of its own)


.. _moobius.network.ws_client.WSClient.update_style:

WSClient.update_style
---------------------------------------------------------------------------------------------------------------------
WSClient.update_style(self, style_content, service_id, channel_id, recipients)


Updates the style (whehter the canvas is expanded, other look-and-feel aspects) that the recipients see.
  Parameters:
    style_content (list of dicts or StyleElement objects): The style content to be updated. Dicts are converted into 1-elemnt lists.
    
    service_id (str): The s always.
    
    channel_id (str): The channel id.
    
    recipients (str): The group id to send to.
    
    dry_run=False: The Don't acually send anything if True.
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
        >>> ws_client.update_style("service_id", "channel_id", style_content, ["user1", "user2"]).
  Raises:
    (this function does not raise any errors of its own)


.. _moobius.network.ws_client.WSClient.update_channel_info:

WSClient.update_channel_info
---------------------------------------------------------------------------------------------------------------------
WSClient.update_channel_info(self, channel_info, service_id, channel_id)


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
    (this function does not raise any errors of its own)


.. _moobius.network.ws_client.WSClient.update_canvas:

WSClient.update_canvas
---------------------------------------------------------------------------------------------------------------------
WSClient.update_canvas(self, service_id, channel_id, canvas_elements, recipients)


Updates the canvas that the recipients see.
  Parameters:
    service_id (str): The s always.
    
    channel_id (str): The channel id.
    
    canvas_elements (dict or CanvasElement; or a list therof): The elements to push to the canvas.
    
    recipients(list): The recipients character_ids who see the update.
    
    dry_run=False: The Don't acually send anything if True.
  Returns:
    The message as a dict.
    
    Example:
      >>> canvas1 = CanvasElement(path="image/url", text="the_text")
      >>> canvas2 = CanvasElement(text="the_text2")
      >>> ws_client.update_canvas("service_id", "channel_id", [canvas1, canvas2], ["user1", "user2"]).
  Raises:
    (this function does not raise any errors of its own)


.. _moobius.network.ws_client.WSClient.update:

WSClient.update
---------------------------------------------------------------------------------------------------------------------
WSClient.update(self, data, target_client_id, service_id)


A generic update function that is rarely used.
  Parameters:
    service_id (str): The s always.
    
    target_client_id (str): The target client id (TODO: not currently used).
    
    data (dict): The content of the update.
    
    dry_run=False: The Don't acually send anything if True.
  Returns:
    The message as a dict.
  Raises:
    (this function does not raise any errors of its own)


.. _moobius.network.ws_client.WSClient.message_up:

WSClient.message_up
---------------------------------------------------------------------------------------------------------------------
WSClient.message_up(self, user_id, service_id, channel_id, recipients, subtype, content)


Used by agents to send messages.
  Parameters:
    user_id (str): The  agent id generally.
    
    channel_id (str): The Which channel to broadcast the message in.
    
    recipients (str): The group id to send to.
    
    subtype (str): The subtype of message to send (text, etc). Goes into message['body'] JSON.
    
    content (MessageContent or dict): The What is inside the message['body']['content'] JSON.
    
    dry_run=False: The Don't acually send anything if True.
  Returns:
    The message as a dict.
  Raises:
    (this function does not raise any errors of its own)


.. _moobius.network.ws_client.WSClient.message_down:

WSClient.message_down
---------------------------------------------------------------------------------------------------------------------
WSClient.message_down(self, user_id, service_id, channel_id, recipients, subtype, content, sender)


Sends a message to the recipients.
  Parameters:
    user_id (str): The  agent id generally.
    
    channel_id (str): The Which channel to broadcast the message in.
    
    recipients (str): The group id to send to.
    
    subtype (str): The subtype of message to send (text, etc). Goes into message['body'] JSON.
    
    content (MessageContent or dict): The What is inside the message['body']['content'] JSON.
    
    sender (str): The sender ID of the message, which determines who the chat shows the message as sent by.
    
    dry_run=False: The Don't acually send anything if True.
  Returns:
    The message as a dict.
  Raises:
    (this function does not raise any errors of its own)


.. _moobius.network.ws_client.WSClient.fetch_characters:

WSClient.fetch_characters
---------------------------------------------------------------------------------------------------------------------
WSClient.fetch_characters(self, user_id, channel_id)


Asks for the list of characters. The socket will send back a message with the information later.
  Parameters:
    user_id (str): The Used in the "action" message that is sent.
    
    channel_id (str): The Used in the body of said message.
    
    dry_run=False: The Don't acually send anything if True.
        These three parameters are common to most fetch messages.
  Returns:
    The message that was sent as a dict.
  Raises:
    (this function does not raise any errors of its own)


.. _moobius.network.ws_client.WSClient.fetch_buttons:

WSClient.fetch_buttons
---------------------------------------------------------------------------------------------------------------------
WSClient.fetch_buttons(self, user_id, channel_id)


Same usage as fetch_characters but for the buttons..
  Parameters:
    user_id: The user_id, the channel_id,.
    
    channel_id: Whether to dry_run.
  Returns:
    The message sent.
  Raises:
    (this function does not raise any errors of its own)


.. _moobius.network.ws_client.WSClient.fetch_style:

WSClient.fetch_style
---------------------------------------------------------------------------------------------------------------------
WSClient.fetch_style(self, user_id, channel_id)


Same usage as fetch_characters but for the style..
  Parameters:
    user_id: The user_id, the channel_id,.
    
    channel_id: Whether to dry_run.
  Returns:
    The message sent.
  Raises:
    (this function does not raise any errors of its own)


.. _moobius.network.ws_client.WSClient.fetch_canvas:

WSClient.fetch_canvas
---------------------------------------------------------------------------------------------------------------------
WSClient.fetch_canvas(self, user_id, channel_id)


Same usage as fetch_characters but for the canvas..
  Parameters:
    user_id: The user_id, the channel_id,.
    
    channel_id: Whether to dry_run.
  Returns:
    The message sent.
  Raises:
    (this function does not raise any errors of its own)


.. _moobius.network.ws_client.WSClient.fetch_channel_info:

WSClient.fetch_channel_info
---------------------------------------------------------------------------------------------------------------------
WSClient.fetch_channel_info(self, user_id, channel_id)


Same usage as fetch_characters but for the channel_info..
  Parameters:
    user_id: The user_id, the channel_id,.
    
    channel_id: Whether to dry_run.
  Returns:
    The message sent.
  Raises:
    (this function does not raise any errors of its own)


.. _moobius.network.ws_client.WSClient.__str__:

WSClient.__str__
---------------------------------------------------------------------------------------------------------------------
WSClient.__str__(self)


The string output function for debugging.
  Parameters:
    (No parameters in this class constructor)
  Returns:
    The  easy-to-read string summary.
  Raises:
    (this function does not raise any errors of its own)


.. _moobius.network.ws_client.WSClient.__repr__:

WSClient.__repr__
---------------------------------------------------------------------------------------------------------------------
WSClient.__repr__(self)


The string output function for debugging.
  Parameters:
    (No parameters in this class constructor)
  Returns:
    The  easy-to-read string summary.
  Raises:
    (this function does not raise any errors of its own)


Class attributes
--------------------


