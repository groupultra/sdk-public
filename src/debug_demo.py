import json
import asyncio
from demo_service import DemoService
from moobius.moobius_wand import MoobiusWand
import aioprocessing
from moobius.basic._types import *
from moobius.basic._logging_config import logger
import time

# For newly bound channels. It doesn't hurt to bind multiple times.
bind_to_channels = ['3457120e-8f05-4786-a3d4-0b53d70e6bba']

def main():
    with open("config.json", "r") as f:
        config = json.load(f)
    
    with open("db_settings.json", "r") as f:
        db_settings = json.load(f)

    service = DemoService(db_settings=db_settings, **config)
    service.start(bind_to_channels=bind_to_channels)
    return service

if __name__ == "__main__":
    
    service = main()
    wand = service.get_wand()
    wand.send_ping()
    wand.send_ping()
    wand.send_ping()
    wand.send_ping()
    wand.send_ping()
    real_characters = wand.fetch_real_characters(bind_to_channels[0])
    logger.info(f"real_characters {real_characters}")
    wand.send_msg_down(channel_id=bind_to_channels[0], 
                       recipients=["321e7409-e19a-4608-a623-2bae497568d0", "b42d0cb1-b97a-4c63-bbab-1d456cc26490"],
                       subtype="text",
                       message_content="Hello! I'm Ayaka!",
                       sender="321e7409-e19a-4608-a623-2bae497568d0")

    my_msg_up = {"type": "msg_up", "body": {"subtype": "text", "content": {"text": "ping"}, "channel_id": "efae7992-0801-4079-bae2-83189b68d71d", "timestamp": 1697944692927, "recipients": ["321e7409-e19a-4608-a623-2bae497568d0", "b42d0cb1-b97a-4c63-bbab-1d456cc26490"], "msg_id": "fae4c198-baca-48d3-ad07-2a7f95e2f0cc", "context": {"recipients": ["321e7409-e19a-4608-a623-2bae497568d0", "b42d0cb1-b97a-4c63-bbab-1d456cc26490"], "group_id": None, "sender": "b42d0cb1-b97a-4c63-bbab-1d456cc26490"}}}
    # need helper class for building msg_up
    wand.on(json.dumps(my_msg_up))