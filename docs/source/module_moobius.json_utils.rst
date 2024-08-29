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
    <style>
        .style0 {
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
    <p class="style0">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **marked_recursive_dataclass**(data)

.. raw:: html

  <embed>
  <head>
    <style>
        .style1 {
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
    <p class="style1">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* **data:** Data.

.. raw:: html

  <embed>
  <head>
    <style>
        .style2 {
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
    <p class="style2">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* The dataclassed data. Used for JSON loading.
Used by json_utils.enhanced_json_load.

.. raw:: html

  <embed>
  <head>
    <style>
        .style3 {
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
    <p class="style3">
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
    <style>
        .style4 {
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
    <p class="style4">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **marked_recursive_undataclass**(data, typemark_dataclasses)

.. raw:: html

  <embed>
  <head>
    <style>
        .style5 {
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
    <p class="style5">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* **data:** Dataclassed data.

* **typemark_dataclasses:** Whether to mark dataclasses in a special way so they are known as such.

.. raw:: html

  <embed>
  <head>
    <style>
        .style6 {
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
    <p class="style6">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* The non-dataclassed data.
Used by json_utils.enhanced_json_save.

.. raw:: html

  <embed>
  <head>
    <style>
        .style7 {
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
    <p class="style7">
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
    <style>
        .style8 {
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
    <p class="style8">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **enhanced_json_load**(filename)

.. raw:: html

  <embed>
  <head>
    <style>
        .style9 {
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
    <p class="style9">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* **filename:** Filename or bytes.

.. raw:: html

  <embed>
  <head>
    <style>
        .style10 {
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
    <p class="style10">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* The possibly-nested datastructure which may have Dataclasses.

.. raw:: html

  <embed>
  <head>
    <style>
        .style11 {
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
    <p class="style11">
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
    <style>
        .style12 {
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
    <p class="style12">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **enhanced_json_save**(filename, data, typemark_dataclasses, indent)

.. raw:: html

  <embed>
  <head>
    <style>
        .style13 {
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
    <p class="style13">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* **filename:** The filename or file object to save to. None if not saving to any file.

* **data:** What needs to be saved. Can be a nested datastructure even with embedded dataclasses.

* **typemark_dataclasses=True:** Save dataclasses as special dicts so that on enhanced_json_load load they are converted back into dataclasses.

* **indent=2:** The indent to display the text at.

.. raw:: html

  <embed>
  <head>
    <style>
        .style14 {
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
    <p class="style14">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* The data as a JSON string.

.. raw:: html

  <embed>
  <head>
    <style>
        .style15 {
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
    <p class="style15">
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
    <style>
        .style16 {
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
    <p class="style16">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **recursive_json_load**(x)

.. raw:: html

  <embed>
  <head>
    <style>
        .style17 {
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
    <p class="style17">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* **x:** Generic input x.

.. raw:: html

  <embed>
  <head>
    <style>
        .style18 {
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
    <p class="style18">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* The modified input.

.. raw:: html

  <embed>
  <head>
    <style>
        .style19 {
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
    <p class="style19">
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
    <style>
        .style20 {
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
    <p class="style20">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **update_jsonfile**(fname, key_path, value)

.. raw:: html

  <embed>
  <head>
    <style>
        .style21 {
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
    <p class="style21">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* **fname:** The json file.

* **key_path:** The path within the datastructure.

* **value:** The new value.

.. raw:: html

  <embed>
  <head>
    <style>
        .style22 {
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
    <p class="style22">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* None.

.. raw:: html

  <embed>
  <head>
    <style>
        .style23 {
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
    <p class="style23">
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
    <style>
        .style24 {
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
    <p class="style24">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **get_config**(config, account_config, service_config, db_config, log_config)

.. raw:: html

  <embed>
  <head>
    <style>
        .style25 {
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
    <p class="style25">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* **config=None:** The entire config, a string (JSON filepath) or dict.

* **account_config=None:** The account-sepcific config with secrets, a string (JSON filepath) or dict.

* **service_config=None:** Service-specific config (the urls, the service id, and the channels).

* **db_config=None:** Config specific to the Moobius db engine. A list of attributes. This feature is an independent feature to the Platform.

* **log_config=None:** Config specific to logging. This feature is an independent feature to the Platform.

.. raw:: html

  <embed>
  <head>
    <style>
        .style26 {
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
    <p class="style26">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* The config as a dict.
  Where to save the new service id as [json filename, datastructure_path], if there is a JSON file to save to.

.. raw:: html

  <embed>
  <head>
    <style>
        .style27 {
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
    <p class="style27">
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
