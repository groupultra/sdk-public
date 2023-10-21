import json
import asyncio
from demo_service import DemoService
import aioprocessing
def main():
    # For newly bound channels. It doesn't hurt to bind multiple times.
    bind_to_channels = ['efae7992-0801-4079-bae2-83189b68d71d']
    
    with open("/home/ubuntu/sdk/src/config.json", "r") as f:
        config = json.load(f)
    
    with open("db_settings.json", "r") as f:
        db_settings = json.load(f)

    service = DemoService(db_settings=db_settings, **config)
    service.start(bind_to_channels=bind_to_channels)
    return service
# def run(self):
#     process_forever = aioprocessing.AioProcess(target=self.main, args=())
#     process_forever.start()
    
if __name__ == "__main__":
    # asyncio.run(main())
    service = main()
    service.parent_pipe.coro_send("Hello from parent")
    print("After run ------------------")
    print("After run ------------------")
    print("After run ------------------")
    print("After run ------------------")
    print("After run ------------------")
    print("After run ------------------")