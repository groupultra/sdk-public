# MISC functions that don't belong anywhere else.
import sys, os, re, json, threading, asyncio, dataclasses
from moobius import types
from loguru import logger
from pydoc import locate
from dacite import from_dict

DTYPE = '_moobius_type'; DVAL = '_moobius_val' # Used to indicate the class name in JSON files.


def _recursive_dataclass(data):
    """Recursively converts nested lists, dicts, etc into dataclasses.
    Accepts the data. Returns the dataclassed data."""
    if type(data) is dict:
        if DTYPE in data and DVAL in data:
            if data[DTYPE] == 'NoneType':
                return None
            class_name_fullpath = data[DTYPE]
            data_type = locate(class_name_fullpath)

            if data_type:
                if dataclasses.is_dataclass(data_type):
                    return from_dict(data_class=data_type, data=data[DVAL])
                else: # Attempt a generic constructor.
                    return data_type(data[DVAL])
            else:
                raise TypeError(f'Unknown type: {class_name_fullpath}')
        else:
            return dict(zip(data.keys(), [_recursive_dataclass(d) for d in data.values()]))
    elif type(data) in [tuple, list]:
        return [_recursive_dataclass(d) for d in data]
    elif type(data) is set:
        return set([_recursive_dataclass(d) for d in data])
    else:
        return data


def _recursive_undataclass(data, typemark_dataclasses):
    """The inverse function, converts dataclasses back into dicts.
    Accepts the dataclassed data and whether to mark dataclasses in a special way so they are known as such. Returns the non-dataclassed data."""
    if dataclasses.is_dataclass(data):
        if typemark_dataclasses:
            dtype = type(data).__module__+'.'+type(data).__name__
            dval = dataclasses.asdict(data)
            return {DTYPE:dtype, DVAL: dval}
        else:
            return dataclasses.asdict(data)
    elif type(data) is dict:
            return dict(zip(data.keys(), [_recursive_undataclass(d, typemark_dataclasses) for d in data.values()]))
    elif type(data) in [list, tuple]:
        return [_recursive_undataclass(d, typemark_dataclasses) for d in data] # A little duplicated code copying _recursive_dataclass_load.
    elif type(data) is set:
        return set([_recursive_undataclass(d, typemark_dataclasses) for d in data])
    else:
        return data


def assert_strs(*strs):
    """Given a list. Returns True. Raises an Excpetion if the assert fails."""
    for i, s in enumerate(strs):
        if type(s) is not str:
            raise Exception(f"The {i}th element is not a str")


def enhanced_json_load(filename):
    """Loads JSON from the disk, given the filename or bytes. Returns the possibly-nested datastructure which may have Dataclasses."""
    if hasattr(filename, 'read'):
        data = filename.read()
    elif type(filename) is str:
        with open(filename, 'r', encoding='utf-8') as f:
            data = f.read()
    elif type(filename) is bytes:
        data = filename.decode('utf-8')
    data = json.loads(data)
    return _recursive_dataclass(data)


def enhanced_json_save(filename, data, typemark_dataclasses=True, indent=2):
    """
    Saves the JSON to the disk and/or a string.

    Parameters:
      filename: The filename or file object to save to. None if not saving to any file.
      data: What needs to be saved. Can be a nested datastructure even with embedded dataclasses.
      typemark_dataclasses=True: Save dataclasses as special dicts so that on enhanced_json_load load they are converted back into dataclasses.
      indent=2: The indent to display the text at.
    Returns the data as a JSON string.
    """
    data = _recursive_undataclass(data, typemark_dataclasses)
    txt = json.dumps(data, indent=indent)
    if filename:
        if hasattr(filename, 'write'):
            f = filename
            f.write(txt)
        else:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(txt)
    return txt


def summarize_html(html_str):
    """
    Creates a summary given an html_string.
    Converts HTML to an easier-for-a-human format by cutting out some of the more common tags. Far from perfect.
    Returns the summary as a string.
    """
    rs = [r'<div>\d+<\/div *>', r'<div class *= *"[a-zA-Z0-9]*">', r'<span class *= *"[a-zA-Z0-9]*">']
    for tag in ['div', 'li', 'head', 'body', 'pre', 'span']:
        rs.append(f'<{tag} *>')
        rs.append(f'</{tag} *>')
    for r in rs:
        html_str = re.sub(r, "", html_str)
    html_str = html_str.replace('\r\n','\n').replace('\t','  ')
    while '  ' in html_str or '\n\n' in html_str or '\n ' in html_str:
        html_str = html_str.replace('\n\n\n\n\n\n\n\n\n','\n').replace('\n\n','\n').replace('         ',' ').replace('  ',' ').replace('\n ','\n')
    return html_str.strip()


def make_fn_async(f):
    """
    Converts functions to async functions.
    Can be used as "await (make_fun_asycnc(f)(arg1, arg2, etc)).
    Given a function; returns an async version of the function.
    """
    _ind = [False]
    _result = [None]
    async def run_f(*args, **kwargs):
        def f1():
            _result[0] = f(*args, **kwargs)
            _ind[0] = True
        t=threading.Thread(target=f1)
        t.start()
        while not _ind[0]:
            await asyncio.sleep(0.01)
        return _result[0]
    return run_f


def maybe_make_template_files(args):
    """
    Makes template files if there is a need to do so, based on args and sys.argv.
    Called by wand.run() before initializing the Moobius class if it doesn't have any templates.

    Which files are created:
      A template main.py python file which calls Wand.run:
        Only created if the file does not exist AND "make_main main.py" (or "make_main foo.py", etc) is in the system args.
      A sample config.py:
        Only created if "config_path" is in args (or system args) AND the file does not exist.
        This requires user information:
          email: If no system arg "email my@email.com" or "username my@email.com" is specified, prompts for one with input().
          password: If no system arg "password my_sec**t_pword", prompts for one.
          channels: If no system arg "channels abc... def..." to specify one or more channels, prompts for one or more.
        Note: if the user gives an empty response to input(), a nonfunctional default is used, which can be filled in later.

    Unittests to run in a python prompt in an empty folder:
      >>> # Make a main.py file:
      >>> import sys; sys.argv = '_ make_main main.py'.split(' '); import moobius;
      >>> # Prompt the user for credentials and put these in the service.json (NOTE: will generate an error b/c None class):
      >>> import sys; from moobius import MoobiusWand; MoobiusWand().run(None, config_path="config/service.json")
      >>> # Provide credentials, making a service.json with no user input (NOTE: will generate an error b/c None class):
      >>> import sys; sys.argv = '_ email abc@123.com password IAmSecret channels abc-123 def-4561111111111111111111'.split(' '); from moobius import MoobiusWand; MoobiusWand().run(0, config_path="config/service.json")
      >>> # Provide agent credentials. There is no need to provide a channel id (NOTE: will generate an error b/c None class).
      >>> import sys; sys.argv = '_ email abc@123.com password IAmSecret'.split(' '); from moobius import MoobiusWand; MoobiusWand().run(0, config_path="config/agent.json", is_agent=True)

    Parameters:
      args: The list of args.

    Returns:
      None
    """

    main_py = '''
from service import MyService as TheService # TODO: replace "from service import MyService" with the actual path to your class that inherits Moobius.
from moobius import MoobiusWand
if __name__ == "__main__":
    wand = MoobiusWand()

    handle = wand.run(
        TheService,
        log_file="logs/service.log",
        error_log_file="logs/error.log",
        terminal_log_level="INFO",
        config_path="config/service.json", # Default service. Necessary to avoid hard-coding credentials.
        db_config_path="config/db.json", # Commonly used, but not strictly necessary.
        is_agent=False, # Make this True to run an Agent instead (agents also need thier own config_path).
        background=True)
'''

    template_service = {
        "http_server_uri": "https://api.moobius.net/",
        "ws_server_uri": "wss://ws.moobius.net/",
        "email": "<email>",
        "password": "<password>",
        "service_id": "", # This is filled automatically.
        "channels": ["<Channel id 0>", "<Optional Channel id 1>", "..."],
        "others": "include"}

    template_agent = {
        "http_server_uri": "https://api.moobius.net/",
        "ws_server_uri": "wss://ws.moobius.net/",
        "email": "<email>",
        "password": "<password>"}

    is_agent = args.get('is_agent')
    template = template_agent if is_agent else template_service

    # Parse system args:
    args = args.copy()
    for i in range(len(sys.argv)):
        l = sys.argv[i].lower().replace('-','_')
        if l in ['email', 'user', 'username']:
            args['email'] = sys.argv[i+1]
        if l in ['password', 'passphrase']:
            args['password'] = sys.argv[i+1]
        if l in ['config_file', 'config_path']:
            args['config_path'] = sys.argv[i+1]
        if l == 'channels':
            args['channels'] = []
            for j in range(i+1, len(sys.argv)):
                aj = sys.argv[j]
                if j==i+1 or ('-' in aj and set(aj).issubset('0123456789abcdef-') and len(aj)>24):
                    args['channels'].append(aj)
        if l in ['make_main', 'makemain']:
            args['make_main'] = sys.argv[i+1]

    if 'make_main' in args:
        fname = os.path.realpath(args['make_main']).replace('\\','/')
        if not fname.lower().endswith('.py'):
            fname = fname+'.py'
        if not os.path.exists(fname):
            logger.info(f'Creating template main file: {fname}')
            os.makedirs(os.path.split(fname)[0], exist_ok=True)
            with open(fname,'w', encoding='utf-8') as f:
                f.write(main_py)
    if 'config_path' in args:
        fname = os.path.realpath(args['config_path']).replace('\\','/')
        if not fname.lower().endswith('.json'):
            fname = fname+'.json'
        if not os.path.exists(fname):
            logger.info(f'Creating config file: {fname}')
            for field in ['email', 'password'] + ([] if is_agent else ['channels']):
                if field not in args:
                    args[field] = input(f'Input {field} for creating a config file:').strip()
                    if not args[field]:
                        logger.info('No input {field} supplied, a default will be used.')
                        args[field] = f'<{field}>'
                    if field=='channels': # Allow inputing multible channels.
                        args['channels'] = list(args['channels'].split(' '))
                template[field] = args[field]

            os.makedirs(os.path.split(fname)[0], exist_ok=True)
            with open(fname,'w', encoding='utf-8') as f:
                f.write(json.dumps(template, indent=4, ensure_ascii=False))


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
    if type(c) is str or type(c) is types.Character:
        c = [c]
    c = [ch.character_id if type(ch) is types.Character else ch for ch in c] # Convert Character objects to IDs.
    return c


def set_terminal_logger_level(the_level):
    """Sets the logger from the terminal (but preserves other files) given the level. Returns None."""
    logger.remove() # Remove the default one.
    logger.add(sys.stdout, level=the_level)
