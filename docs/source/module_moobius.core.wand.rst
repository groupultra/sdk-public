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

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="fsig">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **sigint_handler**(signal, frame)

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="fparam">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* __signal:__ Integer signal.

* __frame:__ Stack frame.

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="freturn">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* The os._exit.

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="fraises">
          <b>Raises:</b>
    </p>
  </body>
  </embed>

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

.. _moobius.core.wand.MoobiusWand.run_job:

MoobiusWand.run_job
---------------------------------------------------------------------------------------------------------------------



Runs service.start(), which blocks in an infinite loop, using asyncio.

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="fsig">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **MoobiusWand.run_job**(service)

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="fparam">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* __service:__ Moobius service.

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="freturn">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* The Never.

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="fraises">
          <b>Raises:</b>
    </p>
  </body>
  </embed>

* (this function does not raise any notable errors)



.. _moobius.core.wand.MoobiusWand.run:

MoobiusWand.run
---------------------------------------------------------------------------------------------------------------------



Starts a service or agent, either on the same process in a blocking infinite loop or on another process.

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="fsig">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **MoobiusWand.run**(self, cls, background, kwargs)

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="fparam">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* __cls:__ A subclass of the Moobius class but NOT an instance.

* __background:__ If True, runs on another Process.

* __kwargs=False:__ Kwargs passed to the constructor of cls.

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="freturn">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* None.

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="fraises">
          <b>Raises:</b>
    </p>
  </body>
  </embed>

* (this function does not raise any notable errors)


.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="fexample">
          <b>Example:</b>
    </p>
  </body>
  </embed>

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

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="fsig">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **MoobiusWand.stop_all**(self, force_exit)

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="fparam">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* __force_exit=False:__ N option to force-quit.

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="freturn">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* The exit.

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="fraises">
          <b>Raises:</b>
    </p>
  </body>
  </embed>

* (this function does not raise any notable errors)



.. _moobius.core.wand.MoobiusWand.spell:

MoobiusWand.spell
---------------------------------------------------------------------------------------------------------------------



Sends a message to a service by putting to it's aioprocessing.AioQueue().

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="fsig">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **MoobiusWand.spell**(self, handle, obj)

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="fparam">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* __handle:__ The handle of the service created by the run() function.

* __obj:__ The message to be sent.

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="freturn">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* None.

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="fraises">
          <b>Raises:</b>
    </p>
  </body>
  </embed>

* (this function does not raise any notable errors)


.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="fexample">
          <b>Example:</b>
    </p>
  </body>
  </embed>

    >>> wand = MoobiusWand()
      >>> handle = wand.run(...)
      >>> wand.spell(handle=handle, obj=MessageDown(message_type="test", context={"sender": "1", "recipients": ["2"]}))



.. _moobius.core.wand.MoobiusWand.aspell:

MoobiusWand.aspell
---------------------------------------------------------------------------------------------------------------------



Async version of spell(), uses q.coro_put(obj) instead of q.put(obj) where q = self.services[handle].queue..

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="fsig">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **MoobiusWand.aspell**(self, handle, obj)

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="fparam">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* __handle:__ Handle int.

* __obj:__ The generic pickleable object.

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="freturn">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* None.

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="fraises">
          <b>Raises:</b>
    </p>
  </body>
  </embed>

* (this function does not raise any notable errors)



Class attributes
--------------------



**********************
Internals
**********************
.. toctree::
   :maxdepth: 2

   moobius.core.wand_internal_attrs <moobius.core.wand_internal_attrs>
