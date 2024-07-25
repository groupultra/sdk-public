.. _moobius_core_wand:

moobius.core.wand
===================================

Module-level functions
===================

.. _moobius.core.wand.sigint_handler:
sigint_handler
-----------------------------------
sigint_handler(signal, frame)

Exits using a special error code that the parent process will recognize as a "Ctrl+C" interrupt.

===================

Class MoobiusWand
===================

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
-----------------------------------
MoobiusWand.__init__(self)

Initialize an "empty" MoobiusWand object.

.. _moobius.core.wand.MoobiusWand.run_job:
MoobiusWand.run_job
-----------------------------------
MoobiusWand.run_job(service)

Runs service.start(), which blocks in an infinite loop, using asyncio.

.. _moobius.core.wand.MoobiusWand.run:
MoobiusWand.run
-----------------------------------
MoobiusWand.run(self, cls, background, \*kwargs)

Starts a service or agent, either on the same process in a blocking infinite loop or on another process.

Parameters:
  cls: A subclass of the Moobius class but NOT an instance.
  background=False: If True, runs on another Process.
  **kwargs: Kwargs passed to the constructor of cls.

No return value.

Example:
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
-----------------------------------
MoobiusWand.stop_all(self, force_exit)

Stops all processes using the_process.kill().
Also stops the asyncio event loop.

.. _moobius.core.wand.MoobiusWand.spell:
MoobiusWand.spell
-----------------------------------
MoobiusWand.spell(self, handle, obj)

Sends a message to a service by putting to it's aioprocessing.AioQueue().

Parameters:
  handle (int): The handle of the service created by the run() function.
  obj (anything picklable): The message to be sent.

No return value

Example:
  >>> wand = MoobiusWand()
  >>> handle = wand.run(...)
  >>> wand.spell(handle=handle, obj=MessageDown(message_type="test", context={"sender": "1", "recipients": ["2"]}))

.. _moobius.core.wand.MoobiusWand.aspell:
MoobiusWand.aspell
-----------------------------------
MoobiusWand.aspell(self, handle, obj)

Async version of spell(), uses q.coro_put(obj) instead of q.put(obj) where q = self.services[handle].queue.

.. _moobius.core.wand.MoobiusWand.__str__:
MoobiusWand.__str__
-----------------------------------
MoobiusWand.__str__(self)

<No doc string>

.. _moobius.core.wand.MoobiusWand.__repr__:
MoobiusWand.__repr__
-----------------------------------
MoobiusWand.__repr__(self)

<No doc string>
