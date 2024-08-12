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
open_folder_in_explorer(folder_path)

Lets the user select a folder. This is used for gui-mode only.
  Parameters:
    folder_path: The default folder to pick.
  Returns:
    The None.
  Raises:
    (this function does not raise any notable errors)

.. _moobius.quickstart.download_text_file_to_string:

download_text_file_to_string
---------------------------------------------------------------------------------------------------------------------
download_text_file_to_string(url)

A simple download, used to get CCS code from GitHub.
  Parameters:
    url: The URL.
  Returns:
    The text. Raises network exceptions if the request fails.
  Raises:
    (this function does not raise any notable errors)

.. _moobius.quickstart.create_channel:

create_channel
---------------------------------------------------------------------------------------------------------------------
create_channel(email, password, url)

Creates a channel.
  Parameters:
    email: The email.
    password: The password.
    url: The url.
  Returns:
    The service_id, channel_id. Used if no channel is specified.
  Raises:
    (this function does not raise any notable errors)

.. _moobius.quickstart.save:

save
---------------------------------------------------------------------------------------------------------------------
save(fname, x)

Saves a file. Makes dirs if need be.
  Parameters:
    fname: The filename.
    x: The  string.
  Returns:
    The None.
  Raises:
    (this function does not raise any notable errors)

.. _moobius.quickstart._get_boxes:

_get_boxes
---------------------------------------------------------------------------------------------------------------------
_get_boxes()

Gets the value in each GUI box.
  Parameters:
    (this function accepts no arguments)
  Returns:
    The  empty dict if it is not the GUI mode.
  Raises:
    (this function does not raise any notable errors)

.. _moobius.quickstart.submit:

submit
---------------------------------------------------------------------------------------------------------------------
submit(out)

Saves the CCS files (code and config) to a folder.
  Parameters:
    out: The configuration dict with all the settings.
  Returns:
    The sys.exit().
    Calling this function will read the current gui state.
  Raises:
    (this function does not raise any notable errors)

.. _moobius.quickstart.make_box:

make_box
---------------------------------------------------------------------------------------------------------------------
make_box(root, name, detailed_name, default, options)

Makes a box for GUI usage. None options means fill in.
  Parameters:
    root: The Tk.root.
    name: The box name.
    detailed_name: The More details.
    default: The GUI default.
    options=None: The options to pick, for boxes with options.
  Returns:
    The ttk.Combobox object.
  Raises:
    (this function does not raise any notable errors)

.. _moobius.quickstart.save_starter_ccs:

save_starter_ccs
---------------------------------------------------------------------------------------------------------------------
save_starter_ccs()

Reads sys.argv, as well as gui interaction if specified.
Uses this information to construct a CCS app and saves to the folder that was specified.
This function is called, from the __init__.py in src/moobius, when "python -m moobius" is
typed into the command line.
  Parameters:
    (this function accepts no arguments)
  Returns:
    The None.
  Raises:
    (this function does not raise any notable errors)


