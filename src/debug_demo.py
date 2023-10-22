import json
import asyncio
from demo_service import DemoService
from moobius.moobius_wand import MoobiusWand
import aioprocessing
def main():
    # For newly bound channels. It doesn't hurt to bind multiple times.
    bind_to_channels = ['efae7992-0801-4079-bae2-83189b68d71d']
    
    with open("/home/ubuntu/sdk/src/config.json", "r") as f:
        config = json.load(f)
    
    with open("db_settings.json", "r") as f:
        db_settings = json.load(f)

    service = DemoService(db_settings=db_settings, **config)
    service.start(bind_to_channels=bind_to_channels)
    return service
    
if __name__ == "__main__":
    service = main()
    wand = MoobiusWand(service)
    wand.send_ping()
    # elif sent_by == player_id:
    #     continue  # no repeat
    # else:
    #     sender_id = self.bands[self.game_band_id].game_status[real_id]['view_characters'][sent_by]['user_id']

    # await self.send_msg_down(
    #     channel_id=self.game_band_id,
    #     recipients=[real_id],
    #     subtype="text",
    #     message_content=f'{content}',
    #     sender=sender_id
    
    # data = self.http_api.create_service_user(self.service_id, username, nickname, avatar, description)
    # character = from_dict(data_class=Character, data=data)
        
    # debug_sender_id = self._make_character(self.game_band_id, '0000', 'Cicada Host').user_id
    # service.wand.send_msg_down("efae7992-0801-4079-bae2-83189b68d71d", "Hello")
    # def send_msg_down(self, channel_id, recipients, subtype, message_content, sender):
    #     payload = self._ws_payload_builder.msg_down(self.service_id, channel_id, recipients, subtype, message_content, sender)
    #     self.wand.coro_send(payload)
    # service.wand.send_ping()