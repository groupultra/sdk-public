# ws_client.py

import asyncio
import websockets, dataclasses

from loguru import logger

import uuid
import json
import time

import moobius.utils as utils


def send_tweak(the_message):
    if the_message['type'] == 'message_up' or the_message['type'] == 'message_down':
        b = the_message['body']
        if 'context' in b:
            b['context'] = {}
    if the_message['type'] == 'message_down':
        if 'service_id' not in the_message:
            raise Exception('Message_down must have service_id.')
    return the_message


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
        async def _on_connect(self): logger.info(f"Connected to {self.ws_server_uri}")
        async def _default_handle(self, message): logger.debug(f"{message}")
        self.on_connect = on_connect or _on_connect
        self.handle = handle or _default_handle

    async def connect(self):
        """Connects to the websocket server. Call after self.authenticate(). Returns None."""
        self.websocket = await websockets.connect(self.ws_server_uri)
        await self.on_connect()

    async def send(self, message):
        """
        Sends a string-valued message to the websocket server. Call this and other socket functions after self.authenticate()
        If the connection is closed, reconnect and send again.
        If an exception is raised, reconnect and send again.
        Returns None, but if the server responds to the message it will be detected in the self.recieve() loop.
        """
        if type(message) is dict:
            message = self.dumps(message)
        try:
            logger.opt(colors=True).info(f"<fg 128,0,240>{message.replace('<', '&lt;').replace('>', '&gt;')}</>")
            await self.websocket.send(message)  # Don't use asyncio.create_task() here, or the message could not be sent in order
        except websockets.exceptions.ConnectionClosed:
            logger.info("Connection closed. Attempting to reconnect...")
            await self.connect()
            logger.info("Reconnected! Attempting to send message again...")
            await self.websocket.send(message)
        except Exception as e:
            logger.error(e)
            await self.connect()
            logger.info("Reconnected! Attempting to send message again...")
            await self.websocket.send(message)

    async def receive(self):
        """
        Waits in a loop for messages from the websocket server or from the wand queue. Never returns.
        If the connection is closed, reconnect and keep going.
        If an exception is raised, reconnect and keep going.
        """

        while True:
            try:
                message = await self.websocket.recv()
                logger.opt(colors=True).info(f"<yellow>{message.replace('<', '&lt;').replace('>', '&gt;')}</yellow>")
                asyncio.create_task(self.safe_handle(message))
            except websockets.exceptions.ConnectionClosed:
                logger.info("WSClient.receive() Connection closed. Attempting to reconnect...")
                await self.connect()
                logger.info("Reconnected!")
            except Exception as e:
                logger.error(e)
                await self.connect()
                logger.info("Reconnected!")

    async def safe_handle(self, message):
        """
        Handles a string-valued message from the websocket server. Returns None.
        The handle() function is defined by the user.
        If an exception is raised, reconnect and handle again.
        """
        try:
            await self.handle(message)
        except Exception as e:
            logger.error(e)
            await self.connect()
            logger.info("Reconnected!")

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
        return json.dumps(data, cls=utils.EnhancedJSONEncoder)

    ########################## Authentication and join/leave #########################

    async def service_login(self, service_id, access_token, *, dry_run=False):
        """
        Constructs and sends a message that logs the service in. Need to be sent before any other messages.
        Of course it is an service function not an agent function.

        Parameters:
          service_id: str
            The service id.
          access_token: str
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
    async def update_character_list(self, service_id, channel_id, character_list, recipients, *, dry_run=False):
        """
        Constructs and sends the update message for user list.

        Parameters:
          service_id (str): The client id. This is actually the service id.
          channel_id (str): The channel id.
          character_list (list): The list of character_id strings to be updated.
          recipients (list): Who sees the update. Also a list of IDs.
          dry_run=False: if True don't acually send the message (messages are sent in thier JSON-strin format).

        Returns:
          The message as a dict.
        """
        message = {
            "type": "update",
            "request_id": str(uuid.uuid4()),
            "service_id": service_id,
            "body": {
                "subtype": "update_characters",
                "channel_id": channel_id,
                "recipients": recipients,
                "content":{"characters": character_list}
            }
        }
        if not dry_run:
            await self.send(message)
        return message

    async def update_buttons(self, service_id, channel_id, buttons, recipients, *, dry_run=False):
        """
        Constructs and sends the update message for buttons list.

        Parameters:
          service_id (str): The client id. This is actually the service id.
          channel_id (str): The channel id.
          buttons (list of Buttons): The buttons list to be updated.
          recipients (list): The recipients to see the update.
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

    async def update_rclick_buttons(self, service_id, channel_id, item_dict, recipients, *, dry_run=False):
        """Updates the right click context menu."""
        basic_content = [{'item_name':v, 'item_id':k, 'support_subtype':["text","file"]} for k, v in item_dict.items()]
        message = {
            "type": "update",
            "request_id": str(uuid.uuid4()),
            "service_id": service_id,
            "body": {
                "subtype": "update_context_menu",
                "channel_id": channel_id,
                "recipients": recipients,
                "content": basic_content,
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
          service_id (str): The client id. This is actually the service id.
          channel_id (str): The channel id.
          style_content (list of dicts): The style content to be updated.
          recipients (list): The recipients to see the update.
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

    async def update_channel_info(self, service_id, channel_id, channel_data, *, dry_run=False):
        """
        Constructs and sends the update message for channel info.

        Parameters:
          service_id (str): The client id. This is actually the service id.
          channel_id (str): The channel id.
          channel_data (dict): The data of the update.
          dry_run=False: Don't acually send anything if True.

        Returns: The message as a dict.

        Example:
          >>> ws_client.update_channel_info("service_id", "channel_id", {"name": "new_channel_name"})
        """
        message = {
            "type": "update",
            "subtype": "channel_info",
            "channel_id": channel_id,
            "request_id": str(uuid.uuid4()),
            "service_id": service_id,
            "body": channel_data
        }
        if not dry_run:
            await self.send(message)
        return message

    async def update_canvas(self, service_id, channel_id, canvas_content, recipients, *, dry_run=False):
        """
        Constructs and sends the update message for the canvas.

        Parameters:
          service_id (str): The client id. This is actually the service id.
          channel_id (str): The channel id.
          content (dict): The content of the update.
          recipients(list): The recipients character_ids who see the update.
          dry_run=False: Don't acually send anything if True.

        Returns:
          The message as a dict.

        Example:
          >>> canvas_content = {
          >>>   "path": "4003110a-d480-43da-9a2d-77202deac4a3",
          >>>   "text": ""
          >>> }
          >>> ws_client.update_canvas("service_id", "channel_id", canvas_content, ["user1", "user2"])
        """
        if type(canvas_content) is dict:
            canvas_content = [canvas_content] # Should be a list of items not the item itself.
        message = {
            "type": "update",
            "request_id": str(uuid.uuid4()),
            "service_id": service_id,
            "body": {
                "subtype": "update_canvas",
                "channel_id": channel_id,
                "recipients": recipients,
                "content": canvas_content,
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
          service_id (str): The client id. This is actually the service id.
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
    async def message_up(self, user_id, service_id, channel_id, recipients, subtype, message_content, *, dry_run=False):
        """
        Constructs and sends a message_up message. The same parameters as self.message_down, except that no sender is needed.

        Parameters:
          user_id (str): An agent id generally.
          channel_id (str): Which channel to broadcast the message in.
          recipients (str): The group id to send to.
          subtype (str): The subtype of message to send (text, etc). Goes into message['body'] JSON.
          message_content (str or dict): What is inside the message['body']['content'] JSON.
            Can use a string for the text in a text message.
          dry_run=False: Don't acually send anything if True.

        Returns: The message as a dict.
        """
        if type(message_content) is str:
            content = {("text" if subtype == "text" else "path"): message_content}  # + " (from service)"
        else:
            content = message_content

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
        send_tweak(message)
        if not dry_run:
            await self.send(message)
        return message

    async def message_down(self, user_id, service_id, channel_id, recipients, subtype, message_content, sender, *, dry_run=False):
        """
        Constructs and sends the message_down message.
        Currently, only text message is supported, so the subtype is always "text".

        Parameters:
          user_id (str): An agent id generally.
          channel_id (str): Which channel to broadcast the message in.
          recipients (str): The group id to send to.
          subtype (str): The subtype of message to send (text, etc). Goes into message['body'] JSON.
          message_content (str or dict): What is inside the message['body']['content'] JSON.
          sender (str): The sender ID of the message, which determines who the chat shows the message as sent by.
          dry_run=False: Don't acually send anything if True.

        Returns:
          The message as a dict.
        """
        message = await self.message_up(user_id, service_id, channel_id, recipients, subtype, message_content, dry_run=True)
        message['type'] = "message_down"
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
