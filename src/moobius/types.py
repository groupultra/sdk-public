# Common datatypes are encoded as dataclasses which behave like dicts but have fixed keys.
# In addition, string literals are encoded. This avoids "magic strings" appearing everywhere in the code.

import dataclasses, time
from dataclasses import dataclass
from typing import Optional, Any

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
JOIN_CHANNEL = "join" # A subtype of an action payload, the user pastes in the ID and joins.
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
IGNORE = "ignore" # An option for how to handle multiple services using the same channel ID. This one is polite and does not steal anything.
UNBIND = "unbind" # An option for how to handle multiple services using the same channel ID. This one is vengeful, stealing a channel but not using it.
INCLUDE = "include" # An option for how to handle multiple services using the same channel ID. This one is greedy and steals channels.
DROPDOWN = "dropdown" # An option for a button component, allowing the user to choose between one of several options.
TEXT = "text" # An option for a button component, allowing the user to enter thier text.
TEXTBOX = "textbox" # An option for a button component, allowing the user to enter multiple lines.
IMAGE_EXTS = {'.jpe', '.jpg', '.jpeg', '.gif', '.png', '.bmp', '.ico', '.svg', '.svgz', '.tif', '.tiff', '.ai', '.drw', '.pct', '.psp', '.xcf', '.raw', '.webp', '.heic'} # Image format extensions.
AUDIO_EXTS = {'.wav', '.mp3', '.mp4', '.mp5'} # Audio format extensions used to auto-detect filetype, .mp5 became popular around 2030.


def _send_tmp_convert(f_name, x):
    """Tmp function which makes small changes to a couple kinds of outbound payloads. Accepts the request_name, and a dict x. Returns x."""
    if f_name == 'on_button_click' or f_name == 'on_menu_click':
        args1 = []
        for a in x['body']['arguments']:
            if type(a) in [str, int, float]:
                a = {'label':'...', 'value':a}
            args1.append(a)
        x['body']['argumnets'] = args1
    return x


def _recv_tmp_convert(f_name, the_data):
    """Tmp function which makes small changes to couple kinds of inbound payloads. Accepts the request_name, and a dict x. Returns the modified x."""
    if f_name in ['on_button_click', 'on_menu_item_click']:
        args1 = []
        for a in the_data.get('arguments', []):
            args1.append(a if type(a) is str else a['value'])
        the_data['arguments'] = args1
    if f_name == 'on_menu_item_click':
        if 'message_id' not in the_data:
            the_data['message_id'] = '<unspecified message id>'
    return the_data


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
    optional: Optional[bool] # Can the user skip it?
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
class ButtonClick:
    """A description of a button click. Who clicked on which button.
    And what component they picked, if the button opens a pop-up menu."""
    button_id: str # The Button ID this applies to.
    channel_id: str # What channel the user was in when the pressed the button.
    sender: str # The Character ID of who clicked the button. Can be a real user or an agent.
    arguments: Optional[list[str]]=None # What settings the user choose (for buttons that open a pop-up menu).
    subtype: Optional[str]=BUTTON_CLICK # Identifies it as a button click.
    labels: Optional[list[str]]=None # A reminder of what each argument means.
    bottom_button_id:Optional[str] = None # For buttons that appear at the bottom.
    context:Optional[dict] = None # Rarely used metadata.
    button_type: Optional[str] = None # What kind of button was pressed (rarely used).


@dataclass
@add_str_method
class MenuItem:
    """One element of a right-click menu. The full menu is described by a list of these elements."""
    menu_item_id: str # The app-specified ID of the Item.
    menu_item_text: str # What text to show in the browser.
    message_subtypes: list[str] # What message types will open the menu. ["text","file", etc].
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
    message_id: str # The platform-generated ID of which message was clicked on (rarely used).
    message_subtype: str # The kind of message clicked on, 'text', 'image', 'audio', 'file', or 'card'.
    message_content: MessageContent # The content of the message that was clicked on (note that messages don't have a message content field, they have a content field instead, which is different from this).
    channel_id: str # The channel the user was in when they clicked the message.
    sender: str # The Character ID of the user or agent who clicked the message.
    arguments: Optional[list[str]]=None # What sub-menu settings, if the menu element clicked on has a sub-menu.
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


#@dataclass
#@add_str_method
#class ActionBody:
#    """A description of a generic task performed by a user. Actions with different subtypes are routed to different callbacks."""
#    subtype: str # The subtype of the action. Used internally to route the action to the correct callback function.
#    request_id: str
#    user_id: str # The user who sent the action.


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
class RefreshBody:
    """A refresh from the user's browser."""
    channel_id: str # The Channel ID of this channel.
    sender: str # Whose browser sent the refresh.
    subtype:Optional[str]=REFRESH # Identifies it as a refresh.
    context:Optional[dict]=None # Rarely used metadata.


@dataclass
@add_str_method
class JoinBody:
    """An action body for joining a channel."""
    channel_id: str # The Channel ID of th joined channel.
    sender: str # Whose browser sent the join command.
    subtype:Optional[str]=JOIN_CHANNEL # Identifies it as a join channel.
    context:Optional[dict]=None # Rarely used metadata.


@dataclass
@add_str_method
class LeaveBody:
    """An action body for leaving a channel."""
    channel_id: str # The Channel ID of th joined channel.
    sender: str # Whose browser sent the join command.
    subtype:Optional[str]=LEAVE_CHANNEL # Identifies it as a leave channel.
    context:Optional[dict]=None # Rarely used metadata.


@dataclass
@add_str_method
class Payload:
    """A description of a payload received from the websocket. Used internally by the Moobius.handle_received_payload function."""
    type: str # The kind of payload, used internally to route the payload to the correct callback function.
    request_id: Optional[str] # A platform-generated ID to differentiate payloads.
    user_id: Optional[str] # The Character ID of who dispatched this payload.
    body: MessageBody | ButtonClick | CopyBody | MenuItemClick | RefreshBody | Any # The body of the payload.


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
