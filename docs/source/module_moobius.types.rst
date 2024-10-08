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



Decorator function to make __str__ return the following format:
"Foo(bar=1, baz='two', etc)"; only the non-default or specified fields are included.
This works.

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="fsig">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **add_str_method**(cls)

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="fparam">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* __cls:__ Class to decorate.

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="freturn">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* The decorated function.

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="fraises">
          <b>Raises:</b>
    </p>
  </body>
  </embed>

* (this function does not raise any notable errors)



.. _moobius.types.recv_tmp_convert:

recv_tmp_convert
---------------------------------------------------------------------------------------------------------------------



Tmp function which makes small changes to couple kinds of inbound payloads..

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="fsig">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **recv_tmp_convert**(f_name, the_data)

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="fparam">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* __f_name:__ Request_name,.

* __the_data:__ A dict x.

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="freturn">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* The modified x.

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="fraises">
          <b>Raises:</b>
    </p>
  </body>
  </embed>

* (this function does not raise any notable errors)



.. _moobius.types.assert_strs:

assert_strs
---------------------------------------------------------------------------------------------------------------------



Given a list.

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="fsig">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **assert_strs**()

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="fparam">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* __(this function accepts no arguments):__

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="freturn">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* The True. Raises an Excpetion if the assert fails.

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="fraises">
          <b>Raises:</b>
    </p>
  </body>
  </embed>

* (this function does not raise any notable errors)



.. _moobius.types.limit_len:

limit_len
---------------------------------------------------------------------------------------------------------------------



.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="fsig">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **limit_len**(txt, n)

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="fparam">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* __txt:__ Text.

* __n:__ The maximum length,.

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="freturn">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* The  string with a limited length.
If the string is shortened "...<number of> chars" will be shown at the end.

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="fraises">
          <b>Raises:</b>
    </p>
  </body>
  </embed>

* (this function does not raise any notable errors)



.. _moobius.types.to_char_id_list:

to_char_id_list
---------------------------------------------------------------------------------------------------------------------



Converts the input to a list of character_ids, designed to accept a wide range of inputs.

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="fsig">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **to_char_id_list**(c)

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="fparam">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* __c:__ This can be one of many things:
    A Character (returns it's id as one-element list).
    A string (assumes it's an id wraps it into a one element list).
    A list of Characters (extracts the ids).
    A list of strings (returns a copy of the list).
    A mixed character and string list.

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="freturn">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* The list of character ids.

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="fraises">
          <b>Raises:</b>
    </p>
  </body>
  </embed>

* (this function does not raise any notable errors)



.. _moobius.types.normalize_message:

normalize_message
---------------------------------------------------------------------------------------------------------------------



Normalizes a message to a format that the websocket client understands. See sdk.send_message() for more details.
Note: No file uploading nor interaction is performed. These steps are to be performed in Moobius.send_message().
This function is generally for internal use..
All arguments except message are optional.

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="fsig">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **normalize_message**(message, channel_id, sender, recipients, subtype, len_limit, file_display_name, context, text, link, title, button, path)

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="fparam">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* __message:__ Message.

* __channel_id=None:__ A channel_id.

* __sender=None:__ A sender.

* __recipients=None:__ The recipients.

* __subtype=None:__ A subtype.

* __len_limit=None:__ The optional len_limit.

* __file_display_name=None:__ A file_display_name.

* __context=None:__ The context.

* __text=None:__ The text.

* __link=None:__ The optional link.

* __title=None:__ The optional title.

* __button=None:__ The card button.

* __path=None:__ The file/url path.

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="freturn">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* The  normalized message as a dict but with a MessageContent inside of it.

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="fraises">
          <b>Raises:</b>
    </p>
  </body>
  </embed>

* (this function does not raise any notable errors)



.. _moobius.types.as_update_body:

as_update_body
---------------------------------------------------------------------------------------------------------------------



.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="fsig">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **as_update_body**(payload_body)

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="fparam">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* __payload_body:__ Payload body.

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="freturn">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* The UpdateBody version of it.

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="fraises">
          <b>Raises:</b>
    </p>
  </body>
  </embed>

* (this function does not raise any notable errors)



.. _moobius.types.payload_as_dict:

payload_as_dict
---------------------------------------------------------------------------------------------------------------------



Converts a payload to a dict..

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="fsig">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **payload_as_dict**(payload_type, payload_body, client_id, the_uuid)

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="fparam">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* __payload_type:__ Payload type.

* __payload_body:__ The Payload object or dict-valued payload.

* __client_id:__ The client/service id.

* __the_uuid:__ Any unique uuid.

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="freturn">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* The payload as a dict.

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="fraises">
          <b>Raises:</b>
    </p>
  </body>
  </embed>

* (this function does not raise any notable errors)



************************************
Class InputComponent
************************************

Describes pop-up menus inside of buttons. Such buttons have "componetns" as a list of InputComponent.
Not used if the button does not contain a pop-up menu.



Class attributes
--------------------



InputComponent.label: str:
  Also uses as the app-specified ID of the component.

InputComponent.type: str:
  What kind of box the user sees; types.TEXT | types.DROPDOWN | types.TEXTBOX

InputComponent.required: Optional[bool] = False:
  Is the user forced to use it?

InputComponent.placeholder: Optional[str] = None:
  A hint to the user.

InputComponent.choices: Optional[list[str]] = None:
  What options are available, if the type is types.DROPDOWN.

************************************
Class BottomButton
************************************

Buttons appearing at the bottom of pop-up menus.



Class attributes
--------------------



BottomButton.id: str:
  The app-specified ID of the button that was pressed.

BottomButton.text: str:
  The button text as shown in the screen.

BottomButton.submit: bool:
  True to submit the button press, False to cancel and not submit anything to the service.

************************************
Class Dialog
************************************

<no class docstring>



Class attributes
--------------------



Dialog.title: str = 'Dialog':
  The title on top of the dialog box.

Dialog.components: Optional[list[InputComponent]] = None:
  Each one is a place where the user selects or enters something.

Dialog.bottom_buttons: Optional[list[BottomButton]] = None:
  Bottom buttons.

************************************
Class Button
************************************

A description of a button. These buttons appear above the chat-box.



Class attributes
--------------------



Button.button_id: str:
  The app-specified ID of the button that was pressed.

Button.button_text: str:
  The text which appears in the browser.

Button.dialog: Optional[Dialog] = None:
  If the button opens up a dialog box

************************************
Class ClickArgument
************************************

A button click argument.



Class attributes
--------------------



ClickArgument.label: str:
  A reminder of what label was clicked on.

ClickArgument.value: str:
  The value clicked on.

ClickArgument.filename: Optional[str] = None:
  A filename associated with the argument's label.

************************************
Class ButtonClick
************************************

A description of a button click. Who clicked on which button.
And what component they picked, if the button opens a pop-up menu.



Class attributes
--------------------



ButtonClick.button_id: str:
  The Button ID this applies to.

ButtonClick.channel_id: str:
  What channel the user was in when the pressed the button.

ButtonClick.sender: str:
  The Character ID of who clicked the button. Can be a real user or an agent.

ButtonClick.arguments: Optional[list[ClickArgument]] = None:
  What settings the user choose (for buttons that open a pop-up menu).

ButtonClick.subtype: Optional[str] = BUTTON_CLICK:
  Identifies it as a button click.

ButtonClick.BUTTON_CLICK 

ButtonClick.labels: Optional[list[str]] = None:
  A reminder of what each argument means.

ButtonClick.bottom_button_id: Optional[str] = None:
  For buttons that appear at the bottom.

ButtonClick.context: Optional[dict] = None:
  Rarely used metadata.

ButtonClick.button_type: Optional[str] = None:
  What kind of button was pressed (rarely used).

************************************
Class SimpleAction
************************************

Join, leave, and refresh actions (refresh not technically an action, but has the same data).



Class attributes
--------------------



SimpleAction.subtype: str:
  Subtypes are 'join', 'leave', etc.

SimpleAction.channel_id: str:
  The channel that the user performed the action in.

SimpleAction.sender: str:
  The user id.

SimpleAction.context: Optional[dict] = None:
  Rarely used metadata.

************************************
Class MenuItem
************************************

One element of a right-click menu. The full menu is described by a list of these elements.



Class attributes
--------------------



MenuItem.menu_item_id: str:
  The app-specified ID of the Item.

MenuItem.menu_item_text: str:
  What text to show in the browser.

MenuItem.message_subtypes: str | list[str]:
  What message types will open the menu. ["text","file", etc].

MenuItem.dialog: Optional[Dialog] = None:
  If this menu item opens up a dialog box when clicked.

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
Class MenuItemClick
************************************

A description of a menu right-click. Includes a "copy" of the message that was clicked on.



Class attributes
--------------------



MenuItemClick.menu_item_id: str:
  The MenuItem ID that this click applies to.

MenuItemClick.message_subtype: str:
  The kind of message clicked on, 'text', 'image', 'audio', 'file', or 'card'.

MenuItemClick.message_content: MessageContent:
  The content of the message that was clicked on (note that messages don't have a message content field, they have a content field instead, which is different from this).

MenuItemClick.channel_id: str:
  The channel the user was in when they clicked the message.

MenuItemClick.sender: str:
  The Character ID of the user or agent who clicked the message.

MenuItemClick.message_id: Optional[str] = None:
  The platform-generated ID of which message was clicked on (rarely used).

MenuItemClick.arguments: Optional[list[ClickArgument]] = None:
  What sub-menu settings, if the menu element clicked on has a sub-menu.

MenuItemClick.bottom_button_id: Optional[str] = None:
  For the bottom buttons, if there is a dialog and it has any.

MenuItemClick.context: Optional[dict] = None:
  Metadata rarely used.

MenuItemClick.subtype: Optional[str] = MENU_ITEM_CLICK:
  Identifies it as a menu item click.

MenuItemClick.MENU_ITEM_CLICK 

************************************
Class CanvasItem
************************************

A description of a canvas element. The full canvas description is a list of these elements.



Class attributes
--------------------



CanvasItem.text: Optional[str] = None:
  The text displayed.

CanvasItem.path: Optional[str] = None:
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
  The Character ID of who sent the message. Removed in the Aug 2024 change I think.

MessageBody.message_id: str | None:
  The platform-generated ID of the message itself. Rarely used.

MessageBody.context: Optional[dict] = None:
  Metadata that is rarely used.

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
Class CopyBody
************************************

Used internally for the on_copy_client() callback. Most CCS apps do not need to override the callback.



Class attributes
--------------------



CopyBody.request_id: str:
  Just a platform-generated ID to differentiate different copies.

CopyBody.origin_type: str:
  What kind of data this copy comes from.

CopyBody.status: bool:
  Rarely used. Usually True.

CopyBody.context: Optional[dict] = None:
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

Payload.body: MessageBody | ButtonClick | CopyBody | MenuItemClick | Any:
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
Class StyleItem
************************************

A description of a visual style element. The full visual style description is a list of these elements.



Class attributes
--------------------



StyleItem.widget: str:
  The type of widget. Typically "CANVAS" but other widgets.

StyleItem.display: str:
  Is it visible? "invisible", "visible", or "highlight"

StyleItem.expand: Optional[bool] = None:
  Should the canvas be expanded? Only used for visible.

StyleItem.button_id: Optional[str] = None:
  What button does this apply to?

StyleItem.text: Optional[str] = None:
  What text, if any, does this apply do?

************************************
Class UpdateItem
************************************

A single update of something. A description of an update is a list of these elements.
Most fields are None, only one is non-None at a given time.



Class attributes
--------------------



UpdateItem.character: Character | None:
  The new Character. Only used if a character is bieng updated.

UpdateItem.button: Button | None:
  The new Button. Only used if a Button is bieng updated.

UpdateItem.channel_info: ChannelInfo | None:
  The new ChanelInfo. Only used if a Channel is bieng updated.

UpdateItem.menu_item: MenuItem | None:
  The new MenuItem. Only used if the right-click menu is bieng updated.

UpdateItem.canvas_item: CanvasItem | None:
  The new CanvasItem. Only used if the Canvas is bieng updated.

UpdateItem.style_item: StyleItem | None:
  The new StyleItem. Only used if an element's look and feel is bieng changed.

************************************
Class UpdateBody
************************************

A description of an update. Includes update elements as well as who sees the update.
Used for on_update_xyz callbacks. Not used for the send_update functions.
This is sent to agents to notify them that something that they can "see" has been updated.



Class attributes
--------------------



UpdateBody.subtype: str:
  What is bieng updated, route the Update to the correct callback function. Such as 'update_characters', 'update_channel_info', 'update_canvas', 'update_buttons', 'update_style', etc.

UpdateBody.channel_id: str:
  The Channel ID of the channel this Update is in.

UpdateBody.content: list[UpdateItem]:
  The list of indivual changes in this update.

UpdateBody.recipients: list[str]:
  The list of Character IDs of who sees this update.

UpdateBody.group_id: Optional[str] = None:
  The Group ID of the group of users/agents who see this update.

UpdateBody.context: Optional[dict] = None:
  Rarely used metadata.

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

**********************
Internals
**********************
.. toctree::
   :maxdepth: 2

   moobius.types_internal_attrs <moobius.types_internal_attrs>
