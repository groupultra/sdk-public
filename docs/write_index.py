def make_txt(modules):
    """Makes the text of index.py given the modules."""
    with open('./index.rst', 'r', encoding='utf-8') as f:
        template = f.read()
    module_ix_lines = []
    for mdoc in modules:
        ref_link = mdoc.modulename.replace('.','_')
        ref_link_viz = ref_link.replace('_','.')
        module_ix_lines.append(f"* :ref:`{ref_link_viz} <{ref_link}>`")
    module_ix_lines = '\n'.join(module_ix_lines)
    return template.replace('{LINES}', module_ix_lines)
