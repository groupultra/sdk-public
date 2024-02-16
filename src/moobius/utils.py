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


###################### Temporary state where the .app uses an older format ########################
# This is temporary code.

_subsk = [['features', 'buttons'], ['update_features', 'update_buttons'], ['feature_id', 'button_id'],
          ['fetch_features', 'fetch_buttons'], ['feature_name', 'button_name'], # Note: button_text does NOT become feature text.
          ['msg_id', 'message_id']] # Substitute key with other key.
_subskv = [['type', 'feature_call', 'button_click'], ['widget', 'playground', 'canvas'],
           ['subtype', 'update_features', 'update_buttons'], ['subtype', 'update_playground', 'update_canvas'], ['subtype', 'fetch_playground', 'fetch_canvas'], ['subtype', 'fetch_features', 'fetch_buttons'],
           ['type', 'msg_up', 'message_up'], ['type', 'msg_down', 'message_down'], ['type', 'ping', 'heartbeat'],
           ['origin_type', 'msg_up', 'message_up'], ['origin_type', 'msg_down', 'message_down'], ['origin_type', 'ping', 'heartbeat']] # Substitude key bearing value with other value.
_subsurl = [['/service/user/create', '/service/character/create'], ['/service/user/update', '/service/character/update'],
            ['channel/userlist', 'channel/character_list'], ['/user/fetch_profile', '/character/fetch_profile']]
           # Note: do NOT '/service/user/list' '/service/character/list' because the .app is actually using the newer version here.
def bespoke_legacy2modern(d):
    """Yes all nicknames become names!"""
    if type(d) is dict:
        if 'nickname' in d:
            d['name'] = d['nickname']
            del d['nickname']
    return d
def bespoke_modern2legacy(d):
    """But not all names become nicknames!"""
    if type(d) is dict:
        if 'name' in d and 'avatar' in d and 'description' in d:
            d['nickname'] = d['name']
            del d['name']
    return d
def add_user_id(d, user_id):
    """This should no longer be needed in the modern version; this function marks legacy code."""
    if user_id:
        d['user_id'] = user_id
    return d


def pair_subs(pairs, is_forward, x, partial_match=False):
    ab = [0,1] if is_forward else [1,0]
    for p in pairs:
        if partial_match and x is not None:
            x = x.replace(p[ab[0]], p[ab[1]])
        elif x==p[ab[0]]:
                x = p[ab[1]]
    return x


def triplet_dsubs(triplets, is_forward, d):
    ab = [1,2] if is_forward else [2,1]
    if type(d) is dict:
        for tr in triplets:
            k = tr[0]; v0 = tr[ab[0]]; v1 = tr[ab[1]]
            if k in d and d[k]==v0:
                d[k] = v1
    return d


def _dsubs_walk(d, fk, fv):
    """Recursive walk updating dict keys"""
    d = fv(d)
    if type(d) is list or type(d) is tuple:
        return [_dsubs_walk(di, fk, fv) for di in d]
    if type(d) is dict:
        d_out = {}
        for k in list(d.keys()):
            v = _dsubs_walk(d[k], fk, fv)
            k1 = fk(k)
            if not k1:
                k1 = k
            d_out[k1] = fv(v)
        return d_out
    return d


def dictlegacy2modern(d, url=None):
    """The .app uses "features", the .link will call it "buttons" and this can be ignored."""
    url = pair_subs(_subsurl, True, url, partial_match=True)
    if d is None:
        return d, url
    if type(d) is not dict:
        raise Exception('Not a dict')
    def fv(v):
        v = triplet_dsubs(_subskv, True, v)
        v = bespoke_legacy2modern(v)
        return v
    out = _dsubs_walk(d, lambda k: pair_subs(_subsk, True, k), fv)
    return out, url
def dictmodern2legacy(d, url=None): # TODO: duplicate code with last fn.
    """Going back the opposite direction as dictlegacy2modern. Note that the conversion to/from buttons is handled as soon/late as possible."""
    url = pair_subs(_subsurl, False, url, partial_match=True)
    if d is None:
        return d, url
    if type(d) is not dict:
        raise Exception('Not a dict')
    def fv(v):
        v = triplet_dsubs(_subskv, False, v)
        v = bespoke_modern2legacy(v)
        return v
    out = _dsubs_walk(d, lambda k: pair_subs(_subsk, False, k), fv)
    return out, url
