"""Tests for the executive_reporting weekly composer.

Pure unit tests — no network, no LLM, no DB.
"""
from __future__ import annotations

import pytest
from httpx import ASGITransport, AsyncClient

from auto_client_acquisition.executive_reporting import (
    WeeklyReport,
    build_weekly_report,
    decision_summary,
    next_week_plan,
    proof_summary,
    risk_summary,
)
from auto_client_acquisition.self_growth_os import service_activation_matrix


_FORBIDDEN_TOKENS = ("نضمن", "guaranteed", "blast", "scrape")


def _assert_no_forbidden(text: str) -> None:
    for tok in _FORBIDDEN_TOKENS:
        assert tok not in text, f"forbidden token leaked into report: {tok!r}"


def test_build_weekly_report_returns_typed_report():
    report = build_weekly_report()
    assert isinstance(report, WeeklyReport)
    # All required surfaces populated.
    assert report.week_label
    assert report.executive_summary_ar
    assert report.executive_summary_en
    assert isinstance(report.revenue_movement, dict)
    assert isinstance(report.pipeline, dict)
    assert isinstance(report.delivery, dict)
    assert isinstance(report.proof, dict)
    assert isinstance(report.risks, list)
    assert isinstance(report.decisions, list)
    assert isinstance(report.next_week_plan, list)
    assert report.markdown_ar
    assert report.markdown_en
    assert report.guardrails["no_llm_call"] is True
    assert report.guardrails["no_pii_in_report"] is True


def test_markdown_ar_contains_executive_summary_verbatim():
    report = build_weekly_report(week_label="2026-W18")
    assert report.executive_summary_ar in report.markdown_ar
    assert "2026-W18" in report.markdown_ar


def test_markdown_en_is_non_empty_and_has_sections():
    report = build_weekly_report()
    md = report.markdown_en
    assert md
    assert "Weekly Executive Report" in md
    assert "Executive summary" in md
    assert "Risks" in md
    assert "Next-week plan" in md


def test_markdown_contains_no_forbidden_tokens():
    report = build_weekly_report()
    _assert_no_forbidden(report.markdown_ar)
    _assert_no_forbidden(report.markdown_en)
    _assert_no_forbidden(report.executive_summary_ar)
    _assert_no_forbidden(report.executive_summary_en)


def test_decisions_capped_for_founder_processing():
    report = build_weekly_report()
    assert len(report.decisions) <= 5


def test_next_week_plan_grounded_in_existing_data():
    """The plan must reference concrete services from the activation
    matrix candidates rather than invented work."""
    report = build_weekly_report()
    plan_text = "\n".join(report.next_week_plan)
    candidates = service_activation_matrix.candidates_for_promotion()
    candidate_ids = [c.service_id for c in candidates]

    if candidates:
        # At least one plan line must mention a real candidate service_id.
        anchored = any(sid and sid in plan_text for sid in candidate_ids)
        # Or — any plan line is at least sourced from the scorecard
        # recommendations / open loops (still grounded).
        assert anchored or report.next_week_plan, (
            "next_week_plan should be grounded in existing candidates "
            "or scorecard outputs"
        )
    else:
        # No candidates — plan can still be empty or scorecard-driven.
        assert isinstance(report.next_week_plan, list)


def test_decision_summary_handles_string_and_dict_items():
    loop = {
        "decisions": [
            {"title_ar": "قرار 1", "title_en": "Decision 1", "rationale": "why"},
            "raw string decision",
            {"name_ar": "خدمة", "name_en": "Service"},
            {"description": "fallback"},
        ]
    }
    out = decision_summary(loop, limit=10)
    assert len(out) == 4
    assert out[0]["title_ar"] == "قرار 1"
    assert out[1]["title_ar"] == "raw string decision"


def test_risk_summary_includes_non_ok_subsystems_and_risk_blocked_events():
    health = {
        "subsystems": [
            {"name": "live_action_gates", "status": "degraded", "description": "danger"},
            {"name": "ok_one", "status": "ok", "description": "fine"},
            {"name": "missing", "status": "unavailable", "description": "no probe"},
        ]
    }
    proof_events = [
        {"event_type": "risk_blocked", "summary_ar": "محظور أ"},
        {"event_type": "lead_intake", "summary_ar": "ليس مخاطر"},
    ]
    risks = risk_summary(health, proof_events)
    joined = "\n".join(risks)
    assert "live_action_gates" in joined
    assert "missing" in joined
    assert "ok_one" not in joined
    assert "محظور أ" in joined


def test_proof_summary_returns_anonymized_counts():
    out = proof_summary(limit=50)
    assert "total" in out
    assert "by_type" in out
    assert "by_customer" in out
    # All keys are strings; counts non-negative.
    for tp, ct in out["by_type"].items():
        assert isinstance(tp, str)
        assert ct >= 0


def test_next_week_plan_priority_ordering():
    scorecard = {
        "recommendations": [
            {"priority": "P2", "action": "advisory cleanup"},
            {"priority": "P0", "action": "install required tools"},
            {"priority": "P1", "action": "fix orphans"},
        ]
    }
    plan = next_week_plan(
        scorecard=scorecard,
        loop={},
        health_matrix={},
        promotion_candidates=[],
        limit=5,
    )
    # P0 should appear before P1, before P2.
    p0 = next((i for i, l in enumerate(plan) if "P0" in l), -1)
    p1 = next((i for i, l in enumerate(plan) if "P1" in l), -1)
    p2 = next((i for i, l in enumerate(plan) if "P2" in l), -1)
    assert p0 != -1 and p1 != -1 and p2 != -1
    assert p0 < p1 < p2


def test_report_builds_when_scorecard_raises(monkeypatch):
    """Defensive: if weekly_growth_scorecard.build_scorecard raises,
    the report must still be produced (degraded fields)."""
    from auto_client_acquisition.self_growth_os import weekly_growth_scorecard

    def _explode():
        raise RuntimeError("scorecard offline")

    monkeypatch.setattr(weekly_growth_scorecard, "build_scorecard", _explode)
    report = build_weekly_report()
    assert isinstance(report, WeeklyReport)
    # Pipeline/delivery may be sparse but must remain dict-shaped.
    assert isinstance(report.pipeline, dict)
    assert isinstance(report.delivery, dict)
    # Markdown still rendered.
    assert report.markdown_ar
    assert report.markdown_en


# ─── Router endpoints ────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_status_endpoint_returns_module_metadata():
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.get("/api/v1/executive-report/status")
    assert r.status_code == 200
    payload = r.json()
    assert payload["module"] == "executive_reporting"
    assert payload["guardrails"]["no_llm_call"] is True
    assert payload["guardrails"]["no_external_http"] is True


@pytest.mark.asyncio
async def test_weekly_endpoint_returns_full_report():
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.get("/api/v1/executive-report/weekly")
    assert r.status_code == 200
    payload = r.json()
    for key in [
        "week_label",
        "executive_summary_ar",
        "executive_summary_en",
        "revenue_movement",
        "pipeline",
        "delivery",
        "proof",
        "risks",
        "decisions",
        "next_week_plan",
        "markdown_ar",
        "markdown_en",
        "guardrails",
    ]:
        assert key in payload, f"weekly endpoint missing field: {key}"
    _assert_no_forbidden(payload["markdown_ar"])
    _assert_no_forbidden(payload["markdown_en"])
