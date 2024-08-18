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

.. _moobius.quickstart._get_boxes:

_get_boxes
---------------------------------------------------------------------------------------------------------------------

Gets the value in each GUI box.

* Signature

    * _get_boxes()

* Parameters

    * (this function accepts no arguments)

* Returns

  * The  empty dict if it is not the GUI mode.

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


