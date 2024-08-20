from moobius import Moobius, MoobiusWand
from moobius.types import *
import moobius.types as types


class ButtonService(Moobius):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    async def on_refresh(self, action):
        simple_button = Button(button_id='easy', button_text='Simple button.')
        pieces = [InputComponent(label='Pick a fruit!', type=types.DROPDOWN, required=False, choices=['Apple', 'Banana', 'Coconut'], placeholder="Tasty!"),
                  InputComponent(label='Favorite color!', type=types.TEXT, required=False, placeholder="Artsy!", choices=[])]
        dialog = Dialog("options", components=pieces)
        complex_button = Button(button_id='hard', button_text='Pop-up button.', dialog=dialog)

        b0 = BottomButton(id="b0", submit=False, text='Dont send the click')
        b1 = BottomButton(id="b1", submit=True, text='Send it!')
        dialog1 = Dialog("options", components=[], bottom_buttons=[b0, b1])
        bottom_button = Button(button_id='bottom', button_text='Bottom button.', dialog=dialog1)
        await self.send_buttons([simple_button, complex_button, bottom_button], action.channel_id, [action.sender])

    async def on_button_click(self, button_click: ButtonClick):
        print('Button click:', button_click)
        which_one = button_click.button_id
        txt = ''
        if which_one == 'easy':
            txt = 'Pressed the Simple button'
        elif which_one == 'hard':
            txt = 'Pressed a fancy button choices:'
            for a in button_click.arguments:
                txt = txt+' '+a
        elif which_one == 'bottom':
            txt = "Bottom button: "+str(button_click)

        await self.send_message(txt, button_click.channel_id, button_click.sender, [button_click.sender])


if __name__ == "__main__":
    MoobiusWand().run(ButtonService, config='config/config.json')