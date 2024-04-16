# Automatically generates read-the-docs documentation in docs/source *of the sdk-public folder* (asking for an input if it can't find it).
# The default generate-from-docstring lacks enough flexibility (API hooks) to work properly on this source.
# Note: This file customizes the docs a plenty.
import os, shutil
import dglobals, write_moduledoc, write_index, write_findex

def _sdk_path():
    sdk_public_path = '../../sdk-public'
    if not os.path.exists(sdk_public_path): # One time choice.
        from tkinter import filedialog, Tk
        root = Tk()
        root.withdraw()
        sdk_public_path = filedialog.askdirectory('Choose the Moobius SDK Public folder.')
    sdk_public_path = sdk_public_path.replace('\\','/')
    return sdk_public_path


def save_files_sdkpublic(save_files):
    """Saves a dict from filename to contents. The paths are local with respect to the docs/source."""

    sdk_public_path = _sdk_path()

    sdk_docsource_path = sdk_public_path+'/docs/source'
    for windoze in range(8):
        if os.path.exists(sdk_docsource_path):
            try:
                shutil.rmtree(sdk_docsource_path) # Clean up.
            except Exception as e:
                import time
                time.sleep(0.5)
                if windoze==7:
                    shutil.rmtree(sdk_docsource_path)
    for local_path, txt in save_files.items():
        the_path = sdk_docsource_path+'/'+local_path
        os.makedirs(os.path.dirname(the_path), exist_ok=True)
        with open(the_path, 'w', encoding='utf-8') as f:
            f.write(txt)


def render_docs_sdkpublic():
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

if __name__ == '__main__':
    modules = dglobals.load_all_modules(base_folder='../src/')
    modules = list(filter(lambda m: m.modulename not in ['moobius.__init__', 'setup'], modules))

    save_files = {}
    for copy_this in ['conf.py', './requirements.txt']:
        with open('./'+copy_this, 'r', encoding='utf-8') as f:
            save_files[copy_this] = f.read()
            save_files['../'+copy_this] = f.read()

    save_files['index.rst'] = write_index.make_txt(modules)
    save_files['function_index.rst'] = write_findex.make_txt(modules)
    for mdoc in modules:
        save_files[mdoc.modulename.replace('.','_')+'.rst'] = write_moduledoc.make_txt(mdoc)

    save_files_sdkpublic(save_files)
    render_docs_sdkpublic()
