# agent.py

import json
import time

from dataclasses import asdict
from dacite import from_dict

from .basic_agent import MoobiusBasicAgent


# with database
class MoobiusAgent(MoobiusBasicAgent):
    def __init__(self, agent_config_path="", db_config_path="", **kwargs):
        super().__init__(config_path=agent_config_path)

        with open(db_config_path, "r") as f:
            self.db_config = json.load(f)

        self.bands = {}
        
    async def create_message(self, channel_id, content, recipients, subtype='text'):
        await self.send_msg_up(
            channel_id=channel_id,
            recipients=recipients,
            subtype=subtype,
            message_content=content
        )
