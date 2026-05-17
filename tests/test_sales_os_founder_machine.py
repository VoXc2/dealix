from __future__ import annotations

import pytest
from httpx import ASGITransport, AsyncClient

from auto_client_acquisition.sales_os.founder_revenue_machine import (
    RiskScoreInput,
    compute_ops_risk_score,
    score_lead_fit,
    validate_transition,
)


def test_score_lead_fit_qualified_a() -> None:
    result = score_lead_fit(
        signals={
            "decision_maker": True,
            "b2b_company": True,
            "has_crm_or_revenue_process": True,
            "uses_or_plans_ai": True,
            "saudi_or_gcc": True,
            "urgency_within_30_days": True,
            "budget_5k_sar_plus": True,
            "no_company": False,
            "student_or_job_seeker": False,
            "vague_curiosity": False,
        }
    )
    assert result["score"] >= 12
    assert result["stage"] == "qualified_A"
    assert result["recommended_tier"] in {"standard", "executive"}


def test_score_lead_fit_closed_lost_when_low_signal() -> None:
    result = score_lead_fit(
        signals={
            "decision_maker": False,
            "b2b_company": False,
            "has_crm_or_revenue_process": False,
            "uses_or_plans_ai": False,
            "saudi_or_gcc": False,
            "urgency_within_30_days": False,
            "budget_5k_sar_plus": False,
            "no_company": True,
            "student_or_job_seeker": True,
            "vague_curiosity": True,
        }
    )
    assert result["score"] < 5
    assert result["stage"] == "closed_lost"
    assert result["recommended_tier"] is None


def test_compute_ops_risk_high_when_ai_and_missing_controls() -> None:
    result = compute_ops_risk_score(
        RiskScoreInput(
            has_crm=False,
            uses_ai=True,
            has_external_approval_gate=False,
            can_link_workflow_to_financial_outcome=False,
            follow_up_is_documented=False,
            source_clarity_for_decisions=True,
            has_evidence_pack=False,
        )
    )
    assert result["risk_band"] == "high"
    assert result["missing_controls"] >= 3


def test_validate_transition_requires_meeting_notes() -> None:
    blocked = validate_transition(
        current_state="meeting_booked",
        target_state="meeting_done",
        context={},
    )
    assert blocked["allowed"] is False
    assert blocked["reason"] == "meeting_notes_required"

    allowed = validate_transition(
        current_state="meeting_booked",
        target_state="meeting_done",
        context={"meeting_notes": "Pain confirmed and scope requested"},
    )
    assert allowed["allowed"] is True
    assert allowed["reason"] == "ok"


@pytest.mark.asyncio
async def test_sales_os_machine_config_endpoint() -> None:
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/v1/sales-os/machine-config")
    assert response.status_code == 200
    payload = response.json()
    assert payload["offer_name"] == "7-Day Governed Revenue & AI Ops Diagnostic"
    assert "qualified_A" in payload["pipeline_states"]
    assert "No scope_sent without fit score." in payload["strict_rules"]


@pytest.mark.asyncio
async def test_sales_os_risk_score_endpoint() -> None:
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/api/v1/sales-os/risk-score",
            json={
                "has_crm": False,
                "uses_ai": True,
                "has_external_approval_gate": False,
                "can_link_workflow_to_financial_outcome": False,
                "follow_up_is_documented": False,
                "source_clarity_for_decisions": False,
                "has_evidence_pack": False,
            },
        )
    assert response.status_code == 200
    payload = response.json()
    assert payload["risk_band"] == "high"
    assert payload["hard_gates"]["approval_required_for_external_actions"] is True


@pytest.mark.asyncio
async def test_sales_os_pipeline_transition_endpoint() -> None:
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        blocked = await client.post(
            "/api/v1/sales-os/pipeline-transition",
            json={
                "current_state": "meeting_booked",
                "target_state": "meeting_done",
                "context": {},
            },
        )
        allowed = await client.post(
            "/api/v1/sales-os/pipeline-transition",
            json={
                "current_state": "meeting_booked",
                "target_state": "meeting_done",
                "context": {"meeting_notes": "Discovery complete"},
            },
        )
    assert blocked.status_code == 200
    assert blocked.json()["allowed"] is False
    assert blocked.json()["reason"] == "meeting_notes_required"
    assert allowed.status_code == 200
    assert allowed.json()["allowed"] is True
