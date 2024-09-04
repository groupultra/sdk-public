.. _moobius_database_json_database:

###################################################################################
moobius.database.json_database
###################################################################################

******************************
Module-level functions
******************************

(No module-level functions)

************************************
Class JSONDatabase
************************************

JSONDatabase simply stores information as JSON strings in a list of files.
Each domain, key combination is stored as one file.
Dataclass objects can be seralized as well.

.. _moobius.database.json_database.JSONDatabase.get_value:

JSONDatabase.get_value
---------------------------------------------------------------------------------------------------------------------



Gets the value (which is a dict).
Note: This "key" is different from a key to look up a CachedDict file.
Note: This function should not be called directly.

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

* **JSONDatabase.get_value**(self, key)

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

* __key:__ String-valued key.

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

* The is_sucessful, the_value.

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

* TypeError: If the type of the value is unknown, so we can't construct the object.



.. _moobius.database.json_database.JSONDatabase.set_value:

JSONDatabase.set_value
---------------------------------------------------------------------------------------------------------------------



Updates and saves a cached dict,.

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

* **JSONDatabase.set_value**(self, key, value)

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

* __key:__ String-valued key.

* __value:__ A dict-valued value.

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

* (is_success, the key).
Note: This function should not be called directly.

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



.. _moobius.database.json_database.JSONDatabase.delete_key:

JSONDatabase.delete_key
---------------------------------------------------------------------------------------------------------------------



Deletes a cached dict.

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

* **JSONDatabase.delete_key**(self, key)

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

* (True, the key)
Note: This function should not be called directly.

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



.. _moobius.database.json_database.JSONDatabase.all_keys:

JSONDatabase.all_keys
---------------------------------------------------------------------------------------------------------------------



Gets all the cached dicts in the database.

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

* **JSONDatabase.all_keys**(self)

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

* The dicts as an iterable which internally uses yield().

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

JSONDatabase.DatabaseInterface 

**********************
Internals
**********************
.. toctree::
   :maxdepth: 2

   moobius.database.json_database_internal_attrs <moobius.database.json_database_internal_attrs>
