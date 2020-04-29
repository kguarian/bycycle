# -*- coding: utf-8 -*-
#
# Configuration file for the Sphinx documentation builder.
#
# For a full list of documentation options, see:
# https://www.sphinx-doc.org/en/master/usage/configuration.html


# ----------------------------------------------------------------------------

import os
from os.path import dirname as up

from datetime import date

import sphinx_gallery
import sphinx_bootstrap_theme
from sphinx_gallery.sorting import FileNameSortKey


# -- Project information -----------------------------------------------------

# General information about the project.
project = 'bycycle'
copyright = '2018-{}, VoytekLab'.format(date.today().year)
author = 'Scott Cole'

# Get the current version number from inside the module
with open(os.path.join(up(up(__file__)), 'bycycle', 'version.py')) as vf:
    exec(vf.read())

# The short X.Y version
version = __version__
# The full version, including alpha/beta/rc tags
release = version


# -- General configuration ------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.doctest',
    'sphinx.ext.coverage',
    'sphinx.ext.githubpages',
    'sphinx.ext.mathjax',
    'sphinx.ext.viewcode',
    'sphinx_gallery.gen_gallery',
    'sphinx.ext.intersphinx',
    'sphinx_copybutton',
    'numpydoc'
]

# generate autosummary even if no references
autosummary_generate = True

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
# source_suffix = ['.rst', '.md']
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = None

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This patterns also effect to html_static_path and html_extra_path
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# numpydoc interacts with autosummary, that creates excessive warnings
# This line is a 'hack' for that interaction that stops the warnings
numpydoc_show_class_members = False

# Set to generate sphinx docs for class members (methods)
autodoc_default_options = {
    'members': None,
    'inherited-members': None,
}

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# Settings for sphinx_copybutton
copybutton_prompt_text = "$ "

# -- Options for HTML output ----------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
# html_theme = 'alabaster'
# html_theme = 'classic'
# html_theme = 'haiku'
html_theme = 'bootstrap'
html_theme_path = sphinx_bootstrap_theme.get_html_theme_path()

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#
html_theme_options = {
    # A list of tuples containing pages or urls to link to.
    'navbar_links': [
        ("API", "api"),
        ("Tutorial", "auto_tutorials/index"),
        ("Examples", "auto_examples/index"),
        ("GitHub", "https://github.com/bycycle-tools/bycycle", True)
    ],

    # Bootswatch (http://bootswatch.com/) theme.
    #
    # Options are nothing (default) or the name of a valid theme
    # such as "cosmo" or "sandstone".
    #
    # The set of valid themes depend on the version of Bootstrap
    # that's used (the next config option).
    #
    # Currently, the supported themes are:
    # - Bootstrap 2: https://bootswatch.com/2
    # - Bootstrap 3: https://bootswatch.com/3
    'bootswatch_theme': "flatly",

    # Set the page width to not be restricted to hardset value
    'body_max_width': None,

    # Render the current pages TOC in the navbar. (Default: true)
    'navbar_pagenav': False,

    # Render the next and previous page links in navbar. (Default: true)
    'navbar_sidebarrel': False,
}

# Settings for whether to copy over and show link rst source pages
html_copy_source = False
html_show_sourcelink = False

# Add logo
html_logo = 'logo.jpg'


# Example configuration for intersphinx: refer to the Python standard library.
intersphinx_mapping = {'https://docs.python.org/': None}


# -- Extension configuration -------------------------------------------------

sphinx_gallery_conf = {
     # path to your examples scripts
    'examples_dirs': ['../examples', '../tutorials'],
     # path where to save gallery generated examples
    'gallery_dirs': ['auto_examples', 'auto_tutorials'],
    'within_subsection_order': FileNameSortKey,
    'backreferences_dir': 'generated',
    'thumbnail_size': (250, 250),
    'doc_module': ('bycycle'),
    'reference_url': {
        'bycycle': None
        }
}
