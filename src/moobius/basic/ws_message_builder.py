# ws_messages.py

import uuid
import json
import time

# This should be a basic builder. Do NOT put dependencies here.
class WSMessageBuilder:
    def __init__(self):
        pass

    def update_userlist(self, client_id, channel_id, user_list, recipients):
        """
        Constructs the update message for user list.
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
        return json.dumps(message)
    
    def update_features(self, client_id, channel_id, features, recipients):
        """
        Constructs the update message for features list.
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
        return json.dumps(message)

    
    def update_channel_info(self, client_id, channel_id, channel_data):
        """
        Constructs the update message for channel info.
        """
        message = {
            "type": "update",
            "subtype": "channel_info",
            "channel_id": channel_id,
            "request_id": str(uuid.uuid4()),
            "client_id": client_id,
            "body": channel_data
        }
        return json.dumps(message)

    
    def update_playground(self, client_id, channel_id, content, recipients):
        """
        Constructs the update message for features list.
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
        return json.dumps(message)

    
    def service_login(self, service_id, access_token):
        """
        Constructs the service_login message.
        """
        message = {
            "type": "service_login",
            "request_id": str(uuid.uuid4()),
            "auth_origin": "cognito",
            "access_token": access_token,
            "service_id": service_id
        }
        return json.dumps(message)

    
    def msg_down(self, client_id, channel_id, recipients, subtype, message_content, sender):
        """
        Constructs the msg_down message.
        """
        message = {
            "type": "msg_down",
            "request_id": str(uuid.uuid4()),
            "client_id": client_id,
            "body": {
                "subtype": subtype,
                "channel_id": channel_id,
                "content": {
                    ("text" if subtype == "text" else "path"): message_content #+ " (from service)"
                },
                "recipients": recipients,
                # "group_id": group_id,
                "sender": sender,
                "timestamp": int(time.time() * 1000),
                "context": {}
            }
        }
        print("msg_down", message)
        return json.dumps(message)

    
    def update(self, client_id, target_client_id, data):
        """
        Constructs the update message.
        """
        message = {
            "type": "update",
            "request_id": str(uuid.uuid4()),
            "client_id": client_id,
            "body": data
        }
        return json.dumps(message)

    
    def ping(self):
        """
        Constructs the ping message.
        """
        message = {
            "type": "ping",
            "request_id": str(uuid.uuid4())
        }
        return json.dumps(message)
