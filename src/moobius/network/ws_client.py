# ws_client.py

import asyncio
import websockets

from loguru import logger

import uuid
import json
import time

from moobius.utils import EnhancedJSONEncoder


class WSClient:
    '''
    WSClient is a websocket client that automatically reconnects when the connection is closed.
    It contains the standard socket functions such as on_connect(), send(), receive().
    Custom on_connect() and handle() functions are also supported.
    Finally, there is a wide variety of Moobius-specific functions that send payloads recognized by the platform.
    Users should call all websocket APIs through this class just as they should call all HTTP APIs through HTTPAPIWrapper.
    '''

    ############################## Standard socket features ########################
    def __init__(self, ws_server_uri, on_connect=None, handle=None):
        '''
        Initialize a WSClient object.

        Parameters:
            ws_server_uri: str
                The URI of the websocket server.
            on_connect: function
                The function to be called when the websocket is connected.
            handle: function
                The function to be called when a message is received.

        Returns:
            None

        Example:
            >>> ws_client = WSClient("ws://localhost:8765", on_connect=on_connect, handle=handle)
            >>> await self.authenticate()
            >>> await self.ws_client.connect()
        '''
        self.websocket = None
        self.ws_server_uri = ws_server_uri
        async def _on_connect(self): logger.info(f"Connected to {self.ws_server_uri}")
        async def _default_handle(self, message): logger.debug(f"{message}")
        self.on_connect = on_connect or _on_connect
        self.handle = handle or _default_handle

    async def connect(self):
        '''
        Connect to the websocket server.

        Parameters:
            None

        Returns:
            None

        Example:
            Note: This is a hidden function, you don't need to call it directly.
            >>> ws_client = WSClient("ws://localhost:8765", on_connect=on_connect, handle=handle)
            >>> await self.authenticate()
            >>> await self.ws_client.connect()
        '''

        self.websocket = await websockets.connect(self.ws_server_uri)
        await self.on_connect()

    async def send(self, message):
        '''
        Send a message to the websocket server.
        If the connection is closed, reconnect and send again.
        If an exception is raised, reconnect and send again.

        Parameters:
            message: str
                The message to be sent.

        Returns:
            None

        Example:
            Note: This is a hidden function, you don't need to call it directly.
            >>> ws_client = WSClient("ws://localhost:8765", on_connect=on_connect, handle=handle)
            >>> await self.authenticate()
            >>> await self.ws_client.connect()
            >>> await self.send("Hello World!")
        '''
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
        '''
        Receive a message from the websocket server, or from the wand queue.
        If the connection is closed, reconnect and receive again.
        If an exception is raised, reconnect and receive again.

        Parameters:
            None

        Returns:
            None

        Example:
            Note: This is a hidden function, you don't need to call it directly.
            >>> ws_client = WSClient("ws://localhost:8765", on_connect=on_connect, handle=handle)
            >>> await self.authenticate()
            >>> await self.ws_client.connect()
            >>> # program will be blocked here until a message is received
            >>> await self.ws_client.receive()
        '''

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
        '''
        Handle a message from the websocket server.
        The handle() function is defined by the user.
        If an exception is raised, reconnect and handle again.

        Parameters:
            message: str
                The message to be handled.

        Returns:
            None

        Example:
            Note: This function is called by receive(), so you don't need to call it manually.
        '''
        try:
            await self.handle(message)
        except Exception as e:
            logger.error(e)
            await self.connect()
            logger.info("Reconnected!")

    async def ping(self, *, dry_run=False):
        """
        Constructs the ping message.

        Parameters:
            dry_run=False: Don't acually send anything.

        Returns: The message as a dict.

        Example:
            Note: This is a hidden function, you don't need to call it directly. Usually you could use send_ping() instead which helps you to add the client_id.
            >>> ws_client = WSClient()
            >>> ws_client.ping()
        """
        message = {
            "type": "ping",
            "request_id": str(uuid.uuid4())
        }
        if not dry_run:
            await self.send(self.dumps(message))
        return message

    @staticmethod
    def dumps(data):
        '''A slightly better json.dumps.'''
        return json.dumps(data, cls=EnhancedJSONEncoder)

    ########################## Authentication and join/leave #########################
    async def service_login(self, service_id, access_token, *, dry_run=False):
        """
        Constructs and sends a service_login message. Need to be sent before any other messages.
        Of course it is an service function not an agent function.

        Parameters:
            service_id: str
                The service id.
            access_token: str
                TODO: This is the access token from http_api_wrapper; for clean code decouple access_token here!
            dry_run=False: Don't acually send anything.

        Returns: The message as a dict.

        Example:
            Note: This is a hidden function, you don't need to call it directly. Usually you could use send_service_login() instead which helps you to add the client_id.
            >>> ws_client = WSClient()
            >>> ws_client.service_login("service_id", "access_token")
        """
        message = {
            "type": "service_login",
            "request_id": str(uuid.uuid4()),
            "auth_origin": "cognito",
            "access_token": access_token,
            "service_id": service_id
        }
        if not dry_run:
            logger.info("service_login payload, should show up as another log in a second or so")
            await self.send(self.dumps(message))
        return message

    async def agent_login(self, access_token, *, dry_run=False):
        """
        Constructs the agent_login message. Of course it is an agent function not a service function.

        Every 2h AWS will force-disconnect, so it is a good idea to send agent_login on connect.

        Parameters:
            access_token: Used in the user_login message that is sent.
              TODO: This is the access token from http_api_wrapper; for clean code decouple access_token here!
            dry_run=False: Don't acually send anything.

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
            await self.send(self.dumps(message))
        return message

    async def leave_channel(self, client_id, channel_id, *, dry_run=False):
        """
        Makes the agent character leave the band.

        Parameters:
            client_id: Used in the "action" message that is sent.
            channel_id: Used in the body of said message.
            dry_run=False: Don't acually send anything.

        Returns: The message as a dict.
        """
        message = {
            "type": "action",
            "request_id": str(uuid.uuid4()),
            "client_id": client_id,
            "body": {
                "subtype": "leave_channel",
                "channel_id": channel_id,
                "context": {}
            }
        }
        if not dry_run:
            await self.send(self.dumps(message))
        return message

    async def join_channel(self, client_id, channel_id, *, dry_run=False):
        """
        Makes the agent character join the band.

        Parameters:
            client_id: Used in the "action" message that is sent.
            channel_id: Used in the body of said message.
            dry_run=False: Don't acually send anything.

        Returns: The message as a dict.
        """
        message = {
            "type": "action",
            "request_id": str(uuid.uuid4()),
            "client_id": client_id,
            "body": {
                "subtype": "join_channel",
                "channel_id": channel_id,
                "context": {}
            }
        }
        if not dry_run:
            await self.send(self.dumps(message))
        return message

    #################################### Updating ########################################
    async def update_userlist(self, client_id, channel_id, user_list, recipients, *, dry_run=False):
        """
        Constructs the update message for user list.

        Parameters:
            client_id: str
                The client id. This is actually the service id.
            channel_id: str
                The channel id.
            user_list: list
                The user list to be updated.
            recipients: list
                The recipients to see the update.
            dry_run=False: if True don't acually send the message (messages are sent in thier JSON-strin format).
              Used to obtain the message that would have been sent.

        Returns: The message as a dict.

        Example:
            Note: This is a hidden function, you don't need to call it directly. Usually you could use send_update_userlist() instead which helps you to add the client_id.
            >>> ws_client = WSClient()
            >>> ws_client.update_userlist("client_id", "channel_id", ["user1", "user2"], ["user1", "user2"])
        """
        message = {
            "type": "update",
            "request_id": str(uuid.uuid4()),
            "client_id": client_id,
            "body": {
                "subtype": "update_userlist",
                "channel_id": channel_id,
                "recipients": recipients,
                # "recipients": [],
                "userlist": user_list,
                # "group_id": group_id,
                "context": {}
            }
        }
        for ul in user_list: # Old legacy platform API would accept non-user-ids.
            if type(ul) is not str:
                raise Exception('User list must be a list of ids.')
        if not dry_run:
            await self.send(self.dumps(message))
        return message

    async def update_features(self, client_id, channel_id, features, recipients, *, dry_run=False):
        """
        Constructs the update message for features list.

        Parameters:
            client_id: str
                The client id. This is actually the service id.
            channel_id: str
                The channel id.
            features: list
                The features list to be updated.
            recipients: list
                The recipients to see the update.
            dry_run=False: Don't acually send anything.

        Returns: The message as a dict.

        Example:
            Note: This is a hidden function, you don't need to call it directly. Usually you could use send_update_features() instead which helps you to add the client_id.
            >>> self.continue_feature = {
            >>>         "feature_id": "play",
            >>>         "feature_name": "Continue Playing",
            >>>         "button_text": "Continue Playing",
            >>>         "new_window": False,
            >>>         "arguments": [
            >>>         ]
            >>>     }
            >>> features = [
            >>>     self.continue_feature
            >>> ]
            >>> ws_client = WSClient()
            >>> ws_client.update_features("client_id", "channel_id", features, ["user1", "user2"])
        """
        message = {
            "type": "update",
            "request_id": str(uuid.uuid4()),
            "client_id": client_id,
            "body": {
                "subtype": "update_features",
                "channel_id": channel_id,
                "recipients": recipients,
                "features": features,
                "group_id": "temp",
                "context": {}
            }
        }
        if not dry_run:
            await self.send(self.dumps(message))
        return message

    async def update_style(self, client_id, channel_id, style_content, recipients, *, dry_run=False):
        """
        Constructs the update message for style update.

        Parameters:
            client_id: str
                The client id. This is actually the service id.
            channel_id: str
                The channel id.
            style_content: list
                The style content to be updated, check the example below.
            recipients: list
                The recipients to see the update.
            dry_run=False: Don't acually send anything.

        Returns: The message as a dict.

        Example:
            Note: This is a hidden function, you don't need to call it directly. Usually you could use send_update_style() instead which helps you to add the client_id.
            >>> content = [
            >>> {
            >>>     "widget": "channel",
            >>>     "display": "invisible",
            >>> },
            >>> {
            >>>     "widget": "feature",
            >>>     "display": "highlight",
            >>>     "feature_hook": {
            >>>         "feature_id": "feature_id",
            >>>         "button_text": "done",
            >>>         "arguments": []
            >>>     },
            >>>     "text": "<h1>Start from here.</h1><p>This is a Feature, what the most channles has</p>"
            >>> }
            >>> ]
            >>> ws_client = WSClient()
            >>> ws_client.update_style("client_id", "channel_id", content, ["user1", "user2"])
        """
        message = {
            "type": "update",
            "request_id": str(uuid.uuid4()),
            "client_id": client_id,
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
            await self.send(self.dumps(message))
        return message

    async def update_channel_info(self, client_id, channel_id, channel_data, *, dry_run=False):
        """
        Constructs the update message for channel info.

        Parameters:
            client_id: str
                The client id. This is actually the service id.
            channel_id: str
                The channel id.
            channel_data: dict
                The channel data to be updated.
            dry_run=False: Don't acually send anything.

        Returns: The message as a dict.

        Example:
            Note: This is a hidden function, you don't need to call it directly. Usually you could use send_update_channel_info() instead which helps you to add the client_id.
            >>> ws_client = WSClient()
            >>> ws_client.update_channel_info("client_id", "channel_id", {"name": "new_channel_name"})
        """
        message = {
            "type": "update",
            "subtype": "channel_info",
            "channel_id": channel_id,
            "request_id": str(uuid.uuid4()),
            "client_id": client_id,
            "body": channel_data
        }
        if not dry_run:
            await self.send(self.dumps(message))
        return message

    async def update_playground(self, client_id, channel_id, content, recipients, *, dry_run=False):
        """
        Constructs the update message for features list.

        Parameters:
            client_id: str
                The client id. This is actually the service id.
            channel_id: str
                The channel id.
            content: dict
                The playground content, consists of a image path and a text.
            recipients: list
                The recipients to see the update.
            dry_run=False: Don't acually send anything.

        Returns: The message as a dict.

        Example:
            Note: This is a hidden function, you don't need to call it directly. Usually you could use send_update_playground() instead which helps you to add the client_id.
            >>> content = {
            >>>     "path": "4003740a-d480-43da-9a5d-77202de5c4a3",
            >>>     "text": ""
            >>> }
            >>> ws_client = WSClient()
            >>> ws_client.update_playground("client_id", "channel_id", content, ["user1", "user2"])
        """
        message = {
            "type": "update",
            "request_id": str(uuid.uuid4()),
            "client_id": client_id,
            "body": {
                "subtype": "update_playground",
                "channel_id": channel_id,
                "recipients": recipients,
                "content": content,
                "group_id": "temp",
                "context": {}
            }
        }
        if not dry_run:
            await self.send(self.dumps(message))
        return message

    async def update(self, client_id, target_client_id, data, *, dry_run=False):
        """
        Constructs the update message. (I think) more of a Service than Agent function.

        Parameters:
            client_id: str
                The client id. This is actually the service id.
            target_client_id: str
                The target client id (TODO: not currently used)
            data: dict
                The data to be updated, can be any data.
            dry_run=False: Don't acually send anything.

        Returns: The message as a dict.

        Example:
            Note: This is a hidden function, you don't need to call it directly. Usually you could use send_update() instead which helps you to add the client_id.
            >>> ws_client = WSClient()
            >>> ws_client.update("client_id", "target_client_id", {"data": "data"})
        """
        message = {
            "type": "update",
            "request_id": str(uuid.uuid4()),
            "client_id": client_id,
            "body": data
        }
        if not dry_run:
            await self.send(self.dumps(message))
        return message

    ########################## Sending messages ###################################
    async def msg_up(self, client_id, channel_id, recipients, subtype, message_content, *, dry_run=False):
        """
        Constructs and sends a msg_up message. The same parameters as self.msg_down, except that no sender is needed.

        Parameters:
            client_id: An agent id generally.
            channel_id: Which channel to broadcast the message in.
            recipients: Can be a dict or Payload object.
            subtype: The subtype of message to send (text, etc). Goes into message['body'] JSON.
            message_content: What is inside the message['body']['content'] JSON.
            dry_run=False: Don't acually send anything.

        Returns: The message as a dict.
        """
        message = {
            "type": "msg_up",
            "request_id": str(uuid.uuid4()),
            "client_id": client_id,
            "body": {
                "subtype": subtype,
                "channel_id": channel_id,
                "content": {
                    ("text" if subtype == "text" else "path"): message_content  # + " (from service)"
                },
                "recipients": recipients,
                # "group_id": group_id,
                "timestamp": int(time.time() * 1000),
                "context": {}
            }
        }
        if not dry_run:
            await self.send(self.dumps(message))
        return message

    async def msg_down(self, client_id, channel_id, recipients, subtype, message_content, sender, *, dry_run=False):
        """
        Constructs the msg_down message.
        Currently, only text message is supported, so the subtype is always "text".

        Parameters:
            client_id: str
                The client id. This is actually the service id.
            channel_id: str
                The channel id.
            recipients: list
                The recipients to see the message.
            subtype: str
                The subtype of the message.
            message_content: str
                The message content.
            sender: str
                The sender of the message.
            dry_run=False: Don't acually send anything.

        Returns: The message as a dict.

        Example:
            Note: This is a hidden function, you don't need to call it directly. Usually you could use send_msg_down() instead which helps you to add the client_id.
            >>> ws_client = WSClient()
            >>> ws_client.msg_down("client_id", "channel_id", ["user1", "user2"], "text", "message_content", "sender")
        """
        message = await self.msg_up(client_id, channel_id, recipients, subtype, message_content, dry_run=True)
        message['type'] = "msg_down"
        message['body']['sender'] = sender
        if not dry_run:
            await self.send(self.dumps(message))
        return message

    ######################### Fetching data ############################
    async def fetch_userlist(self, client_id, channel_id, *, dry_run=False):
        """
        Constructs the fetch_user_list message.

        Parameters:
            client_id: Used in the "action" message that is sent.
            channel_id: Used in the body of said message.
            dry_run=False: Don't acually send anything.

        Returns: The message as a dict.
        """
        message = {
            "type": "action",
            "request_id": str(uuid.uuid4()),
            "client_id": client_id,
            "body": {
                "subtype": "fetch_userlist",
                "channel_id": channel_id,
                "context": {}
            }
        }
        if not dry_run:
            logger.info("send_fetch_userlist", channel_id)
            await self.send(self.dumps(message))
        return message

    async def fetch_features(self, client_id, channel_id, *, dry_run=False):
        """
        Constructs the fetch_features message.

        Parameters:
            client_id: Used in the "action" message that is sent.
            channel_id: Used in the body of said message.
            dry_run=False: Don't acually send anything.

        Returns: The message as a dict.
        """
        message = {
            "type": "action",
            "request_id": str(uuid.uuid4()),
            "client_id": client_id,
            "body": {
                "subtype": "fetch_features",
                "channel_id": channel_id,
                "context": {}
            }
        }
        if not dry_run:
            await self.send(self.dumps(message))
        return message

    async def fetch_style(self, client_id, channel_id, *, dry_run=False):
        """
        Constructs the fetch_style message.

        Parameters:
            client_id: Used in the "action" message that is sent.
            channel_id: Used in the body of said message.
            dry_run=False: Don't acually send anything.

        Returns: The message as a dict.
        """
        message = {
            "type": "action",
            "request_id": str(uuid.uuid4()),
            "client_id": client_id,
            "body": {
                "subtype": "fetch_style",
                "channel_id": channel_id,
                "context": {}
            }
        }
        if not dry_run:
            await self.send(self.dumps(message))
        return message

    async def fetch_playground(self, client_id, channel_id, *, dry_run=False):
        """
        Constructs the fetch_playground message.

        Parameters:
            client_id: Used in the "action" message that is sent.
            channel_id: Used in the body of said message.
            dry_run=False: Don't acually send anything.

        Returns: The message as a dict.
        """
        message = {
            "type": "action",
            "request_id": str(uuid.uuid4()),
            "client_id": client_id,
            "body": {
                "subtype": "fetch_playground",
                "channel_id": channel_id,
                "context": {}
            }
        }
        if not dry_run:
            await self.send(self.dumps(message))
        return message

    async def fetch_channel_info(self, client_id, channel_id, *, dry_run=False):
        """
        Constructs the fetch_channel_info message.

        Parameters:
            client_id: Used in the "action" message that is sent.
            channel_id: Used in the body of said message.
            dry_run=False: Don't acually send anything.

        Returns: The message as a dict.
        """
        message = {
            "type": "action",
            "request_id": str(uuid.uuid4()),
            "client_id": client_id,
            "body": {
                "subtype": "fetch_channel_info",
                "channel_id": channel_id,
                "context": {}
            }
        }
        if not dry_run:
            await self.send(self.dumps(message))
        return message

    def __str__(self):
        return f'moobius.WSClient(ws_server_uri={self.ws_server_uri}, on_connect={self.on_connect}, handle={self.handle})'
    def __repr__(self):
        return self.__str__()
