# service.py
import json, sys, asyncio, pprint, os, time, pathlib
import copy
from datetime import datetime

from loguru import logger
from moobius import Moobius, MoobiusStorage, MoobiusWand
from moobius.database.storage import CachedDict
import moobius.types as types
from moobius.types import Button, CanvasItem, StyleItem, MenuItem


class DemoService(Moobius):
    def __init__(self, **kwargs):

        with open('./config/client.json') as f: # Demo-specific config.
            self.client_config = json.load(f)

        super().__init__(**kwargs)

        with open('resources/buttons.json', 'r') as f:
            self._default_buttons = [Button(**b) for b in json.load(f)]
        self.image_show_dict = {}

        _menu = lambda name, the_id, tys: MenuItem(item_text=name, item_id=the_id, message_subtypes=tys)
        menus = [_menu('Text 1', '1', [types.TEXT]), _menu('Text 2', '2', [types.TEXT]), _menu('Text 3', '3', [types.TEXT]),
                 _menu('Image 1', 'R', [types.IMAGE]), _menu('Image 2', 'G', [types.IMAGE]), _menu('Image 3', 'B', [types.IMAGE]),
                 _menu('Audio 1', 'doe', [types.AUDIO]), _menu('Audio 2', 're', [types.AUDIO]), _menu('Audio 3', 'mi', [types.AUDIO]),
                 _menu('File 1', 'Loads', [types.FILE]), _menu('File 2', 'Loading', [types.FILE]), _menu('File 3', 'Loaded', [types.FILE]),
                 _menu('Card 1', 'Ace', [types.CARD]), _menu('Card 2', 'Jack', [types.CARD]), _menu('Card 3', 'King', [types.CARD])]
        self.menu_list = menus
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

    async def on_channel_init(self, channel_id):
        """Initalizes the channel (given by channel_id) with the images and real and puppet characters.
           All of this is stored in a MoobiusStorage object."""

        the_channel = MoobiusStorage(self.client_id, channel_id, db_config=self.db_config)
        self.channel_storages[channel_id] = the_channel

        member_ids = await self.fetch_member_ids(channel_id, raise_empty_list_err=False)

        for character_id, character_profile in zip(member_ids, await self.fetch_character_profile(member_ids)):
            if type(character_id) is not str:
                raise Exception('character_id must be a str.')
            the_channel.real_characters[character_id] = character_profile

            if character_id not in the_channel.buttons:
                the_channel.buttons[character_id] = self.default_buttons

            if character_id not in the_channel.states:
                the_channel.states[character_id] = self.default_status

        for name in self.images: # Once per startup upload images.
            if name not in self.image_paths:
                self.image_paths[name] = await self.upload(self.images[name])

        for sn in range(self.MICKEY_LIMIT):
            key = f"{self.MICKEY}_{sn}"

            if key not in the_channel.puppet_characters:
                image_path = self.image_paths[self.MICKEY]

                the_channel.puppet_characters[key] = await self.create_agent(
                    f'{self.MICKEY} {sn}', image_path, f'I am {self.MICKEY} {sn}!'
                )

        the_channel.puppet_characters[self.WAND] = await self.create_agent(
            self.WAND, self.image_paths[self.WAND], f'I am {self.WAND}!'
        )

        self.image_show_dict = {
            self.LIGHT: CanvasItem(path=self.image_paths[self.LIGHT], text="Let There Be Light!"),
            self.DARK: [CanvasItem(path=self.image_paths[self.DARK], text="Let There Be Dark!"), CanvasItem(path=self.image_paths[self.DARK], text="Let There Be Dark Again!")]
        }

        recipients = list(the_channel.real_characters.keys())
        talker = the_channel.puppet_characters[self.WAND].character_id
        await self.send_message(channel_id, 'Service started on this channel', talker, recipients)
        return the_channel

    async def get_channel(self, channel_id):
        """Prevents KeyErrors by creating new channel databases if they don't exist yet."""
        if channel_id not in self.channel_storages:
            await self.on_channel_init(channel_id)
        return self.channel_storages[channel_id]

    async def on_message_down(self, message_down):
        pass

    async def on_update(self, the_update):
        pass

    async def on_message_up(self, message_up):
        """Runs various commands, such as resetting when the user types in "reset"."""
        channel_id = message_up.channel_id
        recipients = message_up.recipients
        sender = message_up.sender
        to_whom = await self.fetch_member_ids(channel_id, raise_empty_list_err=False) if self.client_config['show_us_all'] else [sender]

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
                else:
                    await self.send_message(txt, channel_id, sender, recipients)
            else: # DEMO: commands to Service(Infinity)
                if txt1 == "hide":
                    for usr in to_whom:
                        if usr in the_channel.buttons:
                            the_channel.buttons[sender] = []
                    await self.send_buttons_from_database(channel_id, sender)
                    await self.send_style([StyleItem(widget=types.CANVAS, display="invisible", expand=False)], channel_id, to_whom)
                elif txt1 == "show":
                    for usr in to_whom:
                        if usr in the_channel.buttons:
                            the_channel.buttons[sender] = self.default_buttons
                    await self.send_buttons_from_database(channel_id, sender)
                    await self.send_style([StyleItem(widget=types.CANVAS, display="visible", expand=True)], channel_id, to_whom)
                elif txt1 == "reset":
                    for sn in range(self.MICKEY_LIMIT):
                        the_character_id = the_channel.puppet_characters[f"{self.MICKEY}_{sn}"].character_id
                        await self.update_agent(agent_id=the_character_id, avatar=self.image_paths[self.MICKEY], description='Mickey reset!', name=f'Mickey {sn}')

                    for usr in to_whom:
                        if usr in the_channel.states:
                            the_channel.states[usr]['mickey_num'] = 0
                            the_channel.states.save(usr)

                    await self.calculate_and_update_character_list_from_database(channel_id, sender)
                    the_channel = await self.get_channel(channel_id) # TODO: why call this twice?
                    for usr in to_whom:
                        if usr in the_channel.buttons:
                            the_channel.buttons[sender] = self.default_buttons # Reset buttons etc.
                    await self.send_buttons(self.default_buttons, channel_id, to_whom)
                else:
                    txt = txt+' (this message has no recipients, either it was sent to service or there is a bug).'
                    await self.send_message(txt, channel_id, sender, to_whom)
        else:
            await self.send_message(message_up) # This is so that everyone can see the message you sent.

    async def on_refresh(self, action):
        await self.calculate_and_update_character_list_from_database(action.channel_id, action.sender)

        await self.send_buttons_from_database(action.channel_id, action.sender)

        """Pipes self.image_show_dict from channel.states into self.send_canvas."""
        channel_id = action.channel_id
        sender = action.sender
        the_channel = await self.get_channel(channel_id)
        to_whom = await self.fetch_member_ids(channel_id, raise_empty_list_err=False) if self.client_config['show_us_all'] else [sender]

        state = the_channel.states[sender]['canvas_mode']
        await self.send_canvas(self.image_show_dict[state], channel_id, to_whom)
        await self.send_style([StyleItem(widget=types.CANVAS, display="visible", expand=True)], channel_id, to_whom)

    async def add_real_character(self, channel_id, character_id, intro="joined the channel!"):
        character = await self.fetch_character_profile(character_id)
        name = character.name
        the_channel = await self.get_channel(channel_id)

        the_channel.real_characters[character_id] = character
        the_channel.buttons[character_id] = self.default_buttons
        the_channel.states[character_id] = self.default_status

        character_ids = list(the_channel.real_characters.keys())
        await self.send_characters(character_ids, channel_id, character_ids)
        await self.send_message(f'{name} {intro} (id={character_id})', channel_id, character_id, character_ids)

    async def on_join_channel(self, action):
        """Most join handlers, as this one does, will send_characters with the new character added and send a "user joined!" message."""
        sender_id = action.sender
        channel_id = action.channel_id
        await self.add_real_character(channel_id, sender_id, intro="joined the channel!")

    async def on_leave_channel(self, action):
        """Most leave handlers, as this one does, will send_characters with the character removed and maybe send a "user left!" message."""
        sender = action.sender
        channel_id = action.channel_id
        character = (await self.get_channel(action.channel_id)).real_characters.pop(sender, None)
        (await self.get_channel(channel_id)).states.pop(sender, None)
        (await self.get_channel(channel_id)).buttons.pop(sender, None)
        name = character.name

        real_characters = (await self.get_channel(channel_id)).real_characters
        character_ids = list(real_characters.keys())

        await self.send_characters(character_ids, channel_id, character_ids)
        await self.send_message(f'{name} left the channel!', channel_id, sender, character_ids)

    async def on_copy_client(self, the_copy):
        await super().on_copy_client(the_copy) # One of the few callbacks to have an action.

    async def on_update_style(self, update):
        pass

    async def on_update_buttons(self, update):
        pass

    async def on_update_canvas(self, update):
        pass

    async def on_update_characters(self, update):
        pass

    async def on_button_click(self, button_click):
        """Called when the user presses a button (and selecting an option of a list appears). button_click is a ButtonClick object.
           This is a major switchyard which handles most of the different buttons in the demo."""
        channel_id = button_click.channel_id
        button_id = button_click.button_id.lower()
        who_clicked = button_click.sender
        the_channel = await self.get_channel(channel_id)

        to_whom = await self.fetch_member_ids(channel_id, raise_empty_list_err=False) if self.client_config['show_us_all'] else [who_clicked]

        value = None
        if button_click.arguments:
            value0 = button_click.arguments[0].value
            value = value0.lower()

        def _make_image(vignette=0.0):
            """Generates a "random" image and returns the local file_path (as a string) as well as a removal function (if the image is dynamic)."""
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
            if value == 'Text'.lower():
                import random
                some_text = ((str(random.random())+'   ')[0:3])*int(random.random()*12+3)
                await self.send_message(some_text, channel_id, who_clicked, to_whom)
            elif value == 'Card'.lower():
                card_message = {'link':'https://neocities.org/', 'title':'Where have all the websites gone?', 'button':'Here!',
                                'text':'Domain names? Urls? wwwdotcoms?'}
                await self.send_message(card_message, channel_id, who_clicked, to_whom, subtype=types.CARD)
            elif value == 'Image'.lower():
                file_path, rm_fn = _make_image(0.0)
                path_obj = pathlib.Path(file_path) # Conversion to a Path makes the Moobius class recognize it as an image.
                await self.send_message(path_obj, channel_id, who_clicked, to_whom)
                rm_fn()
            elif value == 'Audio'.lower():
                await self.send_message(pathlib.Path('./resources/tiny.mp3'), channel_id, who_clicked, to_whom)
            elif value == 'File'.lower():
                await self.send_message(pathlib.Path('./resources/tiny.pdf'), channel_id, who_clicked, to_whom)
            elif value == 'Swap Canvas'.lower():
                if the_channel.states[who_clicked]['canvas_mode'] == self.LIGHT: 
                    the_channel.states[who_clicked]['canvas_mode'] = self.DARK
                else:
                    the_channel.states[who_clicked]['canvas_mode'] = self.LIGHT

                the_channel.states.save(who_clicked)
                state = the_channel.states[who_clicked]['canvas_mode']
                await self.send_canvas(self.image_show_dict[state], channel_id, to_whom)

                image_uri = self.image_paths[state] # Shows using an online image.
                await self.send_message(image_uri, channel_id, who_clicked, to_whom, subtype=types.IMAGE)
            elif value == "Fancy Right Click".lower():
                await self.send_menu(self.menu_list, channel_id, to_whom)
                await self.send_message("Try right-clicking on a message.", channel_id, who_clicked, to_whom)
            else:
                raise Exception(f'Strange value for button channel_btn: {value}')
        elif button_id == "channel_btn".lower():
            extra_channel_ids = list(self.xtra_channels.keys())
            if value == "New Channel".lower():
                channel_name = '>>Demo TEMP channel'+str(len(extra_channel_ids))
                new_channel_id = await self.create_channel(channel_name, 'Channel created by the GUI.')
                await self.on_channel_init(new_channel_id) # Prevents KeyErrors.
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
                         if c_id in self.channel_storages:
                             del self.channel_storages[c_id]
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
            elif value == "List All Channels".lower():
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
            else:
                raise Exception(f'Strange value for button channel_btn: {value}')
        elif button_id == "user_btn".lower():
            if not hasattr(self, 'n_usr_update'):
                self.n_usr_update = -1
            self.n_usr_update += 1
            image_list = [self.image_paths[x] for x in [self.LIGHT, self.DARK, self.WAND]]
            image_path = image_list[self.n_usr_update%len(image_list)] # Cycle through non-mickey images.

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
                    talker = the_channel.puppet_characters[f"{self.MICKEY}_{sn}"].character_id
                    await self.send_message(f"Mickey {sn} Here! Mickeys are stored in JSON db.", channel_id, talker, to_whom)
            elif value == "update mickey (not user) name".lower():
                if the_channel.states[who_clicked]['mickey_num'] == 0:
                    await self.send_message("Please Create Mickey First!", channel_id, who_clicked, to_whom)
                else:
                    sn = the_channel.states[who_clicked]['mickey_num'] - 1
                    the_character_id = the_channel.puppet_characters[f"{self.MICKEY}_{sn}"].character_id
                    await self.update_agent(agent_id=the_character_id, avatar=image_path, description='Mickey updated name!', name=f'Update Mickey Nick {self.n_usr_update}')
                    await self.send_message(f"Updated Mickey name and image (refresh to see).", channel_id, who_clicked, to_whom)
            elif value == "List Characters".lower():
                char_list = await self.fetch_agents()

                await self.send_message(f"Puppet id list:\n {pprint.pformat(char_list)}", channel_id, who_clicked, to_whom, len_limit=4096)
                real_ids = await self.fetch_member_ids(channel_id, raise_empty_list_err=False)
                await self.send_message(f'Member ids: {real_ids}', channel_id, to_whom, who_clicked)
                await self.send_message(f'Member profiles: {await self.fetch_character_profile(real_ids)}', channel_id, who_clicked, to_whom)
            else:
                raise Exception(f'Strange value for button user_btn: {value}')
        elif button_id == "command_btn".lower():
            cmds = """
"show" (send to service): Show buttons and canvas.
"hide" (send to service): Hide buttons and canvas.
"reset" (send to service): Reset mickeys and refresh buttons.
""".strip().replace('\n','\n\n')
            await self.send_message(f"Commands (some must be sent to all 'all' some to 'service'):\n{cmds}", channel_id, who_clicked, to_whom)
        else:
            logger.warning(f"Unknown button_id: {button_id}")

    async def on_menu_item_click(self, menu_click):
        """Right-click the context menu."""
        item_id = menu_click.item_id
        message_content = menu_click.message_content
        menu_dict = dict(zip([m.item_id for m in self.menu_list], self.menu_list))
        txt = f'You choose "{menu_dict[item_id].item_text}" on message "{message_content} (this message only sent to whoever clicked)".'
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

        for channel_id in self.channel_storages.keys():
            the_channel = await self.get_channel(channel_id)
            recipients = list(the_channel.real_characters.keys())
            talker = the_channel.puppet_characters[self.WAND].character_id
            await self.send_message(text, channel_id, talker, recipients)

    ########################### helper functions #####################################

    async def send_buttons_from_database(self, channel_id, character_id):
        """Pipes the buttons (loaded from the JSON) to self.send_buttons."""
        button_list = (await self.get_channel(channel_id)).buttons.get(character_id, self._default_buttons) # Contents of buttons.json.
        await self.send_buttons(button_list, channel_id, [character_id])

    async def calculate_and_update_character_list_from_database(self, channel_id, character_id):
        """Pipes all real users + the correct number of Mickeys to self.send_characters."""
        the_channel = await self.get_channel(channel_id)
        real_characters = the_channel.real_characters
        character_list = list(real_characters.keys())

        mickey_num = the_channel.states[character_id]['mickey_num']

        for sn in range(mickey_num):
            key = f"{self.MICKEY}_{sn}"
            character_list.append(the_channel.puppet_characters[key].character_id)

        await self.send_characters(character_list, channel_id, [character_id])


if __name__ == "__main__":
    MoobiusWand().run(DemoService, config='config/config.json')