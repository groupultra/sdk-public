.. _moobius_database_null_database:

###################################################################################
moobius.database.null_database
###################################################################################

******************************
Module-level functions
******************************

(No module-level functions)

************************************
Class NullDatabase
************************************

The NullDatabase is like /dev/null; nothing is ever stored.
Get returns (True, None) and set/delete return (True, "").

.. _moobius.database.null_database.NullDatabase.get_value:

NullDatabase.get_value
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

* **NullDatabase.get_value**(self, key)

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

* (True, None).

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



.. _moobius.database.null_database.NullDatabase.set_value:

NullDatabase.set_value
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

* **NullDatabase.set_value**(self, key, value)

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

* (True, '').

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



.. _moobius.database.null_database.NullDatabase.delete_key:

NullDatabase.delete_key
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

* **NullDatabase.delete_key**(self, key)

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

* (True, '').

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



.. _moobius.database.null_database.NullDatabase.all_keys:

NullDatabase.all_keys
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

* **NullDatabase.all_keys**(self)

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

* The [].

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

NullDatabase.DatabaseInterface 

**********************
Internals
**********************
.. toctree::
   :maxdepth: 2

   moobius.database.null_database_internal_attrs <moobius.database.null_database_internal_attrs>
