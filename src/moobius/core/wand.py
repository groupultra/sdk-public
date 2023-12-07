# wand.py

import asyncio
from multiprocessing import Process
import time
from loguru import logger


class MoobiusWand:
    def __init__(self):
        self.services = {}
        self.processes = {}
        self.current_service_handle = 0     # todo: use handle to terminate or restart a service

    @staticmethod
    def run_job(service):
        asyncio.run(service.start())

    def run(self, cls, background=False, **kwargs):
        service = cls(**kwargs)
        
        if background:
            p_service = Process(target=self.run_job, args=(service, ), name=f"{cls.__name__}<handle={self.current_service_handle}>")
            p_service.start()
            
            time.sleep(1)   # IMPORTANT!
            
            self.current_service_handle += 1
            self.services[self.current_service_handle] = service
            self.processes[self.current_service_handle] = p_service

            return self.current_service_handle
        else:
            asyncio.run(service.start())

    def spell(self, handle, obj):
        if handle in self.services:
            try:
                self.services[handle].queue.put(obj)
            except Exception as e:
                logger.error(e)
        else:
            logger.error(f"Service handle {handle} not found")

    async def aspell(self, handle, obj):
        if handle in self.services:
            try:
                await self.services[handle].queue.coro_put(obj)
            except Exception as e:
                logger.error(e)
        else:
            logger.error(f"Service handle {handle} not found")
