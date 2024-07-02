# Need a FAST start to your CCS app?
# This offers both cli and gui options.
# CLI (defaults will be provided if not given, channels can be a comma-seperated list):
"""
pip install moobius
python -m moobius.quickstart channels=1234abcd... email=foo@bar.com password=password folder=~/my_moobius template=Buttons
echo "Done!"
"""
# GUI (specifying cmds is possible as well as shown in this example):
"""
pip install moobius
python -m moobius.quickstart gui email=foo@bar.com
echo "Done!"
"""

import requests, json, os, sys, shlex
import platform, subprocess
from moobius import types


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

boxes = {}


def open_folder_in_explorer(folder_path):
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
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.HTTPError as http_err:
        raise Exception(f"HTTP error occurred: {http_err}")
    except Exception as err:
        raise Exception(f"Other error occurred: {err}")


def save(fname, x):
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
    out = {**out, **_get_boxes()}
    the_folder = os.path.realpath(out['folder'].replace('~', os.path.expanduser("~"))).replace('\\','/')
    print('Values choosen:', out)

    service_template['channels'] = out['channels'].strip().replace(',', ' ').replace('  ',' ').split(' ')
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
            x = download_text_file_to_string(base_url+ky)

        save(the_folder+'/'+ky, x)

    print('Saved to:', the_folder)
    open_folder_in_explorer(the_folder)
    sys.exit()

cur_row = 1


def make_box(name, detailed_name, default, options=None):
    """None options means fill in."""
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

if __name__ == '__main__': 
    print('Quickstart!')
    #print('Sys args:', sys.argv)
    opts = {'channels':'<channel-id>', 'email':'<name@site.com>', 'password':'<secret>', 'template':'Zero',
            'service_id':'', 'others':'include', 'url':'moobius.net', 'others':'include'}

    # Handle spaces around the = signs if there are any. Note: the [0] arg is the filename, not needed.
    txt = ' '.join([f"{ai}" for ai in sys.argv[1:]])
    while '= ' in txt:
        txt = txt.replace('= ', '=')
    while ' =' in txt:
        txt = txt.replace(' =', '=')
    txt = txt.replace('=""','=').replace('""=','=') # Smash args seperating = and space from single args.
    argv = shlex.split(txt)
    #print('Argv:', argv)

    for a in argv:
        if '=' not in a:
            if a == 'gui' or a == 'Gui':
                a = 'gui=True'
            else:
                raise Exception(f'Argument is not k=v format: {a}')
        k,v = a.strip().split('=')
        if v in ['False', '0', 'false']:
            v = False
        opts[k.strip().lower().replace('channel', 'channels')] = v.strip()

    if opts.get('gui', False):
        import tkinter as tk
        from tkinter import ttk, filedialog

        # Create main window
        root = tk.Tk()
        root.geometry('600x300')
        root.title("Input your channel params")

        # Options:
        make_box("channels", "Channel id(s)", opts['channels'], None)
        make_box("email", "Account email/username", opts['email'], None)
        make_box("password", "Account password (.gitignore!)", opts['password'], None)
        make_box("template", "Choose a starting point", opts['template'], ["Zero", "Bot puppet", "Buttons", "Database", "Demo", "Group chat", "Menu Canvas", "Battleship"])
        make_box("url", "(Advanced) choose URL", opts['url'], ['moobius.net', 'moobius.link', 'moobius.net'])
        make_box("service_id", "(Advanced) Reuse old service_id", opts['service_id'])
        make_box("others", "(Advanced) Orphan channels", opts['others'], [types.INCLUDE, types.IGNORE, types.UNBIND])
        folder_box = make_box("folder", "Working folder", opts.get('folder', ''))

        # Pick a folder:
        def _folder_button_callback(*args, **kwargs):
            the_folder = filedialog.askdirectory()
            if the_folder:
                the_folder = os.path.realpath(the_folder).replace('\\','/')
                folder_box.delete(0, tk.END); folder_box.insert(0, the_folder)

        folder_button = ttk.Button(root, text="Browse", command=_folder_button_callback)
        folder_button.grid(row=cur_row+1, column=0, columnspan=2, pady=10)

        # Press this when they are all done:
        submit_button = ttk.Button(root, text="Submit", command=lambda: submit(opts))
        submit_button.grid(row=cur_row+1, column=1, columnspan=2, pady=10)

        root.mainloop()
    else:
        if 'folder' not in opts:
            opts['folder'] = input('No folder specified. Please input a folder: ').strip()
            raise Exception('At minimum, specify "folder=..." in this input.')
        submit(opts)

