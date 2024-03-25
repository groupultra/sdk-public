# Automatically generates read-the-docs documentation in docs/source *of the sdk-public folder* (asking for an input if it can't find it).
# The default generate-from-docstring lacks enough flexibility (API hooks) to work properly on this source.
# Note: This file customizes the docs a plenty.
import load_source, render_module

modules = load_source.load_all_modules(base_folder='../src/')
modules = list(filter(lambda m: '__init__' not in m.modulename, modules))
ref_links = [m.modulename.replace('.','_') for m in modules] # Used by render_module.
strings = [render_module.blit(m, l) for m, l in zip(modules, ref_links)]

save_fnames = [r+'.rst' for r in ref_links]
save_files = dict(zip(save_fnames, strings))
for copy_this in ['conf.py', '../index.rst', '../requirements.txt']:
    with open('./source/'+copy_this, 'r', encoding='utf-8') as f:
        save_files[copy_this] = f.read()

index_lines = []
for i in range(len(modules)):
    ref_link_viz = ref_links[i].replace('_','.')
    index_lines.append(f"* :ref:`{ref_link_viz} <{ref_links[i]}>`")
index_lines = '\n'.join(index_lines)

index_txt = f"""
Welcome to the Moobius SDK
===================================

**Moobius** is a group-driven social interaction platform which resembles Discord but has more features and flexibility.

This library is the open-source SDK for building CCS apps. These apps interface with the Platform and allow your computer (or a cloud instance) to have full awareness and control as to who is joinded and which users see what content.

Don't worry about network configuration! The included Demo in the `public Github repo <https://github.com/groupultra/sdk-public>`_ needs nothing more than your Moobius account credentials and the ID of a Moobius channel you created in the browser.

Check out the :doc:`usage` section for further information, including
how to :ref:`installation` the project.

.. note::

   This project is out of Beta but is still under active development.

Modules
==================

{index_lines}

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""

save_files['index.rst'] = index_txt

render_module.save_files_sdkpublic(save_files)

render_module.render_docs_sdkpublic(save_files)