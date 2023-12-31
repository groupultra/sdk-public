# wand.py

import asyncio
from multiprocessing import Process
import time
from loguru import logger
import signal
import os

class MoobiusWand:
    '''
    MoobiusWand is a class that starts and manages services.
    It can also be used to send messages to a service using the spell() function or the aspell() function.
    To use this class, you need to specify the service config in the config file.
    
    Functions:
        run(): Run a service.
        spell(): Send a message to a service.
        aspell(): Async version of spell().
    '''
    def __init__(self):
        '''
        Initialize a MoobiusWand object.
        
        Parameters:
            None
        
        Returns:
            None
        
        Example:
            >>> wand = MoobiusWand()
        '''
        self.services = {}
        self.processes = {}
        self.current_service_handle = 0     # todo: use handle to terminate or restart a service
        signal.signal(signal.SIGINT, self.stop)
        
    @staticmethod
    def run_job(service):
        asyncio.run(service.start())

    def run(self, cls, background=False, **kwargs):
        '''
        Run a service.
        
        Parameters:
            cls: class
                The class of the service.
            background: bool
                Whether to run the service in the background.
            kwargs: dict
                The parameters of the service.
        
        Returns:
            None
        
        Example:
            >>> wand = MoobiusWand()
            >>> handle = wand.run(
            >>>     CicadaService,
            >>>     service_config_path="config/service.json",
            >>>     db_config_path="config/db.json",
            >>>     background=True
            >>> )
        '''
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
            
    def stop(self, signum, frame):
        for _process in self.processes.values():
            _process.kill()
            print(f"Service {_process.name} terminated")
        asyncio.get_event_loop().stop()
        
    def spell(self, handle, obj):
        '''
        Send a message to a service.
        
        Parameters:
            handle: int
                The handle of the service, created by the run() function.
            obj: object
                The message to be sent.
            
        Returns:
            None
        
        Example:
            >>> wand = MoobiusWand()
            >>> handle = wand.run(
            >>>     CicadaService,
            >>>     service_config_path="config/service.json",
            >>>     db_config_path="config/db.json",
            >>>     background=True
            >>> )
            >>> wand.spell(handle=handle, obj=MessageDown(msg_type="test", context={"sender": "1", "recipients": ["2"]}))
        '''
        if handle in self.services:
            try:
                self.services[handle].queue.put(obj)
            except Exception as e:
                logger.error(e)
        else:
            logger.error(f"Service handle {handle} not found")

    async def aspell(self, handle, obj):
        '''
        Async version of spell().
        
        Parameters:
            handle: int
                The handle of the service, created by the run() function.
            obj: object
                The message to be sent.
            
        Returns:
            None
        
        Example:
            >>> wand = MoobiusWand()
            >>> handle = wand.run(
            >>>     CicadaService,
            >>>     service_config_path="config/service.json",
            >>>     db_config_path="config/db.json",
            >>>     background=True
            >>> )
            >>> await wand.aspell(handle=handle, obj=MessageDown(msg_type="test", context={"sender": "1", "recipients": ["2"]}))
        '''
        if handle in self.services:
            try:
                await self.services[handle].queue.coro_put(obj)
            except Exception as e:
                logger.error(e)
        else:
            logger.error(f"Service handle {handle} not found")
