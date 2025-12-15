Changelog
=========

All notable changes to Shepherd MCP will be documented in this file.

The format is based on `Keep a Changelog <https://keepachangelog.com/>`_, 
and this project adheres to `Semantic Versioning <https://semver.org/>`_.

[0.1.0] - 2024
--------------

Added
^^^^^

- Initial release of Shepherd MCP
- AIOBS (Shepherd) provider support

  - ``aiobs_list_sessions`` - List all sessions
  - ``aiobs_get_session`` - Get session details with trace tree
  - ``aiobs_search_sessions`` - Search and filter sessions
  - ``aiobs_diff_sessions`` - Compare two sessions

- Langfuse provider support

  - ``langfuse_list_traces`` - List traces with pagination
  - ``langfuse_get_trace`` - Get trace with observations
  - ``langfuse_list_sessions`` - List sessions
  - ``langfuse_get_session`` - Get session details
  - ``langfuse_list_observations`` - List observations
  - ``langfuse_get_observation`` - Get observation details
  - ``langfuse_list_scores`` - List scores/evaluations
  - ``langfuse_get_score`` - Get score details
  - ``langfuse_search_traces`` - Search traces with filters
  - ``langfuse_search_sessions`` - Search sessions with filters

- Automatic ``.env`` file loading
- Support for Claude Desktop and Cursor integration
- Comprehensive session diffing with system prompt comparison
- Legacy tool aliases for backwards compatibility

