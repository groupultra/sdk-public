# service.py
import json, sys, asyncio
import copy
from datetime import datetime

from loguru import logger
from moobius import SDK, MoobiusStorage
from moobius.types import Button

avoid_redis_on_windoze = True # Redis requires WSL2 to run on windows since it is Linux-only.
avoid_redis = (avoid_redis_on_windoze and (sys.platform.lower() in ['win', 'win32', 'win64', 'windows', 'windoze'])) or avoid_redis_on_windoze == 'also linux'
load_xtra_channels_on_start = True

example_socket_callback_payloads = {} # Print these out when the AI is done.

class DemoService(SDK):
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

        self.LIGHT = "light"
        self.DARK = "dark"
        self.MICKEY = "Mickey"
        self.WAND = "Wand"
        self.MICKEY_LIMIT = 5

        self.image_paths = {}

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
        self.left_channels = []

    @property
    def default_status(self):
        return copy.deepcopy(self._default_status)

    @property
    def default_buttons(self):
        return copy.deepcopy(self._default_buttons)

    async def initialize_channel(self, channel_id):
        """Initalizes the channel (given by channel_id) with the images and real and virtual characters.
           All of this is stored in a MoobiusStorage object."""
        the_channel = MoobiusStorage(self.client_id, channel_id, db_config=self.db_config)
        self.channels[channel_id] = the_channel

        real_user_ids = await self.fetch_channel_users(channel_id, raise_empty_list_err=False)

        for character_id in real_user_ids:
            the_channel.real_characters[character_id] = await self.fetch_user_profile(character_id)

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
                    self.MICKEY, f'{self.MICKEY} {sn}', image_path, f'I am {self.MICKEY} {sn}!'
                )

        the_channel.virtual_characters[self.WAND] = await self.create_character(
            self.WAND, self.WAND, self.image_paths[self.WAND], f'I am {self.WAND}!'
        )

        self.image_show_dict = {
            self.LIGHT: {
                "path": self.image_paths[self.LIGHT],
                "text": "Let There Be Light!"
            },

            self.DARK: {
                "path": self.image_paths[self.DARK],
                "text": "Let There Be Dark!"
            }
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

        channel2service = await self.fetch_bound_channels()
        for c_id, s_id in channel2service.items():
            if s_id == self.client_id and c_id not in self.channels:
                if load_xtra_channels_on_start:
                    logger.info(f'EXTRA channel bound to this service on startup will be added: {c_id}')
                    await self.initialize_channel(c_id)
                else:
                    logger.info(f'EXTRA channel bound to this service on startup will NOT be added b/c load_xtra_channels_on_start is False: {c_id}')

    async def cron_task(self):
        """Sends a check-in message to each channel."""
        for channel_id in self.channels.keys():
            the_channel = await self.get_channel(channel_id)
            recipients = list(the_channel.real_characters.keys())
            talker = the_channel.virtual_characters[self.WAND].user_id
            txt = f"Check in every minute! {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            await self.create_message(channel_id, txt, recipients, sender=talker)

    async def on_message_down(self, message_down):
        """This and several other callbacks only exist to record the API calls."""
        example_socket_callback_payloads['on_message_down'] = message_down

    async def on_update(self, the_update):
        """This and several other callbacks only exist to record the API calls."""
        example_socket_callback_payloads['on_update'] = the_update

    async def on_message_up(self, message_up):
        """Runs various commands, such as resetting when the user types in "reset".
           (Agent-related commands are found in the agent.py instead of here)."""
        example_socket_callback_payloads['on_message_up'] = message_up
        if message_up.subtype == "text":
            txt = message_up.content['text']
            channel_id = message_up.channel_id
            sender = message_up.sender
            if type(sender) is not str:
                raise Exception(f'Sender must be a string, instead it is: {sender}')
            recipients = message_up.recipients
            the_channel = await self.get_channel(channel_id)

            if recipients: # DEMO: text modification
                if txt.lower() == "moobius":
                    await self.create_message(channel_id, "Moobius is Great!", recipients, sender=sender)
                elif txt.lower() == "api":
                    lines = []
                    for k,v in example_socket_callback_payloads.items():
                        lines.append(k+': '+str(v))
                    txt = '\n\n'.join(lines)
                    await self.create_message(channel_id, 'Socket api call examples recorded:\n'+txt, recipients, sender=sender)
                else:
                    await self.create_message(channel_id, txt, recipients, sender=sender)
                    #await self.send(payload_type='message_down', payload_body=message_up) # equivalent.
            else: # DEMO: commands to Service(Infinity)
                if txt.lower() == "hide":
                    the_channel.buttons[sender] = []
                    await self.send_buttons_from_database(channel_id, sender)
                elif txt.lower() == "show":
                    the_channel.buttons[sender] = self.default_buttons
                    await self.send_buttons_from_database(channel_id, sender)
                elif txt.lower() == "reset":

                    for sn in range(self.MICKEY_LIMIT):
                        the_user_id = the_channel.virtual_characters[f"{self.MICKEY}_{sn}"].user_id
                        await self.update_character(user_id=the_user_id, username=f'Mickey {sn} uname', avatar=self.image_paths[self.MICKEY], description='Mickey restet!', name=f'Mickey {sn}')

                    the_channel.states[sender]['mickey_num'] = 0
                    the_channel.states.save(sender)

                    await self.calculate_and_update_user_list_from_database(channel_id, sender)
                    the_channel = await self.get_channel(channel_id) # TODO: why call this twice?
                    the_channel.buttons[sender] = self.default_buttons # Reset buttons etc.
                    await self.send_update_buttons(channel_id, self.default_buttons, [sender])
                else:
                    pass

        # DEMO: other message types.
        else:
            await self.create_message(channel_id, str(message_up), recipients, sender=sender) # Not sure if this works or the generic next line is needed?
            #await self.send(payload_type='message_down', payload_body=message_up)

    async def on_fetch_user_list(self, action):
        example_socket_callback_payloads['on_fetch_user_list'] = action
        await self.calculate_and_update_user_list_from_database(action.channel_id, action.sender)

    async def on_fetch_buttons(self, action):
        example_socket_callback_payloads['on_fetch_buttons'] = action
        if hasattr(self, 'TMP_print_buttons') and getattr(self, 'TMP_print_buttons'): # Set to True to indicate an extra call to print the buttons.
            self.TMP_print_buttons = False
            channel_id = action.channel_id
            sender = action.sender
            await self.create_message(channel_id, f"Fetch button action\n: {action}.", [sender], sender=sender)
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

        state = the_channel.states[sender]['canvas_mode']
        await self.send_update_canvas(channel_id, self.image_show_dict[state], [sender])

        content = [
            {
                "widget": "canvas",
                "display": "visible",
                "expand": "true"
            }
        ]

        await self.send_update_style(channel_id, content, [sender])

    async def on_join_channel(self, action):
        """Most join handlers, as this one does, will send_update_user_list with the new character added and send a "user joined!" message."""
        example_socket_callback_payloads['on_join_channel'] = action
        sender_id = action.sender
        channel_id = action.channel_id
        character = await self.fetch_user_profile(sender_id)
        name = character.user_context.name
        the_channel = await self.get_channel(channel_id)

        the_channel.real_characters[sender_id] = character
        the_channel.buttons[sender_id] = self.default_buttons
        the_channel.states[sender_id] = self.default_status

        character_ids = list(the_channel.real_characters.keys())
        await self.send_update_user_list(channel_id, character_ids, character_ids)
        await self.create_message(channel_id, f'{name} joined the channel!', character_ids, sender=sender_id)

    async def on_leave_channel(self, action):
        """Most leave handlers, as this one does, will send_update_user_list with the character removed and maybe send a "user left!" message."""
        example_socket_callback_payloads['on_leave_channel'] = action
        sender = action.sender
        channel_id = action.channel_id
        character = (await self.get_channel(action.channel_id)).real_characters.pop(sender, None)
        (await self.get_channel(channel_id)).states.pop(sender, None)
        (await self.get_channel(channel_id)).buttons.pop(sender, None)
        name = character.user_context.name

        real_characters = (await self.get_channel(channel_id)).real_characters
        character_ids = list(real_characters.keys())

        await self.send_update_user_list(channel_id, character_ids, character_ids)
        await self.create_message(channel_id, f'{name} left the channel!', character_ids, sender=sender)

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

    async def on_update_userlist(self, x):
        example_socket_callback_payloads['on_update_userlist'] = x

    async def on_button_click(self, button_click):
        """Called when the user presses a button (and selecting an option of a list appears). button_click is a Button object.
           This is a major switchyard which handles most of the different buttons in the demo."""
        example_socket_callback_payloads['on_button_click'] = button_click
        channel_id = button_click.channel_id
        button_id = button_click.button_id.lower()
        who_clicked = button_click.sender
        the_channel = await self.get_channel(channel_id)

        character = the_channel.real_characters[who_clicked]
        name = character.user_context.name
        recipients = list(the_channel.real_characters.keys())

        redis_txt = 'not-the-Redis' if avoid_redis else 'Redis'
        value = None
        if button_click.arguments:
            value0 = button_click.arguments[0].value
            value = value0.lower()
        if button_id == "canvas_btn".lower():
            if the_channel.states[who_clicked]['canvas_mode'] == self.LIGHT: 
                 the_channel.states[who_clicked]['canvas_mode'] = self.DARK
            else:
                 the_channel.states[who_clicked]['canvas_mode'] = self.LIGHT

            the_channel.states.save(who_clicked)
            state = the_channel.states[who_clicked]['canvas_mode']
            await self.send_update_canvas(channel_id, self.image_show_dict[state], [who_clicked])

            image_uri = self.image_paths[state]
            await self.create_message(channel_id, image_uri, [who_clicked], subtype='image', sender=who_clicked)
        elif button_id == "money_btn".lower():
            if value == '(Print Savings)'.lower() or value == '(Donate all)'.lower():
                if value == '(Donate all)'.lower():
                    tot = 0
                    for k in the_channel.currency.keys():
                        tot += the_channel.currency[k]
                        the_channel.currency[k] = 0
                    await self.create_message(channel_id, f"{tot} weeks of savings donated to mysterious unknown charities.", [who_clicked], sender=who_clicked)
                desc = []
                unicode_map = {'naira':'₦', 'dollar':'$', 'peso':'₱', 'yuan':'¥', 'euro': '€', 'kina':'K', 'penguin':'🐧'}
                for k in the_channel.currency.keys():
                    desc.append(f'{unicode_map[k.lower()]}={the_channel.currency[k]}')
                desc = '['+', '.join(desc)+']'
                await self.create_message(channel_id, f"{redis_txt} query; number of weeks of living expenses saved in each currency:\n {desc}", [who_clicked], sender=who_clicked)
            else:
                msg_map = {'naira':'Nigerian', 'dollar':'American', 'peso':'Chilean', 'yuan':'Chinese', 'euro': 'West European', 'kina':'Papua New Guinean', 'penguin':'Antarctican'}

                await self.create_message(channel_id, f"You earn two weeks salary of {msg_map[value]}. Your bank account will be stored in {redis_txt}!", [who_clicked], sender=who_clicked)

                if value0 not in the_channel.currency:
                    the_channel.currency[value0] = 0
                the_channel.currency[value0] += 2 # Number of weeks.
        elif button_id == "channel_btn".lower():
            #channel2service = self.fetch_bound_channels() TODO
            extra_channel_ids = list(self.xtra_channels.keys())
            if value == "New Channel".lower():
                channel_name = '>>Demo TEMP channel'+str(len(extra_channel_ids))
                new_channel_id = await self.create_and_bind_channel(channel_name, 'Channel created by the GUI.')
                await self.initialize_channel(new_channel_id) # Prevents KeyErrors.
                self.xtra_channels[new_channel_id] = 'A channel'
                await self.create_message(channel_id, f"New channel created, refresh and it should appear on the left bar: {channel_name} ({new_channel_id})", [who_clicked], sender=who_clicked)
            elif value == "Ping Channels".lower():
                tasks = [self.create_message(channel_id, f"Pinging Channel ids: {extra_channel_ids} (one ping message should show up in each channel)", [who_clicked], sender=who_clicked)]
                for extra_channel_id in extra_channel_ids + self.left_channels: # Ideally the left out channels should no longer respond.
                    tasks.append(self.create_message(extra_channel_id, f"Ping from channel {channel_id} to channel {extra_channel_id}!", [who_clicked], sender=who_clicked))
                await asyncio.wait(tasks)
            elif value == "Reset Extra Channels".lower():
                await self.create_message(channel_id, f"Leaving Channel ids: {extra_channel_ids}", [who_clicked], sender=who_clicked)
                tasks = []
                for channel_id in extra_channel_ids:
                    tasks.append(self.send_leave_channel(channel_id))
                    if channel_id in self.channels: # Should always be.
                        del self.channels[channel_id]
                self.xtra_channels = {}
                if tasks:
                    await asyncio.wait(tasks)
                self.left_channels += extra_channel_ids
            elif value == "Fetch Channel List".lower():
                x = await self.fetch_channel_list()
                await self.create_message(channel_id, f"Channel list:\n{str(x)}", [who_clicked], sender=who_clicked)
                x = await self.fetch_popular_channels()
                await self.create_message(channel_id, f"Popular channel list:\n{str(x)}", [who_clicked], sender=who_clicked)
            elif value == "Update Extra Channels".lower():
                extra_channel_ids = list(self.xtra_channels.keys())
                ix = 0
                for bid in extra_channel_ids:
                    await self.update_channel(bid, f'<>DemoTmpChannel{ix}<>', 'Pressed the update extra channels button.')
                    ix = ix+1
                await self.create_message(channel_id, f"Updated these channel names (refresh to see changes):\n{extra_channel_ids}", [who_clicked], sender=who_clicked)
            elif value == "Fetch Chat History".lower():
                history = await self.fetch_history_message(channel_id, limit=6, before="null")
                await self.create_message(channel_id, f"Recent chat history of this channel:\n{history}", [who_clicked], sender=who_clicked)
            elif value == "Fetch Buttons".lower():
                print('Asking for Buttons (will have to wait for the WS to get back).')
                self.TMP_print_buttons = True
                await self.send_fetch_buttons(channel_id)
            elif value == "Fancy Right Click".lower():
                await self.create_message(channel_id, "WARNING: this feature only works on the .link version.", [who_clicked], sender=who_clicked)
                button_data = {'a':1, 'b':2, 'c':3}
                await self.send_update_rclick_buttons(channel_id, button_data, [who_clicked])
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
                    await self.create_message(channel_id, "You have reached the limit of Mickey!", [who_clicked], sender=who_clicked)
                else:
                    the_channel.states[who_clicked]['mickey_num'] += 1
                    the_channel.states.save(who_clicked)

                    await self.calculate_and_update_user_list_from_database(channel_id, who_clicked)
            elif value == 'Mickey Talk'.lower():
                if the_channel.states[who_clicked]['mickey_num'] == 0:
                    await self.create_message(channel_id, "Please Create Mickey First!", [who_clicked], sender=who_clicked)
                else:
                    sn = the_channel.states[who_clicked]['mickey_num'] - 1
                    talker = the_channel.virtual_characters[f"{self.MICKEY}_{sn}"].user_id
                    await self.create_message(channel_id, f"Mickey {sn} Here! Mickeys are stored in JSON db.", [who_clicked], sender=talker)
            elif value == "Update Mickey (not agent) name".lower():
                if the_channel.states[who_clicked]['mickey_num'] == 0:
                    await self.create_message(channel_id, "Please Create Mickey First!", [who_clicked], sender=who_clicked)
                else:
                    sn = the_channel.states[who_clicked]['mickey_num'] - 1
                    the_user_id = the_channel.virtual_characters[f"{self.MICKEY}_{sn}"].user_id
                    await self.update_character(user_id=the_user_id, username='Updated Mickey Name', avatar=image_path, description='Mickey updated name!', name=f'Update Mickey Nick {self.n_usr_update}')
                    await self.create_message(channel_id, f"Updated Mickey name and image (refresh to see).", [who_clicked], sender=who_clicked)
            elif value == "List Characters".lower():
                await self.create_message(channel_id, f"Warning! This feature broken in the .app version.", [who_clicked], sender=who_clicked)
                char_list = await self.fetch_character_list()
                await self.create_message(channel_id, f"Character list:\n {char_list}", [who_clicked], sender=who_clicked)
            else:
                raise Exception(f'Strange value for button user_btn: {value}')
        elif button_id == "group_btn".lower(): # Not usable in the .app, only usable in the .link.
            await self.create_message(channel_id, f"WARNING: Groups are a .link feature only!", [who_clicked], sender=who_clicked)
            #def _find_matching_group(the_list, member_id): # May never be needed.
            #    """Matching group_id to a user or channel id inside the list."""
            #    for l in the_list:
            #        if member_id in l.members:
            #            return l.group_id
            #    raise Exception("Cannot find matching group_id")
            if value == "Group Service's Channels".lower():
                channel_id_list = (await self.fetch_bound_channels())[self.client_id]
                group_name = 'ChDemoGroup101'
                await self.create_message(channel_id, f"Creating channel group named {group_name} with these channels: {channel_id_list}", [who_clicked], sender=who_clicked)
                await self.create_channel_group(channel_id, group_name, channel_id_list)
            elif value == "List Channel Groups".lower():
                await self.create_message(channel_id, f"Listing channel groups.", [who_clicked], sender=who_clicked)
                glist = await self.fetch_channel_group_list(channel_id)
                await self.create_message(channel_id, f"Channel group list:\n{glist}", [who_clicked], sender=who_clicked)
            else:
                raise Exception(f'Strange value for button group_btn: {value}')
        elif button_id == "command_btn".lower():
            cmds = '"moobius": Print Moobius is Great msg.\n\n"meow": Have Agent print nya.\n\n"reset": Reset mickeys and refresh buttons.\n\n"API": Print special socket API doc.\n\n"log agent out": Log out agent, will re-auth next session.\n\n"agent info": See printout of agent info.\n\n"rename agent foo": Set agent name to foo. "show": Show buttons. "hide": Hide buttons.'
            await self.create_message(channel_id, f"Commands (some get sent to all 'all' some to 'service'):\n{cmds}", [who_clicked], sender=who_clicked)
        else:
            logger.warning(f"Unknown button_id: {button_id}")

    async def on_context_rclick(self, menu_click):
        raise Exception('TODO: handle this.')

    async def on_unknown_message(self, message_data):
        example_socket_callback_payloads['on_button_click'] = message_data
        logger.warning(f"Received unknown message: {message_data}")

    async def on_spell(self, spell):
        """Just send the content of the spell to the message."""
        try:
            content, times = spell
            content = str(content)
            times = int(times)
        except:
            content = 'DEFAULT'
            times = 1

        text = f"WAND: {content * times}"

        for channel_id in self.channels.keys():
            the_channel = await self.get_channel(channel_id)
            recipients = list(the_channel.real_characters.keys())
            talker = the_channel.virtual_characters[self.WAND].user_id
            await self.create_message(channel_id, text, recipients, sender=talker)

    ########################### helper functions #####################################

    async def send_buttons_from_database(self, channel_id, character_id):
        """Pipes the buttons (loaded from the JSON) to self.send_update_buttons."""
        button_data_list = (await self.get_channel(channel_id)).buttons.get(character_id, self._default_buttons) # Contents of buttons.json.
        await self.send_update_buttons(channel_id, button_data_list, [character_id])

    async def calculate_and_update_user_list_from_database(self, channel_id, character_id):
        """Pipes all real users + the correct number of Mickeys to self.send_update_user_list."""
        the_channel = await self.get_channel(channel_id)
        real_characters = the_channel.real_characters
        user_list = list(real_characters.keys())

        mickey_num = the_channel.states[character_id]['mickey_num']

        for sn in range(mickey_num):
            key = f"{self.MICKEY}_{sn}"
            user_list.append(the_channel.virtual_characters[key].user_id)

        await self.send_update_user_list(channel_id, user_list, [character_id])
