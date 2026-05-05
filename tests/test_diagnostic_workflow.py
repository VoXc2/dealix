"""Tests for auto_client_acquisition.diagnostic_workflow.

Pure local composition: no LLM, no live sends, no charge. Pilot price
is FIXED at 499 SAR. Raw email/phone must never appear in the parsed
record. Forbidden marketing tokens must never appear in any rendered
bilingual string.
"""
from __future__ import annotations

import re

import pytest
from fastapi.testclient import TestClient

from api.main import create_app
from auto_client_acquisition.company_brain_v6.service_matcher import (
    CUSTOMER_FACING_BUNDLES,
)
from auto_client_acquisition.diagnostic_workflow import (
    DiagnosticBundle,
    IntakeRecord,
    IntakeRequest,
    PilotOffer,
    ProofPlan,
    build_delivery_plan_for_recommendation,
    build_diagnostic,
    build_pilot_offer,
    build_proof_plan,
    parse_intake,
    recommend_service,
)
from auto_client_acquisition.proof_ledger import ProofEventType


# Marketing-claim tokens (positive phrasing — what we MUST never say).
# We do NOT scan for bare "scraping" / "cold X" because the upstream
# diagnostic brief renders the NEGATIVE phrasing ("No scraping", "No
# cold WhatsApp") explicitly to communicate guardrails. Mirrors the
# strict-match list used by tests/test_diagnostic_engine.py.
_FORBIDDEN_TOKENS: tuple[re.Pattern, ...] = (
    re.compile(r"نضمن لكم"),
    re.compile(r"\bguaranteed\s+(revenue|ranking|results)\b", re.IGNORECASE),
    re.compile(r"\bblast\b", re.IGNORECASE),
    re.compile(r"\b(we\s+)?scrape\b", re.IGNORECASE),
)


def _no_forbidden(text: str) -> bool:
    for pat in _FORBIDDEN_TOKENS:
        if pat.search(text):
            return False
    return True


@pytest.fixture(scope="module")
def client() -> TestClient:
    return TestClient(create_app())


def test_parse_intake_anonymizes_contact_handle():
    """Even if the founder accidentally pastes a raw email, the parsed
    record must NOT echo it back. ``customer_handle`` becomes a derived
    placeholder; ``contact_handle`` is forced to a static placeholder."""
    raw_email = "founder@example.com"
    req = IntakeRequest(
        company="ACME Saudi Co.",
        sector="b2b_services",
        contact_handle=raw_email,
    )
    record = parse_intake(req)
    assert isinstance(record, IntakeRecord)
    dumped = record.model_dump_json()
    assert raw_email not in dumped
    assert record.contact_handle == "PLACEHOLDER-HANDLE"
    # Period is stripped by the safe-token filter, spaces become dashes.
    assert record.customer_handle == "ACME-SAUDI-CO-PILOT-PLACEHOLDER"
    assert record.consent_recorded is False
    assert record.intake_id.startswith("intake_")


def test_build_diagnostic_returns_full_bundle_with_approval_required():
    record = parse_intake(
        IntakeRequest(
            company="ACME",
            sector="b2b_services",
            pipeline_state="WhatsApp incoming, founder responds at night.",
        )
    )
    bundle = build_diagnostic(record)
    assert isinstance(bundle, DiagnosticBundle)
    assert bundle.company == "ACME"
    assert bundle.recommended_bundle in CUSTOMER_FACING_BUNDLES
    assert bundle.approval_status == "approval_required"
    assert bundle.brief_markdown_ar_en
    assert len(bundle.gaps) >= 3
    assert bundle.brain.company_handle.endswith("-PILOT-PLACEHOLDER")


def test_recommend_service_returns_one_of_five_bundles():
    record = parse_intake(IntakeRequest(company="ACME", sector="agency"))
    bundle = build_diagnostic(record)
    result = recommend_service(bundle)
    assert result in CUSTOMER_FACING_BUNDLES
    assert len(CUSTOMER_FACING_BUNDLES) == 5


def test_pilot_offer_is_exactly_499_sar():
    record = parse_intake(IntakeRequest(company="ACME"))
    bundle = build_diagnostic(record)
    offer = build_pilot_offer(bundle)
    assert isinstance(offer, PilotOffer)
    assert offer.amount_sar == 499
    # Literal[499] enforces this — assigning anything else must raise.
    with pytest.raises(Exception):
        PilotOffer(
            company="X",
            recommended_bundle="growth_starter",
            amount_sar=500,  # type: ignore[arg-type]
            description_ar="x",
            description_en="x",
            terms_ar="x",
            terms_en="x",
        )


def test_pilot_description_in_both_languages_no_forbidden_tokens():
    record = parse_intake(IntakeRequest(company="ACME"))
    bundle = build_diagnostic(record)
    offer = build_pilot_offer(bundle)
    # Bilingual: Arabic chars in AR fields, English-language markers in EN.
    assert any("؀" <= ch <= "ۿ" for ch in offer.description_ar)
    assert any("؀" <= ch <= "ۿ" for ch in offer.terms_ar)
    assert "pilot" in offer.description_en.lower()
    assert "Moyasar" in offer.terms_en
    # No forbidden marketing claims anywhere.
    for txt in (
        offer.description_ar,
        offer.description_en,
        offer.terms_ar,
        offer.terms_en,
    ):
        assert _no_forbidden(txt), f"forbidden token found in: {txt}"


def test_proof_plan_lists_at_least_three_proof_event_types():
    record = parse_intake(IntakeRequest(company="ACME"))
    bundle = build_diagnostic(record)
    plan = build_proof_plan(record, bundle.recommended_bundle)
    assert isinstance(plan, ProofPlan)
    assert len(plan.expected_proof_events) >= 3
    valid = {e.value for e in ProofEventType}
    for evt in plan.expected_proof_events:
        assert evt in valid, f"unknown proof event {evt}"
    assert plan.publishable_with_consent is False
    assert plan.summary_ar
    assert plan.summary_en


def test_delivery_plan_for_recommendation_returns_dict_for_real_bundle():
    record = parse_intake(IntakeRequest(company="ACME", sector="b2b_services"))
    bundle = build_diagnostic(record)
    plan = build_delivery_plan_for_recommendation(bundle.recommended_bundle)
    assert isinstance(plan, dict)
    assert plan["bundle"] == bundle.recommended_bundle
    assert plan["service_id"]
    assert plan["approval_required"] is True


def test_router_intake_with_valid_payload_returns_200(client: TestClient):
    resp = client.post(
        "/api/v1/diagnostic-workflow/intake",
        json={
            "company": "ACME Saudi",
            "sector": "b2b_services",
            "contact_handle": "PUBLIC-HANDLE-001",
            "pipeline_state": "warm intro from partner",
        },
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["company"] == "ACME Saudi"
    assert body["customer_handle"] == "ACME-SAUDI-PILOT-PLACEHOLDER"
    assert body["consent_recorded"] is False


def test_router_intake_with_empty_company_returns_422(client: TestClient):
    resp = client.post(
        "/api/v1/diagnostic-workflow/intake",
        json={"company": "", "sector": "b2b_services"},
    )
    assert resp.status_code == 422


def test_router_pilot_offer_triggers_full_pipeline(client: TestClient):
    resp = client.post(
        "/api/v1/diagnostic-workflow/pilot-offer",
        json={
            "company": "ACME Saudi",
            "sector": "b2b_services",
            "pipeline_state": "WhatsApp incoming, founder responds at night.",
        },
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["company"] == "ACME Saudi"
    assert body["amount_sar"] == 499
    assert body["recommended_bundle"] in CUSTOMER_FACING_BUNDLES
    assert body["payment_url"] is None


def test_router_status_reports_guardrails(client: TestClient):
    resp = client.get("/api/v1/diagnostic-workflow/status")
    assert resp.status_code == 200
    body = resp.json()
    assert body["module"] == "diagnostic_workflow"
    g = body["guardrails"]
    assert g["no_llm_calls"] is True
    assert g["no_live_sends"] is True
    assert g["pilot_price_locked_499_sar"] is True
    assert g["no_raw_email_or_phone"] is True


def test_module_never_produces_forbidden_marketing_token():
    """End-to-end sweep: across every bilingual string the workflow
    can render, NO forbidden marketing token appears."""
    record = parse_intake(
        IntakeRequest(
            company="ACME Saudi",
            sector="b2b_services",
            pipeline_state="founder responds manually at night",
        )
    )
    bundle = build_diagnostic(record)
    offer = build_pilot_offer(bundle)
    plan = build_proof_plan(record, bundle.recommended_bundle)

    rendered_strings: list[str] = [
        bundle.brief_markdown_ar_en,
        bundle.brain.as_markdown(),
        offer.description_ar,
        offer.description_en,
        offer.terms_ar,
        offer.terms_en,
        plan.summary_ar,
        plan.summary_en,
    ]
    for txt in rendered_strings:
        assert _no_forbidden(txt), f"forbidden token in rendered text: {txt[:120]!r}"


def test_router_extra_field_returns_422(client: TestClient):
    """IntakeRequest is extra='forbid'; rogue fields must 422."""
    resp = client.post(
        "/api/v1/diagnostic-workflow/intake",
        json={"company": "ACME", "rogue": "no"},
    )
    assert resp.status_code == 422
