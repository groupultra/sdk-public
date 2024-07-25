.. _moobius_quickstart:

moobius.quickstart
===================================

Module-level functions
===================

.. _moobius.quickstart.open_folder_in_explorer:
open_folder_in_explorer
-----------------------------------
open_folder_in_explorer(folder_path)

Lets the user select a folder. This is used for gui-mode only.

.. _moobius.quickstart.download_text_file_to_string:
download_text_file_to_string
-----------------------------------
download_text_file_to_string(url)

A simple download, used to get CCS code from GitHub.

.. _moobius.quickstart.create_channel:
create_channel
-----------------------------------
create_channel(email, password, url)

Creates a channel and returns the service_id, channel_id. Used if no channel is specified.

.. _moobius.quickstart.save:
save
-----------------------------------
save(fname, x)

Saves a file to a string, making dirs if need be.

.. _moobius.quickstart._get_boxes:
_get_boxes
-----------------------------------
_get_boxes()

Empty dict if there are no boxes choosen.

.. _moobius.quickstart.submit:
submit
-----------------------------------
submit(out)

Given a configuration dict with all the settings, saves the CCS files (code and config) to a folder.

.. _moobius.quickstart.make_box:
make_box
-----------------------------------
make_box(root, name, detailed_name, default, options)

Makes a box for GUI usage. None options means fill in.

.. _moobius.quickstart.save_starter_ccs:
save_starter_ccs
-----------------------------------
save_starter_ccs()

Reads sys.argv, as well as gui interaction if specified.
Uses this information to construct a CCS app and saves to the folder that was specified.
This function is called, from the __init__.py in src/moobius, when "python -m moobius" is
typed into the command line.

.. _moobius.quickstart.save_starter_ccs._folder_button_callback:
save_starter_ccs._folder_button_callback
-----------------------------------
save_starter_ccs._folder_button_callback(\*kwargs)

<No doc string>

===================


