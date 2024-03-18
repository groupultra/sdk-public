# Configuration file for the Sphinx documentation builder.

html_theme = 'sphinx_rtd_theme'
import os
import sys
sys.path.insert(0, os.path.abspath('../../src/')) #https://sphinx-rtd-tutorial.readthedocs.io/en/latest/sphinx-config.html?highlight=autodoc#autodoc-configuration

# -- Project information

project = 'Moobius'
copyright = '2021, GroupUltra Ltd'
author = 'Kevin Kostlan'

release = '1.0'
version = '1.0.x'

# -- General configuration

extensions = [
    'sphinx.ext.duration',
    'sphinx.ext.doctest',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.intersphinx',
]

intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
    'sphinx': ('https://www.sphinx-doc.org/en/master/', None),
}
intersphinx_disabled_domains = ['std']

templates_path = ['_templates']

# -- Options for HTML output

html_theme = 'sphinx_rtd_theme'

# -- Options for EPUB output
epub_show_urls = 'footnote'