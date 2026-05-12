"""Unit tests for api/middleware/business_hours.py (T3e)."""

from __future__ import annotations

import pytest


def test_disabled_by_default(monkeypatch) -> None:
    monkeypatch.delenv("BUSINESS_HOURS_ENFORCE", raising=False)
    from api.middleware.business_hours import _enabled

    assert _enabled() is False


def test_enabled_truthy_values(monkeypatch) -> None:
    from api.middleware.business_hours import _enabled

    for v in ("1", "true", "yes"):
        monkeypatch.setenv("BUSINESS_HOURS_ENFORCE", v)
        assert _enabled() is True


def test_next_open_window_is_iso_string() -> None:
    from api.middleware.business_hours import _next_open_window_iso

    out = _next_open_window_iso()
    assert isinstance(out, str)
    assert "T" in out  # ISO 8601


@pytest.mark.asyncio
async def test_pass_through_without_intent_header(async_client, monkeypatch) -> None:
    monkeypatch.setenv("BUSINESS_HOURS_ENFORCE", "1")
    # Default route should pass through because no X-Dealix-Intent header.
    r = await async_client.get("/api/v1/public/health")
    assert r.status_code == 200
