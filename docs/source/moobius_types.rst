.. _moobius_types:

moobius.types
====================================================================================

Module-level functions
===================================================================================

.. _moobius.types.add_str_method:

add_str_method
---------------------------------------------------------------------------------------------------------------------
add_str_method(cls)

Decorator function to make __str__ return the following format:
"Foo(bar=1, baz='two', etc)"; only the non-default fields are included.

.. _moobius.types.add_str_method.__str__:

add_str_method.__str__
---------------------------------------------------------------------------------------------------------------------
add_str_method.__str__(self)

<No doc string>

===================================================================================

Class ButtonArgument
===========================================================================================

Describes pop-up menus inside of buttons. Such buttons have "arguments" as a list of ButtonArguments.
Not used if the button does not contain a pop-up menu.



Class BottomButton
===========================================================================================

Buttons appearing at the bottom of pop-up menus.



Class Button
===========================================================================================

A description of a button. These buttons appear above the chat-box.



Class ButtonClickArgument
===========================================================================================

Describes which option users clicked on in a pop-up menu.
A ButtonClick will have a list of ButtonClickArguments if the button opens up a pop-up menu.
Also used, uncommonly, for context-menu clicks which use pop-up submenus.
Not used if the button does not contain a pop-up menu.



Class ButtonClick
===========================================================================================

A description of a button click. Who clicked on which button.
And what arguments they picked, if the button opens a pop-up menu.



Class ContextMenuElement
===========================================================================================

One element of a right-click context menu. The full menu is described by a list of these elements.



Class MessageContent
===========================================================================================

The content of a message. Most messages only have a single non-None item; for example "text" messages only have a "text" element.
The exteption is "card" messages; they have links, title, and buttons.



Class MenuClick
===========================================================================================

A description of a context menu right-click. Includes a "copy" of the message that was clicked on.



Class CanvasElement
===========================================================================================

A description of a canvas element. The full canvas description is a list of these elements.



Class View
===========================================================================================

An unused feature, for now.



Class Group
===========================================================================================

A group of users. Only to be used internally.



Class MessageBody
===========================================================================================

A message. Contains the content as well as who, when, and where the message was sent.



Class Action
===========================================================================================

A description of a generic task performed by a user. Actions with different subtypes are routed to different callbacks.



Class ChannelInfo
===========================================================================================

A decription of an update for an old, rarely-used feature.



Class Copy
===========================================================================================

Used internally for the on_copy_client() callback. Most CCS apps do not need to override the callback.



Class Payload
===========================================================================================

A description of a payload received from the websocket. Used internally by the Moobius.handle_received_payload function.



Class Character
===========================================================================================

A description (name, id, image url, etc) of a real or puppet user.



Class StyleElement
===========================================================================================

A description of a visual style element. The full visual style description is a list of these elements.



Class UpdateElement
===========================================================================================

A single update of something. A description of an update is a list of these elements.
Most fields are None, only one is non-None at a given time.



Class Update
===========================================================================================

A description of an update. Includes update elements as well as who sees the update.
Used for on_update_xyz callbacks. Not used for the send_update functions.
This is sent to agents to notify them that something that they can "see" has been updated.



Class UserInfo
===========================================================================================

A description of a user profile.
This is sent to agents so that they can learn about "themselves".


