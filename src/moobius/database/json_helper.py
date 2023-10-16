# json_helper.py

import json
import os
from moobius.database.database_helper import DatabaseHelper

class JSONHelper(DatabaseHelper):
    def __init__(self, root_dir='jsons', **kwargs):
        super().__init__()
        os.makedirs(root_dir, exist_ok=True)
        self.main_path = os.path.join(root_dir, "main.json")
        self.feature_path = os.path.join(root_dir, "feature.json")
        self.user_path = os.path.join(root_dir, "user.json")
        self.singleton_user_path = os.path.join(root_dir, "singleton_user.json")
        self.user_list_path = os.path.join(root_dir, "user_list.json")
        self.feature_info_path = os.path.join(root_dir, "feature_info.json")
        self.features_for_user_path = os.path.join(root_dir, "features_for_user.json")
        self.playground_path = os.path.join(root_dir, "playground.json")
        self.channel_info_path = os.path.join(root_dir, "channel_info.json")
        self.if_user_in_channel_path = os.path.join(root_dir, "if_user_in_channel.json")
        
    def safe_open_json(self, path):
        """
        Opens a json file safely.
        """
        try:
            if os.path.exists(path):
                with open(path, "r") as f:
                    return json.load(f)
            else:
                with open(path, "w") as f:
                    json.dump({}, f)
                return {}
        except Exception as e:
            print(f"Error in safe_open_json(self, path): {e}")
    
    def safe_write_json(self, path, data):
        """
        Writes to a json file safely.
        """
        try:
            with open(path, "w") as f:
                json.dump(data, f)
        except Exception as e:
            print(f"Error in safe_write_json(self, path, data): {e}")
            
    def set_service_id(self, service_id):
        """
        Stores the service_id in main.json.
        """
        try:
            data = self.safe_open_json(self.main_path)
            data["service_id"] = service_id
            self.safe_write_json(self.main_path, data)
        except Exception as e:
            print(f"Error in set_service_id(self, service_id): {e}")
    
    def get_service_id(self):
        """
        Retrieves the service_id from main.json.
        """
        try:
            data = self.safe_open_json(self.main_path)
            return data["service_id"]
        except Exception as e:
            print(f"Error in get_service_id(self): {e}")
            
    def set_feature(self, feature_id, function_name):
        """
        Stores the association of feature_id with a function name in feature.json.
        """
        try:
            data = self.safe_open_json(self.feature_path)
            data[feature_id] = function_name
            self.safe_write_json(self.feature_path, data)
        except Exception as e:
            print(f"Error in set_feature(self, feature_id, function_name): {e}")

    def get_feature_function(self, feature_id):
        """
        Retrieves the function name associated with a feature_id from feature.json.
        """
        try:
            data = self.safe_open_json(self.feature_path)
            return data[feature_id]
        except Exception as e:
            print(f"Error in get_feature_function(self, feature_id): {e}")
    

    def set_user_info(self, real_id, avatar, nickname, description):
        """
        Stores full information for a user in user.json.
        """
        try:
            data = self.safe_open_json(self.user_path)
            data[real_id] = {
                "avatar": avatar,
                "nickname": nickname,
                "description": description
            }
            self.safe_write_json(self.user_path, data)
        except Exception as e:
            print(f"Error in set_user_info(self, real_id, avatar, nickname, description): {e}")

    def set_singleton_user_info(self, singleton_local_id, avatar, nickname, description, singleton_uuid=None):
        """
        Stores full information for a singleton user in singleton_user.json.
        """
        try:
            data = self.safe_open_json(self.singleton_user_path)
            data[singleton_local_id] = {
                "avatar": avatar,
                "nickname": nickname,
                "description": description,
                "singleton_uuid": singleton_uuid if singleton_uuid else ""
            }
            self.safe_write_json(self.singleton_user_path, data)
        except Exception as e:
            print(f"Error in set_singleton_user_info(self, singleton_local_id, avatar, nickname, description, singleton_uuid=None): {e}")

    def get_user_info(self, real_id):
        """
        Retrieves full information for a user from user.json.
        """
        try:
            data = self.safe_open_json(self.user_path)
            return data[real_id]
        except Exception as e:
            print(f"Error in get_user_info(self, real_id): {e}")

    def get_singleton_user_info(self, singleton_local_id):
        """
        Retrieves full information for a singleton user from singleton_user.json.
        """
        try:
            data = self.safe_open_json(self.singleton_user_path)
            return data[singleton_local_id]
        except Exception as e:
            print(f"Error in get_singleton_user_info(self, singleton_local_id): {e}")

    def get_singleton_uuid(self, singleton_local_id):
        """
        Retrieves the singleton_uuid for a given singleton user from singleton_user.json.
        """
        try:
            data = self.safe_open_json(self.singleton_user_path)
            return data[singleton_local_id]["singleton_uuid"]
        except Exception as e:
            print(f"Error in get_singleton_uuid(self, singleton_local_id): {e}")

    def set_user_list_for_real_user(self, real_user_id, user_list):
        """
        Stores the user list (real_id and virtual_id pairs) that a real user can see in user_list.json.
        """
        
        try:
            data = self.safe_open_json(self.user_list_path)
            data[real_user_id] = []
            for user in user_list:
                real_id = user['real_id']
                virtual_id = user['virtual_id']
                data[real_user_id].append(json.dumps({
                        "real_id": real_id,
                        "virtual_id": virtual_id
                    }))
            data[real_user_id] = json.dumps(data[real_user_id])
            self.safe_write_json(self.user_list_path, data)
        except Exception as e:
            print(f"Error in set_user_list_for_real_user(self, real_user_id, user_list): {e}")
        
    def get_user_list_for_real_user(self, real_user_id):
        """
        Retrieves the user list (real_id and virtual_id pairs) that a real user can see from user_list.json.
        """
        try:
            data = self.safe_open_json(self.user_list_path)
            print("data", data)
            serialized_pairs = json.loads(data[real_user_id])
            print("serialized_pairs", serialized_pairs)
            # serialized_pairs = json.loads(serialized_pairs)
            return [json.loads(pair) for pair in serialized_pairs]
        except Exception as e:
            print(f"Error in get_user_list_for_real_user(self, real_user_id): {e}")


    def set_feature_info(self, feature_id, feature_data):
        """
        Stores the information for a feature in feature_info.json.
        """
        try:
            data = self.safe_open_json(self.feature_info_path)
            if feature_id not in data:
                data[feature_id] = {}
            data[feature_id]["feature_data"] = feature_data
            self.safe_write_json(self.feature_info_path, data)
        except Exception as e:
            print(f"Error in set_feature_info(self, feature_id, feature_data): {e}")
        
    def get_feature_info(self, feature_id):
        """
        Retrieves the information for a feature from feature_info.json.
        """
        try:
            data = self.safe_open_json(self.feature_info_path)
            return data[feature_id]
        except Exception as e:
            print(f"Error in get_feature_info(self, feature_id): {e}")

    def set_features_for_user(self, real_user_id, feature_ids):
        """
        Stores the feature_ids that are available for a user in features_for_user.json.
        """
        try:
            data = self.safe_open_json(self.features_for_user_path)
            data[real_user_id] = feature_ids
            self.safe_write_json(self.features_for_user_path, data)
        except Exception as e:
            print(f"Error in set_features_for_user(self, real_user_id, feature_ids): {e}")

    def get_features_for_user(self, real_user_id):
        """
        Retrieves the feature_ids that are available for a user from features_for_user.json.
        """
        try:
            data = self.safe_open_json(self.features_for_user_path)
            return data[real_user_id]
        except Exception as e:
            print(f"Error in get_features_for_user(self, real_user_id): {e}")

    # Playground related methods
    def set_playground_info(self, real_user_id, path, text):
        """
        Stores the playground information for a user in playground.json.
        """
        try:
            data = self.safe_open_json(self.playground_path)
            data[real_user_id] = {
                "path": path,
                "text": text
            }
            print("set_playground_info data", data)
            self.safe_write_json(self.playground_path, data)
        except Exception as e:
            print(f"Error in set_playground_info(self, real_user_id, path, text): {e}")

    def get_playground_info(self, real_user_id):
        """
        Retrieves the playground information for a user from playground.json.
        """
        try:
            data = self.safe_open_json(self.playground_path)
            print("get_playground_info data", data)
            if real_user_id not in data:
                return {}
            return data[real_user_id]
        except Exception as e:
            print(f"Error in get_playground_info(self, real_user_id): {e}")
            
    # Channel related methods
    def set_channel_info(self, real_user_id, channel_description, channel_avatar):
        """
        Stores the channel information for a user in channel_info.json.
        """
        try:
            data = self.safe_open_json(self.channel_info_path)
            data[real_user_id] = {
                "channel_description": channel_description,
                "channel_avatar": channel_avatar
            }
            self.safe_write_json(self.channel_info_path, data)
        except Exception as e:
            print(f"Error in set_channel_info(self, real_user_id, channel_description, channel_avatar): {e}")

    def get_channel_info(self, real_user_id):
        """
        Retrieves the channel information for a user from channel_info.json.
        """
        try:
            data = self.safe_open_json(self.channel_info_path)
            return data[real_user_id]
        except Exception as e:
            print(f"Error in get_channel_info(self, real_user_id): {e}")
    
    def set_if_user_in_channel(self, real_user_id, in_channel = True):
        """
        Stores the playground information for a user in if_user_in_channel.json.
        """
        try:
            data = self.safe_open_json(self.if_user_in_channel_path)
            data[real_user_id] = {
                "in_channel": str(in_channel)
            }
            self.safe_write_json(self.if_user_in_channel_path, data)
        except Exception as e:
            print(f"Error in set_if_user_in_channel(self, real_user_id, in_channel = True): {e}")
            
            

    def get_if_user_in_channel(self, real_user_id):
        """
        Retrieves the playground information for a user from if_user_in_channel.json.
        """
        try:
            data = self.safe_open_json(self.if_user_in_channel_path)
            return data[real_user_id]
        except Exception as e:
            print(f"Error in get_if_user_in_channel(self, real_user_id): {e}")
