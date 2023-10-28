import json
import asyncio
from cicada_service import CicadaService

async def main():
    # For newly bound channels. It doesn't hurt to bind multiple times.
    bind_to_channels = []
    
    with open("cicada/cicada_config.json", "r") as f:
        config = json.load(f)
    
    with open("cicada/cicada_db_settings.json", "r") as f:
        db_settings = json.load(f)

    service = CicadaService(db_settings=db_settings, **config)
    await service.start(bind_to_channels=bind_to_channels)

if __name__ == "__main__":
    asyncio.run(main())