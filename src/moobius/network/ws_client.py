# Uses websockets to interact with the platform's Websocket API.
# Websockets, unlike https, have seperate "send" and "recieve" functions.
# This module is designed to be used by the Moobius service.

import asyncio, uuid, json, time
import websockets, dataclasses
from loguru import logger

import moobius.utils as utils
import moobius.types as types
from moobius.types import *


def asserted_dataclass_asdict(x, the_class):
    """
    Asserts that the input is the correct dataclass or is a dict which matches to a dataclsss.

    Parameters:
      x: The input dict or dataclass.
      the_class: The class to match to, such as types.Button

    Returns:
      The modified value of x, as a dict.

    Raises:
      An Exception if there is a mismatch in the formatting.
    """
    if type(x) is dict:
        # TODO: enforce type: print("Fields:", types.Button.__dataclass_fields__)
        #  default=dataclasses._MISSING_TYPE means manditory
        #  name=name; type=str, typing.Optional[moobius.types.Dialog], etc.
        x1 = the_class(**x)
    elif type(x) is the_class:
        return dataclasses.asdict(x)
    else:
        raise Exception(f'Wrong format for conversion to dataclass {the_class}')
    return x


async def time_out_wrap(co_routine, timeout=16):
    """Sometimes the connection can hang forever. Adds a timeout that will make await raise an asyncio.TimeoutError if the function takes too long.
    Accepts a co-routine and a timeout. Returns the co-routine with a timeout. 
    """
    return await asyncio.wait_for(co_routine, timeout=timeout)


class WSClient:
    """
    WSClient is a websocket client that has a wide variety of Moobius-specific functions for sending payloads specific to the Moobius platform.
    It contains the standard socket functions such as on_connect(), send(), and receive() and is more robust:
    it has a queuing system and will automatically reconnect.
    """

    ############################## Standard socket interaction ########################
    def __init__(self, ws_server_uri, on_connect=None, handle=None, report_str=None):
        """
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
        """
        self.websocket = None
        self.ws_server_uri = ws_server_uri
        async def _default_on_connect(self): logger.info(f"Connected to {self.ws_server_uri}")
        async def _default_handle(self, message): logger.debug(f"{message}")
        self.on_connect = on_connect or _default_on_connect # THe SDK sets on_connect to service or user login.
        self.handle = handle or _default_handle
        self.outbound_queue = asyncio.Queue()
        self.outbound_queue_running = False
        self.timeout = 16 # Connection and socket sending timeout (seems to hang every so often).
        self.is_connected = False # Flag to indicate if the service is connected. Can only consume from the queue if connected.
        self.report_str = report_str if report_str else '' # Debug information, such is user vs service mode.

    async def connect(self): # Called from sdk.start() and from other functions when trying to reconnect.
        """Connects to the websocket server. Call after self.authenticate(). Returns None.
        Keeps trying if it fails!"""
        while True:
            try:
                logger.info('Attempting to (re)connect...')
                self.websocket = await time_out_wrap(websockets.connect(self.ws_server_uri), timeout=self.timeout)
                logger.info('Reconnected sucessfully!')
                self.is_connected = True
                break
            except Exception as e:
                logger.warning(f'{e} {type(e)}; Will keep trying in this connection loop.')
        await self.on_connect()

    async def _queue_consume(self):
        """Consumes tasks from an internal asyncio queue. Returns Never."""
        while True:
            message = await self.outbound_queue.get()
            if not self.is_connected:
                await self.connect() # This will likely fill the queue more.
            try:
                await time_out_wrap(self.websocket.send(message), self.timeout)
                logger.opt(colors=True).info(f"<fg 128,0,240>Sent to socket{self.report_str}: {str(message).replace('<', '&lt;').replace('>', '&gt;')}</>")
            except Exception as e:
                logger.warning(f'Failed to send data, the connection seems to be lost: {e}; {type(e)}.')
                self.is_connected = False # No longer connected!
                # Put back the data since it failed to send. TODO: Does this change the order in a harmful way?
                await self.outbound_queue.put(message)

    async def send(self, message):
        """
        Accepts a dict-valued message (or JSON string). Adds the message to self.outbound_queue for sending to the server.
        Note: Call this and other socket functions after self.authenticate()
        Returns None. If the server responds to the message it will be detected in the self.recieve() loop.
        """
        if not self.outbound_queue_running: # This must be inside an async, and __init__ is not async.
            loop = asyncio.get_running_loop()
            self.outbound_queue_running = True
            loop.create_task(self._queue_consume())
        if type(message) is dict:
            message = self.dumps(message) # This converts dataclasses into dicts.
        elif type(message) is not str:
            raise Exception("must send a string or dict-valued message into ws_client.send")
        await self.outbound_queue.put(message)

    async def receive(self):
        """
        Waits in a loop for messages from the websocket server or from the wand queue. Never returns.
        Reconnectes if the connection fails or self.websocket.recv() stops getting anything (no heartbeats nor messages).
        """

        while True:
            if not self.is_connected:
                await self.connect()
            try:
                message = await time_out_wrap(self.websocket.recv(), 256) # BIG timeout so heartbeats can have time.
                logger.opt(colors=True).info(f"<yellow>{self.report_str} {str(message).replace('<', '&lt;').replace('>', '&gt;')}</yellow>")
                asyncio.create_task(self.safe_handle(message))
            except Exception as e:
                logger.warning(f"WSClient.receive() failed; the connection seems to be no longer: {e}; {type(e)}")
                self.is_connected = False # Will connect next loop iteration.

    async def safe_handle(self, message):
        """
        Accepts a string-valued message from the websocket server. Returns None.
        Handles it with self.handle, which is specified on construction, catching errors.
        """
        try:
            await self.handle(message)
        except Exception as e:
            logger.error(e)

    async def heartbeat(self, *, dry_run=False):
        """Sends a heartbeat unless dry_run is True. Returns the message dict."""
        message = {
            "type": "heartbeat",
            "request_id": str(uuid.uuid4()),
            "body": {}
        }
        if not dry_run:
            await self.send(message)
        return message

    @staticmethod
    def dumps(data):
        """A slightly better json.dumps. Accepts a datastructure or dataclass and returns a JSON string."""
        return utils.enhanced_json_save(None, data, typemark_dataclasses=False, indent=None)

    ########################## Authentication and join/leave #########################

    async def service_login(self, service_id, access_token, *, dry_run=False):
        """
        Logs in. Much like the HTTP api, this needs to be sent before any other messages.

        Parameters:
          service_id (str): The client_id of a Moobius service object, which is the ID of the running service.
            Used in almost every function.
          access_token (str):
            TODO: This is the access token from http_api_wrapper; for clean code decouple access_token here!
          dry_run=False: Don't acually send anything (must functions offer a dry-run option)

        Returns:
          The message as a dict."""
        utils.assert_strs(service_id, access_token)
        message = {
            "type": "service_login",
            "request_id": str(uuid.uuid4()),
            "auth_origin": "cognito",
            "access_token": access_token,
            "service_id": service_id
        }
        if not dry_run:
            logger.info("service_login payload, should show up as another log in a second or so")
            await self.send(message)
        return message

    async def user_login(self, access_token, *, dry_run=False):
        """
        Logs-in a user.
        Every 2h AWS will force-disconnect, so it is a good idea to send this on connect.

        Parameters:
          access_token: Used in the user_login message that is sent.
            This is the access token from http_api_wrapper.
          dry_run=False: Don't acually send anything if True.

        Returns: The message as a dict.
        """
        utils.assert_strs(access_token)
        message = {
            "type": "user_login",
            "request_id": str(uuid.uuid4()),
            "auth_origin": "cognito" or "oauth2",
            "access_token": access_token
        }
        if not dry_run:
            logger.info("user_login payload, should show up as another log in a second or so")
            await self.send(message)
        return message

    async def leave_channel(self, user_id, channel_id, *, dry_run=False):
        """A user leaves the channel with channel_id, unless dry_run is True. Accepts the user_id, the channel_id, and whether to dry_run. Returns the message sent."""
        utils.assert_strs(user_id, channel_id)
        message = {
            "type": "action",
            "request_id": str(uuid.uuid4()),
            "user_id": user_id,
            "body": {
                "subtype": "leave_channel",
                "channel_id": channel_id,
                "context": {}
            }
        }
        if not dry_run:
            await self.send(message)
        return message

    async def join_channel(self, user_id, channel_id, *, dry_run=False):
        """A user joins the channel with channel_id, unless dry_run is True. Accepts the user_id, the channel_id, and whether to dry_run. Returns the message sent."""
        utils.assert_strs(user_id, channel_id)
        message = {
            "type": "action",
            "request_id": str(uuid.uuid4()),
            "user_id": user_id,
            "body": {
                "subtype": "join_channel",
                "channel_id": channel_id,
                "context": {}
            }
        }
        if not dry_run:
            await self.send(message)
        return message

    #################################### Updating ########################################
    async def update_character_list(self, characters, service_id, channel_id, recipients, *, dry_run=False):
        """
        Updates the characters that the recipients see.

        Parameters:
          characters (str): The group id to represent the characters who are updated.
          service_id (str): As always.
          channel_id (str): The channel id.
          recipients (str): The group id to send to.
          dry_run=False: if True don't acually send the message (messages are sent in thier JSON-strin format).

        Returns:
          The message as a dict.
        """
        if not recipients:
            return None
        utils.assert_strs(characters, service_id, channel_id, recipients)
        message = {
            "type": "update",
            "request_id": str(uuid.uuid4()),
            "service_id": service_id,
            "body": {
                "subtype": types.UPDATE_CHARACTERS,
                "channel_id": channel_id,
                "recipients": recipients,
                "content":{"characters": characters}
            }
        }
        if not dry_run:
            await self.send(message)
        return message

    async def update_buttons(self, buttons, service_id, channel_id, recipients, *, dry_run=False):
        """
        Updates the buttons that the recipients see.

        Parameters:
          buttons (list of Buttons): The buttons list to be updated.
          service_id (str): As always.
          channel_id (str): The channel id.
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
        """
        if not recipients:
            return None
        if type(buttons) not in [list, tuple]:
            buttons = [buttons]
        utils.assert_strs(service_id, channel_id, recipients)
        buttons = [asserted_dataclass_asdict(b, Button) for b in buttons]
        button_dicts = [b if type(b) is dict else dataclasses.asdict(b) for b in buttons]
        for b in button_dicts: # Not sure if this helps?
            if 'bottom_buttons' in b and not b['bottom_buttons']:
                del b['bottom_buttons']
        message = {
            "type": "update",
            "request_id": str(uuid.uuid4()),
            "service_id": service_id,
            "body": {
                "subtype": types.UPDATE_BUTTONS,
                "channel_id": channel_id,
                "recipients": recipients,
                "content": button_dicts,
                "group_id": "temp",
                "context": {}
            }
        }
        if not dry_run:
            await self.send(message)
        return message

    async def update_menu(self, menu_items, service_id, channel_id, recipients, *, dry_run=False):
        """
        Updates the right-click menu that the recipients can open on various messages.

        Parameters:
          menu_items (list): List of MenuItem dataclasses.
          service_id (str): As always.
          channel_id (str): The channel id.

        Returns:
          The message as a dict.
        """
        if not recipients:
            return None
        utils.assert_strs(service_id, channel_id, recipients)
        menu_items = [asserted_dataclass_asdict(item, MenuItem) for item in menu_items]
        message = {
            "type": "update",
            "request_id": str(uuid.uuid4()),
            "service_id": service_id,
            "body": {
                "subtype": types.UPDATE_MENU,
                "channel_id": channel_id,
                "recipients": recipients,
                "content": menu_items,
                "context": {}
            }
        }
        if not dry_run:
            await self.send(message)
        return message

    async def update_style(self, style_items, service_id, channel_id, recipients, *, dry_run=False):
        """
        Updates the style (whether the canvas is expanded, other look-and-feel aspects) that the recipients see.

        Parameters:
          style_items (list of dicts or StyleItem objects): The style content to be updated. Dicts are converted into 1-elemnt lists.
          service_id (str): As always.
          channel_id (str): The channel id.
          recipients (str): The group id to send to.
          dry_run=False: Don't acually send anything if True.

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
            >>> ws_client.update_style("service_id", "channel_id", style_items, ["user1", "user2"])
        """
        if not recipients:
            return None
        if type(style_items) not in [list, tuple]:
            style_items = [style_items]
        utils.assert_strs(service_id, channel_id, recipients)
        style_items = [asserted_dataclass_asdict(item, StyleItem) for item in style_items]
        message = {
            "type": "update",
            "request_id": str(uuid.uuid4()),
            "service_id": service_id,
            "body": {
                "subtype": types.UPDATE_STYLE,
                "channel_id": channel_id,
                "recipients": recipients,
                "content": style_items,
                "group_id": "temp",
                "context": {}
            }
        }
        if not dry_run:
            await self.send(message)
        return message

    async def update_channel_info(self, channel_info, service_id, channel_id, *, dry_run=False):
        """
        Updates the channel name, description, etc for a given channel.

        Parameters:
          channel_info (ChannelInfo or dict): The data of the update.
          service_id (str): As always.
          channel_id (str): The channel id.
          dry_run=False: Don't acually send anything if True.

        Returns: The message as a dict.

        Example:
          >>> ws_client.update_channel_info("service_id", "channel_id", {"name": "new_channel_name"})
        """
        channel_info = asserted_dataclass_asdict(channel_info, ChannelInfo)
        utils.assert_strs(service_id, channel_id)
        channel_info['context'] = {'channel_description': channel_info['channel_description'],
                                   'channel_type': channel_info['channel_type']}
        message = {
            "type": "update",
            "subtype": types.UPDATE_CHANNEL_INFO,
            "channel_id": channel_id,
            "request_id": str(uuid.uuid4()),
            "service_id": service_id,
            "body": channel_info
        }
        if not dry_run:
            await self.send(message)
        return message

    async def update_canvas(self, service_id, channel_id, canvas_items, recipients, *, dry_run=False):
        """
        Updates the canvas that the recipients see.

        Parameters:
          service_id (str): As always.
          channel_id (str): The channel id.
          canvas_items (dict or CanvasItem; or a list therof): The elements to push to the canvas.
          recipients(list): The recipients character_ids who see the update.
          dry_run=False: Don't acually send anything if True.

        Returns:
          The message as a dict.

        Example:
          >>> canvas1 = CanvasItem(path="image/url", text="the_text")
          >>> canvas2 = CanvasItem(text="the_text2")
          >>> ws_client.update_canvas("service_id", "channel_id", [canvas1, canvas2], ["user1", "user2"])
        """
        if not recipients:
            return None
        if type(canvas_items) is dict or type (canvas_items) is CanvasItem:
            canvas_items = [canvas_items] # Should be a list of items not the item itself.
        utils.assert_strs(service_id, channel_id, recipients)
        canvas_items = [asserted_dataclass_asdict(item, CanvasItem) for item in canvas_items]

        for i in range(len(canvas_items)):
            if type(canvas_items[i]) is CanvasItem:
                canvas_items[i] = dataclasses.asdict(canvas_items[i])
                for k in list(canvas_items[i].keys()):
                    if canvas_items[i][k] is None:
                        del canvas_items[i][k]
        message = {
            "type": "update",
            "request_id": str(uuid.uuid4()),
            "service_id": service_id,
            "body": {
                "subtype": types.UPDATE_CANVAS,
                "channel_id": channel_id,
                "recipients": recipients,
                "content": canvas_items,
                "group_id": "temp",
                "context": {}
            }
        }
        if not dry_run:
            await self.send(message)
        return message

    async def update(self, data, target_client_id, service_id, *, dry_run=False):
        """
        A generic update function that is rarely used.

        Parameters:
          service_id (str): As always.
          target_client_id (str): The target client id (TODO: not currently used)
          data (dict): The content of the update.
          dry_run=False: Don't acually send anything if True.

        Returns: The message as a dict.
        """
        message = {
            "type": "update",
            "request_id": str(uuid.uuid4()),
            "service_id": service_id,
            "body": data
        }
        utils.assert_strs(service_id, target_client_id)

        if not dry_run:
            await self.send(message)
        return message

    ########################## Sending messages ###################################
    async def message_up(self, user_id, service_id, channel_id, recipients, subtype, content, *, dry_run=False):
        """
        Used by users to send messages.

        Parameters:
          user_id (str): An enduser id generally.
          channel_id (str): Which channel to broadcast the message in.
          recipients (str): The group id to send to.
          subtype (str): The subtype of message to send (text, etc). Goes into message['body'] JSON.
          content (MessageContent or dict): What is inside the message['body']['content'] JSON.
          dry_run=False: Don't acually send anything if True.

        Returns: The message as a dict.
        """
        if not recipients:
            return None
        utils.assert_strs(user_id, service_id, channel_id, recipients, subtype)
        content = asserted_dataclass_asdict(content, MessageContent)
        message = {
            "type": "message_up",
            "request_id": str(uuid.uuid4()),
            "user_id": user_id, "service_id": service_id, # TODO: is service id necessary?
            "body": {
                "subtype": subtype,
                "channel_id": channel_id,
                "content": content,
                "recipients": recipients,
                "timestamp": int(time.time() * 1000),
                "context": {}
            }
        }
        for k in list(message['body']['content'].keys()): # Makes the messages cleaner, if nothing else.
            if message['body']['content'][k] is None:
                del message['body']['content'][k]
        if not dry_run:
            await self.send(message)
        return message

    async def message_down(self, user_id, service_id, channel_id, recipients, subtype, content, sender, *, dry_run=False):
        """
        Sends a message to the recipients.

        Parameters:
          user_id (str): An service id generally.
          channel_id (str): Which channel to broadcast the message in.
          recipients (str): The group id to send to.
          subtype (str): The subtype of message to send (text, etc). Goes into message['body'] JSON.
          content (MessageContent or dict): What is inside the message['body']['content'] JSON.
          sender (str): The sender ID of the message, which determines who the chat shows the message as sent by.
          dry_run=False: Don't acually send anything if True.

        Returns:
          The message as a dict.
        """
        if not recipients:
            return None
        utils.assert_strs(user_id, service_id, channel_id, recipients, subtype)
        content = asserted_dataclass_asdict(content, MessageContent)
        message = await self.message_up(user_id, service_id, channel_id, recipients, subtype, content, dry_run=True)
        message['type'] = types.MESSAGE_DOWN
        message['body']['sender'] = sender
        del message['user_id'] # Only used for message_up.
        if not dry_run:
            await self.send(message)
        return message

    ############################# Sending UI interactions ###################################
    async def send_button_click(self, button_id, bottom_button_id, button_args, channel_id, user_id, *, dry_run=False):
        """
        Sends a button click as a user.

        Parameters:
          button_id: The button's ID.
          bottom_button_id: The bottom button, set to "confirm" if there is no bottom button.
          button_args: What arguments (if any) were selected on the button (use an empty list of there are none).
          channel_id: The id of the channel the user pressed the button in.
          user_id: The ID of the (user mode) service.
          dry_run = False: Don't actually send anything if True.

        Returns:
          The message sent as a dict.
        """
        utils.assert_strs(button_id, bottom_button_id, user_id, channel_id)
        if button_args in [None, False]:
            button_args = []
        message = {"user_id": user_id,
                   "type": "action",
                   "request_id": str(uuid.uuid4()),
                   "body": {
                       "subtype": "button_click",
                       "button_id": button_id,
                       "channel_id": channel_id,
                   "arguments": [button_args],
                   "bottom_button_id": bottom_button_id,
                   "context": {}}}
        message = types._send_tmp_convert('send_button_click', message)
        if not dry_run:
            await self.send(message)
        return message

    async def send_menu_item_click(self, menu_item_id, bottom_button_id, button_args, the_message, channel_id, user_id, *, dry_run=False):
        """
        Sends a menu item click as a user.

        Parameters:
          menu_item_id: The menu item's ID.
          bottom_button_id: The bottom button, set to "confirm" if there is no bottom button.
          button_args: What arguments (if any) were selected on the menu item's dialog (use an empty list of there are none).
          the_message: Can be a string-valued message_id, or a full message body. If a full message the subtype and content will be filled in.
          channel_id: The id of the channel the user pressed the button in.
          user_id: The ID of the (user mode) service.
          dry_run = False: Don't actually send anything if True.

        Returns:
          The message sent as a dict.
        """
        utils.assert_strs(menu_item_id, bottom_button_id, user_id, channel_id)
        if button_args in [None, False]:
            button_args = []
        if type(the_message) is types.MessageBody:
            the_message = dataclass.asdict(the_message)
        if type(the_message) is dict:
            the_id = the_message['message_id']
            the_subtype = the_message['message_subtype']
            the_content = the_message['content']
        else:
            utils.assert_strs(the_message)
            the_id = the_message
            the_content = {}
            the_subtype = '<unknown>'

        message = {
                    "user_id": user_id,
                    "type": "action",
                    "request_id": str(uuid.uuid4()),
                    "body": {
                        "subtype": types.MENU_ITEM_CLICK,
                        "menu_item_id": menu_item_id,
                        "channel_id": channel_id,
                        "message_id": the_id,
                        "message_subtype": the_subtype,
                        "message_content": the_content,
                        "arguments": [button_args],
                        "bottom_button_id": bottom_button_id,
                        "context": {}
                    }
                 }
        message = types._send_tmp_convert('send_menu_item_click', message)
        if not dry_run:
            await self.send(message)
        return message

    ######################### Refresh ############################
    async def refresh_as_user(self, user_id, channel_id, *, dry_run=False):
        """
        Refreshes everything the user can see. The socket will send back messages with the information later.

        Parameters:
          user_id (str): Used in the "action" message that is sent.
          channel_id (str): Used in the body of said message.
          dry_run=False: Don't acually send anything if True.
            These three parameters are common to most fetch messages.

        Returns:
          The message that was sent as a dict.
        """
        utils.assert_strs(user_id, channel_id)
        message = {
            "type": "action",
            "request_id": str(uuid.uuid4()),
            "user_id": user_id,
            "body": {
                "subtype": types.REFRESH,
                "channel_id": channel_id,
                "context": {}
            }
        }
        if not dry_run:
            logger.info("socket refresh", channel_id)
            await self.send(message)
        return message

    def __str__(self):
        return f'moobius.WSClient(ws_server_uri={self.ws_server_uri}, on_connect={self.on_connect}, handle={self.handle})'
    def __repr__(self):
        return self.__str__()
