import asyncio
from signal import SIGINT, SIGTERM
from dataclasses import asdict
from dacite import from_dict
import uuid
import json
import time
import traceback

from multiprocessing import Process

from loguru import logger
from moobius.moobius_basic_service import MoobiusBasicService

class MoobiusWand:
    def __init__(self):
        self.services = {}
        self.processes = {}
        self.current_service_handle = 0     # todo: use handle to terminate or restart a service

    @staticmethod
    def run_job(service):
        asyncio.run(service.start())

    def run(self, service_cls, background=False, **kwargs):
        service = service_cls(**kwargs)

        if background:
            p_service = Process(target=self.run_job, args=(service,), name=f"{service_cls.__name__}<handle={self.current_service_handle}>")
            p_service.start()
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
