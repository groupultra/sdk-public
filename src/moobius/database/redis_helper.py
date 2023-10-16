# redis_helper.py
import redis
import json
from moobius.database.database_helper import DatabaseHelper

class RedisHelper(DatabaseHelper):
    _instance = None
    
    def __new__(cls, password="", **kwargs):
        if cls._instance is None:
            cls._instance = super(RedisHelper, cls).__new__(cls)
            cls._instance.connection = redis.StrictRedis(password=password, decode_responses=True)
        return cls._instance

    def set_feature(self, feature_id, function_name):
        """
        Stores the association of feature_id with a function name in Redis.
        """
        self.connection.set(f"feature:{feature_id}", function_name)

    def get_feature_function(self, feature_id):
        """
        Retrieves the function name associated with a feature_id from Redis.
        """
        return self.connection.get(f"feature:{feature_id}").decode("utf-8")

    def set_user_info(self, real_id, avatar, nickname, description):
        """
        Stores full information for a user.
        """
        self.connection.hmset(f"user:{real_id}", {
            "avatar": avatar,
            "nickname": nickname,
            "description": description
        })
    
    def set_singleton_user_info(self, singleton_local_id, avatar, nickname, description, singleton_uuid=None):
        """
        Stores full information for a singleton user.
        """
        self.connection.hmset(f"singleton_user:{singleton_local_id}", {
            "avatar": avatar,
            "nickname": nickname,
            "description": description,
            "singleton_uuid": singleton_uuid if singleton_uuid else ""
        })
    
    def get_user_info(self, real_id):
        """
        Retrieves full information for a user.
        """
        return self.connection.hgetall(f"user:{real_id}")

    def get_singleton_user_info(self, singleton_local_id):
        """
        Retrieves full information for a singleton user.
        """
        return self.connection.hgetall(f"singleton_user:{singleton_local_id}")

    def get_singleton_uuid(self, singleton_local_id):
        """
        Retrieves the singleton_uuid for a given singleton user.
        """
        return self.connection.hget(f"singleton_user:{singleton_local_id}", "singleton_uuid")

    def set_user_list_for_real_user(self, real_user_id, user_list):
        """
        Stores the user list (real_id and virtual_id pairs) that a real user can see.
        """
        for user in user_list:
            real_id = user['real_id']
            virtual_id = user['virtual_id']
            # Store real_id and virtual_id pairs as a serialized JSON string
            self.connection.sadd(f"userlist:{real_user_id}", json.dumps({"real_id": real_id, "virtual_id": virtual_id}))

    def get_user_list_for_real_user(self, real_user_id):
        """
        Retrieves the user list (real_id and virtual_id pairs) that a real user can see.
        """
        serialized_pairs = self.connection.smembers(f"userlist:{real_user_id}")
        return [json.loads(pair) for pair in serialized_pairs]

    def set_feature_info(self, feature_id, feature_data):
        """
        Stores the information for a feature.
        """
        self.connection.hmset(f"feature:{feature_id}", {"feature_data": feature_data})
        
    def get_feature_info(self, feature_id):
        """
        Retrieves the information for a feature.
        """
        return self.connection.hgetall(f"feature:{feature_id}")

    def set_features_for_user(self, real_user_id, feature_ids):
        """
        Stores the feature_ids that are available for a user.
        """
        self.connection.sadd(f"features_for_user:{real_user_id}", *feature_ids)

    def get_features_for_user(self, real_user_id):
        """
        Retrieves the feature_ids that are available for a user.
        """
        return self.connection.smembers(f"features_for_user:{real_user_id}")

    # Playground related methods
    def set_playground_info(self, real_user_id, path, text):
        """
        Stores the playground information for a user.
        """
        self.connection.hmset(f"playground:{real_user_id}", {
            "path": path,
            "text": text
        })

    def get_playground_info(self, real_user_id):
        """
        Retrieves the playground information for a user.
        """
        return self.connection.hgetall(f"playground:{real_user_id}")

    # Channel related methods
    def set_channel_info(self, real_user_id, channel_description, channel_avatar):
        """
        Stores the channel information for a user.
        """
        self.connection.hmset(f"channel_info:{real_user_id}", {
            "channel_description": channel_description,
            "channel_avatar": channel_avatar
        })

    def get_channel_info(self, real_user_id):
        """
        Retrieves the channel information for a user.
        """
        return self.connection.hgetall(f"channel_info:{real_user_id}")
    
    def set_if_user_in_channel(self, real_user_id, in_channel = True):
        """
        Stores the playground information for a user.
        """
        try:
            self.connection.hmset(f"if_user_in_channel:{real_user_id}", {
                "in_channel": str(in_channel)
            })
        except redis.RedisError as e:
            print(f"Error in set_if_user_in_channel(self, function with Redis operation: {e}")

    def get_if_user_in_channel(self, real_user_id):
        """
        Retrieves the playground information for a user.
        """
        try:
            return self.connection.hgetall(f"if_user_in_channel:{real_user_id}")
        except redis.RedisError as e:
            print(f"Error in get_if_user_in_channel(self, function with Redis operation: {e}")
