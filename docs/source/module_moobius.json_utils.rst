.. _moobius_json_utils:

###################################################################################
moobius.json_utils
###################################################################################

******************************
Module-level functions
******************************

.. _moobius.json_utils.marked_recursive_dataclass:

marked_recursive_dataclass
---------------------------------------------------------------------------------------------------------------------



Recursively converts nested lists, dicts, etc into dataclasses if they have been markd with types._DTYPE and types._DVAL.

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

* **marked_recursive_dataclass**(data)

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

* __data:__ Data.

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

* The dataclassed data. Used for JSON loading.
Used by json_utils.enhanced_json_load.

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



.. _moobius.json_utils.marked_recursive_undataclass:

marked_recursive_undataclass
---------------------------------------------------------------------------------------------------------------------



Converts data containing dataclasses back into pure dicts, making them with json_utils._DTYPE and json_utils._DVAL..

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

* **marked_recursive_undataclass**(data, typemark_dataclasses)

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

* __data:__ Dataclassed data.

* __typemark_dataclasses:__ Whether to mark dataclasses in a special way so they are known as such.

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

* The non-dataclassed data.
Used by json_utils.enhanced_json_save.

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



.. _moobius.json_utils.enhanced_json_load:

enhanced_json_load
---------------------------------------------------------------------------------------------------------------------



Loads JSON from the disk,.

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

* **enhanced_json_load**(filename)

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

* __filename:__ Filename or bytes.

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

* The possibly-nested datastructure which may have Dataclasses.

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



.. _moobius.json_utils.enhanced_json_save:

enhanced_json_save
---------------------------------------------------------------------------------------------------------------------



Saves the JSON to the disk and/or a string.

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

* **enhanced_json_save**(filename, data, typemark_dataclasses, indent)

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

* __filename:__ The filename or file object to save to. None if not saving to any file.

* __data:__ What needs to be saved. Can be a nested datastructure even with embedded dataclasses.

* __typemark_dataclasses=True:__ Save dataclasses as special dicts so that on enhanced_json_load load they are converted back into dataclasses.

* __indent=2:__ The indent to display the text at.

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

* The data as a JSON string.

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



.. _moobius.json_utils.recursive_json_load:

recursive_json_load
---------------------------------------------------------------------------------------------------------------------



Loads json files into dicts and lists, including dicts/lists of json filenames. Used for the app configuration.
Strings anywhere in x that have no newlines and end in .json or .JSON will be treated like filenames.
Does not use enhanced_json features..

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

* **recursive_json_load**(x)

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

* __x:__ Generic input x.

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

* The modified input.

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



.. _moobius.json_utils.update_jsonfile:

update_jsonfile
---------------------------------------------------------------------------------------------------------------------



Updates a json file. Uses enhanced_json_load (which makes dataclasses have metadata).

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

* **update_jsonfile**(fname, key_path, value)

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

* __fname:__ The json file.

* __key_path:__ The path within the datastructure.

* __value:__ The new value.

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



.. _moobius.json_utils.get_config:

get_config
---------------------------------------------------------------------------------------------------------------------



Calculates the configuration in various ways. Config files are automatically generated by quickstart.py which is invoked by running the command "moobius".
This may involve JSON file reading.

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

* **get_config**(config, account_config, service_config, db_config, log_config)

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

* __config=None:__ The entire config, a string (JSON filepath) or dict.

* __account_config=None:__ The account-sepcific config with secrets, a string (JSON filepath) or dict.

* __service_config=None:__ Service-specific config (the urls, the service id, and the channels).

* __db_config=None:__ Config specific to the Moobius db engine. A list of attributes. This feature is an independent feature to the Platform.

* __log_config=None:__ Config specific to logging. This feature is an independent feature to the Platform.

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

* The config as a dict.
  Where to save the new service id as [json filename, datastructure_path], if there is a JSON file to save to.

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





**********************
Internals
**********************
.. toctree::
   :maxdepth: 2

   moobius.json_utils_internal_attrs <moobius.json_utils_internal_attrs>
