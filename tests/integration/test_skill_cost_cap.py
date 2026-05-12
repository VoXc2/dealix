"""Integration test for T11 cost-cap enforcement on /api/v1/skills/{id}/run."""

from __future__ import annotations

import pytest


@pytest.mark.asyncio
async def test_run_returns_402_when_estimated_above_per_request_cap(
    async_client, monkeypatch
) -> None:
    # Force a 0.10 USD cap and request 1.00 USD — must short-circuit 402.
    monkeypatch.setenv("LLM_MAX_USD_PER_REQUEST", "0.10")
    r = await async_client.post(
        "/api/v1/skills/sales_qualifier/run",
        json={
            "inputs": {
                "lead_snapshot": {"budget": "y", "authority": "y", "need": "y", "timeline": "y"},
                "compliance_signals": {"has_pdpl_consent": True},
            },
            "estimated_usd": 1.00,
        },
    )
    assert r.status_code == 402
    body = r.json()
    detail = body["detail"] if isinstance(body["detail"], dict) else body
    assert detail.get("error") == "cost_cap_exceeded"
    assert detail.get("reason") in {
        "per_request_cap_exceeded",
        "tenant_day_cap_exceeded",
    }


@pytest.mark.asyncio
async def test_run_includes_tenant_id_in_response(async_client) -> None:
    """The traced run path always echoes the resolved tenant_id."""
    r = await async_client.post(
        "/api/v1/skills/lead_scorer/run",
        json={"inputs": {"lead": {"industry": "real-estate"}}},
    )
    assert r.status_code == 200
    assert "tenant_id" in r.json()


@pytest.mark.asyncio
async def test_run_zero_estimate_skips_cost_guard(async_client) -> None:
    """estimated_usd=0 must bypass CostGuard entirely (free deterministic
    handler path). Sanity-check the happy path still works."""
    r = await async_client.post(
        "/api/v1/skills/ar_en_translator/run",
        json={"inputs": {"text": "احتاج فاتورة", "from": "ar", "to": "en"}, "estimated_usd": 0.0},
    )
    assert r.status_code == 200
    assert "invoice" in r.json()["result"]["translated"]
