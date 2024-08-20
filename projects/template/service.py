# service.py
import json, sys, asyncio, pprint, os, time, pathlib
import copy
from datetime import datetime

from loguru import logger
from moobius import Moobius, MoobiusStorage, MoobiusWand
from moobius.database.storage import CachedDict
import moobius.types as types
from moobius.types import Button, CanvasItem, StyleItem, MenuItem

example_socket_callback_payloads = {} # Print these out when the AI is done.

class TemplateService(Moobius):
    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        with open('./config/client.json') as f: # Demo-specific config.
            self.client_config = json.load(f)

        with open('resources/buttons.json', 'r') as f:
            self._default_buttons = [Button(**b) for b in json.load(f)]
        self.image_show_dict = {}

        self.mickey_LIMIT = 5

        self.images = {
            "light": "resources/light.png",
            "dark": "resources/dark.png",
            "Mickey": "resources/Mickey.jpg",
            "wand": "resources/wand.png"
        }
        self.image_paths = {}
        self.database_debugs = {}

        self._default_status = {
            'canvas_mode': "light",
            'Mickey_num': 0
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

        for sn in range(self.mickey_LIMIT):
            key = f"Mickey_{sn}"

            if key not in the_channel.puppet_characters:
                image_path = self.image_paths["Mickey"]
                the_channel.puppet_characters[key] = await self.create_agent(
                    f'Mickey {sn}', image_path, f'I am Mickey {sn}!'
                )

        the_channel.puppet_characters["wand"] = await self.create_agent(
            "wand", self.image_paths["wand"], f'I am Wand!'
        )

        self.image_show_dict = {
            "light": CanvasItem(path=self.image_paths["light"], text="Let There Be Light!"),
            "dark": [CanvasItem(path=self.image_paths["dark"], text="Let There Be Dark!"), CanvasItem(path=self.image_paths["dark"], text="Let There Be Dark Again!")]
        }

        recipients = list(the_channel.real_characters.keys())
        talker = the_channel.puppet_characters["wand"].character_id
        await self.send_message(channel_id, 'Service started on this channel', talker, recipients)
        return the_channel

    async def get_channel(self, channel_id):
        """Prevents KeyErrors by creating new channel databases if they don't exist yet."""
        if channel_id not in self.channel_storages:
            await self.on_channel_init(channel_id)
        return self.channel_storages[channel_id]

    async def on_start(self):
        """Called after successful connection to websocket server and service login success.
           Searches for extra channels bound to this service."""
        pass

    async def on_message_down(self, message_down):
        pass

    async def on_update(self, the_update):
        pass

    async def on_message_up(self, message_up):
        """Runs various commands, such as resetting when the user types in "reset".
           (Agent-related commands are found in the agent.py instead of here)."""
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
                    for sn in range(self.mickey_LIMIT):
                        the_character_id = the_channel.puppet_characters[f"Mickey_{sn}"].character_id
                        await self.update_agent(agent_id=the_character_id, avatar=self.image_paths["Mickey"], description='Mickey reset!', name=f'Mickey {sn}')

                    for usr in to_whom:
                        if usr in the_channel.states:
                            the_channel.states[usr]['Mickey_num'] = 0
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
        example_socket_callback_payloads['on_message_up'] = message_up

    async def on_refresh(self, action):
        await self.calculate_and_update_character_list_from_database(action.channel_id, action.sender)
        sender = action.sender
        to_whom = await self.fetch_member_ids(action.channel_id, raise_empty_list_err=False) if self.client_config['show_us_all'] else [sender]
        if hasattr(self, 'TMP_print_buttons') and getattr(self, 'TMP_print_buttons'): # Set to True to indicate an extra call to print the buttons.
            self.TMP_print_buttons = False
            channel_id = action.channel_id
            await self.send_message(f"Fetch button action\n: {action}.", channel_id, sender, to_whom)
        else:
            await self.send_buttons_from_database(action.channel_id, sender)

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
        example_socket_callback_payloads['on_join_channel'] = action
        sender_id = action.sender
        channel_id = action.channel_id
        await self.add_real_character(channel_id, sender_id, intro="joined the channel!")

    async def on_leave_channel(self, action):
        """Most leave handlers, as this one does, will send_characters with the character removed and maybe send a "user left!" message."""
        example_socket_callback_payloads['on_leave_channel'] = action
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

        to_whom = await self.fetch_member_ids(channel_id, raise_empty_list_err=False) if self.client_config['show_us_all'] else [who_clicked]

        value = None
        if button_click.arguments:
            value0 = button_click.arguments[0].value
            value = value0.lower()

        if button_id == "message_btn".lower():
            if value == 'Text'.lower():
                import random
                some_text = ((str(random.random())+'   ')[0:3])*int(random.random()*12+3)
                await self.send_message(some_text, channel_id, who_clicked, to_whom)
            elif value == 'Image'.lower():
                file_path = './resources/Mickey.jpg'
                path_obj = pathlib.Path(file_path) # Conversion to a Path makes the Moobius class recognize it as an image.
                await self.send_message(path_obj, channel_id, who_clicked, to_whom)
        elif button_id == "user_btn".lower():
            if not hasattr(self, 'n_usr_update'):
                self.n_usr_update = -1
            self.n_usr_update += 1

            if value == 'Make Mickey'.lower():
                if the_channel.states[who_clicked]['Mickey_num'] >= self.mickey_LIMIT:
                    await self.send_message("You have reached the limit of Mickey!", channel_id, who_clicked, to_whom)
                else:
                    the_channel.states[who_clicked]['Mickey_num'] += 1
                    the_channel.states.save(who_clicked)

                    await self.calculate_and_update_character_list_from_database(channel_id, who_clicked)
            elif value == 'Mickey Talk'.lower():
                if the_channel.states[who_clicked]['Mickey_num'] == 0:
                    await self.send_message("Please Create Mickey First!", channel_id, who_clicked, to_whom)
                else:
                    sn = the_channel.states[who_clicked]['Mickey_num'] - 1
                    talker = the_channel.puppet_characters[f"Mickey_{sn}"].character_id
                    await self.send_message(f"Mickey {sn} Here! Mickeys are stored in JSON db.", channel_id, talker, to_whom)
        elif button_id == "command_btn".lower():
            cmds = """
"show" (send to service): Show buttons and canvas.
"hide" (send to service): Hide buttons and canvas.
"reset" (send to service): Reset Mickeys and refresh buttons.
""".strip().replace('\n','\n\n')
            await self.send_message(f"Commands (must be sent to 'service'):\n{cmds}", channel_id, who_clicked, to_whom)
        else:
            logger.warning(f"Unknown button_id: {button_id}")

    async def on_menu_item_click(self, menu_click):
        """Context menus open on right-click and can be enabled with send_menu()."""
        pass

    async def on_spell(self, spell):
        """Spells from Wand can be any pickelable object and can come from other processes."""
        pass

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

        Mickey_num = the_channel.states[character_id]['Mickey_num']

        for sn in range(Mickey_num):
            key = f"Mickey_{sn}"
            character_list.append(the_channel.puppet_characters[key].character_id)

        await self.send_characters(character_list, channel_id, [character_id])


if __name__ == "__main__":
    MoobiusWand().run(TemplateService, config='config/config.json')