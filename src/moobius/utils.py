# MISC functions TODO: Just move these to a better place, having a MISC category isn't clean code.
import json, uuid
import dataclasses
from moobius.types import Group
from loguru import logger
import re
import sys


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


def summarize_html(html_str):
    """Converts HTML to an easier-for-a-human format by cutting out some of the more common tags. Far from perfect."""
    rs = [r'<div>\d+<\/div *>', r'<div class *= *"[a-zA-Z0-9]*">', r'<span class *= *"[a-zA-Z0-9]*">']
    for tag in ['div', 'li', 'head', 'body', 'pre', 'span']:
        rs.append(f'<{tag} *>')
        rs.append(f'</{tag} *>')
    for r in rs:
        html_str = re.sub(r, "", html_str)
    html_str = html_str.replace('\r\n','\n').replace('\t','  ')
    while '  ' in html_str or '\n\n' in html_str or '\n ' in html_str:
        html_str = html_str.replace('\n\n\n\n\n\n\n\n\n','\n').replace('\n\n','\n').replace('         ',' ').replace('  ',' ').replace('\n ','\n')
    return html_str.strip()
