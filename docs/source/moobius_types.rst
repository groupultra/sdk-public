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



Class attributes
--------------------



ButtonArgument.name: str

ButtonArgument.type: str

ButtonArgument.optional: Optional[bool]

ButtonArgument.values: Optional[list[str]]

ButtonArgument.placeholder: str

Class BottomButton
===========================================================================================

Buttons appearing at the bottom of pop-up menus.



Class attributes
--------------------



BottomButton.text: str

BottomButton.type: str

Class Button
===========================================================================================

A description of a button. These buttons appear above the chat-box.



Class attributes
--------------------



Button.button_id: str

Button.button_name: str

Button.new_window: bool

Button.arguments: Optional[list[ButtonArgument]] = None

Button.bottom_buttons: Optional[list[BottomButton]] = None

Class ButtonClickArgument
===========================================================================================

Describes which option users clicked on in a pop-up menu.
A ButtonClick will have a list of ButtonClickArguments if the button opens up a pop-up menu.
Also used, uncommonly, for context-menu clicks which use pop-up submenus.
Not used if the button does not contain a pop-up menu.



Class attributes
--------------------



ButtonClickArgument.name: str

ButtonClickArgument.value: str | int

Class ButtonClick
===========================================================================================

A description of a button click. Who clicked on which button.
And what arguments they picked, if the button opens a pop-up menu.



Class attributes
--------------------



ButtonClick.button_id: str

ButtonClick.channel_id: str

ButtonClick.button_type: str

ButtonClick.sender: str

ButtonClick.arguments: list[ButtonClickArgument]

ButtonClick.context: dict

Class ContextMenuElement
===========================================================================================

One element of a right-click context menu. The full menu is described by a list of these elements.



Class attributes
--------------------



ContextMenuElement.item_name: str

ContextMenuElement.item_id: str

ContextMenuElement.support_subtype: list[str]

ContextMenuElement.new_window: Optional[bool] = False

ContextMenuElement.arguments: Optional[list[ButtonArgument]] = None

Class MessageContent
===========================================================================================

The content of a message. Most messages only have a single non-None item; for example "text" messages only have a "text" element.
The exteption is "card" messages; they have links, title, and buttons.



Class attributes
--------------------



MessageContent.text: Optional[str] = None

MessageContent.path: Optional[str] = None

MessageContent.size: Optional[int] = None

MessageContent.filename: Optional[str] = None

MessageContent.link: Optional[str] = None

MessageContent.title: Optional[str] = None

MessageContent.button: Optional[str] = None

Class MenuClick
===========================================================================================

A description of a context menu right-click. Includes a "copy" of the message that was clicked on.



Class attributes
--------------------



MenuClick.item_id: str

MenuClick.message_id: str

MenuClick.message_subtype: str

MenuClick.message_content: MessageContent

MenuClick.channel_id: str

MenuClick.sender: str

MenuClick.recipients: list[str]

MenuClick.context: dict

MenuClick.arguments: Optional[list[ButtonClickArgument]] = None

Class CanvasElement
===========================================================================================

A description of a canvas element. The full canvas description is a list of these elements.



Class attributes
--------------------



CanvasElement.text: Optional[str] = None

CanvasElement.path: Optional[str] = None

Class View
===========================================================================================

An unused feature, for now.



Class attributes
--------------------



View.character_ids: list[str]

View.button_ids: list[str]

View.canvas_id: str

Class Group
===========================================================================================

A group of users. Only to be used internally.



Class attributes
--------------------



Group.group_id: str

Group.character_ids: list[str]

Class MessageBody
===========================================================================================

A message. Contains the content as well as who, when, and where the message was sent.



Class attributes
--------------------



MessageBody.subtype: str

MessageBody.channel_id: str

MessageBody.content: MessageContent

MessageBody.timestamp: int

MessageBody.recipients: list[str]

MessageBody.sender: str

MessageBody.message_id: str | None

MessageBody.context: dict | None

Class Action
===========================================================================================

A description of a generic task performed by a user. Actions with different subtypes are routed to different callbacks.



Class attributes
--------------------



Action.subtype: str

Action.channel_id: str

Action.sender: str

Action.context: Optional[dict]

Class ChannelInfo
===========================================================================================

A decription of an update for an old, rarely-used feature.



Class attributes
--------------------



ChannelInfo.channel_id: str

ChannelInfo.channel_name: str

ChannelInfo.channel_description: str

ChannelInfo.channel_type: str

Class Copy
===========================================================================================

Used internally for the on_copy_client() callback. Most CCS apps do not need to override the callback.



Class attributes
--------------------



Copy.request_id: str

Copy.origin_type: str

Copy.status: bool

Copy.context: dict

Class Payload
===========================================================================================

A description of a payload received from the websocket. Used internally by the Moobius.handle_received_payload function.



Class attributes
--------------------



Payload.type: str

Payload.request_id: Optional[str]

Payload.user_id: Optional[str]

Payload.body: MessageBody | ButtonClick | Action | Copy | MenuClick | Any

Class Character
===========================================================================================

A description (name, id, image url, etc) of a real or puppet user.



Class attributes
--------------------



Character.character_id: str

Character.name: str

Character.avatar: Optional[str] = None

Character.description: Optional[str] = None

Character.character_context: Optional[dict] = None

Class StyleElement
===========================================================================================

A description of a visual style element. The full visual style description is a list of these elements.



Class attributes
--------------------



StyleElement.widget: str

StyleElement.display: str

StyleElement.expand: Optional[bool] = None

StyleElement.button_id: Optional[str] = None

StyleElement.text: Optional[str] = None

Class UpdateElement
===========================================================================================

A single update of something. A description of an update is a list of these elements.
Most fields are None, only one is non-None at a given time.



Class attributes
--------------------



UpdateElement.character: Character | None

UpdateElement.button: Button | None

UpdateElement.channel_info: ChannelInfo | None

UpdateElement.context_menu_element: ContextMenuElement | None

UpdateElement.canvas_element: CanvasElement | None

UpdateElement.style_element: StyleElement | None

Class Update
===========================================================================================

A description of an update. Includes update elements as well as who sees the update.
Used for on_update_xyz callbacks. Not used for the send_update functions.
This is sent to agents to notify them that something that they can "see" has been updated.



Class attributes
--------------------



Update.subtype: str

Update.channel_id: str

Update.content: list[UpdateElement]

Update.context: dict

Update.recipients: list[str]

Update.group_id: Optional[str] = None

Class UserInfo
===========================================================================================

A description of a user profile.
This is sent to agents so that they can learn about "themselves".



Class attributes
--------------------



UserInfo.avatar: str

UserInfo.description: str

UserInfo.name: str

UserInfo.email: str

UserInfo.email_verified: str

UserInfo.user_id: str

UserInfo.system_context: Optional[dict] = None
