.. _moobius_utils:

###################################################################################
moobius.utils
###################################################################################

******************************
Module-level functions
******************************

.. _moobius.utils._recursive_dataclass:

_recursive_dataclass
---------------------------------------------------------------------------------------------------------------------
_recursive_dataclass(data)


Recursively converts nested lists, dicts, etc into dataclasses..
  Parameters:
    data: Data.
  Returns:
    The dataclassed data.
  Raises:
    (this function does not raise any notable errors)


.. _moobius.utils._recursive_undataclass:

_recursive_undataclass
---------------------------------------------------------------------------------------------------------------------
_recursive_undataclass(data, typemark_dataclasses)


The inverse function, converts dataclasses back into dicts..
  Parameters:
    data: Dataclassed data.
    typemark_dataclasses: Whether to mark dataclasses in a special way so they are known as such.
  Returns:
    The non-dataclassed data.
  Raises:
    (this function does not raise any notable errors)


.. _moobius.utils.assert_strs:

assert_strs
---------------------------------------------------------------------------------------------------------------------
assert_strs()


Given a list.
  Parameters:
    (this function accepts no arguments)
  Returns:
    The True. Raises an Excpetion if the assert fails.
  Raises:
    (this function does not raise any notable errors)


.. _moobius.utils.enhanced_json_load:

enhanced_json_load
---------------------------------------------------------------------------------------------------------------------
enhanced_json_load(filename)


Loads JSON from the disk,.
  Parameters:
    filename: Filename or bytes.
  Returns:
    The possibly-nested datastructure which may have Dataclasses.
  Raises:
    (this function does not raise any notable errors)


.. _moobius.utils.enhanced_json_save:

enhanced_json_save
---------------------------------------------------------------------------------------------------------------------
enhanced_json_save(filename, data, typemark_dataclasses, indent)


Saves the JSON to the disk and/or a string.
  Parameters:
    filename: The filename or file object to save to. None if not saving to any file.
    data: What needs to be saved. Can be a nested datastructure even with embedded dataclasses.
    typemark_dataclasses=True: Save dataclasses as special dicts so that on enhanced_json_load load they are converted back into dataclasses.
    indent=2: The indent to display the text at.
  Returns:
    The data as a JSON string.
  Raises:
    (this function does not raise any notable errors)


.. _moobius.utils.summarize_html:

summarize_html
---------------------------------------------------------------------------------------------------------------------
summarize_html(html_str)


Creates a summary.
Converts HTML to an easier-for-a-human format by cutting out some of the more common tags. Far from perfect.
  Parameters:
    html_str: N html_string.
  Returns:
    The summary as a string.
  Raises:
    (this function does not raise any notable errors)


.. _moobius.utils.make_fn_async:

make_fn_async
---------------------------------------------------------------------------------------------------------------------
make_fn_async(f)


Converts functions to async functions.
Can be used as "await (make_fun_asycnc(f)(arg1, arg2, etc))..
  Parameters:
    f: Function;.
  Returns:
    The  async version of the function.
  Raises:
    (this function does not raise any notable errors)


.. _moobius.utils.maybe_make_template_files:

maybe_make_template_files
---------------------------------------------------------------------------------------------------------------------
maybe_make_template_files(args)


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
  Parameters:
    args: The list of args.
  Returns:
    The None.
  Raises:
    (this function does not raise any notable errors)


.. _moobius.utils.to_char_id_list:

to_char_id_list
---------------------------------------------------------------------------------------------------------------------
to_char_id_list(c)


Converts the input to a list of character_ids, designed to accept a wide range of inputs.
  Parameters:
    c: This can be one of many things:
        A Character (returns it's id as one-element list).
        A string (assumes it's an id wraps it into a one element list).
        A list of Characters (extracts the ids).
        A list of strings (returns a copy of the list).
        A mixed character and string list.
  Returns:
    The list of character ids.
  Raises:
    (this function does not raise any notable errors)


.. _moobius.utils.set_terminal_logger_level:

set_terminal_logger_level
---------------------------------------------------------------------------------------------------------------------
set_terminal_logger_level(the_level)


Sets the logger from the terminal (but preserves other files).
  Parameters:
    the_level: Level.
  Returns:
    The None.
  Raises:
    (this function does not raise any notable errors)



