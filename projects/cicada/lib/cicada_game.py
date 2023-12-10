import json


class CicadaGame:
    SUCCESS = 0
    ERR_TOO_VERBOSE = 1
    ERR_NOT_YOUR_TURN = 2
    ERR_NOT_TALK_STAGE = 3
    ERR_NOT_VOTE_STAGE = 4
    ERR_ALREADY_VOTED = 5
    ERR_INVALID_VOTES = 6
    ERR_NOT_ENDED = 7
    ERR_ALREADY_STARTED = 8
    ERR_INVALID_PLAYER_ID = 9
    ERR_NOT_FINISHED = 10
    ERROR_ALREADY_ENDED = 11

    STAGE_WAIT = 100
    STAGE_TALK = 101
    STAGE_VOTE = 102
    STAGE_END = 103

    error_to_msg = {
        SUCCESS: "Success",
        ERR_TOO_VERBOSE: "Too verbose",
        ERR_NOT_YOUR_TURN: "Not your turn",
        ERR_NOT_TALK_STAGE: "Not talk stage",
        ERR_NOT_VOTE_STAGE: "Not vote stage",
        ERR_ALREADY_VOTED: "Already voted",
        ERR_INVALID_VOTES: "Invalid votes",
        ERR_NOT_ENDED: "Not ended",
        ERR_ALREADY_STARTED: "Already started",
        ERR_INVALID_PLAYER_ID: "Invalid player id",
        ERR_NOT_FINISHED: "Not finished",
        ERROR_ALREADY_ENDED: "Already ended"
    }

    def __init__(self, from_file=None, total_players=5, total_rounds=3, vote_score=25, voted_score=100, char_limit=500, game_id='NO_GAME_ID', record_path=None):
        self.stage = None
        self.current_turn = None
        if not from_file:
            self._init_new(total_players, total_rounds, vote_score, voted_score, char_limit, game_id, record_path)
        else:
            self._init_from_file(from_file)

    def _init_from_file(self, from_file):
        with open(from_file, 'r', encoding='utf-8') as f:
            record = json.load(f)
            self.total_players = record['total_players']
            self.total_rounds = record['total_rounds']
            self.vote_score = record['vote_score']
            self.voted_score = record['voted_score']

            self.game_id = record['game_id']
            self.record_path = record['record_path']
            self.char_limit = record['char_limit']

            self.current_round = record['current_round']
            self.current_turn = record['current_turn']

            self.stage = record['stage']
            self.players = record['players']

    def _init_new(self, total_players, total_rounds, vote_score, voted_score, char_limit, game_id, record_path):
        self.total_players = total_players
        self.total_rounds = total_rounds
        self.vote_score = vote_score
        self.voted_score = voted_score

        self.char_limit = char_limit

        self.game_id = game_id
        self.record_path = record_path
        
        self.current_round = 0
        self.current_turn = 0

        self.stage = self.STAGE_WAIT

        self.players = [{
            "name": f"Agent {i}",
            "is_offline": False,
            "is_human": False,
            "real_id": None,
            "conversations": [],
            "voted": False,
            "vote_to": [],      # vote to all humans
            "total_score": 0
        } for i in range(self.total_players)]

    @property
    def record(self):
        return {
            "game_id": self.game_id,
            
            "total_players": self.total_players,
            "total_rounds": self.total_rounds,
            "char_limit": self.char_limit,
            "vote_score": self.vote_score,
            "voted_score": self.voted_score,
            
            "current_round": self.current_round,
            "current_turn": self.current_turn,

            "record_path": self.record_path,

            "stage": self.stage,
            "players": self.players
        }

    @property
    def is_finished(self):
        return self.stage == self.STAGE_END

    def start(self):
        if self.stage != self.STAGE_WAIT:
            return self.ERR_ALREADY_STARTED
        else:
            self.stage = self.STAGE_TALK
            self.save()
            return self.SUCCESS

    def add_human_player(self, name, player_id, real_id):
        if self.stage != self.STAGE_WAIT:
            return self.ERR_ALREADY_STARTED
        elif player_id >= self.total_players or player_id < 0:
            return self.ERR_INVALID_PLAYER_ID
        else:
            self.players[player_id]['name'] = name
            self.players[player_id]['is_human'] = True
            self.players[player_id]['real_id'] = real_id
            self.save()

            return self.SUCCESS

    def save(self):
        if not self.record_path:
            return
        else:
            with open(self.record_path, 'w', encoding='utf-8') as f:
                json.dump(self.record, f, indent=4)

    def try_to_talk(self, player_id, content):
        if self.stage != self.STAGE_TALK:
            return self.ERR_NOT_TALK_STAGE
        elif player_id != self.current_turn:
            return self.ERR_NOT_YOUR_TURN
        elif len(content) > self.char_limit:
            return self.ERR_TOO_VERBOSE
        else:
            self.players[player_id]['conversations'].append(content)
            self.current_turn += 1
            
            if self.current_turn == self.total_players:
                self.current_turn = 0
                self.current_round += 1

                if self.current_round == self.total_rounds:
                    self.stage = self.STAGE_VOTE
                    self.save()
                    return self.SUCCESS
                else:
                    self.save()
                    return self.SUCCESS
            else:
                self.save()
                return self.SUCCESS
    
    # vote_to的合法性由调用者保证
    def try_to_vote(self, player_id, vote_to=()):
        if self.stage != self.STAGE_VOTE:
            return self.ERR_NOT_VOTE_STAGE
        elif self.players[player_id]['voted']:
            return self.ERR_ALREADY_VOTED
        else:
            if not all([v in range(self.total_players) for v in vote_to]):
                return self.ERR_INVALID_VOTES
            else:
                vote_to = set(vote_to)
                vote_to.discard(player_id)
                vote_to = list(vote_to)     # 去重，去掉自己
                print(f"{player_id} votes to {vote_to}.")

                self.players[player_id]['voted'] = True
                self.players[player_id]['vote_to'] = vote_to

                if all([p['voted'] for p in self.players]):
                    self.stage = self.STAGE_END
                    self.save()
                    return self.SUCCESS
                else:
                    self.save()
                    return self.SUCCESS
    
    def get_result(self):
        if not self.is_finished:
            return self.ERR_NOT_FINISHED
        else:
            correct_vote_count = [0 for _ in range(self.total_players)]
            voted_count = [0 for _ in range(self.total_players)]

            for i in range(self.total_players):
                for j in range(self.total_players):
                    if j == i:
                        continue    # 自己不算
                    elif i in self.players[j]['vote_to']: # j投了i
                        voted_count[i] += 1

                        if self.players[i]['is_human'] and not self.players[i]['is_offline']:
                            correct_vote_count[j] += 1
                        else:
                            pass
                    else:   # j没投i
                        if self.players[i]['is_human'] and not self.players[i]['is_offline']:
                            pass
                        else:
                            correct_vote_count[j] += 1

            for i in range(self.total_players):
                vote_score = self.vote_score * correct_vote_count[i]
                
                bias = abs(voted_count[i] / (self.total_players - 1) - 0.5) * 2
                voted_score = self.voted_score * (1 - bias)   # 刚好一半的人投了这个人，那么这个人得到的分数最高

                self.players[i]['total_score'] = int(vote_score + voted_score)
                self.save()

            return self.players

    @property
    def game_log(self):
        log = "【Cicada🪰 Game】"
        log += f"Game ID = {self.game_id}\n"
        log += f"Game Parameters: \n"
        log += f"    Total Players = {self.total_players}\n"
        log += f"    Total Rounds = {self.total_rounds}\n"
        log += f"    Vote Score = {self.vote_score}\n"
        log += f"    Voted Score = {self.voted_score}\n"
        log += f"    Char Limit = {self.char_limit}\n"
        # log += f"    Record Path = {self.record_path}\n"
        log += f"    Current Round = {self.current_round}\n"
        log += f"    Current Turn = {self.current_turn}\n"
        log += f"    Stage = {self.stage}\n"
        log += f"    Players: \n"
        
        for i in range(self.total_players):
            log += f"    Player {i}: \n"
            log += f"        Name = {self.players[i]['name'] if self.is_finished else '***'}\n"
            log += f"        Is Offline = {self.players[i]['is_offline']}\n"
            log += f"        Is Human = {self.players[i]['is_human'] if self.is_finished else '***'}\n"
            log += f"        Real ID = {self.players[i]['real_id'] if self.is_finished else '***'}\n"
            log += f"        Conversations = {self.players[i]['conversations']}\n"
            log += f"        Voted = {self.players[i]['voted']}\n"
            log += f"        Vote To = {self.players[i]['vote_to'] if self.is_finished else '***'}\n"
            log += f"        Total Score = {self.players[i]['total_score']}\n"

        return log

    @property
    def chat_history(self):
        msg = ""
        
        if self.stage == self.STAGE_WAIT:
            msg += "Cicada🪰 Game has not started yet."
        else:
            for round in range(self.current_round + 1):
                for turn in range(self.total_players):
                    if round == self.current_round and turn == self.current_turn:
                        break
                    else:
                        msg += f"Player {turn}: {self.players[turn]['conversations'][round]}\n"

        return msg
