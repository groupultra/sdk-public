# Common dataclasses.

import dataclasses
from dataclasses import dataclass
from typing import Optional, Any

SERVICE = "service"
FETCH_CHARACTERS = "fetch_characters"
FETCH_BUTTONS = "fetch_buttons"
FETCH_CANVAS = "fetch_canvas"
JOIN_CHANNEL = "join_channel"
LEAVE_CHANNEL = "leave_channel"
FETCH_CONTEXT_MENU = "fetch_context_menu"
FETCH_CHANNEL_INFO = "fetch_channel_info"
UPDATE = "update"
UPDATE_CHARACTERS = "update_characters"
UPDATE_CHANNEL_INFO = "update_channel_info"
UPDATE_CANVAS = "update_canvas"
UPDATE_BUTTONS = "update_buttons"
UPDATE_STYLE = "update_style"
UPDATE_CONTEXT_MENU = "update_context_menu"
USER_LOGIN = "user_login"
SERVICE_LOGIN = "service_login"
HEARTBEAT = "heartbeat" # Action subtypes.
ROGER = "roger"
COPY = "copy"
IGNORE = "ignore"
UNBIND = "unbind"
INCLUDE = "include"
BUTTON_CLICK = "button_click"
MENU_CLICK = "menu_click"
MESSAGE_UP = "message_up"
MESSAGE_DOWN = "message_down"
ACTION = "action"
TEXT = "text" # Message subtypes.
IMAGE = "image"
AUDIO = "audio"
FILE = "file"
CARD = "card"
IMAGE_EXTS = {'.jpe', '.jpg', '.jpeg', '.gif', '.png', '.bmp', '.ico', '.svg', '.svgz', '.tif', '.tiff', '.ai', '.drw', '.pct', '.psp', '.xcf', '.raw', '.webp', '.heic'}
AUDIO_EXTS = {'.wav', '.mp3', '.mp4', '.mp5'} # .mp5 became popular around 2030.


def add_str_method(cls):
  """Decorator function to make __str__ return the following format:
     "Foo(bar=1, baz='two', etc)"; only the non-default fields are included."""
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
class ButtonArgument:
    """For buttons that open pop-up menus. Such buttons have "arguments" as a list of ButtonArguments."""
    name: str
    type: str
    optional: Optional[bool]
    values: Optional[list[str]]
    placeholder: str


@dataclass
@add_str_method
class Button:
    """A description of a button. These buttons appear above the chat-box."""
    button_id: str # An id choosen by the CCS app to identify which button was pressed.
    button_name: str
    button_text: str # This text appears in the browser.
    new_window: bool
    arguments: Optional[list[ButtonArgument]]=None


@dataclass
@add_str_method
class ButtonClickArgument:
    """Part of the callback of pop-up menu opening buttons. Such buttons, when clicked, return a ButtonClick with a list of ButtonClickArguments.
    Also used, uncommonly, for context-menu clicks which use pop-up submenus."""
    name: str
    value: str | int


@dataclass
@add_str_method
class ButtonClick:
    """A description of a button click. Lists the button's id as well as any information they entered (if the button opens a pop-up menu)."""
    button_id: str
    channel_id: str
    sender: str
    arguments: list[ButtonClickArgument]
    context: dict # Rarely used by CCS apps.


@dataclass
@add_str_method
class ContextMenuElement:
    """A description of a context-menu is a list of these elements."""
    item_name: str # How it appears.
    item_id: str # An id choosen by the CCS app to identify which choice was selected.
    support_subtype: list[str] # What message types will open the context menu. ["text","file", etc].
    new_window: Optional[bool] = False
    arguments: Optional[list[ButtonArgument]] = None

@dataclass
@add_str_method
class MessageContent:
    """The content of a message. Most messages only have a single non-None item; for example "text" messages only have a "text" element.
    Except "card" messages; they have links, title, and buttons."""
    text: Optional[str] = None # Used for text messages.
    path: Optional[str] = None # Used for every kind of non-text message.
    size: Optional[int] = None # Used for downloadable files only.
    filename: Optional[str] = None # Used for downloadable files only (the display filename).
    link: Optional[str] = None # For "card" messages
    title: Optional[str] = None # For "card" messages
    button: Optional[str] = None # For "card" messages


@dataclass
@add_str_method
class MenuClick:
    """A description of a context menu right-click. Includes a "copy" of the message that was clicked on."""
    item_id: str
    message_id: str
    message_subtype: str # 'text', 'image', 'audio', or 'file'
    message_content: MessageContent
    channel_id: str
    sender: str
    recipients: list[str]
    context: dict # Rarely used by CCS apps.
    arguments: Optional[list[ButtonClickArgument]] = None # If the context menu has itself menus.


@dataclass
@add_str_method
class CanvasElement:
    """A description of the canvas is a list of these elements."""
    text: Optional[str] = None
    path: Optional[str] = None


@dataclass
@add_str_method
class View:
    """An unused feature, for now."""
    character_ids: list[str]
    button_ids: list[str]
    canvas_id: str


@dataclass
@add_str_method
class Group:
    """A group of users. Only to be used internally."""
    group_id: str
    character_ids: list[str]


@dataclass
@add_str_method
class MessageBody:
    """A message. Contains the content as well as information about who and where the message was sent."""
    subtype: str
    channel_id: str
    content: MessageContent
    timestamp: int
    recipients: list[str] # The API uses a group id which is converted to/from a list.
    sender: str
    message_id: str | None
    context: dict | None # Rarely used by CCS apps.


@dataclass
@add_str_method
class Action:
    """A description of a generic task performed by a user. Actions with different subtypes are routed to different callbacks."""
    subtype: str
    channel_id: str
    sender: str
    context: Optional[dict]


@dataclass
@add_str_method
class ChannelInfo:
    """Used to descripe an update for an old, rarely-used feature."""
    channel_id: str
    channel_name: str
    channel_description: str
    channel_type: str # dcs, ccs, etc.


@dataclass
@add_str_method
class Copy:
    """Used internally for the on_copy_client() callback. Most CCS apps do not need to override the callback."""
    request_id: str
    origin_type: str
    status: bool
    context: dict


@dataclass
@add_str_method
class Payload:
    """Used internally by the Moobius.handle_received_payload function."""
    type: str
    request_id: Optional[str]
    user_id: Optional[str]
    body: MessageBody | ButtonClick | Action | Copy | MenuClick | Any


@dataclass
@add_str_method
class Character:
    """A description (name, id, image url) of a real or virtual user."""
    character_id: str
    name: str
    avatar: Optional[str] = None
    description: Optional[str] = None
    character_context: Optional[dict] = None # Rarely used by CCS apps.


@dataclass
@add_str_method
class StyleElement:
    """A description of a visual style is a list of these elements."""
    widget: str # Typically "canvas"
    display: str # "invisible", "visible"
    expand: str # "false", "true" (strings not bools! other options such as "force_true" may be added).


@dataclass
@add_str_method
class UpdateElement:
    """Each Update has a list of UpdateElements."""
    character: Character | None # These fields will be None if they are not applicable to the type of update.
    button: Button | None # Only one of these is non-None at any given time.
    channel_info: ChannelInfo | None
    context_menu_element: ContextMenuElement | None
    canvas_element: CanvasElement | None
    style_element: StyleElement | None


@dataclass
@add_str_method
class Update:
    """Used for on_update_xyz callbacks. Not used for send_update functions.
    Used by an *agent* so that they can be notified that something that they can "see" has been updated."""
    subtype:str # 'update_characters' 'update_channel_info' 'update_canvas' 'update_buttons' 'update_style'
    channel_id:str
    content: list[UpdateElement]
    context:dict # Rarely used by CCS apps.
    recipients:list[str] # A group id is converted into a list if character ids.
    group_id: Optional[str]=None


@dataclass
@add_str_method
class UserInfo:
    """Used by an *agent* so that they can find out information about themselves."""
    avatar:str
    description:str
    name:str
    email:str
    email_verified:str #"false" or "true"
    user_id:str
    system_context:Optional[dict]=None # Rarely used by CCS apps.
