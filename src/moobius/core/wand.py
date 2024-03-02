# Runs services and casts spells (sending commands to services).

from moobius import utils
import asyncio
from multiprocessing import Process
import time
from loguru import logger
import signal
import os

class MoobiusWand:
    """
    MoobiusWand is a class that starts and manages services.
    It can also be used to send messages to a service using the spell() function or the async aspell() function.
    To use this class, you need to specify the service config in the config file.
    """

    def __init__(self):
        """Initialize an "empty" MoobiusWand object."""
        self.services = {}
        self.processes = {}
        self.current_service_handle = 0     # TODO: use handle to terminate or restart a service
        signal.signal(signal.SIGINT, self.stop)

    @staticmethod
    def run_job(service):
        asyncio.run(service.start())

    def run(self, cls, background=False, **kwargs):
        """
        Starts a service or agent.

        Parameters:
          cls (Class object). A subclass of the SDK class but NOT an instance.
          background=False: If True run on another Process instead of creating an infinite loop.
          **kwargs: These are passed to the constructor of cls.

        No return value.

        Example:
          >>> wand = MoobiusWand()
          >>> handle = wand.run(
          >>>     CicadaService,
          >>>     config_path="config/service.json",
          >>>     db_config_path="config/db.json",
          >>>     background=True)
        """
        service = cls(**kwargs)

        if background:
            p_service = Process(target=self.run_job, args=(service, ), name=f"{cls.__name__}<handle={self.current_service_handle}>")
            p_service.start()

            time.sleep(1)   # IMPORTANT! TODO: Why is it important? Is there a way to check the service is ready so that it if takes >1 sec this fn can wait?

            self.current_service_handle += 1
            self.services[self.current_service_handle] = service
            self.processes[self.current_service_handle] = p_service

            return self.current_service_handle
        else:
            asyncio.run(service.start())

    def stop(self, signum, frame):
        """Stops all processes using the_process.kill()
           Also stops asyncio's event loop.
           TODO: Unused arguments sgnum and frame. Maybe renamining this to stop_all()?"""
        for _process in self.processes.values():
            _process.kill()
            logger.info(f"Service {_process.name} terminated")
        asyncio.get_event_loop().stop()

    def spell(self, handle, obj):
        """
        Send a message to a service.

        Parameters:
          handle (int): The handle of the service created by the run() function.
          obj (anything picklable): The message to be sent.

        No return value

        Example:
          >>> wand = MoobiusWand()
          >>> handle = wand.run(
          >>>     CicadaService,
          >>>     config_path="config/service.json",
          >>>     db_config_path="config/db.json",
          >>>     background=True)
          >>> wand.spell(handle=handle, obj=MessageDown(msg_type="test", context={"sender": "1", "recipients": ["2"]}))
        """
        if handle in self.services:
            try:
                self.services[handle].queue.put(obj)
            except Exception as e:
                logger.error(e)
        else:
            logger.error(f"Service handle {handle} not found")

    async def aspell(self, handle, obj):
        """Async version of spell(), uses q.coro_put(obj) instead of q.put(obj) where q = self.services[handle].queue."""
        if handle in self.services:
            try:
                await self.services[handle].queue.coro_put(obj)
            except Exception as e:
                logger.error(e)
        else:
            logger.error(f"Service handle {handle} not found")

    def __str__(self):
        return f'moobius.MoobiusWand(services={list(self.services.keys())}, processes={list(self.processes.keys())})'
    def __repr__(self):
        return self.__str__()
