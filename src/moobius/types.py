# This module does three things:
# 1. Defines string literals so that all the "magic strings" are in one place.
# 2. Defines Dataclass types for messages, buttons, etc.
# 3. Provides "type-projection" functions that are used to convert a range of different data all to a particular format.

import os, dataclasses, pathlib
from dataclasses import dataclass
from typing import Optional, Any

from loguru import logger


########################################### Constants #############################################################
BUTTON = "button" # Widget type, clickable button.
CANVAS = "canvas" # Widget type, canvas. No interaction except expanding it and contracting it.
SERVICE = "service" # A special value for a group_id to indicate a message sent to the service with no recipients.
ACTION = "action" # A type of websocket payload, an action.
UPDATE = "update" # A type of websocket payload, an update.
COPY = "copy" # A type of websocket payload, for compying a message. Used internally.
ROGER = "roger" # A type of websocket payload, similar to COPY.
BUTTON_CLICK = "button_click" # A type of websocket payload, sending a button click.
MENU_ITEM_CLICK = "menu_item_click" # A type of websocket payload, sending a menu click.
MESSAGE_UP = "message_up" # A type of websocket payload, sending a message to the service.
MESSAGE_DOWN = "message_down" # A type of websocket payload, recieving a message from the service.
FETCH_CHARACTERS = "fetch_characters" # A subtype of an action payload, requesting the characters.
FETCH_BUTTONS = "fetch_buttons" # A subtype of an action payload, requesting the buttons.
FETCH_CANVAS = "fetch_canvas" # A subtype of an action payload, requesting the canvas.
FETCH_STYLE = "fetch_style" # A subtype of an action payload, requesting the style.
FETCH_MENU = "fetch_menu"  # A subtype of an action payload, requesting the right-click menu.
FETCH_CHANNEL_INFO = "fetch_channel_info" # A subtype of an action payload, requesting the 
JOIN = "join" # A subtype of an action payload, the user pastes in the ID and joins.
LEAVE_CHANNEL = "leave" # A subtype of an action payload, the user presses the leave channel button.
REFRESH = "refresh"
HEARTBEAT = "heartbeat" # A subtype of an action payload, that is called periodically.
UPDATE_CHARACTERS = "characters" # A subtype of the update payload, an update to the characters.
UPDATE_CHANNEL_INFO = "channel_info" # A subtype of the update payload, an Update for the channel name, description, etc.
UPDATE_CANVAS = "canvas" # A subtype of the update payload, an Update for the canvas.
UPDATE_BUTTONS = "buttons" # A subtype of the update payload, an Update for the buttons.
UPDATE_STYLE = "style" # A subtype of the update payload, an Update for the style.
UPDATE_MENU = "menu" # An Update for the right-click menu.
USER_LOGIN = "user_login" # A subtype of the update payload, an Update for logging in.
SERVICE_LOGIN = "service_login" # A subtype of the update payload, an Update for logging in.
TEXT = "text" # A message subtype, a simple string.
IMAGE = "image" # A message subtype, an image to display.
AUDIO = "audio" # A message subtype, an audio clip to play.
FILE = "file" # A message subtype, a downloadable file.
CARD = "card" # A message subtype, a box with a button to go to a website.
ALL = "all" # A message subtype, any message.
CUSTOM = "custom" # A message subtype, custom messages.
IGNORE = "ignore" # An option for how to handle multiple services using the same channel ID. This one is polite and does not steal anything.
UNBIND = "unbind" # An option for how to handle multiple services using the same channel ID. This one is vengeful, stealing a channel but not using it.
INCLUDE = "include" # An option for how to handle multiple services using the same channel ID. This one is greedy and steals channels.
DROPDOWN = "dropdown" # An option for a button component, allowing the user to choose between one of several options.
TEXT = "text" # An option for a button component, allowing the user to enter thier text.
TEXTBOX = "textbox" # An option for a button component, allowing the user to enter multiple lines.
NUMBER = "number" # An option for a button component, allowing the user to enter a floating point number.
PASSWORD = "password" # An option for a button component, allowing the user to enter a one-line string secretly.
INVALID ="invalid"  # An option for a button component, which does not allow the user to do much.
S3BUCKET = 'gbaaibuild0.s3.us-west-1'
IMAGE_EXTS = {'.jpe', '.jpg', '.jpeg', '.gif', '.png', '.bmp', '.ico', '.svg', '.svgz', '.tif', '.tiff', '.ai', '.drw', '.pct', '.psp', '.xcf', '.raw', '.webp', '.heic'} # Image format extensions.
AUDIO_EXTS = {'.wav', '.mp3', '.mp4', '.mp5'} # Audio format extensions used to auto-detect filetype, .mp5 became popular around 2030.


########################################### Dataclasses #############################################################
def add_str_method(cls):
  """Decorator function to make __str__ return the following format:
     "Foo(bar=1, baz='two', etc)"; only the non-default or specified fields are included.
     This works given a class to decorate.
     Returns the decorated function.
     """
  #Example from https://stackoverflow.com/questions/71344648/how-to-define-str-for-dataclass-that-omits-default-values
  def __str__(self):
    s = ', '.join(f'{field.name}={getattr(self, field.name)}'
                  for field in dataclasses.fields(self)
                  if getattr(self, field.name) != field.default)
    ty = 'moobius.'+type(self).__name__.split('.')[-1]
    return f'{ty}({s})'

  setattr(cls, '__str__', __str__)
  setattr(cls, '__repr__', __str__)
  return cls


@dataclass
@add_str_method
class InputComponent:
    """Describes pop-up menus inside of buttons. Such buttons have "componetns" as a list of InputComponent.
    Not used if the button does not contain a pop-up menu."""
    label: str # Also uses as the app-specified ID of the component.
    type: str # What kind of box the user sees; types.TEXT | types.DROPDOWN | types.TEXTBOX
    required: Optional[bool]=False # Is the user forced to use it?
    placeholder: Optional[str]=None # A hint to the user.
    choices: Optional[list[str]]=None # What options are available, if the type is types.DROPDOWN.


@dataclass
@add_str_method
class BottomButton:
    """Buttons appearing at the bottom of pop-up menus."""
    id: str # The app-specified ID of the button that was pressed.
    text: str # The button text as shown in the screen.
    submit: bool # True to submit the button press, False to cancel and not submit anything to the service.


@dataclass
@add_str_method
class Dialog:
    title:str='Dialog' # The title on top of the dialog box.
    components: Optional[list[InputComponent]]=None # Each one is a place where the user selects or enters something.
    bottom_buttons: Optional[list[BottomButton]]=None # Bottom buttons.


@dataclass
@add_str_method
class Button:
    """A description of a button. These buttons appear above the chat-box."""
    button_id: str # The app-specified ID of the button that was pressed.
    button_text: str # The text which appears in the browser.
    dialog: Optional[Dialog]=None # If the button opens up a dialog box


@dataclass
@add_str_method
class ClickArgument:
    """A button click argument."""
    label: str # A reminder of what label was clicked on.
    value: str # The value clicked on.
    filename: Optional[str]=None # A filename associated with the argument's label.


@dataclass
@add_str_method
class ButtonClick:
    """A description of a button click. Who clicked on which button.
    And what component they picked, if the button opens a pop-up menu."""
    button_id: str # The Button ID this applies to.
    channel_id: str # What channel the user was in when the pressed the button.
    sender: str # The Character ID of who clicked the button. Can be a real user or an agent.
    arguments: Optional[list[ClickArgument]]=None # What settings the user choose (for buttons that open a pop-up menu).
    subtype: Optional[str]=BUTTON_CLICK # Identifies it as a button click.
    labels: Optional[list[str]]=None # A reminder of what each argument means.
    bottom_button_id:Optional[str] = None # For buttons that appear at the bottom.
    context:Optional[dict] = None # Rarely used metadata.
    button_type: Optional[str] = None # What kind of button was pressed (rarely used).


@dataclass
@add_str_method
class SimpleAction:
    """Join, leave, and refresh actions (refresh not technically an action, but has the same data)."""
    subtype: str # Subtypes are 'join', 'leave', etc.
    channel_id: str # The channel that the user performed the action in.
    sender: str # The user id.
    context:Optional[dict] = None # Rarely used metadata.


@dataclass
@add_str_method
class MenuItem:
    """One element of a right-click menu. The full menu is described by a list of these elements."""
    menu_item_id: str # The app-specified ID of the Item.
    menu_item_text: str # What text to show in the browser.
    message_subtypes: str | list[str] # What message types will open the menu. ["text","file", etc].
    dialog: Optional[Dialog] = None # If this menu item opens up a dialog box when clicked.


@dataclass
@add_str_method
class MessageContent:
    """The content of a message. Most messages only have a single non-None item; for example "text" messages only have a "text" element.
    The exteption is "card" messages; they have links, title, and buttons."""
    text: Optional[str] = None # The string (for "text" messages).
    path: Optional[str] = None # The URL (for any non-text message).
    size: Optional[int] = None # The size in bytes, used for downloadable "file" messages only.
    filename: Optional[str] = None # The filename to display, used for downloadable "file" messages only.
    link: Optional[str] = None # The URL, used for "card" messages which have a clickable link.
    title: Optional[str] = None # The title shown, used for "card" messages which have a clickable link.
    button: Optional[str] = None # The text of the button shown, used for "card" messages which have a clickable link.


@dataclass
@add_str_method
class MenuItemClick:
    """A description of a menu right-click. Includes a "copy" of the message that was clicked on."""
    menu_item_id: str # The MenuItem ID that this click applies to.
    message_subtype: str # The kind of message clicked on, 'text', 'image', 'audio', 'file', or 'card'.
    message_content: MessageContent # The content of the message that was clicked on (note that messages don't have a message content field, they have a content field instead, which is different from this).
    channel_id: str # The channel the user was in when they clicked the message.
    sender: str # The Character ID of the user or agent who clicked the message.
    message_id: Optional[str]=None # The platform-generated ID of which message was clicked on (rarely used).
    arguments: Optional[list[ClickArgument]]=None # What sub-menu settings, if the menu element clicked on has a sub-menu.
    bottom_button_id: Optional[str]=None # For the bottom buttons, if there is a dialog and it has any.
    context:Optional[dict]=None # Metadata rarely used.
    subtype:Optional[str]=MENU_ITEM_CLICK # Identifies it as a menu item click.


@dataclass
@add_str_method
class CanvasItem:
    """A description of a canvas element. The full canvas description is a list of these elements."""
    text: Optional[str] = None # The text displayed.
    path: Optional[str] = None # The URL of the displayed image.


@dataclass
@add_str_method
class View:
    """An unused feature, for now."""
    character_ids: list[str] # List of Character IDs.
    button_ids: list[str] # List of Button ids.
    canvas_id: str # The platform-generated Canvas ID.


@dataclass
@add_str_method
class Group:
    """A group of users. Only to be used internally."""
    group_id: str # The platform-generated Group ID, used internally to send messages.
    character_ids: list[str] # A list of character ids who belong to this group.


@dataclass
@add_str_method
class MessageBody:
    """A message. Contains the content as well as who, when, and where the message was sent."""
    subtype: str # What kind of message it is; "text", "image", "audio", "file", or "card".
    channel_id: str # The Channel ID of the channel the message was sent in.
    content: MessageContent # The content of the message.
    timestamp: int # When the message was sent.
    recipients: list[str] # The Character IDs of who the message was sent to.
    sender: str # The Character ID of who sent the message. Removed in the Aug 2024 change I think.
    message_id: str | None # The platform-generated ID of the message itself. Rarely used.
    context:Optional[dict]=None # Metadata that is rarely used.


@dataclass
@add_str_method
class ChannelInfo:
    """A decription of an update for an old, rarely-used feature."""
    channel_id: str # The Channel ID of this channel.
    channel_name: str # The name of the channel, as appears in the list of channels.
    channel_description: str # A description that ideally should give information about what the channel is about.
    channel_type: str # An enum with "dcs", "ccs", etc. Rarely used.


@dataclass
@add_str_method
class CopyBody:
    """Used internally for the on_copy_client() callback. Most CCS apps do not need to override the callback."""
    request_id: str # Just a platform-generated ID to differentiate different copies.
    origin_type: str # What kind of data this copy comes from.
    status: bool # Rarely used. Usually True.
    context:Optional[dict]=None # Rarely used metadata.


@dataclass
@add_str_method
class Payload:
    """A description of a payload received from the websocket. Used internally by the Moobius.handle_received_payload function."""
    type: str # The kind of payload, used internally to route the payload to the correct callback function.
    request_id: Optional[str] # A platform-generated ID to differentiate payloads.
    user_id: Optional[str] # The Character ID of who dispatched this payload.
    body: MessageBody | ButtonClick | CopyBody | MenuItemClick | Any # The body of the payload.


@dataclass
@add_str_method
class Character:
    """A description (name, id, image url, etc) of a real or puppet user."""
    character_id: str # The platform-generated ID of the character. Both for real and puppet users.
    name: str # The name as appears in the group chat.
    avatar: Optional[str] = None # The image the character has.
    description: Optional[str] = None # Information about who this Character is.
    character_context: Optional[dict] = None # Rarely used metadata.


@dataclass
@add_str_method
class StyleItem:
    """A description of a visual style element. The full visual style description is a list of these elements."""
    widget: str # The type of widget. Typically "CANVAS" but other widgets.
    display: str # Is it visible? "invisible", "visible", or "highlight"
    expand: Optional[bool] = None # Should the canvas be expanded? Only used for visible.
    button_id: Optional[str] = None # What button does this apply to?
    text: Optional[str] = None # What text, if any, does this apply do?


@dataclass
@add_str_method
class UpdateItem:
    """A single update of something. A description of an update is a list of these elements.
    Most fields are None, only one is non-None at a given time."""
    character: Character | None # The new Character. Only used if a character is bieng updated.
    button: Button | None # The new Button. Only used if a Button is bieng updated.
    channel_info: ChannelInfo | None # The new ChanelInfo. Only used if a Channel is bieng updated.
    menu_item: MenuItem | None # The new MenuItem. Only used if the right-click menu is bieng updated.
    canvas_item: CanvasItem | None # The new CanvasItem. Only used if the Canvas is bieng updated.
    style_item: StyleItem | None # The new StyleItem. Only used if an element's look and feel is bieng changed.


@dataclass
@add_str_method
class UpdateBody:
    """
    A description of an update. Includes update elements as well as who sees the update.
    Used for on_update_xyz callbacks. Not used for the send_update functions.
    This is sent to agents to notify them that something that they can "see" has been updated.
    """
    subtype:str # What is bieng updated, route the Update to the correct callback function. Such as 'update_characters', 'update_channel_info', 'update_canvas', 'update_buttons', 'update_style', etc.
    channel_id:str # The Channel ID of the channel this Update is in.
    content: list[UpdateItem] # The list of indivual changes in this update.
    recipients:list[str] # The list of Character IDs of who sees this update.
    group_id: Optional[str]=None # The Group ID of the group of users/agents who see this update.
    context:Optional[dict]=None # Rarely used metadata.


@dataclass
@add_str_method
class UserInfo:
    """A description of a user profile.
    This is sent to agents so that they can learn about "themselves"."""
    avatar:str # The URL to the image shown in the group chat.
    description:str # A description of who this user is.
    name:str # The user's name.
    email:str # The user's email.
    email_verified:str # Did the user check thier email and click that link?
    user_id:str # The platform-generated Character ID for this user.
    system_context:Optional[dict]=None # Rarely-used metadata.


############################# Type-standardization functions. #################################
def recv_tmp_convert(f_name, the_data):
    """Tmp function which makes small changes to couple kinds of inbound payloads. Accepts the request_name, and a dict x. Returns the modified x."""
    if f_name == 'on_message_down':
        if 'recipients' not in the_data:
            the_data['recipients'] = ['<Unknown>']
    return the_data


def assert_strs(*strs):
    """Given a list. Returns True. Raises an Excpetion if the assert fails."""
    for i, s in enumerate(strs):
        if type(s) is not str:
            raise Exception(f"Element[{i}] is not a str")
    return strs


def limit_len(txt, n): # Not 100% sure which module this function belongs in.
    """Given the text and the maximum length, returns a string with a limited length.
    If the string is shortened "...<number of> chars" will be shown at the end."""
    if len(txt)>n:
        txt = txt[0:n]+'...'+str(len(txt))+' chars'
    return txt


def to_char_id_list(c):
    """
    Converts the input to a list of character_ids, designed to accept a wide range of inputs.
    Parameters:
      c: This can be one of many things:
        A Character (returns it's id as one-element list).
        A string (assumes it's an id wraps it into a one element list).
        A list of Characters (extracts the ids).
        A list of strings (returns a copy of the list).
        A mixed character and string list.

    Returns the list of character ids.
    """
    if type(c) is str or type(c) is Character:
        c = [c]
    c = [ch.character_id if type(ch) is Character else ch for ch in c] # Convert Character objects to IDs.
    return c


def normalize_message(message, channel_id=None, sender=None, recipients=None, subtype=None, len_limit=None, file_display_name=None, context=None,
                      text=None, link=None, title=None, button=None, path=None):
    """
    Normalizes a message to a format that the websocket client understands. See sdk.send_message() for more details.
    Note: No file uploading nor interaction is performed. These steps are to be performed in Moobius.send_message().
    This function is generally for internal use.

    Accepts a message, a channel_id, a sender, the recipients, a subtype, the optional len_limit, a file_display_name, the context, the text, the optional link, the optional title, the card button, and the file/url path.
    All arguments except message are optional.
    Returns a normalized message as a dict but with a MessageContent inside of it.
    """

    def _get_file_message_content(file_path, file_display_name=None, subtype=None):
        """Converts a file_path into a MessageContent object. Accepts the filepath/url, the name to show in the chat, and the message subtype. Returns the MessageContent."""
        if not file_path:
            file_path = f"https://{S3BUCKET}.amazonaws.com/LogoLight.jpg"
        if type(file_path) is not str:
            file_path = file_path.as_posix() # For pathlib.paths.
        size = None
        if os.path.exists(file_path):
            size = os.stat(file_path).st_size
        ext = '.'+file_path.lower().split('.')[-1]
        filename = file_display_name if file_display_name else file_path.replace('\\','/').split('/')[-1]
        if not subtype:
            subtype = IMAGE if ext in IMAGE_EXTS else (AUDIO if ext in AUDIO_EXTS else FILE)
        return MessageContent(filename=filename, size=size, path=file_path), subtype

    if file_display_name:
        if not subtype:
            subtype = FILE
        if subtype != FILE:
            logger.warning(f'file_display_name is set, but the subtype is set to {subtype} not types.FILE')

    # Part 1: Convert to dict except for the internal MessageContent.
    if type(message) is MessageBody:
        message = dataclasses.asdict(message)
    elif type(message) is str:
        if not subtype or subtype == TEXT:
            message = {'subtype':TEXT, 'content':MessageContent(text=message)}
        else:
            message = message.strip()
            mcontent, subtype = _get_file_message_content(message, file_display_name=file_display_name, subtype=subtype)
            message = {'subtype':subtype, 'content':mcontent}
    elif type(message) in [pathlib.Path, pathlib.PosixPath, pathlib.PurePath, pathlib.PurePosixPath, pathlib.PureWindowsPath, pathlib.WindowsPath]:
        mcontent, subtype = _get_file_message_content(message, file_display_name=file_display_name, subtype=subtype)
        message = {'subtype':subtype, 'content':mcontent}
    elif type(message) is dict:
        message = message.copy()
    else:
        message = str(message)

    # Additional normalization steps:
    if 'link' in message and 'button' in message and 'text' in message:
        if not subtype:
            subtype = CARD
        message['content'] = {**message, **(message['content'] if type(message.get('content')) is dict else {})} # Convert contents of a card into an actual card.
    for ky in ['text', 'button', 'link', 'title']:
        if ky in message:
            del message[ky]
    if 'recipients' not in message and recipients is None:
        logger.error('None "recipients" (None as in not an empty list) but "recipients" not specified by the message. This may indicate that recipients was unfilled.')
    if 'content' not in message:
        logger.error('Dict/MessageBody message with no "content" specified.')
        message['content'] = MessageContent()
    if 'message_id' in message: #message['message_id'] = str(uuid.uuid4()) # The CCS does not generate an ID.
        del message['message_id']
    if 'timestamp' in message: # The timestamp will be updated to the current time.
        del message['timestamp']
    if type(message['content']) is dict:
        message['content'] = MessageContent(**message['content'])

    # Part 2: Use the arguments to update the message:
    if text:
        message['content'].text = text
    if link:
        message['content'].link = link
    if title:
        message['content'].title = title
    if button:
        message['content'].button = button
    if path:
        message['content'].path = path
    if channel_id:
        message['channel_id'] = channel_id
    if sender:
        if type(sender) is Character:
            sender = sender.character_id
        message['sender'] = sender
    if recipients:
        message['recipients'] = recipients
    if context:
        message['context'] = context
    if message.get('recipients'):
        if len_limit and message['content'].text:
            message['content'].text = limit_len(message['content'].text, len_limit)
    if subtype:
        message['subtype'] = subtype
    return message


def as_update_body(payload_body):
    """Given a payload body, returns the UpdateBody version of it."""
    subty = payload_body['subtype']
    content0 = payload_body['content'] # This dict needs to be converted into a list of UpdateItem's
    empty_elem_dict = {'character':None, 'button':None, 'channel_info':None, 'canvas_item':None, 'style_item':None, 'menu_item':None}
    def _make_elem(d):
        """Accepts a dict with the update information. Returns the UpdateItem with defaults filled in if they are not in the dict."""
        return UpdateItem(**{**empty_elem_dict, **d})
    content = []
    if subty == UPDATE_CHARACTERS:
        content = [_make_elem({'character':Character({**c, **c['character_context']})}) for c in content0['characters']]
    elif subty == UPDATE_CHANNEL_INFO:
        content = [_make_elem({'channel_info':ChannelInfo(content0)})]
    elif subty == UPDATE_CANVAS:
        content = [_make_elem({'canvas_item':CanvasItem(**ce)}) for ce in content0]
    elif subty == UPDATE_MENU:
        content = [_make_elem({'menu_item':MenuItem(**ce)}) for ce in content0]
    elif subty == UPDATE_BUTTONS:
        buttons = []
        for b in content0:
            if b.get('arguments'): # For some reason this wasn't bieng converted to a InputComponent data.
                b['arguments'] = [InputComponent(**a) for a in b['arguments']]
            buttons.append(Button(**b))
        content = [_make_elem({'button':b}) for b in buttons]
    elif subty == UPDATE_STYLE:
        content = [_make_elem({'style_item':StyleItem(**b)}) for b in content0]
    else:
        logger.error(f'Unknown recieved update subtype, cannot encode: {subty}')
        content = [] # Unknown.

    if 'recipients' not in payload_body:
        payload_body = payload_body.copy()
        payload_body['recipients'] = None
    return UpdateBody(**{**payload_body, **{'content':content}})


def payload_as_dict(payload_type, payload_body, client_id, the_uuid):
    """Converts a payload to a dict. Accepts the payload type, the Payload object or dict-valued payload, the client/service id, and any unique uuid. Returns the payload as a dict."""
    if isinstance(payload_body, dict):
        payload_dict = {
            'type': payload_type,
            'request_id': the_uuid,
            'character_id': client_id,
            'body': payload_body
        }
    else: # Need to wrap non-dataclasses into a dataclass, in this case Payload, in order to use asdict() on them.
        payload_obj = Payload(
            type=payload_type,
            request_id=the_uuid,
            user_id=client_id,
            body=payload_body
        )
        try:
            payload_dict = dataclasses.asdict(payload_obj)
        except Exception as error_e: # Track down those pickle errors!
            _pr = logger.error
            print("asdict FAILURE on", payload_type, payload_body, error_e)
            try:
                dataclasses.asdict(payload_body)
                _pr('HUH? The payload body CAN be dictified?')
            except:
                pass
            for k, v in payload_body.__dict__.items():
                if type(v) in [str, int, bool, float]:
                    _pr('Elemetary type, no problem pickling:', k, v)
                else:
                    try:
                        dataclasses.asdict(Payload(type=payload_type, request_id=the_uuid, user_id=client_id, body=v))
                        _pr('No problem pickling:', k, v)
                    except Exception as e:
                        _pr('UNDICTABLE part of __dict__ error:', k, 'Value is:', v, 'type is:', type(v), 'error is:', e)
            raise error_e
    if 'type' in payload_dict and payload_dict['type'] == MESSAGE_DOWN:
        payload_dict['service_id'] = client_id
    return payload_dict
