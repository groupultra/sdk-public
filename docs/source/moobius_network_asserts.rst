.. _moobius_network_asserts:

###################################################################################
moobius.network.asserts
###################################################################################

******************************
Module-level functions
******************************

.. _moobius.network.asserts.types_assert:

types_assert
---------------------------------------------------------------------------------------------------------------------
types_assert(ty, \*kwargs)


Asserts that every one of kwargs is of this type.
  Parameters:
    ty: The type.
  Returns:
    The True.
    Raises a PlatformAssertException if there is a mismatch.
  Raises:
    (this function does not raise any errors of its own)


.. _moobius.network.asserts.structure_assert:

structure_assert
---------------------------------------------------------------------------------------------------------------------
structure_assert(gold, green, base_message, path)


Asserts whether a data-structure follows a given pattern.
  Parameters:
    gold: The datastructure to match. This is a nested datastructure with the following elements.
    
    Lists: These can be any length in the green data structure, including zero.
    
    Tuples: These impose a fixed length with the gold and green corresponding 1:1.
    
    Dicts: These must have the exact same keys gold vs green (like tuples not like lists).
    
    Bools: The Must be True or False, not None.
    
    Ints: The Must be ints in the green.
    
    Floats: The Must be numbers in the green (ints or floats).
    
    Note: The Platform expects many number literals to be strings.
    
    Strings: The Must be strings in the green. They do not have to match.
    
    Functions: The Used for more complex cases.
          calls f(green, base_message, path). f can in turn call structure_assert or other functions.
    
    green: The datastructure (before conversion to a JSON string) that must fit the gold datastructure.
    
    base_message: The Give some useful information as to the error message!.
    
    path=None: The path within the datastructure. None will be [].
  Returns:
    The True if the assert passes.
  Raises:
    PlatformAssertException if the assert fails, using the base_message.


.. _moobius.network.asserts.min_subset_dict:

min_subset_dict
---------------------------------------------------------------------------------------------------------------------
min_subset_dict(min_keys, dtemplate)


Creates a template-matching function that will not error on missing keys, unless they are in in min_keys..
  Parameters:
    min_keys: The minimum list of keys.
    
    dtemplate: The  template dict.
  Returns:
    The matching function.
  Raises:
    (this function does not raise any errors of its own)


.. _moobius.network.asserts.temp_modify:

temp_modify
---------------------------------------------------------------------------------------------------------------------
temp_modify(socket_request)


Sometimes the request has extra stuff. This function removes it. Somewhat deprecated..
  Parameters:
    socket_request: The socket_request dict.
  Returns:
    The modified socket_request dict.
  Raises:
    (this function does not raise any errors of its own)


.. _moobius.network.asserts._style_check:

_style_check
---------------------------------------------------------------------------------------------------------------------
_style_check(style_element, base_message, path)


Asserts element in a style vector. This is the most flexible..
  Parameters:
    style_element: The style_element.
    
    base_message: The base_message for debugging.
    
    path: The path for debugging.
  Returns:
    The True if it works. Raises a PlatformAssertException if it fails.
  Raises:
    (this function does not raise any errors of its own)


.. _moobius.network.asserts._context_menu_item_check:

_context_menu_item_check
---------------------------------------------------------------------------------------------------------------------
_context_menu_item_check(cmenu_item, base_message, path)


Checks the right-click context menu..
  Parameters:
    cmenu_item: The context menu element.
    
    base_message: The base_message for debugging.
    
    path: The path for debugging.
  Returns:
    The True if it works. Raises a PlatformAssertException if it fails.
  Raises:
    (this function does not raise any errors of its own)


.. _moobius.network.asserts._socket_update_body_assert:

_socket_update_body_assert
---------------------------------------------------------------------------------------------------------------------
_socket_update_body_assert(b, base_message, path)


Many requests are updates with a body..
  Parameters:
    b: The body.
    
    base_message: The base_message for debugging.
    
    path: The path for debugging.
  Returns:
    The True if it works. Raises a PlatformAssertException if it fails.
  Raises:
    (this function does not raise any errors of its own)


.. _moobius.network.asserts._socket_message_body_assert1:

_socket_message_body_assert1
---------------------------------------------------------------------------------------------------------------------
_socket_message_body_assert1(b, base_message, path, is_up)


All message types, including text and image messages, are supported..
  Parameters:
    b: The body.
    
    base_message: The base_message for debugging.
    
    path: The path for debugging.
    
    is_up: The  flag for the message bieng a message_up.
  Returns:
    The True if it works. Raises a PlatformAssertException if it fails.
  Raises:
    (this function does not raise any errors of its own)


.. _moobius.network.asserts._button_click_body_assert:

_button_click_body_assert
---------------------------------------------------------------------------------------------------------------------
_button_click_body_assert(b, base_message, path)


Some buttons have options. Some don't, so options are optional..
  Parameters:
    b: The button click body.
    
    base_message: The base_message for debugging.
    
    path: The path for debugging.
  Returns:
    The True if it works. Raises a PlatformAssertException if it fails.
  Raises:
    (this function does not raise any errors of its own)


.. _moobius.network.asserts._context_menuclick_body_assert:

_context_menuclick_body_assert
---------------------------------------------------------------------------------------------------------------------
_context_menuclick_body_assert(b, base_message, path)


Right click context menu click..
  Parameters:
    b: The context menu click body.
    
    base_message: The base_message for debugging.
    
    path: The path for debugging.
  Returns:
    The True if it works. Raises a PlatformAssertException if it fails.
  Raises:
    (this function does not raise any errors of its own)


.. _moobius.network.asserts._action_body_assert:

_action_body_assert
---------------------------------------------------------------------------------------------------------------------
_action_body_assert(b, base_message, path)


Various actions..
  Parameters:
    b: The n action body.
    
    base_message: The base_message for debugging.
    
    path: The path for debugging.
  Returns:
    The True if it works. Raises a PlatformAssertException if it fails.
  Raises:
    (this function does not raise any errors of its own)


.. _moobius.network.asserts.socket_assert:

socket_assert
---------------------------------------------------------------------------------------------------------------------
socket_assert(x)


The main assert function. Asserts that a socket call is correct, using the type and subtype to determine the socket.
Note: There is no HTTPs assert fn, instead the arguments to the function are asserted...
  Parameters:
    x: The generic socket payload.
  Returns:
    The True if the assert suceeds.
  Raises:
    PlatformAssertException if it fails.


************************************
Class PlatformAssertException
************************************

A special Exception that is raised when the datastructure is not the correct format.



Class attributes
--------------------

PlatformAssertException.Exception
