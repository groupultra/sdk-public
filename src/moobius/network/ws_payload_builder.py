# ws_messages.py

import uuid
import json
import time

from moobius.utils import EnhancedJSONEncoder


# Do NOT put dependencies here.
# todo: Use dataclass!
class WSPayloadBuilder:
    '''
    WSPayloadBuilder is a helper class that constructs websocket messages.
    It helps use to construct websocket messages in a more readable way.
    Basically, it is a wrapper of json.dumps() with some default values.
    
    Update:
        - update_userlist(client_id, channel_id, user_list, recipients)
        - update_features(client_id, channel_id, features, recipients)
        - update_style(client_id, channel_id, style_content, recipients)
        - update_channel_info(client_id, channel_id, channel_data)
        - update_playground(client_id, channel_id, content, recipients)
        - update(client_id, target_client_id, data)
        
    Login:
        - service_login(service_id, access_token)
        
    Msg:
        - msg_down(client_id, channel_id, recipients, subtype, message_content, sender)
    
    Util:
        - ping()
    '''
    def __init__(self):
        '''
        Initialize a WSPayloadBuilder object. Since this class is a wrapper of json.dumps(), there is no need to initialize it.
        
        Parameters:
            None
        
        Returns:
            None
            
        Example:
            >>> ws_payload_builder = WSPayloadBuilder()
        '''
        pass

    @staticmethod
    def dumps(data):
        return json.dumps(data, cls=EnhancedJSONEncoder)

    # ==================== Update ====================
    
    def update_userlist(self, client_id, channel_id, user_list, recipients):
        """
        Constructs the update message for user list.
        
        Parameters:
            client_id: str
                The client id. This is actually the service id.
            channel_id: str
                The channel id.
            user_list: list
                The user list to be updated.
            recipients: list
                The recipients to see the update.
        
        Returns:
            str
                The dumped message for user list update, in json format.
        
        Example:
            Note: This is a hidden function, you don't need to call it directly. Usually you could use send_update_userlist() instead which helps you to add the client_id.
            >>> ws_payload_builder = WSPayloadBuilder()
            >>> ws_payload_builder.update_userlist("client_id", "channel_id", ["user1", "user2"], ["user1", "user2"])
        """
        message = {
            "type": "update",
            "request_id": str(uuid.uuid4()),
            "client_id": client_id,
            "body": {
                "subtype": "update_userlist",
                "channel_id": channel_id,
                "recipients": recipients,
                # "recipients": [],
                "userlist": user_list,
                # "group_id": group_id,
                "context": {}
            }
        }
        # Print the message (for debugging purposes)
        return self.dumps(message)

    def update_features(self, client_id, channel_id, features, recipients):
        """
        Constructs the update message for features list.
        
        Parameters:
            client_id: str
                The client id. This is actually the service id.
            channel_id: str
                The channel id.
            features: list
                The features list to be updated.
            recipients: list
                The recipients to see the update.
        
        Returns:
            str
                The dumped message for features list update, in json format.
        
        Example:
            Note: This is a hidden function, you don't need to call it directly. Usually you could use send_update_features() instead which helps you to add the client_id.
            >>> self.continue_feature = {
            >>>         "feature_id": "play",
            >>>         "feature_name": "Continue Playing",
            >>>         "button_text": "Continue Playing",
            >>>         "new_window": False,
            >>>         "arguments": [
            >>>         ]
            >>>     }
            >>> features = [
            >>>     self.continue_feature
            >>> ]
            >>> ws_payload_builder = WSPayloadBuilder()
            >>> ws_payload_builder.update_features("client_id", "channel_id", features, ["user1", "user2"])
        """
        message = {
            "type": "update",
            "request_id": str(uuid.uuid4()),
            "client_id": client_id,
            "body": {
                "subtype": "update_features",
                "channel_id": channel_id,
                "recipients": recipients,
                "features": features,
                "group_id": "temp",
                "context": {}
            }
        }
        # Print the message (for debugging purposes)
        return self.dumps(message)

    def update_style(self, client_id, channel_id, style_content, recipients):
        """
        Constructs the update message for style update.
        
        Parameters:
            client_id: str
                The client id. This is actually the service id.
            channel_id: str
                The channel id.
            style_content: list
                The style content to be updated, check the example below.
            recipients: list
                The recipients to see the update.
        
        Returns:
            str
                The dumped message for style update, in json format.
        
        Example:
            Note: This is a hidden function, you don't need to call it directly. Usually you could use send_update_style() instead which helps you to add the client_id.
            >>> content = [
            >>> {
            >>>     "widget": "channel",
            >>>     "display": "invisible",
            >>> },
            >>> {
            >>>     "widget": "feature",
            >>>     "display": "highlight",
            >>>     "feature_hook": {
            >>>         "feature_id": "feature_id",
            >>>         "button_text": "done",
            >>>         "arguments": []
            >>>     },
            >>>     "text": "<h1>Start from here.</h1><p>This is a Feature, what the most channles has</p>"
            >>> }
            >>> ]
            >>> ws_payload_builder = WSPayloadBuilder()
            >>> ws_payload_builder.update_style("client_id", "channel_id", content, ["user1", "user2"])
        """
        message = {
            "type": "update",
            "request_id": str(uuid.uuid4()),
            "client_id": client_id,
            "body": {
                "subtype": "update_style",
                "channel_id": channel_id,
                "recipients": recipients,
                "content": style_content,
                "group_id": "temp",
                "context": {}
            }
        }
        # Print the message (for debugging purposes)
        return self.dumps(message)

    def update_channel_info(self, client_id, channel_id, channel_data):
        """
        Constructs the update message for channel info.
        
        Parameters:
            client_id: str
                The client id. This is actually the service id.
            channel_id: str
                The channel id.
            channel_data: dict
                The channel data to be updated.
        
        Returns:
            str
                The dumped message for channel info update, in json format.
        
        Example:
            Note: This is a hidden function, you don't need to call it directly. Usually you could use send_update_channel_info() instead which helps you to add the client_id.
            >>> ws_payload_builder = WSPayloadBuilder()
            >>> ws_payload_builder.update_channel_info("client_id", "channel_id", {"name": "new_channel_name"})
        """
        message = {
            "type": "update",
            "subtype": "channel_info",
            "channel_id": channel_id,
            "request_id": str(uuid.uuid4()),
            "client_id": client_id,
            "body": channel_data
        }
        return self.dumps(message)

    def update_playground(self, client_id, channel_id, content, recipients):
        """
        Constructs the update message for features list.
        
        Parameters:
            client_id: str
                The client id. This is actually the service id.
            channel_id: str
                The channel id.
            content: dict
                The playground content, consists of a image path and a text.
            recipients: list
                The recipients to see the update.
        
        Returns:
            str
                The dumped message for playground update, in json format.
        
        Example:
            Note: This is a hidden function, you don't need to call it directly. Usually you could use send_update_playground() instead which helps you to add the client_id.
            >>> content = {
            >>>     "path": "4003740a-d480-43da-9a5d-77202de5c4a3",
            >>>     "text": ""
            >>> }
            >>> ws_payload_builder = WSPayloadBuilder()
            >>> ws_payload_builder.update_playground("client_id", "channel_id", content, ["user1", "user2"])
        """
        message = {
            "type": "update",
            "request_id": str(uuid.uuid4()),
            "client_id": client_id,
            "body": {
                "subtype": "update_playground",
                "channel_id": channel_id,
                "recipients": recipients,
                "content": content,
                "group_id": "temp",
                "context": {}
            }
        }
        # Print the message (for debugging purposes)
        return self.dumps(message)
    
    def update(self, client_id, target_client_id, data):
        """
        Constructs the update message.
        
        Parameters:
            client_id: str
                The client id. This is actually the service id.
            target_client_id: str
                The target client id.
            data: dict
                The data to be updated, can be any data.
                
        Returns:
            str
                The dumped message for update, in json format.
        
        Example:
            Note: This is a hidden function, you don't need to call it directly. Usually you could use send_update() instead which helps you to add the client_id.
            >>> ws_payload_builder = WSPayloadBuilder()
            >>> ws_payload_builder.update("client_id", "target_client_id", {"data": "data"})
        """
        message = {
            "type": "update",
            "request_id": str(uuid.uuid4()),
            "client_id": client_id,
            "body": data
        }
        return self.dumps(message)

    # ==================== Login ====================
    
    def service_login(self, service_id, access_token):
        """
        Constructs the service_login message. Need to be sent before any other messages.
        
        Parameters:
            service_id: str
                The service id.
            access_token: str
                The access token.
        
        Returns:
            str
                The dumped message for service_login, in json format.
                
        Example:
            Note: This is a hidden function, you don't need to call it directly. Usually you could use send_service_login() instead which helps you to add the client_id.
            >>> ws_payload_builder = WSPayloadBuilder()
            >>> ws_payload_builder.service_login("service_id", "access_token")
        """
        message = {
            "type": "service_login",
            "request_id": str(uuid.uuid4()),
            "auth_origin": "cognito",
            "access_token": access_token,
            "service_id": service_id
        }
        return self.dumps(message)

    # ==================== Message ====================

    def msg_up(self, client_id, channel_id, recipients, subtype, message_content, str_dump=True):
        """
        Constructs the msg_up message. The same parameters as self.msg_down, except that no sender is needed.
        """
        message = {
            "type": "msg_up",
            "request_id": str(uuid.uuid4()),
            "client_id": client_id,
            "body": {
                "subtype": subtype,
                "channel_id": channel_id,
                "content": {
                    ("text" if subtype == "text" else "path"): message_content  # + " (from service)"
                },
                "recipients": recipients,
                # "group_id": group_id,
                "timestamp": int(time.time() * 1000),
                "context": {}
            }
        }
    
        return self.dumps(message) if str_dump else message

    def msg_down(self, client_id, channel_id, recipients, subtype, message_content, sender, str_dump=True):
        """
        Constructs the msg_down message.
        Currently, only text message is supported, so the subtype is always "text".
        
        Parameters:
            client_id: str
                The client id. This is actually the service id.
            channel_id: str
                The channel id.
            recipients: list
                The recipients to see the message.
            subtype: str
                The subtype of the message.
            message_content: str
                The message content.
            sender: str
                The sender of the message.
            str_dump=True: bool
                Turn off in order to get a dict instead. Usually this is kept on.
                
        Returns:
            str
                The dumped message for msg_down, in json format.
                
        Example:
            Note: This is a hidden function, you don't need to call it directly. Usually you could use send_msg_down() instead which helps you to add the client_id.
            >>> ws_payload_builder = WSPayloadBuilder()
            >>> ws_payload_builder.msg_down("client_id", "channel_id", ["user1", "user2"], "text", "message_content", "sender")
        """
        message = self.msg_up(client_id, channel_id, recipients, subtype, message_content, str_dump=False)
        message['type'] = "msg_down"
        message['body']['sender'] = sender

        return self.dumps(message) if str_dump else message

    # ==================== Utilization ====================
    
    def ping(self):
        """
        Constructs the ping message.
        
        Parameters:
            None
        
        Returns:
            str
                The dumped message for ping, in json format.
                
        Example:
            Note: This is a hidden function, you don't need to call it directly. Usually you could use send_ping() instead which helps you to add the client_id.
            >>> ws_payload_builder = WSPayloadBuilder()
            >>> ws_payload_builder.ping()
        """
        message = {
            "type": "ping",
            "request_id": str(uuid.uuid4())
        }
        return self.dumps(message)
    

    # ==================== Agent ====================
    def agent_login(self, access_token):
        """
        Constructs the agent_login message.
        """
        message = {
            "type": "user_login",
            "request_id": str(uuid.uuid4()),
            "auth_origin": "cognito" or "oauth2",
            "access_token": access_token
        }
        return self.dumps(message)

    def fetch_userlist(self, client_id, channel_id):
        """
        Constructs the fetch_user_list message.
        """
        message = {
            "type": "action",
            "request_id": str(uuid.uuid4()),
            "client_id": client_id,
            "body": {
                "subtype": "fetch_userlist",
                "channel_id": channel_id,
                "context": {}
            }
        }
        return self.dumps(message)

    def fetch_features(self, client_id, channel_id):
        """
        Constructs the fetch_features message.
        """
        message = {
            "type": "action",
            "request_id": str(uuid.uuid4()),
            "client_id": client_id,
            "body": {
                "subtype": "fetch_features",
                "channel_id": channel_id,
                "context": {}
            }
        }
        return self.dumps(message)
    
    def fetch_style(self, client_id, channel_id):
        """
        Constructs the fetch_style message.
        """
        message = {
            "type": "action",
            "request_id": str(uuid.uuid4()),
            "client_id": client_id,
            "body": {
                "subtype": "fetch_style",
                "channel_id": channel_id,
                "context": {}
            }
        }
        return self.dumps(message)

    def fetch_playground(self, client_id, channel_id):
        """
        Constructs the fetch_playground message.
        """
        message = {
            "type": "action",
            "request_id": str(uuid.uuid4()),
            "client_id": client_id,
            "body": {
                "subtype": "fetch_playground",
                "channel_id": channel_id,
                "context": {}
            }
        }
        return self.dumps(message)
    
    def fetch_channel_info(self, client_id, channel_id):
        """
        Constructs the fetch_channel_info message.
        """
        message = {
            "type": "action",
            "request_id": str(uuid.uuid4()),
            "client_id": client_id,
            "body": {
                "subtype": "fetch_channel_info",
                "channel_id": channel_id,
                "context": {}
            }
        }
        return self.dumps(message)
    
    def leave_channel(self, client_id, channel_id):
        message = {
            "type": "action",
            "request_id": str(uuid.uuid4()),
            "client_id": client_id,
            "body": {
                "subtype": "leave_channel",
                "channel_id": channel_id,
                "context": {}
            }
        }
        return self.dumps(message)
    
    def join_channel(self, client_id, channel_id):
        message = {
            "type": "action",
            "request_id": str(uuid.uuid4()),
            "client_id": client_id,
            "body": {
                "subtype": "join_channel",
                "channel_id": channel_id,
                "context": {}
            }
        }
        return self.dumps(message)