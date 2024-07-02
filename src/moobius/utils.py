# MISC functions TODO: Just move these to a better place, having a MISC category isn't clean code.
import sys, os, re, json, threading, asyncio, dataclasses
from moobius import types
from loguru import logger


class EnhancedJSONEncoder(json.JSONEncoder):
    """Json Encoder but with automatic conversion of dataclasses to dict."""
    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        else:
            return super().default(o)

    def __str__(self):
        return f'moobius.EnhancedJSONEncoder()'
    def __repr__(self):
        return self.__str__()


def summarize_html(html_str):
    """Converts HTML to an easier-for-a-human format by cutting out some of the more common tags. Far from perfect."""
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
    """Converts functions to async functions."""
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
    Called by "import moobius" with no args and by wand.run() before initializing the Moobius class.

    A template main.py python file which calls Wand.run:
      Only created if the file does not exist AND "make_main main.py" (or "make_main foo.py", etc) is in the system args.

    A sample config.py:
      Only created if "config_path" is in args (or system args) AND the file does not exist.
      This requires user information:
        email: If no system arg "email my@email.com" or "username my@email.com" is specified, prompts for one with input().
        password: If no system arg "password my_sec**t_pword", prompts for one.
        channels: If no system arg "channels abc... def..." to specify one or more channels, prompts for one or more.
      Note: when the user inputs an empty input() than a nonfunctional default is used, which can be filled in later.

    Unittests to run in a python prompt in an empty folder:
      >>> # Make a main.py file:
      >>> import sys; sys.argv = '_ make_main main.py'.split(' '); import moobius;
      >>> # Prompt the user for credentials and put these in the service.json (NOTE: will generate an error b/c None class):
      >>> import sys; from moobius import MoobiusWand; MoobiusWand().run(None, config_path="config/service.json")
      >>> # Provide credentials, making a service.json with no user input (NOTE: will generate an error b/c None class):
      >>> import sys; sys.argv = '_ email abc@123.com password IAmSecret channels abc-123 def-4561111111111111111111'.split(' '); from moobius import MoobiusWand; MoobiusWand().run(0, config_path="config/service.json")
      >>> # Provide agent credentials. There is no need to provide a channel id (NOTE: will generate an error b/c None class).
      >>> import sys; sys.argv = '_ email abc@123.com password IAmSecret'.split(' '); from moobius import MoobiusWand; MoobiusWand().run(0, config_path="config/agent.json", is_agent=True)
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
    """Converts c to a list of character_ids.
    x can be a string, a list of strings (idempotent), a list of Character, a Character.
    lists can actually be tuples or generators etc."""
    if type(c) is str or type(c) is types.Character:
        c = [c]
    c = list(c)
    c = [ch.character_id if type(ch) is types.Character else ch for ch in c] # Convert Character objects to IDs.
    return c


def set_terminal_logger_level(the_level):
    """Sets the logger from the terminal, but preserves other files."""
    logger.remove() # Remove the default one.
    logger.add(sys.stdout, level=the_level)
