# moobius_service.py

import json
import time

from dataclasses import asdict
from dacite import from_dict

from moobius.basic._types import MessageDown
from moobius.moobius_basic_service import MoobiusBasicService

# with database
class MoobiusService(MoobiusBasicService):
    def __init__(self, service_config_path="", db_config_path=""):
        super().__init__(config_path=service_config_path)

        with open(db_config_path, "r") as f:
            self.db_config = json.load(f)

        self.bands = {}

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