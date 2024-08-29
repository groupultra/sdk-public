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
    <style>
        .style545 {
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
    <p class="style545">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **NullDatabase.get_value**(self, key)

.. raw:: html

  <embed>
  <head>
    <style>
        .style546 {
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
    <p class="style546">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* **key:** Key.

.. raw:: html

  <embed>
  <head>
    <style>
        .style547 {
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
    <p class="style547">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* (True, None).

.. raw:: html

  <embed>
  <head>
    <style>
        .style548 {
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
    <p class="style548">
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
    <style>
        .style549 {
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
    <p class="style549">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **NullDatabase.set_value**(self, key, value)

.. raw:: html

  <embed>
  <head>
    <style>
        .style550 {
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
    <p class="style550">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* **key:** Key.

* **value:** Value.

.. raw:: html

  <embed>
  <head>
    <style>
        .style551 {
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
    <p class="style551">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* (True, '').

.. raw:: html

  <embed>
  <head>
    <style>
        .style552 {
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
    <p class="style552">
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
    <style>
        .style553 {
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
    <p class="style553">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **NullDatabase.delete_key**(self, key)

.. raw:: html

  <embed>
  <head>
    <style>
        .style554 {
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
    <p class="style554">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* **key:** Key.

.. raw:: html

  <embed>
  <head>
    <style>
        .style555 {
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
    <p class="style555">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* (True, '').

.. raw:: html

  <embed>
  <head>
    <style>
        .style556 {
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
    <p class="style556">
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
    <style>
        .style557 {
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
    <p class="style557">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **NullDatabase.all_keys**(self)

.. raw:: html

  <embed>
  <head>
    <style>
        .style558 {
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
    <p class="style558">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* **(this class constructor accepts no arguments):**

.. raw:: html

  <embed>
  <head>
    <style>
        .style559 {
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
    <p class="style559">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* The [].

.. raw:: html

  <embed>
  <head>
    <style>
        .style560 {
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
    <p class="style560">
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
