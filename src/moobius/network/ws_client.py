# Websockets. Send responses and wait for the reply.

import asyncio, uuid, json, time
import websockets, dataclasses
from loguru import logger

import moobius.utils as utils
import moobius.types as types
from moobius.types import CanvasElement, ChannelInfo
from moobius.network import asserts


def send_tweak(the_message):
    if the_message['type'] == types.MESSAGE_UP or the_message['type'] == types.MESSAGE_DOWN:
        b = the_message['body']
        if 'context' in b:
            b['context'] = {}
    if the_message['type'] == types.MESSAGE_DOWN:
        if 'service_id' not in the_message:
            raise Exception('Message_down must have service_id.')
    return the_message


async def time_out_wrap(co_routine, timeout=16):
    """Sometimes the connection can hang forever.
    """
    return await asyncio.wait_for(co_routine, timeout=timeout)


class WSClient:
    """
    WSClient is a websocket client that automatically reconnects when the connection is closed.
    It contains the standard socket functions such as on_connect(), send(), receive().
    Custom on_connect() and handle() functions are also supported.
    Finally, there is a wide variety of Moobius-specific functions that send payloads recognized by the platform.
    Users should call all websocket APIs through this class just as they should call all HTTP APIs through HTTPAPIWrapper.
    """

    ############################## Standard socket interaction ########################
    def __init__(self, ws_server_uri, on_connect=None, handle=None):
        """
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
        """
        self.websocket = None
        self.ws_server_uri = ws_server_uri
        async def _default_on_connect(self): logger.info(f"Connected to {self.ws_server_uri}")
        async def _default_handle(self, message): logger.debug(f"{message}")
        self.on_connect = on_connect or _default_on_connect # THe SDK sets on_connect to self.service or self.agent login.
        self.handle = handle or _default_handle
        self.outbound_queue = asyncio.Queue()
        self.outbound_queue_running = False
        self.timeout = 16 # Connection and socket sending timeout (seems to hang every so often).
        self.is_connected = False # Flag to indicate if the service is connected. Can only consume from the queue if connected.

    async def connect(self): # Called from sdk.start() and from other functions when trying to reconnect.
        """Connects to the websocket server. Call after self.authenticate(). Returns None.
        Keeps trying if it failed!"""
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
        """If the connection goes down a queue forms.
        This sends out queued tasks in a loop."""
        while True:
            message = await self.outbound_queue.get()
            if not self.is_connected:
                await self.connect() # This will likely fill the queue more.
            try:
                await time_out_wrap(self.websocket.send(message), self.timeout)
                logger.opt(colors=True).info(f"<fg 128,0,240>{str(message).replace('<', '&lt;').replace('>', '&gt;')}</>")
            except Exception as e:
                logger.warning(f'Failed to send data, the connection seems to be lost: {e}; {type(e)}.')
                self.is_connected = False # No longer connected!
                # Put back the data since it failed to send. TODO: Does this change the order in a harmful way?
                await self.outbound_queue.put(message)

    async def send(self, message):
        """
        Sends a dict-valued message (or JSON string) to the websocket server. Call this and other socket functions after self.authenticate()
        If the connection is closed, reconnect and send again.
        If an exception is raised, reconnect and send again.
        Returns None, but if the server responds to the message it will be detected in the self.recieve() loop.
        """
        if not self.outbound_queue_running: # This must be inside an async, and __init__ is not async.
            loop = asyncio.get_running_loop()
            self.outbound_queue_running = True
            loop.create_task(self._queue_consume())
        if type(message) is dict:
            message = self.dumps(message)
        asserts.socket_assert(json.loads(message))
        await self.outbound_queue.put(message)

    async def receive(self):
        """
        Waits in a loop for messages from the websocket server or from the wand queue. Never returns.
        If the connection is closed, reconnect and keep going.
        If an exception is raised, reconnect and keep going.
        """

        while True:
            if not self.is_connected:
                await self.connect()
            try:
                message = await time_out_wrap(self.websocket.recv(), 256) # BIG timeout so heartbeats can have time.
                logger.opt(colors=True).info(f"<yellow>{str(message).replace('<', '&lt;').replace('>', '&gt;')}</yellow>")
                asyncio.create_task(self.safe_handle(message))
            except Exception as e:
                logger.warning(f"WSClient.receive() failed; the connection seems to be no longer: {e}; {type(e)}")
                self.is_connected = False # Will connect next loop iteration.

    async def safe_handle(self, message):
        """
        Handles a string-valued message from the websocket server. Returns None.
        The handle() function is defined by the user.
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
        """A slightly better json.dumps. Takes in data and returns a JSON string."""
        return json.dumps(data, cls=utils.EnhancedJSONEncoder, ensure_ascii=False)

    ########################## Authentication and join/leave #########################

    async def service_login(self, service_id, access_token, *, dry_run=False):
        """
        Constructs and sends a message that logs the service in. Need to be sent before any other messages.
        Of course it is an service function not an agent function.

        Parameters:
          service_id (str): The client_id of a Moobius service object, which is the ID of the running service.
            Used in almost every function.
          access_token (str):
            TODO: This is the access token from http_api_wrapper; for clean code decouple access_token here!
          dry_run=False: Don't acually send anything (must functions offer a dry-run option)

        Returns:
          The message as a dict."""
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

    async def agent_login(self, access_token, *, dry_run=False):
        """
        Constructs the agent_login message. Of course it is an agent function not a service function.
        Every 2h AWS will force-disconnect, so it is a good idea to send agent_login on connect.

        Parameters:
          access_token: Used in the user_login message that is sent.
            TODO: This is the access token from http_api_wrapper; for clean code decouple access_token here!
          dry_run=False: Don't acually send anything if True.

        Returns: The message as a dict.
        """
        message = {
            "type": "user_login",
            "request_id": str(uuid.uuid4()),
            "auth_origin": "cognito" or "oauth2",
            "access_token": access_token
        }
        if not dry_run:
            logger.info("agent_login payload, should show up as another log in a second or so")
            await self.send(message)
        return message

    async def leave_channel(self, user_id, channel_id, *, dry_run=False):
        """Makes the character with user_id leave the channel with channel_id, unless dry_run is True. Returns the message dict."""
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
        """Makes the character with user_id join the channel with channel_id, unless dry_run is True. Returns the message dict."""
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
    async def update_character_list(self, service_id, channel_id, characters, recipients, *, dry_run=False):
        """
        Constructs and sends the update message for user list.

        Parameters:
          service_id (str): As always.
          channel_id (str): The channel id.
          characters (str): The group id to represent the characters who are updated.
          recipients (str): The group id to send to.
          dry_run=False: if True don't acually send the message (messages are sent in thier JSON-strin format).

        Returns:
          The message as a dict.
        """
        if not recipients:
            return None
        message = {
            "type": "update",
            "request_id": str(uuid.uuid4()),
            "service_id": service_id,
            "body": {
                "subtype": "update_characters",
                "channel_id": channel_id,
                "recipients": recipients,
                "content":{"characters": characters}
            }
        }
        if not dry_run:
            await self.send(message)
        return message

    async def update_buttons(self, service_id, channel_id, buttons, recipients, *, dry_run=False):
        """
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
        """
        if not recipients:
            return None
        button_dicts = [b if type(b) is dict else dataclasses.asdict(b) for b in buttons]
        message = {
            "type": "update",
            "request_id": str(uuid.uuid4()),
            "service_id": service_id,
            "body": {
                "subtype": "update_buttons",
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

    async def update_context_menu(self, service_id, channel_id, menu_items, recipients, *, dry_run=False):
        """
        Updates the right click context menu.

        Parameters:
          service_id (str): As always.
          channel_id (str): The channel id.
          menu_items (list): List of ContextMenuElement dataclasses.

        Returns:
          The message as a dict.
        """
        if not recipients:
            return None
        message = {
            "type": "update",
            "request_id": str(uuid.uuid4()),
            "service_id": service_id,
            "body": {
                "subtype": "update_context_menu",
                "channel_id": channel_id,
                "recipients": recipients,
                "content": [dataclasses.asdict(item) for item in menu_items],
                "context": {}
            }
        }
        if not dry_run:
            await self.send(message)
        return message

    async def update_style(self, service_id, channel_id, style_content, recipients, *, dry_run=False):
        """
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
        """
        if not recipients:
            return None
        message = {
            "type": "update",
            "request_id": str(uuid.uuid4()),
            "service_id": service_id,
            "body": {
                "subtype": "update_style",
                "channel_id": channel_id,
                "recipients": recipients,
                "content": style_content,
                "group_id": "temp",
                "context": {}
            }
        }
        if not dry_run:
            await self.send(message)
        return message

    async def update_channel_info(self, service_id, channel_id, channel_info, *, dry_run=False):
        """
        Constructs and sends the update message for channel info.

        Parameters:
          service_id (str): As always.
          channel_id (str): The channel id.
          channel_info (ChannelInfo or dict): The data of the update.
          dry_run=False: Don't acually send anything if True.

        Returns: The message as a dict.

        Example:
          >>> ws_client.update_channel_info("service_id", "channel_id", {"name": "new_channel_name"})
        """
        if type(channel_info) is ChannelInfo:
            channel_info = dataclasses.asdict(channel_info)
        channel_info['context'] = {'channel_description': channel_info['channel_description'],
                                   'channel_type': channel_info['channel_type']}
        message = {
            "type": "update",
            "subtype": "channel_info",
            "channel_id": channel_id,
            "request_id": str(uuid.uuid4()),
            "service_id": service_id,
            "body": channel_info
        }
        if not dry_run:
            await self.send(message)
        return message

    async def update_canvas(self, service_id, channel_id, canvas_elements, recipients, *, dry_run=False):
        """
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
        """
        if not recipients:
            return None
        if type(canvas_elements) is dict or type (canvas_elements) is CanvasElement:
            canvas_elements = [canvas_elements] # Should be a list of items not the item itself.
        for i in range(len(canvas_elements)):
            if type(canvas_elements[i]) is CanvasElement:
                canvas_elements[i] = dataclasses.asdict(canvas_elements[i])
                for k in list(canvas_elements[i].keys()):
                    if canvas_elements[i][k] is None:
                        del canvas_elements[i][k]
        message = {
            "type": "update",
            "request_id": str(uuid.uuid4()),
            "service_id": service_id,
            "body": {
                "subtype": "update_canvas",
                "channel_id": channel_id,
                "recipients": recipients,
                "content": canvas_elements,
                "group_id": "temp",
                "context": {}
            }
        }
        if not dry_run:
            await self.send(message)
        return message

    async def update(self, service_id, target_client_id, data, *, dry_run=False):
        """
        Constructs the update message. (I think) more of a Service than Agent function.

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
        if not dry_run:
            await self.send(message)
        return message

    ########################## Sending messages ###################################
    async def message_up(self, user_id, service_id, channel_id, recipients, subtype, content, *, dry_run=False):
        """
        Constructs and sends a message_up message. The same parameters as self.message_down, except that no sender is needed.

        Parameters:
          user_id (str): An agent id generally.
          channel_id (str): Which channel to broadcast the message in.
          recipients (str): The group id to send to.
          subtype (str): The subtype of message to send (text, etc). Goes into message['body'] JSON.
          content (MessageContent or dict): What is inside the message['body']['content'] JSON.
          dry_run=False: Don't acually send anything if True.

        Returns: The message as a dict.
        """
        if not recipients:
            return None
        message = {
            "type": "message_up",
            "request_id": str(uuid.uuid4()),
            "user_id": user_id, "service_id": service_id, # TODO: is service id necessary?
            "body": {
                "subtype": subtype,
                "channel_id": channel_id,
                "content": content if type(content) is dict else dataclasses.asdict(content), # TODO: function to make vanilla dicts.
                "recipients": recipients,
                "timestamp": int(time.time() * 1000),
                "context": {}
            }
        }
        for k in list(message['body']['content'].keys()): # Makes the messages cleaner, if nothing else.
            if message['body']['content'][k] is None:
                del message['body']['content'][k]
        send_tweak(message)
        if not dry_run:
            await self.send(message)
        return message

    async def message_down(self, user_id, service_id, channel_id, recipients, subtype, content, sender, *, dry_run=False):
        """
        Constructs and sends the message_down message.
        Currently, only text message is supported, so the subtype is always "text".

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
        """
        if not recipients:
            return None
        message = await self.message_up(user_id, service_id, channel_id, recipients, subtype, content, dry_run=True)
        message['type'] = types.MESSAGE_DOWN
        message['body']['sender'] = sender
        del message['user_id'] # Only used for message_up.
        send_tweak(message)
        if not dry_run:
            await self.send(message)
        return message

    ######################### Fetching data ############################
    async def fetch_characters(self, user_id, channel_id, *, dry_run=False):
        """
        Constructs and sends the fetch_service_characters message.
        If everything works the server will send back a message with the information later.

        Parameters (these are common to most fetch messages):
          user_id (str): Used in the "action" message that is sent.
          channel_id (str): Used in the body of said message.
          dry_run=False: Don't acually send anything if True.

        Returns:
          The message as a dict.
        """
        message = {
            "type": "action",
            "request_id": str(uuid.uuid4()),
            "user_id": user_id,
            "body": {
                "subtype": "fetch_characters",
                "channel_id": channel_id,
                "context": {}
            }
        }
        logger.warning('Not sure if websocket fetch_characters will work, but there is an HTTP API version to fetch groups and each group comes with its own list of characters.')
        if not dry_run:
            logger.info("send_fetch_characters", channel_id)
            await self.send(message)
        return message

    async def fetch_buttons(self, user_id, channel_id, *, dry_run=False):
        """Same usage as fetch_characters but for the buttons. Returns the message dict."""
        message = {
            "type": "action",
            "request_id": str(uuid.uuid4()),
            "user_id": user_id,
            "body": {
                "subtype": "fetch_buttons",
                "channel_id": channel_id,
                "context": {}
            }
        }
        if not dry_run:
            await self.send(message)
        return message

    async def fetch_style(self, user_id, channel_id, *, dry_run=False):
        """Same usage as fetch_characters but for the style. Returns the message dict."""
        message = {
            "type": "action",
            "request_id": str(uuid.uuid4()),
            "user_id": user_id,
            "body": {
                "subtype": "fetch_style",
                "channel_id": channel_id,
                "context": {}
            }
        }
        if not dry_run:
            await self.send(message)
        return message

    async def fetch_canvas(self, user_id, channel_id, *, dry_run=False):
        """Same usage as fetch_characters but for the canvas. Returns the message dict."""
        message = {
            "type": "action",
            "request_id": str(uuid.uuid4()),
            "user_id": user_id,
            "body": {
                "subtype": "fetch_canvas",
                "channel_id": channel_id,
                "context": {}
            }
        }
        if not dry_run:
            await self.send(message)
        return message

    async def fetch_channel_info(self, user_id, channel_id, *, dry_run=False):
        """Same usage as fetch_characters but for the channel_info. Returns the message dict."""
        message = {
            "type": "action",
            "request_id": str(uuid.uuid4()),
            "user_id": user_id,
            "body": {
                "subtype": "fetch_channel_info",
                "channel_id": channel_id,
                "context": {}
            }
        }
        if not dry_run:
            await self.send(message)
        return message

    def __str__(self):
        return f'moobius.WSClient(ws_server_uri={self.ws_server_uri}, on_connect={self.on_connect}, handle={self.handle})'
    def __repr__(self):
        return self.__str__()
