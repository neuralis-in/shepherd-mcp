# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys

# Add source directory to path for autodoc
sys.path.insert(0, os.path.abspath("../src"))

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "Shepherd MCP"
copyright = "2024, Neuralis"
author = "Neuralis"
release = "0.1.0"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "sphinx.ext.autosummary",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# Napoleon settings for Google/NumPy style docstrings
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = True
napoleon_use_admonition_for_notes = True
napoleon_use_admonition_for_references = False

# Autodoc settings
autodoc_default_options = {
    "members": True,
    "undoc-members": True,
    "show-inheritance": True,
    "member-order": "bysource",
}
autodoc_typehints = "description"
autodoc_class_signature = "separated"

# Intersphinx mapping
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "pydantic": ("https://docs.pydantic.dev/latest/", None),
}

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "alabaster"
html_static_path = ["_static"]
html_css_files = ["custom.css"]

# Alabaster theme options - white monochrome
html_theme_options = {
    # Main colors - pure white/monochrome
    "body_bg": "#ffffff",
    "page_width": "1000px",
    "sidebar_width": "260px",
    # Header styling
    "head_font_family": "'IBM Plex Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
    "font_family": "'IBM Plex Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
    "code_font_family": "'IBM Plex Mono', 'SF Mono', 'Monaco', 'Consolas', monospace",
    "font_size": "16px",
    "code_font_size": "14px",
    # Link colors - subtle gray/black
    "link": "#1a1a1a",
    "link_hover": "#000000",
    # Sidebar
    "sidebar_header": "#1a1a1a",
    "sidebar_text": "#333333",
    "sidebar_link": "#1a1a1a",
    "sidebar_link_underscore": "#cccccc",
    "sidebar_search_button": "#333333",
    # Code blocks
    "code_bg": "#f8f8f8",
    "code_text": "#1a1a1a",
    "code_highlight_bg": "#f0f0f0",
    # Headings
    "narrow_sidebar_bg": "#fafafa",
    "narrow_sidebar_link": "#1a1a1a",
    # Other
    "note_bg": "#f5f5f5",
    "note_border": "#dddddd",
    "warn_bg": "#f5f5f5",
    "warn_border": "#999999",
    "seealso_bg": "#f5f5f5",
    "seealso_border": "#dddddd",
    "topic_bg": "#f5f5f5",
    # Footer
    "footer_text": "#666666",
    # Misc
    "gray_1": "#333333",
    "gray_2": "#666666",
    "gray_3": "#999999",
    # Show related
    "show_related": False,
    "show_relbars": False,
    # Logo/branding
    "logo_name": False,
    "description": "Debug your AI agents like you debug your code",
    "github_user": "neuralis",
    "github_repo": "shepherd-mcp",
    "github_button": True,
    "github_type": "star",
}

# Title
html_title = "Shepherd MCP Documentation"
html_short_title = "Shepherd MCP"

# Favicon
# html_favicon = "_static/favicon.ico"

# Don't show "Created using Sphinx" in the footer
html_show_sphinx = False

# Show copyright
html_show_copyright = True

