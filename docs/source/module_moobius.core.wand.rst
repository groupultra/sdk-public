.. _moobius_core_wand:

###################################################################################
moobius.core.wand
###################################################################################

******************************
Module-level functions
******************************

.. _moobius.core.wand.sigint_handler:

sigint_handler
---------------------------------------------------------------------------------------------------------------------
sigint_handler(signal, frame)


Exits using a special error code that the parent process will recognize as a "Ctrl+C" interrupt..
  Parameters:
    signal: Integer signal.
    frame: Stack frame.
  Returns:
    The os._exit.
  Raises:
    (this function does not raise any notable errors)


************************************
Class MoobiusWand
************************************

Starts and manages services.
It can also be used to send messages to a service using the spell() function or the async aspell() function.

The typical use-case and suggested file paths:
  >>> wand = MoobiusWand()
  >>> handle = wand.run(MyService, config_path="config/service.json", db_config_path="config/db.json",
  >>>                   log_file="logs/service.log", error_log_file="logs/error.log", terminal_log_level="INFO",
  >>>                   is_agent=False, background=True)
  >>> wand.spell(handle, xyz_message) # Use to send data to the service.

.. _moobius.core.wand.MoobiusWand.__init__:

MoobiusWand.__init__
---------------------------------------------------------------------------------------------------------------------
MoobiusWand.__init__(self)


Initialize an "empty" MoobiusWand object.
  Parameters:
    (this class constructor accepts no arguments)
  Returns:
    (Class constructors have no explicit return value)
  Raises:
    (this function does not raise any notable errors)


.. _moobius.core.wand.MoobiusWand.run_job:

MoobiusWand.run_job
---------------------------------------------------------------------------------------------------------------------
MoobiusWand.run_job(service)


Runs service.start(), which blocks in an infinite loop, using asyncio.
  Parameters:
    service: Moobius service.
  Returns:
    The Never.
  Raises:
    (this function does not raise any notable errors)


.. _moobius.core.wand.MoobiusWand.run:

MoobiusWand.run
---------------------------------------------------------------------------------------------------------------------
MoobiusWand.run(self, cls, background, \*kwargs)


Starts a service or agent, either on the same process in a blocking infinite loop or on another process.
  Parameters:
    cls: A subclass of the Moobius class but NOT an instance.
    background=False: If True, runs on another Process.
    **kwargs: Kwargs passed to the constructor of cls.
  Returns:
    The None.
    
    Example:
      >>> wand = MoobiusWand()
      >>> handle = wand.run(
      >>>     MyService,
      >>>     log_file="logs/service.log",
      >>>     error_log_file="logs/error.log",
      >>>     terminal_log_level="INFO",
      >>>     config_path="config/service.json",
      >>>     db_config_path="config/db.json",
      >>>     background=True).
  Raises:
    (this function does not raise any notable errors)


.. _moobius.core.wand.MoobiusWand.stop_all:

MoobiusWand.stop_all
---------------------------------------------------------------------------------------------------------------------
MoobiusWand.stop_all(self, force_exit)


Stops all processes using the_process.kill()..
Also stops the asyncio event loop.
  Parameters:
    force_exit: N option to force-quit.
  Returns:
    The exit.
  Raises:
    (this function does not raise any notable errors)


.. _moobius.core.wand.MoobiusWand.spell:

MoobiusWand.spell
---------------------------------------------------------------------------------------------------------------------
MoobiusWand.spell(self, handle, obj)


Sends a message to a service by putting to it's aioprocessing.AioQueue().
  Parameters:
    handle (int): The handle of the service created by the run() function.
    obj (anything picklable): The message to be sent.
  Returns:
    The None.
    
    Example:
      >>> wand = MoobiusWand()
      >>> handle = wand.run(...)
      >>> wand.spell(handle=handle, obj=MessageDown(message_type="test", context={"sender": "1", "recipients": ["2"]})).
  Raises:
    (this function does not raise any notable errors)


.. _moobius.core.wand.MoobiusWand.aspell:

MoobiusWand.aspell
---------------------------------------------------------------------------------------------------------------------
MoobiusWand.aspell(self, handle, obj)


Async version of spell(), uses q.coro_put(obj) instead of q.put(obj) where q = self.services[handle].queue..
  Parameters:
    handle: Handle int.
    obj: The generic pickleable object.
  Returns:
    The None.
  Raises:
    (this function does not raise any notable errors)


.. _moobius.core.wand.MoobiusWand.__str__:

MoobiusWand.__str__
---------------------------------------------------------------------------------------------------------------------
MoobiusWand.__str__(self)


The string output function for debugging.
  Parameters:
    (this class constructor accepts no arguments)
  Returns:
    The  easy-to-read string summary.
  Raises:
    (this function does not raise any notable errors)


.. _moobius.core.wand.MoobiusWand.__repr__:

MoobiusWand.__repr__
---------------------------------------------------------------------------------------------------------------------
MoobiusWand.__repr__(self)


The string output function for debugging.
  Parameters:
    (this class constructor accepts no arguments)
  Returns:
    The  easy-to-read string summary.
  Raises:
    (this function does not raise any notable errors)


Class attributes
--------------------


