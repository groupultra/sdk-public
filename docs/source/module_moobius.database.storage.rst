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
  </head>
  <body>
    <p class="fsig">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **get_engine**(implementation)

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

* __implementation:__ N implementation string.

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

* The engine's Class. 
Last-minute-imports the module so that no pip package is needed for unused engines.

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
  </head>
  <body>
    <p class="fsig">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **CachedDict.load**(self)

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



.. _moobius.database.storage.CachedDict.save:

CachedDict.save
---------------------------------------------------------------------------------------------------------------------



Saves a key to the database.. 
For a JSONDatabase, this will create a new json file named after the database's domain and key.

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

* **CachedDict.save**(self, key)

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



.. _moobius.database.storage.CachedDict.pop:

CachedDict.pop
---------------------------------------------------------------------------------------------------------------------



Overrides "v = d.pop(k)" to get and delete k from the database..

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

* **CachedDict.pop**(self, key, default)

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

* __default='__unspecified__':__ An optional default value.

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

* The value.

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



.. _moobius.database.storage.CachedDict.clear:

CachedDict.clear
---------------------------------------------------------------------------------------------------------------------



Overrides "d.clear()" to clear the database.

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

* **CachedDict.clear**(self)

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
  </head>
  <body>
    <p class="fsig">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **MoobiusStorage.put**(self, attr_name, database, load, clear)

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

* __attr_name:__ The attr name to add dynamically to self, setting it to a CachedDict.

* __database:__ The database.

* __load=True:__ Whether to load the dict in full at startup instead of gradually.

* __clear=False:__ Whether to clear the dict (which deletes the files).

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



.. _moobius.database.storage.MoobiusStorage.add_container:

MoobiusStorage.add_container
---------------------------------------------------------------------------------------------------------------------



Adds a database using the config dict.

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

* **MoobiusStorage.add_container**(self, implementation, settings, name, load, clear)

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

* __implementation:__ The engine of the database.

* __settings:__ Contains "root_dir" of the json files, for example.

* __name:__ The attribute that will be added to self for later use.

* __load=True:__ Whether to load the database when initializing the database.

* __clear=False:__ Whether to clear the database when initializing the database.

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
