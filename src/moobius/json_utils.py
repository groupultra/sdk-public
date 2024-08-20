# JSON-related utils for loading, etc.
import json, dataclasses
from typing import Optional

import dacite, pydoc


_DTYPE = '_moobius_type'; _DVAL = '_moobius_val' # Unique IDs to indicate the class name in JSON files.
def marked_recursive_dataclass(data):
    """
    Recursively converts nested lists, dicts, etc into dataclasses if they have been markd with types._DTYPE and types._DVAL
    Accepts the data. Returns the dataclassed data. Used for JSON loading.
    Used by json_utils.enhanced_json_load.
    """
    if type(data) is dict:
        if _DTYPE in data and _DVAL in data:
            if data[_DTYPE] == 'NoneType':
                return None
            class_name_fullpath = data[_DTYPE]
            data_type = pydoc.locate(class_name_fullpath)

            if data_type:
                if dataclasses.is_dataclass(data_type):
                    return dacite.from_dict(data_class=data_type, data=data[_DVAL])
                else: # Attempt a generic constructor.
                    return data_type(data[_DVAL])
            else:
                raise TypeError(f'Unknown type: {class_name_fullpath}')
        else:
            return dict(zip(data.keys(), [marked_recursive_dataclass(d) for d in data.values()]))
    elif type(data) in [tuple, list]:
        return [marked_recursive_dataclass(d) for d in data]
    elif type(data) is set:
        return set([marked_recursive_dataclass(d) for d in data])
    else:
        return data


def marked_recursive_undataclass(data, typemark_dataclasses):
    """
    Converts data containing dataclasses back into pure dicts, making them with json_utils._DTYPE and json_utils._DVAL.
    Accepts the dataclassed data and whether to mark dataclasses in a special way so they are known as such. Returns the non-dataclassed data.
    Used by json_utils.enhanced_json_save.
    """
    if dataclasses.is_dataclass(data):
        if typemark_dataclasses:
            dtype = type(data).__module__+'.'+type(data).__name__
            dval = dataclasses.asdict(data)
            return {_DTYPE:dtype, _DVAL: dval}
        else:
            return dataclasses.asdict(data)
    elif type(data) is dict:
            return dict(zip(data.keys(), [marked_recursive_undataclass(d, typemark_dataclasses) for d in data.values()]))
    elif type(data) in [list, tuple]:
        return [marked_recursive_undataclass(d, typemark_dataclasses) for d in data] # A little duplicated code copying _marked_recursive_dataclass_load.
    elif type(data) is set:
        return set([marked_recursive_undataclass(d, typemark_dataclasses) for d in data])
    else:
        return data



def enhanced_json_load(filename):
    """Loads JSON from the disk, given the filename or bytes. Returns the possibly-nested datastructure which may have Dataclasses."""
    if hasattr(filename, 'read'):
        data = filename.read()
    elif type(filename) is str:
        with open(filename, 'r', encoding='utf-8') as f:
            data = f.read()
    elif type(filename) is bytes:
        data = filename.decode('utf-8')
    data = json.loads(data)
    return marked_recursive_dataclass(data)


def enhanced_json_save(filename, data, typemark_dataclasses=True, indent=2):
    """
    Saves the JSON to the disk and/or a string.

    Parameters:
      filename: The filename or file object to save to. None if not saving to any file.
      data: What needs to be saved. Can be a nested datastructure even with embedded dataclasses.
      typemark_dataclasses=True: Save dataclasses as special dicts so that on enhanced_json_load load they are converted back into dataclasses.
      indent=2: The indent to display the text at.
    Returns the data as a JSON string.
    """
    data = marked_recursive_undataclass(data, typemark_dataclasses)
    txt = json.dumps(data, indent=indent)
    if filename:
        if hasattr(filename, 'write'):
            f = filename
            f.write(txt)
        else:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(txt)
    return txt


def recursive_json_load(x):
    """
    Loads json files into dicts and lists, including dicts/lists of json filenames. Used for the app configuration.
    Strings anywhere in x that have no newlines and end in .json or .JSON will be treated like filenames.
    Does not use enhanced_json features. Accepts a generic input x. Returns the modified input.
    """
    if type(x) is dict:
        return dict(zip(x.keys(), [recursive_json_load(v) for v in x.values()]))
    elif type(x) in [list, tuple]:
        return [recursive_json_load(xi) for xi in x]
    elif type(x) is str:
        if x.endswith('.json') or x.endswith('.JSON') and '\n' not in x:
            with open(x, 'r', encoding='utf-8') as f:
                return recursive_json_load(json.load(f))
        else:
            return x
    else:
        return x


def update_jsonfile(fname, key_path, value):
    """
    Updates a json file. Uses enhanced_json_load (which makes dataclasses have metadata).

    Parameters:
      fname: The json file.
      key_path: the path within the datastructure.
      value: The new value.

    Returns None.
    """
    x = enhanced_json_load(fname)
    y = x
    while len(key_path)>1:
        y = x[key_path[0]]; key_path = key_path[1:]
    y[key_path[0]] = value # This will modifiy x in-place.
    enhanced_json_save(fname, x)


def get_config(config: Optional[str|dict]=None, account_config: Optional[str|dict]=None, service_config: Optional[str|dict]=None, db_config: Optional[str|dict]=None, log_config: Optional[str|dict]=None):
    """
    Calculates the configuration in various ways. Config files are automatically generated by quickstart.py which is invoked by running the command "moobius".
    This may involve JSON file reading.

    Parameters:
       config: The entire config, a string (JSON filepath) or dict.
       account_config: The account-sepcific config with secrets, a string (JSON filepath) or dict.
       service_config: Service-specific config (the urls, the service id, and the channels).
       db_config: Config specific to the Moobius db engine. A list of attributes. This feature is an independent feature to the Platform.
       log_config: Config specific to logging. This feature is an independent feature to the Platform.

    Returns:
      The config as a dict.
      Where to save the new service id as [json filename, datastructure_path], if there is a JSON file to save to.
    """

    where_save_new_service_id = None
    if service_config and type(service_config) is str:
        where_save_new_service_id  = [service_config, ['service_id']] # Args to json_utils.update_jsonfile. Cannot be a function because it must pickle and be sent to another process.
    elif config and type(config) is str:
        with open(config, 'r', encoding='utf-8') as f:
            _cdata = json.load(f)
            _sconf = _cdata.get('service_config')
            if type(_sconf) is str:
                where_save_new_service_id = [_sconf, ['service_id']]
            elif type(_sconf) is dict:
                where_save_new_service_id = [config, ['service_config', 'service_id']]

    if not where_save_new_service_id and not service_config.get('no_warn_cannot_save_service_id'):
        print("WARNING: No way to save service_id because no JSON.") # Logger is not be set up yet.

    # Settings, settings, settings...
    if not config:
        config = {}
    config = recursive_json_load(config)
    for pair in [['account_config', account_config], ['service_config', service_config], ['db_config', db_config], ['log_config', log_config]]:
        config[pair[0]] = config.get(pair[0], pair[1]) # Smaller changes override the larger config.
    config = recursive_json_load(config)
    account_config = config.get('account_config',{})
    service_config = config.get('service_config',{})
    account_config ['email'] = account_config.get('email', None)
    account_config ['password'] = account_config.get('password', None)
    service_config['http_server_uri'] = service_config.get("http_server_uri", "https://api.moobius.ai/")
    service_config['ws_server_uri'] = service_config.get("ws_server_uri", "wss://ws.moobius.ai/")
    db_config = config.get('db_config',{})
    log_config = config.get('log_config',{})

    if not config['log_config']:
        log_config = {}
    config['log_config'] = log_config
    log_config['log_level'] = log_config.get("log_level", "INFO")
    log_config['log_retention'] = log_config.get('log_retention', {'rotation':"1 day", 'retention':"7 days"})
    log_config['log_file'] = log_config.get('log_file', None)
    log_config['error_log_file'] = log_config.get('error_log_file', log_config['log_file'])
    #if log_config.get('error_log'): # Alternate name.
    #    log_config['error_log_file'] = log_config['error_log']
    log_config['error_log_level'] = log_config.get('error_log_level', "WARNING")
    log_config['terminal_log_level'] = log_config.get('terminal_log_level', "INFO")
    if type(log_config['log_retention']) is str:
        log_config['log_retention'] = {'retention':log_config['log_retention']}
    log_config['log_level'] = log_config['log_level'].upper()
    log_config['error_log_level'] = log_config['error_log_level'].upper()

    return config, where_save_new_service_id
