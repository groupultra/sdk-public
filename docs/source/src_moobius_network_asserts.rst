.. _src_moobius_network_asserts:

src.moobius.network.asserts
===================================

Module-level functions
==================

types_assert
----------------------
types_assert(ty, \*kwargs)
Asserts that every one of kwargs is type ty, giving an error message if there is a mismatch.
types_assert(str, foo=foo, bar=bar)

structure_assert
----------------------
structure_assert(gold, green, base_message, path)
Asserts whether "green" follows the data-structure in "gold".

Parameters:
  gold: The datastructure to match. This is a nested datastructure with the following elements.
    Lists: These can be any length in the green data structure, including zero.
    Tuples: These impose a fixed length with the gold and green corresponding 1:1.
    Dicts: These must have the exact same keys gold vs green (like tuples not like lists).
    Bools: Must be True or False, not None.
    Ints: Must be ints in the green.
    Floats: Must be numbers in the green (ints or floats).
      Note: The Platform expects many number literals to be strings.
    Strings: Must be strings in the green. They do not have to match.
    Functions: Used for more complex cases.
      calls f(green, base_message, path). f can in turn call structure_assert or other functions.
  green: The datastructure (before conversion to a JSON string) that must fit the gold datastructure.
  base_message: Give some useful information as to the error message!
  path=None: The path within the datastructure. None will be [].

Returns: True if the assert passes.
Raises: PlatformAssertException if the assert fails, using the base_message.

optional_dict_template
----------------------
optional_dict_template(min_keys, dtemplate)
Creates a template function will not error on missing keys unless missing keys are in min_keys.

temp_modify
----------------------
temp_modify(socket_request)
Sometimes the request has extra stuff. This function removes it so it works.
But TODO remove extra stuff and test.

_style_check
----------------------
_style_check(style_element, base_message, path)
One element in a style vector. This is the most flexible.

_socket_update_body_assert
----------------------
_socket_update_body_assert(b, base_message, path)
Many requests are updates with a body.

_socket_message_body_assert1
----------------------
_socket_message_body_assert1(b, base_message, path, is_up)
Both text and image messages are supported.

_button_click_body_assert
----------------------
_button_click_body_assert(b, base_message, path)
Some buttons have options. Some don't.

_context_menuclick_body_assert
----------------------
_context_menuclick_body_assert(b, base_message, path)
Right click context menu click

_action_body_assert
----------------------
_action_body_assert(b, base_message, path)
Various actions

socket_assert
----------------------
socket_assert(x)
Asserts that a socket call is correct, using the type and subtype to determine the socket.
Note: There is no HTTPs assert fn, instead the arguments to the function are asserted.

optional_dict_template.t_fn
----------------------
optional_dict_template.t_fn(d, base_message, path)
<No doc string>

_socket_update_body_assert._each_button
----------------------
_socket_update_body_assert._each_button(x, base_message, the_path)
<No doc string>

==================


Class PlatformAssertException
==================

(No doc string)