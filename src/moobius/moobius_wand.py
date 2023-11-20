import asyncio
from dataclasses import asdict
from dacite import from_dict
from moobius.basic._types import MessageUp, Action, FeatureCall, Copy, Payload, Character
from moobius.basic._logging_config import logger
class MoobiusWand:
    def __init__(self, service, loop, wand):
        self.service = service
        self.loop = loop
        self.wand = wand
        
    # =================== on_xxx, to be override ===================
    def on(self, payload):
        # self.wand.coro_send("RECV" + payload)
        self.loop.call_soon_threadsafe(self.wand.put_nowait, "RECV" + payload)
    
    
    def fetch_real_characters(self, channel_id):
        data = self.service.http_api.get_channel_userlist(channel_id, self.service.service_id)

        if data["code"] == 10000:
            userlist = data["data"]["userlist"]

            return [from_dict(data_class=Character, data=d) for d in userlist]
        else:
            logger.error(f"fetch_real_characters error {data}")

            return []
    
    # =================== send_xxx, to be used ===================
    def send(self, payload_type, payload_body):
        if isinstance(payload_body, dict):
            payload_dict = {
                'type': payload_type,
                'request_id': str(uuid.uuid4()),
                'client_id': self.service.service_id,
                'body': payload_body
            }
        else:
            payload_obj = Payload(
                type=payload_type,
                request_id=str(uuid.uuid4()),
                client_id=self.service.service_id,
                body=payload_body
            )

            payload_dict = asdict(payload_obj)

        payload_str = self.service._ws_payload_builder.dumps(payload_dict)
        self.loop.call_soon_threadsafe(self.wand.put_nowait, payload_str)

    def send_service_login(self):
        payload = self.service._ws_payload_builder.service_login(self.service.service_id, self.service.access_token)
        logger.info(f"payload {payload}")
        self.loop.call_soon_threadsafe(self.wand.put_nowait, payload)

    def send_msg_down(self, channel_id, recipients, subtype, message_content, sender):
        payload = self.service._ws_payload_builder.msg_down(self.service.service_id, channel_id, recipients, subtype, message_content, sender)
        logger.info(f"msg_down payload {payload}")
        self.loop.call_soon_threadsafe(self.wand.put_nowait, payload)

    def send_update(self, target_client_id, data):
        payload = self.service._ws_payload_builder.update(self.service.service_id, target_client_id, data)
        logger.info(payload)
        self.loop.call_soon_threadsafe(self.wand.put_nowait, payload)

    def send_update_userlist(self, channel_id, user_list, recipients):
        payload = self.service._ws_payload_builder.update_userlist(self.service.service_id, channel_id, user_list, recipients)
        logger.info(f"send_update_userlist {payload}")
        self.loop.call_soon_threadsafe(self.wand.put_nowait, payload)

    def send_update_channel_info(self, channel_id, channel_data):
        payload = self.service._ws_payload_builder.update_channel_info(self.service.service_id, channel_id, channel_data)
        logger.info(payload)
        self.loop.call_soon_threadsafe(self.wand.put_nowait, payload)

    def send_update_playground(self, channel_id, content, recipients):
        payload = self.service._ws_payload_builder.update_playground(self.service.service_id, channel_id, content, recipients)
        logger.info(payload)
        self.loop.call_soon_threadsafe(self.wand.put_nowait, payload)

    def send_update_features(self, channel_id, feature_data, recipients):
        payload = self.service._ws_payload_builder.update_features(self.service.service_id, channel_id, feature_data, recipients)
        logger.info(payload)
        self.loop.call_soon_threadsafe(self.wand.put_nowait, payload)

    def send_ping(self):
        logger.info("Sending ping...")
        payload = self.service._ws_payload_builder.ping()
        self.loop.call_soon_threadsafe(self.wand.put_nowait, payload)