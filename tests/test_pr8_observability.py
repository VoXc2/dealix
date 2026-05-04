"""PR-8 Observability + Daily Ops Orchestrator tests."""

from __future__ import annotations

import uuid

import pytest
from sqlalchemy import select

from auto_client_acquisition.agent_observability.cost_tracker import estimate_cost_usd
from auto_client_acquisition.agent_observability.quality_metrics import compute
from auto_client_acquisition.agent_observability.trace_redactor import (
    redact_dict, redact_text,
)
from auto_client_acquisition.agent_observability.unsafe_action_monitor import _severity_for
from auto_client_acquisition.revenue_company_os.daily_ops_orchestrator import (
    WINDOWS, list_windows,
)
from db.models import (
    AgentRunCostRecord, DailyOpsRunRecord, UnsafeActionRecord,
)


# ── Trace Redactor ────────────────────────────────────────────────


def test_redact_text_strips_email():
    assert redact_text("contact: ahmed@dealix.sa") == "contact: <email>"


def test_redact_text_strips_saudi_phone():
    assert redact_text("call +966501234567 now") == "call <phone:sa> now"
    assert redact_text("local 0501234567") == "local <phone:sa>"


def test_redact_text_strips_api_key():
    out = redact_text("token sk-abcdef1234567890ABCDEF rest")
    assert "<api_key>" in out
    assert "sk-abcdef1234567890ABCDEF" not in out


def test_redact_text_strips_payment_id():
    out = redact_text("invoice inv_abc12345 was paid")
    assert "<payment_id>" in out
    assert "inv_abc12345" not in out


def test_redact_dict_scrubs_sensitive_keys():
    out = redact_dict({"password": "supersecret", "name": "ahmed", "phone": "+966501234567"})
    assert out["password"] == "<redacted>"
    # phone is in sensitive keys list — fully redacted
    assert out["phone"] == "<redacted>"
    assert out["name"] == "ahmed"


def test_redact_dict_recurses_lists_and_nesteds():
    out = redact_dict({"meta": {"api_key": "sk-XYZ12345abcdef", "items": ["a@b.com", 1]}})
    assert out["meta"]["api_key"] == "<redacted>"
    assert "<email>" in out["meta"]["items"][0]


def test_redact_dict_truncates_very_long_strings():
    long = "x" * 5000
    out = redact_dict({"body": long}, max_str_len=1024)
    assert len(out["body"]) <= 1024 + len("…(truncated)")


# ── Cost Tracker ─────────────────────────────────────────────────


def test_estimate_cost_zero_for_unknown_provider():
    assert estimate_cost_usd(provider=None, model=None, input_tokens=1000, output_tokens=500) == 0.0
    assert estimate_cost_usd(provider="ufo-co", model="x", input_tokens=1, output_tokens=1) == 0.0


def test_estimate_cost_anthropic_haiku():
    # haiku rate: $0.80 in / $4.00 out per 1M tokens
    out = estimate_cost_usd(provider="anthropic", model="claude-haiku-4.5",
                            input_tokens=1_000_000, output_tokens=1_000_000)
    assert abs(out - 4.80) < 0.01


def test_estimate_cost_handles_partial_tokens():
    out = estimate_cost_usd(provider="anthropic", model="claude-sonnet",
                            input_tokens=500, output_tokens=200)
    # Tiny number, just confirm > 0 and < $1
    assert 0.0 < out < 1.0


@pytest.mark.asyncio
async def test_observability_cost_endpoint(async_client):
    r = await async_client.post("/api/v1/observability/costs/runs", json={
        "agent_name": "test_agent",
        "provider": "anthropic",
        "model": "claude-sonnet-4.6",
        "input_tokens": 1000,
        "output_tokens": 500,
        "latency_ms": 250,
        "role": "sales_manager",
        "service_id": "growth_starter",
        "meta": {"api_key": "sk-LIVEsensitive123456", "user_phone": "+966501234567"},
    })
    assert r.status_code == 200
    body = r.json()
    assert body["cost_estimate_usd"] > 0
    assert body["cost_estimate_sar"] > 0


@pytest.mark.asyncio
async def test_observability_cost_summary_filters(async_client):
    r = await async_client.get("/api/v1/observability/costs/summary?days=30")
    assert r.status_code == 200
    body = r.json()
    assert "total_cost_sar" in body
    assert "cost_sar_by_role" in body
    assert "avg_latency_ms" in body


@pytest.mark.asyncio
async def test_cost_record_redacts_pii_in_meta(async_client):
    """Confirm meta_json never stores raw API keys / phones."""
    payload = {
        "agent_name": "redact_test",
        "provider": "anthropic",
        "model": "haiku",
        "input_tokens": 1, "output_tokens": 1,
        "meta": {
            "api_key": "sk-SHOULDBEREDACTED1234",
            "free_text": "phone +966501234567 emails me at me@dealix.sa",
        },
    }
    r = await async_client.post("/api/v1/observability/costs/runs", json=payload)
    assert r.status_code == 200
    cid = r.json()["id"]
    from db.session import get_session
    async with get_session() as s:
        row = (await s.execute(
            select(AgentRunCostRecord).where(AgentRunCostRecord.id == cid)
        )).scalar_one()
    meta = row.meta_json or {}
    # api_key key was scrubbed
    assert meta.get("api_key") == "<redacted>"
    # phone + email in free text were redacted to tokens
    free = meta.get("free_text", "")
    assert "+966501234567" not in free
    assert "me@dealix.sa" not in free


# ── Unsafe Action Monitor ────────────────────────────────────────


def test_severity_high_for_cold_whatsapp():
    assert _severity_for("cold_whatsapp") == "high"
    assert _severity_for("scrape_linkedin") == "high"
    assert _severity_for("guaranteed_claim") == "high"


def test_severity_medium_for_mass_send():
    assert _severity_for("mass_send") == "medium"
    assert _severity_for("missing_consent") == "medium"


def test_severity_low_for_unknown():
    assert _severity_for("foobar") == "low"


@pytest.mark.asyncio
async def test_unsafe_record_endpoint(async_client):
    r = await async_client.post("/api/v1/observability/unsafe/record", json={
        "pattern": "cold_whatsapp",
        "blocked_reason": "no_opt_in",
        "source_module": "operator",
    })
    assert r.status_code == 200
    body = r.json()
    assert body["severity"] == "high"


@pytest.mark.asyncio
async def test_unsafe_summary_invariant(async_client):
    """The 'no_unsafe_action_executed' invariant must always be True."""
    r = await async_client.get("/api/v1/observability/unsafe/summary?days=7")
    assert r.status_code == 200
    body = r.json()
    assert body["no_unsafe_action_executed"] is True


@pytest.mark.asyncio
async def test_unsafe_summary_counts_severity(async_client):
    # Insert one high + one medium
    await async_client.post("/api/v1/observability/unsafe/record",
                            json={"pattern": "cold_whatsapp"})
    await async_client.post("/api/v1/observability/unsafe/record",
                            json={"pattern": "mass_send"})
    r = await async_client.get("/api/v1/observability/unsafe/summary?days=7")
    body = r.json()
    assert body["by_severity"]["high"] >= 1
    assert body["by_severity"]["medium"] >= 1


# ── Quality Metrics ──────────────────────────────────────────────


def test_quality_metrics_zero_when_empty():
    out = compute(proof_events=[], objection_events=[], tickets=[], unsafe_actions=[])
    assert out["draft_acceptance_rate"] == 0.0
    assert out["override_rate"] == 0.0


def test_quality_metrics_acceptance_rate():
    class E:
        def __init__(self, t): self.unit_type = t
    drafts = [E("draft_created")] * 10
    approvals = [E("approval_collected")] * 6
    out = compute(proof_events=drafts + approvals, objection_events=[], tickets=[], unsafe_actions=[])
    assert out["draft_acceptance_rate"] == 0.6


def test_quality_metrics_complaint_rate():
    class T:
        def __init__(self, p, c): self.priority = p; self.category = c
    tickets = [T("P0", "security"), T("P3", "question"), T("P1", "billing_dispute")]
    out = compute(proof_events=[], objection_events=[], tickets=tickets, unsafe_actions=[])
    # 2 complaint tickets out of 3
    assert abs(out["complaint_rate"] - 2 / 3) < 0.01


@pytest.mark.asyncio
async def test_quality_endpoint(async_client):
    r = await async_client.get("/api/v1/observability/quality?days=30")
    assert r.status_code == 200
    body = r.json()
    assert "kpis" in body
    assert "samples" in body["kpis"]


# ── Daily Ops Orchestrator ───────────────────────────────────────


def test_windows_constant_has_four():
    assert set(WINDOWS.keys()) == {"morning", "midday", "closing", "scorecard"}


def test_morning_includes_ceo_and_compliance():
    assert "ceo" in WINDOWS["morning"]
    assert "compliance" in WINDOWS["morning"]


@pytest.mark.asyncio
async def test_daily_ops_run_morning_persists(async_client):
    r = await async_client.post("/api/v1/daily-ops/run", json={"window": "morning"})
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["window"] == "morning"
    assert body["roles_processed"]
    assert "ceo" in body["roles_processed"]
    # Verify a row was written
    from db.session import get_session
    async with get_session() as s:
        rows = list((await s.execute(
            select(DailyOpsRunRecord).where(DailyOpsRunRecord.run_window == "morning")
        )).scalars().all())
    assert any(r.id == body["run_id"] for r in rows)


@pytest.mark.asyncio
async def test_daily_ops_run_unknown_400(async_client):
    r = await async_client.post("/api/v1/daily-ops/run", json={"window": "midnight"})
    assert r.status_code == 400


@pytest.mark.asyncio
async def test_daily_ops_windows_endpoint(async_client):
    r = await async_client.get("/api/v1/daily-ops/windows")
    assert r.status_code == 200
    assert r.json()["count"] == 4


@pytest.mark.asyncio
async def test_daily_ops_history(async_client):
    # Trigger a run so history is non-empty.
    await async_client.post("/api/v1/daily-ops/run", json={"window": "scorecard"})
    r = await async_client.get("/api/v1/daily-ops/history?limit=5")
    assert r.status_code == 200
    body = r.json()
    assert body["count"] >= 1


def test_list_windows_returns_roles():
    rows = list_windows()
    morning = next(r for r in rows if r["window"] == "morning")
    assert "sales_manager" in morning["roles"]


# ── Compliance dashboard wiring (live unsafe data feeds the CS module) ──


@pytest.mark.asyncio
async def test_compliance_brief_picks_up_high_severity_blocks(async_client):
    """After we record a high-severity block, compliance summary should reflect it."""
    await async_client.post("/api/v1/observability/unsafe/record",
                            json={"pattern": "cold_whatsapp"})
    r = await async_client.get("/api/v1/observability/unsafe/summary?days=1")
    assert r.json()["by_severity"]["high"] >= 1
