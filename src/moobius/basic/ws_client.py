# ws_client.py

import asyncio
import traceback
import websockets

import time
import aioprocessing
from moobius.basic.logging_config import log


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
        log(f"WSClient.on_connect <Default> Connected to{self.ws_server_uri}")

    # todo: max retries
    async def send(self, message):
        try:
            await self.websocket.send(message)  # Don't use asyncio.create_task() here, or the message could not be sent in order
        except websockets.exceptions.ConnectionClosed:
            log("WSClient.send() Connection closed. Attempting to reconnect...")
            await self.connect()
            log("Reconnected! Attempting to send message again...")
            await self.websocket.send(message)
        except Exception as e:
            traceback.print_exc()
            log(f"WSClient.send() Error occurred: {e}", error=True)
            await self.connect()
            log("Reconnected! Attempting to send message again...")
            await self.websocket.send(message)

    async def receive(self):
        while True:
            try:
                message = await self.websocket.recv()
                asyncio.create_task(self.safe_handle(message))
            except websockets.exceptions.ConnectionClosed:
                log("WSClient.receive() Connection closed. Attempting to reconnect...")
                await self.connect()
                log("Reconnected!")
                break
            except Exception as e:
                traceback.print_exc()
                log(f"WSClient.receive() Error occurred: {e}", error=True)
                await self.connect()
                log("Reconnected!")
                break

    async def safe_handle(self, message):
        try:
            log(f"safe_handle message {message}" )
            await self.handle(message)
        except Exception as e:
            traceback.print_exc()
            log(f"WSClient.safe_handle() Error occurred: {e}", error=True)
            await self.connect()
            log("Reconnected!")

    async def _default_handle(self, message):
        log(f"WSClient._handle <Default> Received: {message}")