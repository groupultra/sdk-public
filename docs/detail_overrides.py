# Override function-level docstrings, etc, generally for when more verbosity is needed.
import dglobals
from dglobals import FunctionDoc

def override_docstring(fdoc: FunctionDoc):
    """Optionally overrides the docstring."""
    big_doc_dict = dglobals.module_doc_dict
    #print(fdoc.sym_qual)
    #print(fdoc.docstring)
    shortcuts = {'Calls self.http_api':big_doc_dict['moobius.network.http_api_wrapper'],
                 'Calls self.ws_client':big_doc_dict['moobius.network.ws_client']}
    for k, v in shortcuts.items():
        if fdoc.docstring and k.lower() in fdoc.docstring.lower():
            fn_name_lower = fdoc.docstring.strip().replace(k, '').split(' ')[0]
            if fn_name_lower[0] == '.':
                fn_name_lower = fn_name_lower[1:]
            if fn_name_lower[-1] == '.':
                fn_name_lower = fn_name_lower[0:-1]
            target_fdoc = None
            for fdoc1 in v.function_docs:
                if fn_name_lower in fdoc1.sym_qual.lower():
                    target_fdoc = fdoc1
            if not target_fdoc:
                print(fdoc.docstring)
                print([fdoc1.sym_qual.lower() for fdoc1 in v.function_docs])
                raise Exception(f'Cannot find shortcut to: {fn_name_lower}')
            return fdoc.docstring+'\nDoc for the called function:\n'+target_fdoc.docstring
    return None


def override_function_doc(fdoc, default_doc):
    """
    Optionally overrides the function documentation.
    More flexible than override_docstring, but harder to use.

    Parameters:
      fdoc: The dglobals.FunctionDoc object.
      default_doc: The non-overriden function doc.
      """
    return None


def override_class_docstring(class_name, class_docstring, class_fdocs):
    """Optionally overrides the doc string for a class docstring."""
    return None


def override_class_docs(class_name, class_docstring, class_fdocs, default_class_docs):
    """More flexible than override_class_docstring, but harder to use."""
    return None


def override_module_doc(mdoc, template):
    """Optionally override the module docs."""
    return None
