.. _src_moobius_utils:

src.moobius.utils
===================================


Module-level functions
==================

summarize_html
----------------------
**summarize_html(html_str)**

Converts HTML to an easier-for-a-human format by cutting out some of the more common tags. Far from perfect.

make_fn_async
----------------------
**make_fn_async(f)**

Converts functions to async functions.

maybe_make_template_files
----------------------
**maybe_make_template_files(args)**

Makes template files if there is a need to do so, based on args and sys.argv.
Called by "import moobius" with no args and by wand.run() before initializing the Moobius class.

A template main.py python file which calls Wand.run:
  Only created if the file does not exist AND "make_main main.py" (or "make_main foo.py", etc) is in the system args.

A sample config.py:
  Only created if "config_path" is in args (or system args) AND the file does not exist.
  This requires user information:
     email: If no system arg "email my@email.com" or "username my@email.com" is specified, prompts for one with input().
     password: If no system arg "password my_sec**t_pword", prompts for one.
     channels: If no system arg "channels abc... def..." to specify one or more channels, prompts for one or more.
  Note: when the user inputs an empty input() than a nonfunctional default is used, which can be filled in later.

Unittests to run in a python prompt in an empty folder:
  >>> # Make a main.py file:
  >>> import sys; sys.argv = '_ make_main main.py'.split(' '); import moobius;
  >>> # Prompt the user for credentials and put these in the service.json (NOTE: will generate an error b/c None class):
  >>> import sys; from moobius import MoobiusWand; MoobiusWand().run(None, config_path="config/service.json")
  >>> # Provide credentials, making a service.json with no user input (NOTE: will generate an error b/c None class):
  >>> import sys; sys.argv = '_ email abc@123.com password IAmSecret channels abc-123 def-4561111111111111111111'.split(' '); from moobius import MoobiusWand; MoobiusWand().run(0, config_path="config/service.json")
  >>> # Provide agent credentials. There is no need to provide a channel id (NOTE: will generate an error b/c None class).
  >>> import sys; sys.argv = '_ email abc@123.com password IAmSecret'.split(' '); from moobius import MoobiusWand; MoobiusWand().run(0, config_path="config/agent.json", is_agent=True)

make_fn_async.run_f
----------------------
**make_fn_async.run_f(\*kwargs)**

<No doc string>

make_fn_async.run_f.f1
----------------------
**make_fn_async.run_f.f1()**

<No doc string>


==================


Class EnhancedJSONEncoder
==================

Json Encoder but with automatic conversion of dataclasses to dict.

EnhancedJSONEncoder.default
----------------------
**EnhancedJSONEncoder.default(self, o)**

<No doc string>

EnhancedJSONEncoder.__str__
----------------------
**EnhancedJSONEncoder.__str__(self)**

<No doc string>

EnhancedJSONEncoder.__repr__
----------------------
**EnhancedJSONEncoder.__repr__(self)**

<No doc string>