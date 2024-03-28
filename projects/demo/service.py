# service.py
import json, sys, asyncio, pprint, os, time, pathlib
import copy
from datetime import datetime

from loguru import logger
from moobius import Moobius, MoobiusStorage
from moobius.database.storage import CachedDict
import moobius.types as types
from moobius.types import Button, CanvasElement, StyleElement, ContextMenuElement

avoid_redis_on_windoze = True # Redis requires WSL2 to run on windows since it is Linux-only.
avoid_redis = (avoid_redis_on_windoze and (sys.platform.lower() in ['win', 'win32', 'win64', 'windows', 'windoze'])) or avoid_redis_on_windoze == 'also linux'
load_xtra_channels_on_start = False # There can be way too many sometimes!
show_us_all = True # When one user presses a button, do all users see the effect?

example_socket_callback_payloads = {} # Print these out when the AI is done.


class DemoService(Moobius):
    def __init__(self, log_file="logs/service.log", error_log_file="logs/error.log", **kwargs):
        super().__init__(**kwargs)

        for c in self.db_config: # Windoze!
            if 'redis' in c['implementation'].lower():
                if avoid_redis:
                    logger.warning('WARNING: No Redis this demo b/c avoid_redis is True, using JSON instead for: '+ str(c))
                    c['implementation'] = 'json'

        self.log_file = log_file
        self.error_log_file = error_log_file

        with open('resources/buttons.json', 'r') as f:
            self._default_buttons = [Button(**b) for b in json.load(f)]
        self.image_show_dict = {}

        _menu = lambda name, the_id, tys: ContextMenuElement(item_name=name, item_id=the_id, support_subtype=tys)
        menus = [_menu('Text 1', '1', [types.TEXT]), _menu('Text 2', '2', [types.TEXT]), _menu('Text 3', '3', [types.TEXT]),
                 _menu('Image 1', 'R', [types.IMAGE]), _menu('Image 2', 'G', [types.IMAGE]), _menu('Image 3', 'B', [types.IMAGE]),
                 _menu('Audio 1', 'doe', [types.AUDIO]), _menu('Audio 2', 're', [types.AUDIO]), _menu('Audio 3', 'mi', [types.AUDIO]),
                 _menu('File 1', 'Loads', [types.FILE]), _menu('File 2', 'Loading', [types.FILE]), _menu('File 3', 'Loaded', [types.FILE])]
        self.context_menu_list = menus
        self.LIGHT = "light"
        self.DARK = "dark"
        self.MICKEY = "Mickey"
        self.WAND = "Wand"
        self.MICKEY_LIMIT = 5

        self.image_paths = {}
        self.database_debugs = {}

        self._default_status = {
            'canvas_mode': self.LIGHT,
            'mickey_num': 0
        }

        self.images = {
            self.LIGHT: "resources/light.png",
            self.DARK: "resources/dark.png",
            self.MICKEY: "resources/mickey.jpg",
            self.WAND: "resources/wand.png"
        }

        self.xtra_channels = {}

    @property
    def default_status(self):
        return copy.deepcopy(self._default_status)

    @property
    def default_buttons(self):
        return copy.deepcopy(self._default_buttons)

    def populate_debug_storage(self, channel_id):
        """Debug to make sure that CachedDict is working correctly."""
        # Debug feature to test MoobiusStorage objects:
        debug_channel = MoobiusStorage(self.client_id, channel_id, db_config=self.db_config)
        self.database_debugs[channel_id] = {'cached_dict_keys_no_load_test':{}, 'cached_dict_keys_YES_load_test':{},
                                            'cached_dict_keys_ALLPOP_test':{}}
        for k, v in debug_channel.__dict__.items():
            if type(v) is CachedDict:
                self.database_debugs[channel_id]['cached_dict_keys_no_load_test'][k] = dict(zip(v.keys(), v.values()))

        debug_channel = MoobiusStorage(self.client_id, channel_id, db_config=self.db_config)
        for k, v in debug_channel.__dict__.items():
            if type(v) is CachedDict:
                v.load()
                self.database_debugs[channel_id]['cached_dict_keys_YES_load_test'][k] = dict(zip(v.keys(), v.values()))

                for k1 in list(v.keys()):
                    v.pop(k1)
                self.database_debugs[channel_id]['cached_dict_keys_ALLPOP_test'][k] = dict(zip(v.keys(), v.values()))

    async def initialize_channel(self, channel_id):
        """Initalizes the channel (given by channel_id) with the images and real and virtual characters.
           All of this is stored in a MoobiusStorage object."""
        self.populate_debug_storage(channel_id)

        the_channel = MoobiusStorage(self.client_id, channel_id, db_config=self.db_config)
        self.channels[channel_id] = the_channel

        real_character_ids = await self.fetch_real_character_ids(channel_id, raise_empty_list_err=False)

        for character_id, character_profile in zip(real_character_ids, await self.fetch_character_profile(real_character_ids)):
            if type(character_id) is not str:
                raise Exception('character_id must be a str.')
            the_channel.real_characters[character_id] = character_profile

            if character_id not in the_channel.buttons:
                the_channel.buttons[character_id] = self.default_buttons

            if character_id not in the_channel.states:
                the_channel.states[character_id] = self.default_status

        for name in self.images: # Once per startup upload images.
            if name not in self.image_paths:
                self.image_paths[name] = await self.upload_file(self.images[name])

        for sn in range(self.MICKEY_LIMIT):
            key = f"{self.MICKEY}_{sn}"

            if key not in the_channel.virtual_characters:
                image_path = self.image_paths[self.MICKEY]

                the_channel.virtual_characters[key] = await self.create_character(
                    f'{self.MICKEY} {sn}', image_path, f'I am {self.MICKEY} {sn}!'
                )

        the_channel.virtual_characters[self.WAND] = await self.create_character(
            self.WAND, self.image_paths[self.WAND], f'I am {self.WAND}!'
        )

        self.image_show_dict = {
            self.LIGHT: CanvasElement(path=self.image_paths[self.LIGHT], text="Let There Be Light!"),
            self.DARK: [CanvasElement(path=self.image_paths[self.DARK], text="Let There Be Dark!"), CanvasElement(path=self.image_paths[self.DARK], text="Let There Be Dark Again!")]
        }
        return the_channel

    async def get_channel(self, channel_id):
        """Prevents KeyErrors by creating new channel databases if they don't exist yet."""
        if channel_id not in self.channels:
            await self.initialize_channel(channel_id)
        return self.channels[channel_id]

    async def on_start(self):
        """Called after successful connection to websocket server and service login success.
           Launches the chron check-in task and searches for extra channels bound to this service."""
        logger.add(self.log_file, rotation="1 day", retention="7 days", level="DEBUG")
        logger.add(self.error_log_file, rotation="1 day", retention="7 days", level="ERROR")

        self.scheduler.add_job(self.cron_task, 'interval', minutes=1)

        channel_ids = await self.fetch_bound_channels()
        for c_id in channel_ids:
            if c_id not in self.channels:
                if load_xtra_channels_on_start:
                    logger.info(f'EXTRA channel bound to this service on startup will be added: {c_id}')
                    await self.initialize_channel(c_id)
                else:
                    logger.info(f'EXTRA channel bound to this service on startup will NOT be added b/c load_xtra_channels_on_start is False: {c_id}')

    async def cron_task(self):
        """Sends a check-in message to each channel."""
        for c_id in self.channels.keys():
            the_channel = await self.get_channel(c_id)
            recipients = list(the_channel.real_characters.keys())
            talker = the_channel.virtual_characters[self.WAND].character_id
            txt = f"Check in every minute! {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            await self.send_message(c_id, txt, talker, recipients)

    async def on_message_down(self, message_down):
        """This and several other callbacks only exist to record the API calls."""
        example_socket_callback_payloads['on_message_down'] = message_down

    async def on_update(self, the_update):
        """This and several other callbacks only exist to record the API calls."""
        example_socket_callback_payloads['on_update'] = the_update

    async def on_message_up(self, message_up):
        """Runs various commands, such as resetting when the user types in "reset".
           (Agent-related commands are found in the agent.py instead of here)."""
        from moobius.types import MessageBody
        if type(message_up) is not MessageBody: # DEBUG TODO.
            print(message_up)
            raise Exception('message_up not message body see above.')
        channel_id = message_up.channel_id
        recipients = message_up.recipients
        sender = message_up.sender
        to_whom = await self.fetch_real_character_ids(channel_id, raise_empty_list_err=False) if show_us_all else [sender]

        if message_up.subtype == types.TEXT:
            txt = message_up.content.text
            txt1 = txt.lower().strip()
            the_channel = await self.get_channel(channel_id)
            if type(sender) is not str:
                raise Exception(f'Sender must be a string, instead it is: {sender}')
            if sender not in list(the_channel.real_characters.keys()):
                await self.add_real_character(channel_id, sender, intro="oops looks like (bug) did not add this character on startup.")

            if recipients: # DEMO: text modification
                if txt1.lower() == "moobius":
                    await self.send_message("Moobius is Great!", channel_id, sender, recipients)
                elif txt1.lower() == "api":
                    lines = []
                    for k,v in example_socket_callback_payloads.items():
                        lines.append(k+': '+str(v))
                    txt2 = '\n\n'.join(lines)
                    await self.send_message('Socket api call examples recorded:\n'+txt2, channel_id, sender, recipients)
                else:
                    await self.send_message(txt, channel_id, sender, recipients)
            else: # DEMO: commands to Service(Infinity)
                if txt1 == "hide":
                    for usr in to_whom:
                        if usr in the_channel.buttons:
                            the_channel.buttons[sender] = []
                    await self.send_buttons_from_database(channel_id, sender)
                    await self.send_update_style(channel_id, [StyleElement(widget="canvas", display="invisible", expand="false")], to_whom)
                elif txt1 == "show":
                    for usr in to_whom:
                        if usr in the_channel.buttons:
                            the_channel.buttons[sender] = self.default_buttons
                    await self.send_buttons_from_database(channel_id, sender)
                    await self.send_update_style(channel_id, [StyleElement(widget="canvas", display="visible", expand="true")], to_whom)
                elif txt1 == "reset":
                    for sn in range(self.MICKEY_LIMIT):
                        the_character_id = the_channel.virtual_characters[f"{self.MICKEY}_{sn}"].character_id
                        await self.update_character(character_id=the_character_id, avatar=self.image_paths[self.MICKEY], description='Mickey reset!', name=f'Mickey {sn}')

                    for usr in to_whom:
                        if usr in the_channel.states:
                            the_channel.states[usr]['mickey_num'] = 0
                            the_channel.states.save(usr)

                    await self.calculate_and_update_character_list_from_database(channel_id, sender)
                    the_channel = await self.get_channel(channel_id) # TODO: why call this twice?
                    for usr in to_whom:
                        if usr in the_channel.buttons:
                            the_channel.buttons[sender] = self.default_buttons # Reset buttons etc.
                    await self.send_update_buttons(channel_id, self.default_buttons, to_whom)
                elif txt1.split(' ')[0] == 'laser':
                    await self.send_message(f"NOTE: The Laser feature is not a standard SDK feature, it is specific to Demo.", channel_id, sender, to_whom)
                    if '>' not in txt1:
                        await self.send_message(f'Must be formatted "laser name > message, and only sent to a single user".', channel_id, sender, to_whom)
                    else:
                        pair = [t.strip() for t in txt.split('>')]
                        the_name = ' '.join(pair[0].split(' ')[1:])
                        the_message = pair[1]
                        if len(the_message.strip())<2:
                            await self.send_message(f'The message was empty, a default message will be used.".', channel_id, sender, to_whom)
                            the_message = 'Empty_message!'
                        real_ids = await self.fetch_real_character_ids(channel_id, raise_empty_list_err=False)
                        real_profiles = await self.fetch_character_profile(real_ids)
                        target_id = None
                        for rp in real_profiles:
                            if rp.name.lower().strip() == the_name.lower().strip():
                                target_id = rp.character_id
                        if target_id:
                            await self.send_message(f'Sending message to name={the_name}, id={target_id}".', channel_id, sender, to_whom)
                            await self.send_message(f'Laser message: "{the_message}".', channel_id, sender, target_id)
                        else:
                            await self.send_message(f'Cannot find character with name={the_name}".', channel_id, sender, to_whom)
                else:
                    txt = txt+' (this message has no recipients, either it was sent to service or there is a bug).'
                    await self.send_message(channel_id, txt, to_whom, sender=sender)
        else:
            await self.send_message(message_up) # This is so that everyone can see the message you sent.
        example_socket_callback_payloads['on_message_up'] = message_up

    async def on_fetch_service_characters(self, action):
        example_socket_callback_payloads['on_fetch_service_characters'] = action
        await self.calculate_and_update_character_list_from_database(action.channel_id, action.sender)

    async def on_fetch_buttons(self, action):
        example_socket_callback_payloads['on_fetch_buttons'] = action
        to_whom = await self.fetch_real_character_ids(action.channel_id, raise_empty_list_err=False) if show_us_all else [sender]
        if hasattr(self, 'TMP_print_buttons') and getattr(self, 'TMP_print_buttons'): # Set to True to indicate an extra call to print the buttons.
            self.TMP_print_buttons = False
            channel_id = action.channel_id
            sender = action.sender
            await self.send_message(f"Fetch button action\n: {action}.", channel_id, sender, to_whom)
        else:
            await self.send_buttons_from_database(action.channel_id, action.sender)

    async def on_fetch_channel_info(self, action):
        example_socket_callback_payloads['on_fetch_channel_info'] = action

    async def on_fetch_canvas(self, action):
        """Pipes self.image_show_dict from channel.states into self.send_update_canvas."""
        example_socket_callback_payloads['on_fetch_canvas'] = action
        channel_id = action.channel_id
        sender = action.sender
        the_channel = await self.get_channel(channel_id)
        to_whom = await self.fetch_real_character_ids(channel_id, raise_empty_list_err=False) if show_us_all else [sender]

        state = the_channel.states[sender]['canvas_mode']
        await self.send_update_canvas(channel_id, self.image_show_dict[state], to_whom)
        await self.send_update_style(channel_id, [StyleElement(widget="canvas", display="visible", expand="true")], to_whom)

    async def add_real_character(self, channel_id, character_id, intro="joined the channel!"):
        character = await self.fetch_character_profile(character_id)
        name = character.name
        the_channel = await self.get_channel(channel_id)

        the_channel.real_characters[character_id] = character
        the_channel.buttons[character_id] = self.default_buttons
        the_channel.states[character_id] = self.default_status

        character_ids = list(the_channel.real_characters.keys())
        await self.send_update_character_list(channel_id, character_ids, character_ids)
        await self.send_message(f'{name} {intro} (id={character_id})', channel_id, character_id, character_ids)

    async def on_join_channel(self, action):
        """Most join handlers, as this one does, will send_update_character_list with the new character added and send a "user joined!" message."""
        example_socket_callback_payloads['on_join_channel'] = action
        sender_id = action.sender
        channel_id = action.channel_id
        await self.add_real_character(channel_id, sender_id, intro="joined the channel!")

    async def on_leave_channel(self, action):
        """Most leave handlers, as this one does, will send_update_character_list with the character removed and maybe send a "user left!" message."""
        example_socket_callback_payloads['on_leave_channel'] = action
        sender = action.sender
        channel_id = action.channel_id
        character = (await self.get_channel(action.channel_id)).real_characters.pop(sender, None)
        (await self.get_channel(channel_id)).states.pop(sender, None)
        (await self.get_channel(channel_id)).buttons.pop(sender, None)
        name = character.name

        real_characters = (await self.get_channel(channel_id)).real_characters
        character_ids = list(real_characters.keys())

        await self.send_update_character_list(channel_id, character_ids, character_ids)
        await self.send_message(f'{name} left the channel!', channel_id, sender, character_ids)

    async def on_copy_client(self, the_copy):
        await super().on_copy_client(the_copy) # One of the few callbacks to have an action.
        example_socket_callback_payloads['on_copy_client'] = the_copy

    async def on_unknown_payload(self, x):
        example_socket_callback_payloads['on_unknown_payload'] = x

    async def on_update_style(self, x):
        example_socket_callback_payloads['on_update_style'] = x

    async def on_update_buttons(self, x):
        example_socket_callback_payloads['on_update_buttons'] = x

    async def on_update_canvas(self, x):
        example_socket_callback_payloads['on_update_canvas'] = x

    async def on_update_characters(self, x):
        example_socket_callback_payloads['on_update_characters'] = x

    async def on_button_click(self, button_click):
        """Called when the user presses a button (and selecting an option of a list appears). button_click is a ButtonClick object.
           This is a major switchyard which handles most of the different buttons in the demo."""
        example_socket_callback_payloads['on_button_click'] = button_click
        channel_id = button_click.channel_id
        button_id = button_click.button_id.lower()
        who_clicked = button_click.sender
        the_channel = await self.get_channel(channel_id)

        #character = the_channel.real_characters[who_clicked]
        #name = character.name
        to_whom = await self.fetch_real_character_ids(channel_id, raise_empty_list_err=False) if show_us_all else [who_clicked]

        redis_txt = 'not-the-Redis' if avoid_redis else 'Redis'
        value = None
        if button_click.arguments:
            value0 = button_click.arguments[0].value
            value = value0.lower()

        def _make_image(vignette=0.0):
            """Generates a "random" image and returns the local filepath (as a string) as well as a removal function (if the image is dynamic)."""
            dyn_mode = False
            try:
                from PIL import Image
                import numpy as np
                dyn_mode = True
            except Exception as e:
                logger.info('no PIL detected, will not be able to dynamically generate an image.')
                pass
            if dyn_mode:
                P = 128
                arr = np.zeros([P, P, 4])
                N = 16
                freq = np.random.random([N, 4])*np.transpose(np.tile(np.arange(N), [4, 1]))
                ampli = np.random.random([N, 4])/(1.0+freq**1.5)
                phase = np.random.random([N, 4])*6.28
                X, Y = np.meshgrid(np.arange(P), np.arange(P))
                for rgba in range(4):
                    for i in range(N):
                        theta = 6.28*np.random.random()
                        arr[:,:,rgba] += np.cos((X*np.cos(theta)+Y*np.sin(theta))*freq[i,rgba]+phase[i,rgba])*ampli[i,rgba]
                    arr[:,:,rgba] = arr[:,:,rgba]*(1.0-vignette+vignette*(1-16*(X-0.5*P)*(X-0.5*P)*(Y-0.5*P)*(Y-0.5*P)/P/P/P/P))
                arr = arr-np.min(arr)
                arr = arr/np.max(arr)
                im = Image.fromarray((arr*255+0.5).astype('uint8'), 'RGBA')
                file_path = './resources/autogen_image.png'
                im.save(file_path)
                rm_fn = lambda: os.remove(file_path)
            else:
                file_path = './resources/mickey.jpg'
                rm_fn = lambda: False
            return file_path, rm_fn

        if button_id == "message_btn".lower():
            if value == 'TextMessage'.lower():
                import random
                some_text = ((str(random.random())+'   ')[0:3])*int(random.random()*12+3)
                await self.send_message(some_text, channel_id, who_clicked, to_whom)
            elif value == 'CardMessage'.lower():
                card_message = {'link':'https://neocities.org/', 'title':'Where have all the websites gone?', 'button':'Here!',
                                'text':'Domain names? Urls? wwwdotcoms?'}
                await self.send_message(card_message, channel_id, who_clicked, to_whom, subtype=types.CARD)
            elif value == 'ImagePath'.lower():
                file_path, rm_fn = _make_image(0.0)
                path_obj = pathlib.Path(file_path) # Conversion to a Path makes the Moobius class recognize it as an image.
                await self.send_message(path_obj, channel_id, who_clicked, to_whom)
                rm_fn()
            elif value == 'AudioPath'.lower():
                await self.send_message(pathlib.Path('./resources/tiny.mp3'), channel_id, who_clicked, to_whom)
            elif value == 'FilePath'.lower():
                await self.send_message(pathlib.Path('./resources/tiny.pdf'), channel_id, who_clicked, to_whom)
            elif value == 'ImageGivenTextPath'.lower(): # Override subtype to not send a boring text message.
                file_path, rm_fn = _make_image(-1.0)
                await self.send_message(file_path, channel_id, who_clicked, to_whom, subtype=types.IMAGE)
                rm_fn()
            elif value == 'DownloadGivenImagePath'.lower():
                file_path, rm_fn = _make_image(1.0)
                await self.send_message(pathlib.Path(file_path), channel_id, who_clicked, to_whom, subtype=types.FILE)
                rm_fn()
            elif value == 'DownloadGivenImagePathWithRename'.lower(): # Show the filename as different from it's actual name.
                file_path, rm_fn = _make_image(2.0)
                await self.send_message(pathlib.Path(file_path), channel_id, who_clicked, to_whom, subtype=types.FILE, file_display_name='Custom_display_name.png')
                rm_fn()
            elif value == 'EmptyRecip'.lower():
                await self.send_message(f'Message 1/3 sent to {to_whom}', channel_id, who_clicked, to_whom)
                await self.send_message(f'Message 2/3 sent to Empty list (you should NOT see this message!)', channel_id, who_clicked, [])
                await self.send_message(f'Message 3/3 sent to {to_whom}. You should NOT see message 2/3', channel_id, who_clicked, to_whom)
            elif value == 'Swap Canvas'.lower():
                if the_channel.states[who_clicked]['canvas_mode'] == self.LIGHT: 
                    the_channel.states[who_clicked]['canvas_mode'] = self.DARK
                else:
                    the_channel.states[who_clicked]['canvas_mode'] = self.LIGHT

                the_channel.states.save(who_clicked)
                state = the_channel.states[who_clicked]['canvas_mode']
                await self.send_update_canvas(channel_id, self.image_show_dict[state], to_whom)

                image_uri = self.image_paths[state] # Shows using an online image.
                await self.send_message(image_uri, channel_id, who_clicked, to_whom, subtype=types.IMAGE)
            elif value == 'Test Socket Asserts'.lower():
                # Tests JSON datastructures which are almost correct. Can assert catch the error? TODO: add more.
                bad_subtype = 'not a valid subtype'
                bad_message_body = {'channel_id':channel_id, 'recipients':to_whom, 'subtype':bad_subtype, 'message_content':{'text':'ok'}}
                bad_message = {'type':types.MESSAGE_DOWN,'request_id':'some_id', 'service_id':self.client_id, 'body': bad_message_body}
                try:
                    await self.ws_client.send(bad_message)
                    await self.send_message('No assert error raised for bad subtype message.', channel_id, who_clicked, to_whom)
                except Exception as e:
                    await self.send_message(f'Assert error raised for bad message subtype:\n{e}', channel_id, who_clicked, to_whom)
                #await self.ws_client.send(bad_message) # uncomment to raise an Exception in the terminal.
            elif value == "Fetch Chat History".lower():
                await self.send_message(f"Fetching chat history (Warning: this feature is likely broken).", channel_id, who_clicked, to_whom)
                history = await self.fetch_message_history(channel_id, limit=6, before="null")
                await self.send_message(f"Recent chat history of this channel:\n{history}", channel_id, who_clicked, to_whom, len_limit=4096)
            elif value == "Fetch Buttons".lower():
                await self.send_message(f"WARNING: Getting a callback for Fetch Buttons will be delayed may need a refresh to see.", channel_id, who_clicked, to_whom)
                self.TMP_print_buttons = True
                await self.send_fetch_buttons(channel_id)
            elif value == "Fancy Right Click".lower():
                await self.send_update_context_menu(channel_id, self.context_menu_list, to_whom)
                await self.send_message("Try right-clicking on a message.", channel_id, who_clicked, to_whom)
            else:
                raise Exception(f'Strange value for button channel_btn: {value}')
        elif button_id == "money_btn".lower():
            if value == '(Print Savings)'.lower() or value == '(Donate all)'.lower():
                if value == '(Donate all)'.lower():
                    tot = 0
                    for k in the_channel.currency.keys():
                        tot += the_channel.currency[k]
                        the_channel.currency[k] = 0
                    await self.send_message(f"{tot} weeks of savings donated to mysterious unknown charities.", channel_id, who_clicked, to_whom)
                desc = []
                unicode_map = {'naira':'₦', 'dollar':'$', 'peso':'₱', 'yuan':'¥', 'euro': '€', 'kina':'K', 'penguin':'🐧'}
                for k in the_channel.currency.keys():
                    desc.append(f'{unicode_map[k.lower()]}={the_channel.currency[k]}')
                desc = '['+', '.join(desc)+']'
                await self.send_message(f"{redis_txt} query; number of weeks of living expenses saved in each currency:\n {desc}", channel_id, who_clicked, to_whom)
            else:
                msg_map = {'naira':'Nigerian', 'dollar':'American', 'peso':'Chilean', 'yuan':'Chinese', 'euro': 'West European', 'kina':'Papua New Guinean', 'penguin':'Antarctican'}

                await self.send_message(f"You earn two weeks salary of {msg_map[value]}. Your bank account will be stored in {redis_txt}!", channel_id, who_clicked, to_whom)

                if value0 not in the_channel.currency:
                    the_channel.currency[value0] = 0
                the_channel.currency[value0] += 2 # Number of weeks.
        elif button_id == "channel_btn".lower():
            extra_channel_ids = list(self.xtra_channels.keys())
            if value == "New Channel".lower():
                channel_name = '>>Demo TEMP channel'+str(len(extra_channel_ids))
                new_channel_id = await self.create_and_bind_channel(channel_name, 'Channel created by the GUI.')
                await self.initialize_channel(new_channel_id) # Prevents KeyErrors.
                self.xtra_channels[new_channel_id] = 'A channel'
                await self.send_message(f"New channel created, refresh and it should appear on the left bar: {channel_name} ({new_channel_id})", channel_id, who_clicked, to_whom)
            elif value == "Ping Channels".lower():
                tasks = [self.send_message(f"Pinging Channel ids: {extra_channel_ids} (one ping message should show up in each channel)", channel_id, who_clicked, to_whom)]
                for extra_channel_id in extra_channel_ids:
                    tasks.append(self.send_message(f"Ping from channel {channel_id} to channel {extra_channel_id}!", extra_channel_id, who_clicked, to_whom))
                await asyncio.wait(tasks)
            elif value == "List Bound Channels".lower():
                channel_ids = await self.fetch_bound_channels()
                await self.send_message(f"All bound channels:\n{channel_ids}.", channel_id, who_clicked, to_whom)
            elif value == "Leave Extra Channels".lower():
                await self.send_message(f"Fetching the list of bound channels, will leave any channels which are not in the config.", channel_id, who_clicked, to_whom)
                left_channels = []
                channel_ids = await self.fetch_bound_channels()
                for c_id in channel_ids:
                         if c_id in self.config["channels"]:
                             continue # Do not leave the core channels.
                         if c_id in self.channels:
                             del self.channels[c_id]
                         left_channels.append(c_id)
                await self.send_message(f"Will try to leave these channels:\n{left_channels}.", channel_id, who_clicked, to_whom)
                sucessfully_left = []
                for c_id in left_channels:
                    success = False
                    try:
                        await self.send_leave_channel(c_id) # This is for the Agent, not the Service.
                        success = True
                    except Exception as e:
                        logger.warning(f'Send_leave_channel failed for {c_id}: {e}.')
                    try:
                        await self.unbind_service_from_channel(c_id) # This is for the Service.
                    except Exception as e:
                        logger.warning(f'Unbind_service_from_channel failed for {c_id}: {e}.')
                        success = True
                    if success:
                        sucessfully_left.append(c_id)
                await self.send_message(f"Has left these channels (refresh to see):\n{sucessfully_left}.", channel_id, who_clicked, to_whom)
            elif value == "Fetch Channel List".lower():
                x = await self.fetch_channel_list()
                await self.send_message(f"Channel list:\n{x}", channel_id, who_clicked, to_whom)
                x = await self.fetch_popular_channels()
                await self.send_message(f"Popular channel list:\n{x}", channel_id, who_clicked, to_whom)
            elif value == "Update Extra Channels".lower():
                extra_channel_ids = list(self.xtra_channels.keys())
                ix = 0
                for bid in extra_channel_ids:
                    await self.update_channel(bid, f'<>Updated DemoTmpChannel Updated{ix}<>', 'Pressed the update extra channels button.')
                    ix = ix+1
                await self.send_message(f"Updated these channel names (refresh to see changes):\n{extra_channel_ids}", channel_id, who_clicked, to_whom)
            elif value == "Test Database".lower():
                tmp_path = './debuggy stuff.txt'
                with open(tmp_path, 'w', encoding='utf-8') as f:
                    f.write(str(self.database_debugs)) # It's a big data dump! So it must be sent as an attachment.
                await self.upload_file_as_message(tmp_path, channel_id, who_clicked, to_whom)
                os.remove(tmp_path)
            elif value == "Wipe DatabaseA".lower() or value == "Wipe DatabaseB".lower():
                two_arg_pop = value == "Wipe DatabaseB".lower()
                await self.send_message(f"WARNING: This may crash the Demo. Wiping {list(self.channels.keys())}. {'Two arg pop.' if two_arg_pop else 'One arg pop.'}", channel_id, who_clicked, to_whom)
                n_keys_popped = 0
                for channel_store in self.channels.values():
                    for k, v in channel_store.__dict__.items():
                        if type(v) is CachedDict:
                            for k1 in list(v.keys()):
                                n_keys_popped += 1
                                if two_arg_pop:
                                    v.pop(k1, 'foo')
                                else:
                                    v.pop(k1)
                            if two_arg_pop:
                                v.pop('non_exist_key', 'should_not_error_when_default_is_provided')
                await self.send_message(f"Cleared these, total popped keys {n_keys_popped}; channels {list(self.channels.values())}, these folders should have no .json files in them.", channel_id, who_clicked, to_whom)
                await self.send_message(f"Blocking sleep 32 seconds, to give a time window within which no new database entries will be saved.", channel_id, who_clicked, to_whom)
                time.sleep(32)
                await self.send_message(f"Done with blocking sleep.", channel_id, who_clicked, to_whom)
            else:
                raise Exception(f'Strange value for button channel_btn: {value}')
        elif button_id == "user_btn".lower():
            if not hasattr(self, 'n_usr_update'):
                self.n_usr_update = -1
            self.n_usr_update += 1
            image_list = [self.image_paths[x] for x in [self.LIGHT, self.DARK, self.WAND]]
            image_path = image_list[self.n_usr_update%len(image_list)] # Cycle through non-mickey images.

            #with open('config/agent.json','r') as f_obj:
            #    agent_config = json.load(f_obj)
            if value == 'Make Mickey'.lower():
                if the_channel.states[who_clicked]['mickey_num'] >= self.MICKEY_LIMIT:
                    await self.send_message("You have reached the limit of Mickey!", channel_id, who_clicked, to_whom)
                else:
                    the_channel.states[who_clicked]['mickey_num'] += 1
                    the_channel.states.save(who_clicked)

                    await self.calculate_and_update_character_list_from_database(channel_id, who_clicked)
            elif value == 'Mickey Talk'.lower():
                if the_channel.states[who_clicked]['mickey_num'] == 0:
                    await self.send_message("Please Create Mickey First!", channel_id, who_clicked, to_whom)
                else:
                    sn = the_channel.states[who_clicked]['mickey_num'] - 1
                    talker = the_channel.virtual_characters[f"{self.MICKEY}_{sn}"].character_id
                    await self.send_message(f"Mickey {sn} Here! Mickeys are stored in JSON db.", channel_id, who_clicked, to_whom)
            elif value == "Update Mickey (not agent) name".lower():
                if the_channel.states[who_clicked]['mickey_num'] == 0:
                    await self.send_message("Please Create Mickey First!", channel_id, who_clicked, to_whom)
                else:
                    sn = the_channel.states[who_clicked]['mickey_num'] - 1
                    the_character_id = the_channel.virtual_characters[f"{self.MICKEY}_{sn}"].character_id
                    await self.update_character(character_id=the_character_id, avatar=image_path, description='Mickey updated name!', name=f'Update Mickey Nick {self.n_usr_update}')
                    await self.send_message(f"Updated Mickey name and image (refresh to see).", channel_id, who_clicked, to_whom)
            elif value == "List Characters".lower():
                char_list = await self.fetch_service_characters()

                await self.send_message(f"Real+Fake character list:\n {pprint.pformat(char_list)}", channel_id, who_clicked, to_whom, len_limit=4096)
                real_ids = await self.fetch_real_character_ids(channel_id, raise_empty_list_err=False)
                await self.send_message(f'Real character ids: {real_ids}', channel_id, to_whom, who_clicked)
                await self.send_message(f'Real character profiles: {await self.fetch_character_profile(real_ids)}', channel_id, who_clicked, to_whom)
            else:
                raise Exception(f'Strange value for button user_btn: {value}')
        elif button_id == "group_btn".lower():
            if value == "List Channel Temp Groups".lower():
                glist = await self.fetch_channel_temp_group(channel_id)
                await self.send_message(f"Channel temp group list (likely empty):\n{pprint.pformat(glist)}", channel_id, who_clicked, to_whom, len_limit=4096)
            elif value == "List Channel Groups".lower():
                glist = await self.fetch_channel_group_list(channel_id)
                await self.send_message(f"Channel group list (likely empty):\n{glist}", channel_id, to_whom, sender=who_clicked, len_limit=4096)
                gdict = await self.http_api.fetch_channel_group_dict(channel_id, self.client_id)
                await self.send_message(f"Channel group, dict form (used internally):\n{pprint.pformat(gdict)}", channel_id, who_clicked, to_whom, len_limit=4096)
            else:
                raise Exception(f'Strange value for button group_btn: {value}')
        elif button_id == "command_btn".lower():
            cmds = """
"moobius": Print "Moobius is Great".
"meow": Have the Agent print nya.
"API": Print one API command per unique socket API call received.
"log agent out": Log out agent, will re-auth next session (the agent may log in again immediatly!).
"agent info": See printout of agent info.
"rename agent foo": Set agent name to foo (need to refresh).
"channel_groups": Have the Agent print channel groups. The Agent is auth'ed with a different servic_id than the Service.
"show_updates": Have the Agent print the most recent update of each kind of update it recieved.
"user_info": Have the Agent print thier own user info.
"show" (send to service): Show buttons and canvas.
"hide" (send to service): Hide buttons and canvas.
"reset" (send to service): Reset mickeys and refresh buttons.
"laser name > message" (send to service): Send a message to a single user only. Messages can be sent to oneself.
""".strip().replace('\n','\n\n')
            await self.send_message(f"Commands (some must be sent to all 'all' some to 'service'):\n{cmds}", channel_id, who_clicked, to_whom)
        else:
            logger.warning(f"Unknown button_id: {button_id}")

    async def on_context_menu_click(self, menu_click):
        """Right-click the context menu."""
        item_id = menu_click.item_id
        message_content = menu_click.message_content
        context_menu_dict = dict(zip([m.item_id for m in self.context_menu_list], self.context_menu_list))
        txt = f'You choose "{context_menu_dict[item_id].item_name}" on message "{message_content} (this message only sent to whoever clicked)".'
        await self.send_message(txt, menu_click.channel_id, menu_click.sender, menu_click.sender)

    async def on_spell(self, spell):
        """Just send the content of the spell to the message."""
        try:
            content, times = spell # The spell can be any object. This Service expects (str, int) tuples.
            content = str(content)
            times = int(times)
        except Exception as e:
            content = f'WARNING: spell error {e}'
            times = 1

        text = f"WAND: {content * times}"

        for channel_id in self.channels.keys():
            the_channel = await self.get_channel(channel_id)
            recipients = list(the_channel.real_characters.keys())
            talker = the_channel.virtual_characters[self.WAND].character_id
            await self.send_message(text, channel_id, talker, recipients)

    ########################### helper functions #####################################

    async def send_buttons_from_database(self, channel_id, character_id):
        """Pipes the buttons (loaded from the JSON) to self.send_update_buttons."""
        button_list = (await self.get_channel(channel_id)).buttons.get(character_id, self._default_buttons) # Contents of buttons.json.
        await self.send_update_buttons(channel_id, button_list, [character_id])

    async def calculate_and_update_character_list_from_database(self, channel_id, character_id):
        """Pipes all real users + the correct number of Mickeys to self.send_update_character_list."""
        the_channel = await self.get_channel(channel_id)
        real_characters = the_channel.real_characters
        character_list = list(real_characters.keys())

        mickey_num = the_channel.states[character_id]['mickey_num']

        for sn in range(mickey_num):
            key = f"{self.MICKEY}_{sn}"
            character_list.append(the_channel.virtual_characters[key].character_id)

        await self.send_update_character_list(channel_id, character_list, [character_id])
