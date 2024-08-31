# This module makes it very easy to gwet started with your own service.
# There is an optional GUI mode as well.
# Run "moobius -help" to learn more.

import requests, json, os, sys, shlex, asyncio, platform, subprocess
import fsspec

from loguru import logger
from moobius import types

TEMPLATE_LIST = ['battleship', 'botpuppet', 'buttons', 'database', 'groupchat', 'menucanvas', 'multiagent', 'template', 'testbed', 'zero']
URL_CHOICES = ['moobius.ai/', 'moobius.link/']

service_template = {
    "http_server_uri": "https://api.moobius.link/",
    "ws_server_uri": "wss://ws.moobius.link/",
    "service_id": "",
    "channels": [],
    "others": "include"
}
account_template = {
    "email": "email",
    "password": "password",
}
usermode_service_template = {
    "http_server_uri": "https://api.moobius.link/",
    "ws_server_uri": "wss://ws.moobius.link/",
}
log_template = {
    "log_level":"INFO",
    "terminal_log_level":"INFO",
    "error_log_level":"WARNING",
    "log_retention":"7 days",
    "log_file":"logs/service.log",
    "error_log_file":"logs/error.log"
}
db_template = {}
global_config = {
    "account_config": "config/account.json",
    "db_config": "config/db.json",
    "service_config": "config/service.json",
    "log_config": "config/log.json"
}
boxes = {}


def download_folder(local_folder, sub_git_folder):
    """Downloads from the GroupUltra Public-CCS-demos. Accepts the local folder to download to and the subfolder within the git repo. Returns None."""
    os.makedirs(local_folder, exist_ok=True)

    # Note: Recursive seems broken, have to manually walk.
    # https://sebastianwallkoetter.wordpress.com/2022/01/30/copy-github-folders-using-python/
    fs = fsspec.filesystem("github", org="groupultra", repo="Public-CCS-demos")
    fs.get(fs.ls(sub_git_folder, recursive=False), os.path.realpath(local_folder).replace('\\','/'), recursive=False)
    sub_local_folders = [fname for fname in os.listdir(local_folder) if os.path.isdir(local_folder+'/'+fname)]
    for sublocal in sub_local_folders:
        download_folder(local_folder+'/'+sublocal, (sub_git_folder+'/'+sublocal).replace('//','/'))


def open_folder_in_explorer(folder_path):
    """Lets the user select a folder given a default folder to pick. This is used for gui-mode only. Returns None."""
    which_os = platform.system()
    try:
        if which_os == "Windows":
            os.startfile(folder_path)
        elif which_os == "Darwin":
            subprocess.run(['open', folder_path])
        elif which_os == "Linux":
            subprocess.run(['xdg-open', folder_path])
        else:
            print(f"Unsupported platform: {platform.system()}")
    except OSError as e:
        print(f"Error opening folder: {e}")


def download_text_file_to_string(url):
    """A simple download, used to get CCS code from GitHub given the URL. Returns the text. Raises network exceptions if the request fails."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.HTTPError as http_err:
        raise Exception(f"HTTP error occurred: {http_err}")
    except Exception as err:
        raise Exception(f"Other error occurred: {err}")


def create_channel(email, password, url):
    """Creates a channel given the email, password, and url. Returns the service_id, channel_id. Used if no channel is specified."""
    http_server_uri = "https://api."+url
    ws_server_uri = "wss://ws."+url

    channel_name = 'starting_channel'
    service_config = {'http_server_uri':http_server_uri, 'ws_server_uri':ws_server_uri, 
                      'service_id':'', 'channels':[], 'others':'include', 'no_warn_cannot_save_service_id':True}
    account_config = {'email':email, 'password':password}
    print('Creating channel...', end='', flush=True)

    from moobius import Moobius # Bury it here so that it can be imported from moobius without issues with circular dependencies.
    service = Moobius(service_config=service_config, account_config=account_config)

    try: # Avoids a spurious error message. https://stackoverflow.com/questions/45600579/asyncio-event-loop-is-closed-when-getting-loop
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    except:
        pass

    asyncio.run(service.authenticate())
    service_id = asyncio.run(service.create_new_service())
    asyncio.run(service.ws_client.connect())
    new_channel_id = asyncio.run(service.create_channel(channel_name, 'Channel created by the GUI.'))
    if not service_id:
        raise Exception('None service id bug.')
    if not new_channel_id:
        raise Exception('None new_channel_id bug.')
    print('Done, id =', service_id, new_channel_id)
    return service_id, new_channel_id


def save(fname, x):
    """Saves a file given a filename and a string. Makes dirs if need be. Returns None."""
    if type(x) is not str:
        x = json.dumps(x, indent=4)
    os.makedirs(os.path.dirname(fname), exist_ok=True)
    with open(fname, 'w', encoding='utf-8') as f:
        f.write(x)


def _get_boxes():
    """Gets the value in each GUI box. Returns an empty dict if it is not the GUI mode."""
    out = {}
    for k, v in boxes.items():
        out[k] = v.get()
    return out


def submit(out):
    """Saves the CCS files (code and config) to a folder given a configuration dict with all the settings. Returns sys.exit().
    Calling this function will read the current gui state."""
    box_values = _get_boxes()
    use_gui = len(box_values)>0
    out = {**out, **box_values}

    while True:
        the_folder = os.path.realpath(out['folder'].replace('~', os.path.expanduser("~"))).replace('\\','/')
        if os.path.exists(the_folder) and os.listdir(the_folder):
            if use_gui:
                from tkinter import messagebox
                gui_response=messagebox.askquestion('Folder not empty', f'{the_folder} already has files in it. Overwrite?').lower().strip()
                if gui_response == "yes":
                    break
                else:
                    return # Don't do anything.
            else:
                confirm = input(f'The folder {the_folder} is not empty. Press y to confirm. Press n to cancel and quit:').strip()
                if confirm and confirm.strip()[0].lower() == 'y':
                    break
                elif confirm and confirm.strip()[0].lower() == 'n':
                    sys.exit(1)
                elif confirm:
                    print("Did not understand, must put in y or n.")
                    #out['folder'] = confirm
        else:
            break

    if not out.get('email') and not use_gui:
        out['email'] = input('Enter account email, or press enter to skip:').strip()
    elif not out.get('email'):
        out['email'] = ''
    if not out.get('password') and not use_gui:
        out['password'] = input('Enter account password, or press enter to skip:').strip()
    elif not out.get('password'):
        out['password'] = ''

    if out.get('email') and out.get('password'):
        if not out.get('channels') and not out.get('service_id'): #Create a channel.
            out['service_id'], out['channels'] = create_channel(out['email'], out['password'], out['url'])

    service_template['channels'] = out['channels'].strip().replace(',', ' ').replace('  ',' ').split(' ')
    print('Channels:', service_template['channels'])
    for k in ['service_id', 'others']:
        service_template[k] = out[k]
    service_template['http_server_uri'] = "https://api."+out['url']
    service_template['ws_server_uri'] = "wss://ws."+out['url']
    for k in ['email', 'password']:
        account_template[k] = out[k]

    download_folder(the_folder, out['template'])
    replace_these = {'config/service.json':service_template, 'config/account.json':account_template, 'config/log.json':log_template,
                    'config/usermode_service.json':service_template, 'config/usermode_account.json':account_template, 'config/usermode_log.json':log_template,
                    'config/config.json':global_config}
    for fname, contents in replace_these.items():
        save(the_folder+'/'+fname, contents)

    print('Saved to:', the_folder)
    open_folder_in_explorer(the_folder)
    sys.exit()

cur_row = 1


def make_box(root, name, detailed_name, default, options=None):
    """
    Makes a box for GUI usage. None options means fill in. Returns ttk.Combobox object.

    Parameters:
      root: Tk.root
      name: The box name.
      detailed_name: More details.
      default: The GUI default.
      options=None: The options to pick, for boxes with options.
    """
    import tkinter as tk
    from tkinter import ttk
    global cur_row

    w = 60
    if options:
        the_label = ttk.Label(root, text=detailed_name)
        the_label.grid(row=cur_row, column=0, padx=10, pady=5, sticky=tk.W)
        the_box = ttk.Combobox(root, values=options, width=w-3)
        for i, o in enumerate(options):
            if o.lower() == default.lower():
                the_box.current(i) # Only works if there is no StringVar arg for GC reasons.
        the_box.grid(row=cur_row, column=1, padx=10, pady=5)
    else:
        the_label = ttk.Label(root, text=detailed_name)
        the_label.grid(row=cur_row, column=0, padx=10, pady=5, sticky=tk.W)
        the_box = ttk.Entry(root, width=w)
        the_box.insert(0, default)
        the_box.grid(row=cur_row, column=1, padx=10, pady=5)

    boxes[name] = the_box
    cur_row += 1
    return the_box


def save_starter_ccs():
    """
    Reads sys.argv, as well as gui interaction if specified.
    Uses this information to construct a CCS app and saves to the folder that was specified.
    This function is called, from the __init__.py in src/moobius, when "python -m moobius" is
    typed into the command line.
    Returns None.
    """

    # Help mode:
    for ai in sys.argv[1:]:
        if ai.lower()=='-h' or ai.lower()=='-help' or ai.lower()=='--h' or ai.lower()=='--help':
            help_msg = '''
Usage: python -m moobius [-h] [-g] [-c] [-e email] [-p ****] [-d directory] [-t template] [-o include] [-url url]
Creates a template service in a given folder to make it easier to get started.

Example:
  python -m moobius channels id1 id2 email foo@bar.com password ****** directory . template=Buttons

Help:
  specify -h to print this help and do nothing else.
Graphical interface:
  specify "-g" to open up a GUI. This can be done in addition to specifying other arguments.
Common arguments:
  -e: The user email (which you use to log in).
  -p: The user password (which you use to log in).
  -t: The starting point for your app. The name of a sub-folder in https://raw.githubusercontent.com/groupultra/Public-CCS-demos/main/...
  -c: The channel-id(s) or a list of comma-seperated channels that you have created in Moobius.
  -d: The folder to save the service to.
Less common arguments:
  -s: Use this to override the default of empty string if you already created and ran a service.
  -o: How to deal with channels that are bound to a different service (set to ignore, unbind, or include), default is "include".
  -url: Use this to override the default url if you are beta-testing a newer version.
'''
            print(help_msg)
            sys.exit()

    print('Quickstart!')
    defaults = {'channels':'', 'email':'', 'password':'', 'template':'Zero',
                'service_id':'', 'others':'include', 'url':'moobius.link/', 'others':'include',
                'folder':'.', 'gui':False}

    opts = {}
    # Parse the arguments.
    singles = ['g']
    vector = ['c']
    name_map = {'g':'gui', 'c':'channels', 'e':'email', 'u':'email', 'p':'password', 'd':'folder', 'f':'folder', 't':'template', 's':'service_id', 'o':'others'}
    ix = 1
    while ix<len(sys.argv):
        if sys.argv[ix] == '-url':
            ty = 'url'
        else:
            ty = sys.argv[ix].replace('-','').lower()[0]
        if ty not in name_map:
            raise Exception('Unrecognized option: ' + sys.argv[ix])
        ky = name_map[ty]
        if ty in singles:
            opts[ky] = True
            ix = ix+1
        elif ty in vector:
            v = []
            ix = ix+1
            while ix<len(sys.argv):
                if sys.argv[ix].startswith('-'):
                    break
                else:
                    v.append(sys.argv[ix])
                    ix = ix+1
            opts[ky] = v
        else:
            opts[ky] = sys.argv[ix+1]
            ix = ix+2

    total_opts = {**defaults, **opts}

    if 'channels' in opts and type(opts['channels']) in [list, tuple]:
        opts['channels'] = ', '.join(opts['channels'])

    if total_opts['gui']:
        import tkinter as tk
        from tkinter import ttk, filedialog

        # Create main window
        root = tk.Tk()
        root.title("Input your channel params")

        # Options:
        make_box(root, "channels", "Channel id(s) comma-sep", total_opts['channels'], None)
        make_box(root, "email", "Account email/username", total_opts['email'], None)
        make_box(root, "password", "Account password (.gitignore!)", total_opts['password'], None)
        make_box(root, "template", "Choose a starting point", total_opts['template'], list(sorted(TEMPLATE_LIST)))
        make_box(root, "url", "(Advanced) choose URL", total_opts['url'], URL_CHOICES)
        make_box(root, "service_id", "(Advanced) Reuse old service_id", total_opts['service_id'])
        make_box(root, "others", "(Advanced) Orphan channels", total_opts['others'], [types.INCLUDE, types.IGNORE, types.UNBIND])
        folder_box = make_box(root, "folder", "Output folder", total_opts['folder'])

        # Pick a folder:
        def _folder_button_callback(*args, **kwargs):
            """A Tkinter callback. Accepts the ignored args/kwargs. Returns None."""
            the_folder = filedialog.askdirectory()
            if the_folder:
                the_folder = os.path.realpath(the_folder).replace('\\','/')
                folder_box.delete(0, tk.END); folder_box.insert(0, the_folder)

        folder_button = ttk.Button(root, text="Browse", command=_folder_button_callback)
        folder_button.grid(row=cur_row+1, column=0, columnspan=2, pady=10)

        # Press this when they are all done:
        submit_button = ttk.Button(root, text="Submit", command=lambda: submit(total_opts))
        submit_button.grid(row=cur_row+1, column=1, columnspan=2, pady=10)

        root.mainloop()
    else:
        submit(total_opts)


# This is not used by the quickstart itself, but is instead another way to fill in channels when running the moobius class.
def maybe_make_template_files(args):
    # TODO: Update this to the latest version.
    """
    Makes template files if there is a need to do so, based on args and sys.argv.
    Called by wand.run() before initializing the Moobius class if it doesn't have any templates.

    Which files are created:
      A service.py file that runs everything.
      A sample config.py:
        Only created if "config_path" is in args (or system args) AND the file does not exist.
        This requires user information:
          email: If no system arg "email my@email.com" or "username my@email.com" is specified, prompts for one with input().
          password: If no system arg "password my_sec**t_pword", prompts for one.
          channels: If no system arg "channels abc... def..." to specify one or more channels, prompts for one or more.
        Note: if the user gives an empty response to input(), a nonfunctional default is used, which can be filled in later.

    Unittests to run in a python prompt in an empty folder:
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
