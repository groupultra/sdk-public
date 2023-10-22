import asyncio

from moobius.basic.types import MessageUp, Action, FeatureCall, Copy, Payload, Character

class MoobiusWand:
    def __init__(self, service, wand):
        self.service = service
        self.wand = wand
        self.loop = asyncio.get_event_loop()
        
    # =================== on_xxx, to be override ===================
    def on(self, payload):
        self.wand.coro_send("RECV" + payload)
    
    
    def fetch_real_characters(self, channel_id):
        return self.loop.run_until_complete(self.service.fetch_real_characters(channel_id))
    
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
        self.wand.coro_send(payload_str)

    def send_service_login(self):
        payload = self.service._ws_payload_builder.service_login(self.service.service_id, self.service.access_token)
        print("payload", payload)
        self.wand.coro_send(payload)

    def send_msg_down(self, channel_id, recipients, subtype, message_content, sender):
        payload = self.service._ws_payload_builder.msg_down(self.service.service_id, channel_id, recipients, subtype, message_content, sender)
        print("msg_down payload", payload)
        self.wand.coro_send(payload)

    def send_update(self, target_client_id, data):
        payload = self.service._ws_payload_builder.update(self.service.service_id, target_client_id, data)
        print(payload)
        self.wand.coro_send(payload)

    def send_update_userlist(self, channel_id, user_list, recipients):
        payload = self.service._ws_payload_builder.update_userlist(self.service.service_id, channel_id, user_list, recipients)
        print("send_update_userlist", payload)
        self.wand.coro_send(payload)

    def send_update_channel_info(self, channel_id, channel_data):
        payload = self.service._ws_payload_builder.update_channel_info(self.service.service_id, channel_id, channel_data)
        print(payload)
        self.wand.coro_send(payload)

    def send_update_playground(self, channel_id, content, recipients):
        payload = self.service._ws_payload_builder.update_playground(self.service.service_id, channel_id, content, recipients)
        print(payload)
        self.wand.coro_send(payload)

    def send_update_features(self, channel_id, feature_data, recipients):
        payload = self.service._ws_payload_builder.update_features(self.service.service_id, channel_id, feature_data, recipients)
        print(payload)
        self.wand.coro_send(payload)

    def send_ping(self):
        print("Sending ping...")
        payload = self.service._ws_payload_builder.ping()
        self.wand.coro_send(payload)
        
    # name _handle_received_payload
    # name fetch_real_characters
    # name handle_received_payload
    # name on_action
    # name on_copy
    # name on_feature_call
    # name on_msg_up
    # name on_start
    # name on_unknown_message
    # name on_unknown_payload
    # name send
    # name send_heartbeat
    # name send_msg_down
    # name send_ping
    # name send_service_login
    # name send_update
    # name send_update_channel_info
    # name send_update_features
    # name send_update_playground
    # name send_update_userlist

    # [('__class__', <class 'demo_service.DemoService'>), 
    #  ('__delattr__', <method-wrapper '__delattr__' of DemoService object at 0x7feee8b904c0>), 
    #  ('__dict__', {'http_api': <moobius.basic.http_api_wrapper.HTTPAPIWrapper object at 0x7feee8b90520>, 'horcrux': <aioprocessing.connection.AioConnection object at 0x7feee7d0ba90>, 'wand': <moobius.basic.ws_client.WSClient object at 0x7feee7d0baf0>, '_ws_payload_builder': <moobius.basic.ws_payload_builder.WSPayloadBuilder object at 0x7feee7d0bb20>}), ('__dir__', <built-in method __dir__ of DemoService object at 0x7feee8b904c0>), ('__doc__', None), ('__eq__', <method-wrapper '__eq__' of DemoService object at 0x7feee8b904c0>), ('__format__', <built-in method __format__ of DemoService object at 0x7feee8b904c0>), ('__ge__', <method-wrapper '__ge__' of DemoService object at 0x7feee8b904c0>), ('__getattribute__', <method-wrapper '__getattribute__' of DemoService object at 0x7feee8b904c0>), ('__gt__', <method-wrapper '__gt__' of DemoService object at 0x7feee8b904c0>), ('__hash__', <method-wrapper '__hash__' of DemoService object at 0x7feee8b904c0>), ('__init__', <bound method DemoService.__init__ of <demo_service.DemoService object at 0x7feee8b904c0>>), ('__init_subclass__', <built-in method __init_subclass__ of type object at 0x562d6ef3acc0>), ('__le__', <method-wrapper '__le__' of DemoService object at 0x7feee8b904c0>), ('__lt__', <method-wrapper '__lt__' of DemoService object at 0x7feee8b904c0>), ('__module__', 'demo_service'), ('__ne__', <method-wrapper '__ne__' of DemoService object at 0x7feee8b904c0>), ('__new__', <built-in method __new__ of type object at 0x562d6d352800>), ('__reduce__', <built-in method __reduce__ of DemoService object at 0x7feee8b904c0>), 
    #  ('__reduce_ex__', <built-in method __reduce_ex__ of DemoService object at 0x7feee8b904c0>), ('__repr__', <method-wrapper '__repr__' of DemoService object at 0x7feee8b904c0>), ('__setattr__', <method-wrapper '__setattr__' of DemoService object at 0x7feee8b904c0>), ('__sizeof__', <built-in method __sizeof__ of DemoService object at 0x7feee8b904c0>), ('__str__', <method-wrapper '__str__' of DemoService object at 0x7feee8b904c0>), ('__subclasshook__', <built-in method __subclasshook__ of type object at 0x562d6ef3acc0>), ('__weakref__', None), ('_handle_received_payload', <bound method MoobiusBasicService._handle_received_payload of <demo_service.DemoService object at 0x7feee8b904c0>>), 
    #  ('wand', <moobius.basic.ws_client.WSClient object at 0x7feee7d0baf0>), ('_ws_payload_builder', <moobius.basic.ws_payload_builder.WSPayloadBuilder object at 0x7feee7d0bb20>), ('fetch_real_characters', <bound method MoobiusBasicService.fetch_real_characters of <demo_service.DemoService object at 0x7feee8b904c0>>), ('handle_received_payload', <bound method MoobiusBasicService.handle_received_payload of <demo_service.DemoService object at 0x7feee8b904c0>>), ('horcrux', <aioprocessing.connection.AioConnection object at 0x7feee7d0ba90>), ('http_api', <moobius.basic.http_api_wrapper.HTTPAPIWrapper object at 0x7feee8b90520>), 
    #  ('main', <bound method MoobiusBasicService.main of <demo_service.DemoService object at 0x7feee8b904c0>>), 
    #  ('msg_up_to_msg_down', <bound method MoobiusService.msg_up_to_msg_down of <demo_service.DemoService object at 0x7feee8b904c0>>), ('on_action', <bound method DemoService.on_action of <demo_service.DemoService object at 0x7feee8b904c0>>), ('on_copy', <bound method MoobiusBasicService.on_copy of <demo_service.DemoService object at 0x7feee8b904c0>>), ('on_feature_call', <bound method DemoService.on_feature_call of <demo_service.DemoService object at 0x7feee8b904c0>>), ('on_msg_up', <bound method DemoService.on_msg_up of <demo_service.DemoService object at 0x7feee8b904c0>>), ('on_start', <bound method DemoService.on_start of <demo_service.DemoService object at 0x7feee8b904c0>>), ('on_unknown_message', <bound method DemoService.on_unknown_message of <demo_service.DemoService object at 0x7feee8b904c0>>), ('on_unknown_payload', <bound method MoobiusBasicService.on_unknown_payload of <demo_service.DemoService object at 0x7feee8b904c0>>), ('send', <bound method MoobiusBasicService.send of <demo_service.DemoService object at 0x7feee8b904c0>>), ('send_heartbeat', <bound method MoobiusBasicService.send_heartbeat of <demo_service.DemoService object at 0x7feee8b904c0>>), ('send_msg_down', <bound method MoobiusBasicService.send_msg_down of <demo_service.DemoService object at 0x7feee8b904c0>>), ('send_ping', <bound method MoobiusBasicService.send_ping of <demo_service.DemoService object at 0x7feee8b904c0>>), ('send_service_login', <bound method MoobiusBasicService.send_service_login of <demo_service.DemoService object at 0x7feee8b904c0>>), ('send_update', <bound method MoobiusBasicService.send_update of <demo_service.DemoService object at 0x7feee8b904c0>>), ('send_update_channel_info', <bound method MoobiusBasicService.send_update_channel_info of <demo_service.DemoService object at 0x7feee8b904c0>>), ('send_update_features', <bound method MoobiusBasicService.send_update_features of <demo_service.DemoService object at 0x7feee8b904c0>>), ('send_update_playground', <bound method MoobiusBasicService.send_update_playground of <demo_service.DemoService object at 0x7feee8b904c0>>), ('send_update_userlist', <bound method MoobiusBasicService.send_update_userlist of <demo_service.DemoService object at 0x7feee8b904c0>>), ('start', <bound method MoobiusBasicService.start of <demo_service.DemoService object at 0x7feee8b904c0>>)]
                        
            