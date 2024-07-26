.. _menu-canvas-tut:

The context menu and the canvas are secondary GUI elements that can round out a more complete experience for the end-users.

The Canvas
===================================================================================

The canvas is a collapsable canvas that can show text and images to users. It is useful because it does not
get buried by the chat messages.


The canvas is a list of CanvasElement objects that specify either a text path or image URL path. Each element *becomes one pane* and can include one text string (markdown) and/or one image URL.

Similar to handling buttons, it is best to call `send_update_canvas` from within `on_fetch_canvas`.

This example creates a simple canvase with three elements:

.. code-block:: Python

    async def on_fetch_canvas(self, action):
        canvas_elements = [CanvasElement(text="Some **text** here, along with an image", path="https://www.moobius.net/images/index/indexH2.png")]
        canvas_elements.append(CanvasElement(path="https://www.moobius.net/images/index/indexBg.png"))
        canvas_elements.append(CanvasElement(text="More `text` here.\nWith multiple lines.\nSeperated by newlines."))
        await self.send_update_canvas(action.channel_id, canvas_elements, [action.sender])
        await self.send_update_style(action.channel_id, [StyleElement(widget="canvas", display="visible", expand="true")], [action.sender])

This canvas is not interactive, it is just a place to display information to the user.

The Context Menu
===================================================================================

The context menu controls right-click behavior when a user clicks a message. This is the primary way to
make messages interactive.

The menu is a list of `ContextMenuElement` objects. Each object specifies the name and which message type (text, image, audio, file, and card) it applies to.

.. code-block:: Python

    ContextMenuElement(item_name='Text here', item_id='use this in your program', support_subtype=[types.TEXT, types.IMAGE, etc])

Similar to handling buttons and the canvas, it is best to call `send_update_context_menu` from within `on_fetch_context_menu`.
This example will respond differently to each message type:

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


Demo code
================================
The demo code is available on

`the public repo <https://github.com/groupultra/sdk-public/tree/main/projects/Menu Canvas>`.
