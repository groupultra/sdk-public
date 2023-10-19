import json
import asyncio
from demo_service import DemoService

async def main():
    # For newly bound channels. It doesn't hurt to bind multiple times.
    bind_to_channels = ['46ed25de-6070-46b0-b13d-a18cb316c090', 'e5842a46-4d8e-4771-80fe-8fa090dde947']
    
    with open("config.json", "r") as f:
        config = json.load(f)
    
    with open("db_settings.json", "r") as f:
        db_settings = json.load(f)

    service = DemoService(db_settings=db_settings, **config)
    await service.start(bind_to_channels=bind_to_channels)

if __name__ == "__main__":
    asyncio.run(main())