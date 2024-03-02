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
class Button:
    button_id: str
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
class ButtonClick:
    button_id: str
    channel_id: str
    sender: str
    arguments: list[ButtonClickArgument]
    context: dict


@dataclass
@add_str_method
class Stage:
    stage_id: str
    stage_args: dict


@dataclass
@add_str_method
class View:
    character_ids: list[str]
    button_ids: list[str]
    stage_id: str


@dataclass
@add_str_method
class Group:
    group_id: str
    character_ids: list[str]


@dataclass
@add_str_method
class MessageContext:
    sender: str
    recipients: list[str]  # TODO: remove this field
    group_id: Optional[str]  # TODO: remove Optional


@dataclass
@add_str_method
class MessageBody:
    subtype: str
    channel_id: str
    content: dict
    timestamp: int
    recipients: list[str] # The API uses a group id which is converted to/from a list.
    sender: str
    message_id: str | None
    context: dict | None


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
    body: MessageBody | ButtonClick | Action | Copy | Any


@dataclass
@add_str_method
class CharacterContext:
    name: str
    description: str
    avatar: str


@dataclass
@add_str_method
class Character:
    character_id: str | None
    name: str | None
    character_context: CharacterContext
