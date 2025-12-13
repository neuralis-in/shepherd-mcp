# 🐑 Shepherd MCP

MCP (Model Context Protocol) server for Shepherd - Debug your AI agents like you debug your code.

This MCP server allows AI assistants (Claude, Cursor, etc.) to query and analyze your AI agent sessions directly.

## Installation

```bash
pip install shepherd-mcp
```

Or run directly with uvx:

```bash
uvx shepherd-mcp
```

## Configuration

### Environment Variables

- `AIOBS_API_KEY` (required) - Your Shepherd API key
- `AIOBS_ENDPOINT` (optional) - Custom API endpoint URL

### .env File Support

shepherd-mcp automatically loads `.env` files from the current directory or any parent directory. This means if you have a `.env` file in your project root:

```bash
# .env
AIOBS_API_KEY=aiobs_sk_xxxx
```

It will be automatically loaded when the MCP server starts.

### Claude Desktop

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "shepherd": {
      "command": "uvx",
      "args": ["shepherd-mcp"],
      "env": {
        "AIOBS_API_KEY": "aiobs_sk_xxxx"
      }
    }
  }
}
```

### Cursor

Add to your `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "shepherd": {
      "command": "uvx",
      "args": ["shepherd-mcp"],
      "env": {
        "AIOBS_API_KEY": "aiobs_sk_xxxx"
      }
    }
  }
}
```

Or if installed via pip:

```json
{
  "mcpServers": {
    "shepherd": {
      "command": "shepherd-mcp",
      "env": {
        "AIOBS_API_KEY": "aiobs_sk_xxxx"
      }
    }
  }
}
```

## Available Tools

### `list_sessions`

List all AI agent sessions from Shepherd.

**Parameters:**
- `limit` (optional): Maximum number of sessions to return

**Example prompt:**
> "List my recent AI agent sessions"

### `get_session`

Get detailed information about a specific session including the full trace tree, LLM calls, function events, and evaluations.

**Parameters:**
- `session_id` (required): The UUID of the session to retrieve

**Example prompt:**
> "Get details for session abc123-def456"

### `search_sessions`

Search and filter sessions with multiple criteria.

**Parameters:**
- `query` (optional): Text search (matches name, ID, labels, metadata)
- `labels` (optional): Filter by labels as key-value pairs
- `provider` (optional): Filter by LLM provider (e.g., 'openai', 'anthropic')
- `model` (optional): Filter by model name (e.g., 'gpt-4o-mini', 'claude-3')
- `function` (optional): Filter by function name
- `after` (optional): Sessions started after date (YYYY-MM-DD)
- `before` (optional): Sessions started before date (YYYY-MM-DD)
- `has_errors` (optional): Only return sessions with errors
- `evals_failed` (optional): Only return sessions with failed evaluations
- `limit` (optional): Maximum number of sessions to return

**Example prompts:**
> "Find all sessions that used OpenAI with errors"
> "Search for sessions from yesterday that failed evaluations"
> "Find sessions using gpt-4o-mini model"

### `diff_sessions`

Compare two sessions and show their differences including:
- **Metadata**: Duration, labels, timestamps
- **LLM calls**: Count, tokens (input/output/total), average latency, errors
- **Provider/Model distribution**: Which providers and models were used
- **Function events**: Total calls, unique functions, function-specific counts
- **Trace structure**: Trace depth, root nodes
- **Evaluations**: Pass/fail counts and rates
- **System prompts**: Compare system prompts across sessions, identify unique and common prompts
- **Request parameters**: Temperature, max_tokens, tools used, streaming requests
- **Response content**: Content length, tool calls, stop reasons

**Parameters:**
- `session_id_1` (required): First session UUID to compare
- `session_id_2` (required): Second session UUID to compare

**Example prompts:**
> "Compare sessions abc123 and def456 and tell me what changed"
> "Did the system prompt change between these two sessions?"
> "Compare the request parameters between session abc and def"

## Use Cases

### 1. Debugging Failed Runs

> "Show me all sessions that had errors in the last 24 hours"

### 2. Performance Analysis

> "Compare session abc123 with session def456 and tell me which one was more efficient"

### 3. Prompt Regression Detection

> "Find sessions using gpt-4 with failed evaluations"

### 4. Cost Tracking

> "List all sessions and summarize the total token usage"

### 5. Session Inspection

> "Get the full trace tree for the most recent session and explain what happened"

## Development

### Setup

```bash
git clone https://github.com/neuralis/shepherd-mcp
cd shepherd-mcp
python -m venv venv
source venv/bin/activate
pip install -e ".[dev]"
```

### Running Tests

```bash
pytest
```

### Running Locally

```bash
export AIOBS_API_KEY=aiobs_sk_xxxx
python -m shepherd_mcp
```

## Architecture

```
┌─────────────────┐     stdio      ┌─────────────────┐
│  Cursor/Claude  │ ◄────────────► │  shepherd-mcp   │
│    (Client)     │   stdin/stdout │   (subprocess)  │
└─────────────────┘                └────────┬────────┘
                                            │ HTTPS
                                            ▼
                                   ┌─────────────────┐
                                   │  Shepherd API   │
                                   │  (Cloud hosted) │
                                   └─────────────────┘
```

## License

MIT

