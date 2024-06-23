.. _buttons-tut:

For implementing buttons, there are two key functions.

The finished tutorial is in the `public repo <https://github.com/groupultra/sdk-public/tree/main/projects/Buttons>`

Implementing buttons
==============================================

There are three functions that are needed.


**self.send_update_buttons(update)**
This function sends buttons to a given list of users in a given channel.

**self.on_fetch_buttons(action)**
This is called when the client asks the Platform what buttons should be displayed. This is one of several fetch functions.

This is a convienent place to call send_update_buttons for initializing each user with thier default buttons.

The Action object tells us who and in what channel to send button updates to.

The combined code of the two functions:

.. code-block:: Python
    async def on_fetch_buttons(self, action):
        simple_button = Button(button_id='easy', button_name='easy', button_text='Simple button.', new_window=False)
        button_args = [ButtonArgument(name='Pick a fruit!', type='enum', optional=False, values=['Apple', 'Banana', 'Coconut'], placeholder="Tasty!"),
                        ButtonArgument(name='Favorite color!', type='string', optional=False, placeholder="Artsy!", values=[])]
        complex_button = Button(button_id='hard', button_name='hard', button_text='Pop-up button.', new_window=True, arguments=button_args)
        await self.send_update_buttons(action.channel_id, [simple_button, complex_button], [action.sender])


**self.on_button_click(action)**
This function responds to button clicks. The Action object tells us who sent it, which allows us to easily send the results back the the sender:

.. code-block:: Python
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

Simple vs complex buttons
==============================================
"Simple" buttons are just buttons that the user clicks on. Just specify a button_id, button_name, and button_text (the text is what is displayed). Set new_window to False.

In the above example there is one simple button 

.. code-block:: Python
    simple_button = Button(button_id='easy', button_name='easy', button_text='Simple button.', new_window=False)

"Complex" buttons are buttons that open up a pop-up menu where the user selects an option. new_window has to be True and there are button arguments. In this example:

.. code-block:: Python
    button_args = [ButtonArgument(name='Pick a fruit!', type='enum', optional=False, values=['Apple', 'Banana', 'Coconut'], placeholder="Tasty!"),
                    ButtonArgument(name='Favorite color!', type='string', optional=False, placeholder="Artsy!", values=[])]
    complex_button = Button(button_id='hard', button_name='hard', button_text='Pop-up button.', new_window=True, arguments=button_args)
