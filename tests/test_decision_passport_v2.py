"""Wave 12 §32.3.4 (Engine 4) — Decision Passport v1.1 hardening tests.

Validates the schema extension (owner, deadline, action_mode) +
runtime validate_passport() guard + POST endpoint, all per plan §32.3.4.

Reuses existing v1.0 builder; v1.1 fields have defaults so old tests
keep passing.
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError

from auto_client_acquisition.decision_passport import (
    SCHEMA_VERSION,
    ActionMode,
    DecisionPassport,
    Owner,
    ScoreBoard,
    ValidationFailure,
    validate_passport,
)


def _passport(
    *,
    proof_target: str = "demo_booked",
    owner: str = "founder",
    deadline: datetime | None = None,
    action_mode: str = "approval_required",
    best_channel: str = "manual_linkedin",
) -> DecisionPassport:
    """Helper: build a minimally-valid passport for tests."""
    return DecisionPassport(
        lead_id="lead_test_v2",
        company="Test Co",
        source="warm_intro",
        why_now_ar="افتتاح فرع",
        why_now_en="new branch",
        icp_tier="A",
        priority_bucket="P1_THIS_WEEK",
        scores=ScoreBoard(
            fit_score=0.8,
            intent_score=0.7,
            urgency_score=0.6,
            revenue_potential_score=0.7,
            engagement_score=0.5,
            data_quality_score=0.6,
            warm_route_score=0.9,
            compliance_risk_score=0.1,
            deliverability_risk_score=0.2,
        ),
        best_channel=best_channel,
        recommended_action="prepare_diagnostic",
        recommended_action_ar="جهّز تشخيصًا",
        proof_target=proof_target,
        proof_target_ar="حجز عرض توضيحي",
        next_step_ar="جهّز تشخيصًا",
        next_step_en="prepare_diagnostic",
        owner=owner,  # type: ignore[arg-type]
        deadline=deadline,
        action_mode=action_mode,  # type: ignore[arg-type]
    )


# ─────────────────────────────────────────────────────────────────────
# Schema (3 tests)
# ─────────────────────────────────────────────────────────────────────


def test_schema_version_bumped_to_v1_1() -> None:
    """Wave 12 §32.3.4 bumps schema_version from 1.0 → 1.1."""
    assert SCHEMA_VERSION == "1.1"
    p = _passport()
    assert p.schema_version == "1.1"


def test_v1_0_callers_still_work_via_defaults() -> None:
    """Backward-compat: a passport built without owner/deadline/action_mode
    must still succeed (defaults apply)."""
    # Build with the v1.0 set of fields only (no owner/deadline/action_mode kwargs)
    p = DecisionPassport(
        lead_id="lead_v1",
        company="Old Caller Co",
        source="warm_intro",
        why_now_ar="x",
        why_now_en="x",
        icp_tier="A",
        priority_bucket="P2_NURTURE",
        scores=ScoreBoard(
            fit_score=0.5, intent_score=0.5, urgency_score=0.5,
            revenue_potential_score=0.5, engagement_score=0.5,
            data_quality_score=0.5, warm_route_score=0.5,
            compliance_risk_score=0.0, deliverability_risk_score=0.0,
        ),
        best_channel="manual_linkedin",
        recommended_action="x",
        recommended_action_ar="x",
        proof_target="any",
        proof_target_ar="x",
        next_step_ar="x",
        next_step_en="x",
    )
    # Defaults must be set
    assert p.owner == "founder"
    assert p.deadline is None
    assert p.action_mode == "approval_required"


def test_invalid_action_mode_rejected_by_pydantic() -> None:
    """ActionMode is a Literal — pydantic refuses unknown values."""
    with pytest.raises(ValidationError):
        _passport(action_mode="auto_send")  # not in canonical 5


# ─────────────────────────────────────────────────────────────────────
# validate_passport — runtime hard-rule guards (5 tests)
# ─────────────────────────────────────────────────────────────────────


def test_validate_passport_passes_on_valid_passport() -> None:
    """Happy path: a fully-valid passport must NOT raise."""
    p = _passport()
    validate_passport(p)  # no raise = PASS


def test_validate_passport_fails_on_empty_proof_target() -> None:
    """Hard rule: No Proof Target = No Action."""
    p = _passport(proof_target="")
    with pytest.raises(ValidationFailure) as excinfo:
        validate_passport(p)
    assert excinfo.value.rule == "no_proof_target"
    assert excinfo.value.field == "proof_target"


def test_validate_passport_fails_on_whitespace_proof_target() -> None:
    """Hard rule: whitespace-only proof_target also blocked."""
    p = _passport(proof_target="   ")
    with pytest.raises(ValidationFailure) as excinfo:
        validate_passport(p)
    assert excinfo.value.rule == "no_proof_target"


def test_validate_passport_fails_on_past_deadline() -> None:
    """Hard rule: deadline in the past = stale passport."""
    yesterday = datetime.now(timezone.utc) - timedelta(days=1)
    p = _passport(deadline=yesterday)
    with pytest.raises(ValidationFailure) as excinfo:
        validate_passport(p)
    assert excinfo.value.rule == "deadline_in_past"


def test_validate_passport_fails_on_blocked_channel() -> None:
    """Hard rule: best_channel must be in customer's allowed_channels."""
    p = _passport(best_channel="cold_whatsapp")
    with pytest.raises(ValidationFailure) as excinfo:
        validate_passport(
            p,
            allowed_channels=["manual_linkedin", "warm_email"],  # cold_whatsapp NOT here
        )
    assert excinfo.value.rule == "channel_blocked"


# ─────────────────────────────────────────────────────────────────────
# Endpoint — POST /api/v1/decision-passport/create (2 tests)
# ─────────────────────────────────────────────────────────────────────


def _client():
    """Build a minimal FastAPI app with just the decision-passport router
    (avoids import cascade from api.main → api.security.jwt → python-jose).
    """
    from fastapi import FastAPI

    from api.routers.decision_passport import router

    app = FastAPI()
    app.include_router(router)
    return TestClient(app)


def test_post_create_endpoint_returns_validated_passport() -> None:
    """POST /api/v1/decision-passport/create echoes a built passport
    after running validate_passport()."""
    client = _client()
    payload = _passport().model_dump(mode="json")
    resp = client.post("/api/v1/decision-passport/create", json=payload)
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert body["schema_version"] == "1.1"
    assert body["owner"] == "founder"
    assert body["action_mode"] == "approval_required"
    assert body["validated"] is True


def test_post_create_endpoint_422_on_blocked_channel() -> None:
    """When allowed_channels is supplied and best_channel violates it,
    endpoint returns 422 with rule + field in the response body."""
    client = _client()
    payload = _passport(best_channel="cold_whatsapp").model_dump(mode="json")
    resp = client.post(
        "/api/v1/decision-passport/create",
        json=payload,
        params={"allowed_channels": "manual_linkedin,warm_email"},
    )
    assert resp.status_code == 422, resp.text
    body = resp.json()
    assert body["detail"]["rule"] == "channel_blocked"
    assert body["detail"]["field"] == "best_channel"


# ─────────────────────────────────────────────────────────────────────
# Total: 10 tests (3 schema + 5 validation + 2 endpoint)
# ─────────────────────────────────────────────────────────────────────
