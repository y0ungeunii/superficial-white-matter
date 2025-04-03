# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import os
import sys

sys.path.insert(0, os.path.abspath('./'))


project = 'superficial-white-matter'
copyright = '2025, Youngeun Hwang'
author = 'Youngeun Hwang'
release = '1.0 beta'

# -- General configuration

extensions = [
    'nbsphinx',
    'sphinx_gallery.load_style',
    'sphinx.ext.duration',
    'sphinx.ext.doctest',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.napoleon',
    'sphinx.ext.intersphinx',
    'sphinx.ext.autosectionlabel',
    'sphinx_gallery.gen_gallery',
    'myst_parser'
]

source_suffix = {
    '.rst': 'restructuredtext',
    '.txt': 'markdown',
    '.md': 'markdown',
}

# source_suffix = '.rst'
source_suffix = ['.rst', '.md']

# -- Sphinx Gallery Configuration --
sphinx_gallery_conf = {
    'examples_dirs': 'examples',  # Directory where your example scripts are located
    'gallery_dirs': 'auto_examples',  # Output directory for generated galleries
    'thumbnail_size': (250, 250),
    'download_all_examples': False,
    'remove_config_comments': True,
}

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

#generate autosummary even if no references
autosummary_generate = True
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
html_show_sourcelink = False
html_copy_source = False
