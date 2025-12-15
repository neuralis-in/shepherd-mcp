Available Tools
===============

Shepherd MCP provides a comprehensive set of tools for querying and analyzing 
AI agent sessions. Tools are organized by provider.

.. contents:: On this page
   :local:
   :depth: 2

AIOBS (Shepherd) Tools
----------------------

These tools interact with the Shepherd/AIOBS observability backend.

aiobs_list_sessions
^^^^^^^^^^^^^^^^^^^

List all AI agent sessions from Shepherd. Returns session metadata, labels, 
and event counts.

**Parameters:**

.. list-table::
   :widths: 20 15 65
   :header-rows: 1

   * - Parameter
     - Type
     - Description
   * - ``limit``
     - integer
     - Maximum number of sessions to return (optional)

**Example prompt:**

   "List my recent AI agent sessions from AIOBS"

aiobs_get_session
^^^^^^^^^^^^^^^^^

Get detailed information about a specific AI agent session including the full 
trace tree, LLM calls, function events, and evaluations.

**Parameters:**

.. list-table::
   :widths: 20 15 65
   :header-rows: 1

   * - Parameter
     - Type
     - Description
   * - ``session_id``
     - string
     - The UUID of the session to retrieve (required)

**Example prompt:**

   "Get AIOBS session details for abc123-def456"

aiobs_search_sessions
^^^^^^^^^^^^^^^^^^^^^

Search and filter sessions with multiple criteria including text search, labels, 
provider, model, function name, date range, errors, and failed evaluations.

**Parameters:**

.. list-table::
   :widths: 20 15 65
   :header-rows: 1

   * - Parameter
     - Type
     - Description
   * - ``query``
     - string
     - Text search query (matches session name, ID, labels, metadata)
   * - ``labels``
     - object
     - Filter by labels as key-value pairs
   * - ``provider``
     - string
     - Filter by LLM provider (e.g., 'openai', 'anthropic')
   * - ``model``
     - string
     - Filter by model name (e.g., 'gpt-4o-mini', 'claude-3')
   * - ``function``
     - string
     - Filter by function name
   * - ``after``
     - string
     - Sessions started after this date (YYYY-MM-DD or ISO format)
   * - ``before``
     - string
     - Sessions started before this date (YYYY-MM-DD or ISO format)
   * - ``has_errors``
     - boolean
     - Only return sessions that have errors
   * - ``evals_failed``
     - boolean
     - Only return sessions with failed evaluations
   * - ``limit``
     - integer
     - Maximum number of sessions to return

**Example prompts:**

   "Find all AIOBS sessions that used OpenAI with errors"
   
   "Search for sessions from yesterday that failed evaluations"

aiobs_diff_sessions
^^^^^^^^^^^^^^^^^^^

Compare two sessions and show their differences including:

- **Metadata**: Duration, labels, timestamps
- **LLM calls**: Count, tokens (input/output/total), average latency, errors
- **Provider/Model distribution**: Which providers and models were used
- **Function events**: Total calls, unique functions, function-specific counts
- **Trace structure**: Trace depth, root nodes
- **Evaluations**: Pass/fail counts and rates
- **System prompts**: Compare system prompts across sessions
- **Request parameters**: Temperature, max_tokens, tools used
- **Response content**: Content length, tool calls, stop reasons

**Parameters:**

.. list-table::
   :widths: 20 15 65
   :header-rows: 1

   * - Parameter
     - Type
     - Description
   * - ``session_id_1``
     - string
     - First session UUID to compare (required)
   * - ``session_id_2``
     - string
     - Second session UUID to compare (required)

**Example prompt:**

   "Compare AIOBS sessions abc123 and def456"

Langfuse Tools
--------------

These tools interact with the Langfuse observability platform.

langfuse_list_traces
^^^^^^^^^^^^^^^^^^^^

List traces with pagination and filters. Traces represent complete workflows 
or conversations.

**Parameters:**

.. list-table::
   :widths: 20 15 65
   :header-rows: 1

   * - Parameter
     - Type
     - Description
   * - ``limit``
     - integer
     - Maximum results per page (default: 50)
   * - ``page``
     - integer
     - Page number (1-indexed)
   * - ``user_id``
     - string
     - Filter by user ID
   * - ``name``
     - string
     - Filter by trace name
   * - ``session_id``
     - string
     - Filter by session ID
   * - ``tags``
     - array
     - Filter by tags
   * - ``from_timestamp``
     - string
     - Filter after timestamp (ISO format or YYYY-MM-DD)
   * - ``to_timestamp``
     - string
     - Filter before timestamp (ISO format or YYYY-MM-DD)

**Example prompt:**

   "List the last 20 Langfuse traces"

langfuse_get_trace
^^^^^^^^^^^^^^^^^^

Get a specific trace with its observations (generations, spans, events).

**Parameters:**

.. list-table::
   :widths: 20 15 65
   :header-rows: 1

   * - Parameter
     - Type
     - Description
   * - ``trace_id``
     - string
     - The trace ID to fetch (required)

**Example prompt:**

   "Get Langfuse trace details for trace-id-123"

langfuse_list_sessions
^^^^^^^^^^^^^^^^^^^^^^

List sessions with pagination. Sessions group related traces together.

**Parameters:**

.. list-table::
   :widths: 20 15 65
   :header-rows: 1

   * - Parameter
     - Type
     - Description
   * - ``limit``
     - integer
     - Maximum results per page
   * - ``page``
     - integer
     - Page number
   * - ``from_timestamp``
     - string
     - Filter after timestamp
   * - ``to_timestamp``
     - string
     - Filter before timestamp

**Example prompt:**

   "Show me Langfuse sessions from the last week"

langfuse_get_session
^^^^^^^^^^^^^^^^^^^^

Get a specific session with its metrics and traces.

**Parameters:**

.. list-table::
   :widths: 20 15 65
   :header-rows: 1

   * - Parameter
     - Type
     - Description
   * - ``session_id``
     - string
     - The session ID to fetch (required)

**Example prompt:**

   "Get Langfuse session details for session-123"

langfuse_list_observations
^^^^^^^^^^^^^^^^^^^^^^^^^^

List observations (generations, spans, events) with filters.

**Parameters:**

.. list-table::
   :widths: 20 15 65
   :header-rows: 1

   * - Parameter
     - Type
     - Description
   * - ``limit``
     - integer
     - Maximum results per page
   * - ``page``
     - integer
     - Page number
   * - ``name``
     - string
     - Filter by observation name
   * - ``user_id``
     - string
     - Filter by user ID
   * - ``trace_id``
     - string
     - Filter by trace ID
   * - ``type``
     - string
     - Filter by type (GENERATION, SPAN, EVENT)
   * - ``from_timestamp``
     - string
     - Filter after timestamp
   * - ``to_timestamp``
     - string
     - Filter before timestamp

**Example prompt:**

   "List all GENERATION type observations from Langfuse"

langfuse_get_observation
^^^^^^^^^^^^^^^^^^^^^^^^

Get a specific observation with full details including input, output, usage, 
and costs.

**Parameters:**

.. list-table::
   :widths: 20 15 65
   :header-rows: 1

   * - Parameter
     - Type
     - Description
   * - ``observation_id``
     - string
     - The observation ID to fetch (required)

**Example prompt:**

   "Get details for Langfuse observation obs-123"

langfuse_list_scores
^^^^^^^^^^^^^^^^^^^^

List scores/evaluations with filters.

**Parameters:**

.. list-table::
   :widths: 20 15 65
   :header-rows: 1

   * - Parameter
     - Type
     - Description
   * - ``limit``
     - integer
     - Maximum results per page
   * - ``page``
     - integer
     - Page number
   * - ``name``
     - string
     - Filter by score name
   * - ``user_id``
     - string
     - Filter by user ID
   * - ``trace_id``
     - string
     - Filter by trace ID
   * - ``from_timestamp``
     - string
     - Filter after timestamp
   * - ``to_timestamp``
     - string
     - Filter before timestamp

**Example prompt:**

   "Show me Langfuse scores for trace trace-123"

langfuse_get_score
^^^^^^^^^^^^^^^^^^

Get a specific score/evaluation with full details.

**Parameters:**

.. list-table::
   :widths: 20 15 65
   :header-rows: 1

   * - Parameter
     - Type
     - Description
   * - ``score_id``
     - string
     - The score ID to fetch (required)

**Example prompt:**

   "Get Langfuse score details for score-123"

langfuse_search_traces
^^^^^^^^^^^^^^^^^^^^^^

Search and filter traces with extended criteria including text search, release, 
cost range, and latency range.

**Parameters:**

.. list-table::
   :widths: 20 15 65
   :header-rows: 1

   * - Parameter
     - Type
     - Description
   * - ``query``
     - string
     - Text search (matches trace name, ID, user ID, session ID, tags)
   * - ``name``
     - string
     - Filter by trace name
   * - ``user_id``
     - string
     - Filter by user ID
   * - ``session_id``
     - string
     - Filter by session ID
   * - ``tags``
     - array
     - Filter by tags
   * - ``release``
     - string
     - Filter by release
   * - ``min_cost``
     - number
     - Minimum total cost
   * - ``max_cost``
     - number
     - Maximum total cost
   * - ``min_latency``
     - number
     - Minimum latency in seconds
   * - ``max_latency``
     - number
     - Maximum latency in seconds
   * - ``from_timestamp``
     - string
     - Filter after timestamp
   * - ``to_timestamp``
     - string
     - Filter before timestamp
   * - ``limit``
     - integer
     - Maximum results
   * - ``page``
     - integer
     - Page number

langfuse_search_sessions
^^^^^^^^^^^^^^^^^^^^^^^^

Search and filter sessions with extended criteria including text search, user ID, 
trace count range, and cost range.

**Parameters:**

.. list-table::
   :widths: 20 15 65
   :header-rows: 1

   * - Parameter
     - Type
     - Description
   * - ``query``
     - string
     - Text search (matches session ID or user IDs)
   * - ``user_id``
     - string
     - Filter by user ID
   * - ``min_traces``
     - integer
     - Minimum number of traces
   * - ``max_traces``
     - integer
     - Maximum number of traces
   * - ``min_cost``
     - number
     - Minimum total cost
   * - ``max_cost``
     - number
     - Maximum total cost
   * - ``from_timestamp``
     - string
     - Filter after timestamp
   * - ``to_timestamp``
     - string
     - Filter before timestamp
   * - ``limit``
     - integer
     - Maximum results
   * - ``page``
     - integer
     - Page number

Legacy Tools (Deprecated)
-------------------------

For backwards compatibility, the following tools are still available but will 
be removed in a future version:

.. list-table::
   :widths: 30 70
   :header-rows: 1

   * - Legacy Tool
     - Replacement
   * - ``list_sessions``
     - ``aiobs_list_sessions``
   * - ``get_session``
     - ``aiobs_get_session``
   * - ``search_sessions``
     - ``aiobs_search_sessions``
   * - ``diff_sessions``
     - ``aiobs_diff_sessions``

