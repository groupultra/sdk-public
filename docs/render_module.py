# Renders a module and uses the docstrings, outputing 
# This module is granular (TODO: improve) to ease customizing the render.
import os
import load_source
import subprocess
sdk_public_path = '../../sdk-public'

def blit_fdoc(fdoc):
    comma_sep_args = ', '.join(fdoc.args+(['\*'+fdoc.kwarg] if fdoc.kwarg else []))
    return f"""
{fdoc.sym_qual}
----------------------
{fdoc.sym_qual}({comma_sep_args})
{fdoc.docstring if fdoc.docstring else "<No doc string>"}
""".strip()

def blit(mdoc: load_source.ModuleDoc, ref_link):
    """Blits a doc into a .rst file. ref_link sets the link to this file"""
    pieces = []

    delim2 = '\n\n'
    class_strs = []
    fdocs = mdoc.function_docs

    for fd in mdoc.function_docs:
        fd.class_name = None # Add this attribute.

    for cname in mdoc.class_names:
        for fd in mdoc.function_docs:
            if fd.sym_qual.startswith(cname):
                fd.class_name = cname

    module_level_f_summaries = [blit_fdoc(fdoc) for fdoc in mdoc.function_docs if fdoc.class_name is None]
    class_summaries = []
    for i in range(len(mdoc.class_names)):
        cname = mdoc.class_names[i]
        cdocstr = mdoc.class_docstrings[i]
        class_level_docs = [blit_fdoc(fdoc) for fdoc in mdoc.function_docs if fdoc.class_name == cname]
        txt = f"""
Class {cname}
==================

{cdocstr if cdocstr else "(No doc string)"}

{delim2.join(class_level_docs)}
"""
        class_summaries.append(txt)
    return f"""
.. _{ref_link}:

{mdoc.modulename}
===================================

Module-level functions
==================

{delim2.join(module_level_f_summaries)}

==================

{delim2.join(class_summaries)}
""".strip()


def _sdk_path():
    global sdk_public_path
    if not os.path.exists(sdk_public_path): # One time choice.
        from tkinter import filedialog, Tk
        root = Tk()
        root.withdraw()
        sdk_public_path = filedialog.askdirectory('Choose the Moobius SDK Public folder.')
    sdk_public_path = sdk_public_path.replace('\\','/')
    return sdk_public_path


def save_files_sdkpublic(d):
    """Saves a dict from filename to contents. The paths are local with respect to the docs/source."""

    sdk_public_path = _sdk_path()

    sdk_docsource_path = sdk_public_path+'/docs/source'
    for local_path, txt in d.items():
        the_path = sdk_docsource_path+'/'+local_path
        os.makedirs(os.path.dirname(the_path), exist_ok=True)
        with open(the_path, 'w', encoding='utf-8') as f:
            f.write(txt)


def render_docs_sdkpublic(d):
    """Calls render modules."""
    sdk_public_path = _sdk_path()
    build_dir = f'{sdk_public_path}/docs/source'
    build_dir = os.path.realpath(build_dir).replace('\\','/')
    output_dir = sdk_public_path+'/../Read_the_docs_AUTOgen'
    output_dir = os.path.realpath(output_dir).replace('\\','/')

    shell_txt = f"""
    sphinx-build -b html "{build_dir}" "{output_dir}"
    """.strip()
    print('Calling sphynx-build from dir:', shell_txt)

    os.system(shell_txt)
    print('Opening the fresh HTML in the browser!')
    import webbrowser
    link='file://'+output_dir+'/index.html'
    firefox = webbrowser.Mozilla("C:/Program Files/Mozilla Firefox/firefox.exe") 
    firefox.open(link) 

# Using open() function to display the URL. 
    #webbrowser.open()