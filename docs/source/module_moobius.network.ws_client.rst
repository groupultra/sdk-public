.. _moobius_network_ws_client:

###################################################################################
moobius.network.ws_client
###################################################################################

******************************
Module-level functions
******************************

.. _moobius.network.ws_client.asserted_dataclass_asdict:

asserted_dataclass_asdict
---------------------------------------------------------------------------------------------------------------------

Asserts that the input is the correct dataclass or is a dict which matches to a dataclsss.

* Signature

    * asserted_dataclass_asdict(x, the_class)

* Parameters

    * x: The input dict or dataclass.
    
    * the_class: The class to match to, such as types.Button.

* Returns

  * The modified value of x, as a dict.

* Raises

  * An Exception if there is a mismatch in the formatting.

.. _moobius.network.ws_client.time_out_wrap:

time_out_wrap
---------------------------------------------------------------------------------------------------------------------

Sometimes the connection can hang forever. Adds a timeout that will make await raise an asyncio.TimeoutError if the function takes too long..

* Signature

    * time_out_wrap(co_routine, timeout)

* Parameters

    * co_routine: Co-routine.
    
    * timeout=16: A timeout.

* Returns

  * The co-routine with a timeout.

* Raises

  * (this function does not raise any notable errors)

************************************
Class WSClient
************************************

WSClient is a websocket client that has a wide variety of Moobius-specific functions for sending payloads specific to the Moobius platform.
It contains the standard socket functions such as on_connect(), send(), and receive() and is more robust:
it has a queuing system and will automatically reconnect.

.. _moobius.network.ws_client.WSClient.connect:

WSClient.connect
---------------------------------------------------------------------------------------------------------------------

Connects to the websocket server. Call after self.authenticate(). 
Keeps trying if it fails!.

* Signature

    * WSClient.connect(self)

* Parameters

    * (this class constructor accepts no arguments)

* Returns

  * The None.

* Raises

  * (this function does not raise any notable errors)

.. _moobius.network.ws_client.WSClient.send:

WSClient.send
---------------------------------------------------------------------------------------------------------------------

Adds the message to self.outbound_queue for sending to the server.
Note: Call this and other socket functions after self.authenticate()
 If the server responds to the message it will be detected in the self.recieve() loop.

* Signature

    * WSClient.send(self, message)

* Parameters

    * message: Dict-valued message (or JSON string).

* Returns

  * The None.

* Raises

  * (this function does not raise any notable errors)

.. _moobius.network.ws_client.WSClient.receive:

WSClient.receive
---------------------------------------------------------------------------------------------------------------------

Waits in a loop for messages from the websocket server or from the wand queue. Never.

* Signature

    * WSClient.receive(self)

* Parameters

    * (this class constructor accepts no arguments)

* Returns

  * The 
  Reconnectes if the connection fails or self.websocket.recv() stops getting anything (no heartbeats nor messages).

* Raises

  * (this function does not raise any notable errors)

.. _moobius.network.ws_client.WSClient.safe_handle:

WSClient.safe_handle
---------------------------------------------------------------------------------------------------------------------

Handles it with self.handle, which is specified on construction, catching errors.

* Signature

    * WSClient.safe_handle(self, message)

* Parameters

    * message: String-valued message from the websocket server.

* Returns

  * The None.

* Raises

  * (this function does not raise any notable errors)

.. _moobius.network.ws_client.WSClient.heartbeat:

WSClient.heartbeat
---------------------------------------------------------------------------------------------------------------------

Sends a heartbeat..

* Signature

    * WSClient.heartbeat(self, dry_run)

* Parameters

    * dry_run: N optional dry_run to not send anything if True.

* Returns

  * The message dict.

* Raises

  * (this function does not raise any notable errors)

.. _moobius.network.ws_client.WSClient.dumps:

WSClient.dumps
---------------------------------------------------------------------------------------------------------------------

A slightly better json.dumps..

* Signature

    * WSClient.dumps(data)

* Parameters

    * data: Datastructure or dataclass and.

* Returns

  * The  JSON string.

* Raises

  * (this function does not raise any notable errors)

.. _moobius.network.ws_client.WSClient.service_login:

WSClient.service_login
---------------------------------------------------------------------------------------------------------------------

Logs in. Much like the HTTP api, this needs to be sent before any other messages.

* Signature

    * WSClient.service_login(self, service_id, access_token, dry_run)

* Parameters

    * service_id: The client_id of a Moobius service object, which is the ID of the running service.
        Used in almost every function.
    
    * access_token: TODO; This is the access token from http_api_wrapper; for clean code decouple access_token here!.
    
    * dry_run: Don't acually send anything (must functions offer a dry-run option).

* Returns

  * The message as a dict.

* Raises

  * (this function does not raise any notable errors)

.. _moobius.network.ws_client.WSClient.user_login:

WSClient.user_login
---------------------------------------------------------------------------------------------------------------------

Logs-in a user.
Every 2h AWS will force-disconnect, so it is a good idea to send this on connect.

* Signature

    * WSClient.user_login(self, access_token, dry_run)

* Parameters

    * access_token: Used in the user_login message that is sent.
        This is the access token from http_api_wrapper.
    
    * dry_run: Don't actually send anything if True.

* Returns

  * The message as a dict.

* Raises

  * (this function does not raise any notable errors)

.. _moobius.network.ws_client.WSClient.leave_channel:

WSClient.leave_channel
---------------------------------------------------------------------------------------------------------------------

A user leaves the channel with channel_id, unless dry_run is True..

* Signature

    * WSClient.leave_channel(self, user_id, channel_id, dry_run)

* Parameters

    * user_id: User_id.
    
    * channel_id: The channel_id.
    
    * dry_run: Whether to dry_run.

* Returns

  * The message sent.

* Raises

  * (this function does not raise any notable errors)

.. _moobius.network.ws_client.WSClient.join_channel:

WSClient.join_channel
---------------------------------------------------------------------------------------------------------------------

A user joins the channel with channel_id, unless dry_run is True..

* Signature

    * WSClient.join_channel(self, user_id, channel_id, dry_run)

* Parameters

    * user_id: User_id.
    
    * channel_id: The channel_id.
    
    * dry_run: Whether to dry_run.

* Returns

  * The message sent.

* Raises

  * (this function does not raise any notable errors)

.. _moobius.network.ws_client.WSClient.send_characters:

WSClient.send_characters
---------------------------------------------------------------------------------------------------------------------

Updates the characters that the recipients see.

* Signature

    * WSClient.send_characters(self, characters, service_id, channel_id, recipients, dry_run)

* Parameters

    * characters: The group id to represent the characters who are updated.
    
    * service_id: As always.
    
    * channel_id: The channel id.
    
    * recipients: The group id to send to.
    
    * dry_run: If True don't acually send the message (messages are sent in thier JSON-strin format).

* Returns

  * The message as a dict.

* Raises

  * (this function does not raise any notable errors)

.. _moobius.network.ws_client.WSClient.send_buttons:

WSClient.send_buttons
---------------------------------------------------------------------------------------------------------------------

Updates the buttons that the recipients see.

* Signature

    * WSClient.send_buttons(self, buttons, service_id, channel_id, recipients, dry_run)

* Parameters

    * buttons: The buttons list to be updated.
    
    * service_id: As always.
    
    * channel_id: The channel id.
    
    * recipients: The group id to send to.
    
    * dry_run: Don't actually send anything if True.

* Returns

  * The message as a dict.

* Raises

  * (this function does not raise any notable errors)

* Example

    >>> continue_button =
      >>>   {"button_name": "Continue Playing", "button_id": "play",
      >>>    "button_name": "Continue Playing", "new_window": False,
      >>>    "arguments": []}
      >>> ws_client.update_buttons("service_id", "channel_id", [continue_button], ["user1", "user2"])

.. _moobius.network.ws_client.WSClient.send_menu:

WSClient.send_menu
---------------------------------------------------------------------------------------------------------------------

Updates the right-click menu that the recipients can open on various messages.

* Signature

    * WSClient.send_menu(self, menu_items, service_id, channel_id, recipients, dry_run)

* Parameters

    * menu_items: List of MenuItem dataclasses.
    
    * service_id: As always.
    
    * channel_id: The channel id.
    
    * recipients: The group id to send the changes to.
    
    * dry_run: Don't actually send anything if True.

* Returns

  * The message as a dict.

* Raises

  * (this function does not raise any notable errors)

.. _moobius.network.ws_client.WSClient.send_style:

WSClient.send_style
---------------------------------------------------------------------------------------------------------------------

Updates the style (whether the canvas is expanded, other look-and-feel aspects) that the recipients see.

* Signature

    * WSClient.send_style(self, style_items, service_id, channel_id, recipients, dry_run)

* Parameters

    * style_items: The style content to be updated. Dicts are converted into 1-elemnt lists.
    
    * service_id: As always.
    
    * channel_id: The channel id.
    
    * recipients: The group id to send to.
    
    * dry_run: Don't actually send anything if True.

* Returns

  * The message as a dict.

* Raises

  * (this function does not raise any notable errors)

* Example

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
        >>> ws_client.update_style("service_id", "channel_id", style_items, ["user1", "user2"])

.. _moobius.network.ws_client.WSClient.update_channel_info:

WSClient.update_channel_info
---------------------------------------------------------------------------------------------------------------------

Updates the channel name, description, etc for a given channel.

* Signature

    * WSClient.update_channel_info(self, channel_info, service_id, channel_id, dry_run)

* Parameters

    * channel_info: The data of the update.
    
    * service_id: As always.
    
    * channel_id: The channel id.
    
    * dry_run: Don't actually send anything if True.

* Returns

  * The message as a dict.

* Raises

  * (this function does not raise any notable errors)

* Example

    >>> ws_client.update_channel_info("service_id", "channel_id", {"name": "new_channel_name"})

.. _moobius.network.ws_client.WSClient.update_canvas:

WSClient.update_canvas
---------------------------------------------------------------------------------------------------------------------

Updates the canvas that the recipients see.

* Signature

    * WSClient.update_canvas(self, service_id, channel_id, canvas_items, recipients, dry_run)

* Parameters

    * service_id: As always.
    
    * channel_id: The channel id.
    
    * canvas_items: The elements to push to the canvas.
    
    * recipients: The recipients character_ids who see the update.
    
    * dry_run: Don't actually send anything if True.

* Returns

  * The message as a dict.

* Raises

  * (this function does not raise any notable errors)

* Example

    >>> canvas1 = CanvasItem(path="image/url", text="the_text")
      >>> canvas2 = CanvasItem(text="the_text2")
      >>> ws_client.update_canvas("service_id", "channel_id", [canvas1, canvas2], ["user1", "user2"])

.. _moobius.network.ws_client.WSClient.update:

WSClient.update
---------------------------------------------------------------------------------------------------------------------

A generic update function that is rarely used.

* Signature

    * WSClient.update(self, data, target_client_id, service_id, dry_run)

* Parameters

    * data: The content of the update.
    
    * target_client_id: The target client id (TODO: not currently used).
    
    * service_id: The ID of the service.
    
    * dry_run: Don't actually send anything if True.

* Returns

  * The message as a dict.

* Raises

  * (this function does not raise any notable errors)

.. _moobius.network.ws_client.WSClient.message_up:

WSClient.message_up
---------------------------------------------------------------------------------------------------------------------

Used by users to send messages.

* Signature

    * WSClient.message_up(self, user_id, service_id, channel_id, recipients, subtype, content, context, dry_run)

* Parameters

    * user_id: An enduser id generally.
    
    * service_id: Which service to send to.
    
    * channel_id: Which channel to broadcast the message in.
    
    * recipients: The group id to send to.
    
    * subtype: The subtype of message to send (text, etc). Goes into message['body'] JSON.
    
    * content: What is inside the message['body']['content'] JSON.
    
    * context: Don't actually send anything if True.
    
    * dry_run=None: Optional metadata.

* Returns

  * The message as a dict.

* Raises

  * (this function does not raise any notable errors)

.. _moobius.network.ws_client.WSClient.message_down:

WSClient.message_down
---------------------------------------------------------------------------------------------------------------------

Sends a message to the recipients.

* Signature

    * WSClient.message_down(self, user_id, service_id, channel_id, recipients, subtype, content, sender, context, dry_run)

* Parameters

    * user_id: An service id generally.
    
    * service_id: Which service to send to.
    
    * channel_id: Which channel to broadcast the message in.
    
    * recipients: The group id to send to.
    
    * subtype: The subtype of message to send (text, etc). Goes into message['body'] JSON.
    
    * content: What is inside the message['body']['content'] JSON.
    
    * sender: The sender ID of the message, which determines who the chat shows the message as sent by.
    
    * context: Don't actually send anything if True.
    
    * dry_run=None: Optional metadata.

* Returns

  * The message as a dict.

* Raises

  * (this function does not raise any notable errors)

.. _moobius.network.ws_client.WSClient.send_button_click:

WSClient.send_button_click
---------------------------------------------------------------------------------------------------------------------

Sends a button click as a user.

* Signature

    * WSClient.send_button_click(self, button_id, bottom_button_id, button_args, channel_id, user_id, dry_run)

* Parameters

    * button_id: The button's ID.
    
    * bottom_button_id: The bottom button, set to "confirm" if there is no bottom button.
    
    * button_args: What arguments (if any) were selected on the button (use an empty list of there are none).
    
    * channel_id: The id of the channel the user pressed the button in.
    
    * user_id: The ID of the (user mode) service.
    
    * dry_run: Don't actually send anything if True.

* Returns

  * The message sent as a dict.

* Raises

  * (this function does not raise any notable errors)

.. _moobius.network.ws_client.WSClient.send_menu_item_click:

WSClient.send_menu_item_click
---------------------------------------------------------------------------------------------------------------------

Sends a menu item click as a user.

* Signature

    * WSClient.send_menu_item_click(self, menu_item_id, bottom_button_id, button_args, the_message, channel_id, user_id, dry_run)

* Parameters

    * menu_item_id: The menu item's ID.
    
    * bottom_button_id: The bottom button, set to "confirm" if there is no bottom button.
    
    * button_args: What arguments (if any) were selected on the menu item's dialog (use an empty list of there are none).
    
    * the_message: Can be a string-valued message_id, or a full message body. If a full message the subtype and content will be filled in.
    
    * channel_id: The id of the channel the user pressed the button in.
    
    * user_id: The ID of the (user mode) service.
    
    * dry_run: Don't actually send anything if True.

* Returns

  * The message sent as a dict.

* Raises

  * (this function does not raise any notable errors)

.. _moobius.network.ws_client.WSClient.refresh_as_user:

WSClient.refresh_as_user
---------------------------------------------------------------------------------------------------------------------

Refreshes everything the user can see. The socket will send back messages with the information later.

* Signature

    * WSClient.refresh_as_user(self, user_id, channel_id, dry_run)

* Parameters

    * user_id: Used in the "action" message that is sent.
    
    * channel_id: Used in the body of said message.
    
    * dry_run: Don't actually send anything if True.
        These three parameters are common to most fetch messages.

* Returns

  * The message that was sent as a dict.

* Raises

  * (this function does not raise any notable errors)

Class attributes
--------------------



**********************
Internals
**********************
.. toctree::
   :maxdepth: 2

   moobius.network.ws_client_internal_attrs <moobius.network.ws_client_internal_attrs>
