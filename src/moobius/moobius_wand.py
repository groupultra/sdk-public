import asyncio
from dataclasses import asdict
from dacite import from_dict
import uuid
import json
import time
import traceback

from multiprocessing import Process

from moobius.basic.logging_config import log
from moobius.moobius_basic_service import MoobiusBasicService

class MoobiusWand:
    def __init__(self):
        self.services = {}
        self.processes = {}
        self.current_service_handle = 0     # todo: use handle to terminate or restart a service

    @staticmethod
    def run_job(service):
        asyncio.run(service.start())

    def run(self, service_cls, service_config_path, db_config_path, background=False):
        service = service_cls(service_config_path=service_config_path, db_config_path=db_config_path)

        if background:
            p_service = Process(target=self.run_job, args=(service,))
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
                traceback.print_exc()
                log(f"MoobiusWand.spell(): error {e}", print_to_console=True)
        else:
            log(f"MoobiusWand.spell(): service handle {handle} not found", print_to_console=True)

    async def aspell(self, handle, obj):
        if handle in self.services:
            try:
                await self.services[handle].queue.coro_put(obj)
            except Exception as e:
                traceback.print_exc()
                log(f"MoobiusWand.aspell(): error {e}", print_to_console=True)
        else:
            log(f"MoobiusWand.aspell() service handle {handle} not found", print_to_console=True)
