.. _moobius_database_storage:

###################################################################################
moobius.database.storage
###################################################################################

******************************
Module-level functions
******************************

.. _moobius.database.storage.get_engine:

get_engine
---------------------------------------------------------------------------------------------------------------------



.. raw:: html

  <embed>
  <head>
    <style>
        .style593 {
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
    <p class="style593">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **get_engine**(implementation)

.. raw:: html

  <embed>
  <head>
    <style>
        .style594 {
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
    <p class="style594">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* **implementation:** N implementation string.

.. raw:: html

  <embed>
  <head>
    <style>
        .style595 {
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
    <p class="style595">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* The engine's Class. 
Last-minute-imports the module so that no pip package is needed for unused engines.

.. raw:: html

  <embed>
  <head>
    <style>
        .style596 {
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
    <p class="style596">
          <b>Raises:</b>
    </p>
  </body>
  </embed>

* (this function does not raise any notable errors)



************************************
Class CachedDict
************************************

CachedDict is a custom dictionary-like class that inherits from the built-in dict class.
The MagicalStorage class manages the creation of CachedDict instances with different attribute names, allowing users to cache and retrieve data in a structured way, with optional database interaction.

.. _moobius.database.storage.CachedDict.load:

CachedDict.load
---------------------------------------------------------------------------------------------------------------------



Loads all keys from the database to the cache.

.. raw:: html

  <embed>
  <head>
    <style>
        .style597 {
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
    <p class="style597">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **CachedDict.load**(self)

.. raw:: html

  <embed>
  <head>
    <style>
        .style598 {
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
    <p class="style598">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* **(this class constructor accepts no arguments):**

.. raw:: html

  <embed>
  <head>
    <style>
        .style599 {
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
    <p class="style599">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* None.

.. raw:: html

  <embed>
  <head>
    <style>
        .style600 {
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
    <p class="style600">
          <b>Raises:</b>
    </p>
  </body>
  </embed>

* (this function does not raise any notable errors)



.. _moobius.database.storage.CachedDict.save:

CachedDict.save
---------------------------------------------------------------------------------------------------------------------



Saves a key to the database.. 
For a JSONDatabase, this will create a new json file named after the database's domain and key.

.. raw:: html

  <embed>
  <head>
    <style>
        .style601 {
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
    <p class="style601">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **CachedDict.save**(self, key)

.. raw:: html

  <embed>
  <head>
    <style>
        .style602 {
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
    <p class="style602">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* **key:** String-valued key.

.. raw:: html

  <embed>
  <head>
    <style>
        .style603 {
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
    <p class="style603">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* None.

.. raw:: html

  <embed>
  <head>
    <style>
        .style604 {
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
    <p class="style604">
          <b>Raises:</b>
    </p>
  </body>
  </embed>

* (this function does not raise any notable errors)



.. _moobius.database.storage.CachedDict.pop:

CachedDict.pop
---------------------------------------------------------------------------------------------------------------------



Overrides "v = d.pop(k)" to get and delete k from the database..

.. raw:: html

  <embed>
  <head>
    <style>
        .style605 {
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
    <p class="style605">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **CachedDict.pop**(self, key, default)

.. raw:: html

  <embed>
  <head>
    <style>
        .style606 {
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
    <p class="style606">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* **key:** Key.

* **default='__unspecified__':** An optional default value.

.. raw:: html

  <embed>
  <head>
    <style>
        .style607 {
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
    <p class="style607">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* The value.

.. raw:: html

  <embed>
  <head>
    <style>
        .style608 {
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
    <p class="style608">
          <b>Raises:</b>
    </p>
  </body>
  </embed>

* (this function does not raise any notable errors)



.. _moobius.database.storage.CachedDict.clear:

CachedDict.clear
---------------------------------------------------------------------------------------------------------------------



Overrides "d.clear()" to clear the database.

.. raw:: html

  <embed>
  <head>
    <style>
        .style609 {
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
    <p class="style609">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **CachedDict.clear**(self)

.. raw:: html

  <embed>
  <head>
    <style>
        .style610 {
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
    <p class="style610">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* **(this class constructor accepts no arguments):**

.. raw:: html

  <embed>
  <head>
    <style>
        .style611 {
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
    <p class="style611">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* None.

.. raw:: html

  <embed>
  <head>
    <style>
        .style612 {
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
    <p class="style612">
          <b>Raises:</b>
    </p>
  </body>
  </embed>

* (this function does not raise any notable errors)



Class attributes
--------------------

CachedDict.dict 

************************************
Class MoobiusStorage
************************************

MoobiusStorage combines multiple databases together.
Each database becomes one attribute using dynamic attribute creation.

.. _moobius.database.storage.MoobiusStorage.put:

MoobiusStorage.put
---------------------------------------------------------------------------------------------------------------------



Sets self.attr_name to database (a DatabaseInterface object) for later retrieval. 
load (default True) to load the dict immediatly, clear (default False) to clear the dict and skip loading it.

.. raw:: html

  <embed>
  <head>
    <style>
        .style613 {
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
    <p class="style613">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **MoobiusStorage.put**(self, attr_name, database, load, clear)

.. raw:: html

  <embed>
  <head>
    <style>
        .style614 {
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
    <p class="style614">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* **attr_name:** The attr name to add dynamically to self, setting it to a CachedDict.

* **database:** The database.

* **load=True:** Whether to load the dict in full at startup instead of gradually.

* **clear=False:** Whether to clear the dict (which deletes the files).

.. raw:: html

  <embed>
  <head>
    <style>
        .style615 {
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
    <p class="style615">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* None.

.. raw:: html

  <embed>
  <head>
    <style>
        .style616 {
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
    <p class="style616">
          <b>Raises:</b>
    </p>
  </body>
  </embed>

* (this function does not raise any notable errors)



.. _moobius.database.storage.MoobiusStorage.add_container:

MoobiusStorage.add_container
---------------------------------------------------------------------------------------------------------------------



Adds a database using the config dict.

.. raw:: html

  <embed>
  <head>
    <style>
        .style617 {
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
    <p class="style617">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **MoobiusStorage.add_container**(self, implementation, settings, name, load, clear)

.. raw:: html

  <embed>
  <head>
    <style>
        .style618 {
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
    <p class="style618">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* **implementation:** The engine of the database.

* **settings:** Contains "root_dir" of the json files, for example.

* **name:** The attribute that will be added to self for later use.

* **load=True:** Whether to load the database when initializing the database.

* **clear=False:** Whether to clear the database when initializing the database.

.. raw:: html

  <embed>
  <head>
    <style>
        .style619 {
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
    <p class="style619">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* None.

.. raw:: html

  <embed>
  <head>
    <style>
        .style620 {
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
    <p class="style620">
          <b>Raises:</b>
    </p>
  </body>
  </embed>

* (this function does not raise any notable errors)


.. raw:: html

  <embed>
  <head>
    <style>
        .style621 {
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
    <p class="style621">
          <b>Example:</b>
    </p>
  </body>
  </embed>

    Note: This is a hidden function, you don't need to call it directly.
      >>> storage = MoobiusStorage(service_id='1', channel_id='1')
      >>> storage.add_container(implementation='json', settings={'root_dir': 'data'}, name='character', load=True, clear=False)



Class attributes
--------------------



**********************
Internals
**********************
.. toctree::
   :maxdepth: 2

   moobius.database.storage_internal_attrs <moobius.database.storage_internal_attrs>
