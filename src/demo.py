import json
import asyncio
from demo_service import DemoService
from moobius.moobius_wand import MoobiusWand
import aioprocessing
import time
def main():    
    # For newly bound channels. It doesn't hurt to bind multiple times.
    bind_to_channels = ["3457120e-8f05-4786-a3d4-0b53d70e6bba"]
    with open("config.json", "r") as f:
        config = json.load(f)
    
    with open("db_settings.json", "r") as f:
        db_settings = json.load(f)

    service = DemoService(db_settings=db_settings, **config)
    wand = MoobiusWand(service)
    wand.start_background_service(bind_to_channels=bind_to_channels)
    return wand
    
if __name__ == "__main__":
    wand = main()
    
    async def test_async_send():
        for i in range(5):
            await asyncio.sleep(1)
            msg_down_body = {
                "channel_id": "3457120e-8f05-4786-a3d4-0b53d70e6bba",
                "recipients": ["321e7409-e19a-4608-a623-2bae497568d0", "b42d0cb1-b97a-4c63-bbab-1d456cc26490"],
                "subtype": "text",
                "content": {
                    "text": "Hello! I'm Async Async Async Ayaka! " + str(i)
                },
                "sender": "321e7409-e19a-4608-a623-2bae497568d0",
                "timestamp": int(time.time() * 1000)
            }
            await wand.async_send("msg_down", msg_down_body)
    
    asyncio.run(test_async_send())
    
    for i in range(5):
        time.sleep(1)
        msg_down_body = {
            "channel_id": "3457120e-8f05-4786-a3d4-0b53d70e6bba",
            "recipients": ["321e7409-e19a-4608-a623-2bae497568d0", "b42d0cb1-b97a-4c63-bbab-1d456cc26490"],
            "subtype": "text",
            "content": {
                "text": "Hello! I'm Ayaka! " + str(i)
            },
            "sender": "321e7409-e19a-4608-a623-2bae497568d0",
            "timestamp": int(time.time() * 1000)
        }
        wand.send("msg_down", msg_down_body)
        
    