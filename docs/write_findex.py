import write_function

def make_txt(modules):
    with open('./findex.rst', 'r', encoding='utf-8') as f:
        template = f.read()
    ixf_lines = []
    for mdoc in modules:
        for fdoc in mdoc.function_docs:
            fname, fargs = write_function.oneliner_fdoc(fdoc)
            ixf_lines.append(f'* :ref:`{mdoc.modulename}.{fname} <{fdoc.sym_qual}>` {fargs}')
    ixf_lines = '\n'.join(ixf_lines)
    template = template.replace('{FLINES}', ixf_lines)
    return template