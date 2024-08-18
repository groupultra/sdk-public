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

Exits using a special error code that the parent process will recognize as a "Ctrl+C" interrupt..

* Signature

    * sigint_handler(signal, frame)

* Parameters

    * signal: Integer signal.
    
    * frame: Stack frame.

* Returns

  * The os._exit.

* Raises

  * (this function does not raise any notable errors)

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

Initialize an "empty" MoobiusWand object.

* Signature

    * MoobiusWand.__init__(self)

* Parameters

    * (this class constructor accepts no arguments)

* Returns

  * (Class constructors have no explicit return value)

* Raises

  * (this function does not raise any notable errors)

.. _moobius.core.wand.MoobiusWand.run_job:

MoobiusWand.run_job
---------------------------------------------------------------------------------------------------------------------

Runs service.start(), which blocks in an infinite loop, using asyncio.

* Signature

    * MoobiusWand.run_job(service)

* Parameters

    * service: Moobius service.

* Returns

  * The Never.

* Raises

  * (this function does not raise any notable errors)

.. _moobius.core.wand.MoobiusWand.run:

MoobiusWand.run
---------------------------------------------------------------------------------------------------------------------

Starts a service or agent, either on the same process in a blocking infinite loop or on another process.

* Signature

    * MoobiusWand.run(self, cls, background, kwargs)

* Parameters

    * cls: A subclass of the Moobius class but NOT an instance.
    
    * background: If True, runs on another Process.
    
    * kwargs=False: Kwargs passed to the constructor of cls.

* Returns

  * The None.

* Raises

  * (this function does not raise any notable errors)

* Example

    >>> wand = MoobiusWand()
      >>> handle = wand.run(
      >>>     MyService,
      >>>     log_file="logs/service.log",
      >>>     error_log_file="logs/error.log",
      >>>     terminal_log_level="INFO",
      >>>     config_path="config/service.json",
      >>>     db_config_path="config/db.json",
      >>>     background=True)

.. _moobius.core.wand.MoobiusWand.stop_all:

MoobiusWand.stop_all
---------------------------------------------------------------------------------------------------------------------

Stops all processes using the_process.kill()..
Also stops the asyncio event loop.

* Signature

    * MoobiusWand.stop_all(self, force_exit)

* Parameters

    * force_exit=False: N option to force-quit.

* Returns

  * The exit.

* Raises

  * (this function does not raise any notable errors)

.. _moobius.core.wand.MoobiusWand.spell:

MoobiusWand.spell
---------------------------------------------------------------------------------------------------------------------

Sends a message to a service by putting to it's aioprocessing.AioQueue().

* Signature

    * MoobiusWand.spell(self, handle, obj)

* Parameters

    * handle: The handle of the service created by the run() function.
    
    * obj: The message to be sent.

* Returns

  * The None.

* Raises

  * (this function does not raise any notable errors)

* Example

    >>> wand = MoobiusWand()
      >>> handle = wand.run(...)
      >>> wand.spell(handle=handle, obj=MessageDown(message_type="test", context={"sender": "1", "recipients": ["2"]}))

.. _moobius.core.wand.MoobiusWand.aspell:

MoobiusWand.aspell
---------------------------------------------------------------------------------------------------------------------

Async version of spell(), uses q.coro_put(obj) instead of q.put(obj) where q = self.services[handle].queue..

* Signature

    * MoobiusWand.aspell(self, handle, obj)

* Parameters

    * handle: Handle int.
    
    * obj: The generic pickleable object.

* Returns

  * The None.

* Raises

  * (this function does not raise any notable errors)

.. _moobius.core.wand.MoobiusWand.__str__:

MoobiusWand.__str__
---------------------------------------------------------------------------------------------------------------------

The string output function for debugging.

* Signature

    * MoobiusWand.__str__(self)

* Parameters

    * (this class constructor accepts no arguments)

* Returns

  * The  easy-to-read string summary.

* Raises

  * (this function does not raise any notable errors)

.. _moobius.core.wand.MoobiusWand.__repr__:

MoobiusWand.__repr__
---------------------------------------------------------------------------------------------------------------------

The string output function for debugging.

* Signature

    * MoobiusWand.__repr__(self)

* Parameters

    * (this class constructor accepts no arguments)

* Returns

  * The  easy-to-read string summary.

* Raises

  * (this function does not raise any notable errors)

Class attributes
--------------------


