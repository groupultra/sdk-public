# **This tool is ONLY FOR DEBUGGING, it is not useful in production **
#An alternative logging system to loguru that runs at a much higher level of detail.
#  It is most useful when hunting down exceptions that get "hidden" by async code.
#Run as __main__ to and choose between three functions:
#   "d" = Modify source files to use of dtrack instead of logger.
#      Does not change ANY files unless ALL of them can be reverted perfectly.
#   "l" = Revert to loguru.
#      Don't forget to revert before the "git add"!
#   "rm" = Remove ALL logs in ALL projects (they can get quite big).
#     press "y" to confirm deleting all these logs.

import os, sys, inspect, threading, datetime, functools, time, requests, difflib, re, shutil
enclosing_folder = os.path.dirname(os.path.realpath(__file__)).replace('\\','/')
use_loguru = False # For saving files. But it wasn't working for some reason?
debug_block_savecycle = False # Set to True in debug modes to maintain access to the code.
debug_on_fcall = None # f(Fcall object) can be set by debuggers. 
if use_loguru:
    from loguru import logger
else:
    logger = None # No need to even have loguru installed if using this library


def check_if_logio_i_fied():
    """Returns weather @dtrack.logios are enabled by checking the wand.py file."""
    with open(enclosing_folder+'/wand.py','r', encoding='utf-8') as f_obj:
        txt = f_obj.read()
    return '@dtrack.logio' in txt


def errorfree_str(x):
    """Returns an attempted repr(x), catching and str()-ing errors thrown by i.e. custom __repr__ methods."""
    try:
        return repr(x)
    except Exception as e:
        return str(type(x))+'(exception in objects __str__ method: '+str(e)+')'


def _convert_http_response(response): # TODO: support both requests and aiohttp.
    """Returns the response-as-str or an error code."""
    if type(response) is not requests.models.Response:
        return response # Not sure if this will ever happen, but just in case.
    status_code = response.status_code
    if status_code<400:
        return f'requests.Response({response.text})'
    else:
        return f'requests.Response(ERROR {status_code})'

############# Classes ###############

class Fcall:
    """Function call class that holds information about a single function call."""
    def __init__(self, is_async, sym_qual, argnames, args, kwargs, f_output):
        self.pid = os.getpid()
        self.thread_id = threading.get_ident()
        self.calling_time = datetime.datetime.now()
        self.is_async = is_async
        self.sym_qual = sym_qual
        self.argnames = argnames
        self.args = args # A deepcopy() may be useful sometimes because args mutate. But it would be overkill to use all the time.
        self.kwargs = kwargs
        self.f_output = f_output

    def get_report(self):
        """Returns a pretty-printed string representation."""
        #Based on https://www.geeksforgeeks.org/python-get-function-signature/
        async_ness = 'async ' if self.is_async else ''
        txt = 'FUNCTIONCALL: '+async_ness+self.sym_qual+ "("
        txt +=', '.join(entry[0]+' = '+errorfree_str(entry[1]) for entry in zip(self.argnames, self.args[:len(self.argnames)]))+ ", " # Args.
        txt += "args = ["+ ', '.join(errorfree_str(x) for x in self.args[len(self.argnames):])+ "], " # Printing the variable length Arguments  
        txt +="kwargs = {"
        kv_pairs = []
        for k, v in self.kwargs.items():
            kv_pairs.append(str(k)+': '+errorfree_str(v))
        txt += ', '.join(kv_pairs)+'} '
        txt += "output = " + errorfree_str(self.f_output)+')\n'
        return txt

    def __str__(self):
        return self.get_report()
    def __repr__(self):
        return self.get_report()


class LogStore:
    """Thread-safe log storage. Note: (I think) each process spawned gets it's own LogStore"""
    def __init__(self):
        self.fcalls = {} # Dict from qualified symbol to function call.
        self.fcall_list = [] # Chronological.
        self.GET_calls = []
        self.POST_calls = []
        self.errors = []
        self.other_logs = [] # When the logger adds something.
        self.print_fcalls = False
        self.print_errors = True
        self.print_api = False
        self.print_others = False
        self.disk_files = [] # Where all the logs go. List of [file, high_level_alert_only]
        self.lock = threading.Lock()
        self.disk_save_thread = threading.Thread(target=self.file_save_loop, daemon=True)
        self.disk_save_thread.start()

    def add_fcall(self, is_async, sym_qual, argnames, args, kwargs, f_output):
        """
        Adds a single function call to the storage. Thread-safe like all operations

        Parameters:
          is_async (bool): If the function is async.
          sym_qual (str): The name of the function and any enclosing modules.
            Example: "module_name.Class_name.method_name"
          argnames (list): The name of each argument.
          kwargs (dict): The kv-pair passed to the function.
            Example: (a=1, b=2) => {'a':1, 'b':2}
          f_output: The functions output.

        Returns None
        """
        fcall = Fcall(is_async, sym_qual, argnames, args, kwargs, f_output)
        with self.lock:
            self.fcalls[sym_qual] = self.fcalls.get(sym_qual, [])
            self.fcalls[sym_qual].append(fcall)
            self.fcall_list.append(fcall)
            if self.print_fcalls:
                try:
                    report = fcall.get_report()
                    print(report); sys.stdout.flush() # Flush may improve multiprocess reporting.
                except Exception as e:
                    [print('DTRACK.PY ERROR PLEASE BUGFIX THIS:'+str(e)) for _ in range(256)]
                    #raise e
            if isinstance(f_output, Exception): # The try-catch encloding the function returns an Exception if it raises one.
                self.errors.append(f_output)
                if self.print_errors:
                    print('Dtrack exception:', f_output, 'For function:', sym_qual) # TODO: use loguru.error? Or another way to report?
                    sys.stdout.flush()
        if debug_on_fcall is not None and debug_on_fcall is not False:
            try:
                debug_on_fcall(fcall)
            except Exception as e:
                print(f'WARNING: debug_on_fcall is set and raises an error, {e}')

    def filter_txt(self, log_txt):
        """Removes a specific "spam-test" in Moobius demo."""
        for k in [65536, 8192, 1024, 128, 16]:
            log_txt = log_txt.replace('BOMB'*k,f'BOMB*{k}') # Stress test of large packet sizes.
        return log_txt

    def clear_logs(self): # This is also called by the file_save_loop if there is a log_file specified.
        """Empties the entire storage."""
        with self.lock:
            self.fcalls = {}; self.fcall_list = []
            self.GET_calls = []; self.POST_calls = []; self.errors = []; self.other_logs = []

    def add_log_entry(self, x):
        """Adds and (optionally) prints a log that is not related to a specific function call. Much like loguru.info()"""
        with self.lock:
            self.other_logs.append(x)
        if self.print_others:
            print(errorfree_str(x)); sys.stdout.flush()

    def add_error(self, x):
        """Adds a special high-alert log message. Does not throw an exception. Much like loguru.error()"""
        with self.lock:
            self.errors.append(x)
        if self.print_errors:
            print('ERROR:', errorfree_str(x)); sys.stdout.flush()

    def file_save_loop(self):
        """Save logs to disk, clearning them from this file."""
        def _get_log_txt(self, highlev_only):
            append_lines = []
            try:
                if not highlev_only:
                    for k in self.fcalls.keys():
                        for fcall in self.fcalls[k]:
                            append_lines.append(self.filter_txt(fcall.get_report()))
                pairs = [['APIGET:', self.GET_calls], ['APIPOST:', self.POST_calls], ['ERROR:', self.errors], ['LOG:', self.other_logs]]
                if highlev_only:
                    pairs = [['ERROR:', self.errors]]
                for p in pairs:
                    for lg in p[1]:
                        append_lines.append(self.filter_txt(p[0]+errorfree_str(lg)))
            except Exception as e:
                print('WARNING: Error creating log. Likely bug in dtrack.py')
                append_lines.append('ERROR CREATING LOG likely bug in dtrack.py:'+str(e))
            return '\n'.join(append_lines)+'\n'
        while True:
            if len(self.disk_files)>0 and not debug_block_savecycle:
                with self.lock:
                    if use_loguru:
                        logger.info(_get_log_txt(self, False))
                    else:
                        for disk_file_lev in self.disk_files:
                            disk_file = disk_file_lev[0]; is_high_lev = disk_file_lev[1]
                            write_this = _get_log_txt(self, is_high_lev)
                            for j in range(64): # Make multible attempts, self.lock is thread-safe but not process-safe.
                                try:
                                    with open(disk_file, 'a' if os.path.exists(disk_file) else 'w', encoding='utf-8') as f_obj:
                                        f_obj.write(write_this)
                                except Exception as e:
                                    time.sleep(0.25)
                                    if j==63:
                                        print(f'WARNING: Cannot safe to log file {disk_file} despite repeated attempts to: {e}. Logs will be lost.')
                                    continue
                                break
                    self.clear_logs()
            time.sleep(4)

    def add_GET_call(self, url, response, **kwargs):
        """Stores a get call given a url, response, and the .get()'s **kwargs. Optionally prints it."""
        response = _convert_http_response(response)
        self.GET_calls.append({**kwargs, **{'url':url, 'response':response}})
        if self.print_api:
            print('APIGET:',self.GET_calls[-1])
    def add_POST_call(self, url, response, **kwargs):
        """Same as add_GET_call but for POST."""
        response = _convert_http_response(response)
        self.POST_calls.append({**kwargs, **{'url':url, 'response':response}})
        if self.print_api:
            print('APIPOST:',self.POST_calls[-1])

    def __str__(self):
        return f'LogStore({len(self.fcalls)} unique functions, {len(self.GET_calls)} GET calls, {len(self.POST_calls)} POST calls, {len(self.errors)} errors, {len(self.other_logs)} other logs)'
    def __repr__(self):
        return self.__str__()

############### Core logging API ################

def add_logfile(disk_file, *args, **kwargs):
    """Adds a log file given a disk_file string and "level" kwarg. Pass in disk_file=None to instead clear all disk_files."""
    if disk_file:
        high_alert_only = False
        lev = str(kwargs.get('level','info')).lower().strip()
        if lev=='warning' or lev=='error':
            high_alert_only = True
        disk_file = os.path.realpath(disk_file).replace('\\','/')
        if use_loguru:
            logger.add(disk_file, retention="2 hours", enqueue=True) # enqueue for process-safety.
        main_logstore.disk_files.append([disk_file, high_alert_only])
        print('logfile added:', disk_file+(' (high alert only)' if high_alert_only else ''))
    else:
        main_logstore.disk_files = []
        print('All logfiles disabled')


def _log_core(func, args, kwargs, out, is_async):
    """
    Logs a function given its inputs and outputs, returning the function output.

    Parameters:
      func (callable): The function object.
      args (list): Positional arguments to said function.
      kwargs (dict): key-value args to said function.
      out: The output of the function.
      is_async (bool): If the function is a coroutine.
        coroutines are logged twice, with a <Begin await> output and then the actual output.

    Returns: the "out" param it is given (this isn't generally used).
    """
    fname = '(unknown fn name)'
    argnames = ['(unknown argname)']*len(args)
    mname = '(unknown module name)'
    if hasattr(func, '__qualname__'): # A blanket logging system may once in a while encounter some strange object that doesn't have all attributes. Thus these guardrails.
        fname = func.__qualname__
    elif hasattr(func, '__name__'):
        fname = func.__name__
    if hasattr(func, '__code__'):
        argnames = func.__code__.co_varnames[:func.__code__.co_argcount]
    if hasattr(func, '__module__'):
        mname = func.__module__
    sym_qual = mname+'.'+fname

    main_logstore.add_fcall(is_async, sym_qual, argnames, args, kwargs, out)
    return out


def logio(func):
    """Log i/o decorator that takes in a function and returns a function which behaves the same except that it logs it's inputs and outputs."""
    if inspect.iscoroutinefunction(func):
        async def logio_wrapped_function(*args, **kwargs):
            _log_core(func, args, kwargs, '<Begin await>', True)
            out = await func(*args, **kwargs)
            _log_core(func, args, kwargs, out, True)
            return out
    else:
        def logio_wrapped_function(*args, **kwargs):
            try:
                out = func(*args, **kwargs)
            except Exception as e:
                out = e
                _log_core(func, args, kwargs, out, False)
                raise e
            return out
    functools.update_wrapper(logio_wrapped_function, func) # Prevents pickling problems with multiprocessing.
    return logio_wrapped_function


def log_info_color(*args):
    # TODO: colors!
    if len(args)==1:
        args = args[0]
    main_logstore.add_log_entry(args)
def log_debug(*args):
    """Drop-in replacement for loguru.debug()"""
    log_info(*(['(debug)']+list(args)))
def log_info(*args):
    """Drop-in replacement for loguru.info()"""
    if len(args)==1:
        args = args[0]
    main_logstore.add_log_entry(args)
def log_warning(*args):
    """Drop-in replacement for loguru.warning()"""
    log_info(*(['WARNING']+list(args)))
def log_error(*args):
    """Drop-in replacement for loguru.error()"""
    txt = ', '.join([errorfree_str(a) for a in args])
    main_logstore.add_error(txt)


def log_get_call(url, response, **kwargs):
    """Logs a get call given a url, reponse, and any kwargs passed to .get() to the main_logstore singleton object."""
    main_logstore.add_GET_call(url, response, **kwargs)
def log_post_call(url, response, **kwargs):
    """log_get_call but POST instead of GET."""
    main_logstore.add_POST_call(url, response, **kwargs)


def recent_calls(n=8):
    """Returns up to n recent Fcall objects in chronolgical order. But for this process only."""
    with main_logstore.lock:
        clist = main_logstore.fcall_list
        if len(clist)<=n:
            return clist
        return clist[-n:]

############# Enable/disable per-function logging mode ###############

def _decorator_update(txt,f):
    """Applies f(decorator lines, def_line) => decorator lines to each def. Returns the modified txt."""
    def _is_def_line(the_line):
        return the_line.strip().replace('async def ','def ').startswith('def ') and ':' in the_line
    def _is_class_line(the_line):
        return the_line.strip().replace('async class ','class ').startswith('class ') and ':' in the_line # aync classes are a favorite in Python 4.0.
    def _is_decorator_line(the_line):
        return the_line.strip().replace('#','').startswith('@') # Include commentet-out decorators.
    def _is_emptyish_line(the_line):
        return (l+'#').strip()[0]=='#'
    lines = txt.split('\n')
    lines1 = []
    local_dec_lines = []
    for l in lines:
        if _is_decorator_line(l) or _is_class_line(l) or _is_def_line(l):
            n_indent = len(l)-len(l.lstrip())

        if _is_decorator_line(l) or (_is_emptyish_line(l) and len(local_dec_lines)>0):
            local_dec_lines.append(l if len(l.strip()) == 0 else l.lstrip())
        elif _is_def_line(l) or _is_class_line(l):
            dec_lines1 = f(local_dec_lines, l.strip()) if _is_def_line(l) else local_dec_lines # Don't process class lines.

            for j in range(len(dec_lines1)):
                if len(dec_lines1[j].strip()) > 0:
                    dec_lines1[j] = ' '*n_indent+dec_lines1[j].lstrip()
            lines1.extend(dec_lines1); local_dec_lines = []
            lines1.append(l)
        else:
            lines1.extend(local_dec_lines); local_dec_lines = []
            lines1.append(l)
    lines1.extend(local_dec_lines); local_dec_lines = []
    return '\n'.join(lines1)


def set_to_dtrack_or_loguru(txt, is_to_dtrack):
    """Sets the source code *txt* to use dtrack's logger system instead of loguru OR the reverse of this, if *is_to_dtrack*=False.
       Modify main_logstore.print_fcalls, etc to change what is printed to console."""
    import_txt = 'import moobius.core.dtrack as dtrack\n'
    import_txt1 = 'from loguru import logger'
    if import_txt not in txt and is_to_dtrack:
        txt = import_txt+txt
    if not is_to_dtrack:
        txt = txt.replace(import_txt,'')
    txt = txt.replace('#'+import_txt1, import_txt1)
    if is_to_dtrack:
        txt = txt.replace(import_txt1, '#'+import_txt1)
    fname_ignores = ['__str__','__repr__']
    comment_these = ['@logger.catch']
    uncomment_these = []
    add_these = ['@dtrack.logio']
    remove_these = []
    no_change_if = ['@property', '@staticmethod']
    log_call_remap = [['logger.add(', 'dtrack.add_logfile('], ['logger.debug(', 'dtrack.log_debug('], ['logger.info(', 'dtrack.log_info('],
                      ['logger.warning(', 'dtrack.log_warning('], ['logger.error(', 'dtrack.log_error('],
                      ['logger.opt(colors=True).info(', 'dtrack.log_info_color(']]

    if not is_to_dtrack:
        comment_these, uncomment_these = uncomment_these, comment_these
        add_these, remove_these = remove_these, add_these
        log_call_remap = [[remp[1], remp[0]] for remp in log_call_remap]

    def _decf(decorators, def_line):
        for ignore_this in fname_ignores:
            if ignore_this in def_line:
                return decorators
        for d in decorators:
            for nc in no_change_if:
                if nc in d:
                    return decorators
        decorators1 = []
        for d in decorators:
            if any([x in d for x in add_these+remove_these]):
                continue
            du = d[1:] if len(d)>0 and d[0]=='#' else d
            for c in comment_these:
                if c in d:
                    d = '#'+du
            for u in uncomment_these:
                if u in d:
                    d = du
            decorators1.append(d)
        for a in add_these:
            decorators1.append(a)
        return decorators1

    txt1 = _decorator_update(txt, _decf)

    for pair in log_call_remap:
        txt1 = txt1.replace(pair[0], pair[1])
    return txt1


def checked_modification(to_dtrack):
    """Modifies ALL files to use or not use dtrack.
       When modifying files to use dtrack, an exception is thrown and NO files are modified unless ALL modifications are reversable."""
    src_root = os.path.realpath(enclosing_folder+'/../../..').replace('\\','/')
    print(f'dtrack enable={to_dtrack} applied to all .py files recursivly in {src_root}')
    def show_difference(str1, str2, diff_message):
        whitespace_replace = True
        if '\r\n' in str1 or '\r\n' in str2:
            raise Exception('CRLF shouldnt ever get here bug in this code.')
        if whitespace_replace:
            diff_message += ' (whitespace replacing is used in this report)'
            str1 = str1.replace(' ','ₒ'); str2 = str2.replace(' ','ₒ')
        print(diff_message)
        if str1==str2:
            print('<No string difference detected>')
            return
        use_differ = False # The differ may be hard to understand.
        if use_differ:
            d = difflib.Differ()
            diff = d.compare(str1.splitlines(), str2.splitlines())
            print('\n'.join(diff))
        else:
            first_ix = 0
            for i in range(max(len(str1), len(str2))):
                if i>=len(str1):
                    print(f'<Second string is longer, {len(str2)} vs {len(str1)}, but agreement up to length of first string>')
                    return
                if i>=len(str2):
                    print(f'<First string is longer, {len(str1)} vs {len(str2)}, but agreement up to length of second string>')
                    return
                if str1[i] != str2[i]:
                    first_ix = i
                    break
            radius = 48
            piece1 = str1[max(0, first_ix-radius):min(len(str1), first_ix+radius)]
            piece2 = str2[max(0, first_ix-radius):min(len(str2), first_ix+radius)]
            print('First difference A vs B:')
            print('...'+piece1+'...'); print('----'); print('...'+piece2+'...'); print('END first difference')
    cf = set_to_dtrack_or_loguru

    blocklist = ['.*__init__.py.*', '\\/src\\/setup.py'] # These are not useful for dtrack.

    # Debug option to limit or stop certain problem files.
    debug_which_break_counter = 8
    file_boundaries = [None, None]
    debuggy_f = lambda the_filename: False # Change this function to give yes for problem files.

    files2deltas = {}
    for foldername, subfolders, filenames in os.walk(src_root):
        for filename in filenames:
            if filename.endswith('.py') and not filename.endswith('dtrack.py'):
                file_path = foldername.replace('\\','/')+'/'+filename.replace('\\','/')
                file_pat_rel = file_path.replace(src_root,'')
                if any([re.match(skip, file_pat_rel) for skip in blocklist]):
                    continue
                if to_dtrack:
                    # DEBUG eliminate some files if it isnt working.
                    if debuggy_f(filename):
                        debug_which_break_counter = debug_which_break_counter-1
                        if debug_which_break_counter<=1 and debug_which_break_counter>=0:
                            file_boundaries[debug_which_break_counter] = file_path
                        if debug_which_break_counter<=0:
                            continue
                with open(file_path, 'r', encoding='utf-8') as file_obj:
                    txt = file_obj.read().replace('\r\n','\n')

                if len(txt.strip())==0: # Empty files.
                    continue

                if '\t' in txt:
                    raise Exception(f'TABS in {filename}. Python is allergic to TABS. Please remove all TABS in this file.')

                # Various checks to ensure the modification is working properly and can be undone:
                txt1 = cf(txt, True); txt11 = cf(txt1, True)
                txt0 = cf(txt, False); txt00 = cf(txt0, False)
                if txt1 != txt11:
                    raise Exception(f'set_to_dtrack_or_loguru(txt, True) failed to be a idempotent for {file_path}.')
                if txt0 != txt00:
                    raise Exception(f'set_to_dtrack_or_loguru(txt, False) failed to be a idempotent for {file_path}.')
                txt_result = txt1 if to_dtrack else txt0
                if txt_result == txt:
                    continue
                txt10 = cf(txt1, False)
                if to_dtrack and txt10 != txt:
                    show_difference(txt, txt1, 'b4 vs after, difference is OK')
                    show_difference(txt, txt10, 'b4 vs revert, difference is an error')
                    raise Exception(f'The modification would not have been revertable for {file_path}. This may be due to trailing whitespace.')
                files2deltas[file_path] = [txt, txt_result]
    for file_path in files2deltas.keys():
        file_pat_rel = file_path.replace(src_root,'')
        print(f'{"Modifying" if to_dtrack else "Reverting"} file: {src_root} / {file_pat_rel}')
        with open(file_path, 'w', encoding='utf-8', newline='\n') as file_obj:
            new_txt = files2deltas[file_path][1]
            file_obj.write(new_txt.replace('\r\n','\n'))

    if file_boundaries[0] is not None:
        print(f'Debug cutoff, did {file_boundaries[1]} but skipped {file_boundaries[0]}')

############### Delete logs or databases if they get too big #############

def delete_all_logs():
    """Deletes all logs across all projects, both loguru and dtrack-based logs are deleted."""
    projects_folder = os.path.realpath(enclosing_folder+'/../../../projects').replace('\\','/')
    for project_folder in os.listdir(projects_folder):
        log_folder = (projects_folder+'/'+project_folder+'/logs')
        if os.path.isdir(log_folder):
            print('Deleting .log files in:', log_folder)
            for fname in os.listdir(log_folder):
                if fname.endswith('.log'):
                    fnamefull = log_folder+'/'+fname
                    print(f'  Deleting: {fnamefull}')
                    os.remove(fnamefull)


def delete_all_databases(): # TODO: duplicate code with delete_all_logs.
    """Deletes all logs across all projects, both loguru and dtrack-based logs are deleted."""
    projects_folder = os.path.realpath(enclosing_folder+'/../../../projects').replace('\\','/')
    for project_folder in os.listdir(projects_folder):
        json_folder = (projects_folder+'/'+project_folder+'/json_db')
        if os.path.isdir(json_folder):
            print('Deleting:', json_folder)
            shutil.rmtree(json_folder)

############### One-time startup ################

if 'main_logstore' not in locals() and 'main_logstore' not in globals():
    main_logstore = LogStore()
    if check_if_logio_i_fied():
        if use_loguru:
            print(f'Removing the default logger sink because dtrack.io is bieng used, pid = {os.getpid()}.')
            logger.remove()
    else:
        print('Assumed to not be using dtrack.logio this run') # Doesn't even get here lol.
    if 'main_logstore' not in locals() and 'main_logstore' not in globals():
        raise Exception('Bug in this code variable not added')

if __name__ == '__main__': # Call this script directly to change the logging mode.
    while True:
        x = input('Press "d" to make the source use the dtrack logger, press "l" to revert to logger modification, rm to delete all log files:')
        x = str(x).lower().strip()
        if x=='d':
            checked_modification(True)
        elif x=='l':
            checked_modification(False)
        elif x=='rm':
            x1 = input('Y to confirm LOG deletion (cleans up after a run):').lower()
            if x1 == 'y':
                delete_all_logs()
            x1 = input('Y to confirm JSON database deletion (resets after a run):').lower()
            if x1 == 'y':
                delete_all_databases()
