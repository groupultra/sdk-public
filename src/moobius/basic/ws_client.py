# ws_client.py

import asyncio
import traceback
import websockets

import time
import aioprocessing


class WSClient:
    def __init__(self, ws_server_uri, on_connect=None, handle=None, horcrux=None):
        self.websocket = None
        self.ws_server_uri = ws_server_uri
        self.on_connect = on_connect or self._on_connect
        self.handle = handle or self._default_handle
        self.horcrux = horcrux

    async def connect(self):
        self.websocket = await websockets.connect(self.ws_server_uri)
        await self.on_connect()
        # Start listening for messages in the background
        asyncio.create_task(self.receive())

    async def _on_connect(self):
        print("WSClient.on_connect <Default> Connected to", self.ws_server_uri)

    # todo: max retries
    async def send(self, message):
        try:
            await self.websocket.send(message)  # Don't use asyncio.create_task() here, or the message could not be sent in order
        except websockets.exceptions.ConnectionClosed:
            print("WSClient.send() Connection closed. Attempting to reconnect...")
            await self.connect()
            print("Reconnected! Attempting to send message again...")
            await self.websocket.send(message)
        except Exception as e:
            traceback.print_exc()
            print("WSClient.send() Error occurred:", e)
            await self.connect()
            print("Reconnected! Attempting to send message again...")
            await self.websocket.send(message)

    async def receive(self):
        while True:
            try:
                message = await self.websocket.recv()
                asyncio.create_task(self.safe_handle(message))
            except websockets.exceptions.ConnectionClosed:
                print("WSClient.receive()Connection closed. Attempting to reconnect...")
                await self.connect()
                print("Reconnected!")
                break
            except Exception as e:
                traceback.print_exc()
                print("WSClient.receive() Error occurred:", e)
                await self.connect()
                print("Reconnected!")
                break
    
    async def pipe_receive(self):
        while True:
            try:
                if self.horcrux:
                    message = await self.horcrux.coro_recv()
                    print("WSClient.pipe_receive received:", type(message), message)
                    if str(message[:4]) == "RECV":
                        await self.safe_handle(message[4:])
                    else:
                        await self.websocket.send(message)
                    
            except websockets.exceptions.ConnectionClosed:
                print("Connection closed. Attempting to reconnect...")
                await self.connect()
                print("Reconnected!")
                break
            except Exception as e:
                traceback.print_exc()
                print("WSClient.receive() Error occurred:", e)
                await self.connect()
                print("Reconnected!")
                break
    
    async def pipe_receive(self):
        while True:
            try:
                if self.horcrux:
                    message = await self.horcrux.coro_recv()
                    print("WSClient.pipe_receive received:", type(message), message)
                    if str(message[:4]) == "RECV":
                        await self.safe_handle(message[4:])
                    else:
                        await self.websocket.send(message)
                    
            except websockets.exceptions.ConnectionClosed:
                print("Connection closed. Attempting to reconnect...")
                await self.connect()
                print("Reconnected!")
                break
            except Exception as e:
                traceback.print_exc()
                print("Error occurred:", e)
                await self.connect()
                print("Reconnected!")
                break

    async def safe_handle(self, message):
        try:
            print("safe_handle message", message)
            await self.handle(message)
        except Exception as e:
            traceback.print_exc()
            print("WSClient.safe_handle() Error occurred:", e)
            await self.connect()
            print("Reconnected!")

    async def _default_handle(self, message):
        print("WSClient._handle <Default> Received:", message)