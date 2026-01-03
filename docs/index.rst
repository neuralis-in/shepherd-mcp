Shepherd MCP
============

**Debug your AI agents like you debug your code.**

Shepherd MCP is a Model Context Protocol (MCP) server that allows AI assistants 
(Claude, Cursor, etc.) to query and analyze your AI agent sessions from multiple 
observability providers.

----

Quick Start
-----------

Installation
^^^^^^^^^^^^

Install via pip:

.. code-block:: bash

   pip install shepherd-mcp

Or run directly with uvx (no installation required):

.. code-block:: bash

   uvx shepherd-mcp

Configuration
^^^^^^^^^^^^^

Set your environment variables based on your observability provider:

.. tab-set::

   .. tab-item:: AIOBS (Shepherd)

      .. code-block:: bash

         export AIOBS_API_KEY=aiobs_sk_xxxx

   .. tab-item:: Langfuse

      .. code-block:: bash

         export LANGFUSE_PUBLIC_KEY=pk-lf-xxxx
         export LANGFUSE_SECRET_KEY=sk-lf-xxxx
         export LANGFUSE_HOST=https://cloud.langfuse.com

Supported Providers
-------------------

Shepherd MCP supports multiple observability providers:

.. list-table::
   :header-rows: 1
   :widths: 20 50 30

   * - Provider
     - Description
     - Status
   * - **AIOBS (Shepherd)**
     - Native Shepherd observability backend with deep insights
     - ✅ Full Support
   * - **Langfuse**
     - Open-source LLM observability platform
     - ✅ Full Support

AIOBS (Shepherd)
^^^^^^^^^^^^^^^^

Native Shepherd observability backend. Provides deep insights into your AI agent 
sessions including LLM calls, function events, and evaluations.

**Required Environment Variables:**

- ``AIOBS_API_KEY`` — Your Shepherd API key

**Optional Environment Variables:**

- ``AIOBS_ENDPOINT`` — Custom API endpoint URL

Langfuse
^^^^^^^^

Open-source LLM observability platform. Supports traces, observations, sessions, 
and scores.

**Required Environment Variables:**

- ``LANGFUSE_PUBLIC_KEY`` — Your Langfuse public API key
- ``LANGFUSE_SECRET_KEY`` — Your Langfuse secret API key

**Optional Environment Variables:**

- ``LANGFUSE_HOST`` — Custom Langfuse host URL (defaults to cloud.langfuse.com)

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

----

.. toctree::
   :maxdepth: 2
   :caption: 📖 User Guide
   :hidden:

   tools
   use-cases

.. toctree::
   :maxdepth: 2
   :caption: 📚 API Reference
   :hidden:

   api/providers
   api/models

.. toctree::
   :maxdepth: 1
   :caption: 🛠️ Development
   :hidden:

   development
   changelog

.. grid:: 2
   :gutter: 3

   .. grid-item-card:: 📖 User Guide
      :link: tools
      :link-type: doc

      Learn about available MCP tools and how to use them effectively.

   .. grid-item-card:: 💡 Use Cases
      :link: use-cases
      :link-type: doc

      Explore real-world examples and debugging workflows.

   .. grid-item-card:: 📚 API Reference
      :link: api/providers
      :link-type: doc

      Detailed documentation of providers, models, and interfaces.

   .. grid-item-card:: 🛠️ Development
      :link: development
      :link-type: doc

      Contributing guidelines and development setup.

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
