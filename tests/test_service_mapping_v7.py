"""Tests for service_mapping_v7 (v7 Phase 5)."""
from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from api.main import create_app
from auto_client_acquisition.service_mapping_v7 import (
    MapRequest,
    map_goal_to_service,
    value_ladder,
)
from auto_client_acquisition.service_mapping_v7.schemas import FORBIDDEN_ACTIONS


@pytest.fixture(scope="module")
def client() -> TestClient:
    return TestClient(create_app())


def test_lead_intake_pain_routes_to_growth_starter():
    req = MapRequest(
        company_handle="acme_sa",
        goal_ar="نريد تحسين أوّل ردّ على العملاء",
        goal_en="we want to improve first replies",
        pain_points=["lead intake is slow", "no qualify step"],
    )
    rec = map_goal_to_service(req)
    assert rec.recommended_service == "growth_starter"
    assert rec.price_band_sar == "499"
    assert rec.approval_required is True
    assert rec.risk_level == "low"


def test_no_matching_pain_falls_back_to_diagnostic():
    req = MapRequest(
        company_handle="zeta_co",
        goal_ar="هدف عام بدون تفاصيل",
        goal_en="general goal no specifics",
        pain_points=["random unrelated thing"],
    )
    rec = map_goal_to_service(req)
    assert rec.recommended_service == "diagnostic"
    assert rec.price_band_sar == "0"


def test_excluded_actions_always_include_five_hard_rules():
    req = MapRequest(company_handle="any_co", pain_points=["weekly report for C-level"])
    rec = map_goal_to_service(req)
    for forbidden in (
        "cold_whatsapp",
        "linkedin_automation",
        "scrape_web",
        "live_charge",
        "send_email_live",
    ):
        assert forbidden in rec.excluded_actions
    # Sanity: schemas constant matches what we asserted above.
    for forbidden in FORBIDDEN_ACTIONS:
        assert forbidden in rec.excluded_actions


def test_value_ladder_has_seven_rungs():
    rungs = value_ladder()
    assert len(rungs) >= 7
    services = {r["service"] for r in rungs}
    assert "diagnostic" in services
    assert "compliance_trust_pack" in services


def test_post_recommend_v7_valid_body_returns_200(client: TestClient):
    resp = client.post(
        "/api/v1/services/recommend-v7",
        json={
            "company_handle": "acme_sa",
            "goal_en": "improve first replies and lead intake",
            "pain_points": ["lead intake"],
            "urgency": "high",
        },
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["company_handle"] == "acme_sa"
    assert body["recommended_service"] == "growth_starter"
    assert body["approval_required"] is True


def test_post_recommend_v7_empty_company_handle_returns_422(client: TestClient):
    resp = client.post(
        "/api/v1/services/recommend-v7",
        json={"company_handle": "", "pain_points": ["lead intake"]},
    )
    assert resp.status_code == 422


def test_recommendation_never_claims_guaranteed_outcomes():
    cases = [
        MapRequest(company_handle="a", pain_points=["lead intake"]),
        MapRequest(company_handle="b", pain_points=["list cleanup"]),
        MapRequest(company_handle="c", pain_points=["weekly report C-level"]),
        MapRequest(company_handle="d", pain_points=["partner channel"]),
        MapRequest(company_handle="e", pain_points=["xyz"]),
    ]
    forbidden = ("نضمن", "guaranteed")
    for req in cases:
        rec = map_goal_to_service(req)
        for field in (rec.why_ar, rec.why_en, rec.next_step):
            low = field.lower()
            for token in forbidden:
                assert token.lower() not in low, (
                    f"forbidden marketing claim {token!r} found in: {field!r}"
                )


def test_get_value_ladder_endpoint(client: TestClient):
    resp = client.get("/api/v1/services/value-ladder")
    assert resp.status_code == 200
    body = resp.json()
    assert body["n_rungs"] >= 7
    assert isinstance(body["rungs"], list)


def test_extra_field_returns_422(client: TestClient):
    resp = client.post(
        "/api/v1/services/recommend-v7",
        json={
            "company_handle": "acme",
            "rogue_field": "should_be_rejected",
        },
    )
    assert resp.status_code == 422
