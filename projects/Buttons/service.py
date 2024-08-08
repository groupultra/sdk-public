from moobius import Moobius
from moobius.types import Button, ButtonClick, InputComponent
from moobius import types


class ButtonService(Moobius):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    async def on_fetch_buttons(self, action):
        simple_button = Button(button_id='easy', button_text='Simple button.', dialog=False)
        button_args = [InputComponent(label='Pick a fruit!', type=types.DROPDOWN, optional=False, choices=['Apple', 'Banana', 'Coconut'], placeholder="Tasty!"),
                       InputComponent(label='Favorite color!', type=types.TEXT, optional=False, placeholder="Artsy!", choices=[])]
        complex_button = Button(button_id='hard', button_text='Pop-up button.', dialog=True, components=button_args)
        await self.send_update_buttons([simple_button, complex_button], action.channel_id, [action.sender])

    async def on_button_click(self, button_click: ButtonClick):
        print('Button click:', button_click)
        which_one = button_click.button_id
        txt = ''
        if which_one == 'easy':
            txt = 'Pressed the Simple button'
        elif which_one == 'hard':
            for a in button_click.components:
                if a.label == 'Favorite color!':
                    txt += ' Color: '+a.choice # Both kinds of arguments have a value.
                elif a.label == 'Pick a fruit!':
                    txt += ' Fruit: '+a.choice
        await self.send_message(txt, button_click.channel_id, button_click.sender, [button_click.sender])
