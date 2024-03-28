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
    name: str
    type: str
    optional: Optional[bool]
    values: Optional[list[str]]
    placeholder: str


@dataclass
@add_str_method
class Button: # Used for encoding Buttons, both for sending out updates and for recieving the on_update_buttons callback.
    button_id: str # An id choosen by the CCS app to identify which button was pressed.
    button_name: str
    button_text: str # This text appears in the browser.
    new_window: bool
    arguments: Optional[list[ButtonArgument]]=None


@dataclass
@add_str_method
class ButtonClickArgument:
    name: str
    value: str | int


@dataclass
@add_str_method
class ButtonClick: # When the user clicks on a button or a menu opened by a button.
    button_id: str
    channel_id: str
    sender: str
    arguments: list[ButtonClickArgument]
    context: dict # Rarely used by CCS apps.


@dataclass
@add_str_method
class ContextMenuElement: # A single item in a context menu. This will likely be expanded upon with more features.
    item_name: str # How it appears.
    item_id: str # An id choosen by the CCS app to identify which choice was selected.
    support_subtype: list[str] # What message types will open the context menu. ["text","file", etc].


@dataclass
@add_str_method
class MessageContent:
    text: Optional[str] = None # Used for text messages.
    path: Optional[str] = None # Used for every kind of non-text message.
    size: Optional[int] = None # Used for downloadable files only.
    filename: Optional[str] = None # Used for downloadable files only (the display filename).
    link: Optional[str] = None # For "card" messages
    title: Optional[str] = None # For "card" messages
    button: Optional[str] = None # For "card" messages
    text: Optional[str] = None # For "card" messages

@dataclass
@add_str_method
class MenuClick: # Right-click context menu.
    item_id: str
    message_id: str
    message_subtype: str # 'text', 'image', 'audio', or 'file'
    message_content: MessageContent
    channel_id: str
    sender: str
    recipients: list[str]
    context: dict # Rarely used by CCS apps.


@dataclass
@add_str_method
class CanvasElement: # Updates to the Canvas are lists of CanvasElements.
    text: Optional[str] = None
    path: Optional[str] = None


@dataclass
@add_str_method
class View: # TODO: What is this for?
    character_ids: list[str]
    button_ids: list[str]
    canvas_id: str


@dataclass
@add_str_method
class Group:
    group_id: str
    character_ids: list[str]


@dataclass
@add_str_method
class MessageBody:
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
    subtype: str
    channel_id: str
    sender: str
    context: Optional[dict]


@dataclass
@add_str_method
class ChannelInfo:
    channel_id: str
    channel_name: str
    context: dict


@dataclass
@add_str_method
class Copy:
    request_id: str
    origin_type: str
    status: bool
    context: dict


@dataclass
@add_str_method
class Payload:
    type: str
    request_id: Optional[str]
    user_id: Optional[str]
    body: MessageBody | ButtonClick | Action | Copy | MenuClick | Any


@dataclass
@add_str_method
class Character:
    character_id: str
    name: str
    avatar: str
    description: str
    character_context: dict # Rarely used by CCS apps.


@dataclass
@add_str_method
class ChannelInfo:
    channel_id: str
    channel_name: str
    channel_description: str
    channel_type: str # dcs, ccs, etc.


@dataclass
@add_str_method
class StyleElement: # As of 2024_3_15 this is a work-in-progress on the Platform. When the Platform is updated this dataclass will be updated.
    widget: str # Typically "canvas"
    display: str # "invisible", "visible"
    expand: str # "false", "true" (strings not bools! other options such as "force_true" may be added).


@dataclass
@add_str_method
class UpdateElement: # Used for on_update_xyz callbacks. Not used for send_update functions.
    character: Character | None # These fields will be None if they are not applicable to the type of update.
    button: Button | None # Only one of these is non-None at any given time.
    channel_info: ChannelInfo | None
    context_menu_element: ContextMenuElement | None
    canvas_element: CanvasElement | None
    style_element: StyleElement | None


@dataclass
@add_str_method
class Update: # Used for on_update_xyz callbacks. Not used for send_update functions.
    subtype:str # 'update_characters' 'update_channel_info' 'update_canvas' 'update_buttons' 'update_style'
    channel_id:str
    content: list[UpdateElement]
    context:dict # Rarely used by CCS apps.
    recipients:list[str] # A group id is converted into a list if character ids.
    group_id: Optional[str]=None


@dataclass
@add_str_method
class UserInfo:
    avatar:str
    description:str
    name:str
    email:str
    email_verified:str #"false" or "true"
    user_id:str
    system_context:Optional[dict]=None # Rarely used by CCS apps.
