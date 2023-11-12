import json
import asyncio
from demo_service import DemoService
import aioprocessing
def main():
    # For newly bound channels. It doesn't hurt to bind multiple times.
    bind_to_channels = ['efae7992-0801-4079-bae2-83189b68d71d']
    
    with open(r"C:\\Users\\Administrator\\Desktop\\ss\\sdk\\src\\config.json", "r") as f:
        config = json.load(f)
    
    with open("db_settings.json", "r") as f:
        db_settings = json.load(f)

    service = DemoService(db_settings=db_settings, **config)
    service.start(bind_to_channels=bind_to_channels)
    return service
    
if __name__ == "__main__":
    service = main()
    # service.wand.send_ping()