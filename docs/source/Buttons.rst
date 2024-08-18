.. _buttons-tut:

###################################################################################
Buttons
###################################################################################


Buttons appear just below the group chat (just above the message box). They are the main GUI component the user interacts and can open
up choice and textboxes that accept user input.

Implementing buttons

There are three functions that are needed to get a button to work.


**self.on_fetch_buttons(action)**
This is called when the client asks the Platform what buttons should be displayed. This is one of several fetch functions.

**self.send_update_buttons(update)**
This function sends buttons to a given list of users in a given channel.

This is commonly called inside of `on_fetch_buttons`. This is example code that creates two buttons, one is a simple button
but the other opens up a pop-up menu when pressed:

.. code-block:: Python

    async def on_refresh(self, action):
        simple_button = Button(button_id='easy', button_name='Simple button.', new_window=False)
        button_args = [ButtonArgument(name='Pick a fruit!', type='enum', values=['Apple', 'Banana', 'Coconut'], placeholder="Tasty!"),
                        ButtonArgument(name='Favorite color!', type='string', placeholder="Artsy!", values=[])]
        complex_button = Button(button_id='hard', button_name='Pop-up button.', new_window=True, arguments=button_args)
        await self.send_update_buttons([simple_button, complex_button], action.channel_id, [action.sender])


**self.on_button_click(action)**
This function responds to button clicks and accepts a ButtonClick object as it's only argument.

The ButtonClick tells us who sent it and information about what was pressed as well as what menu choices were choosen (if it opens a menu).
This example uses the `button_click.sender` to send a confirmation message back to the user who pressed the button.

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
"Simple" buttons are just buttons that the user clicks on.
They only have a button_id and button_name specified. The button_id is used by your service to identify which button was pressed
while the button name is displayed in the browser.

In the above example there is one simple button:

.. code-block:: Python

    simple_button = Button(button_id='easy', button_name='easy', button_name='Simple button.', new_window=False)

"Complex" buttons are buttons that open up a pop-up menu where the user selects an option.
The parameter `new_window` has to be True and a list of ButtonArgument objects provided. In this example:

.. code-block:: Python

    button_args = [ButtonArgument(name='Pick a fruit!', type='enum', values=['Apple', 'Banana', 'Coconut'], placeholder="Tasty!"),
                    ButtonArgument(name='Favorite color!', type='string', placeholder="Artsy!", values=[])]
    complex_button = Button(button_id='hard', button_name='hard', button_name='Pop-up button.', new_window=True, arguments=button_args)


Demo code
================================
The demo code is available on

`the public repo <https://github.com/groupultra/sdk-public/tree/main/projects/Buttons>`.
