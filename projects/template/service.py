# service.py

from moobius.moobius_service import MoobiusService

class TemplateService(MoobiusService):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)