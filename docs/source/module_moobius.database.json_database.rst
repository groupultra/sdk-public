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
    <style>
        .style521 {
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
    <p class="style521">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **JSONDatabase.get_value**(self, key)

.. raw:: html

  <embed>
  <head>
    <style>
        .style522 {
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
    <p class="style522">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* **key:** String-valued key.

.. raw:: html

  <embed>
  <head>
    <style>
        .style523 {
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
    <p class="style523">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* The is_sucessful, the_value.

.. raw:: html

  <embed>
  <head>
    <style>
        .style524 {
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
    <p class="style524">
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
    <style>
        .style525 {
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
    <p class="style525">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **JSONDatabase.set_value**(self, key, value)

.. raw:: html

  <embed>
  <head>
    <style>
        .style526 {
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
    <p class="style526">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* **key:** String-valued key.

* **value:** A dict-valued value.

.. raw:: html

  <embed>
  <head>
    <style>
        .style527 {
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
    <p class="style527">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* (is_success, the key).
Note: This function should not be called directly.

.. raw:: html

  <embed>
  <head>
    <style>
        .style528 {
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
    <p class="style528">
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
    <style>
        .style529 {
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
    <p class="style529">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **JSONDatabase.delete_key**(self, key)

.. raw:: html

  <embed>
  <head>
    <style>
        .style530 {
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
    <p class="style530">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* **key:** Key.

.. raw:: html

  <embed>
  <head>
    <style>
        .style531 {
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
    <p class="style531">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* (True, the key)
Note: This function should not be called directly.

.. raw:: html

  <embed>
  <head>
    <style>
        .style532 {
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
    <p class="style532">
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
    <style>
        .style533 {
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
    <p class="style533">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **JSONDatabase.all_keys**(self)

.. raw:: html

  <embed>
  <head>
    <style>
        .style534 {
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
    <p class="style534">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* **(this class constructor accepts no arguments):**

.. raw:: html

  <embed>
  <head>
    <style>
        .style535 {
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
    <p class="style535">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* The dicts as an iterable which internally uses yield().

.. raw:: html

  <embed>
  <head>
    <style>
        .style536 {
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
    <p class="style536">
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
