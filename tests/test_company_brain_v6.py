"""Phase 3 — per-customer CompanyBrain v6 tests."""
from __future__ import annotations

from fastapi.testclient import TestClient

from api.main import create_app
from auto_client_acquisition.company_brain_v6 import (
    BuildRequest,
    CompanyBrainV6,
    build_company_brain_v6,
    next_best_action,
    recommend_service,
)
from auto_client_acquisition.company_brain_v6.service_matcher import (
    CUSTOMER_FACING_BUNDLES,
)


_FORBIDDEN = ("cold_whatsapp", "linkedin_automation", "scrape_web")


def _req(**kwargs) -> BuildRequest:
    base = {
        "company_handle": "acme",
        "sector": "b2b_services",
        "region": "ksa",
        "current_channels": ["email"],
        "allowed_channels": ["email", "phone"],
        "blocked_channels": [],
        "tone_preference": "professional",
        "language_preference": "ar",
        "pain_points": ["low conversion"],
        "growth_goal": "double pipeline in 90 days",
    }
    base.update(kwargs)
    return BuildRequest(**base)


def test_build_returns_full_structure_with_all_fields():
    brain = build_company_brain_v6(_req())
    assert isinstance(brain, CompanyBrainV6)
    assert brain.company_handle == "acme"
    assert brain.sector == "b2b_services"
    assert brain.region == "ksa"
    assert brain.offer
    assert brain.icp
    assert isinstance(brain.current_channels, list)
    assert isinstance(brain.allowed_channels, list)
    assert isinstance(brain.blocked_channels, list)
    assert brain.tone_preference == "professional"
    assert brain.language_preference == "ar"
    assert brain.pain_points == ["low conversion"]
    assert brain.growth_goal == "double pipeline in 90 days"
    assert brain.service_recommendation
    assert isinstance(brain.risk_profile, dict)
    assert brain.next_best_action
    assert isinstance(brain.evidence_ids, list)
    assert brain.generated_at is not None


def test_blocked_channels_always_contains_three_forbidden_even_if_user_allowed():
    req = _req(
        allowed_channels=[
            "email",
            "cold_whatsapp",
            "linkedin_automation",
            "scrape_web",
        ],
        blocked_channels=[],
    )
    brain = build_company_brain_v6(req)
    for ch in _FORBIDDEN:
        assert ch in brain.blocked_channels, (
            f"{ch} must be in blocked_channels even when user allowed it"
        )
        assert ch not in brain.allowed_channels, (
            f"{ch} must be removed from allowed_channels"
        )


def test_service_recommendation_is_one_of_five_customer_facing_bundles():
    for sector in (
        "b2b_services",
        "b2b_saas",
        "agency",
        "ecommerce_b2c",
        "enterprise",
    ):
        brain = build_company_brain_v6(_req(sector=sector))
        assert brain.service_recommendation in CUSTOMER_FACING_BUNDLES
    assert len(CUSTOMER_FACING_BUNDLES) == 5


def test_unknown_sector_falls_back_to_growth_starter():
    brain = build_company_brain_v6(_req(sector="space_tourism"))
    assert recommend_service(brain) == "growth_starter"
    assert brain.service_recommendation == "growth_starter"


def test_markdown_does_not_contain_forbidden_marketing_terms():
    brain = build_company_brain_v6(_req())
    md = brain.as_markdown().lower()
    md_raw = brain.as_markdown()
    assert "نضمن" not in md_raw
    assert "guaranteed" not in md
    assert "blast" not in md
    assert "scrape" not in md


def test_router_post_build_with_valid_payload_returns_200():
    client = TestClient(create_app())
    resp = client.post(
        "/api/v1/company-brain-v6/build",
        json={
            "company_handle": "acme",
            "sector": "b2b_services",
            "growth_goal": "double pipeline",
        },
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["company_handle"] == "acme"
    assert body["service_recommendation"] in CUSTOMER_FACING_BUNDLES
    for ch in _FORBIDDEN:
        assert ch in body["blocked_channels"]


def test_router_post_build_with_empty_company_handle_returns_422():
    client = TestClient(create_app())
    resp = client.post(
        "/api/v1/company-brain-v6/build",
        json={"company_handle": ""},
    )
    assert resp.status_code == 422


def test_next_best_action_mentions_approval_required_language():
    brain = build_company_brain_v6(_req())
    nba = next_best_action(brain)
    assert "approval_required" in nba
    assert brain.next_best_action == nba


def test_router_status_advertises_guardrails():
    client = TestClient(create_app())
    resp = client.get("/api/v1/company-brain-v6/status")
    assert resp.status_code == 200
    body = resp.json()
    assert body["module"] == "company_brain_v6"
    assert body["guardrails"]["no_llm_calls"] is True
    assert body["guardrails"]["no_external_http"] is True
    assert body["guardrails"]["approval_required"] is True


def test_router_service_match_and_next_action_endpoints():
    client = TestClient(create_app())
    payload = {"company_handle": "acme", "sector": "agency"}
    sm = client.post("/api/v1/company-brain-v6/service-match", json=payload)
    assert sm.status_code == 200
    assert sm.json()["recommended_service"] in CUSTOMER_FACING_BUNDLES

    na = client.post("/api/v1/company-brain-v6/next-action", json=payload)
    assert na.status_code == 200
    assert "approval_required" in na.json()["next_best_action"]


def test_build_request_extra_forbidden():
    import pytest
    from pydantic import ValidationError

    with pytest.raises(ValidationError):
        BuildRequest(company_handle="acme", unknown_field="x")
