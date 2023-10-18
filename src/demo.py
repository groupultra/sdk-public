import json
import asyncio
from demo_agent import DemoAgent
import aioprocessing
def main():
    # For newly bound channels. It doesn't hurt to bind multiple times.
    bind_to_channels = ['efae7992-0801-4079-bae2-83189b68d71d']
    
    with open("/home/ubuntu/sdk/src/config.json", "r") as f:
        config = json.load(f)
    
    service_agent = DemoAgent(**config)
    service_agent.start(bind_to_channels=bind_to_channels)
    return service_agent
    # self.parent_pipe, self.child_pipe = aioprocessing.AioPipe()

# def run(self):
#     process_forever = aioprocessing.AioProcess(target=self.main, args=())
#     process_forever.start()
    
if __name__ == "__main__":
    # asyncio.run(main())
    service_agent = main()
    service_agent.parent_pipe.coro_send("Hello from parent")
    print("After run ------------------")
    print("After run ------------------")
    print("After run ------------------")
    print("After run ------------------")
    print("After run ------------------")
    print("After run ------------------")