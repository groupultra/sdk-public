# ws_client.py

import asyncio
import traceback
import websockets

import time
import aioprocessing
from moobius.basic._logging_config import logger


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
        logger.info(f"WSClient.on_connect <Default> Connected to{self.ws_server_uri}")

    # todo: max retries
    async def send(self, message):
        try:
            print(f"WSClient.send() {message}")
            await self.websocket.send(message)  # Don't use asyncio.create_task() here, or the message could not be sent in order
        except websockets.exceptions.ConnectionClosed:
            logger.info("WSClient.send() Connection closed. Attempting to reconnect...")
            await self.connect()
            logger.info("Reconnected! Attempting to send message again...")
            await self.websocket.send(message)
        except Exception as e:
            traceback.print_exc()
            logger.error(f"WSClient.send() Error occurred: {e}")
            await self.connect()
            logger.info("Reconnected! Attempting to send message again...")
            await self.websocket.send(message)

    async def receive(self):
        while True:
            try:
                message = await self.websocket.recv()
                print(f"WSClient.receive() {message}")
                asyncio.create_task(self.safe_handle(message))
            except websockets.exceptions.ConnectionClosed:
                logger.info("WSClient.receive()Connection closed. Attempting to reconnect...")
                await self.connect()
                logger.info("Reconnected!")
                break
            except Exception as e:
                traceback.print_exc()
                logger.error(f"WSClient.receive() Error occurred: {e}")
                await self.connect()
                logger.info("Reconnected!")
                break

    async def safe_handle(self, message):
        try:
            logger.info(f"safe_handle message {message}" )
            await self.handle(message)
        except Exception as e:
            traceback.print_exc()
            logger.error(f"WSClient.safe_handle() Error occurred: {e}")
            await self.connect()
            logger.info("Reconnected!")

    async def _default_handle(self, message):
        logger.info(f"WSClient._handle <Default> Received: {message}")