# ws_client.py

import asyncio
import traceback
import websockets

import time
import aioprocessing


class WSClient:
    def __init__(self, ws_server_uri, handle=None):
        self.websocket = None
        self.ws_server_uri = ws_server_uri
        self.handle = handle or self._default_handle

    async def connect(self):
        self.websocket = await websockets.connect(self.ws_server_uri)
        
        # Start listening for messages in the background
        asyncio.create_task(self.receive())


    async def send(self, message):
        asyncio.create_task(self.websocket.send(message))
        
    async def receive(self):
        while True:
            try:
                message = await self.websocket.recv()
                asyncio.create_task(self.safe_handle(message))
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
    
    async def pipe_receive(self):
        while True:
            try:
                print("pipe pipe pipe receive receive receive")
                if self.child_pipe:
                    message = await self.child_pipe.coro_recv()
                    print("My My My Child Msg: ", message)
                else:
                    print("No child pipe")
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
            await self.handle(message)
        except Exception as e:
            traceback.print_exc()
            print("Error occurred:", e)
            await self.connect()
            print("Reconnected!")

    async def _default_handle(self, message):
        print("WSClient._handle <Default> Received:", message)