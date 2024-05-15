# Ensures that the Socket and the HTTPAPI are acceptable for the Platform. No one wants Internal Server Error.
import json
from loguru import logger
from moobius import types

check_asserts = True # Can be turned to False in order to avoid assertion errors.
allow_temp_modifications = True # TODO: There is some extra stuff sent to the socket. It probably can be safely removed.
                                # Before removing it, this fn will remove it from (a copy of) the data.

class PlatformAssertException(Exception):
    pass


def types_assert(ty, **kwargs):
    """Asserts that every one of kwargs is type ty, giving an error message if there is a mismatch.
    types_assert(str, foo=foo, bar=bar)"""
    if not check_asserts:
        return True
    for k, v in kwargs.items():
        if type(v) is not ty:
            raise PlatformAssertException(f'Value {k} is a {type(v)} not a {ty}')
    return True


def structure_assert(gold, green, base_message, path=None):
    """
    Asserts whether "green" follows the data-structure in "gold".

    Parameters:
      gold: The datastructure to match. This is a nested datastructure with the following elements.
        Lists: These can be any length in the green data structure, including zero.
        Tuples: These impose a fixed length with the gold and green corresponding 1:1.
        Dicts: These must have the exact same keys gold vs green (like tuples not like lists).
        Bools: Must be True or False, not None.
        Ints: Must be ints in the green.
        Floats: Must be numbers in the green (ints or floats).
          Note: The Platform expects many number literals to be strings.
        Strings: Must be strings in the green. They do not have to match.
        Functions: Used for more complex cases.
          calls f(green, base_message, path). f can in turn call structure_assert or other functions.
      green: The datastructure (before conversion to a JSON string) that must fit the gold datastructure.
      base_message: Give some useful information as to the error message!
      path=None: The path within the datastructure. None will be [].

    Returns: True if the assert passes.
    Raises: PlatformAssertException if the assert fails, using the base_message.
    """
    if not check_asserts:
        return True
    if not path:
        path = []

    ty = type(gold)
    err1 = None
    if ty is tuple and len(gold) != len(green):
        err1 = '(tuple length mismatch)'
    elif ty is list:
        if len(gold) != 1:
            raise Exception('Error in template. Lists must be length 1.')
        else:
            if type(green) not in [list, tuple]:
                raise PlatformAssertException(f'Not a list when expected to be a list; {base_message}; where={path}')
            out = True
            for i in range(len(green)):
                out = out and structure_assert(gold[0], green[i], base_message, path=path+[i])
            return out
    elif ty is dict:
        kys_gold = set(gold.keys())
        if type(green) is not dict:
            raise PlatformAssertException(f'Not a dict when expected to be a dict; {base_message}; where={path}')
        kys_green = set(green.keys())
        missing = kys_gold - kys_green
        extra = kys_green - kys_gold
        if len(missing) > 0:
            err1 = f"(missing keys: {list(missing)})"
        elif len(extra) > 0:
            err1 = f"(extra keys: {list(extra)})"
        else:
            out = True
            for k in green.keys():
                out = out and structure_assert(gold[k], green[k], base_message, path=path+[k])
            return out
    elif ty in [int, float, str, bool]:
        ty_green = type(green)
        if ty_green != ty and not (ty_green is int and ty is float):
            err1 = f"(leaf type mismatch: gold={ty}, green={ty_green})"
    elif callable(gold): # Functions can have any uer-defined behavior.s
        return gold(green, base_message, path)
    else:
        raise Exception(f'Error in template. Unrecognized template type: {ty}')
    if err1:
        raise PlatformAssertException(f'{err1}; {base_message}; where={path}')
    else:
        return True


def min_subset_dict(min_keys, dtemplate):
    """Creates a template function that will not error on missing keys unless missing keys are in min_keys."""
    dtemplate = dtemplate.copy() # Not sure if necessary.
    def t_fn(d, base_message, path):
        for k in min_keys:
            if k not in dtemplate:
                raise PlatformAssertException(f'Missing key {k}; {base_message}; where={path}')
        out = True
        for k in d.keys():
            if k not in dtemplate:
                raise PlatformAssertException(f'Extra key {k}; {base_message}; where={path}')
            out = out and structure_assert(dtemplate[k], d[k], base_message, path=path+[k])
        return out
    return t_fn

######################### Temporary modifications (TODO: Get rid of once not working) ##########################

def temp_modify(socket_request):
    """Sometimes the request has extra stuff. This function removes it so it works.
    But TODO remove extra stuff and test."""
    if not allow_temp_modifications:
        return socket_request
    socket_request = socket_request.copy()
    if 'body' in socket_request:
        socket_request['body'] = socket_request['body'].copy()

    if socket_request['type'] == 'button_click':
        if 'sender' in socket_request['body']:
            del socket_request['body']['sender']
    if socket_request['type'] == 'message_up':
        if 'service_id' in socket_request:
            del socket_request['service_id']
    if socket_request['type'] == 'update':
        subty = socket_request['body']['subtype']
        if subty in ['update_buttons', 'update_canvas', 'update_style']:
            for ky in ['context', 'group_id']:
                if ky in socket_request['body']:
                    del socket_request['body'][ky]
    return socket_request

######################### Specific requests ##########################

def _style_check(style_element, base_message, path):
    """One element in a style vector. This is the most flexible."""
    template_dict = {'widget':'button1','display':'visible', 'text':'<h1>html_tags!</h1>', 'expand':'true', # Expand is a string?
                     'button_hook':{'button_id':'a.button', 'button_text':'A', 'arguments':[]}}
    template = min_subset_dict([], template_dict)
    return structure_assert(template, style_element, base_message, path)
def _context_menu_item_check(cmenu_item, base_message, path):
    if cmenu_item.get('new_window'):
        if 'arguments' not in cmenu_item:
            raise PlatformAssertException(f'context menu item with no arguments but a new_window specified; {base_message}; where={path}')
        argtemplate = [min_subset_dict(['name', 'type', 'values', 'placeholder'],
                                              {'name':'the_name', 'type':'enum', 'values':['choice1'],'placeholder':'place',
                                               'optional':False})]
        assert_so_far = structure_assert(argtemplate, cmenu_item['arguments'], base_message, path+['arguments'])
    else:
        assert_so_far = True

    # Check the non-argument pard
    cmenu_item = cmenu_item.copy()
    for k in ['new_window', 'arguments']:
        if k in cmenu_item:
            del cmenu_item[k]
    template = {'item_name':'option 1', 'item_id':'opt1','support_subtype':['txt']}
    return assert_so_far and structure_assert(template, cmenu_item, base_message, path)
def _socket_update_body_assert(b, base_message, path):
    """Many requests are updates with a body."""
    subty = b['subtype']
    template = {'subtype':'the_subtype', 'channel_id':'1234...', 'recipients':'1234...'}
    if subty=='update_characters':
        template['content'] = {'characters': '1234... group_id'}
    elif subty=='update_buttons':
        button_arg_template = min_subset_dict(['name', 'type', 'placeholder', 'optional'], # Values is optional.
                                                     {'name':'opt1', 'type':'enum', 'values':['a'], 'placeholder':'in-situ', 'optional':False})
        def _each_button(x, base_message, the_path):
            each_btn = {'button_id':'pressA', 'button_name':'pressA', 'button_text':'press this A',
                        'new_window':True, 'arguments':[button_arg_template]}
            if not x.get('new_window'):
                if 'arguments' not in x or x.get('arguments') is None: # Falsey new_window is allowed to have None or missing arguments.
                    del each_btn['arguments']
                    x = x.copy()
                    if 'arguments' in x:
                        del x['arguments']
            return structure_assert(each_btn, x, base_message, the_path)
        template['content'] = [_each_button]
    elif subty=='update_channel_info':
        template['content'] = {'channel_id':'123...', 'channel_name':'123...',
                               'context':{'channel_description':'a channel', 'channel_type':'ccs'}}
    elif subty=='update_canvas':
        template['content'] = [min_subset_dict([], {'path':'url', 'text':'see this text here.'})]
    elif subty=='update_style':
        template['content'] = [_style_check]
    elif subty=='update_context_menu':
        template['content'] = [_context_menu_item_check]
        template['context'] = {}
    elif subty=='update_characters':
        template['context'] = {}
        template['content'] = {'characters':'1234...group_id'}
    else:
        raise PlatformAssertException(f'Unrecognized subtype for an update request {subty}; {base_message}.')
    return structure_assert(template, b, base_message, path)
def _socket_message_body_assert1(b, base_message, path, is_up):
    """Both text and image messages are supported."""
    subty = b['subtype']
    template = {'subtype':'the_subtype', 'channel_id':'1234...', 'recipients':'1234... group_id',
                'timestamp':12334567, 'context':{}}
    if not is_up:
        template['sender'] = '1234...'
    if 'recipients' in b and b['recipients'] is None: # Accept None type.
        b = b.copy()
        b['recipients'] = 'noooone'
    if subty in [types.TEXT, types.IMAGE, types.AUDIO, types.FILE]:
        content = b['content'].copy()
        if not content.get('path') and subty != types.TEXT:
            raise PlatformAssertException(f'File-bearing message body has no/None path; {base_message}.')
        for k in ['text', 'path', 'filename', 'size']:
            if k in content:
                if content[k] is None:
                    pass
                elif type(content[k]) is int and k=='size':
                    pass
                elif k != 'size' and type(content[k]) is str:
                    pass
                else:
                    raise PlatformAssertException(f'Message body has invalid type for {k}: {type(content[k])}; {base_message}.')
                del content[k]
        b = b.copy()
        del b['content']
    elif subty == types.CARD:
        content = b['content'].copy()
        for k in ['link', 'button', 'text']: # 'title' may also be necessary.
            if k not in b['content']:
                raise PlatformAssertException(f'Card message is missing {k}.')
        return True
    else:
        raise PlatformAssertException(f'Unrecognized subtype for a message body: {subty}; {base_message}.')
    return structure_assert(template, b, base_message, path)
def _button_click_body_assert(b, base_message, path):
    """Some buttons have options. Some don't."""
    template = {'button_id':'button1', 'channel_id':'1234...',
                'arguments':[{'name':'category', 'value':'A'}],
                'context':{}}
    return structure_assert(template, b, base_message, path)
def _context_menuclick_body_assert(b, base_message, path):
    """Right click context menu click"""
    template = {'item_id':'item1', 'channel_id':'1234...', 'message_id':'1234...', 'message_subtype':'text/file/etc',
                'message_content':min_subset_dict([], {'text':'text!', 'image':'url'}), 'context':{}}
    return structure_assert(template, b, base_message, path)
def _action_body_assert(b, base_message, path):
    """Various actions"""
    subty = b['subtype']
    template = {'subtype':'the_subtype', 'channel_id':'1234...', 'context':{}}
    if subty.startswith('fetch_') or subty=='leave_channel':
        pass
    else:
        logger.warning(f'Unknown action subtype for assert, assert may not be valid: {subty}')
    return structure_assert(template, b, base_message, path)


def socket_assert(x):
    """Asserts that a socket call is correct, using the type and subtype to determine the socket.
    Note: There is no HTTPs assert fn, instead the arguments to the function are asserted."""
    if not check_asserts:
        return True
    if 'type' not in x:
        raise PlatformAssertException('The socket request must have a type.')
    x = temp_modify(x)
    template = {'type':'the_request_type', 'request_id':'1234...'}
    service_or_agent = 'service_id' # Can be user_id.
    if x['type'] == types.UPDATE:
        template['body'] = _socket_update_body_assert
    elif x['type'] == types.SERVICE_LOGIN or x['type'] == types.USER_LOGIN:
        template['access_token'] = 'xyzxyz-long-string'; template['auth_origin'] = 'cognito'
        if x['type'] == types.USER_LOGIN:
            service_or_agent = None
    elif x['type'] == types.HEARTBEAT:
        template['body'] = {}
        service_or_agent = None
    elif x['type'] == types.ROGER:
        template['body'] = {'message_id':'1234...', 'context':{}}
        service_or_agent = None
    elif x['type'] == types.COPY:
        template['body'] = {'request_id':'1234...', 'origin_type':'the_type', 'status':True, 'context':{}}
        service_or_agent = None
    elif x['type'] == types.MESSAGE_DOWN:
        template['body'] = lambda b, bm, p: _socket_message_body_assert1(b, bm, p, False)
    elif x['type'] == types.MESSAGE_UP:
        service_or_agent = 'user_id'
        template['body'] = lambda b, bm, p: _socket_message_body_assert1(b, bm, p, True)
    elif x['type'] == types.BUTTON_CLICK:
        service_or_agent = 'user_id'
        template['body'] = _button_click_body_assert
    elif x['type'] == types.MENU_CLICK:
        service_or_agent = 'user_id'
        template['body'] = _context_menuclick_body_assert
    elif x['type'] == types.ACTION:
        service_or_agent = 'user_id'
        template['body'] = _action_body_assert
    else:
        raise PlatformAssertException(f'Unrecognized socket request type {x["type"]}.')
    if service_or_agent:
        template[service_or_agent] = '1234...'
    base_message = x['type']
    if 'body' in x:
        if 'subtype' in x['body']:
            base_message += '_'+x['body']['subtype']
    try:
        return structure_assert(template, x, base_message)
    except Exception as e:
        txt = json.dumps(x, indent=2, ensure_ascii=False)
        raise PlatformAssertException(str(e)+'\nCaused by this request below:\n'+txt)
