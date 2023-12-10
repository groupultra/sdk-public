import json
import copy
import os
import random

from loguru import logger

from moobius import MoobiusService, MoobiusStorage
from lib.cicada_director import CicadaDirector


class CicadaService(MoobiusService):
    def __init__(self, log_file="logs/service.log", error_log_file="logs/error.log", **kwargs):
        super().__init__(**kwargs)
        self.log_file = log_file
        self.error_log_file = error_log_file

        self.host = None
        self.names = None
        self.resource_dir = 'resources/'
        self.record_dir = 'temp/'
        self.game_band_id = '372386d6-8435-4e76-b8d1-8fe18d3da323'

        self.default_game_status = {
            'last_game_id': None,
            'view_characters': []
        }

        os.makedirs(self.resource_dir, exist_ok=True)
        os.makedirs(self.record_dir, exist_ok=True)

        self.director = CicadaDirector(
            record_dir=self.record_dir,
            send_to_audience=self._send_to_audience,
            send_to_all_players=self._send_to_all_players,
            notify_player=self._notify_player
        )

    async def on_start(self):
        """
        Called after successful connection to websocket server and service login success.
        """
        # ==================== load features ====================
        logger.add(self.log_file, rotation="1 day", retention="7 days", level="DEBUG")
        logger.add(self.error_log_file, rotation="1 day", retention="7 days", level="ERROR")

        with open(f'{self.resource_dir}/features.json', 'r') as f:
            features = json.load(f)

        for channel_id in self.channels:
            self.bands[channel_id] = MoobiusStorage(self.service_id, channel_id, db_config=self.db_config)
            
            real_characters = self.http_api.get_channel_user_list(channel_id, self.service_id)

            for character in real_characters:
                character_id = character.user_id
                self.bands[channel_id].real_characters[character_id] = character

                if character_id not in self.bands[channel_id].game_status:
                    self.bands[channel_id].game_status[character_id] = copy.deepcopy(self.default_game_status)

            for feature in features:
                feature_id = feature["feature_id"]
                self.bands[channel_id].features[feature_id] = feature

            # ====================== upload avatars ======================

            with open(f'{self.resource_dir}/names.json', 'r') as f:
                self.names = json.load(f)

            for local_id, name in self.names.items():
                if local_id not in self.bands[channel_id].avatars:
                    logger.info(f'Uploading avatar {local_id}...')
                    file_name = f'resources/icons/{local_id}.jpg'
                    avatar_uri = self.http_api.upload_file(file_name)
                    self.bands[channel_id].avatars[local_id] = avatar_uri
                else:
                    pass
        
        self.host = self.create_and_save_character(self.game_band_id, '0000', 'Cicada Host')
        
        await self.director.on_load()

    def create_and_save_character(self, band_id, local_id, nickname):
        username = f'{nickname}'
        avatar = self.bands[band_id].avatars[local_id]
        description = f'I am {nickname}!'

        character = self.http_api.create_service_user(self.service_id, username, nickname, avatar, description)
        self.bands[band_id].virtual_characters[character.user_id] = character

        return character

    def view_to_user_list(self, channel_id, sender):
        user_list = []

        band = self.bands[channel_id]

        for cid in band.game_status[sender]['view_characters']:
            if cid == sender:
                user_list.append(band.real_characters[cid])
            else:
                user_list.append(band.virtual_characters[cid])

        return user_list

    async def _send_to_audience(self, game, content, sent_by=-1):
        game_status = self.bands[self.game_band_id].game_status

        audience = [cid for cid in game_status if not self.query_character(self.game_band_id, cid)[0]]

        if sent_by < 0:
            prefix = f'Game[{game.game_id}]: '
        else:
            prefix = f'Game[{game.game_id}] Player {sent_by} said: '

        await self.create_message(self.game_band_id, f'{prefix}{content}', audience, sender=self.host.user_id)

    @logger.catch
    async def _send_to_all_players(self, game, content, sent_by=-1):
        for player_id in range(game.total_players):
            real_id = game.players[player_id]['real_id']

            if not real_id:
                continue
            else:
                if sent_by < 0:
                    sender_id = self.host.user_id
                elif sent_by == player_id:
                    continue  # no repeat
                else:
                    sender_id = self.bands[self.game_band_id].game_status[real_id]['view_characters'][sent_by]

                await self.create_message(self.game_band_id, f'{content}', [real_id], sender=sender_id)

    @logger.catch
    async def _notify_player(self, game, player_id, content, sent_by=-1):
        real_id = game.players[player_id]['real_id']

        if not real_id or player_id == sent_by:     # no repeat!
            return
        else:
            prefix = f'Game[{game.game_id}] Host: ' if sent_by < 0 else f'Game[{game.game_id}] Player {sent_by}: '

            await self.create_message(self.game_band_id, f'{prefix}{content}', [real_id], sender=self.host.user_id)

    async def on_msg_up(self, msg_up):
        """
        Handle the received message.
        """
        channel_id = msg_up.channel_id
        sender = msg_up.context.sender
        game_id, player_id = self.query_character(channel_id, sender)

        if game_id:
            if msg_up.subtype == "text":
                text = msg_up.content['text']
                game = self.director.get_game(game_id)
                
                if game.stage == game.STAGE_WAIT:
                    await self.create_message(self.game_band_id, 'Please wait for other players to join!', [sender], sender=self.host.user_id)

                elif game.stage == game.STAGE_TALK:
                    await self.director.on_talk_attempt(game_id, player_id, text)
                    
                elif game.stage == game.STAGE_VOTE:
                    recipients = msg_up.context.recipients

                    vote_to = []

                    game_status = self.bands[msg_up.channel_id].game_status[sender]

                    for i in range(game.total_players):
                        if game_status['view_characters'][i] in recipients:
                            vote_to.append(i)
                        else:
                            pass
                    
                    text = ''.join([str(v) for v in vote_to])     # for compatibility with the old version
                    
                    await self.director.on_vote_attempt(game_id, player_id, text)
                
                elif game.stage == game.STAGE_END:
                    await self.create_message(self.game_band_id, 'The Game has ended!', [sender], sender=self.host.user_id)

                else:
                    pass
            
            else:
                await self.create_message(self.game_band_id, 'Please send text messages only!', [sender], sender=self.host.user_id)

        else:
            msg_down = self.msg_up_to_msg_down(msg_up, remove_self=True)
            await self.send(payload_type='msg_down', payload_body=msg_down)

    async def refresh_audience_views(self, channel_id):
        audience = [cid for cid in self.bands[channel_id].game_status if self.query_character(channel_id, cid)[0] is None]
        audience_characters = [self.bands[channel_id].real_characters[cid] for cid in audience if cid in self.bands[channel_id].real_characters]
        audience_features = [self.bands[channel_id].features['Cicada']]

        await self.send_update_user_list(channel_id, audience_characters, audience)
        await self.send_update_features(channel_id, audience_features, audience)

    # game_id, player_id
    def query_character(self, channel_id, character_id):
        return self.director.query_real_id(character_id)

    async def on_fetch_features(self, action):
        channel_id = action.channel_id
        sender = action.sender
        band = self.bands[channel_id]

        if self.query_character(channel_id, sender)[0]:
            feature_data_list = [band.features['Quit']]
        else:
            feature_data_list = [band.features['Cicada']]

        await self.send_update_features(action.channel_id, feature_data_list, [action.sender])

    async def on_fetch_user_list(self, action):
        channel_id = action.channel_id
        sender = action.sender
        band = self.bands[channel_id]

        if action.subtype == "fetch_userlist":
            game_status_dict = band.game_status

            if sender in game_status_dict:
                pass
            else:
                game_status_dict[sender] = copy.deepcopy(self.default_game_status)

            if self.query_character(channel_id, sender)[0]:
                user_list = self.view_to_user_list(channel_id, sender)
                await self.send_update_user_list(channel_id, user_list, [sender])
            else:
                audience = [cid for cid in band.game_status if
                            self.query_character(channel_id, cid)[0] is None]
                audience_characters = [band.real_characters[cid] for cid in audience]
                await self.send_update_user_list(channel_id, audience_characters, [sender])

    async def on_fetch_playground(self, action):
        pass

    async def on_join_channel(self, action):
        sender = action.sender
        channel_id = action.channel_id
        character = self.http_api.fetch_user_profile(sender)
        nickname = character.user_context.nickname
        band = self.bands[channel_id]

        band.real_characters[sender] = character
        band.game_status[sender] = copy.deepcopy(self.default_game_status)

        await self.refresh_audience_views(channel_id)
        audience = [cid for cid in band.game_status if self.query_character(channel_id, cid)[0] is None]

        await self.create_message(channel_id, f'{nickname} joined the band!', audience, sender=sender)

    async def on_leave_channel(self, action):
        channel_id = action.channel_id
        sender = action.sender
        band = self.bands[channel_id]
        character = band.real_characters.pop(sender, None)
        nickname = character.user_context.nickname

        await self.dismiss_game(channel_id, sender)     # refresh audience view here
        band.game_status.pop(sender, None)

        await self.refresh_audience_views(channel_id)
        audience = [cid for cid in band.game_status if self.query_character(channel_id, cid)[0] is None]

        await self.create_message(channel_id, f'{nickname} left the band (but still talks~)!', audience, sender=sender)

    # Quit after director has been dismissed
    # todo: add on_end trigger!!!
    async def dismiss_game(self, channel_id, sender):
        game_id, player_id = self.query_character(channel_id, sender)
        game = self.director.get_game(game_id)

        if game is not None:
            real_ids = [game.players[i]['real_id'] for i in range(game.total_players) if game.players[i]['is_human']]
            await self.director.dismiss_game(game_id)
            
            for real_id in real_ids:
                # do not just modify inner fields or the database will not update
                self.bands[channel_id].game_status[real_id] = copy.deepcopy(self.default_game_status)   

            await self.refresh_audience_views(channel_id)
        else:
            logger.warning('Warning: Attempted to dismiss an empty game!')
            last_game_id = self.bands[channel_id].game_status[sender]['last_game_id']

            if last_game_id:
                real_ids = [cid for cid in self.bands[channel_id].game_status if self.bands[channel_id].game_status[cid]['last_game_id'] == last_game_id]

                for real_id in real_ids:
                    # do not just modify inner fields or the database will not update
                    self.bands[channel_id].game_status[real_id] = copy.deepcopy(self.default_game_status)   
                    
                await self.refresh_audience_views(channel_id)
            else:
                pass

    async def on_feature_call(self, feature_call):
        """
        Handle the received feature call.
        """
        sender = feature_call.sender
        channel_id = feature_call.channel_id
        feature_id = feature_call.feature_id
        character = self.bands[channel_id].real_characters[feature_call.sender]
        nickname = character.user_context.nickname
        band = self.bands[channel_id]

        if feature_id == "Cicada":
            game_id, player_id = self.query_character(channel_id, sender)
 
            if game_id:
                logger.warning(f'{nickname} attempted to join a game twice!')
                return
            else:
                await self.director.on_human_join(sender, name=nickname)
            
            game_id, player_id = self.query_character(channel_id, sender)
            game = self.director.get_game(game_id)

            game_status = copy.deepcopy(self.default_game_status)

            game_status['last_game_id'] = game_id

            feature_data_list = [self.bands[channel_id].features['Quit']]
            await self.send_update_features(channel_id, feature_data_list, [feature_call.sender])
                           
            local_ids = random.sample(list(self.names.keys())[1:], game.total_players)
            names = [f'Player {i} - {self.names[local_ids[i]]}' for i in range(game.total_players)]
            
            for i in range(game.total_players):
                if i != player_id:
                    game_status['view_characters'].append(self.create_and_save_character(channel_id, local_ids[i], names[i]).user_id)
                else:
                    game_status['view_characters'].append(sender)
            
            band.game_status[sender] = game_status

            user_list = self.view_to_user_list(channel_id, sender)
            await self.send_update_user_list(self.game_band_id, user_list, [feature_call.sender])
            await self.refresh_audience_views(channel_id)
            
            total_human = [p['is_human'] for p in game.players].count(True)

            if total_human >= 1:    # modify this
                await self.director.start_game(game_id)
            else:
                pass
            
        elif feature_id == "Quit":
            if feature_call.arguments[0].value == 'Yes':
                await self.dismiss_game(channel_id, feature_call.sender)
                feature_data_list = [band.features['Cicada']]
                await self.send_update_features(channel_id, feature_data_list, [feature_call.sender])
            else:
                pass
        else:
            pass

    async def on_unknown_message(self, message_data):
        logger.warning(f"Received unknown message: {message_data}")
