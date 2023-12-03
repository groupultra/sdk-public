import json
import asyncio
from demo_service import DemoService
from moobius.moobius_wand import MoobiusWand
import aioprocessing
import time
def main():    
    # For newly bound channels. It doesn't hurt to bind multiple times.
    bind_to_channels = ["c067ba03-106e-4119-9dc3-cc2bd339a28d"]
    config_path = "config.json"
    with open(config_path, "r") as f:
        config = json.load(f)
    
    with open("db_settings.json", "r") as f:
        db_settings = json.load(f)

    service = DemoService(db_settings=db_settings, config_path=config_path, **config)
    wand = MoobiusWand(service)
    wand.start_background_service(bind_to_channels=bind_to_channels)
    return wand
    
if __name__ == "__main__":
    wand = main()
    
    async def test_async_send():
        for i in range(3):
            await asyncio.sleep(1)
            msg_down_body = {
                "channel_id": "c067ba03-106e-4119-9dc3-cc2bd339a28d",
                "recipients": ["321e7409-e19a-4608-a623-2bae497568d0", "b42d0cb1-b97a-4c63-bbab-1d456cc26490"],
                "subtype": "text",
                "content": {
                    "text": "Hello! I'm Async Async Async Ayaka! " + str(i)
                },
                "sender": "321e7409-e19a-4608-a623-2bae497568d0",
                "timestamp": int(time.time() * 1000)
            }
            await wand.async_send("msg_down", msg_down_body)
            await asyncio.sleep(5)
            await wand.async_send("msg_down", "P"* 32 * 1024)
    
    asyncio.run(test_async_send())
    
    for i in range(3):
        time.sleep(1)
        msg_down_body = {
            "channel_id": "c067ba03-106e-4119-9dc3-cc2bd339a28d",
            "recipients": ["321e7409-e19a-4608-a623-2bae497568d0", "b42d0cb1-b97a-4c63-bbab-1d456cc26490"],
            "subtype": "text",
            "content": {
                "text": "Hello! I'm Ayaka! " + str(i)
            },
            "sender": "321e7409-e19a-4608-a623-2bae497568d0",
            "timestamp": int(time.time() * 1000)
        }
        wand.send("msg_down", "I" * 32 * 1024)
        wand.send("msg_down", msg_down_body)
   
    async def test_async_on():
        for i in range(3):
            await asyncio.sleep(1)
            msg_up_body = {"subtype": "text", 
                "content": {"text": "ping"}, 
                "channel_id": "c067ba03-106e-4119-9dc3-cc2bd339a28d", 
                "timestamp": 1697944692927, 
                "recipients": ["321e7409-e19a-4608-a623-2bae497568d0", "b42d0cb1-b97a-4c63-bbab-1d456cc26490"], 
                "msg_id": "fae4c198-baca-48d3-ad07-2a7f95e2f0cc", 
                "context": {
                    "recipients": ["321e7409-e19a-4608-a623-2bae497568d0", "b42d0cb1-b97a-4c63-bbab-1d456cc26490"], "group_id": None, "sender": "b42d0cb1-b97a-4c63-bbab-1d456cc26490"}
            }
            await wand.async_on("msg_up", msg_up_body)
    
    asyncio.run(test_async_on())
    