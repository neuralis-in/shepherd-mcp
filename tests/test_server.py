"""Tests for the Shepherd MCP server."""

import pytest

from shepherd_mcp.models import Session, SessionsResponse
from shepherd_mcp.server import (
    calc_avg_latency,
    calc_total_tokens,
    count_errors,
    format_duration,
    format_timestamp,
    get_model_distribution,
    get_provider_distribution,
    session_to_dict,
)


class TestFormatTimestamp:
    """Tests for format_timestamp."""

    def test_basic_timestamp(self):
        # Unix timestamp for 2025-01-01 00:00:00 UTC
        ts = 1735689600.0
        result = format_timestamp(ts)
        assert "2025" in result
        assert "01" in result


class TestFormatDuration:
    """Tests for format_duration."""

    def test_milliseconds(self):
        assert format_duration(500) == "500ms"
        assert format_duration(999) == "999ms"

    def test_seconds(self):
        assert format_duration(1000) == "1.0s"
        assert format_duration(5500) == "5.5s"

    def test_minutes(self):
        assert format_duration(60000) == "1.0m"
        assert format_duration(90000) == "1.5m"


class TestSessionToDict:
    """Tests for session_to_dict."""

    def test_basic_session(self):
        session = Session(
            id="test-123",
            name="test-session",
            started_at=1735689600.0,
            ended_at=1735689660.0,
            meta={"cwd": "/test"},
            labels={"env": "test"},
        )
        result = session_to_dict(session, [], [])

        assert result["id"] == "test-123"
        assert result["name"] == "test-session"
        assert result["duration_ms"] == 60000.0
        assert result["duration"] == "1.0m"
        assert result["labels"]["env"] == "test"


class TestCalcTotalTokens:
    """Tests for calc_total_tokens."""

    def test_empty_events(self):
        result = calc_total_tokens([])
        assert result == {"input": 0, "output": 0, "total": 0}


class TestCalcAvgLatency:
    """Tests for calc_avg_latency."""

    def test_empty_events(self):
        result = calc_avg_latency([])
        assert result == 0.0


class TestCountErrors:
    """Tests for count_errors."""

    def test_no_errors(self):
        result = count_errors([], [])
        assert result == 0


class TestGetProviderDistribution:
    """Tests for get_provider_distribution."""

    def test_empty_events(self):
        result = get_provider_distribution([])
        assert result == {}


class TestGetModelDistribution:
    """Tests for get_model_distribution."""

    def test_empty_events(self):
        result = get_model_distribution([])
        assert result == {}

