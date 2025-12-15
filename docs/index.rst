Shepherd MCP Documentation
==========================

**Debug your AI agents like you debug your code.**

Shepherd MCP is a Model Context Protocol (MCP) server that allows AI assistants 
(Claude, Cursor, etc.) to query and analyze your AI agent sessions from multiple 
observability providers.

.. contents:: Table of Contents
   :local:
   :depth: 2

Quick Start
-----------

Installation
^^^^^^^^^^^^

Install via pip:

.. code-block:: bash

   pip install shepherd-mcp

Or run directly with uvx:

.. code-block:: bash

   uvx shepherd-mcp

Configuration
^^^^^^^^^^^^^

Set your environment variables:

.. code-block:: bash

   # AIOBS (Shepherd)
   export AIOBS_API_KEY=aiobs_sk_xxxx

   # Langfuse
   export LANGFUSE_PUBLIC_KEY=pk-lf-xxxx
   export LANGFUSE_SECRET_KEY=sk-lf-xxxx
   export LANGFUSE_HOST=https://cloud.langfuse.com

Supported Providers
-------------------

Shepherd MCP supports multiple observability providers:

AIOBS (Shepherd)
^^^^^^^^^^^^^^^^

Native Shepherd observability backend. Provides deep insights into your AI agent 
sessions including LLM calls, function events, and evaluations.

**Environment Variables:**

- ``AIOBS_API_KEY`` (required) - Your Shepherd API key
- ``AIOBS_ENDPOINT`` (optional) - Custom API endpoint URL

Langfuse
^^^^^^^^

Open-source LLM observability platform. Supports traces, observations, sessions, 
and scores.

**Environment Variables:**

- ``LANGFUSE_PUBLIC_KEY`` (required) - Your Langfuse public API key
- ``LANGFUSE_SECRET_KEY`` (required) - Your Langfuse secret API key
- ``LANGFUSE_HOST`` (optional) - Custom Langfuse host URL

Integration
-----------

Claude Desktop
^^^^^^^^^^^^^^

Add to your ``claude_desktop_config.json``:

.. code-block:: json

   {
     "mcpServers": {
       "shepherd": {
         "command": "uvx",
         "args": ["shepherd-mcp"],
         "env": {
           "AIOBS_API_KEY": "aiobs_sk_xxxx",
           "LANGFUSE_PUBLIC_KEY": "pk-lf-xxxx",
           "LANGFUSE_SECRET_KEY": "sk-lf-xxxx"
         }
       }
     }
   }

Cursor
^^^^^^

Add to your ``.cursor/mcp.json``:

.. code-block:: json

   {
     "mcpServers": {
       "shepherd": {
         "command": "uvx",
         "args": ["shepherd-mcp"],
         "env": {
           "AIOBS_API_KEY": "aiobs_sk_xxxx",
           "LANGFUSE_PUBLIC_KEY": "pk-lf-xxxx",
           "LANGFUSE_SECRET_KEY": "sk-lf-xxxx"
         }
       }
     }
   }

.. toctree::
   :maxdepth: 2
   :caption: User Guide

   tools
   use-cases

.. toctree::
   :maxdepth: 2
   :caption: API Reference

   api/providers
   api/models

.. toctree::
   :maxdepth: 1
   :caption: Development

   development
   changelog

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

