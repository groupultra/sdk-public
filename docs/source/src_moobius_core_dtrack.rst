.. _src_moobius_core_dtrack:

src.moobius.core.dtrack
===================================


Module-level functions
==================

check_if_logio_i_fied
----------------------
**check_if_logio_i_fied()**

Returns weather @dtrack.logios are enabled by checking the wand.py file.

errorfree_str
----------------------
**errorfree_str(x)**

Returns an attempted repr(x), catching and str()-ing errors thrown by i.e. custom __repr__ methods.

_convert_http_response
----------------------
**_convert_http_response(response)**

Returns the response-as-str or an error code.

add_logfile
----------------------
**add_logfile(disk_file, \*kwargs)**

Adds a log file given a disk_file string and "level" kwarg. Pass in disk_file=None to instead clear all disk_files.

_log_core
----------------------
**_log_core(func, args, kwargs, out, is_async)**

Logs a function given its inputs and outputs, returning the function output.

Parameters:
  func (callable): The function object.
  args (list): Positional arguments to said function.
  kwargs (dict): key-value args to said function.
  out: The output of the function.
  is_async (bool): If the function is a coroutine.
    coroutines are logged twice, with a <Begin await> output and then the actual output.

Returns: the "out" param it is given (this isn't generally used).

logio
----------------------
**logio(func)**

Log i/o decorator that takes in a function and returns a function which behaves the same except that it logs it's inputs and outputs.

log_info_color
----------------------
**log_info_color()**

<No doc string>

log_debug
----------------------
**log_debug()**

Drop-in replacement for loguru.debug()

log_info
----------------------
**log_info()**

Drop-in replacement for loguru.info()

log_warning
----------------------
**log_warning()**

Drop-in replacement for loguru.warning()

log_error
----------------------
**log_error()**

Drop-in replacement for loguru.error()

log_get_call
----------------------
**log_get_call(url, response, \*kwargs)**

Logs a get call given a url, reponse, and any kwargs passed to .get() to the main_logstore singleton object.

log_post_call
----------------------
**log_post_call(url, response, \*kwargs)**

log_get_call but POST instead of GET.

recent_calls
----------------------
**recent_calls(n)**

Returns up to n recent Fcall objects in chronolgical order. But for this process only.

_decorator_update
----------------------
**_decorator_update(txt, f)**

Applies f(decorator lines, def_line) => decorator lines to each def. Returns the modified txt.

set_to_dtrack_or_loguru
----------------------
**set_to_dtrack_or_loguru(txt, is_to_dtrack)**

Sets the source code *txt* to use dtrack's logger system instead of loguru OR the reverse of this, if *is_to_dtrack*=False.
Modify main_logstore.print_fcalls, etc to change what is printed to console.

checked_modification
----------------------
**checked_modification(to_dtrack)**

Modifies ALL files to use or not use dtrack.
When modifying files to use dtrack, an exception is thrown and NO files are modified unless ALL modifications are reversable.

delete_all_logs
----------------------
**delete_all_logs()**

Deletes all logs across all projects, both loguru and dtrack-based logs are deleted.

delete_all_databases
----------------------
**delete_all_databases()**

Deletes all logs across all projects, both loguru and dtrack-based logs are deleted.

_decorator_update._is_def_line
----------------------
**_decorator_update._is_def_line(the_line)**

<No doc string>

_decorator_update._is_class_line
----------------------
**_decorator_update._is_class_line(the_line)**

<No doc string>

_decorator_update._is_decorator_line
----------------------
**_decorator_update._is_decorator_line(the_line)**

<No doc string>

_decorator_update._is_emptyish_line
----------------------
**_decorator_update._is_emptyish_line(the_line)**

<No doc string>

set_to_dtrack_or_loguru._decf
----------------------
**set_to_dtrack_or_loguru._decf(decorators, def_line)**

<No doc string>

checked_modification.show_difference
----------------------
**checked_modification.show_difference(str1, str2, diff_message)**

<No doc string>

logio.logio_wrapped_function
----------------------
**logio.logio_wrapped_function(\*kwargs)**

<No doc string>

logio.logio_wrapped_function
----------------------
**logio.logio_wrapped_function(\*kwargs)**

<No doc string>


==================


Class LogStore
==================

Thread-safe log storage. Note: (I think) each process spawned gets it's own LogStore

LogStore.__init__
----------------------
**LogStore.__init__(self)**

<No doc string>

LogStore.add_fcall
----------------------
**LogStore.add_fcall(self, is_async, sym_qual, argnames, args, kwargs, f_output)**

Adds a single function call to the storage. Thread-safe like all operations

Parameters:
  is_async (bool): If the function is async.
  sym_qual (str): The name of the function and any enclosing modules.
    Example: "module_name.Class_name.method_name"
  argnames (list): The name of each argument.
  kwargs (dict): The kv-pair passed to the function.
    Example: (a=1, b=2) => {'a':1, 'b':2}
  f_output: The functions output.

Returns None

LogStore.filter_txt
----------------------
**LogStore.filter_txt(self, log_txt)**

Removes a specific "spam-test" in Moobius demo.

LogStore.clear_logs
----------------------
**LogStore.clear_logs(self)**

Empties the entire storage.

LogStore.add_log_entry
----------------------
**LogStore.add_log_entry(self, x)**

Adds and (optionally) prints a log that is not related to a specific function call. Much like loguru.info()

LogStore.add_error
----------------------
**LogStore.add_error(self, x)**

Adds a special high-alert log message. Does not throw an exception. Much like loguru.error()

LogStore.file_save_loop
----------------------
**LogStore.file_save_loop(self)**

Save logs to disk, clearning them from this file.

LogStore.add_GET_call
----------------------
**LogStore.add_GET_call(self, url, response, \*kwargs)**

Stores a get call given a url, response, and the .get()'s **kwargs. Optionally prints it.

LogStore.add_POST_call
----------------------
**LogStore.add_POST_call(self, url, response, \*kwargs)**

Same as add_GET_call but for POST.

LogStore.__str__
----------------------
**LogStore.__str__(self)**

<No doc string>

LogStore.__repr__
----------------------
**LogStore.__repr__(self)**

<No doc string>

LogStore.file_save_loop._get_log_txt
----------------------
**LogStore.file_save_loop._get_log_txt(self, highlev_only)**

<No doc string>