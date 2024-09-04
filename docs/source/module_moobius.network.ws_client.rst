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

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="fsig">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **asserted_dataclass_asdict**(x, the_class)

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="fparam">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* __x:__ The input dict or dataclass.

* __the_class:__ The class to match to, such as types.Button.

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="freturn">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* The modified value of x, as a dict.

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="fraises">
          <b>Raises:</b>
    </p>
  </body>
  </embed>

* An Exception if there is a mismatch in the formatting.



.. _moobius.network.ws_client.time_out_wrap:

time_out_wrap
---------------------------------------------------------------------------------------------------------------------



Sometimes the connection can hang forever. Adds a timeout that will make await raise an asyncio.TimeoutError if the function takes too long..

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="fsig">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **time_out_wrap**(co_routine, timeout)

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="fparam">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* __co_routine:__ Co-routine.

* __timeout=16:__ A timeout.

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="freturn">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* The co-routine with a timeout.

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="fraises">
          <b>Raises:</b>
    </p>
  </body>
  </embed>

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

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="fsig">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **WSClient.connect**(self)

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="fparam">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* __(this class constructor accepts no arguments):__

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="freturn">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* None.

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="fraises">
          <b>Raises:</b>
    </p>
  </body>
  </embed>

* (this function does not raise any notable errors)



.. _moobius.network.ws_client.WSClient.send:

WSClient.send
---------------------------------------------------------------------------------------------------------------------



Adds the message to self.outbound_queue for sending to the server.
Note: Call this and other socket functions after self.authenticate()
 If the server responds to the message it will be detected in the self.recieve() loop.

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="fsig">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **WSClient.send**(self, message)

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="fparam">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* __message:__ Dict-valued message (or JSON string).

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="freturn">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* None.

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="fraises">
          <b>Raises:</b>
    </p>
  </body>
  </embed>

* (this function does not raise any notable errors)



.. _moobius.network.ws_client.WSClient.receive:

WSClient.receive
---------------------------------------------------------------------------------------------------------------------



Waits in a loop for messages from the websocket server or from the wand queue. Never.

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="fsig">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **WSClient.receive**(self)

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="fparam">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* __(this class constructor accepts no arguments):__

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="freturn">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* The 
Reconnectes if the connection fails or self.websocket.recv() stops getting anything (no heartbeats nor messages).

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="fraises">
          <b>Raises:</b>
    </p>
  </body>
  </embed>

* (this function does not raise any notable errors)



.. _moobius.network.ws_client.WSClient.safe_handle:

WSClient.safe_handle
---------------------------------------------------------------------------------------------------------------------



Handles it with self.handle, which is specified on construction, catching errors.

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="fsig">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **WSClient.safe_handle**(self, message)

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="fparam">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* __message:__ String-valued message from the websocket server.

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="freturn">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* None.

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="fraises">
          <b>Raises:</b>
    </p>
  </body>
  </embed>

* (this function does not raise any notable errors)



.. _moobius.network.ws_client.WSClient.heartbeat:

WSClient.heartbeat
---------------------------------------------------------------------------------------------------------------------



Sends a heartbeat..

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="fsig">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **WSClient.heartbeat**(self, dry_run)

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="fparam">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* __dry_run:__ N optional dry_run to not send anything if True.

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="freturn">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* The message dict.

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="fraises">
          <b>Raises:</b>
    </p>
  </body>
  </embed>

* (this function does not raise any notable errors)



.. _moobius.network.ws_client.WSClient.dumps:

WSClient.dumps
---------------------------------------------------------------------------------------------------------------------



A slightly better json.dumps..

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="fsig">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **WSClient.dumps**(data)

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="fparam">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* __data:__ Datastructure or dataclass and.

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="freturn">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* The  JSON string.

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="fraises">
          <b>Raises:</b>
    </p>
  </body>
  </embed>

* (this function does not raise any notable errors)



.. _moobius.network.ws_client.WSClient.service_login:

WSClient.service_login
---------------------------------------------------------------------------------------------------------------------



Logs in. Much like the HTTP api, this needs to be sent before any other messages.

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="fsig">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **WSClient.service_login**(self, service_id, access_token, dry_run)

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="fparam">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* __service_id:__ The client_id of a Moobius service object, which is the ID of the running service.
    Used in almost every function.

* __access_token:__ TODO; This is the access token from http_api_wrapper; for clean code decouple access_token here!.

* __dry_run:__ Don't acually send anything (must functions offer a dry-run option).

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="freturn">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* The message as a dict.

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="fraises">
          <b>Raises:</b>
    </p>
  </body>
  </embed>

* (this function does not raise any notable errors)



.. _moobius.network.ws_client.WSClient.user_login:

WSClient.user_login
---------------------------------------------------------------------------------------------------------------------



Logs-in a user.
Every 2h AWS will force-disconnect, so it is a good idea to send this on connect.

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="fsig">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **WSClient.user_login**(self, access_token, dry_run)

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="fparam">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* __access_token:__ Used in the user_login message that is sent.
    This is the access token from http_api_wrapper.

* __dry_run:__ Don't actually send anything if True.

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="freturn">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* The message as a dict.

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="fraises">
          <b>Raises:</b>
    </p>
  </body>
  </embed>

* (this function does not raise any notable errors)



.. _moobius.network.ws_client.WSClient.leave_channel:

WSClient.leave_channel
---------------------------------------------------------------------------------------------------------------------



A user leaves the channel with channel_id, unless dry_run is True..

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="fsig">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **WSClient.leave_channel**(self, user_id, channel_id, dry_run)

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="fparam">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* __user_id:__ User_id.

* __channel_id:__ The channel_id.

* __dry_run:__ Whether to dry_run.

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="freturn">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* The message sent.

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="fraises">
          <b>Raises:</b>
    </p>
  </body>
  </embed>

* (this function does not raise any notable errors)



.. _moobius.network.ws_client.WSClient.join_channel:

WSClient.join_channel
---------------------------------------------------------------------------------------------------------------------



A user joins the channel with channel_id, unless dry_run is True..

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="fsig">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **WSClient.join_channel**(self, user_id, channel_id, dry_run)

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="fparam">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* __user_id:__ User_id.

* __channel_id:__ The channel_id.

* __dry_run:__ Whether to dry_run.

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="freturn">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* The message sent.

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="fraises">
          <b>Raises:</b>
    </p>
  </body>
  </embed>

* (this function does not raise any notable errors)



.. _moobius.network.ws_client.WSClient.send_characters:

WSClient.send_characters
---------------------------------------------------------------------------------------------------------------------



Updates the characters that the recipients see.

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="fsig">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **WSClient.send_characters**(self, characters, service_id, channel_id, recipients, dry_run)

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="fparam">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* __characters:__ The group id to represent the characters who are updated.

* __service_id:__ As always.

* __channel_id:__ The channel id.

* __recipients:__ The group id to send to.

* __dry_run:__ If True don't acually send the message (messages are sent in thier JSON-strin format).

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="freturn">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* The message as a dict.

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="fraises">
          <b>Raises:</b>
    </p>
  </body>
  </embed>

* (this function does not raise any notable errors)



.. _moobius.network.ws_client.WSClient.send_buttons:

WSClient.send_buttons
---------------------------------------------------------------------------------------------------------------------



Updates the buttons that the recipients see.

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="fsig">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **WSClient.send_buttons**(self, buttons, service_id, channel_id, recipients, dry_run)

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="fparam">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* __buttons:__ The buttons list to be updated.

* __service_id:__ As always.

* __channel_id:__ The channel id.

* __recipients:__ The group id to send to.

* __dry_run:__ Don't actually send anything if True.

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="freturn">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* The message as a dict.

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="fraises">
          <b>Raises:</b>
    </p>
  </body>
  </embed>

* (this function does not raise any notable errors)


.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="fexample">
          <b>Example:</b>
    </p>
  </body>
  </embed>

    >>> continue_button =
      >>>   {"button_name": "Continue Playing", "button_id": "play",
      >>>    "button_name": "Continue Playing", "new_window": False,
      >>>    "arguments": []}
      >>> ws_client.update_buttons("service_id", "channel_id", [continue_button], ["user1", "user2"])



.. _moobius.network.ws_client.WSClient.send_menu:

WSClient.send_menu
---------------------------------------------------------------------------------------------------------------------



Updates the right-click menu that the recipients can open on various messages.

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="fsig">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **WSClient.send_menu**(self, menu_items, service_id, channel_id, recipients, dry_run)

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="fparam">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* __menu_items:__ List of MenuItem dataclasses.

* __service_id:__ As always.

* __channel_id:__ The channel id.

* __recipients:__ The group id to send the changes to.

* __dry_run:__ Don't actually send anything if True.

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="freturn">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* The message as a dict.

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="fraises">
          <b>Raises:</b>
    </p>
  </body>
  </embed>

* (this function does not raise any notable errors)



.. _moobius.network.ws_client.WSClient.send_style:

WSClient.send_style
---------------------------------------------------------------------------------------------------------------------



Updates the style (whether the canvas is expanded, other look-and-feel aspects) that the recipients see.

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="fsig">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **WSClient.send_style**(self, style_items, service_id, channel_id, recipients, dry_run)

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="fparam">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* __style_items:__ The style content to be updated. Dicts are converted into 1-elemnt lists.

* __service_id:__ As always.

* __channel_id:__ The channel id.

* __recipients:__ The group id to send to.

* __dry_run:__ Don't actually send anything if True.

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="freturn">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* The message as a dict.

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="fraises">
          <b>Raises:</b>
    </p>
  </body>
  </embed>

* (this function does not raise any notable errors)


.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="fexample">
          <b>Example:</b>
    </p>
  </body>
  </embed>

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

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="fsig">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **WSClient.update_channel_info**(self, channel_info, service_id, channel_id, dry_run)

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="fparam">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* __channel_info:__ The data of the update.

* __service_id:__ As always.

* __channel_id:__ The channel id.

* __dry_run:__ Don't actually send anything if True.

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="freturn">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* The message as a dict.

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="fraises">
          <b>Raises:</b>
    </p>
  </body>
  </embed>

* (this function does not raise any notable errors)


.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="fexample">
          <b>Example:</b>
    </p>
  </body>
  </embed>

    >>> ws_client.update_channel_info("service_id", "channel_id", {"name": "new_channel_name"})



.. _moobius.network.ws_client.WSClient.update_canvas:

WSClient.update_canvas
---------------------------------------------------------------------------------------------------------------------



Updates the canvas that the recipients see.

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="fsig">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **WSClient.update_canvas**(self, service_id, channel_id, canvas_items, recipients, dry_run)

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="fparam">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* __service_id:__ As always.

* __channel_id:__ The channel id.

* __canvas_items:__ The elements to push to the canvas.

* __recipients:__ The recipients character_ids who see the update.

* __dry_run:__ Don't actually send anything if True.

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="freturn">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* The message as a dict.

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="fraises">
          <b>Raises:</b>
    </p>
  </body>
  </embed>

* (this function does not raise any notable errors)


.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="fexample">
          <b>Example:</b>
    </p>
  </body>
  </embed>

    >>> canvas1 = CanvasItem(path="image/url", text="the_text")
      >>> canvas2 = CanvasItem(text="the_text2")
      >>> ws_client.update_canvas("service_id", "channel_id", [canvas1, canvas2], ["user1", "user2"])



.. _moobius.network.ws_client.WSClient.update:

WSClient.update
---------------------------------------------------------------------------------------------------------------------



A generic update function that is rarely used.

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="fsig">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **WSClient.update**(self, data, target_client_id, service_id, dry_run)

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="fparam">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* __data:__ The content of the update.

* __target_client_id:__ The target client id (TODO: not currently used).

* __service_id:__ The ID of the service.

* __dry_run:__ Don't actually send anything if True.

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="freturn">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* The message as a dict.

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="fraises">
          <b>Raises:</b>
    </p>
  </body>
  </embed>

* (this function does not raise any notable errors)



.. _moobius.network.ws_client.WSClient.message_up:

WSClient.message_up
---------------------------------------------------------------------------------------------------------------------



Used by users to send messages.

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="fsig">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **WSClient.message_up**(self, user_id, service_id, channel_id, recipients, subtype, content, context, dry_run)

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="fparam">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* __user_id:__ An enduser id generally.

* __service_id:__ Which service to send to.

* __channel_id:__ Which channel to broadcast the message in.

* __recipients:__ The group id to send to.

* __subtype:__ The subtype of message to send (text, etc). Goes into message['body'] JSON.

* __content:__ What is inside the message['body']['content'] JSON.

* __context:__ Optional metadata.

* __dry_run=None:__ Don't actually send anything if True.

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="freturn">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* The message as a dict.

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="fraises">
          <b>Raises:</b>
    </p>
  </body>
  </embed>

* (this function does not raise any notable errors)



.. _moobius.network.ws_client.WSClient.message_down:

WSClient.message_down
---------------------------------------------------------------------------------------------------------------------



Sends a message to the recipients.

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="fsig">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **WSClient.message_down**(self, user_id, service_id, channel_id, recipients, subtype, content, sender, context, dry_run)

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="fparam">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* __user_id:__ An service id generally.

* __service_id:__ Which service to send to.

* __channel_id:__ Which channel to broadcast the message in.

* __recipients:__ The group id to send to.

* __subtype:__ The subtype of message to send (text, etc). Goes into message['body'] JSON.

* __content:__ What is inside the message['body']['content'] JSON.

* __sender:__ The sender ID of the message, which determines who the chat shows the message as sent by.

* __context:__ Optional metadata.

* __dry_run=None:__ Don't actually send anything if True.

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="freturn">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* The message as a dict.

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="fraises">
          <b>Raises:</b>
    </p>
  </body>
  </embed>

* (this function does not raise any notable errors)



.. _moobius.network.ws_client.WSClient.send_button_click:

WSClient.send_button_click
---------------------------------------------------------------------------------------------------------------------



Sends a button click as a user.

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="fsig">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **WSClient.send_button_click**(self, button_id, bottom_button_id, button_args, channel_id, user_id, dry_run)

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="fparam">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* __button_id:__ The button's ID.

* __bottom_button_id:__ The bottom button, set to "confirm" if there is no bottom button.

* __button_args:__ What arguments (if any) were selected on the button (use an empty list of there are none).

* __channel_id:__ The id of the channel the user pressed the button in.

* __user_id:__ The ID of the (user mode) service.

* __dry_run:__ Don't actually send anything if True.

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="freturn">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* The message sent as a dict.

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="fraises">
          <b>Raises:</b>
    </p>
  </body>
  </embed>

* (this function does not raise any notable errors)



.. _moobius.network.ws_client.WSClient.send_menu_item_click:

WSClient.send_menu_item_click
---------------------------------------------------------------------------------------------------------------------



Sends a menu item click as a user.

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="fsig">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **WSClient.send_menu_item_click**(self, menu_item_id, bottom_button_id, button_args, the_message, channel_id, user_id, dry_run)

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="fparam">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* __menu_item_id:__ The menu item's ID.

* __bottom_button_id:__ The bottom button, set to "confirm" if there is no bottom button.

* __button_args:__ What arguments (if any) were selected on the menu item's dialog (use an empty list of there are none).

* __the_message:__ Can be a string-valued message_id, or a full message body. If a full message the subtype and content will be filled in.

* __channel_id:__ The id of the channel the user pressed the button in.

* __user_id:__ The ID of the (user mode) service.

* __dry_run:__ Don't actually send anything if True.

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="freturn">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* The message sent as a dict.

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="fraises">
          <b>Raises:</b>
    </p>
  </body>
  </embed>

* (this function does not raise any notable errors)



.. _moobius.network.ws_client.WSClient.refresh_as_user:

WSClient.refresh_as_user
---------------------------------------------------------------------------------------------------------------------



Refreshes everything the user can see. The socket will send back messages with the information later.

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="fsig">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **WSClient.refresh_as_user**(self, user_id, channel_id, dry_run)

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="fparam">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* __user_id:__ Used in the "action" message that is sent.

* __channel_id:__ Used in the body of said message.

* __dry_run:__ Don't actually send anything if True.
    These three parameters are common to most fetch messages.

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="freturn">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* The message that was sent as a dict.

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="fraises">
          <b>Raises:</b>
    </p>
  </body>
  </embed>

* (this function does not raise any notable errors)



Class attributes
--------------------



**********************
Internals
**********************
.. toctree::
   :maxdepth: 2

   moobius.network.ws_client_internal_attrs <moobius.network.ws_client_internal_attrs>
