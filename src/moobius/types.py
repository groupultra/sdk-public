# Common dataclasses.

import dataclasses
from dataclasses import dataclass
from typing import Optional, Any


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
    button_id: str # Button_ids are choosen by the CCS app. This is *different* from other _id fields.
    button_name: str
    button_text: str
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
class MessageContent:
    text: Optional[str] = None # Used for text messages.
    path: Optional[str] = None # Used for every kind of non-text message.
    size: Optional[str] = None # Used for downloadable files only.
    filename: Optional[str] = None # Used for downloadable files only (the display filename).


@dataclass
@add_str_method
class MenuClick: # Right-click context menu.
    item_id: str
    message_id: str
    message_subtype: str
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
    button: Button | None # Onle one of these is non-None at any given time.
    channel_info: ChannelInfo | None
    canvas: CanvasElement | None
    style: StyleElement | None


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
