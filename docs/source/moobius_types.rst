.. _moobius_types:

###################################################################################
moobius.types
###################################################################################

******************************
Module-level functions
******************************

.. _moobius.types.add_str_method:

add_str_method
---------------------------------------------------------------------------------------------------------------------
add_str_method(cls)


Decorator function to make __str__ return the following format:
"Foo(bar=1, baz='two', etc)"; only the non-default or specified fields are included.
This works.
  Parameters:
    cls: The class to decorate.
  Returns:
    The decorated function.
  Raises:
    (this function does not raise any errors of its own)


************************************
Class ButtonArgument
************************************

Describes pop-up menus inside of buttons. Such buttons have "arguments" as a list of ButtonArguments.
Not used if the button does not contain a pop-up menu.



Class attributes
--------------------



ButtonArgument.name: str:
  The app-specified ID of the argument.

ButtonArgument.type: str:
  What kind of box the user sees; "string" | "enum"

ButtonArgument.optional: Optional[bool]:
  Can the user skip it?

ButtonArgument.placeholder: str:
  A hint to the user.

ButtonArgument.values: Optional[list[str]] = None:
  What values are available, if the type is enum. Use None if the type is str.

************************************
Class BottomButton
************************************

Buttons appearing at the bottom of pop-up menus.



Class attributes
--------------------



BottomButton.text: str:
  The button text.

BottomButton.type: str:
  The button type.

************************************
Class Button
************************************

A description of a button. These buttons appear above the chat-box.



Class attributes
--------------------



Button.button_id: str:
  The app-specified ID of the button was pressed.

Button.button_name: str:
  The text which appears in the browser.

Button.new_window: bool:
  Does the button open up a menu to select options in?

Button.arguments: Optional[list[ButtonArgument]] = None:
  If new_window, what arguments appear in the pop-up.

Button.bottom_buttons: Optional[list[BottomButton]] = None:
  If new_window, what buttons appear at the bottom of the pop-up.

************************************
Class ButtonClickArgument
************************************

Describes which option users clicked on in a pop-up menu.
A ButtonClick will have a list of ButtonClickArguments if the button opens up a pop-up menu.
Also used, uncommonly, for context-menu clicks which use pop-up submenus.
Not used if the button does not contain a pop-up menu.



Class attributes
--------------------



ButtonClickArgument.name: str:
  The ButtonArgument ID this applies to.

ButtonClickArgument.value: str | int:
  The choice itself. Int for the "enum" button type. String for the "string" button type.

************************************
Class ButtonClick
************************************

A description of a button click. Who clicked on which button.
And what arguments they picked, if the button opens a pop-up menu.



Class attributes
--------------------



ButtonClick.button_id: str:
  The Button ID this applies to.

ButtonClick.channel_id: str:
  What channel the user was in when the pressed the button.

ButtonClick.button_type: str:
  What kind of button was pressed (rarely used).

ButtonClick.sender: str:
  The Character ID of who clicked the button. Can be a real user or an agent.

ButtonClick.arguments: list[ButtonClickArgument]:
  What settings the user chosse (for buttons that open a pop-up menu).

ButtonClick.context: dict:
  Rarely used metadata.

************************************
Class ContextMenuElement
************************************

One element of a right-click context menu. The full menu is described by a list of these elements.



Class attributes
--------------------



ContextMenuElement.item_id: str:
  The app-specified ID of the Element.

ContextMenuElement.item_name: str:
  What text to show in the browser.

ContextMenuElement.support_subtype: list[str]:
  What message types will open the context menu. ["text","file", etc].

ContextMenuElement.new_window: Optional[bool] = False:
  Does clicking this menu open it's own sub-menu (this is an advanced feature).

ContextMenuElement.arguments: Optional[list[ButtonArgument]] = None:
  If clicking this menu opens a sub-menu, what is inside said sub-menu.

************************************
Class MessageContent
************************************

The content of a message. Most messages only have a single non-None item; for example "text" messages only have a "text" element.
The exteption is "card" messages; they have links, title, and buttons.



Class attributes
--------------------



MessageContent.text: Optional[str] = None:
  The string (for "text" messages).

MessageContent.path: Optional[str] = None:
  The URL (for any non-text message).

MessageContent.size: Optional[int] = None:
  The size in bytes, used for downloadable "file" messages only.

MessageContent.filename: Optional[str] = None:
  The filename to display, used for downloadable "file" messages only.

MessageContent.link: Optional[str] = None:
  The URL, used for "card" messages which have a clickable link.

MessageContent.title: Optional[str] = None:
  The title shown, used for "card" messages which have a clickable link.

MessageContent.button: Optional[str] = None:
  The text of the button shown, used for "card" messages which have a clickable link.

************************************
Class MenuClick
************************************

A description of a context menu right-click. Includes a "copy" of the message that was clicked on.



Class attributes
--------------------



MenuClick.item_id: str:
  The ContextMenuElement ID that this click applies to.

MenuClick.message_id: str:
  The platform-generated ID of which message was clicked on (rarely used).

MenuClick.message_subtype: str:
  The kind of message clicked on, 'text', 'image', 'audio', 'file', or 'card'.

MenuClick.message_content: MessageContent:
  The content of the message that was clicked on.

MenuClick.channel_id: str:
  The channel the user was in when they clicked the message.

MenuClick.sender: str:
  The Character ID of the user or agent who clicked the message.

MenuClick.recipients: list[str]:
  Rarely used.

MenuClick.context: dict:
  Metadata rarely used.

MenuClick.arguments: Optional[list[ButtonClickArgument]] = None:
  What sub-menu settings, if the menu element clicked on has a sub-menu.

************************************
Class CanvasElement
************************************

A description of a canvas element. The full canvas description is a list of these elements.



Class attributes
--------------------



CanvasElement.text: Optional[str] = None:
  The text displayed.

CanvasElement.path: Optional[str] = None:
  The URL of the displayed image.

************************************
Class View
************************************

An unused feature, for now.



Class attributes
--------------------



View.character_ids: list[str]:
  List of Character IDs.

View.button_ids: list[str]:
  List of Button ids.

View.canvas_id: str:
  The platform-generated Canvas ID.

************************************
Class Group
************************************

A group of users. Only to be used internally.



Class attributes
--------------------



Group.group_id: str:
  The platform-generated Group ID, used internally to send messages.

Group.character_ids: list[str]:
  A list of character ids who belong to this group.

************************************
Class MessageBody
************************************

A message. Contains the content as well as who, when, and where the message was sent.



Class attributes
--------------------



MessageBody.subtype: str:
  What kind of message it is; "text", "image", "audio", "file", or "card".

MessageBody.channel_id: str:
  The Channel ID of the channel the message was sent in.

MessageBody.content: MessageContent:
  The content of the message.

MessageBody.timestamp: int:
  When the message was sent.

MessageBody.recipients: list[str]:
  The Character IDs of who the message was sent to.

MessageBody.sender: str:
  The Character ID of who sent the message.

MessageBody.message_id: str | None:
  The platform-generated ID of the message itself. Rarely used.

MessageBody.context: dict | None:
  Metadata that is rarely used.

************************************
Class Action
************************************

A description of a generic task performed by a user. Actions with different subtypes are routed to different callbacks.



Class attributes
--------------------



Action.subtype: str:
  The subtype of the action. Used internally to route the action to the correct callback function.

Action.channel_id: str:
  The Channel ID of the channel the action is in.

Action.sender: str:
  The Character ID of who did the action.

Action.context: Optional[dict]:
  Rarely used metadata.

************************************
Class ChannelInfo
************************************

A decription of an update for an old, rarely-used feature.



Class attributes
--------------------



ChannelInfo.channel_id: str:
  The Channel ID of this channel.

ChannelInfo.channel_name: str:
  The name of the channel, as appears in the list of channels.

ChannelInfo.channel_description: str:
  A description that ideally should give information about what the channel is about.

ChannelInfo.channel_type: str:
  An enum with "dcs", "ccs", etc. Rarely used.

************************************
Class Copy
************************************

Used internally for the on_copy_client() callback. Most CCS apps do not need to override the callback.



Class attributes
--------------------



Copy.request_id: str:
  Just a platform-generated ID to differentiate different copies.

Copy.origin_type: str:
  What kind of data this copy comes from.

Copy.status: bool:
  Rarely used.

Copy.context: dict:
  Rarely used metadata.

************************************
Class Payload
************************************

A description of a payload received from the websocket. Used internally by the Moobius.handle_received_payload function.



Class attributes
--------------------



Payload.type: str:
  The kind of payload, used internally to route the payload to the correct callback function.

Payload.request_id: Optional[str]:
  A platform-generated ID to differentiate payloads.

Payload.user_id: Optional[str]:
  The Character ID of who dispatched this payload.

Payload.body: MessageBody | ButtonClick | Action | Copy | MenuClick | Any:
  The body of the payload.

************************************
Class Character
************************************

A description (name, id, image url, etc) of a real or puppet user.



Class attributes
--------------------



Character.character_id: str:
  The platform-generated ID of the character. Both for real and puppet users.

Character.name: str:
  The name as appears in the group chat.

Character.avatar: Optional[str] = None:
  The image the character has.

Character.description: Optional[str] = None:
  Information about who this Character is.

Character.character_context: Optional[dict] = None:
  Rarely used metadata.

************************************
Class StyleElement
************************************

A description of a visual style element. The full visual style description is a list of these elements.



Class attributes
--------------------



StyleElement.widget: str:
  The type of widget. Typically "CANVAS" but other widgets.

StyleElement.display: str:
  Is it visible? "invisible", "visible", or "highlight"

StyleElement.expand: Optional[bool] = None:
  Should the canvas be expanded? Only used for visible.

StyleElement.button_id: Optional[str] = None:
  What button does this apply to?

StyleElement.text: Optional[str] = None:
  What text, if any, does this apply do?

************************************
Class UpdateElement
************************************

A single update of something. A description of an update is a list of these elements.
Most fields are None, only one is non-None at a given time.



Class attributes
--------------------



UpdateElement.character: Character | None:
  The new Character. Only used if a character is bieng updated.

UpdateElement.button: Button | None:
  The new Button. Only used if a Button is bieng updated.

UpdateElement.channel_info: ChannelInfo | None:
  The new ChanelInfo. Only used if a Channel is bieng updated.

UpdateElement.context_menu_element: ContextMenuElement | None:
  The new ContextMenuElement. Only used if the right-click menu is bieng updated.

UpdateElement.canvas_element: CanvasElement | None:
  The new CanvasElement. Only used if the Canvas is bieng updated.

UpdateElement.style_element: StyleElement | None:
  The new StyleElement. Only used if an element's look and feel is bieng changed.

************************************
Class Update
************************************

A description of an update. Includes update elements as well as who sees the update.
Used for on_update_xyz callbacks. Not used for the send_update functions.
This is sent to agents to notify them that something that they can "see" has been updated.



Class attributes
--------------------



Update.subtype: str:
  What is bieng updated, route the Update to the correct callback function. Such as 'update_characters', 'update_channel_info', 'update_canvas', 'update_buttons', 'update_style', etc.

Update.channel_id: str:
  The Channel ID of the channel this Update is in.

Update.content: list[UpdateElement]:
  The list of indivual changes in this update.

Update.context: dict:
  Rarely used metadata.

Update.recipients: list[str]:
  The list of Character IDs of who sees this update.

Update.group_id: Optional[str] = None:
  The Group ID of the group of users/agents who see this update.

************************************
Class UserInfo
************************************

A description of a user profile.
This is sent to agents so that they can learn about "themselves".



Class attributes
--------------------



UserInfo.avatar: str:
  The URL to the image shown in the group chat.

UserInfo.description: str:
  A description of who this user is.

UserInfo.name: str:
  The user's name.

UserInfo.email: str:
  The user's email.

UserInfo.email_verified: str:
  Did the user check thier email and click that link?

UserInfo.user_id: str:
  The platform-generated Character ID for this user.

UserInfo.system_context: Optional[dict] = None:
  Rarely-used metadata.
