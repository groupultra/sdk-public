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

* Signature

    * open_folder_in_explorer(folder_path)

* Parameters

    * folder_path: Default folder to pick.

* Returns

  * The None.

* Raises

  * (this function does not raise any notable errors)

.. _moobius.quickstart.download_text_file_to_string:

download_text_file_to_string
---------------------------------------------------------------------------------------------------------------------

A simple download, used to get CCS code from GitHub.

* Signature

    * download_text_file_to_string(url)

* Parameters

    * url: URL.

* Returns

  * The text. Raises network exceptions if the request fails.

* Raises

  * (this function does not raise any notable errors)

.. _moobius.quickstart.create_channel:

create_channel
---------------------------------------------------------------------------------------------------------------------

Creates a channel.

* Signature

    * create_channel(email, password, url)

* Parameters

    * email: Email.
    
    * password: Password.
    
    * url: Url.

* Returns

  * The service_id, channel_id. Used if no channel is specified.

* Raises

  * (this function does not raise any notable errors)

.. _moobius.quickstart.save:

save
---------------------------------------------------------------------------------------------------------------------

Saves a file. Makes dirs if need be.

* Signature

    * save(fname, x)

* Parameters

    * fname: Filename.
    
    * x: A string.

* Returns

  * The None.

* Raises

  * (this function does not raise any notable errors)

.. _moobius.quickstart.submit:

submit
---------------------------------------------------------------------------------------------------------------------

Saves the CCS files (code and config) to a folder.

* Signature

    * submit(out)

* Parameters

    * out: Configuration dict with all the settings.

* Returns

  * The sys.exit().
  Calling this function will read the current gui state.

* Raises

  * (this function does not raise any notable errors)

.. _moobius.quickstart.make_box:

make_box
---------------------------------------------------------------------------------------------------------------------

Makes a box for GUI usage. None options means fill in.

* Signature

    * make_box(root, name, detailed_name, default, options)

* Parameters

    * root: Tk.root.
    
    * name: The box name.
    
    * detailed_name: More details.
    
    * default: The GUI default.
    
    * options=None: The options to pick, for boxes with options.

* Returns

  * The ttk.Combobox object.

* Raises

  * (this function does not raise any notable errors)

.. _moobius.quickstart.save_starter_ccs:

save_starter_ccs
---------------------------------------------------------------------------------------------------------------------

Reads sys.argv, as well as gui interaction if specified.
Uses this information to construct a CCS app and saves to the folder that was specified.
This function is called, from the __init__.py in src/moobius, when "python -m moobius" is
typed into the command line.

* Signature

    * save_starter_ccs()

* Parameters

    * (this function accepts no arguments)

* Returns

  * The None.

* Raises

  * (this function does not raise any notable errors)

.. _moobius.quickstart.maybe_make_template_files:

maybe_make_template_files
---------------------------------------------------------------------------------------------------------------------

Makes template files if there is a need to do so, based on args and sys.argv.
Called by wand.run() before initializing the Moobius class if it doesn't have any templates.

Which files are created:
  A template main.py python file which calls Wand.run:
    Only created if the file does not exist AND "make_main main.py" (or "make_main foo.py", etc) is in the system args.
  A sample config.py:
    Only created if "config_path" is in args (or system args) AND the file does not exist.
    This requires user information:
      email: If no system arg "email my@email.com" or "username my@email.com" is specified, prompts for one with input().
      password: If no system arg "password my_sec**t_pword", prompts for one.
      channels: If no system arg "channels abc... def..." to specify one or more channels, prompts for one or more.
    Note: if the user gives an empty response to input(), a nonfunctional default is used, which can be filled in later.

Unittests to run in a python prompt in an empty folder:
  >>> # Make a main.py file:
  >>> import sys; sys.argv = '_ make_main main.py'.split(' '); import moobius;
  >>> # Prompt the user for credentials and put these in the service.json (NOTE: will generate an error b/c None class):
  >>> import sys; from moobius import MoobiusWand; MoobiusWand().run(None, config_path="config/service.json")
  >>> # Provide credentials, making a service.json with no user input (NOTE: will generate an error b/c None class):
  >>> import sys; sys.argv = '_ email abc@123.com password IAmSecret channels abc-123 def-4561111111111111111111'.split(' '); from moobius import MoobiusWand; MoobiusWand().run(0, config_path="config/service.json")
  >>> # Provide agent credentials. There is no need to provide a channel id (NOTE: will generate an error b/c None class).
  >>> import sys; sys.argv = '_ email abc@123.com password IAmSecret'.split(' '); from moobius import MoobiusWand; MoobiusWand().run(0, config_path="config/agent.json", is_agent=True).

* Signature

    * maybe_make_template_files(args)

* Parameters

    * args: The list of args.

* Returns

  * The None.

* Raises

  * (this function does not raise any notable errors)



**********************
Internals
**********************
.. toctree::
   :maxdepth: 2

   moobius.quickstart_internal_attrs <moobius.quickstart_internal_attrs>
