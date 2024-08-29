.. _moobius_database_redis_database:

###################################################################################
moobius.database.redis_database
###################################################################################

******************************
Module-level functions
******************************

(No module-level functions)

************************************
Class RedisDatabase
************************************

The redis database make use of a redis.Redis(...) server (Redis servers are set to localhost:6379 by default).
By default uses the domains's hash code to differentiate different domains, unless a user-supplied "db" value is given.

.. _moobius.database.redis_database.RedisDatabase.get_value:

RedisDatabase.get_value
---------------------------------------------------------------------------------------------------------------------



.. raw:: html

  <embed>
  <head>
    <style>
        .style569 {
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
    <p class="style569">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **RedisDatabase.get_value**(self, key)

.. raw:: html

  <embed>
  <head>
    <style>
        .style570 {
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
    <p class="style570">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* **key:** Key.

.. raw:: html

  <embed>
  <head>
    <style>
        .style571 {
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
    <p class="style571">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* (sucess, the value).

.. raw:: html

  <embed>
  <head>
    <style>
        .style572 {
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
    <p class="style572">
          <b>Raises:</b>
    </p>
  </body>
  </embed>

* (this function does not raise any notable errors)



.. _moobius.database.redis_database.RedisDatabase.set_value:

RedisDatabase.set_value
---------------------------------------------------------------------------------------------------------------------



.. raw:: html

  <embed>
  <head>
    <style>
        .style573 {
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
    <p class="style573">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **RedisDatabase.set_value**(self, key, value)

.. raw:: html

  <embed>
  <head>
    <style>
        .style574 {
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
    <p class="style574">
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
        .style575 {
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
    <p class="style575">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* (sucess, the key).

.. raw:: html

  <embed>
  <head>
    <style>
        .style576 {
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
    <p class="style576">
          <b>Raises:</b>
    </p>
  </body>
  </embed>

* (this function does not raise any notable errors)



.. _moobius.database.redis_database.RedisDatabase.delete_key:

RedisDatabase.delete_key
---------------------------------------------------------------------------------------------------------------------



.. raw:: html

  <embed>
  <head>
    <style>
        .style577 {
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
    <p class="style577">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **RedisDatabase.delete_key**(self, key)

.. raw:: html

  <embed>
  <head>
    <style>
        .style578 {
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
    <p class="style578">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* **key:** Key.

.. raw:: html

  <embed>
  <head>
    <style>
        .style579 {
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
    <p class="style579">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* (True, the key).

.. raw:: html

  <embed>
  <head>
    <style>
        .style580 {
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
    <p class="style580">
          <b>Raises:</b>
    </p>
  </body>
  </embed>

* (this function does not raise any notable errors)



.. _moobius.database.redis_database.RedisDatabase.all_keys:

RedisDatabase.all_keys
---------------------------------------------------------------------------------------------------------------------



.. raw:: html

  <embed>
  <head>
    <style>
        .style581 {
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
    <p class="style581">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **RedisDatabase.all_keys**(self)

.. raw:: html

  <embed>
  <head>
    <style>
        .style582 {
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
    <p class="style582">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* **(this class constructor accepts no arguments):**

.. raw:: html

  <embed>
  <head>
    <style>
        .style583 {
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
    <p class="style583">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* The list of keys.

.. raw:: html

  <embed>
  <head>
    <style>
        .style584 {
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
    <p class="style584">
          <b>Raises:</b>
    </p>
  </body>
  </embed>

* (this function does not raise any notable errors)



Class attributes
--------------------

RedisDatabase.DatabaseInterface 

**********************
Internals
**********************
.. toctree::
   :maxdepth: 2

   moobius.database.redis_database_internal_attrs <moobius.database.redis_database_internal_attrs>
