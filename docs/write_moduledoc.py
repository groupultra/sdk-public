import write_function, write_class, detail_overrides

def make_txt(mdoc):
    """Renders and returns the text."""
    with open('./module.rst', 'r', encoding='utf-8') as f:
        template = f.read()
    template = template.replace('{MODULE_REF_LINK}', mdoc.modulename.replace('.','_'))
    template = template.replace('{MODULENAME}', mdoc.modulename)

    by_class = class_level_organize(mdoc)
    fsummaries = [write_function.make_txt(fdoc) for fdoc in by_class[None]]
    if len(fsummaries)==0:
        fsummaries = ['(No module-level functions)']

    template = template.replace('{FSUMMARYSMOD}', '\n\n'.join(fsummaries))
    class_summaries = []
    for i in range(len(mdoc.class_names)):
        cname = mdoc.class_names[i]
        class_summaries.append(write_class.make_txt(cname, mdoc.class_docstrings[i], by_class[cname]))

    template = template.replace('{CLASSSUMMARIES}', '\n\n'.join(class_summaries))
    if x:=detail_overrides.override_module_doc(mdoc, template):
        template = x
    return template


def class_level_organize(mdoc):
    """Mdoc flattens out all methods. This function organizes the fdocs by the class level."""
    out = {None:[]}
    for cname in mdoc.class_names:
        out[cname] = []

    for fd in mdoc.function_docs:
        out[fd.class_name].append(fd)
    return out
