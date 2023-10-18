# types.py

from dataclasses import dataclass
from typing import Optional, Any


@dataclass
class Character:
    character_id: str
    username: str
    nickname: str
    avatar: str
    description: str


@dataclass
class FeatureArgument:
    name: str
    type: str
    optional: Optional[bool]
    values: Optional[list[str]]
    placeholder: str


@dataclass
class Feature:
    feature_id: str
    feature_name: str
    button_text: str
    new_window: bool
    arguments: list[FeatureArgument]


@dataclass
class FeatureCallArgument:
    name: str
    value: str|int


@dataclass
class FeatureCall:
    feature_id: str
    channel_id: str
    arguments: list[FeatureCallArgument]
    context: dict


@dataclass
class Stage:
    stage_id: str
    stage_args: dict


@dataclass
class View:
    character_ids: list[str]
    feature_ids: list[str]
    stage_id: str


@dataclass
class Group:
    group_id: str
    character_ids: list[str]

@dataclass
class MessageContext:
    sender: str
    recipients: list[str]  # todo: remove this field
    group_id: Optional[str]  # todo: remove Optional


@dataclass
class MessageUp:
    subtype: str
    content: dict
    channel_id: str
    timestamp: int
    recipients: list[str]
    msg_id: str
    context: MessageContext
    content: dict
    

@dataclass
class Action:
    subtype: str
    channel_id: str
    sender: str
    context: Optional[dict]


@dataclass
class ChannelInfo:
    channel_id: str
    channel_name: str
    context: dict



@dataclass
class Copy:
    request_id: str
    origin_type: str
    status: bool
    context: dict



@dataclass
class Message:
    type: str
    body: MessageUp|FeatureCall|Action|Copy|Any



@dataclass
class CharacterContext:
    nickname: str
    description: str
    avatar: str


@dataclass
class Character:
    user_id: str
    user_context: CharacterContext

    