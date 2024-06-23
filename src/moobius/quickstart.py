# Need a FAST start to your CCS app?  `from moobius import quickstart`

print('Quickstart!')

import requests, json, os
import platform, subprocess
import tkinter as tk
from tkinter import ttk, filedialog

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

the_folder = filedialog.askdirectory()


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
        x = json.dumps(x)
    os.makedirs(os.path.dirname(fname), exist_ok=True)
    with open(fname, 'w', encoding='utf-8') as f:
        f.write(x)


def submit():
    out = {}
    for k, v in boxes.items():
        out[k] = v.get()
    print('Values:', out)

    service_template['channels'] = out['channels'].strip().replace(',', ' ').replace('  ',' ').split(' ')
    for k in ['email', 'password']:
        service_template[k] = out[k] 

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

cur_row = 1


def make_box(name, detailed_name, options=None):
    """None options means fill in."""
    global cur_row

    if options:
        the_label = ttk.Label(root, text=detailed_name)
        the_label.grid(row=cur_row, column=0, padx=10, pady=5, sticky=tk.W)
        the_var = tk.StringVar()
        the_box = ttk.Combobox(root, textvariable=the_var, values=options)
        the_box.grid(row=cur_row, column=1, padx=10, pady=5)
        the_box.current(0)
    else:
        the_label = ttk.Label(root, text=detailed_name)
        the_label.grid(row=cur_row, column=0, padx=10, pady=5, sticky=tk.W)
        the_box = ttk.Entry(root, width=20)
        the_box.insert(0, 'Input '+name)
        the_box.grid(row=cur_row, column=1, padx=10, pady=5)

    boxes[name] = the_box
    cur_row += 1


# Create main window
root = tk.Tk()
root.title("Input your channel params")

# Options:
make_box("channels", "Channel id(s)", None)
make_box("email", "Account email/username", None)
make_box("password", "Account password (.gitignore!)", None)
make_box("template", "Choose a starting point", ["Zero", "Bot puppet", "Buttons", "Database", "Demo", "Group chat", "Menu Canvas", "Battleship"])

# Press submit when all ready.
submit_button = ttk.Button(root, text="Submit", command=submit)
submit_button.grid(row=cur_row+1, column=0, columnspan=2, pady=10)

root.mainloop()
