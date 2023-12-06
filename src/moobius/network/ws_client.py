# ws_client.py

import asyncio
import websockets

from loguru import logger


class WSClient:
    def __init__(self, ws_server_uri, on_connect=None, handle=None):
        self.websocket = None
        self.ws_server_uri = ws_server_uri
        self.on_connect = on_connect or self._on_connect
        self.handle = handle or self._default_handle
                
    async def connect(self):
        self.websocket = await websockets.connect(self.ws_server_uri)
        await self.on_connect()

    async def _on_connect(self):
        logger.info(f"Connected to {self.ws_server_uri}")

    async def send(self, message):
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
        try:
            await self.handle(message)
        except Exception as e:
            logger.error(e)
            await self.connect()
            logger.info("Reconnected!")

    async def _default_handle(self, message):
        logger.debug(f"{message}")