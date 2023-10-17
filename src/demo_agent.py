# demo_agent.py

import asyncio
import json

from moobius.moobius_agent import MoobiusAgent

class DemoAgent(MoobiusAgent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        

    async def on_start(self):
        """
        Called after successful connection to websocket server.
        """
        self.db_helper.set_service_id(self.service_id)
        li = self.http_api.get_service_list()
        self.channel_ids = []
        

        for d in li:
            if d.get('service_id', None) == self.service_id:
                self.channel_ids = d.get('channel_ids', [])
                break

        print("channel_ids", self.channel_ids)
        
        for channel_id in self.channel_ids:
            await self.fetch_and_save_userlist(channel_id)


    # on_xxx, default implementation, to be override
    async def on_msg_up(self, message_data):
        """
        Handle the received message.
        """
        recipients = message_data.get("body").get("context").get("recipients")
        subtype = message_data.get("body").get("subtype")
        channel_id = message_data.get("body").get("channel_id")
        
        if subtype == "text":
            text_content =  message_data.get("body").get("content").get("text")
            await self.send_msg_down(channel_id, recipients, "text", text_content, message_data.get("body").get("context").get("sender"))
        else:
            pass

    async def on_action(self, message_data):
        """
        Handle the received action.
        """
        action_subtype = message_data.get("body").get("subtype")
        client_id = message_data.get("body").get("sender")
        channel_id = message_data.get("body").get("channel_id")

        if action_subtype == "fetch_userlist":
            user_list_pairs = self.db_helper.get_user_list_for_real_user(client_id)
            detailed_user_list = []
            detailed_user_list += [{
                "user_id": pair["virtual_id"],
                "context": self.db_helper.get_user_info(pair["real_id"])
            } for pair in user_list_pairs]
            
            await self.send_update_userlist(channel_id, detailed_user_list, [client_id])

        elif action_subtype == "fetch_features":
            # Test the function with the provided sample data
            feature_ids = self.db_helper.get_features_for_user(client_id)
            feature_data_list = []
            
            for feature_id in feature_ids:
                feature_data = json.loads(self.db_helper.get_feature_info(feature_id)['feature_data'])
                feature_data_list.append(feature_data)
            
            await self.send_update_features(channel_id, feature_data_list, [client_id])
        
        elif action_subtype == "fetch_playground":
            content = self.db_helper.get_playground_info(client_id)
            await self.send_update_playground(channel_id, content, [client_id])

        elif action_subtype == "join_channel":
            await asyncio.sleep(3)
            data = self.http_api.get_channel_userlist(channel_id, self.service_id)
            
            if data["code"] == 10000:
                userlist = data["data"]["userlist"]
             
                user_id_list = [user["user_id"] for user in userlist]
                print("userlist", userlist)
                print("user_id_list", user_id_list)
                self.maintain_user_list(userlist)
                origin_user_list = [{
                    "user_id": user_temp["user_id"],
                    "context": user_temp["user_context"]
                    }
                    for user_temp in userlist
                ]
                print("origin_user_list", origin_user_list)
                # update for all users, by default everyone can see everyone
                await self.send_update_userlist(channel_id, origin_user_list, user_id_list)
        
            elif action_subtype == "leave_channel":
                await asyncio.sleep(3)
                data = self.http_api.get_channel_userlist(channel_id, self.service_id)
                
                if data["code"] == 10000:
                    userlist = data["data"]["userlist"]
                    user_id_list = [user["user_id"] for user in userlist]
                    print("userlist", userlist)
                    print("user_id_list", user_id_list)
                    self.maintain_user_list(userlist)
                    self.db_helper.set_user_list_for_real_user(client_id, [])
                    
                    origin_user_list = [{
                        "user_id": user_temp["user_id"],
                        "context": user_temp["user_context"]
                        }
                        for user_temp in userlist
                    ]
                    
                    print("origin_user_list", origin_user_list)
                    
                    await self.send_update_userlist(channel_id, origin_user_list, user_id_list)
                else:
                    raise Exception("Failed to get channel user list")

        elif action_subtype == "fetch_channel_info":
            await self.send_update_channel_info(channel_id, self.db_helper.get_channel_info(channel_id))
        
        else:
            raise Exception("Unknown action subtype:", action_subtype)

    async def on_feature_call(self, message_data):
        """
        Handle the received feature call.
        """
        feature_id = message_data.get("body").get("feature_id")
        arguments = message_data.get("body").get("arguments")
        client_id = message_data.get("body").get("sender")
        
        # await features[feature_id](arguments, client_id)

    async def on_unknown_message(self, message_data):
        """
        Handle the received unknown message.
        """
        print("Received unknown message:", message_data)
