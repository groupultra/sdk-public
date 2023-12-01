import asyncio
from dataclasses import asdict
from dacite import from_dict
import uuid
import json
import time

from multiprocessing import Process

from moobius.basic._types import MessageUp, Action, FeatureCall, Copy, Payload, Character
from moobius.basic.logging_config import log_error, log_info
    
class MoobiusWand:
    def __init__(self, service):
        self.service = service
        
    def _service_job(self, bind_to_channels=None):
        try:
            asyncio.run(self.service.start(bind_to_channels))
        except KeyboardInterrupt:
            pass
        
    def start_background_service(self, bind_to_channels=None):
        p_service = Process(target=self._service_job, args=(bind_to_channels, ))
        p_service.start()
        time.sleep(10)
    
    def fetch_real_characters(self, channel_id):
        data = self.service.http_api.get_channel_userlist(channel_id, self.service.service_id)

        if data["code"] == 10000:
            userlist = data["data"]["userlist"]

            return [from_dict(data_class=Character, data=d) for d in userlist]
        else:
            log_error(f"fetch_real_characters error {data}")

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
        self.service.queue.put(payload_str)
    
    async def async_send(self, payload_type, payload_body):
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
        await self.service.queue.coro_put(payload_str)
        
    def on(self, payload_type, payload_body):
        if isinstance(payload_body, dict):
            payload_dict = {
                'type': payload_type,
                'body': payload_body
            }
        else:
            payload_obj = Payload(
                type=payload_type,
                body=payload_body
            )

            payload_dict = asdict(payload_obj)
        
        payload_str = self.service._ws_payload_builder.dumps(payload_dict)
        self.service.queue.put("RECV" + payload_str)
    
    async def async_on(self, payload_type, payload_body):
        if isinstance(payload_body, dict):
            payload_dict = {
                'type': payload_type,
                'body': payload_body
            }
        else:
            payload_obj = Payload(
                type=payload_type,
                body=payload_body
            )

            payload_dict = asdict(payload_obj)
        
        payload_str = self.service._ws_payload_builder.dumps(payload_dict)
        await self.service.queue.coro_put("RECV" + payload_str)