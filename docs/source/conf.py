# Configuration file for the Sphinx documentation builder.
# TODO: CSS color like this:
# https://docs.readthedocs.io/en/stable/guides/adding-custom-css.html

import os
import sys
#sys.path.insert(0, os.path.abspath('../../src/')) #https://sphinx-rtd-tutorial.readthedocs.io/en/latest/sphinx-config.html?highlight=autodoc#autodoc-configuration

#def setup(app): # Can't get this way of making colors working
#    app.add_css_file('/custom.css')

# -- Project information

project = 'Moobius'
copyright = '2024, GroupUltra Ltd'
author = 'Kevin Kostlan'

release = '1.3'
version = '1.3.x'

# -- General configuration

extensions = [
    'sphinx.ext.duration',
    'sphinx.ext.doctest',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.intersphinx',
    'sphinx_rtd_theme'
]

intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
    'sphinx': ('https://www.sphinx-doc.org/en/master/', None),
}
intersphinx_disabled_domains = ['std']

templates_path = ['_templates']

html_static_path = ['_static']
html_css_files = ['super_custom.css']
# -- Options for HTML output
html_theme = 'pydata_sphinx_theme'
html_theme_options = {
    "logo": {
        "text": "",
        "image_light": "https://groupultra.github.io/moobius/img/logo-light.png",
        "image_dark": "https://groupultra.github.io/moobius/img/logo-dark.png",
    },
    "search_bar_position": "sidebar",
}
# -- Options for EPUB output
epub_show_urls = 'footnote'
