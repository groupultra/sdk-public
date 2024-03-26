.. _moobius_core_wand:

moobius.core.wand
===================================



===================


Class MoobiusWand
===================

MoobiusWand is a class that starts and manages services.
It can also be used to send messages to a service using the spell() function or the async aspell() function.
To use this class, you need to specify the service config in the config file.

.. _moobius.core.wand.MoobiusWand.__init__:
MoobiusWand.__init__
-----------------------------------
**MoobiusWand.__init__(self)**

Initialize an "empty" MoobiusWand object.

.. _moobius.core.wand.MoobiusWand.run_job:
MoobiusWand.run_job
-----------------------------------
**MoobiusWand.run_job(service)**

<No doc string>

.. _moobius.core.wand.MoobiusWand.run:
MoobiusWand.run
-----------------------------------
**MoobiusWand.run(self, cls, background, \*kwargs)**

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

.. _moobius.core.wand.MoobiusWand.stop:
MoobiusWand.stop
-----------------------------------
**MoobiusWand.stop(self, signum, frame)**

Stops all processes using the_process.kill()
Also stops asyncio's event loop.
TODO: Unused arguments sgnum and frame. Maybe renamining this to stop_all()?

.. _moobius.core.wand.MoobiusWand.spell:
MoobiusWand.spell
-----------------------------------
**MoobiusWand.spell(self, handle, obj)**

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
  >>> wand.spell(handle=handle, obj=MessageDown(message_type="test", context={"sender": "1", "recipients": ["2"]}))

.. _moobius.core.wand.MoobiusWand.aspell:
MoobiusWand.aspell
-----------------------------------
**MoobiusWand.aspell(self, handle, obj)**

Async version of spell(), uses q.coro_put(obj) instead of q.put(obj) where q = self.services[handle].queue.

.. _moobius.core.wand.MoobiusWand.__str__:
MoobiusWand.__str__
-----------------------------------
**MoobiusWand.__str__(self)**

<No doc string>

.. _moobius.core.wand.MoobiusWand.__repr__:
MoobiusWand.__repr__
-----------------------------------
**MoobiusWand.__repr__(self)**

<No doc string>