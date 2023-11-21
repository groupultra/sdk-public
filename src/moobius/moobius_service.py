# moobius_service.py

from dataclasses import asdict
import time

from dacite import from_dict

from moobius.basic._types import MessageDown
from moobius.moobius_basic_service import MoobiusBasicService

# with database
class MoobiusService(MoobiusBasicService):
    def __init__(self, db_settings=(), **config):
        super().__init__(**config)

        self.bands = {}
        self.db_settings = db_settings

    def msg_up_to_msg_down(self, msg_up, remove_self=False):
        """
        Convert a MessageUp object to a MessageDown object.
        """
        msg_body = asdict(msg_up)
        msg_body['timestamp'] = int(time.time() * 1000)
        msg_body['sender'] = msg_body['context']['sender']
        msg_body.pop('msg_id', None)
        
        if remove_self and (msg_body['sender'] in msg_body['recipients']):
            msg_body['recipients'].remove(msg_body['sender'])
        else:
            pass

        msg_body['context'] = {}

        msg_down = from_dict(data_class=MessageDown, data=msg_body)
        
    
        return msg_down