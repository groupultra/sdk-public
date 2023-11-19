import json
import asyncio
from demo_service import DemoService
from moobius.moobius_wand import MoobiusWand
import aioprocessing
from moobius.basic._types import *
from moobius.basic._logging_config import logger
import time

def main():
    # For newly bound channels. It doesn't hurt to bind multiple times.
    bind_to_channels = ['efae7992-0801-4079-bae2-83189b68d71d']
    
    # with open(r"C:\\Users\\Administrator\\Desktop\\ss\\sdk\\src\\config.json", "r") as f:
    with open("/home/ubuntu/sdk/src/config.json", "r") as f:
        config = json.load(f)
    
    with open("db_settings.json", "r") as f:
        db_settings = json.load(f)

    service = DemoService(db_settings=db_settings, **config)
    service.start(bind_to_channels=bind_to_channels)
    # global process_forever
    # process_forever = aioprocessing.AioProcess(target=waitt, args=())
    # # # process_forever = aioprocessing.AioProcess(target=pipe_forever, args=())
    # process_forever.start()
    return service


if __name__ == "__main__":
    
    service = main()
    service.parent_pipe.coro_send("ping")
    wand = service.get_wand()
    wand.send_ping()
    wand.send_ping()
    wand.send_ping()
    wand.send_ping()
    wand.send_ping()
    real_characters = wand.fetch_real_characters("efae7992-0801-4079-bae2-83189b68d71d")
    logger.info(f"real_characters {real_characters}")
    wand.send_msg_down(channel_id="efae7992-0801-4079-bae2-83189b68d71d", 
                       recipients=["321e7409-e19a-4608-a623-2bae497568d0", "b42d0cb1-b97a-4c63-bbab-1d456cc26490"],
                       subtype="text",
                       message_content="Hello! I'm Ayaka!",
                       sender="321e7409-e19a-4608-a623-2bae497568d0")

    my_msg_up = {"type": "msg_up", "body": {"subtype": "text", "content": {"text": "ping"}, "channel_id": "efae7992-0801-4079-bae2-83189b68d71d", "timestamp": 1697944692927, "recipients": ["321e7409-e19a-4608-a623-2bae497568d0", "b42d0cb1-b97a-4c63-bbab-1d456cc26490"], "msg_id": "fae4c198-baca-48d3-ad07-2a7f95e2f0cc", "context": {"recipients": ["321e7409-e19a-4608-a623-2bae497568d0", "b42d0cb1-b97a-4c63-bbab-1d456cc26490"], "group_id": None, "sender": "b42d0cb1-b97a-4c63-bbab-1d456cc26490"}}}
    # need helper class for building msg_up
    wand.on(json.dumps(my_msg_up))
    
    while True:
        time.sleep(1)
    # import time
    # time.sleep(10)