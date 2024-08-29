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
    <style>
        .style463 {
            background-color: #BBBBDD;
            padding: 5px;
            border-radius: 2px;
            font-family: Times New Roman;
            color: black;
            font-size: 16px;
        }
    </style>
  </head>
  <body>
    <p class="style463">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **sigint_handler**(signal, frame)

.. raw:: html

  <embed>
  <head>
    <style>
        .style464 {
            background-color: #BBDDDD;
            padding: 5px;
            border-radius: 2px;
            font-family: Times New Roman;
            color: black;
            font-size: 16px;
        }
    </style>
  </head>
  <body>
    <p class="style464">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* **signal:** Integer signal.

* **frame:** Stack frame.

.. raw:: html

  <embed>
  <head>
    <style>
        .style465 {
            background-color: #BBBBDD;
            padding: 5px;
            border-radius: 2px;
            font-family: Times New Roman;
            color: black;
            font-size: 16px;
        }
    </style>
  </head>
  <body>
    <p class="style465">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* The os._exit.

.. raw:: html

  <embed>
  <head>
    <style>
        .style466 {
            background-color: #DDBBBB;
            padding: 5px;
            border-radius: 2px;
            font-family: Times New Roman;
            color: black;
            font-size: 16px;
        }
    </style>
  </head>
  <body>
    <p class="style466">
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
    <style>
        .style467 {
            background-color: #BBBBDD;
            padding: 5px;
            border-radius: 2px;
            font-family: Times New Roman;
            color: black;
            font-size: 16px;
        }
    </style>
  </head>
  <body>
    <p class="style467">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **MoobiusWand.run_job**(service)

.. raw:: html

  <embed>
  <head>
    <style>
        .style468 {
            background-color: #BBDDDD;
            padding: 5px;
            border-radius: 2px;
            font-family: Times New Roman;
            color: black;
            font-size: 16px;
        }
    </style>
  </head>
  <body>
    <p class="style468">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* **service:** Moobius service.

.. raw:: html

  <embed>
  <head>
    <style>
        .style469 {
            background-color: #BBBBDD;
            padding: 5px;
            border-radius: 2px;
            font-family: Times New Roman;
            color: black;
            font-size: 16px;
        }
    </style>
  </head>
  <body>
    <p class="style469">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* The Never.

.. raw:: html

  <embed>
  <head>
    <style>
        .style470 {
            background-color: #DDBBBB;
            padding: 5px;
            border-radius: 2px;
            font-family: Times New Roman;
            color: black;
            font-size: 16px;
        }
    </style>
  </head>
  <body>
    <p class="style470">
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
    <style>
        .style471 {
            background-color: #BBBBDD;
            padding: 5px;
            border-radius: 2px;
            font-family: Times New Roman;
            color: black;
            font-size: 16px;
        }
    </style>
  </head>
  <body>
    <p class="style471">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **MoobiusWand.run**(self, cls, background, kwargs)

.. raw:: html

  <embed>
  <head>
    <style>
        .style472 {
            background-color: #BBDDDD;
            padding: 5px;
            border-radius: 2px;
            font-family: Times New Roman;
            color: black;
            font-size: 16px;
        }
    </style>
  </head>
  <body>
    <p class="style472">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* **cls:** A subclass of the Moobius class but NOT an instance.

* **background:** If True, runs on another Process.

* **kwargs=False:** Kwargs passed to the constructor of cls.

.. raw:: html

  <embed>
  <head>
    <style>
        .style473 {
            background-color: #BBBBDD;
            padding: 5px;
            border-radius: 2px;
            font-family: Times New Roman;
            color: black;
            font-size: 16px;
        }
    </style>
  </head>
  <body>
    <p class="style473">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* None.

.. raw:: html

  <embed>
  <head>
    <style>
        .style474 {
            background-color: #DDBBBB;
            padding: 5px;
            border-radius: 2px;
            font-family: Times New Roman;
            color: black;
            font-size: 16px;
        }
    </style>
  </head>
  <body>
    <p class="style474">
          <b>Raises:</b>
    </p>
  </body>
  </embed>

* (this function does not raise any notable errors)


.. raw:: html

  <embed>
  <head>
    <style>
        .style475 {
            background-color: #DDBBDD;
            padding: 5px;
            border-radius: 2px;
            font-family: Times New Roman;
            color: black;
            font-size: 16px;
        }
    </style>
  </head>
  <body>
    <p class="style475">
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
    <style>
        .style476 {
            background-color: #BBBBDD;
            padding: 5px;
            border-radius: 2px;
            font-family: Times New Roman;
            color: black;
            font-size: 16px;
        }
    </style>
  </head>
  <body>
    <p class="style476">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **MoobiusWand.stop_all**(self, force_exit)

.. raw:: html

  <embed>
  <head>
    <style>
        .style477 {
            background-color: #BBDDDD;
            padding: 5px;
            border-radius: 2px;
            font-family: Times New Roman;
            color: black;
            font-size: 16px;
        }
    </style>
  </head>
  <body>
    <p class="style477">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* **force_exit=False:** N option to force-quit.

.. raw:: html

  <embed>
  <head>
    <style>
        .style478 {
            background-color: #BBBBDD;
            padding: 5px;
            border-radius: 2px;
            font-family: Times New Roman;
            color: black;
            font-size: 16px;
        }
    </style>
  </head>
  <body>
    <p class="style478">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* The exit.

.. raw:: html

  <embed>
  <head>
    <style>
        .style479 {
            background-color: #DDBBBB;
            padding: 5px;
            border-radius: 2px;
            font-family: Times New Roman;
            color: black;
            font-size: 16px;
        }
    </style>
  </head>
  <body>
    <p class="style479">
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
    <style>
        .style480 {
            background-color: #BBBBDD;
            padding: 5px;
            border-radius: 2px;
            font-family: Times New Roman;
            color: black;
            font-size: 16px;
        }
    </style>
  </head>
  <body>
    <p class="style480">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **MoobiusWand.spell**(self, handle, obj)

.. raw:: html

  <embed>
  <head>
    <style>
        .style481 {
            background-color: #BBDDDD;
            padding: 5px;
            border-radius: 2px;
            font-family: Times New Roman;
            color: black;
            font-size: 16px;
        }
    </style>
  </head>
  <body>
    <p class="style481">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* **handle:** The handle of the service created by the run() function.

* **obj:** The message to be sent.

.. raw:: html

  <embed>
  <head>
    <style>
        .style482 {
            background-color: #BBBBDD;
            padding: 5px;
            border-radius: 2px;
            font-family: Times New Roman;
            color: black;
            font-size: 16px;
        }
    </style>
  </head>
  <body>
    <p class="style482">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* None.

.. raw:: html

  <embed>
  <head>
    <style>
        .style483 {
            background-color: #DDBBBB;
            padding: 5px;
            border-radius: 2px;
            font-family: Times New Roman;
            color: black;
            font-size: 16px;
        }
    </style>
  </head>
  <body>
    <p class="style483">
          <b>Raises:</b>
    </p>
  </body>
  </embed>

* (this function does not raise any notable errors)


.. raw:: html

  <embed>
  <head>
    <style>
        .style484 {
            background-color: #DDBBDD;
            padding: 5px;
            border-radius: 2px;
            font-family: Times New Roman;
            color: black;
            font-size: 16px;
        }
    </style>
  </head>
  <body>
    <p class="style484">
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
    <style>
        .style485 {
            background-color: #BBBBDD;
            padding: 5px;
            border-radius: 2px;
            font-family: Times New Roman;
            color: black;
            font-size: 16px;
        }
    </style>
  </head>
  <body>
    <p class="style485">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **MoobiusWand.aspell**(self, handle, obj)

.. raw:: html

  <embed>
  <head>
    <style>
        .style486 {
            background-color: #BBDDDD;
            padding: 5px;
            border-radius: 2px;
            font-family: Times New Roman;
            color: black;
            font-size: 16px;
        }
    </style>
  </head>
  <body>
    <p class="style486">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* **handle:** Handle int.

* **obj:** The generic pickleable object.

.. raw:: html

  <embed>
  <head>
    <style>
        .style487 {
            background-color: #BBBBDD;
            padding: 5px;
            border-radius: 2px;
            font-family: Times New Roman;
            color: black;
            font-size: 16px;
        }
    </style>
  </head>
  <body>
    <p class="style487">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* None.

.. raw:: html

  <embed>
  <head>
    <style>
        .style488 {
            background-color: #DDBBBB;
            padding: 5px;
            border-radius: 2px;
            font-family: Times New Roman;
            color: black;
            font-size: 16px;
        }
    </style>
  </head>
  <body>
    <p class="style488">
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
