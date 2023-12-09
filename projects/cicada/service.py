# demo_service.py

import asyncio
import json
import copy
import uuid
import random
from dataclasses import asdict
import traceback

from moobius.moobius_service import MoobiusService
from moobius.basic.types import Character, CharacterContext
from moobius.dbtools.moobius_band import MoobiusBand
from cicada.lib.cicada_director import CicadaDirector

from dacite import from_dict

class CicadaService(MoobiusService):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.resource_dir = 'cicada/games/'
        self.game_band_id = '372386d6-8435-4e76-b8d1-8fe18d3da323'

        self.director = CicadaDirector(
            resource_dir=self.resource_dir,
            send_to_audience = self._send_to_audience,
            send_to_all_players = self._send_to_all_players,
            notify_player = self._notify_player
        )

        self.default_game_status = {
            'last_game_id': None,
            # 'player_id': -999,
            'view_characters': []
        }

    async def on_start(self):
        """
        Called after successful connection to websocket server and service login success.
        """
        li = self.http_api.get_service_list()
        self.channel_ids = []

        for d in li:
            if d.get('service_id', None) == self.service_id:
                self.channel_ids = d.get('channel_ids', [])
                break

        print("channel_ids", self.channel_ids)
        
        # ==================== load features ====================

        with open('cicada/cicada_features.json', 'r') as f:
            features = json.load(f)

        for channel_id in self.channel_ids:
            self.bands[channel_id] = MoobiusBand(self.service_id, channel_id, db_settings=self.db_settings)
            
            real_characters = await self.fetch_real_characters(channel_id)

            for character in real_characters:
                character_id = character.user_id
                self.bands[channel_id].real_characters[character_id] = character

                if character_id not in self.bands[channel_id].game_status:
                    self.bands[channel_id].game_status[character_id] = copy.deepcopy(self.default_game_status)

            for feature in features:
                feature_id = feature["feature_id"]
                self.bands[channel_id].features[feature_id] = feature

            # ====================== uploadload avatars ======================

            with open ('cicada/cicada_names.json', 'r') as f:
                self.names = json.load(f)

            for local_id, name in self.names.items():
                if local_id not in self.bands[channel_id].avatars:
                    print(f'Uploading avatar {local_id}...')
                    file_name = f'cicada/icons/{local_id}.jpg'
                    avatar_uri = self.http_api.upload_file(file_name)
                    self.bands[channel_id].avatars[local_id] = avatar_uri
                else:
                    pass
        
        await self.director.on_load()

    def _make_character(self, band_id, local_id, nickname):
        username = f'{nickname}'
        avatar = self.bands[band_id].avatars[local_id]
        description = f'I am {nickname}!'

        data = self.http_api.create_service_user(self.service_id, username, nickname, avatar, description)
        character = from_dict(data_class=Character, data=data)

        return character

    async def _send_to_audience(self, game, content, sent_by=-1):
        print('send_to_audience')
        host_character = self._make_character(self.game_band_id, '0000', 'Cicada Host')
        game_status = self.bands[self.game_band_id].game_status

        audience = [cid for cid in game_status if not self.query_character(self.game_band_id, cid)[0]]

        if sent_by < 0:
            prefix = f'Game[{game.game_id}]: '
        else:
            prefix = f'Game[{game.game_id}] Player {sent_by} said: '

        await self.send_msg_down(
            channel_id=self.game_band_id,
            recipients=audience,
            subtype="text",
            message_content=f'{prefix}{content}',
            sender=host_character.user_id
        )

    async def _send_to_all_players(self, game, content, sent_by=-1):
        print('send_to_all_players')
        for player_id in range(game.total_players):
            real_id = game.players[player_id]['real_id']

            if not real_id:
                continue
            else:
                try:
                    if sent_by < 0:
                        sender_id = self._make_character(self.game_band_id, '0000', 'Cicada Host').user_id
                    elif sent_by == player_id:
                        continue  # no repeat
                    else:
                        sender_id = self.bands[self.game_band_id].game_status[real_id]['view_characters'][sent_by]['user_id']

                    await self.send_msg_down(
                        channel_id=self.game_band_id,
                        recipients=[real_id],
                        subtype="text",
                        message_content=f'{content}',
                        sender=sender_id
                    )
                except:
                    traceback.print_exc()
                    print(f'Error: send_to_all_players: send to Player {player_id} [{real_id}] failed.')


    async def _notify_player(self, game, player_id, content, sent_by=-1):
        print('notify_player')
        real_id = game.players[player_id]['real_id']

        if not real_id or player_id == sent_by:     # no repeat!
            return
        else:
            try:
                character = self._make_character(self.game_band_id, '0000', 'Cicada Host')
                prefix = f'Game[{game.game_id}] Host: ' if sent_by < 0 else f'Game[{game.game_id}] Player {sent_by}: '
            
                await self.send_msg_down(
                    channel_id=self.game_band_id,
                    recipients=[real_id],
                    subtype="text",
                    message_content=f'{prefix}{content}',
                    sender=character.user_id
                )
            
            except:
                traceback.print_exc()
                print(f'Error: notify_player: notify Player {player_id} [{real_id}] failed.')



    # on_xxx, default implementation, to be override
    async def on_msg_up(self, msg_up):
        """
        Handle the received message.
        """
        print("on_msg_up", msg_up)

        channel_id = msg_up.channel_id
        sender = msg_up.context.sender
        game_id, player_id = self.query_character(channel_id, sender)

        if game_id:
            if msg_up.subtype == "text":
                text = msg_up.content['text']
                game = self.director.get_game(game_id)
                host_character = self._make_character(self.game_band_id, '0000', 'Cicada Host')
                
                if game.stage == game.STAGE_WAIT:
                    await self.send_msg_down(
                        channel_id=msg_up.channel_id,
                        recipients=[sender],
                        subtype="text",
                        message_content=f'Please wait for other players to join!',
                        sender=host_character.user_id
                    )

                elif game.stage == game.STAGE_TALK:
                    await self.director.on_talk_attempt(game_id, player_id, text)
                    
                elif game.stage == game.STAGE_VOTE:
                    recipients = msg_up.context.recipients

                    vote_to = []

                    game_status = self.bands[msg_up.channel_id].game_status[sender]

                    for i in range(game.total_players):
                        if game_status['view_characters'][i]['user_id'] in recipients:
                            vote_to.append(i)
                        else:
                            pass
                    
                    text = ''.join([str(v) for v in vote_to])     # for compatibility with the old version
                    
                    await self.director.on_vote_attempt(game_id, player_id, text)
                
                elif game.stage == game.STAGE_END:
                    await self.send_msg_down(
                        channel_id=msg_up.channel_id,
                        recipients=[sender],
                        subtype="text",
                        message_content=f'The Game has ended!',
                        sender=host_character.user_id
                    )

                else:
                    pass
            
            else:
                host_character = self._make_character(self.game_band_id, '0000', 'Cicada Host')

                await self.send_msg_down(
                    channel_id=msg_up.channel_id,
                    recipients=[sender],
                    subtype="text",
                    message_content=f'Please send text messages only!',
                    sender=host_character.user_id
                )
        else:
            msg_down = self.msg_up_to_msg_down(msg_up, remove_self=True)
            await self.send(payload_type='msg_down', payload_body=msg_down)


    async def refresh_audience_views(self, channel_id):
        audience = [cid for cid in self.bands[channel_id].game_status if self.query_character(channel_id, cid)[0] is None]
        audience_characters = [self.bands[channel_id].real_characters[cid] for cid in audience if cid in self.bands[channel_id].real_characters]
        audience_features = [self.bands[channel_id].features['Cicada']]

        await self.send_update_userlist(channel_id, audience_characters, audience)
        await self.send_update_features(channel_id, audience_features, audience)


    # game_id, player_id
    def query_character(self, channel_id, character_id):
        return self.director.query_real_id(character_id)

    async def on_action(self, action):
        """
        Handle the received action.
        """
        print("on_action", action)
        sender = action.sender
        channel_id = action.channel_id

        if action.subtype == "fetch_userlist":
            print("fetch_userlist")
            game_status_dict = self.bands[channel_id].game_status

            if sender in game_status_dict:
                pass
            else:
                game_status_dict[sender] = copy.deepcopy(self.default_game_status)
            
            game_status = game_status_dict[sender]
            
            if self.query_character(channel_id, sender)[0]:
                await self.send_update_userlist(action.channel_id, game_status['view_characters'], [sender])
            else:
                audience = [cid for cid in self.bands[channel_id].game_status if self.query_character(channel_id, cid)[0] is None]
                audience_characters = [self.bands[channel_id].real_characters[cid] for cid in audience]           
                await self.send_update_userlist(channel_id, audience_characters, [sender])

        elif action.subtype == "fetch_features":
            print("fetch_features")
            
            if self.query_character(channel_id, sender)[0]:
                feature_data_list = [self.bands[channel_id].features['Quit']]
            else:
                feature_data_list = [self.bands[channel_id].features['Cicada']]
            
            await self.send_update_features(action.channel_id, feature_data_list, [action.sender])

        elif action.subtype == "fetch_playground":
            print("fetch_playground")
            """
            content = self.db_helper.get_playground_info(client_id)
            await self.send_update_playground(channel_id, content, [client_id])
            """
        
        elif action.subtype == "join_channel":
            print("join_channel")

            channel_id = action.channel_id
            data = self.http_api.fetch_user_profile([sender])

            if data['code'] == 10000:
                d = data['data'][sender]
                d['user_id'] = sender
                character = from_dict(data_class=Character, data=d)
                
                self.bands[action.channel_id].real_characters[sender] = character
                self.bands[action.channel_id].game_status[sender] = copy.deepcopy(self.default_game_status)

                await self.refresh_audience_views(channel_id)
                audience = [cid for cid in self.bands[channel_id].game_status if self.query_character(channel_id, cid)[0] is None]

                await self.send_msg_down(
                    channel_id=channel_id,
                    recipients=audience,
                    subtype="text",
                    message_content=f'{character.user_context.nickname} joined the band!',
                    sender=sender
                )
            
            else:
                print("Error fetching user profile:", data['msg'])
        
        elif action.subtype == "leave_channel":
            print("leave_channel")
            channel_id = action.channel_id
            character = self.bands[action.channel_id].real_characters.pop(sender, None)

            await self.dismiss_game(channel_id, sender)     # refresh audience view here

            self.bands[action.channel_id].game_status.pop(sender, None)


            audience = [cid for cid in self.bands[channel_id].game_status if self.query_character(channel_id, cid)[0] is None]

            await self.send_msg_down(
                channel_id=channel_id,
                recipients=audience,
                subtype="text",
                message_content=f'{character.user_context.nickname} left the band (but still talks~)!',
                sender=sender
            )

            # await self.refresh_audience_views(channel_id)


        elif action.subtype == "fetch_channel_info":
            print("fetch_channel_info")
            """
            await self.send_update_channel_info(channel_id, self.db_helper.get_channel_info(channel_id))
            """
        else:
            print("Unknown action subtype:", action_subtype)


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
            print(f'Warning: Attempted to dismiss an empty game!')

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
        print("Feature call received:", feature_call)
        sender = feature_call.sender
        channel_id = feature_call.channel_id
        feature_id = feature_call.feature_id
        feature_name = self.bands[channel_id].features[feature_id]["feature_name"]
        character = self.bands[channel_id].real_characters[feature_call.sender]
        nickname = character.user_context.nickname

        if feature_id == "Cicada":
            game_id, player_id = self.query_character(channel_id, sender)
 
            if game_id:
                print(f'Warning: {nickname} attempted to join a game twice!')
                return
            else:
                await self.director.on_human_join(sender, name=nickname)
            
            game_id, player_id = self.query_character(channel_id, sender)
            game = self.director.get_game(game_id)

            game_band = self.bands[self.game_band_id]
            game_status = copy.deepcopy(self.default_game_status)
            
            """
            game_status = copy.deepcopy(game_band.game_status.get(feature_call.sender, None))

            if not game_status:
                game_status = copy.deepcopy(self.default_game_status)   # in case it has not been recorded
            else:
                pass
            """

            game_status['last_game_id'] = game_id

            feature_data_list = [self.bands[channel_id].features['Quit']]
            await self.send_update_features(channel_id, feature_data_list, [feature_call.sender])
                           
            local_ids = random.sample(list(self.names.keys())[1:], game.total_players)
            names = [f'Player {i} - {self.names[local_ids[i]]}' for i in range(game.total_players)]
            
            for i in range(game.total_players):
                if i != player_id:
                    game_status['view_characters'].append(asdict(self._make_character(self.game_band_id, local_ids[i], names[i])))
                else:
                    game_status['view_characters'].append(asdict(character))
            
            game_band.game_status[feature_call.sender] = game_status

            await self.send_update_userlist(self.game_band_id, game_status['view_characters'], [feature_call.sender])
            await self.refresh_audience_views(channel_id)
            
            total_human = [p['is_human'] for p in game.players].count(True)

            if total_human >= 1:
                await self.director.start_game(game_id)

            else:
                pass
            
        elif feature_id == "Quit":
            if feature_call.arguments[0].value == 'Yes':
                await self.dismiss_game(channel_id, feature_call.sender)
                feature_data_list = [self.bands[channel_id].features['Cicada']]
                await self.send_update_features(channel_id, feature_data_list, [feature_call.sender])
            else:
                pass
        else:
            pass


    async def on_unknown_message(self, message_data):
        """
        Handle the received unknown message.
        """
        print("Received unknown message:", message_data)
