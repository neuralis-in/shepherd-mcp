"""Shepherd MCP Server - Debug your AI agents like you debug your code."""

from __future__ import annotations

import json
from datetime import datetime
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool

from shepherd_mcp.client import (
    AIOBSClient,
    AIOBSError,
    AuthenticationError,
    SessionNotFoundError,
    filter_sessions,
    parse_date,
)
from shepherd_mcp.models import Event, FunctionEvent, SessionsResponse, TraceNode

# Create the MCP server
server = Server("shepherd-mcp")


# ============================================================================
# Helper functions
# ============================================================================


def format_timestamp(ts: float) -> str:
    """Format a Unix timestamp to ISO format string."""
    return datetime.fromtimestamp(ts).isoformat()


def format_duration(ms: float) -> str:
    """Format duration in milliseconds to human-readable string."""
    if ms < 1000:
        return f"{ms:.0f}ms"
    elif ms < 60000:
        return f"{ms / 1000:.1f}s"
    else:
        return f"{ms / 60000:.1f}m"


def session_to_dict(session: Any, events: list[Event], function_events: list[FunctionEvent]) -> dict:
    """Convert a session to a dictionary with computed fields."""
    # Count events for this session
    event_count = sum(1 for e in events if e.session_id == session.id)
    fn_event_count = sum(1 for e in function_events if e.session_id == session.id)

    # Calculate duration
    duration_ms = None
    if session.ended_at and session.started_at:
        duration_ms = (session.ended_at - session.started_at) * 1000

    return {
        "id": session.id,
        "name": session.name,
        "started_at": format_timestamp(session.started_at),
        "ended_at": format_timestamp(session.ended_at) if session.ended_at else None,
        "duration_ms": duration_ms,
        "duration": format_duration(duration_ms) if duration_ms else None,
        "llm_call_count": event_count,
        "function_call_count": fn_event_count,
        "total_event_count": event_count + fn_event_count,
        "labels": dict(session.labels),
        "meta": dict(session.meta),
    }


def calc_total_tokens(events: list[Event]) -> dict[str, int]:
    """Calculate total tokens from events."""
    total = {"input": 0, "output": 0, "total": 0}
    for event in events:
        if event.response and "usage" in event.response:
            usage = event.response["usage"]
            total["input"] += usage.get("prompt_tokens", 0) or usage.get("input_tokens", 0)
            total["output"] += usage.get("completion_tokens", 0) or usage.get("output_tokens", 0)
            total["total"] += usage.get("total_tokens", 0)
    return total


def calc_avg_latency(events: list[Event]) -> float:
    """Calculate average latency from events."""
    if not events:
        return 0.0
    return sum(e.duration_ms for e in events) / len(events)


def count_errors(events: list[Event], function_events: list[FunctionEvent]) -> int:
    """Count errors in events."""
    count = sum(1 for e in events if e.error)
    count += sum(1 for e in function_events if e.error)
    return count


def get_provider_distribution(events: list[Event]) -> dict[str, int]:
    """Get provider distribution from events."""
    dist: dict[str, int] = {}
    for event in events:
        dist[event.provider] = dist.get(event.provider, 0) + 1
    return dist


def get_model_distribution(events: list[Event]) -> dict[str, int]:
    """Get model distribution from events."""
    dist: dict[str, int] = {}
    for event in events:
        if event.request:
            model = event.request.get("model", "unknown")
            dist[model] = dist.get(model, 0) + 1
    return dist


def trace_node_to_dict(node: TraceNode) -> dict:
    """Convert a trace node to a simplified dictionary."""
    result = {
        "type": node.event_type or ("function" if node.name else "provider"),
        "provider": node.provider,
        "api": node.api,
        "duration_ms": node.duration_ms,
        "duration": format_duration(node.duration_ms),
        "span_id": node.span_id,
    }

    if node.name:
        result["function_name"] = node.name
        result["module"] = node.module

    if node.request and "model" in node.request:
        result["model"] = node.request["model"]

    if node.error:
        result["error"] = node.error

    if node.evaluations:
        result["evaluations"] = [
            {
                "type": e.get("eval_type"),
                "passed": e.get("passed"),
                "score": e.get("score"),
                "feedback": e.get("feedback"),
            }
            for e in node.evaluations
        ]

    if node.children:
        result["children"] = [trace_node_to_dict(child) for child in node.children]

    return result


# ============================================================================
# Diff calculation (ported from shepherd-cli)
# ============================================================================


def eval_is_failed(evaluation: dict) -> bool:
    """Check if an evaluation result indicates failure."""
    if not isinstance(evaluation, dict):
        return False
    if evaluation.get("passed") is False:
        return True
    if evaluation.get("result") is False:
        return True
    if str(evaluation.get("status", "")).lower() in ("failed", "fail", "error"):
        return True
    return evaluation.get("success") is False


def count_evaluations(events: list[Event], function_events: list[FunctionEvent]) -> dict[str, int]:
    """Count evaluation results."""
    result = {"total": 0, "passed": 0, "failed": 0}
    all_evals = []
    for event in events:
        all_evals.extend(event.evaluations)
    for event in function_events:
        all_evals.extend(event.evaluations)

    result["total"] = len(all_evals)
    for ev in all_evals:
        if eval_is_failed(ev):
            result["failed"] += 1
        else:
            result["passed"] += 1
    return result


def get_trace_depth(nodes: list[TraceNode]) -> int:
    """Get maximum trace depth."""
    if not nodes:
        return 0

    def _depth(node: TraceNode) -> int:
        if not node.children:
            return 1
        return 1 + max(_depth(c) for c in node.children)

    return max(_depth(n) for n in nodes)


def get_errors_list(events: list[Event], function_events: list[FunctionEvent]) -> list[str]:
    """Get list of error messages."""
    errors = []
    for event in events:
        if event.error:
            errors.append(f"[{event.provider}/{event.api}] {event.error}")
    for event in function_events:
        if event.error:
            errors.append(f"[fn:{event.name}] {event.error}")
    return errors


def get_function_counts(function_events: list[FunctionEvent]) -> dict[str, int]:
    """Get function call counts."""
    counts: dict[str, int] = {}
    for event in function_events:
        if event.name:
            counts[event.name] = counts.get(event.name, 0) + 1
    return counts


def extract_system_prompts(events: list[Event]) -> list[dict]:
    """Extract system prompts from events."""
    prompts = []
    for i, event in enumerate(events):
        if not event.request:
            continue
        messages = event.request.get("messages", [])
        system_content = None

        # Check for system message in messages array
        for msg in messages:
            if isinstance(msg, dict) and msg.get("role") == "system":
                content = msg.get("content", "")
                if isinstance(content, list):
                    # Handle content blocks (e.g., Anthropic format)
                    content = " ".join(
                        block.get("text", "") for block in content if isinstance(block, dict)
                    )
                system_content = content
                break

        # Check for top-level system parameter (Anthropic style)
        if not system_content:
            system_content = event.request.get("system", "")

        if system_content:
            prompts.append(
                {
                    "index": i,
                    "provider": event.provider,
                    "model": event.request.get("model", "unknown"),
                    "content": system_content[:500] + "..."
                    if len(system_content) > 500
                    else system_content,
                    "full_length": len(system_content),
                }
            )
    return prompts


def compare_system_prompts(prompts1: list[dict], prompts2: list[dict]) -> dict:
    """Compare system prompts between sessions."""
    # Get unique prompts by content
    set1 = {p["content"] for p in prompts1}
    set2 = {p["content"] for p in prompts2}

    return {
        "session1": prompts1,
        "session2": prompts2,
        "unique_to_session1": list(set1 - set2),
        "unique_to_session2": list(set2 - set1),
        "common": list(set1 & set2),
        "changed": len(set1) != len(set2) or set1 != set2,
    }


def extract_request_params(events: list[Event]) -> list[dict]:
    """Extract request parameters from events."""
    params_list = []
    for i, event in enumerate(events):
        if not event.request:
            continue

        params = {
            "index": i,
            "provider": event.provider,
            "api": event.api,
            "model": event.request.get("model", "unknown"),
        }

        # Common parameters across providers
        param_keys = [
            "temperature",
            "max_tokens",
            "top_p",
            "top_k",
            "frequency_penalty",
            "presence_penalty",
            "stop",
            "stream",
            "tools",
            "tool_choice",
            "response_format",
        ]

        for key in param_keys:
            if key in event.request:
                value = event.request[key]
                # Summarize tools if present
                if key == "tools" and isinstance(value, list):
                    params[key] = [
                        t.get("function", {}).get("name", "unknown")
                        if isinstance(t, dict)
                        else str(t)
                        for t in value
                    ]
                else:
                    params[key] = value

        # Extract user message preview
        messages = event.request.get("messages", [])
        user_msgs = [m for m in messages if isinstance(m, dict) and m.get("role") == "user"]
        if user_msgs:
            last_user = user_msgs[-1]
            content = last_user.get("content", "")
            if isinstance(content, list):
                content = " ".join(
                    block.get("text", "")
                    for block in content
                    if isinstance(block, dict) and block.get("type") == "text"
                )
            params["user_message_preview"] = (
                content[:200] + "..." if len(str(content)) > 200 else content
            )

        params_list.append(params)
    return params_list


def compare_request_params(params1: list[dict], params2: list[dict]) -> dict:
    """Compare request parameters between sessions."""

    def aggregate_params(params_list: list[dict]) -> dict:
        agg: dict = {
            "temperatures": [],
            "max_tokens": [],
            "models": [],
            "tools_used": set(),
            "stream_count": 0,
        }
        for p in params_list:
            if "temperature" in p:
                agg["temperatures"].append(p["temperature"])
            if "max_tokens" in p:
                agg["max_tokens"].append(p["max_tokens"])
            agg["models"].append(p.get("model", "unknown"))
            if "tools" in p:
                agg["tools_used"].update(p["tools"])
            if p.get("stream"):
                agg["stream_count"] += 1
        agg["tools_used"] = list(agg["tools_used"])
        return agg

    agg1 = aggregate_params(params1)
    agg2 = aggregate_params(params2)

    return {
        "session1": {
            "requests": params1,
            "summary": {
                "avg_temperature": sum(agg1["temperatures"]) / len(agg1["temperatures"])
                if agg1["temperatures"]
                else None,
                "avg_max_tokens": sum(agg1["max_tokens"]) / len(agg1["max_tokens"])
                if agg1["max_tokens"]
                else None,
                "tools_used": agg1["tools_used"],
                "streaming_requests": agg1["stream_count"],
            },
        },
        "session2": {
            "requests": params2,
            "summary": {
                "avg_temperature": sum(agg2["temperatures"]) / len(agg2["temperatures"])
                if agg2["temperatures"]
                else None,
                "avg_max_tokens": sum(agg2["max_tokens"]) / len(agg2["max_tokens"])
                if agg2["max_tokens"]
                else None,
                "tools_used": agg2["tools_used"],
                "streaming_requests": agg2["stream_count"],
            },
        },
        "tools_added": list(set(agg2["tools_used"]) - set(agg1["tools_used"])),
        "tools_removed": list(set(agg1["tools_used"]) - set(agg2["tools_used"])),
    }


def extract_responses(events: list[Event]) -> list[dict]:
    """Extract response content from events."""
    responses = []
    for i, event in enumerate(events):
        if not event.response:
            continue

        model = event.response.get("model")
        if not model and event.request:
            model = event.request.get("model", "unknown")
        resp = {
            "index": i,
            "provider": event.provider,
            "model": model or "unknown",
            "duration_ms": event.duration_ms,
        }

        # Extract usage info
        usage = event.response.get("usage", {})
        if usage:
            resp["tokens"] = {
                "input": usage.get("prompt_tokens") or usage.get("input_tokens", 0),
                "output": usage.get("completion_tokens") or usage.get("output_tokens", 0),
                "total": usage.get("total_tokens", 0),
            }

        # Extract response content - handle different formats
        content = None

        # OpenAI format
        choices = event.response.get("choices", [])
        if choices and isinstance(choices, list):
            first_choice = choices[0]
            if isinstance(first_choice, dict):
                message = first_choice.get("message", {})
                content = message.get("content", "")
                # Check for tool calls
                tool_calls = message.get("tool_calls", [])
                if tool_calls:
                    resp["tool_calls"] = [
                        {
                            "name": tc.get("function", {}).get("name", "unknown"),
                            "arguments_preview": str(
                                tc.get("function", {}).get("arguments", "")
                            )[:100],
                        }
                        for tc in tool_calls
                        if isinstance(tc, dict)
                    ]

        # Anthropic format
        if not content:
            content_blocks = event.response.get("content", [])
            if isinstance(content_blocks, list):
                text_blocks = [
                    b.get("text", "")
                    for b in content_blocks
                    if isinstance(b, dict) and b.get("type") == "text"
                ]
                content = " ".join(text_blocks)
                # Check for tool use
                tool_uses = [
                    b
                    for b in content_blocks
                    if isinstance(b, dict) and b.get("type") == "tool_use"
                ]
                if tool_uses:
                    resp["tool_calls"] = [
                        {
                            "name": tu.get("name", "unknown"),
                            "arguments_preview": str(tu.get("input", ""))[:100],
                        }
                        for tu in tool_uses
                    ]
            elif isinstance(content_blocks, str):
                content = content_blocks

        # Direct text field
        if not content:
            content = event.response.get("text", "")

        if content:
            resp["content_preview"] = (
                content[:300] + "..." if len(str(content)) > 300 else content
            )
            resp["content_length"] = len(str(content))

        # Stop reason
        stop_reason = event.response.get("stop_reason") or (
            choices[0].get("finish_reason") if choices else None
        )
        if stop_reason:
            resp["stop_reason"] = stop_reason

        responses.append(resp)
    return responses


def compare_responses(responses1: list[dict], responses2: list[dict]) -> dict:
    """Compare responses between sessions."""

    def summarize_responses(resp_list: list[dict]) -> dict:
        total_content_len = 0
        tool_call_count = 0
        stop_reasons: dict[str, int] = {}

        for r in resp_list:
            total_content_len += r.get("content_length", 0)
            tool_call_count += len(r.get("tool_calls", []))
            reason = r.get("stop_reason", "unknown")
            stop_reasons[reason] = stop_reasons.get(reason, 0) + 1

        return {
            "total_content_length": total_content_len,
            "avg_content_length": total_content_len / len(resp_list) if resp_list else 0,
            "tool_call_count": tool_call_count,
            "stop_reasons": stop_reasons,
        }

    summary1 = summarize_responses(responses1)
    summary2 = summarize_responses(responses2)

    return {
        "session1": {
            "responses": responses1,
            "summary": summary1,
        },
        "session2": {
            "responses": responses2,
            "summary": summary2,
        },
        "delta": {
            "avg_content_length": (
                summary2["avg_content_length"] - summary1["avg_content_length"]
            ),
            "tool_call_count": (summary2["tool_call_count"] - summary1["tool_call_count"]),
        },
    }


def compute_session_diff(session1: SessionsResponse, session2: SessionsResponse) -> dict:
    """Compute the diff between two sessions."""
    s1 = session1.sessions[0] if session1.sessions else None
    s2 = session2.sessions[0] if session2.sessions else None

    if not s1 or not s2:
        return {"error": "One or both sessions not found"}

    # Session metadata
    s1_duration = (s1.ended_at - s1.started_at) * 1000 if s1.ended_at and s1.started_at else 0
    s2_duration = (s2.ended_at - s2.started_at) * 1000 if s2.ended_at and s2.started_at else 0

    # Labels diff
    s1_labels = set(s1.labels.items())
    s2_labels = set(s2.labels.items())
    labels_added = dict(s2_labels - s1_labels)
    labels_removed = dict(s1_labels - s2_labels)

    # Token calculations
    tokens1 = calc_total_tokens(session1.events)
    tokens2 = calc_total_tokens(session2.events)

    # Latency
    avg_latency1 = calc_avg_latency(session1.events)
    avg_latency2 = calc_avg_latency(session2.events)

    # Errors
    errors1 = count_errors(session1.events, session1.function_events)
    errors2 = count_errors(session2.events, session2.function_events)

    # Provider/model distribution
    providers1 = get_provider_distribution(session1.events)
    providers2 = get_provider_distribution(session2.events)
    models1 = get_model_distribution(session1.events)
    models2 = get_model_distribution(session2.events)

    # Function events
    fn_counts1 = get_function_counts(session1.function_events)
    fn_counts2 = get_function_counts(session2.function_events)
    fns1 = set(fn_counts1.keys())
    fns2 = set(fn_counts2.keys())

    # Evaluations
    evals1 = count_evaluations(session1.events, session1.function_events)
    evals2 = count_evaluations(session2.events, session2.function_events)

    # Trace depth
    trace_depth1 = get_trace_depth(session1.trace_tree)
    trace_depth2 = get_trace_depth(session2.trace_tree)

    # Errors list
    errors_list1 = get_errors_list(session1.events, session1.function_events)
    errors_list2 = get_errors_list(session2.events, session2.function_events)

    # System prompts comparison
    system_prompts1 = extract_system_prompts(session1.events)
    system_prompts2 = extract_system_prompts(session2.events)
    system_prompts_comparison = compare_system_prompts(system_prompts1, system_prompts2)

    # Request parameters comparison
    request_params1 = extract_request_params(session1.events)
    request_params2 = extract_request_params(session2.events)
    request_params_comparison = compare_request_params(request_params1, request_params2)

    # Responses comparison
    responses1 = extract_responses(session1.events)
    responses2 = extract_responses(session2.events)
    responses_comparison = compare_responses(responses1, responses2)

    return {
        "metadata": {
            "session1": {
                "id": s1.id,
                "name": s1.name,
                "started_at": format_timestamp(s1.started_at),
                "duration_ms": s1_duration,
                "duration": format_duration(s1_duration),
            },
            "session2": {
                "id": s2.id,
                "name": s2.name,
                "started_at": format_timestamp(s2.started_at),
                "duration_ms": s2_duration,
                "duration": format_duration(s2_duration),
            },
            "duration_delta_ms": s2_duration - s1_duration,
            "labels_added": labels_added,
            "labels_removed": labels_removed,
        },
        "llm_calls": {
            "session1": {
                "total": len(session1.events),
                "tokens": tokens1,
                "avg_latency_ms": round(avg_latency1, 2),
                "errors": errors1,
            },
            "session2": {
                "total": len(session2.events),
                "tokens": tokens2,
                "avg_latency_ms": round(avg_latency2, 2),
                "errors": errors2,
            },
            "delta": {
                "total": len(session2.events) - len(session1.events),
                "tokens": {
                    "input": tokens2["input"] - tokens1["input"],
                    "output": tokens2["output"] - tokens1["output"],
                    "total": tokens2["total"] - tokens1["total"],
                },
                "avg_latency_ms": round(avg_latency2 - avg_latency1, 2),
                "errors": errors2 - errors1,
            },
        },
        "providers": {"session1": providers1, "session2": providers2},
        "models": {"session1": models1, "session2": models2},
        "functions": {
            "session1": {
                "total": len(session1.function_events),
                "unique": len(fns1),
                "counts": fn_counts1,
            },
            "session2": {
                "total": len(session2.function_events),
                "unique": len(fns2),
                "counts": fn_counts2,
            },
            "only_in_session1": list(fns1 - fns2),
            "only_in_session2": list(fns2 - fns1),
            "in_both": list(fns1 & fns2),
        },
        "trace": {
            "session1": {"depth": trace_depth1, "root_nodes": len(session1.trace_tree)},
            "session2": {"depth": trace_depth2, "root_nodes": len(session2.trace_tree)},
        },
        "evaluations": {
            "session1": evals1,
            "session2": evals2,
            "delta": {
                "total": evals2["total"] - evals1["total"],
                "passed": evals2["passed"] - evals1["passed"],
                "failed": evals2["failed"] - evals1["failed"],
            },
            "pass_rate1": evals1["passed"] / evals1["total"] if evals1["total"] > 0 else 0,
            "pass_rate2": evals2["passed"] / evals2["total"] if evals2["total"] > 0 else 0,
        },
        "errors": {"session1": errors_list1, "session2": errors_list2},
        "system_prompts": system_prompts_comparison,
        "request_params": request_params_comparison,
        "responses": responses_comparison,
    }


# ============================================================================
# MCP Tool Handlers
# ============================================================================


@server.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools."""
    return [
        Tool(
            name="list_sessions",
            description="List all AI agent sessions from Shepherd. Returns session metadata, labels, and event counts.",
            inputSchema={
                "type": "object",
                "properties": {
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of sessions to return",
                    },
                },
            },
        ),
        Tool(
            name="get_session",
            description="Get detailed information about a specific AI agent session including the full trace tree, LLM calls, function events, and evaluations.",
            inputSchema={
                "type": "object",
                "properties": {
                    "session_id": {
                        "type": "string",
                        "description": "The UUID of the session to retrieve",
                    },
                },
                "required": ["session_id"],
            },
        ),
        Tool(
            name="search_sessions",
            description="Search and filter AI agent sessions with multiple criteria including text search, labels, provider, model, function name, date range, errors, and failed evaluations.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Text search query (matches session name, ID, labels, metadata)",
                    },
                    "labels": {
                        "type": "object",
                        "additionalProperties": {"type": "string"},
                        "description": "Filter by labels as key-value pairs (e.g., {\"environment\": \"production\"})",
                    },
                    "provider": {
                        "type": "string",
                        "description": "Filter by LLM provider (e.g., 'openai', 'anthropic')",
                    },
                    "model": {
                        "type": "string",
                        "description": "Filter by model name (e.g., 'gpt-4o-mini', 'claude-3')",
                    },
                    "function": {
                        "type": "string",
                        "description": "Filter by function name",
                    },
                    "after": {
                        "type": "string",
                        "description": "Sessions started after this date (YYYY-MM-DD or ISO format)",
                    },
                    "before": {
                        "type": "string",
                        "description": "Sessions started before this date (YYYY-MM-DD or ISO format)",
                    },
                    "has_errors": {
                        "type": "boolean",
                        "description": "Only return sessions that have errors",
                    },
                    "evals_failed": {
                        "type": "boolean",
                        "description": "Only return sessions with failed evaluations",
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of sessions to return",
                    },
                },
            },
        ),
        Tool(
            name="diff_sessions",
            description="Compare two AI agent sessions and show their differences including metadata, LLM calls, tokens, latency, providers, models, functions, evaluations, errors, system prompts, request parameters, and response content.",
            inputSchema={
                "type": "object",
                "properties": {
                    "session_id_1": {
                        "type": "string",
                        "description": "First session UUID to compare",
                    },
                    "session_id_2": {
                        "type": "string",
                        "description": "Second session UUID to compare",
                    },
                },
                "required": ["session_id_1", "session_id_2"],
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    """Handle tool calls."""
    try:
        if name == "list_sessions":
            return await handle_list_sessions(arguments)
        elif name == "get_session":
            return await handle_get_session(arguments)
        elif name == "search_sessions":
            return await handle_search_sessions(arguments)
        elif name == "diff_sessions":
            return await handle_diff_sessions(arguments)
        else:
            return [TextContent(type="text", text=f"Unknown tool: {name}")]
    except AuthenticationError as e:
        return [TextContent(type="text", text=f"Authentication error: {e}\n\nMake sure AIOBS_API_KEY environment variable is set.")]
    except SessionNotFoundError as e:
        return [TextContent(type="text", text=f"Session not found: {e}")]
    except AIOBSError as e:
        return [TextContent(type="text", text=f"API error: {e}")]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {e}")]


async def handle_list_sessions(arguments: dict[str, Any]) -> list[TextContent]:
    """Handle list_sessions tool call."""
    limit = arguments.get("limit")

    with AIOBSClient() as client:
        response = client.list_sessions()

    sessions = response.sessions
    if limit:
        sessions = sessions[:limit]

    result = {
        "sessions": [
            session_to_dict(s, response.events, response.function_events)
            for s in sessions
        ],
        "total": len(response.sessions),
        "returned": len(sessions),
    }

    return [TextContent(type="text", text=json.dumps(result, indent=2))]


async def handle_get_session(arguments: dict[str, Any]) -> list[TextContent]:
    """Handle get_session tool call."""
    session_id = arguments.get("session_id")
    if not session_id:
        return [TextContent(type="text", text="Error: session_id is required")]

    with AIOBSClient() as client:
        response = client.get_session(session_id)

    if not response.sessions:
        return [TextContent(type="text", text=f"Session not found: {session_id}")]

    session = response.sessions[0]

    # Build summary
    tokens = calc_total_tokens(response.events)
    providers = get_provider_distribution(response.events)
    models = get_model_distribution(response.events)
    evals = count_evaluations(response.events, response.function_events)
    errors = count_errors(response.events, response.function_events)

    result = {
        "session": session_to_dict(session, response.events, response.function_events),
        "summary": {
            "total_llm_calls": len(response.events),
            "total_function_calls": len(response.function_events),
            "total_tokens": tokens,
            "avg_latency_ms": round(calc_avg_latency(response.events), 2),
            "providers_used": list(providers.keys()),
            "models_used": list(models.keys()),
            "provider_distribution": providers,
            "model_distribution": models,
            "evaluations": evals,
            "errors": errors,
        },
        "trace_tree": [trace_node_to_dict(node) for node in response.trace_tree],
        "llm_calls": [
            {
                "provider": e.provider,
                "api": e.api,
                "model": e.request.get("model") if e.request else None,
                "duration_ms": e.duration_ms,
                "tokens": e.response.get("usage") if e.response else None,
                "error": e.error,
                "evaluations": [
                    {"type": ev.get("eval_type"), "passed": ev.get("passed"), "score": ev.get("score")}
                    for ev in e.evaluations
                ],
            }
            for e in response.events[:50]  # Limit to first 50 for readability
        ],
        "function_calls": [
            {
                "name": e.name,
                "module": e.module,
                "duration_ms": e.duration_ms,
                "error": e.error,
            }
            for e in response.function_events[:50]  # Limit to first 50
        ],
    }

    # Add note if truncated
    if len(response.events) > 50:
        result["note"] = f"Showing first 50 of {len(response.events)} LLM calls"
    if len(response.function_events) > 50:
        result["note"] = result.get("note", "") + f", first 50 of {len(response.function_events)} function calls"

    return [TextContent(type="text", text=json.dumps(result, indent=2))]


async def handle_search_sessions(arguments: dict[str, Any]) -> list[TextContent]:
    """Handle search_sessions tool call."""
    query = arguments.get("query")
    labels = arguments.get("labels")
    provider = arguments.get("provider")
    model = arguments.get("model")
    function = arguments.get("function")
    after_str = arguments.get("after")
    before_str = arguments.get("before")
    has_errors = arguments.get("has_errors", False)
    evals_failed = arguments.get("evals_failed", False)
    limit = arguments.get("limit")

    # Parse dates
    after = parse_date(after_str) if after_str else None
    before = parse_date(before_str) if before_str else None

    with AIOBSClient() as client:
        response = client.list_sessions()

    # Apply filters
    filtered = filter_sessions(
        response,
        query=query,
        labels=labels,
        provider=provider,
        model=model,
        function=function,
        after=after,
        before=before,
        has_errors=has_errors,
        evals_failed=evals_failed,
    )

    sessions = filtered.sessions
    if limit:
        sessions = sessions[:limit]

    # Build filters applied summary
    filters_applied = {}
    if query:
        filters_applied["query"] = query
    if labels:
        filters_applied["labels"] = labels
    if provider:
        filters_applied["provider"] = provider
    if model:
        filters_applied["model"] = model
    if function:
        filters_applied["function"] = function
    if after_str:
        filters_applied["after"] = after_str
    if before_str:
        filters_applied["before"] = before_str
    if has_errors:
        filters_applied["has_errors"] = True
    if evals_failed:
        filters_applied["evals_failed"] = True

    result = {
        "sessions": [
            session_to_dict(s, filtered.events, filtered.function_events)
            for s in sessions
        ],
        "total_matches": len(filtered.sessions),
        "returned": len(sessions),
        "filters_applied": filters_applied,
    }

    return [TextContent(type="text", text=json.dumps(result, indent=2))]


async def handle_diff_sessions(arguments: dict[str, Any]) -> list[TextContent]:
    """Handle diff_sessions tool call."""
    session_id_1 = arguments.get("session_id_1")
    session_id_2 = arguments.get("session_id_2")

    if not session_id_1 or not session_id_2:
        return [TextContent(type="text", text="Error: session_id_1 and session_id_2 are required")]

    with AIOBSClient() as client:
        session1 = client.get_session(session_id_1)
        session2 = client.get_session(session_id_2)

    if not session1.sessions:
        return [TextContent(type="text", text=f"Session not found: {session_id_1}")]
    if not session2.sessions:
        return [TextContent(type="text", text=f"Session not found: {session_id_2}")]

    diff = compute_session_diff(session1, session2)

    return [TextContent(type="text", text=json.dumps(diff, indent=2))]


# ============================================================================
# Main entry point
# ============================================================================


def main():
    """Run the Shepherd MCP server."""
    import asyncio

    async def run():
        async with stdio_server() as (read_stream, write_stream):
            await server.run(
                read_stream,
                write_stream,
                server.create_initialization_options(),
            )

    asyncio.run(run())


if __name__ == "__main__":
    main()

