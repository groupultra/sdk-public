import random
import re
import json
import traceback

from datetime import datetime

from .cicada_game import CicadaGame
from .cicada_agent import CicadaAgent

class CicadaDirector:
    def __init__(self, resource_dir=None, send_to_audience=None, send_to_all_players=None, notify_player=None):
        super().__init__()

        self.resource_dir = resource_dir or 'resources/cicada/'
        self.record_file = f'{self.resource_dir}record.json'
        self._send_to_audience = send_to_audience or self._default_send_to_audience
        self._send_to_all_players = send_to_all_players or self._default_send_to_all_players
        self._notify_player = notify_player or self._default_notify_player
        self.games = {}

        self.records = {
            "sn": 0,
            "waiting_game_id": None,    # 正在等待玩家加入的游戏id，如果没有则为None
            "games": {}     # 所有未结束的游戏
        }

        """
        {
            "sn": 12,
            "waiting_game_id": None,

            "games": {
                "0001": {
                    "record_path": "resources/cicada/0001.json",
                },
            }
        }
        """

        self._load()
        self._load_games()
        self._save()


    async def _default_send_to_audience(self, game, content, sent_by=-1):
        print(f"Default send to audience:【Cicada {game.game_id}】{content} sent by Player {sent_by}")

    async def _default_send_to_all_players(self, game, content, sent_by=-1):
        print(f"Default send to all players:【Cicada {game.game_id}】{content} sent by Player {sent_by}")

    async def _default_notify_player(self, game, player_id, content, sent_by=-1):
        print(f"Default notify player:【Cicada {game.game_id}】{content} sent by Player {sent_by}")


    def _load(self):
        with open(self.record_file, 'a+', encoding='utf-8') as f:
            try:
                f.seek(0)
                self.records = json.load(f)
            except Exception as e:
                traceback.print_exc()

    def _load_games(self):
        for game_id in self.records['games']:
            self.games[game_id] = CicadaGame(from_file=self.records['games'][game_id]['record_path'])


    def query_real_id(self, real_id):
        for game_id in self.records['games']:
            game = self.games[game_id]
            for player_id in range(game.total_players):
                if game.players[player_id]['real_id'] == real_id:
                    return game_id, int(player_id)
                else:
                    pass
            else:
                pass
        
        return None, None


    def get_game(self, game_id):
        if game_id not in self.games:
            return None
        else:
            return self.games[game_id]


    def _save(self):
        with open(self.record_file, 'w', encoding='utf-8') as f:
            json.dump(self.records, f, indent=4)

    async def _agent_talk(self, game_id, player_id):
        game = self.games[game_id]
        chat_history = game.chat_history
        agent = CicadaAgent(
            total_players=game.total_players,
            total_rounds=game.total_rounds,
            char_limit=game.char_limit,
            vote_score=game.vote_score,
            voted_score=game.voted_score
        )

        try:
            say = await agent.talk(game.current_round, player_id, chat_history)
        except Exception as e:
            say = f"Error: {e}"

        return say

    async def _agent_vote(self, game_id, player_id):
        game = self.games[game_id]
        chat_history = game.chat_history
        agent = CicadaAgent(
            total_players=game.total_players,
            total_rounds=game.total_rounds,
            char_limit=game.char_limit,
            vote_score=game.vote_score,
            voted_score=game.voted_score
        )
        vote_output = await agent.vote(player_id, chat_history)

        try:
            return json.loads(vote_output)
        except Exception:
            traceback.print_exc()
            return []

    async def on_talk_attempt(self, game_id, player_id, content):
        game = self.games[game_id]
        status = game.try_to_talk(player_id, content)

        if status == game.SUCCESS:
            await self._send_to_all_players(game, content, sent_by=player_id)
            await self._send_to_audience(game, content, sent_by=player_id)

            if game.stage == game.STAGE_VOTE:
                await self._on_enter_stage_vote(game_id)
            elif game.stage == game.STAGE_TALK:
                say = f"Your turn now. Please say whatever you want to say."
                
                if game.players[game.current_turn]['real_id'] is None:
                    await self._let_ai_talk(game_id)
                else:
                    await self._notify_player(game, game.current_turn, say)
            else:
                raise Exception("Invalid stage")

            return True, None
        else:
            error = f"Error: {CicadaGame.error_to_msg[status]}"
            await self._notify_player(game, player_id, error)

            return False, status

    async def on_vote_attempt(self, game_id, player_id, content):
        game = self.games[game_id]

        if re.fullmatch(r'\d+', content):
            votes = [int(v) for v in content]
            ret = game.try_to_vote(player_id, votes)

            if ret == game.SUCCESS:
                await self._notify_player(game, player_id, f"You voted to {votes}")

                if game.stage == game.STAGE_END:
                    await self._on_enter_stage_end(game_id)
                else:
                    pass

                return True
            
            else:
                await self._notify_player(game, player_id, f"Error: {CicadaGame.error_to_msg[ret]}")

                return False
        else:
            await self._notify_player(game, player_id, f"Invalid vote format, please vote again to ALL players you believe are human. For example, send me 14 if you believe player 1 and 4 are human.")

            return False

    async def start_game(self, game_id):
        game = self.games[game_id]
        status = game.start()

        if status == game.SUCCESS:
            self.records['waiting_game_id'] = None
            self._save()

            await self._on_enter_stage_talk(game_id)
        else:
            raise Exception(f"Error: {CicadaGame.error_to_msg[status]}")


    async def on_human_join(self, real_id, name):
        if not self.records['waiting_game_id']:
            game_id = f"{self.records['sn']:04d}"
            
            self.records['sn'] += 1
            self.records['waiting_game_id'] = game_id

            file_name = f'{datetime.now().strftime("%Y%m%d%H%M%S")}_{random.randint(1000, 9999)}_{game_id}.json'
            record_path = f"{self.resource_dir}{file_name}"
            game = CicadaGame(game_id=game_id, record_path=record_path)
            self.games[game_id] = game

            self.records['games'][game_id] = {
                "record_path": record_path
            }

            self._save()
            
        else:
            game = self.games[self.records['waiting_game_id']]

        choices = list(set(list(range(game.total_players))) - set([i for i in range(game.total_players) if game.players[i]['real_id']]))
        player_id = random.choice(choices)
        game.add_human_player(name=name, player_id=player_id, real_id=real_id)

        say = f"Welcome to Cicada {game.game_id}, {name}! You are Player #{player_id}."
        await self._notify_player(game, player_id, say)

        return game.game_id

    async def dismiss_game(self, game_id):
        if game_id not in self.games:
            return
        else:
            game = self.games[game_id]

            await self._send_to_all_players(game, f"Game dismissed")
            await self._send_to_audience(game, f"Game dismissed")

            self.records['games'].pop(game_id, None)
            self.games.pop(game_id, None)

            if self.records['waiting_game_id'] == game_id:
                self.records['waiting_game_id'] = None
            else:
                pass
            
            self._save()


    async def on_load(self):
        for game_id in list(self.games.keys()):     # 固定一下，可能中途会有游戏结束导致size迭代中发生变化
            await self._direct(game_id)


    # 人：仅通知，人响应后外部触发_on_xxx
    # AI：通知并调用，直接触发_on_xxx
    # 刚刚发生游戏状态变化时立即调用一次，程序重启时也会在on_load()中自动调用
    async def _direct(self, game_id):
        game = self.get_game(game_id)

        if not game:
            return      # 可能会有 game_id 不存在的情况，比如重启初始化遍历通知时有游戏自动结束并删除记录
        else:
            if game.stage == game.STAGE_WAIT:
                say = f"Game {game_id} is waiting for players to join. Please press the Cicada key to join the game."
                await self._send_to_audience(game, say)
            elif game.stage == game.STAGE_TALK:
                if not game.players[game.current_turn]['is_human'] or game.players[game.current_turn]['is_offline']:
                    await self._let_ai_talk(game_id)
                else:
                    say = f"Your turn now. Please say whatever you want to say."
                    await self._notify_player(game, game.current_turn, say)
            elif game.stage == game.STAGE_VOTE:
                await self._on_enter_stage_vote(game_id)
            elif game.stage == game.STAGE_END:
                await self._on_enter_stage_end(game_id)
            else:
                raise Exception("Invalid stage!")


    async def _on_enter_stage_talk(self, game_id):
        game = self.games[game_id]

        say = f"Game {game_id} started. Now it's time to talk. Every player here (including yourself) could be either human or AI. Try to find humans in 3 rounds of conversations! Note: Also try to make yourself ambiguous to others to get higher scores\n"
        await self._send_to_audience(game, say)
        await self._send_to_all_players(game, say)

        for i in range(game.total_players):
            is_human = game.players[i]['is_human']
            
            if is_human:
                say = f"You are Player #{i}."

                if i == 0:
                    say += f" You are the first player to talk."
                else:
                    pass

                await self._notify_player(game, i, say)
            else:
                pass

        current_turn_real_id = game.players[game.current_turn]['real_id']

        if not current_turn_real_id:
            await self._let_ai_talk(game_id)
        else:
            say = f"Your turn now. Please say whatever you want to say."
            await self._notify_player(game, game.current_turn, say)


    async def _on_enter_stage_vote(self, game_id):
        say = f"Now it's time to vote. Please send any WHISPER message to ALL you think are human (including yourself)"
        game = self.games[game_id]

        await self._send_to_all_players(game, say)
        await self._send_to_audience(game, say)
        await self._let_all_ai_vote(game_id)


    async def _on_enter_stage_end(self, game_id):
        game = self.games[game_id]
        game.get_result()

        say = f"Vote ended. Here is the result: \n"

        for i in range(game.total_players):
            say += f"Player {i} voted to {game.players[i]['vote_to']}\n"

        await self._send_to_all_players(game, say)
        await self._send_to_audience(game, say)

        say = f"Game {game_id} ended. Here is the result: \n"
        
        for i in range(game.total_players):
            say += f"{'👤' if game.players[i]['is_human'] else '🤖'} Player {i}: "
            say += f"[{game.players[i]['name']}] {game.players[i]['total_score']} points\n"

        await self._send_to_all_players(game, say)
        await self._send_to_audience(game, say)

        self.games.pop(game_id, None)
        self.records["games"].pop(game_id, None)

        if self.records['waiting_game_id'] == game_id:
            self.records['waiting_game_id'] = None
        else:
            pass

        self._save()


    async def _let_ai_talk(self, game_id):
        game = self.games[game_id]
        say = await self._agent_talk(game_id, game.current_turn)
        tf, status = await self.on_talk_attempt(game_id, game.current_turn, say)   # todo: 多几次attempt

        if tf:
            pass
        else:
            say = f'Error [{game.error_to_msg[status]}].'
            await self.on_talk_attempt(game_id, game.current_turn, say)

    async def _let_all_ai_vote(self, game_id):
        game = self.games[game_id]

        for i in range(game.total_players):
            if (not game.players[i]['is_human'] or game.players[i]['is_offline']) and not game.players[i]['voted']:
                try:
                    vote = await self._agent_vote(game_id, i)
                except Exception as e:
                    vote = []
                game.try_to_vote(i, vote)
            else:
                pass

        if game.stage == game.STAGE_END:    # 最后一个是AI投的
            await self._on_enter_stage_end(game_id)
        else:
            pass
