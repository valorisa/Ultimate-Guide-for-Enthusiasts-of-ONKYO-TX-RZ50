# Configuration file for the Sphinx documentation builder.
# Ultimate Guide for Enthusiasts of ONKYO TX-RZ50

import os
import sys

# Add the project root to the path for autodoc
sys.path.insert(0, os.path.abspath('../..'))
sys.path.insert(0, os.path.abspath('../../scripts'))

# -- Project information -----------------------------------------------------
project = 'Ultimate Guide for Enthusiasts of ONKYO TX-RZ50'
copyright = '2024, valorisa'
author = 'valorisa'
release = '1.0.0'
version = '1.0'

# -- General configuration ---------------------------------------------------
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx.ext.intersphinx',
    'sphinx.ext.githubpages',
    'myst_parser',
]

# MyST Parser configuration
myst_enable_extensions = [
    "colon_fence",
    "deflist",
    "fieldlist",
    "html_image",
    "linkify",
    "substitution",
    "tasklist",
    "attrs_inline",
]
myst_heading_anchors = 3
myst_footnote_transition = True

# Source suffixes
source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown',
}

# Master document
master_doc = 'index'

# Exclude patterns
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- Options for HTML output -------------------------------------------------
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
html_css_files = ['custom.css'] if os.path.exists('_static/custom.css') else []
html_title = 'ONKYO TX-RZ50 Ultimate Guide'
html_short_title = 'TX-RZ50 Guide'

# -- Options for autodoc -----------------------------------------------------
autodoc_member_order = 'bysource'
autodoc_default_options = {
    'members': True,
    'undoc-members': True,
    'show-inheritance': True,
}

# -- Options for napoleon ----------------------------------------------------
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True

# -- Options for intersphinx -------------------------------------------------
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'requests': ('https://requests.readthedocs.io/en/latest/', None),
    'pyserial': ('https://pyserial.readthedocs.io/en/latest/', None),
}

# -- Language ----------------------------------------------------------------
language = 'fr'

# Ignorer les warnings pour les images manquantes (temporaire)
suppress_warnings = ['image.not_readable', 'toc.not_readable']
