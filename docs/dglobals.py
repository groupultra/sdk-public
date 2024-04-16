# Documentation data-types and global structures.
import os, ast


def _parent_links(tree):
    """In-place add parents."""
    for node in ast.walk(tree): # Add parent nodes.
        for child in ast.iter_child_nodes(node):
            child.parent = node


def _get_sym_semiqual(node_with_parent):
    """Uses the .parent attribute to get the module-level qualified symbol. Which must be added with a walk."""
    x = node_with_parent
    if not hasattr(x, 'parent') and ((isinstance(x, ast.FunctionDef) or isinstance(x, ast.AsyncFunctionDef))):
        raise Exception('Need to add .parent to all nodes.')
    pieces = []
    while hasattr(x, 'parent'):
        if hasattr(x,'name'):
            pieces = [x.name]+pieces
        x = x.parent
    return '.'.join(pieces)


class NoDefault:
    """Mark a function arg as not having a default"""

    def __str__(self):
        return 'NoDefault()'
    def __repr__(self): return str(self)


class FunctionDoc:
    """Docs for one function, which may be a class method."""
    def __init__(self, node_with_parent):
        f = node_with_parent
        self._node = f
        self.docstring = ast.get_docstring(f)
        self.sym_semiqual = _get_sym_semiqual(f)
        self.sym_qual = None
        self.args = [a.arg for a in f.args.args]
        self.class_name = None # None = module level. Non-None = the name of the class.

        self.defaults = [NoDefault()]*(len(self.args)-len(f.args.defaults))+[ast.unparse(d) for d in f.args.defaults]
        self.kwarg = None
        if f.args.kwarg:
           self.kwarg = f.args.kwarg.arg
        self.is_async = isinstance(f, ast.AsyncFunctionDef)

    def __str__(self):
        docshort = self.docstring
        if docshort and len(docshort)>48+6:
            docshort = docshort[0:48]+'...'
        if docshort:
            docshort = docshort.replace('\r\n','\n').replace('\n','\\n')
        return f'FunctionDoc({self.sym_qual}, docstring={docshort}, args={self.args}, kwargs={self.kwarg}, async={self.is_async}, defaults={self.defaults})'

    def __repr__(self): return str(self)


class ModuleDoc:
    """Docs for a module, which includes classes and all internal methods."""
    def __init__(self, filename):
        filename = os.path.realpath(filename).replace('\\','/')

        if not os.path.exists(filename):
            raise Exception(f'Cannot find file: {filename}')

        file_contents = ""
        with open(filename, encoding='utf-8') as fd:
            file_contents = fd.read()
        tree = ast.parse(file_contents)

        self.relative_filename = filename.split('/src/')[1]

        self.modulename = self.relative_filename.replace('.py','').replace('/','.')
        _parent_links(tree)
        splay = [x for x in ast.walk(tree)]
        functions = [f for f in splay if (isinstance(f, ast.FunctionDef) or isinstance(f, ast.AsyncFunctionDef))]

        self.class_names = [c.name for c in splay if isinstance(c, ast.ClassDef)]
        self.class_docstrings = [ast.get_docstring(c) for c in splay if isinstance(c, ast.ClassDef)]

        self.function_docs = [FunctionDoc(f) for f in functions]

        for cname in self.class_names:
            for fd in self.function_docs: # O(n^2) if the module is ridiculously huge.
                if fd.sym_semiqual.startswith(cname):
                    fd.class_name = cname

        for fd in self.function_docs:
            fd.sym_qual = self.modulename+'.'+fd.sym_semiqual

    def __str__(self):
        return f'ModuleDoc(relative_filename={self.relative_filename}, modulename={self.modulename}, class_names={self.class_names}, tree_fn_count={len(self.function_docs)})'
    def __repr__(self): return str(self)


all_module_docs = []
module_doc_dict = {} # Symbol => ModuleDoc object
def load_all_modules(base_folder='../src/'):
    """Recursive walk and saves to all_module_docs."""
    triplets = os.walk(base_folder)
    out = []
    for folder, _, files in triplets:
        filesfull = [folder+'/'+f for f in files if f.endswith('.py')]
        out.extend([ModuleDoc(f) for f in filesfull])
    global all_module_docs
    all_module_docs = out.copy()
    global module_doc_dict
    for mdoc in out:
        module_doc_dict[mdoc.modulename] = mdoc
    return out
