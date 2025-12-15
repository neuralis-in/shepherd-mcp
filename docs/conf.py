# Configuration file for the Sphinx documentation builder.

import os
import sys

sys.path.insert(0, os.path.abspath("../src"))

# -- Project information -----------------------------------------------------

project = "Shepherd MCP"
copyright = "2024, Neuralis"
author = "Neuralis"
release = "0.1.0"

# -- General configuration ---------------------------------------------------

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# Napoleon settings
napoleon_google_docstring = True
napoleon_numpy_docstring = True

# Autodoc settings
autodoc_default_options = {
    "members": True,
    "undoc-members": True,
    "show-inheritance": True,
}
autodoc_typehints = "description"

# Intersphinx
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
}

# -- Options for HTML output -------------------------------------------------

html_theme = "alabaster"

html_theme_options = {
    "description": "Debug your AI agents like you debug your code",
    "github_user": "neuralis",
    "github_repo": "shepherd-mcp",
    "github_button": True,
    "github_type": "star",
}

html_title = "Shepherd MCP"
html_short_title = "Shepherd MCP"
html_show_sphinx = False
html_show_copyright = True
