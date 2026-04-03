import os
import sys
sys.path.insert(0, os.path.abspath('..'))

project = 'Ultimate Guide for Enthusiasts of ONKYO TX-RZ50'
copyright = '2024, valorisa'
author = 'valorisa'
release = '1.0.0'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx.ext.githubpages',
    'myst_parser'
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
language = 'fr'

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
