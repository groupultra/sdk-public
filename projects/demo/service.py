# service.py
import json, sys, asyncio, pprint
import copy
from datetime import datetime

from loguru import logger
from moobius import Moobius, MoobiusStorage
from moobius.types import Button, CanvasElement

avoid_redis_on_windoze = True # Redis requires WSL2 to run on windows since it is Linux-only.
avoid_redis = (avoid_redis_on_windoze and (sys.platform.lower() in ['win', 'win32', 'win64', 'windows', 'windoze'])) or avoid_redis_on_windoze == 'also linux'
load_xtra_channels_on_start = True

example_socket_callback_payloads = {} # Print these out when the AI is done.


def limit_len(message, n=4096):
    message = str(message)
    if len(message)>4096:
        message = message[0:n]+'...'+str(len(message))+' bytes'
    return message


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

        real_character_ids = await self.fetch_real_character_ids(channel_id, raise_empty_list_err=False)

        for character_id in real_character_ids:
            if type(character_id) is not str:
                raise Exception('character_id must be a str.')
            the_channel.real_characters[character_id] = await self.fetch_character_profile(character_id)

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
            await self.create_message(c_id, txt, recipients, sender=talker)

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
        channel_id = message_up.channel_id
        recipients = message_up.recipients
        sender = message_up.sender
        if message_up.subtype == "text":
            txt = message_up.content['text']
            txt1 = txt.lower().strip()
            the_channel = await self.get_channel(channel_id)
            if type(sender) is not str:
                raise Exception(f'Sender must be a string, instead it is: {sender}')
            if sender not in list(the_channel.real_characters.keys()):
                await self.add_real_character(channel_id, sender, intro="oops looks like (bug) did not add this character on startup.")

            if recipients: # DEMO: text modification
                if txt1.lower() == "moobius":
                    await self.create_message(channel_id, "Moobius is Great!", recipients, sender=sender)
                elif txt1.lower() == "api":
                    lines = []
                    for k,v in example_socket_callback_payloads.items():
                        lines.append(k+': '+str(v))
                    txt2 = '\n\n'.join(lines)
                    await self.create_message(channel_id, 'Socket api call examples recorded:\n'+txt2, recipients, sender=sender)
                else:
                    await self.create_message(channel_id, txt, recipients, sender=sender)
            else: # DEMO: commands to Service(Infinity)
                if txt1 == "hide":
                    the_channel.buttons[sender] = []
                    await self.send_buttons_from_database(channel_id, sender)
                elif txt1 == "show":
                    the_channel.buttons[sender] = self.default_buttons
                    await self.send_buttons_from_database(channel_id, sender)
                elif txt1 == "reset":
                    for sn in range(self.MICKEY_LIMIT):
                        the_character_id = the_channel.virtual_characters[f"{self.MICKEY}_{sn}"].character_id
                        await self.update_character(character_id=the_character_id, avatar=self.image_paths[self.MICKEY], description='Mickey reset!', name=f'Mickey {sn}')

                    the_channel.states[sender]['mickey_num'] = 0
                    the_channel.states.save(sender)

                    await self.calculate_and_update_character_list_from_database(channel_id, sender)
                    the_channel = await self.get_channel(channel_id) # TODO: why call this twice?
                    the_channel.buttons[sender] = self.default_buttons # Reset buttons etc.
                    await self.send_update_buttons(channel_id, self.default_buttons, [sender])
                elif txt1.split(' ')[0] == 'laser':
                    await self.create_message(channel_id, limit_len(f"NOTE: The Laser feature is not a standard SDK feature, it is specific to Demo."), [sender], sender=sender)
                    if '>' not in txt1:
                        await self.create_message(channel_id, limit_len(f'Must be formatted "laser name > message, and only sent to a single user".'), [sender], sender=sender)
                    else:
                        pair = [t.strip() for t in txt.split('>')]
                        the_name = ' '.join(pair[0].split(' ')[1:])
                        the_message = pair[1]
                        if len(the_message.strip())<2:
                            await self.create_message(channel_id, limit_len(f'The message was empty, a default message will be used.".'), [sender], sender=sender)
                            the_message = 'Empty_message!'
                        real_ids = await self.fetch_real_character_ids(channel_id, raise_empty_list_err=False)
                        real_profiles = await self.fetch_character_profile(real_ids)
                        target_id = None
                        for rp in real_profiles:
                            if rp.name.lower().strip() == the_name.lower().strip():
                                target_id = rp.character_id
                        if target_id:
                            await self.create_message(channel_id, limit_len(f'Sending message to name={the_name}, id={target_id}".'), [sender], sender=sender)
                            await self.create_message(channel_id, limit_len(f'Laser message: "{the_message}".'), [target_id], sender=sender)
                        else:
                            await self.create_message(channel_id, limit_len(f'Cannot find character with name={the_name}".'), [sender], sender=sender)
                else:
                    txt = txt+' (this message has no recipients, either it was sent to service or there is a bug).'
                    await self.create_message(channel_id, txt, [sender], sender=sender)
        else:
            await self.convert_and_send_message(message_up) # Not sure if this works or the generic next line is needed?

    async def on_fetch_service_characters(self, action):
        example_socket_callback_payloads['on_fetch_service_characters'] = action
        await self.calculate_and_update_character_list_from_database(action.channel_id, action.sender)

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

        style_content = [
            {
                "widget": "canvas",
                "display": "visible",
                "expand": "true"
            }
        ]

        await self.send_update_style(channel_id, style_content, [sender])

    async def add_real_character(self, channel_id, character_id, intro="joined the channel!"):
        character = await self.fetch_character_profile(character_id)
        name = character.character_context.name
        the_channel = await self.get_channel(channel_id)

        the_channel.real_characters[character_id] = character
        the_channel.buttons[character_id] = self.default_buttons
        the_channel.states[character_id] = self.default_status

        character_ids = list(the_channel.real_characters.keys())
        await self.send_update_character_list(channel_id, character_ids, character_ids)
        await self.create_message(channel_id, f'{name} {intro} (id={character_id})', character_ids, sender=character_id)

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
        name = character.character_context.name

        real_characters = (await self.get_channel(channel_id)).real_characters
        character_ids = list(real_characters.keys())

        await self.send_update_character_list(channel_id, character_ids, character_ids)
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

    async def on_update_characters(self, x):
        example_socket_callback_payloads['on_update_characters'] = x

    async def on_button_click(self, button_click):
        """Called when the user presses a button (and selecting an option of a list appears). button_click is a Button object.
           This is a major switchyard which handles most of the different buttons in the demo."""
        example_socket_callback_payloads['on_button_click'] = button_click
        channel_id = button_click.channel_id
        button_id = button_click.button_id.lower()
        who_clicked = button_click.sender
        the_channel = await self.get_channel(channel_id)

        character = the_channel.real_characters[who_clicked]
        name = character.character_context.name
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
            extra_channel_ids = list(self.xtra_channels.keys())
            if value == "New Channel".lower():
                channel_name = '>>Demo TEMP channel'+str(len(extra_channel_ids))
                new_channel_id = await self.create_and_bind_channel(channel_name, 'Channel created by the GUI.')
                await self.initialize_channel(new_channel_id) # Prevents KeyErrors.
                self.xtra_channels[new_channel_id] = 'A channel'
                await self.create_message(channel_id, f"New channel created, refresh and it should appear on the left bar: {channel_name} ({new_channel_id})", [who_clicked], sender=who_clicked)
            elif value == "Ping Channels".lower():
                tasks = [self.create_message(channel_id, f"Pinging Channel ids: {extra_channel_ids} (one ping message should show up in each channel)", [who_clicked], sender=who_clicked)]
                for extra_channel_id in extra_channel_ids:
                    tasks.append(self.create_message(extra_channel_id, f"Ping from channel {channel_id} to channel {extra_channel_id}!", [who_clicked], sender=who_clicked))
                await asyncio.wait(tasks)
            elif value == "List Bound Channels".lower():
                channel_ids = await self.fetch_bound_channels()
                await self.create_message(channel_id, f"All bound channels:\n{channel_ids}.", [who_clicked], sender=who_clicked)
            elif value == "Leave Extra Channels".lower():
                await self.create_message(channel_id, f"Fetching the list of bound channels, will leave any channels which are not in the config.", [who_clicked], sender=who_clicked)
                left_channels = []
                channel_ids = await self.fetch_bound_channels()
                for c_id in channel_ids:
                         if c_id in self.config["channels"]:
                             continue # Do not leave the core channels.
                         if c_id in self.channels:
                             del self.channels[c_id]
                         left_channels.append(c_id)
                await self.create_message(channel_id, f"Will try to leave these channels:\n{left_channels}.", [who_clicked], sender=who_clicked)
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
                await self.create_message(channel_id, f"Has left these channels (refresh to see):\n{sucessfully_left}.", [who_clicked], sender=who_clicked)
            elif value == "Fetch Channel List".lower():
                x = await self.fetch_channel_list()
                await self.create_message(channel_id, f"Channel list:\n{x}", [who_clicked], sender=who_clicked)
                x = await self.fetch_popular_channels()
                await self.create_message(channel_id, f"Popular channel list:\n{x}", [who_clicked], sender=who_clicked)
            elif value == "Update Extra Channels".lower():
                extra_channel_ids = list(self.xtra_channels.keys())
                ix = 0
                for bid in extra_channel_ids:
                    await self.update_channel(bid, f'<>DemoTmpChannel Updated{ix}<>', 'Pressed the update extra channels button.')
                    ix = ix+1
                await self.create_message(channel_id, f"Updated these channel names (refresh to see changes):\n{extra_channel_ids}", [who_clicked], sender=who_clicked)
            elif value == "Fetch Chat History".lower():
                await self.create_message(channel_id, f"Fetching chat history, as HTML (raw HTML will be printed).", [who_clicked], sender=who_clicked)
                history = await self.fetch_message_history(channel_id, limit=6, before="null")
                await self.create_message(channel_id, limit_len(f"Recent chat history of this channel:\n{history}"), [who_clicked], sender=who_clicked)
            elif value == "Fetch Buttons".lower():
                await self.create_message(channel_id, limit_len(f"WARNING: Getting a callback for Fetch Buttons will be delayed may need a refresh to see."), [who_clicked], sender=who_clicked)
                self.TMP_print_buttons = True
                await self.send_fetch_buttons(channel_id)
            elif value == "Fancy Right Click".lower():
                option_dict = {'1':'Press A', '2':'Press B', '3':'Press C'}
                await self.send_update_rclick_buttons(channel_id, option_dict, [who_clicked])
                await self.create_message(channel_id, "Try right-clicking on a message.", [who_clicked], sender=who_clicked)
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

                    await self.calculate_and_update_character_list_from_database(channel_id, who_clicked)
            elif value == 'Mickey Talk'.lower():
                if the_channel.states[who_clicked]['mickey_num'] == 0:
                    await self.create_message(channel_id, "Please Create Mickey First!", [who_clicked], sender=who_clicked)
                else:
                    sn = the_channel.states[who_clicked]['mickey_num'] - 1
                    talker = the_channel.virtual_characters[f"{self.MICKEY}_{sn}"].character_id
                    await self.create_message(channel_id, f"Mickey {sn} Here! Mickeys are stored in JSON db. Sent to characters: {[who_clicked]}", [who_clicked], sender=talker)
            elif value == "Update Mickey (not agent) name".lower():
                if the_channel.states[who_clicked]['mickey_num'] == 0:
                    await self.create_message(channel_id, "Please Create Mickey First!", [who_clicked], sender=who_clicked)
                else:
                    sn = the_channel.states[who_clicked]['mickey_num'] - 1
                    the_character_id = the_channel.virtual_characters[f"{self.MICKEY}_{sn}"].character_id
                    await self.update_character(character_id=the_character_id, avatar=image_path, description='Mickey updated name!', name=f'Update Mickey Nick {self.n_usr_update}')
                    await self.create_message(channel_id, f"Updated Mickey name and image (refresh to see).", [who_clicked], sender=who_clicked)
            elif value == "List Characters".lower():
                char_list = await self.fetch_service_characters()

                await self.create_message(channel_id, limit_len(f"Real+Fake character list:\n {pprint.pformat(char_list)}"), [who_clicked], sender=who_clicked)
                real_ids = await self.fetch_real_character_ids(channel_id, raise_empty_list_err=False)
                await self.create_message(channel_id, f'Real character ids: {real_ids}', [who_clicked], sender=who_clicked)
                await self.create_message(channel_id, f'Real character profiles: {await self.fetch_character_profile(real_ids)}', [who_clicked], sender=who_clicked)
            else:
                raise Exception(f'Strange value for button user_btn: {value}')
        elif button_id == "group_btn".lower():
            if value == "List Channel Temp Groups".lower():
                glist = await self.fetch_channel_temp_group(channel_id)
                await self.create_message(channel_id, limit_len(f"Channel temp group list (likely empty):\n{pprint.pformat(glist)}"), [who_clicked], sender=who_clicked)
            elif value == "List Channel Groups".lower():
                glist = await self.fetch_channel_group_list(channel_id)
                await self.create_message(channel_id, limit_len(f"Channel group list (likely empty):\n{glist}"), [who_clicked], sender=who_clicked)
                gdict = await self.http_api.fetch_channel_group_dict(channel_id, self.client_id)
                await self.create_message(channel_id, limit_len(f"Channel group, dict form (used internally):\n{pprint.pformat(gdict)}"), [who_clicked], sender=who_clicked)
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
"show" (send to service): Show buttons.
"hide" (send to service): Hide buttons.
"reset" (send to service): Reset mickeys and refresh buttons.
"laser name > message" (send to service): Send a message to a single user only. Messages can be sent to oneself.
""".strip().replace('\n','\n\n')
            await self.create_message(channel_id, f"Commands (some must be sent to all 'all' some to 'service'):\n{cmds}", [who_clicked], sender=who_clicked)
        else:
            logger.warning(f"Unknown button_id: {button_id}")

    async def on_menu_click(self, menu_click):
        """Right-click the context menu."""
        item_id = menu_click.item_id
        message_content = menu_click.message_content
        option_dict = {'1':'Press A', '2':'Press B', '3':'Press C'} # This dict was passed into the 
        txt = f'You choose "{option_dict[item_id]}" on message "{message_content["text"]}".'
        await self.create_message(menu_click.channel_id, txt, [menu_click.sender], sender=menu_click.sender)

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

        for c_id in self.channels.keys():
            the_channel = await self.get_channel(c_id)
            recipients = list(the_channel.real_characters.keys())
            talker = the_channel.virtual_characters[self.WAND].character_id
            await self.create_message(c_id, text, recipients, sender=talker)

    ########################### helper functions #####################################

    async def send_buttons_from_database(self, channel_id, character_id):
        """Pipes the buttons (loaded from the JSON) to self.send_update_buttons."""
        button_data_list = (await self.get_channel(channel_id)).buttons.get(character_id, self._default_buttons) # Contents of buttons.json.
        await self.send_update_buttons(channel_id, button_data_list, [character_id])

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
