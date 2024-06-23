from moobius import Moobius

class ZeroService(Moobius):
    def __init__(self, log_file="logs/service.log", error_log_file="logs/error.log", **kwargs):
        super().__init__(log_file=log_file, error_log_file=error_log_file, **kwargs)
