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
    "sphinx_copybutton",
    "sphinx_design",
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

# Copy button settings
copybutton_prompt_text = r">>> |\.\.\. |\$ "
copybutton_prompt_is_regexp = True

# -- Options for HTML output -------------------------------------------------

html_theme = "furo"

html_theme_options = {
    "light_css_variables": {
        "color-brand-primary": "#0ea5e9",
        "color-brand-content": "#0284c7",
        "color-admonition-background": "rgba(14, 165, 233, 0.1)",
        "font-stack": "'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
        "font-stack--monospace": "'JetBrains Mono', 'Fira Code', 'Consolas', monospace",
    },
    "dark_css_variables": {
        "color-brand-primary": "#38bdf8",
        "color-brand-content": "#7dd3fc",
        "color-admonition-background": "rgba(56, 189, 248, 0.1)",
        "color-background-primary": "#0f172a",
        "color-background-secondary": "#1e293b",
        "color-background-hover": "#334155",
        "color-background-border": "#475569",
        "color-foreground-primary": "#f1f5f9",
        "color-foreground-secondary": "#94a3b8",
        "color-foreground-muted": "#64748b",
        "color-foreground-border": "#475569",
    },
    "sidebar_hide_name": False,
    "navigation_with_keys": True,
    "top_of_page_button": "edit",
    "source_repository": "https://github.com/neuralis/shepherd-mcp",
    "source_branch": "main",
    "source_directory": "docs/",
}

html_title = "Shepherd MCP"
html_short_title = "Shepherd MCP"
html_show_sphinx = False
html_show_copyright = True

html_static_path = ["_static"]
html_css_files = ["custom.css"]

# Custom logo and favicon (optional - uncomment if you have them)
# html_logo = "_static/logo.svg"
# html_favicon = "_static/favicon.ico"
