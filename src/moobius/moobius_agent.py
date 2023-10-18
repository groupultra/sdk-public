from dacite import from_dict

from moobius.basic.types import Character
from moobius.moobius_basic_agent import MoobiusBasicAgent

# with database
class MoobiusAgent(MoobiusBasicAgent):
    def __init__(self, db_settings=(), **config):
        super().__init__(**config)

        self.bands = {}
        self.db_settings = db_settings

    # =================== Helper functions for http + ws + db usage ===================


    def demo_make_feature(self, feature_id, feature_name, button_text, new_window, feature_args=None):
        sample_args = [
            {
                "name": "arg1",
                "type": "enum",
                "values": ["choose me", "do not choose me"],
                "placeholder": "placeholder",
            }
        ]

        test_feature_1 = self.db_helper.create_feature("feature_id", "some list", "click", True, sample_args)
        
        return feature_id


    # fetch real users and set features to db
    async def fetch_real_characters(self, channel_id):
        """
        Initialize data after successful service_login.
        Fetches data using HTTP request and populates database.
        """
        
        data = self.http_api.get_channel_userlist(channel_id, self.service_id)

        if data["code"] == 10000:
            userlist = data["data"]["userlist"]

            return [from_dict(data_class=Character, data=d) for d in userlist]
        else:
            print("fetch_real_characters error", data)
            
            return []

    async def fetch_and_send_playground(self, channel_id, recipients):
        """
        Fetch playground data from database and send it via an update message.
        """
        playground_data = self.db_helper.get_playground()
        await self.send_update_playground(channel_id, playground_data, recipients)

    def try_create_singleton_service_user(self, service_id, singleton_local_id, username, nickname, avatar, description):
        singleton_user_info = self.db_helper.get_singleton_user_info(singleton_local_id)
        print("service_id, username, nickname, avatar, description", service_id, username, nickname, avatar, description)
            
        if not singleton_user_info or (not 'singleton_uuid' in singleton_user_info) or (not singleton_user_info['singleton_uuid']):
            singleton_uuid = self.http_api.create_service_user(service_id, username, nickname, avatar, description)['user_id']
            self.db_helper.set_singleton_user_info(singleton_local_id, avatar, nickname, description, singleton_uuid)
            self.db_helper.set_user_info(singleton_uuid, avatar, nickname, description)
            return True, singleton_uuid
        else:
            return False, singleton_user_info['singleton_uuid']