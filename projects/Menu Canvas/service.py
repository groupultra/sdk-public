from moobius import Moobius
from moobius.types import CanvasElement, MenuClick, StyleElement, ContextMenuElement
import moobius.types as types

class MenuCanvasService(Moobius):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    async def on_fetch_canvas(self, action):
        canvas_elements = [CanvasElement(text="Some **text** here, along with an image. Try sending a message and richt-clicking on it.", path="https://www.moobius.net/images/index/indexH2.png")]
        canvas_elements.append(CanvasElement(path="https://www.moobius.net/images/index/indexBg.png"))
        canvas_elements.append(CanvasElement(text="More `text` here.\nWith multiple lines.\nSeperated by newlines."))
        await self.send_update_canvas(canvas_elements, action.channel_id, [action.sender])
        await self.send_update_style([StyleElement(widget="canvas", display="visible", expand=True)], action.channel_id, [action.sender])

    async def on_fetch_context_menu(self, action):
        elements = []
        menu_types = [types.TEXT, types.IMAGE, types.AUDIO, types.FILE, types.CARD]
        await self.send_message('types supported: '+str(menu_types), action.channel_id, action.sender, [action.sender])

        for i in range(len(menu_types)):
            for j in range(3):
                elements.append(ContextMenuElement(item_text=menu_types[i]+' item '+str(j), item_id=menu_types[i]+str(j), support_subtype=[menu_types[i]]))
        await self.send_update_context_menu(elements, action.channel_id, [action.sender])

    async def on_context_menu_click(self, context_click: MenuClick):
        txt = 'Menu choice: '+context_click.item_id+' Message content: '+str(context_click.message_content)
        await self.send_message(txt, context_click.channel_id, context_click.sender, [context_click.sender])

    async def on_message_up(self, message):
        await self.send_message(message) # A trivial group chat so that messages can appear.
