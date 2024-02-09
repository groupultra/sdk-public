# MISC functions TODO: Just move these to a better place, having a MISC category isn't clean code.
import json
import dataclasses


class EnhancedJSONEncoder(json.JSONEncoder):
    """Json Encoder but with automatic conversion of dataclasses to dict."""
    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        else:
            return super().default(o)

    def __str__(self):
        return f'moobius.EnhancedJSONEncoder()'
    def __repr__(self):
        return self.__str__()
