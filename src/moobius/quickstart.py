# This module makes it very easy to gwet started with your own service.
# There is an optional GUI mode as well.
# Run "python -m moobius -help" to learn more.
"""
pip install moobius
python -m moobius channels=1234abcd... email=foo@bar.com password=password folder=~/my_moobius template=Buttons
echo "Done!"
"""
# GUI (specifying cmds is possible as well as shown in this example):
"""
pip install moobius
python -m moobius gui email=foo@bar.com
echo "Done!"
"""

import requests, json, os, sys, shlex, asyncio
import platform, subprocess
from moobius import types, Moobius


service_template = {
    "http_server_uri": "https://api.moobius.net/",
    "ws_server_uri": "wss://ws.moobius.net/",
    "email": "email",
    "password": "password",
    "service_id": "",
    "channels": [],
    "others": "include"
}
agent_template = {
    "http_server_uri": "https://api.moobius.net/",
    "ws_server_uri": "wss://ws.moobius.net/",
    "email": "<agent email>",
    "password": "<agent password>"
}

download_failed_defaults = {'main.py':
                            '''
from service import MyService
from moobius import MoobiusWand

if __name__ == "__main__":

    wand = MoobiusWand()

    handle = wand.run(
        MyService,
        config_path="config/service.json",
        db_config_path="config/db.json",
        log_file="logs/service.log",
        error_log_file="logs/error.log",
        terminal_log_level="INFO",
        is_agent=False,
        background=True)
                            '''.strip(),
'readme.md':'This needs a more detailed description.',
'service.py':'''
from moobius import Moobius


class MyService(Moobius):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    # Put your code here.
'''.strip(),
'config/db.json':'[]'}

boxes = {}


def open_folder_in_explorer(folder_path):
    """Lets the user select a folder. This is used for gui-mode only."""
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
    """A simple download, used to get CCS code from GitHub."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.HTTPError as http_err:
        raise Exception(f"HTTP error occurred: {http_err}")
    except Exception as err:
        raise Exception(f"Other error occurred: {err}")


def create_channel(email, password, url):
    """Creates a channel and returns the service_id, channel_id. Used if no channel is specified."""
    http_server_uri = "https://api."+url
    ws_server_uri = "wss://ws."+url

    channel_name = 'starting_channel'
    config_path = {'http_server_uri':http_server_uri, 'ws_server_uri':ws_server_uri, 'email':email, 'password':password,
                   'service_id':'', 'channels':[], 'others':'include'}
    print('Creating channel...', end='', flush=True)
    service = Moobius(config_path=config_path, db_config_path={}, is_agent=False)

    asyncio.run(service.start())
    service_id = service.client_id
    new_channel_id = asyncio.run(service.create_channel(channel_name, 'Channel created by the GUI.'))
    if not service_id:
        raise Exception('None service id bug.')
    if not new_channel_id:
        raise Exception('None new_channel_id bug.')
    print('Done, id =', service_id, new_channel_id)
    return service_id, new_channel_id


def save(fname, x):
    """Saves a file to a string, making dirs if need be."""
    if type(x) is not str:
        x = json.dumps(x, indent=4)
    os.makedirs(os.path.dirname(fname), exist_ok=True)
    with open(fname, 'w', encoding='utf-8') as f:
        f.write(x)


def _get_boxes():
    """Empty dict if there are no boxes choosen."""
    out = {}
    for k, v in boxes.items():
        out[k] = v.get()
    return out


def submit(out):
    """Given a configuration dict with all the settings, saves the CCS files (code and config) to a folder."""
    out = {**out, **_get_boxes()}
    the_folder = os.path.realpath(out['folder'].replace('~', os.path.expanduser("~"))).replace('\\','/')
    print('Values choosen:', out)

    service_template['channels'] = out['channels'].strip().replace(',', ' ').replace('  ',' ').split(' ')
    print('Channels:', service_template['channels'])
    for k in ['email', 'password', 'service_id', 'others']:
        service_template[k] = out[k]
    service_template['http_server_uri'] = "https://api."+out['url']
    service_template['ws_server_uri'] = "wss://ws."+out['url']

    # URL fun:
    base_url = "https://raw.githubusercontent.com/groupultra/sdk-public/main/projects/"+out['template']+'/'
    kys = ['main.py', 'readme.md', 'service.py', 'config/db.json', 'config/service.json']
    non_requests = {'config/service.json':service_template, 'config/agent.json':agent_template}
    if out['template'] == 'Bot puppet':
        kys.extend(['agent.py','config/agent.json', 'config/agent_db.json'])
    for ky in kys:
        x = non_requests.get(ky, None)
        if not x:
            url = base_url+ky
            try:
                x = download_text_file_to_string(url)
            except Exception as e:
                print(f"Warning: Download {url} failed using a simple default file")
                x = download_failed_defaults[ky]

        save(the_folder+'/'+ky, x)

    print('Saved to:', the_folder)
    open_folder_in_explorer(the_folder)
    sys.exit()

cur_row = 1


def make_box(root, name, detailed_name, default, options=None):
    """Makes a box for GUI usage. None options means fill in."""
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
    """

    # Help mode:
    for ai in sys.argv[1:]:
        if ai.lower()=='-h' or ai.lower()=='-help':
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
  -t: The starting point for your app. The name of a sub-folder in https://github.com/groupultra/sdk-public/tree/main/projects
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
    #print('Sys args:', sys.argv)
    defaults = {'channels':'<channel-id>', 'email':'<name@site.com>', 'password':'<secret>', 'template':'Zero',
                'service_id':'', 'others':'include', 'url':'moobius.net/', 'others':'include',
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

    if 'email' in opts and 'password' in opts and 'channels' not in opts and 'service_id' not in opts: #Create a channel.
        opts['service_id'], opts['channels'] = create_channel(opts['email'], opts['password'], total_opts['url'])

    if type(opts['channels']) in [list, tuple]:
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
        make_box(root, "template", "Choose a starting point", total_opts['template'], ["Zero", "Bot puppet", "Buttons", "Database", "Demo", "Group chat", "Menu Canvas", "Battleship"])
        make_box(root, "url", "(Advanced) choose URL", total_opts['url'], ['moobius.net/', 'moobius.link/', 'moobius.app/'])
        make_box(root, "service_id", "(Advanced) Reuse old service_id", total_opts['service_id'])
        make_box(root, "others", "(Advanced) Orphan channels", total_opts['others'], [types.INCLUDE, types.IGNORE, types.UNBIND])
        folder_box = make_box(root, "folder", "Output folder", total_opts['folder'])

        # Pick a folder:
        def _folder_button_callback(*args, **kwargs):
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

