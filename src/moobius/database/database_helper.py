# database_helper.py

import json

class DatabaseHelper:
    def __init__(self, **kwargs):
        pass

    def maintain_user_list(self, userlist, singleton_local_ids=[]):
        singleton_uuid_list = []
        for singleton_local_id in singleton_local_ids:
            singleton_uuid = self.get_singleton_uuid(singleton_local_id)
            singleton_uuid_list.append({"real_id": singleton_uuid, "virtual_id": singleton_uuid})
        
        for user in userlist:
            user_context = user["user_context"]
            user_id = user["user_id"]
            self.set_user_info(user_id, user_context["avatar"], user_context["nickname"], user_context["description"])
            # For this example, virtual_id is set as user_id. This can be modified as per requirements.
            # decide to add your singleton_uuid here or not
            self.set_user_list_for_real_user(
                user_id, [{"real_id": user_temp["user_id"], "virtual_id": user_temp["user_id"]} for user_temp in userlist] + singleton_uuid_list
            )
    
    def create_feature(self, feature_id, feature_name, button_text, new_window, arguments):
        """
        Constructs the feature data based on the provided parameters.
        """
        feature_data = {
            "feature_id": feature_id,
            "feature_name": feature_name,
            "button_text": button_text,
            "new_window": new_window,
            "arguments": arguments
        }

        self.set_feature_info(feature_id, json.dumps(feature_data))
        return feature_data


    # =================== Below are interfaces for database operations ===================

    def set_service_id(self, service_id):
        """
        Stores the service_id in main.json.
        """
        raise NotImplementedError
    
    def get_service_id(self):
        """
        Retrieves the service_id from main.json.
        """
        raise NotImplementedError
            
    def set_feature(self, feature_id, function_name):
        """
        Stores the association of feature_id with a function name in feature.json.
        """
        raise NotImplementedError

    def get_feature_function(self, feature_id):
        """
        Retrieves the function name associated with a feature_id from feature.json.
        """
        raise NotImplementedError

    def set_user_info(self, real_id, avatar, nickname, description):
        """
        Stores full information for a user in user.json.
        """
        raise NotImplementedError

    def set_singleton_user_info(self, singleton_local_id, avatar, nickname, description, singleton_uuid=None):
        """
        Stores full information for a singleton user in singleton_user.json.
        """
        raise NotImplementedError

    def get_user_info(self, real_id):
        """
        Retrieves full information for a user from user.json.
        """
        raise NotImplementedError

    def get_singleton_user_info(self, singleton_local_id):
        """
        Retrieves full information for a singleton user from singleton_user.json.
        """
        raise NotImplementedError

    def get_singleton_uuid(self, singleton_local_id):
        """
        Retrieves the singleton_uuid for a given singleton user from singleton_user.json.
        """
        raise NotImplementedError

    def set_user_list_for_real_user(self, real_user_id, user_list):
        """
        Stores the user list (real_id and virtual_id pairs) that a real user can see in user_list.json.
        """
        raise NotImplementedError
 
    def get_user_list_for_real_user(self, real_user_id):
        """
        Retrieves the user list (real_id and virtual_id pairs) that a real user can see from user_list.json.
        """
        raise NotImplementedError

    def set_feature_info(self, feature_id, feature_data):
        """
        Stores the information for a feature in feature_info.json.
        """
        raise NotImplementedError

    def get_feature_info(self, feature_id):
        """
        Retrieves the information for a feature from feature_info.json.
        """
        raise NotImplementedError

    def set_features_for_user(self, real_user_id, feature_ids):
        """
        Stores the feature_ids that are available for a user in features_for_user.json.
        """
        raise NotImplementedError

    def get_features_for_user(self, real_user_id):
        """
        Retrieves the feature_ids that are available for a user from features_for_user.json.
        """
        raise NotImplementedError

    # Playground related methods
    def set_playground_info(self, real_user_id, path, text):
        """
        Stores the playground information for a user in playground.json.
        """
        raise NotImplementedError

    def get_playground_info(self, real_user_id):
        """
        Retrieves the playground information for a user from playground.json.
        """
        raise NotImplementedError

    # Channel related methods
    def set_channel_info(self, real_user_id, channel_description, channel_avatar):
        """
        Stores the channel information for a user in channel_info.json.
        """
        raise NotImplementedError

    def get_channel_info(self, real_user_id):
        """
        Retrieves the channel information for a user from channel_info.json.
        """
        raise NotImplementedError

    def set_if_user_in_channel(self, real_user_id, in_channel = True):
        """
        Stores the playground information for a user in if_user_in_channel.json.
        """
        raise NotImplementedError 

    def get_if_user_in_channel(self, real_user_id):
        """
        Retrieves the playground information for a user from if_user_in_channel.json.
        """
        raise NotImplementedError