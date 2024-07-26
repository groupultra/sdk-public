import write_function, detail_overrides

def make_txt(class_name, class_docstring, class_fdocs):
    """Returns the resulting .rst file given the template .rst file, a class_name, and a list of fdocs to said class in order."""
    if x:=detail_overrides.override_class_docstring(class_name, class_docstring, class_fdocs):
        class_docstring = x
    with open('./snippets/class.rst', 'r', encoding='utf-8') as f:
        template = f.read()
    template = template.replace('{CNAME}', class_name)
    template = template.replace('{CDOC}', class_docstring if class_docstring else '<no class docstring>')

    cmethod_docs = [write_function.make_txt(fdoc) for fdoc in class_fdocs]
    template = template.replace('{CMETHODS}', '\n\n'.join(cmethod_docs))
    if x:=detail_overrides.override_class_docs(class_name, class_docstring, class_fdocs, template):
        template = x
    return template
