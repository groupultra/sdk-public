# SDK interface, agent or service. Automatically wraps the two platform APIs (HTTP and Socket)

import json
import time

from dataclasses import asdict
from dacite import from_dict

from moobius.types import MessageBody

import asyncio
import json
import uuid
import aioprocessing

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from moobius.network.ws_client import WSClient
from moobius.network.http_api_wrapper import HTTPAPIWrapper
from moobius.types import MessageBody, Action, Feature, FeatureCall, FeatureCallArgument, Copy, Payload
from loguru import logger

strict_kwargs = False # If True all functions (except __init__) with more than one non-self arg will require kwargs. If False a default ordering will be used.


class SDK:

    ############################ Startup functions ########################################

    def __init__(self, config_path, db_config_path, is_agent=False, **kwargs):
        """
        Initialize a service or agent object.

        Parameters:
          config_path: The path of the agent or service config file. Can also be a dict.
          db_config_path: The path of the database config file.
            Can also be a dict in which case no file will be loaded.
          is_agent=False: True for an agent, False for a service.
            Agents and services have slight differences in auth and how the platform reacts to them, etc.

        Returns:
          None

        Example:
          >>> service = SDK(service_config_path="./config/service.json", db_config_path="./config/database.json", is_agent=False)
        """
        self.config_path = config_path
        self.is_agent = is_agent

        if type(config_path) is dict:
            logger.info('Be careful to keep the secrets in your service config safe!')
            self.config = config_path
        elif type(config_path) is str:
            with open(config_path, "r") as f:
                self.config = json.load(f)
        else:
            raise Exception('config_path not understood')

        if type(db_config_path) is dict:
            self.db_config = db_config_path
        elif type(db_config_path) is str and db_config_path != "":
            with open(db_config_path, "r") as f:
                self.db_config = json.load(f)
        else:
            raise Exception('db_config_path not understood')

        http_server_uri = self.config["http_server_uri"]
        ws_server_uri = self.config["ws_server_uri"]
        email = self.config["email"]
        password = self.config["password"]
        the_id = self.config.get("service_id", "")
        if the_id != '' and the_id and self.is_agent:
            raise Exception('Agents cannot have a "service_id" in there JSON config.')
        if not self.is_agent:
            self.client_id = self.config.get("service_id", "")

        self.channels = []  # real channel ids. Not necessarily the same as self.config["channels"]

        self.http_api = HTTPAPIWrapper(http_server_uri, email, password)
        self.ws_client = WSClient(ws_server_uri, on_connect=self.send_agent_login if self.is_agent else self.send_service_login, handle=self.handle_received_payload)

        self.queue = aioprocessing.AioQueue()

        self.refresh_interval = 6 * 60 * 60             # 24h expire, 6h refresh
        self.authenticate_interval = 7 * 24 * 60 * 60   # 30d expire, 7d refresh
        self.heartbeat_interval = 30                    # 30s heartbeat

        self.scheduler = None

        self.bands = {}

    async def start(self):
        """
        Start the service/agent. start() fns are called with wand.run. There are 6 steps:
          1. Authenticate the service.
          2. Connect to the websocket server.
          3. Bind the service to the channels. If there is no service_id in the config file, create a new service and update the config file.
          4. Start the scheduler, run refresh(), authenticate(), send_heartbeat() periodically.
          5. Call on_start() to perform initialization tasks (override this method to do your own initialization tasks).
          6. Start listening to the websocket and the wand.

        No parameters or return value.
        """

        logger.debug("Starting agent..." if self.is_agent else "Starting service...")

        await self.authenticate()
        await self.ws_client.connect()
        logger.debug("Connected to websocket server.")

        if self.is_agent:
            async def _get_agent_info():
                if not self.is_agent:
                    raise Exception('Not an agent.')
                self.agent_info = await self.http_api.fetch_user_info()
                self.client_id = self.agent_info["sub"]
            await _get_agent_info()
            await self.send_agent_login()
        else:
            if not self.client_id:
                logger.debug('No service_id in config file. Will create a new service.')
                self.client_id = await self.http_api.create_service(description="Generated by MoobiusService")

                logger.info(f"NEW SERVICE CREATED!!!")
                logger.info("=================================================")
                logger.info(f" Service ID: {self.client_id}")
                logger.info("=================================================")
                logger.info(f"Please wait for 5 seconds...")
                self.config["service_id"] = self.client_id
                await asyncio.sleep(5) # TODO: Sleeps "long enough" should be replaced with polling.

            if len(self.config["channels"]) == 0:
                logger.error('No channels specified in self.config')
                return

            channelid2serviceid = await self.fetch_bound_channels() # Channels can only be bound to a SINGLE service.

            others = self.config["others"].lower().strip()
            for channel_id in set(self.config["channels"]):
                bound_to = channelid2serviceid.get(channel_id)
                if bound_to == self.client_id:
                    logger.info(f"Channel {channel_id} already bound to {self.client_id}, no need to bind it.")
                    self.channels.append(channel_id)
                    continue
                elif bound_to: # Conflict resolution.
                    if others=='ignore': # Do not intefere with channels bound to other users.
                        logger.info(f"Channel {channel_id} bound to service {bound_to} and will not be re-bound.")
                        continue
                    elif others=='unbind': # Be spiteful: Unbind channels bound to other users but don't use them.
                        logger.info(f"Unbinding channel {channel_id} from service {bound_to} but this service will not use this channel.")
                        await self.http_api.unbind_service_from_channel(bound_to, channel_id)
                        continue
                    elif others=='include': # Steal channels from other services. Hopefully they won't mind.
                        logger.info(f"Unbinding channel {channel_id} from service {bound_to} so it can be used by this service instead.")
                        await self.http_api.unbind_service_from_channel(bound_to, channel_id)
                    else:
                        raise Exception(f'Unknown others (other bands) option for handling channels already bound to other services: {others}')
                bind_info = await self.http_api.bind_service_to_channel(self.client_id, channel_id) # may already be binded to the service itself
                logger.info(f"Bound service to channel {channel_id}: {bind_info}")
                self.channels.append(channel_id)

            if not self.channels:
                logger.error("All channels are used up by other services and the 'others' option is not set to 'include' to steal them back.")
                return

            if type(self.config_path) is str:
                with open(self.config_path, "w") as f:
                    json.dump(self.config, f, indent=4)
                logger.info(f"Config file updated: {self.config_path}")

            await self.send_service_login() # It is OK (somehow) to log in after all of this not before.

        # Schedulers cannot be serialized so that you have to initialize it here
        self.scheduler = AsyncIOScheduler()

        # The details of access_token and refresh_token are managed by self.http_api
        self.scheduler.add_job(self.refresh, 'interval', seconds=self.refresh_interval)
        self.scheduler.add_job(self.authenticate, 'interval', seconds=self.authenticate_interval)
        self.scheduler.add_job(self.send_heartbeat, 'interval', seconds=self.heartbeat_interval)

        self.scheduler.start()
        logger.debug("Scheduler started.")

        await self.on_start()
        logger.debug("on_start() finished.")

        await asyncio.gather(self.ws_client.receive(), self.listen_loop())

    ################################## Query functions #######################################

    async def fetch_bound_channels(self):
        """Returns a dict of which service is each channel bound to. Channels can only be bound to a single service.
           Channels not bound to any service will not be in the dict."""
        service_list = await self.http_api.fetch_service_list()
        #logger.debug(f"Service list: {service_list}")
        #logger.info(f"Service ID: {self.client_id}")
        channelid2serviceid = {} # Channels can only be bound to a SINGLE service.
        for service in service_list:
            for channel_id in service["channel_ids"]:
                channelid2serviceid[channel_id] = service['service_id']
        return channelid2serviceid

    ################################## Actuators #######################################

    async def upload_avatar_and_create_character(self, username, nickname, image_path, description):
        """
        Upload an avatar image and create a character.
        Service function.

        Parameters:
          username: str
            The username of the character.
          nickname: str
            The nickname of the character.
          image_path: str
            The path of the avatar image. This should be the local path of the image.
          description: str
            The description of the character.

        Returns:
          The created character (Character object).
        """
        avatar = await self.http_api.upload_file(image_path)
        return await self.http_api.create_service_user(self.client_id, username, nickname, avatar, description)

    async def create_message(self, channel_id, content, recipients, subtype='text', sender=None):
        """
        Create a MessageDown (for service) or MessageUp (for agent) request and send it to the channel.

        Parameters:
          channel_id (str): The id of the channel.
          content (str): The text of the message such as "Hello everyone on this band!".
          recipients (list): The recipients of the message.
          subtype='text': The subtype of the message.
          sender: The sender of the message. None for Agents.

        No return value.
        """
        kwargs = {'channel_id':channel_id, 'recipients':recipients, 'subtype':subtype, 'message_content':content}
        if self.is_agent:
            await self.send_msg_up(**kwargs)
        else:
            kwargs['sender'] = sender or 'no_sender'
            await self.send_msg_down(**kwargs)

    async def send(self, payload_type, payload_body):
        """
        Send any kind of payload, including msg_down, update, update_userlist, update_channel_info, update_playground, update_features, update_style, and heartbeat.

        Parameters:
          payload_type (str): The type of the payload.
          payload_body (dict or str): The body of the payload.
            Strings will be converted into a Payload object.

        No return value.

        Example:
          >>> await self.send(payload_type='msg_down', payload_body=msg_up)
        """
        if isinstance(payload_body, dict):
            payload_dict = {
                'type': payload_type,
                'request_id': str(uuid.uuid4()),
                'client_id': self.client_id,
                'body': payload_body
            }
        else: # Need to wrap non-dataclasses into a dataclass, in this case Payload, in order to use asdict() on them.
            payload_obj = Payload(
                type=payload_type,
                request_id=str(uuid.uuid4()),
                client_id=self.client_id,
                body=payload_body
            )
            try:
                payload_dict = asdict(payload_obj)
            except Exception as error_e: # Track down those pickle errors!
                _pr = logger.error
                print("asdict FAILURE on", payload_type, payload_body, error_e)
                try:
                    asdict(payload_body)
                    _pr('HUH? The payload body CAN be dictified?')
                except:
                    pass
                for k, v in payload_body.__dict__.items():
                    if type(v) in [str, int, bool, float]:
                        _pr('Elemetary type, no problem pickling:', k, v)
                    else:
                        try:
                            asdict(Payload(type=payload_type, request_id=str(uuid.uuid4()), client_id=self.client_id, body=v))
                            _pr('No problem pickling:', k, v)
                        except Exception as e:
                            _pr('UNDICTABLE part of __dict__ error:', k, 'Value is:', v, 'type is:', type(v), 'error is:', e)
                raise error_e
        await self.ws_client.send(payload_dict)

    async def send_feature_call(self, channel_id, feature_id, feature_args):
        """
        Use to send a request to ask for a feature call.

        Parameters:
          channel_id (str): Which channel.
          feature_id (str): Which feature.
          feature_args (list of k-v pairs, not a dict): What about said feature should be fetched?

        No return value.
        """
        feature_call_instance = FeatureCall(
            feature_id=feature_id,
            channel_id=channel_id,
            sender=self.client_id,
            arguments=[FeatureCallArgument(name=arg[0], value=arg[1]) for arg in feature_args],
            context={}
        )
        await self.send("feature_call", feature_call_instance)

    async def send_heartbeat(self):
        """Sends a heartbeat to the server. Return None"""
        await self.ws_client.ping()
        if not self.is_agent: # 95% sure this extra line is just there because no one wanted to remove it.
            await self.ws_client.ping()

    async def create_and_bind_channel(self, channel_name, channel_desc):
        """Create a channel (band) with the provided name and description and binds self.client_id (the service_id) to it.
           (I think) a Service function. Returns the channel id."""
        channel_id = await self.http_api.create_channel(channel_name, channel_desc)
        await self.http_api.bind_service_to_channel(self.client_id, channel_id)  # may already be binded to the service itself
        return channel_id

    ################################## Single-line actuators #######################################

    async def refresh(self): """Calls self.http_api.refresh."""; return await self.http_api.refresh()
    async def authenticate(self): """Calls self.http_api.authenticate."""; return await self.http_api.authenticate()
    async def sign_up(self): """Calls self.http_api.sign_up."""; return await self.http_api.sign_up()
    async def sign_out(self): """Calls self.http_api.sign_out."""; return await self.http_api.sign_out()
    async def update_real_user(self, user_id, avatar, description, nickname): """Calls self.http_api.update_real_user."""; return await self.http_api.update_real_user(user_id, avatar, description, nickname)
    async def update_service_user(self, user_id, username, avatar, description, nickname): """Calls self.http_api.update_service_user using self.client_id."""; return await self.http_api.update_service_user(self.client_id, user_id, username, avatar, description, nickname)
    async def update_channel(self, channel_id, channel_name, channel_desc): """Calls self.http_api.update_channel."""; return await self.http_api.update_channel(channel_id, channel_name, channel_desc)
    async def create_channel(self, channel_name, channel_desc): """Calls self.http_api.TODO"""; return await self.http_api.create_channel(channel_name, channel_desc)
    async def create_service_user(self, username, nickname, avatar, description): """Calls self.http_api.create_service_user using self.create_service_user."""; return await self.http_api.create_service_user(self.client_id, username, nickname, avatar, description)
    async def fetch_popular_channels(self): """Calls self.http_api.fetch_popular_channels."""; return await self.http_api.fetch_popular_chanels()
    async def fetch_channel_list(self): """Calls self.http_api.fetch_channel_list."""; return await self.http_api.fetch_channel_list()
    async def fetch_real_characters(self, channel_id, raise_empty_list_err=True): """Calls self.http_api.fetch_real_characters using self.client_id."""; return await self.http_api.fetch_real_characters(channel_id, self.client_id, raise_empty_list_err=raise_empty_list_err)
    async def fetch_user_profile(self, user_id): """Calls self.http_api.fetch_user_profile"""; return await self.http_api.fetch_user_profile(user_id)
    async def fetch_service_list(self): """Calls self.http_api.fetch_service_list"""; return await self.http_api.fetch_service_list()
    async def fetch_service_user_list(self): """Calls self.http_api.fetch_service_user_list using self.client_id."""; return await self.http_api.fetch_service_user_list(self.client_id)
    async def upload_file(self, filepath): """Calls self.http_api.upload_file."""; return await self.http_api.upload_file(filepath)
    async def fetch_history_message(self, channel_id, limit=1024, before="null"): """Calls self.http_api.fetch_history_message."""; return await self.http_api.fetch_history_message(channel_id, limit, before)
    async def create_channel_group(self, channel_id, group_name, members): """Calls self.http_api.create_channel_group."""; return await self.http_api.create_channel_group(channel_id, group_name, members)
    async def create_service_group(self, group_id, members): """Calls self.http_api.create_service_group."""; return await self.http_api.create_service_group(group_id, members)
    async def update_channel_group(self, channel_id, group_id, members): """Calls self.http_api.update_channel_group."""; return await self.http_api.update_channel_group(channel_id, group_id, members)
    async def update_temp_channel_group(self, channel_id, members): """Calls self.http_api.update_temp_channel_group."""; return await self.http_api.update_temp_channel_group(channel_id, members)
    async def fetch_channel_group(self, channel_id): """Calls self.http_api.fetch_channel_group."""; return await self.http_api.fetch_channel_group(channel_id)
    async def fetch_channel_temp_group(self, channel_id): """Calls self.http_api.fetch_channel_temp_group."""; return await self.http_api.fetch_channel_temp_group(channel_id)
    async def fetch_user_from_group(self, user_id, channel_id, group_id): """Calls self.http_api.fetch_user_from_group."""; return await self.http_api.fetch_user_from_group(user_id, channel_id, group_id)
    async def fetch_target_group(self, user_id, channel_id, group_id): """Calls self.http_api.fetch_target_group."""; return await self.http_api.fetch_target_group(user_id, channel_id, group_id)

    async def send_agent_login(self): """Calls self.ws_client.agent_login using self.http_api.access_token; one of the agent vs service differences."""; return await self.ws_client.agent_login(self.http_api.access_token)
    async def send_service_login(self): """Calls self.ws_client.service_login using self.client_id and self.http_api.access_token; one of the agent vs service differences."""; return await self.ws_client.service_login(self.client_id, self.http_api.access_token)
    async def send_msg_up(self, channel_id, recipients, subtype, message_content): """Calls self.ws_client.msg_up using self.client_id."""; return await self.ws_client.msg_up(self.client_id, channel_id, recipients, subtype, message_content)
    async def send_msg_down(self, channel_id, recipients, subtype, message_content, sender): """Calls self.ws_client.TODO using self.client_id."""; return await self.ws_client.msg_down(self.client_id, channel_id, recipients, subtype, message_content, sender)
    async def send_update(self, target_client_id, data): """Calls self.ws_client.TODO"""; return await self.ws_client.update(self.client_id, target_client_id, data)
    async def send_update_user_list(self, channel_id, user_list, recipients): """Calls self.ws_client.update_user_list using self.client_id."""; return await self.ws_client.update_userlist(self.client_id, channel_id, user_list, recipients)
    async def send_update_channel_info(self, channel_id, channel_data): """Calls self.ws_client.update_channel_info using self.client_id."""; return await self.ws_client.update_channel_info(self.client_id, channel_id, channel_data)
    async def send_update_playground(self, channel_id, content, recipients): """Calls self.ws_client.update_playground using self.client_id."""; return await self.ws_client.update_playground(self.client_id, channel_id, content, recipients)
    async def send_update_features(self, channel_id, feature_data, recipients): """Calls self.ws_client.update_features using self.client_id."""; return await self.ws_client.update_features(self.client_id, channel_id, feature_data, recipients)
    async def send_update_style(self, channel_id, style_content, recipients): """Calls self.ws_client.update_style using self.client_id."""; return await self.ws_client.update_style(self.client_id, channel_id, style_content, recipients)
    async def send_fetch_userlist(self, channel_id): """Calls self.ws_client.fetch_userlist using self.client_id."""; return await self.ws_client.fetch_userlist(self.client_id, channel_id)
    async def send_fetch_features(self, channel_id): """Calls self.ws_client.fetch_features using self.client_id."""; return await self.ws_client.fetch_features(self.client_id, channel_id)
    async def send_fetch_style(self, channel_id): """Calls self.ws_client.fetch_style using self.client_id."""; return await self.ws_client.fetch_style(self.client_id, channel_id)
    async def send_fetch_playground(self, channel_id): """Calls self.ws_client.fetch_playground using self.client_id."""; return await self.ws_client.fetch_playground(self.client_id, channel_id)
    async def send_fetch_channel_info(self, channel_id): """Calls self.ws_client.fetch_channel_info using self.client_id."""; return await self.ws_client.fetch_channel_info(self.client_id, channel_id)
    async def send_join_channel(self, channel_id): """Calls self.ws_client.join_channel using self.client_id."""; return await self.ws_client.join_channel(self.client_id, channel_id)
    async def send_leave_channel(self, channel_id): """Calls self.ws_client.leave_channel using self.client_id."""; return await self.ws_client.leave_channel(self.client_id, channel_id)

    ################################## Callback switchyards #######################################

    @logger.catch
    async def listen_loop(self):
        """Listens to the wand (in an infinite loop so) that the wand could send spells to the service at any time (not only before the service is started).
           Uses asyncio.Queue."""
        while True:
            obj = await self.queue.coro_get()
            await self.on_spell(obj)

    @logger.catch
    async def handle_received_payload(self, payload):
        """
        Decode the received payload, a JSON string, and call the handler based on p['type']. Returns None.
        Example methods called:
          on_msg_up(), on_action(), on_feature_call(), on_copy_client(), on_unknown_payload()

        Example use-case:
          >>> self.ws_client = WSClient(ws_server_uri, on_connect=self.send_service_login, handle=self.handle_received_payload)
        """
        payload_data = json.loads(payload)
        if payload_data['type'] == 'msg_down' and 'recipients' not in payload_data['body']:
            payload_data['body']['recipients'] = [] # The conversion to a MessageBody needs all keys to be present! But msg_down doesn't have "recipients".
        if 'type' in payload_data:
            payload = from_dict(data_class=Payload, data=payload_data)
            if payload.type == "msg_down":
                await self.on_msg_down(payload.body)
            elif payload.type == "update":
                await self.on_update(payload.body)
            elif payload.type == "msg_up":
                await self.on_msg_up(payload.body)
            elif payload.type == "action":
                await self.on_action(payload.body)
            elif payload.type == "feature_call":
                await self.on_feature_call(payload.body)
            elif payload.type == "copy_client":     # TODO: legacy, at least for service.
                await self.on_copy_client(payload.body)
            else:   # TODO?: add types?
                await self.on_unknown_payload(payload)
        else:
            logger.error(f"Unknown payload without type: {payload_data}")

    async def on_action(self, action: Action):
        """
        Handles an action (Action object) from a user. Returns None.
        Calls the corresponding method to handle different subtypes of action.
        Example methods called:
          on_fetch_user_list(), on_fetch_features(), on_fetch_playground(), on_join_channel(), on_leave_channel(), on_fetch_channel_info()
        Service function.
        """
        if action.subtype == "fetch_userlist":
            await self.on_fetch_user_list(action)
        elif action.subtype == "fetch_features":
            await self.on_fetch_features(action)
        elif action.subtype == "fetch_playground":
            await self.on_fetch_playground(action)
        elif action.subtype == "join_channel":
            await self.on_join_channel(action)
        elif action.subtype == "leave_channel":
            await self.on_leave_channel(action)
        elif action.subtype == "fetch_channel_info":
            await self.on_fetch_channel_info(action)
        else:
            logger.error(f"Unknown action subtype: {action.action_subtype}")

    async def on_update(self, update):
        """Dispatches an update (a dict) to one of various callbacks. Agent function.
           It is recommended to overload the invididual callbacks instead of this function."""
        if update['subtype'] == "update_userlist":
            for i in range(len(update['userlist'])):
                if type(update['userlist'][i]) is not str: # Newer version of the platform will return a list of user_ids and this won't be needed.
                    update['userlist'][i] = update['userlist'][i]['user_id']
            await self.on_update_userlist(update)
        elif update['subtype'] == "update_channel_info":
            await self.on_update_channel_info(update)
        elif update['subtype'] == "update_playground":
            await self.on_update_playground(update)
        elif update['subtype'] == "update_features":
            update['features'] = [Feature(**f) for f in update['features']]
            await self.on_update_features(update)
        elif update['subtype'] == "update_style":
            await self.on_update_style(update)
        else:
            logger.error(f"Unknown update subtype: {update['subtype']}")

    ################################## Individual callbacks #######################################

    async def on_spell(self, obj):
        """Called when a spell is received, which can be any object but is often a string. Returns None."""
        logger.debug(f'Spell Received {obj}')

    async def on_start(self):
        """Called when the service is initialized. Returns None"""
        logger.debug("Service started. Override this method to perform initialization tasks.")

    async def on_msg_up(self, msg_up: MessageBody):
        """
        Handles a payload from a user. Service function. Returns None.
        Example MessageBody object:
          moobius.MessageBody(subtype=text, channel_id=<band id>, content={'text': 'api'}, timestamp=1707254706635,
                              recipients=[<user id 1>, <user id 2>], sender=<user id>, msg_id=<id>,
                              context={'recipients': ['<user id>', 'c142fb8e-e4ab-48da-9f84-de105769465c'], 'group_id': None, 'sender': <user id>})"""
        logger.debug(f"MessageUp received: {msg_up}")

    async def on_msg_down(self, msg_down):
        """Callback when a message is recieved (a MessageBody object similar to what on_msg_up gets).
           Agent function. Returns None."""
        logger.debug(f"MessageDown received: {msg_down}")

    async def on_update_userlist(self, update):
        """
        Handles changes to the userlist. One of the multiple update callbacks. Returns None.
        Agent function.

        Example update dict:
          {"subtype": "update_userlist",
           "channel_id": "abc...",
           "recipients": [recipient0_userid, recipient1_userid, recipient2_userid...],
           "userlist": [user_id0, user_id1, ...],
           "context": {}}
        """
        logger.debug("on_update_user_list")

    async def on_update_channel_info(self, update):
        """
        Handles changes to the channel info. One of the multiple update callbacks. Returns None.
        Agent function.

        Example update dict:
          {"subtype": "channel_info",
           "channel_id": "abc...", "request_id": "abc...", "client_id": "abc...",
           "body": <dict of channel data>}
        """
        logger.debug("on_update_channel_info")

    async def on_update_playground(self, update):
        """
        Handles changes to the playground. One of the multiple update callbacks. Returns None.
        Agent function.

         Example update dict; note that update['content'] gives the content.
           {"subtype": "update_playground", "channel_id": "8c2...", "group_id": "temp", "context": {},
            "content": {"path": "https://...png", "text": "This appears on the Stage"}}
        """
        logger.debug("on_update_playground")

    async def on_update_features(self, update):
        """
        Handles changes to the playground. One of the multiple update callbacks. Returns None.
        Agent function.

        Example update dict:
          {"subtype": "update_features", "channel_id": "8c23...",
           "features": [Feature(...), Feature(...), Feature(...), ...]}
        """
        logger.debug("on_update_features")

    async def on_update_style(self, update):
        """
        Handles changes in the style. One of the multiple update callbacks. Returns None.
        Agent function.

        Example update dict:
          {"subtype": "update_style",
           "channel_id": <band-id>,
           "recipients": [user_id0, user_id1, user_id2],
           "content": [{"widget": "playground","display": "visible", "expand": "true"}],
           "group_id": "temp",
           "context": {}}
        """
        logger.debug("on_update_style")

    async def on_fetch_user_list(self, action):
        """Handles the received action of fetching a user_list. One of the multiple Action object callbacks. Returns None.
           Example Action object: moobius.Action(subtype="fetch_userlist", channel_id=<band id>, sender=<user id>, context={})."""
        logger.debug("on_action fetch_userlist")

    async def on_fetch_features(self, action): # TODO: This doesn't seem to have the features?
        """Handles the received action of fetching features. One of the multiple Action object callbacks. Returns None.
           Example Action object: moobius.Action(subtype="fetch_features", channel_id=<band id>, sender=<user id>, context={})"""
        logger.debug("on_action fetch_features")

    async def on_fetch_playground(self, action):
        """Handles the received action (Action object) of fetching playground. One of the multiple Action object callbacks. Returns None."""
        logger.debug("on_action fetch_playground")

    async def on_fetch_channel_info(self, action):
        """Handle the received action of fetching channel info. One of the multiple Action object callbacks. Returns None.
           Example Action object: moobius.Action(subtype="fetch_channel_info", channel_id=<band id>, sender=<user id>, context={})."""
        logger.debug("on_action fetch_channel_info")

    async def on_join_channel(self, action):
        """Handles the received action of joining a channel. One of the multiple Action object callbacks. Returns None.
           Example Action object: moobius.Action(subtype="join_channel", channel_id=<band id>, sender=<user id>, context={})."""
        logger.debug("on_action join_channel")

    async def on_leave_channel(self, action):
        """Handles the received action of leaving a channel. One of the multiple Action object callbacks. Returns None.
           Example Action object: moobius.Action(subtype="leave_channel", channel_id=<band id>, sender=<user id>, context={})."""
        logger.debug("on_action leave_channel")

    async def on_feature_call(self, feature_call: FeatureCall):
        """Handles a feature call from a user. Returns None.
           Example FeatureCall object: moobius.FeatureCall(feature_id=button["feature_id"], channel_id=<band id>, sender=<user id>, arguments=[], context={})"""
        logger.debug(f"Feature call received: {feature_call}")

    async def on_copy_client(self, copy):
        """Handles copying (TODO what?). Returns None.
           Example Copy object: moobius.Copy(request_id=<id>, origin_type=msg_down, status=True, context={'msg': 'Message received'})"""
        if not self.is_agent and not copy.status:
            await self.send_service_login()
        logger.debug("on_copy_client")

    async def on_unknown_payload(self, payload: Payload):
        """Catch-all for handling unknown Payload objects. Returns None."""
        logger.debug(f"Unknown payload received: {payload}")

    def __str__(self):
        fname = self.config_path
        http_server_uri = self.config["http_server_uri"]
        ws_server_uri = self.config["ws_server_uri"]
        email = self.config["email"]
        num_bands = len(self.bands)
        agsv = 'Agent' if self.is_agent else 'Service'
        return f'moobius.SDK({agsv}; config=config={fname}, http_server_uri={http_server_uri}, ws_server_uri={ws_server_uri}, ws={ws_server_uri}, email={email}, password=****, num_bands={num_bands})'
    def __repr__(self):
        return self.__str__()
