Development Guide
=================

This guide covers how to set up a development environment and contribute to 
Shepherd MCP.

.. contents:: On this page
   :local:
   :depth: 2

Setup
-----

Clone the repository:

.. code-block:: bash

   git clone https://github.com/neuralis/shepherd-mcp
   cd shepherd-mcp

Create a virtual environment and install dependencies:

.. code-block:: bash

   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -e ".[dev]"

Running Tests
-------------

Run the test suite with pytest:

.. code-block:: bash

   pytest

Run with coverage:

.. code-block:: bash

   pytest --cov=shepherd_mcp

Running Locally
---------------

Set up your environment variables:

.. code-block:: bash

   export AIOBS_API_KEY=aiobs_sk_xxxx
   export LANGFUSE_PUBLIC_KEY=pk-lf-xxxx
   export LANGFUSE_SECRET_KEY=sk-lf-xxxx

Run the MCP server:

.. code-block:: bash

   python -m shepherd_mcp

Code Style
----------

This project uses ``ruff`` for linting and formatting:

.. code-block:: bash

   # Check for issues
   ruff check .
   
   # Auto-fix issues
   ruff check --fix .
   
   # Format code
   ruff format .

Project Structure
-----------------

.. code-block:: text

   src/shepherd_mcp/
   ├── __init__.py          # Package exports
   ├── __main__.py          # Entry point
   ├── server.py            # MCP server with tool handlers
   ├── models/              # Data models
   │   ├── __init__.py
   │   ├── aiobs.py         # AIOBS-specific models
   │   └── langfuse.py      # Langfuse-specific models
   └── providers/           # Provider clients
       ├── __init__.py
       ├── base.py          # Base provider interface
       ├── aiobs.py         # AIOBS client implementation
       └── langfuse.py      # Langfuse client implementation

Architecture
------------

.. code-block:: text

   ┌─────────────────┐     stdio      ┌─────────────────┐
   │  Cursor/Claude  │ ◄────────────► │  shepherd-mcp   │
   │    (Client)     │   stdin/stdout │   (subprocess)  │
   └─────────────────┘                └────────┬────────┘
                                               │ HTTPS
                                     ┌─────────┴─────────┐
                                     │                   │
                                     ▼                   ▼
                            ┌─────────────┐     ┌─────────────┐
                            │ Shepherd API│     │ Langfuse API│
                            │   (AIOBS)   │     │   (Cloud)   │
                            └─────────────┘     └─────────────┘

Building Documentation
----------------------

Build the Sphinx documentation:

.. code-block:: bash

   cd docs
   make html

The built documentation will be in ``docs/_build/html/``.

Publishing to PyPI
------------------

Releases are automatically published to PyPI via GitHub Actions when a release 
is created.

To publish manually:

.. code-block:: bash

   # Build the package
   pip install build twine
   python -m build
   
   # Upload to PyPI
   twine upload dist/*

Adding a New Provider
---------------------

To add support for a new observability provider:

1. Create a new models file in ``src/shepherd_mcp/models/`` with your data models
2. Create a new provider client in ``src/shepherd_mcp/providers/`` inheriting from ``BaseProvider``
3. Add tool definitions in ``server.py`` under ``list_tools()``
4. Add tool handlers in ``server.py`` under ``call_tool()``
5. Update the provider exports in ``providers/__init__.py``
6. Add tests in ``tests/``

Example provider skeleton:

.. code-block:: python

   from shepherd_mcp.providers.base import BaseProvider, AuthenticationError
   
   class MyProvider(BaseProvider):
       def __init__(self, api_key: str | None = None):
           self.api_key = api_key or os.environ.get("MY_PROVIDER_API_KEY")
           if not self.api_key:
               raise AuthenticationError("No API key provided")
           # Initialize HTTP client, etc.
       
       @property
       def name(self) -> str:
           return "my_provider"
       
       def list_sessions(self):
           # Implement session listing
           pass
       
       def close(self) -> None:
           # Clean up resources
           pass

Contributing
------------

1. Fork the repository
2. Create a feature branch: ``git checkout -b feature/my-feature``
3. Make your changes
4. Run tests: ``pytest``
5. Run linting: ``ruff check .``
6. Commit your changes: ``git commit -am 'Add my feature'``
7. Push to the branch: ``git push origin feature/my-feature``
8. Create a Pull Request

