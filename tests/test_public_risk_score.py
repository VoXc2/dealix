"""Public risk-score endpoint + scoring engine — governance-readiness lead magnet."""

from __future__ import annotations

from collections.abc import AsyncGenerator

import pytest
import pytest_asyncio
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from api.routers.public import router as public_router
from auto_client_acquisition import risk_score

_ALL_CONTROLS = {
    "has_crm": True,
    "pipeline_reliable": True,
    "approval_before_external_action": True,
    "followup_documented": True,
    "can_link_workflow_to_value": True,
    "has_evidence_pack": True,
}


# ── Pure scoring engine ───────────────────────────────────────────────


def test_fully_governed_company_scores_zero_risk() -> None:
    result = risk_score.score({**_ALL_CONTROLS, "uses_ai": True})
    assert result["risk_score"] == 0
    assert result["risk_band"] == "low"
    assert result["gaps"] == []
    assert result["is_estimate"] is True


def test_no_controls_scores_high_risk() -> None:
    result = risk_score.score({})
    assert result["risk_score"] == 84  # 6 gaps x 14
    assert result["risk_band"] == "high"
    assert result["gap_count"] == 6


def test_ungoverned_ai_adds_compounder_penalty() -> None:
    # All six controls present EXCEPT the approval boundary, plus AI in use.
    answers = {**_ALL_CONTROLS, "approval_before_external_action": False, "uses_ai": True}
    result = risk_score.score(answers)
    # 1 missing control (14) + ungoverned-AI penalty (16) = 30.
    assert result["risk_score"] == 30
    assert any(g["key"] == "ungoverned_ai" for g in result["gaps"])


def test_score_is_capped_at_100() -> None:
    # Every control missing + AI in use without approval = 84 + 16 = 100.
    result = risk_score.score({"uses_ai": True})
    assert result["risk_score"] == 100
    assert result["risk_band"] == "high"


def test_answers_accept_string_yes_no() -> None:
    assert risk_score.score(dict.fromkeys(_ALL_CONTROLS, "yes"))["risk_score"] == 0
    assert risk_score.score(dict.fromkeys(_ALL_CONTROLS, "no"))["risk_score"] == 84


def test_recommended_next_step_is_free_diagnostic() -> None:
    # No paid promise — the lead magnet always routes to ladder rung 0.
    assert risk_score.score({})["recommended_next_step"]["offer"] == (
        "free_ai_ops_diagnostic"
    )


# ── HTTP endpoint ─────────────────────────────────────────────────────


@pytest_asyncio.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    app = FastAPI()
    app.include_router(public_router)
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        yield c


@pytest.mark.asyncio
async def test_endpoint_returns_score(client: AsyncClient) -> None:
    res = await client.post(
        "/api/v1/public/risk-score",
        json={
            "company": "Test Co",
            "email": "founder@test.sa",
            "consent": True,
            "has_crm": True,
            "uses_ai": True,
        },
    )
    assert res.status_code == 200
    body = res.json()
    assert body["ok"] is True
    assert 0 <= body["risk_score"] <= 100
    assert body["governance_decision"] == "allow"
    assert body["is_estimate"] is True


@pytest.mark.asyncio
async def test_endpoint_requires_consent(client: AsyncClient) -> None:
    res = await client.post(
        "/api/v1/public/risk-score",
        json={"company": "Test Co", "email": "founder@test.sa", "consent": False},
    )
    assert res.status_code == 422
    assert res.json()["detail"] == "consent_required"


@pytest.mark.asyncio
async def test_endpoint_requires_company_and_email(client: AsyncClient) -> None:
    res = await client.post(
        "/api/v1/public/risk-score", json={"company": "", "email": "x", "consent": True}
    )
    assert res.status_code == 422
    assert res.json()["detail"] == "missing_required_fields"


@pytest.mark.asyncio
async def test_endpoint_honeypot_drops_silently(client: AsyncClient) -> None:
    res = await client.post(
        "/api/v1/public/risk-score",
        json={
            "company": "Bot Co",
            "email": "bot@test.sa",
            "consent": True,
            "website": "http://spam.example",
        },
    )
    # Honeypot returns 200 (no signal to the bot) but persists nothing.
    assert res.status_code == 200
    assert res.json()["ok"] is True
    assert "lead_id" not in res.json()
