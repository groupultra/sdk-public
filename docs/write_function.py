import detail_overrides
from dglobals import FunctionDoc

def make_txt(fdoc: FunctionDoc):
    """Makes the text for a single function (module level or class method)."""
    with open('./function.rst', 'r', encoding='utf-8') as f:
        template = f.read()
    if ds:=detail_overrides.override_docstring(fdoc):
        fdoc.docstring = ds
    template = template.replace('{SYM_QUAL}', fdoc.sym_qual)
    template = template.replace('{SYM_SEMIQUAL}', fdoc.sym_semiqual)
    template = template.replace('{DOCLINE}', ''.join(oneliner_fdoc(fdoc)))
    template = template.replace('{DOCSTRING}', fdoc.docstring if fdoc.docstring else "<No doc string>")
    if x:=detail_overrides.override_function_doc(fdoc, template):
        return str(x)
    return template


def oneliner_fdoc(fdoc: FunctionDoc):
    comma_sep_args = ', '.join(fdoc.args+(['\*'+fdoc.kwarg] if fdoc.kwarg else []))
    return fdoc.sym_semiqual, f'({comma_sep_args})'
