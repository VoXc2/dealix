"""Unit tests for core/llm/cost_guard.py (T3b)."""

from __future__ import annotations

import pytest


def test_can_spend_sync_per_request_cap(monkeypatch) -> None:
    monkeypatch.setenv("LLM_MAX_USD_PER_REQUEST", "0.50")
    from core.llm.cost_guard import CostGuard

    g = CostGuard(tenant_id="ten_test", request_cap_usd=0.50)
    ok, reason = g.can_spend_sync(0.10)
    assert ok is True
    ok, reason = g.can_spend_sync(1.00)
    assert ok is False
    assert reason == "per_request_cap_exceeded"


@pytest.mark.asyncio
async def test_record_spend_falls_back_in_process(monkeypatch) -> None:
    monkeypatch.delenv("REDIS_URL", raising=False)
    from core.llm.cost_guard import CostGuard, _local_counters

    _local_counters.clear()
    g = CostGuard(tenant_id="ten_a", tenant_day_cap_usd=10.0)
    await g.record_spend(0.25)
    spent = await g.current_day_spend_usd()
    assert spent == pytest.approx(0.25)
    await g.record_spend(0.10)
    assert (await g.current_day_spend_usd()) == pytest.approx(0.35)


@pytest.mark.asyncio
async def test_tenant_day_cap_blocks(monkeypatch) -> None:
    monkeypatch.delenv("REDIS_URL", raising=False)
    from core.llm.cost_guard import CostGuard, _local_counters

    _local_counters.clear()
    g = CostGuard(tenant_id="ten_b", request_cap_usd=10.0, tenant_day_cap_usd=1.0)
    await g.record_spend(0.95)
    ok, reason = await g.can_spend(0.10)
    assert ok is False
    assert reason == "tenant_day_cap_exceeded"


def test_degrade_model_env(monkeypatch) -> None:
    monkeypatch.setenv("LLM_DEGRADE_MODEL", "claude-haiku")
    from core.llm.cost_guard import degrade_model

    assert degrade_model() == "claude-haiku"
    monkeypatch.delenv("LLM_DEGRADE_MODEL")
    assert degrade_model() is None
