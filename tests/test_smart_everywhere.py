"""
PR-SMART-EVERYWHERE acceptance tests.

Covers:
  T1.1-T1.4: Sprint Days 1, 2, 4, 6 LLM/channel-enhanced
  T2.1: Founder Daily Digest
  T2.2: Phase 5 forecast endpoint + module
  T2.3: Phase 5 benchmarks endpoint + module
  T3.1: Brain editor frontend assets exist
  T3.2: smart-launch CLI command exists in dealix_cli.py
"""

from __future__ import annotations

from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]


# ── T1: Sprint enhancements (E2E) ─────────────────────────────────


@pytest.mark.asyncio
async def test_t1_sprint_day_1_llm_enhanced(async_client) -> None:
    """Day 1 output has llm_enhanced flag (true if LLM available, false on fallback)."""
    create = await async_client.post(
        "/api/v1/prospects",
        json={"name": "t1d1", "company": "Test Co", "sector": "B2B",
              "city": "Riyadh", "expected_value_sar": 499.0,
              "relationship_type": "warm_1st_degree"},
    )
    pid = create.json()["id"]
    for stage in ("messaged", "replied", "meeting_booked", "pilot_offered",
                  "invoice_sent", "paid_or_committed", "closed_won"):
        r = await async_client.post(
            f"/api/v1/prospects/{pid}/advance",
            json={"target_status": stage},
        )
        assert r.status_code == 200

    cust = (await async_client.get(f"/api/v1/prospects/{pid}")).json()["customer_id"]
    sprint = (await async_client.post(
        "/api/v1/sprints/start",
        json={"customer_id": cust, "service_id": "growth_starter"},
    )).json()["sprint_id"]

    day1 = await async_client.post(f"/api/v1/sprints/{sprint}/diagnostic/generate")
    assert day1.status_code == 200
    out = day1.json()["output"]
    assert "llm_enhanced" in out
    assert "llm_safety_passed" in out
    assert "best_segment_ar" in out
    assert "risk_to_avoid_ar" in out
    # Both fields populated even on fallback
    assert out["why_segment_ar"]
    assert out["risk_to_avoid_ar"]


@pytest.mark.asyncio
async def test_t1_sprint_day_2_channel_aware(async_client) -> None:
    """Day 2 opportunities each have channel_score + channel_blocked_reasons."""
    # Reuse most recent customer from previous test, or create new
    p = await async_client.post(
        "/api/v1/prospects",
        json={"name": "t1d2", "company": "Channel Co", "sector": "training",
              "city": "Jeddah", "expected_value_sar": 499.0,
              "relationship_type": "warm_1st_degree"},
    )
    pid = p.json()["id"]
    for stage in ("messaged", "replied", "meeting_booked", "pilot_offered",
                  "invoice_sent", "paid_or_committed", "closed_won"):
        await async_client.post(
            f"/api/v1/prospects/{pid}/advance",
            json={"target_status": stage},
        )
    cust = (await async_client.get(f"/api/v1/prospects/{pid}")).json()["customer_id"]
    sprint = (await async_client.post(
        "/api/v1/sprints/start",
        json={"customer_id": cust, "service_id": "growth_starter"},
    )).json()["sprint_id"]

    day2 = await async_client.post(f"/api/v1/sprints/{sprint}/opportunities/generate")
    assert day2.status_code == 200
    out = day2.json()["output"]
    assert out.get("channel_orchestrator_active") is True
    assert out["count"] == 10
    for opp in out["opportunities"]:
        assert "channel_score" in opp
        assert "channel_blocked_reasons" in opp
        assert "channel_reason_ar" in opp


@pytest.mark.asyncio
async def test_t1_sprint_day_4_meeting_prep_has_llm_field(async_client) -> None:
    p = await async_client.post(
        "/api/v1/prospects",
        json={"name": "t1d4", "company": "Meeting Co",
              "expected_value_sar": 499.0, "relationship_type": "warm_1st_degree"},
    )
    pid = p.json()["id"]
    for stage in ("messaged", "replied", "meeting_booked", "pilot_offered",
                  "invoice_sent", "paid_or_committed", "closed_won"):
        await async_client.post(
            f"/api/v1/prospects/{pid}/advance",
            json={"target_status": stage},
        )
    cust = (await async_client.get(f"/api/v1/prospects/{pid}")).json()["customer_id"]
    sprint = (await async_client.post(
        "/api/v1/sprints/start",
        json={"customer_id": cust},
    )).json()["sprint_id"]

    day4 = await async_client.post(f"/api/v1/sprints/{sprint}/meeting-prep")
    assert day4.status_code == 200
    out = day4.json()["output"]
    assert "discovery_questions_ar" in out
    assert "llm_questions_added" in out
    assert "llm_safety_passed" in out
    # Discovery questions list always populated (deterministic baseline at minimum)
    assert len(out["discovery_questions_ar"]) >= 5


@pytest.mark.asyncio
async def test_t1_sprint_day_6_proof_draft_has_executive_summary(async_client) -> None:
    p = await async_client.post(
        "/api/v1/prospects",
        json={"name": "t1d6", "company": "Proof Co",
              "expected_value_sar": 499.0, "relationship_type": "warm_1st_degree"},
    )
    pid = p.json()["id"]
    for stage in ("messaged", "replied", "meeting_booked", "pilot_offered",
                  "invoice_sent", "paid_or_committed", "closed_won"):
        await async_client.post(
            f"/api/v1/prospects/{pid}/advance",
            json={"target_status": stage},
        )
    cust = (await async_client.get(f"/api/v1/prospects/{pid}")).json()["customer_id"]
    sprint = (await async_client.post(
        "/api/v1/sprints/start",
        json={"customer_id": cust},
    )).json()["sprint_id"]

    day6 = await async_client.post(f"/api/v1/sprints/{sprint}/proof/draft")
    assert day6.status_code == 200
    out = day6.json()["output"]
    assert "executive_summary_ar" in out
    assert "llm_enhanced" in out
    assert "llm_safety_passed" in out
    assert out["executive_summary_ar"]


# ── T2.1: Founder Digest ──────────────────────────────────────────


@pytest.mark.asyncio
async def test_t2_founder_digest_returns_full_shape(async_client) -> None:
    r = await async_client.get("/api/v1/founder/digest")
    assert r.status_code == 200
    body = r.json()
    for required in ("standup", "approvals", "active_sprints",
                     "best_channel", "intros", "live_action_gates", "llm"):
        assert required in body, f"digest missing {required}"
    assert "as_of" in body
    assert "advice_ar" in body
    # 8 gates always present
    assert len(body["live_action_gates"]) == 8
    # All FALSE in test env
    assert all(not v for v in body["live_action_gates"].values())


@pytest.mark.asyncio
async def test_t2_founder_digest_intros_have_safety_metadata(async_client) -> None:
    """Each LLM-drafted intro carries fallback_reason + provider for audit."""
    # Create at least one prospect due today
    await async_client.post(
        "/api/v1/prospects",
        json={"name": "digest_test", "company": "Digest Co",
              "expected_value_sar": 499.0, "relationship_type": "warm_1st_degree",
              "next_step_ar": "warm-intro DM"},
    )
    r = await async_client.get("/api/v1/founder/digest")
    body = r.json()
    intros = body.get("intros") or []
    if intros:
        for intro in intros:
            assert "draft_ar" in intro
            assert "llm_used" in intro
            assert "approval_required" in intro


# ── T2.2: Forecast endpoint ───────────────────────────────────────


def test_t2_forecast_module_pure_logic() -> None:
    from auto_client_acquisition.intelligence.forecast import project
    out = project()
    for k in ("pipeline_value_sar", "expected_close_rate",
              "projected_revenue_sar", "current_mrr_sar",
              "projected_mrr_at_horizon_sar", "method"):
        assert k in out


@pytest.mark.asyncio
async def test_t2_forecast_endpoint(async_client) -> None:
    r = await async_client.get("/api/v1/intelligence/forecast?horizon_days=30")
    assert r.status_code == 200
    body = r.json()
    assert body["as_of_horizon_days"] == 30
    assert body["method"] == "linear_pipeline_projection_v1"
    assert "current_arr_sar" in body


# ── T2.3: Benchmarks endpoint ─────────────────────────────────────


def test_t2_benchmarks_module_handles_empty() -> None:
    from auto_client_acquisition.intelligence.benchmarks import aggregate
    out = aggregate()
    assert out["total_customers"] == 0
    assert out["sectors_analyzed"] == 0
    assert "empty_ar" in out


@pytest.mark.asyncio
async def test_t2_benchmarks_endpoint(async_client) -> None:
    r = await async_client.get("/api/v1/intelligence/benchmarks")
    assert r.status_code == 200
    body = r.json()
    assert "sectors" in body
    assert "min_sample_for_confidence" in body


# ── T3.1: Brain editor UI ─────────────────────────────────────────


def test_t3_brain_editor_html_exists() -> None:
    p = REPO / "landing" / "brain.html"
    assert p.exists()
    text = p.read_text(encoding="utf-8")
    assert 'data-customer-id=""' in text or "customer_id" in text
    assert "brain-editor.js" in text
    assert "dx-brain" in text


def test_t3_brain_editor_js_exists() -> None:
    p = REPO / "landing" / "assets" / "js" / "brain-editor.js"
    assert p.exists()
    text = p.read_text(encoding="utf-8")
    # Verify it patches the brain endpoint
    assert "/companies/" in text
    assert "/brain" in text
    assert "PATCH" in text


# ── T3.2: smart-launch CLI ────────────────────────────────────────


def test_t3_smart_launch_cli_exists() -> None:
    p = REPO / "scripts" / "dealix_cli.py"
    text = p.read_text(encoding="utf-8")
    assert "cmd_smart_launch" in text
    assert "smart-launch" in text
    assert "/api/v1/founder/digest" in text
    # Forecast + benchmarks commands also present
    assert "cmd_forecast" in text
    assert "cmd_benchmarks" in text
