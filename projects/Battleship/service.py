# TODO: work in progress, namely the actual game mechanics (the SDK interaction should need none or little change).
from moobius import Moobius
from moobius.types import ButtonClick, Button, StyleItem, CanvasItem, InputComponent
import moobius.types as types
from moobius import MoobiusWand

SHIPS = {'kayak':[1,1], 'Viking-boat':[2,1],
         'scout':[3,1], 'battleship':[4,1],
         'aircraft-carrier':[5,1],
         'weaponized-cruise-ship':[5,2],
         'floating-city':[6,3]}

WEAPONS = {'cannon':[1,1], 'missle':[3,1], 'depth-charge':[3,3]}
WEAPONCOUNTS = {'cannon':65536, 'missle':6, 'depth-charge':2}


class BattleGame():
    """Ships, on a board."""

    def __init__(self, r=8, c=8, ships=6):
        """Initialize the ships."""

        # Id's of ship:
        self.grid = [[-1]*c for _ in range(r)]
        self.attacked = [[False]*c for _ in range(r)] # Attacked.

        TODO

    def random_add_ship(self, ship_name):
        """Randomally adds ship_name to self.
        Returns True if there was space, False if there was no space and it had to add the ship."""
        TODO

    def attack_and_report(row_ixs, col_ixs):
        """Attack row_ixs/col_ixs. Any sunk ships are replaced with -1s and reported.
        Ignores out-of-bounds ixs."""

        next_to_weight = 1 # Next to a ship.
        hit_weight = 8 # Hit any ship.
        sink_weight = 16 # Multiplied by the ship size!

        TODO
        return reports, total_sinkage


class Player():
    """More powerful weapons are more limited."""
    def __init__(self):
        self.weapons = WEAPONCOUNTS.copy()
        self.sinkage = 0
        self.reports = []

    def get_attack(self, r, c, weapon):
        """Uses up a weapon and gets an attack.
        If the weapon is no longer in the arsenal raises an Exception."""
        TODO
        return rows_attk, cols_attk

    def get_buttons(self):
        """Current buttons for attacking."""
        TODO

class BattleshipService(Moobius):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.games = {} # One game per channel.

    async def on_channel_init(self, channel_id):
        self.games[channel_id] = {'players':{}, 'game': None}

    async def _update_buttons(self, channel_id, user_id):
        """Updates the buttons to match the state, and updates the canvas."""
        buttons = [Button(button_id='new_game', button_name='new_game', button_name='New game/restart', dialog=False)]
        canvas_text = 'No active game'
        if user:= self.games[channel_id].get(user_id, None):
            canvas_text = 'Sinkage: '+user.sinkage+'\n'+'\n'.join(user.reports)
            for weapon, count in user.weapons():
                if count>0:
                    button_args = [InputComponent(label='row', type=types.STRING, required=False, placeholder='Row'),
                                   InputComponent(label='col', type=types.STRING, required=False, placeholder='Column')]
                    buttons.append(Button(button_id=weapon, button_name=weapon, button_name=weapon+f' ({count})', dialog=True,
                                          components=button_args))
        await self.send_canvas([CanvasItem(text=canvas_text)], channel_id, [user_id])
        await self.send_buttons(buttons, channel_id, [user_id])

    async def on_refresh(self, action):
        await self.send_style([StyleItem(widget="canvas", display="visible", expand=True)], action.channel_id, [action.sender])
        await self._update_buttons(action.channel_id, action.sender)

    async def on_button_click(self, button_click: ButtonClick):
        """Buttons depend on the game state."""
        the_game = self.games[button_click.channel_id]
        if button_click.button_id in list(WEAPONS.keys()):
            row = 0; col = 0
            for btn_arg in button_click.arguments:
                if btn_arg.name=='row':
                    row = int(btn_arg.value)
                if btn_arg.name=='col':
                    col = int(btn_arg.value)
            rows_attk, cols_attk = the_game['players'][button_click.sender].get_attack(row, col, button_click.button_id)
            reports, sinkage = the_game['game'].attack_and_report(rows_attk, cols_attk)
            note = '\n'.join(reports) + '\n'+f'Total sinkage this turn={sinkage}'
            await self.send_message(note, button_click.channel_id, button_click.sender, [button_click.sender])
            the_game['players'][button_click.sender].reports += reports
            the_game['players'][button_click.sender].sinkage += sinkage
        elif button_click.button_id == 'new_game':
            real_ids = await self.fetch_member_ids(button_click.channel_id)
            for r_id in real_ids:
                the_game[r_id] = Player()
            the_game['game'] = BattleGame(r=8, c=8, ships=6) # Randomally place ships down.
            await self.send_message('Game reset', button_click.channel_id, button_click.sender, [button_click.sender])
        await self._update_buttons(self, button_click.channel_id, button_click.sender)

    async def one_message_up(self, message):
        await self.send_message(message) # Ez group chat.


if __name__ == "__main__":
    MoobiusWand().run(BattleshipService, config='config/config.json')