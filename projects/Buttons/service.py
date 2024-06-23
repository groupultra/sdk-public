from moobius import Moobius
from moobius.types import Button, ButtonClick, ButtonArgument

class ButtonService(Moobius):
    def __init__(self, log_file="logs/service.log", error_log_file="logs/error.log", **kwargs):
        super().__init__(log_file=log_file, error_log_file=error_log_file, **kwargs)

    async def on_fetch_buttons(self, action):
        simple_button = Button(button_id='easy', button_name='easy', button_text='Simple button.', new_window=False)
        button_args = [ButtonArgument(name='Pick a fruit!', type='enum', optional=False, values=['Apple', 'Banana', 'Coconut'], placeholder="Tasty!"),
                       ButtonArgument(name='Favorite color!', type='string', optional=False, placeholder="Artsy!", values=[])]
        complex_button = Button(button_id='hard', button_name='hard', button_text='Pop-up button.', new_window=True, arguments=button_args)
        await self.send_update_buttons(action.channel_id, [simple_button, complex_button], [action.sender])

    async def on_button_click(self, button_click: ButtonClick):
        which_one = button_click.button_id
        txt = ''
        if which_one == 'easy':
            txt = 'Pressed the Simple button'
        elif which_one == 'hard':
            for a in button_click.arguments:
                if a.name == 'Favorite color!':
                    txt += ' Color: '+a.value # Both kinds of arguments have a value.
                elif a.name == 'Pick a fruit!':
                    txt += ' Fruit: '+a.value
        await self.send_message(txt, button_click.channel_id, button_click.sender, [button_click.sender])
