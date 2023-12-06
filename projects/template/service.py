# service.py

from loguru import logger
from moobius import MoobiusService


class TemplateService(MoobiusService):
    def __init__(self, log_file="logs/service.log", **kwargs):
        super().__init__(**kwargs)
        logger.add(log_file, rotation="1 day", retention="7 days", level="DEBUG")
