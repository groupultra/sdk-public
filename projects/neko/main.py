import asyncio
import time

from service import NekoService
from agent import NekoAgent
from moobius import MoobiusWand

if __name__ == "__main__":
    wand = MoobiusWand()
    
    service_handle = wand.run(
        NekoService,
        log_file="logs/service.log",
        service_config_path="config/service.json",
        db_config_path="config/service_db.json",
        background=True
    )
    
    agent_handle = wand.run(
        NekoAgent,
        log_file="logs/agent.log",
        error_log_file="logs/error.log",
        agent_config_path="config/agent.json",
        db_config_path="config/agent_db.json",
        background=True)
    
    # service on_spell
    wand.spell(service_handle, "meow")
    wand.spell(service_handle, "nya")
    
    
    
    
    
    asyncio.run(asyncio.sleep(3))
    # agent on_spell
    wand.spell(agent_handle, "send_fetch_userlist")
    wand.spell(agent_handle, "send_fetch_features")
    
    wand.spell(agent_handle, "nya_all")
    
    asyncio.run(asyncio.sleep(3))
    
    wand.spell(agent_handle, "send_fetch_playground")
    
    wand.spell(agent_handle, "send_fetch_channel_info")
    wand.spell(agent_handle, "send_feature_call_key1")
    wand.spell(agent_handle, "send_feature_call_key2")
    
    asyncio.run(asyncio.sleep(3))
    wand.spell(agent_handle, "send_leave_channel")
    asyncio.run(asyncio.sleep(3))
    
    wand.spell(agent_handle, "send_join_channel")
   
    
    


