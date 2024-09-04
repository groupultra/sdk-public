.. _moobius_database_database_interface:

###################################################################################
moobius.database.database_interface
###################################################################################

******************************
Module-level functions
******************************

(No module-level functions)

************************************
Class DatabaseInterface
************************************

An abstract base class that is to be inherited by different database backends.
Currently available as of July 2024: JSONDatabase, NullDatabase, and RedisDatabase.

When a MoobiusStorage object is constructed:
>>> MoobiusStorage(self.client_id, channel_id, db_config=self.db_config)
An internal DatabaseInterface is constructed.

Each demo's on_start() function passes calls MoobiusStorage(self.client_id, channel_id, db_config=self.db_config)
The db_config can be a dict or a .json file name. An example:
>>>    [{"implementation": "json", "name": "health_bars", "load": true, "clear": false,
>>>     "settings": {"root_dir": "json_db"}}
>>>    {"implementation": "redis", "name": "mana_bars", "load": true, "clear": false,
>>>     "settings": {"root_dir": "json_db"}}]

The Moobius (service) class, on initialization, create one MoobiusStorage object per channel, unless initalize_channel() is overridden.
Each MoobiusStorage object creates one CachedDict per element in the db-config list, using the "name" to dynamically generate an attribute.
The "implementation" sets the engine to be used by CachedDict.

.. _moobius.database.database_interface.DatabaseInterface.get_value:

DatabaseInterface.get_value
---------------------------------------------------------------------------------------------------------------------



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

* **DatabaseInterface.get_value**(self, key)

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

* __key:__ Key.

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

* The  tuple of (is_success, value).

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



.. _moobius.database.database_interface.DatabaseInterface.set_value:

DatabaseInterface.set_value
---------------------------------------------------------------------------------------------------------------------



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

* **DatabaseInterface.set_value**(self, key, value)

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

* __key:__ Key.

* __value:__ Value.

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

* The  tuple of (is_success=True, key) or (is_success=False, err_message).

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



.. _moobius.database.database_interface.DatabaseInterface.delete_key:

DatabaseInterface.delete_key
---------------------------------------------------------------------------------------------------------------------



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

* **DatabaseInterface.delete_key**(self, key)

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

* __key:__ Key.

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

* The  tuple of (is_success=True, key) or (is_success=False, err_message).

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



.. _moobius.database.database_interface.DatabaseInterface.all_keys:

DatabaseInterface.all_keys
---------------------------------------------------------------------------------------------------------------------



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

* **DatabaseInterface.all_keys**(self)

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

* __(this class constructor accepts no arguments):__

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

* The  iterable of all keys, the details of which depend on the implementation.

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

DatabaseInterface.ABC 

**********************
Internals
**********************
.. toctree::
   :maxdepth: 2

   moobius.database.database_interface_internal_attrs <moobius.database.database_interface_internal_attrs>
