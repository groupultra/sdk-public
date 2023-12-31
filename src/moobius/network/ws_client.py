# ws_client.py

import asyncio
import websockets

from loguru import logger


class WSClient:
    '''
    WSClient is a websocket client that automatically reconnects when the connection is closed.
    It contains default socket functions, such as on_connect(), send(), receive().
    We can also define our own on_connect() and handle() functions and pass them to the constructor.
    Users should call all websocket APIs through this class.
    '''
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
            >>> await self._do_authenticate()
            >>> await self._ws_client.connect()
        '''
        self.websocket = None
        self.ws_server_uri = ws_server_uri
        self.on_connect = on_connect or self._on_connect
        self.handle = handle or self._default_handle
                
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
            >>> await self._do_authenticate()
            >>> await self._ws_client.connect()
        '''
        
        self.websocket = await websockets.connect(self.ws_server_uri)
        await self.on_connect()

    async def _on_connect(self):
        logger.info(f"Connected to {self.ws_server_uri}")

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
            >>> await self._do_authenticate()
            >>> await self._ws_client.connect()
            >>> await self._ws_client.send("Hello World!")
        '''
        try:
            logger.opt(colors=True).info(f"<blue>{message.replace('<', '&lt;').replace('>', '&gt;')}</blue>")
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
            >>> await self._do_authenticate()
            >>> await self._ws_client.connect()
            >>> # program will be blocked here until a message is received
            >>> await self._ws_client.receive()
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

    async def _default_handle(self, message):
        logger.debug(f"{message}")