.. _moobius_quickstart:

###################################################################################
moobius.quickstart
###################################################################################

******************************
Module-level functions
******************************

.. _moobius.quickstart.open_folder_in_explorer:

open_folder_in_explorer
---------------------------------------------------------------------------------------------------------------------



Lets the user select a folder. This is used for gui-mode only.

.. raw:: html

  <embed>
  <head>
    <style>
        .style28 {
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
    <p class="style28">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **open_folder_in_explorer**(folder_path)

.. raw:: html

  <embed>
  <head>
    <style>
        .style29 {
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
    <p class="style29">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* **folder_path:** Default folder to pick.

.. raw:: html

  <embed>
  <head>
    <style>
        .style30 {
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
    <p class="style30">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* None.

.. raw:: html

  <embed>
  <head>
    <style>
        .style31 {
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
    <p class="style31">
          <b>Raises:</b>
    </p>
  </body>
  </embed>

* (this function does not raise any notable errors)



.. _moobius.quickstart.download_text_file_to_string:

download_text_file_to_string
---------------------------------------------------------------------------------------------------------------------



A simple download, used to get CCS code from GitHub.

.. raw:: html

  <embed>
  <head>
    <style>
        .style32 {
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
    <p class="style32">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **download_text_file_to_string**(url)

.. raw:: html

  <embed>
  <head>
    <style>
        .style33 {
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
    <p class="style33">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* **url:** URL.

.. raw:: html

  <embed>
  <head>
    <style>
        .style34 {
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
    <p class="style34">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* The text. Raises network exceptions if the request fails.

.. raw:: html

  <embed>
  <head>
    <style>
        .style35 {
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
    <p class="style35">
          <b>Raises:</b>
    </p>
  </body>
  </embed>

* (this function does not raise any notable errors)



.. _moobius.quickstart.create_channel:

create_channel
---------------------------------------------------------------------------------------------------------------------



Creates a channel.

.. raw:: html

  <embed>
  <head>
    <style>
        .style36 {
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
    <p class="style36">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **create_channel**(email, password, url)

.. raw:: html

  <embed>
  <head>
    <style>
        .style37 {
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
    <p class="style37">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* **email:** Email.

* **password:** Password.

* **url:** Url.

.. raw:: html

  <embed>
  <head>
    <style>
        .style38 {
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
    <p class="style38">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* The service_id, channel_id. Used if no channel is specified.

.. raw:: html

  <embed>
  <head>
    <style>
        .style39 {
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
    <p class="style39">
          <b>Raises:</b>
    </p>
  </body>
  </embed>

* (this function does not raise any notable errors)



.. _moobius.quickstart.save:

save
---------------------------------------------------------------------------------------------------------------------



Saves a file. Makes dirs if need be.

.. raw:: html

  <embed>
  <head>
    <style>
        .style40 {
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
    <p class="style40">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **save**(fname, x)

.. raw:: html

  <embed>
  <head>
    <style>
        .style41 {
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
    <p class="style41">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* **fname:** Filename.

* **x:** A string.

.. raw:: html

  <embed>
  <head>
    <style>
        .style42 {
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
    <p class="style42">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* None.

.. raw:: html

  <embed>
  <head>
    <style>
        .style43 {
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
    <p class="style43">
          <b>Raises:</b>
    </p>
  </body>
  </embed>

* (this function does not raise any notable errors)



.. _moobius.quickstart.submit:

submit
---------------------------------------------------------------------------------------------------------------------



Saves the CCS files (code and config) to a folder.

.. raw:: html

  <embed>
  <head>
    <style>
        .style44 {
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
    <p class="style44">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **submit**(out)

.. raw:: html

  <embed>
  <head>
    <style>
        .style45 {
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
    <p class="style45">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* **out:** Configuration dict with all the settings.

.. raw:: html

  <embed>
  <head>
    <style>
        .style46 {
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
    <p class="style46">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* The sys.exit().
Calling this function will read the current gui state.

.. raw:: html

  <embed>
  <head>
    <style>
        .style47 {
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
    <p class="style47">
          <b>Raises:</b>
    </p>
  </body>
  </embed>

* (this function does not raise any notable errors)



.. _moobius.quickstart.make_box:

make_box
---------------------------------------------------------------------------------------------------------------------



Makes a box for GUI usage. None options means fill in.

.. raw:: html

  <embed>
  <head>
    <style>
        .style48 {
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
    <p class="style48">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **make_box**(root, name, detailed_name, default, options)

.. raw:: html

  <embed>
  <head>
    <style>
        .style49 {
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
    <p class="style49">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* **root:** Tk.root.

* **name:** The box name.

* **detailed_name:** More details.

* **default:** The GUI default.

* **options=None:** The options to pick, for boxes with options.

.. raw:: html

  <embed>
  <head>
    <style>
        .style50 {
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
    <p class="style50">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* The ttk.Combobox object.

.. raw:: html

  <embed>
  <head>
    <style>
        .style51 {
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
    <p class="style51">
          <b>Raises:</b>
    </p>
  </body>
  </embed>

* (this function does not raise any notable errors)



.. _moobius.quickstart.save_starter_ccs:

save_starter_ccs
---------------------------------------------------------------------------------------------------------------------



Reads sys.argv, as well as gui interaction if specified.
Uses this information to construct a CCS app and saves to the folder that was specified.
This function is called, from the __init__.py in src/moobius, when "python -m moobius" is
typed into the command line.

.. raw:: html

  <embed>
  <head>
    <style>
        .style52 {
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
    <p class="style52">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **save_starter_ccs**()

.. raw:: html

  <embed>
  <head>
    <style>
        .style53 {
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
    <p class="style53">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* **(this function accepts no arguments):**

.. raw:: html

  <embed>
  <head>
    <style>
        .style54 {
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
    <p class="style54">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* None.

.. raw:: html

  <embed>
  <head>
    <style>
        .style55 {
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
    <p class="style55">
          <b>Raises:</b>
    </p>
  </body>
  </embed>

* (this function does not raise any notable errors)



.. _moobius.quickstart.maybe_make_template_files:

maybe_make_template_files
---------------------------------------------------------------------------------------------------------------------



Makes template files if there is a need to do so, based on args and sys.argv.
Called by wand.run() before initializing the Moobius class if it doesn't have any templates.

Which files are created:
  A service.py file that runs everything.
  A sample config.py:
    Only created if "config_path" is in args (or system args) AND the file does not exist.
    This requires user information:
      email: If no system arg "email my@email.com" or "username my@email.com" is specified, prompts for one with input().
      password: If no system arg "password my_sec**t_pword", prompts for one.
      channels: If no system arg "channels abc... def..." to specify one or more channels, prompts for one or more.
    Note: if the user gives an empty response to input(), a nonfunctional default is used, which can be filled in later.

Unittests to run in a python prompt in an empty folder:
  >>> # Prompt the user for credentials and put these in the service.json (NOTE: will generate an error b/c None class):
  >>> import sys; from moobius import MoobiusWand; MoobiusWand().run(None, config_path="config/service.json")
  >>> # Provide credentials, making a service.json with no user input (NOTE: will generate an error b/c None class):
  >>> import sys; sys.argv = '_ email abc@123.com password IAmSecret channels abc-123 def-4561111111111111111111'.split(' '); from moobius import MoobiusWand; MoobiusWand().run(0, config_path="config/service.json")
  >>> # Provide agent credentials. There is no need to provide a channel id (NOTE: will generate an error b/c None class).
  >>> import sys; sys.argv = '_ email abc@123.com password IAmSecret'.split(' '); from moobius import MoobiusWand; MoobiusWand().run(0, config_path="config/agent.json", is_agent=True).

.. raw:: html

  <embed>
  <head>
    <style>
        .style56 {
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
    <p class="style56">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **maybe_make_template_files**(args)

.. raw:: html

  <embed>
  <head>
    <style>
        .style57 {
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
    <p class="style57">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* **args:** The list of args.

.. raw:: html

  <embed>
  <head>
    <style>
        .style58 {
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
    <p class="style58">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* None.

.. raw:: html

  <embed>
  <head>
    <style>
        .style59 {
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
    <p class="style59">
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

   moobius.quickstart_internal_attrs <moobius.quickstart_internal_attrs>
