.. _menu-canvas-tut:

The context menu and the canvas are two secondary GUI elements that can be useful.

The Canvas
===================================================================================

This is a place to display information to users, and is.

The canvas is a list of CanvasElement objects that specify either a text path or image URL path. Each element *becomes one pane* and can include one text string (markdown) and one image URL.

Like many other configurations, it is best to set up the menu from the fetch callback. Note that the canvas is automatically expanded:

.. code-block:: Python
    async def on_fetch_canvas(self, action):
        canvas_elements = [CanvasElement(text="Some **text** here, along with an image", path="https://www.moobius.net/images/index/indexH2.png")]
        canvas_elements.append(CanvasElement(path="https://www.moobius.net/images/index/indexBg.png"))
        canvas_elements.append(CanvasElement(text="More `text` here.\nWith multiple lines.\nSeperated by newlines."))
        await self.send_update_canvas(action.channel_id, canvas_elements, [action.sender])
        await self.send_update_style(action.channel_id, [StyleElement(widget="canvas", display="visible", expand="true")], [action.sender])

This canvas is not interactive, it is just a place to display stuff. Use Buttons, message, and the context menu for interaction.

The Context menu
===================================================================================

This is a place to handle right-clicks on various messages.

The actual command requires specifying a name, id, and which message types (text, image, etc) to enable right-click on.

.. code-block:: Python
    ContextMenuElement(item_name='Text here', item_id='use this in your program', support_subtype=[types.TEXT, types.IMAGE, etc])

.. code-block:: Python
    async def on_fetch_context_menu(self, action):
    elements = []
    menu_types = [types.TEXT, types.IMAGE, types.AUDIO, types.FILE, types.CARD]
    await self.send_message('types supported: '+str(menu_types), action.channel_id, action.sender, [action.sender])

    for i in range(len(menu_types)):
        for j in range(3):
            elements.append(ContextMenuElement(item_name=menu_types[i]+' item '+str(j), item_id=menu_types[i]+str(j), support_subtype=[menu_types[i]]))
    await self.send_update_context_menu(action.channel_id, elements, [action.sender])

To respond to the message, use the on_context_menu_click callback:

.. code-block:: Python
    async def on_context_menu_click(self, context_click: MenuClick):
        txt = 'Menu choice: '+context_click.item_id+' Message content: '+str(context_click.message_content)
        await self.send_message(txt, context_click.channel_id, context_click.sender, [context_click.sender])

There is also a way to put pop-up input argumnets inside the menu option using the arguments flag, should this advance use-case be needed:

.. code-block:: Python
    menu_element.arguments = [ButtonArgument(name='popup', type='string', optional=True, values=None, placeholder='Write the input as a string.')]
