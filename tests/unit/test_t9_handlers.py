"""Unit tests for the T9 skill handlers (LLM + data-backed)."""

from __future__ import annotations

import asyncio

# Trigger registration side-effects.
from dealix.agents.skills import handlers_data, handlers_llm  # noqa: F401
from dealix.agents.skills.handlers import get_handler, registered_ids


def test_all_twelve_handlers_registered() -> None:
    ids = set(registered_ids())
    expected = {
        # T8a
        "sales_qualifier",
        "lead_scorer",
        "content_generator_ar",
        "ar_en_translator",
        # T9 LLM-backed
        "proposal_writer",
        "email_triage",
        "contract_analyst",
        "meeting_summarizer",
        # T9 data-backed
        "crm_syncer",
        "market_researcher",
        "renewal_forecaster",
        "compliance_reviewer",
    }
    assert expected <= ids


def test_proposal_writer_includes_vat_and_zatca() -> None:
    handler = get_handler("proposal_writer")
    res = asyncio.run(handler({"pricing_plan_id": "growth", "locale": "ar"}))
    assert res["currency"] == "SAR"
    assert res["vat_amount"] > 0
    assert res["grand_total"] == res["annual_subtotal"] + res["vat_amount"]
    assert "ZATCA" in res["proposal_body"]


def test_proposal_writer_english_locale() -> None:
    handler = get_handler("proposal_writer")
    res = asyncio.run(handler({"pricing_plan_id": "enterprise", "locale": "en", "lead": {"company": "Acme"}}))
    assert "ZATCA" in res["proposal_body"]
    assert "Acme" in res["proposal_body"]
    assert res["plan"] == "enterprise"


def test_email_triage_detects_demo_request_en() -> None:
    handler = get_handler("email_triage")
    res = asyncio.run(handler({"subject": "Demo request", "text": "Can we schedule a demo this week?"}))
    assert res["bucket"] == "demo_request"
    assert res["language"] == "en"
    assert res["confidence"] > 0


def test_email_triage_detects_demo_request_ar() -> None:
    handler = get_handler("email_triage")
    res = asyncio.run(handler({"subject": "عرض ديمو", "text": "نود ترتيب عرض توضيحي."}))
    assert res["bucket"] == "demo_request"
    assert res["language"] == "ar"


def test_email_triage_falls_back_to_general() -> None:
    handler = get_handler("email_triage")
    res = asyncio.run(handler({"text": "Hello, hope you are well."}))
    assert res["bucket"] == "general_inquiry"


def test_email_triage_detects_spam() -> None:
    handler = get_handler("email_triage")
    res = asyncio.run(handler({"text": "$$$ Great deal !!! Make money fast !!!!"}))
    assert res["bucket"] == "spam"


def test_contract_analyst_flags_unlimited_liability() -> None:
    handler = get_handler("contract_analyst")
    res = asyncio.run(handler({"text": "Customer agrees to unlimited liability for damages."}))
    assert any(f["label"] == "unlimited_liability" for f in res["risk_flags"])
    assert res["summary_recommendation"] == "block_for_legal_review"
    assert res["high_severity_count"] >= 1


def test_contract_analyst_clean_text_passes() -> None:
    handler = get_handler("contract_analyst")
    res = asyncio.run(handler({"text": "Standard clean contract. SAR 100,000 fee."}))
    assert res["risk_flags"] == []
    assert res["summary_recommendation"] == "ok_for_signature"
    assert "SAR 100,000" in res["extracted_amounts"][0] or "SAR" in res["extracted_amounts"][0]


def test_meeting_summarizer_extracts_actions() -> None:
    handler = get_handler("meeting_summarizer")
    transcript = (
        "We discussed pricing. The customer needs a follow-up call by Friday. "
        "We will send a revised proposal."
    )
    res = asyncio.run(handler({"transcript": transcript, "locale": "en"}))
    assert len(res["action_items"]) >= 1
    assert res["language"] == "en"


def test_crm_syncer_no_hubspot_key_returns_reason() -> None:
    handler = get_handler("crm_syncer")
    res = asyncio.run(handler({"lead": {"full_name": "Test"}, "target": "hubspot", "action": "create"}))
    # Without HUBSPOT_API_KEY in env, must return the documented reason.
    if res["ok"]:
        # If a real key is present in the test env, we just confirm the
        # shape is sane and skip the negative-path assertion.
        assert "target" in res
    else:
        assert res["reason"] in {"hubspot_not_configured", "lead_shape_mismatch", "hubspot_error:" + res.get("reason", "").split(":", 1)[-1]} or res["reason"].startswith("hubspot_")


def test_crm_syncer_salesforce_not_implemented() -> None:
    handler = get_handler("crm_syncer")
    res = asyncio.run(handler({"target": "salesforce", "action": "create"}))
    assert res["ok"] is False
    assert res["reason"] == "salesforce_not_implemented"


def test_market_researcher_degrades_without_keys() -> None:
    handler = get_handler("market_researcher")
    res = asyncio.run(handler({"cr_number": "1010101010", "tadawul_symbol": "2222"}))
    # Without any vendor keys, sources is empty but the brief still returns.
    assert isinstance(res["_meta"]["sources"], list)
    assert "data" in res


def test_renewal_forecaster_high_risk() -> None:
    handler = get_handler("renewal_forecaster")
    res = asyncio.run(handler({
        "tenant_id": "ten_at_risk",
        "health_score": 0.2,
        "usage_trend": "declining",
        "last_nps": -30,
        "days_to_renewal": 10,
    }))
    assert res["bucket"] == "high"
    assert res["recommended_action"] == "escalate_to_csm_now"


def test_renewal_forecaster_low_risk() -> None:
    handler = get_handler("renewal_forecaster")
    res = asyncio.run(handler({
        "tenant_id": "ten_healthy",
        "health_score": 0.95,
        "usage_trend": "rising",
        "last_nps": 75,
        "days_to_renewal": 200,
    }))
    assert res["bucket"] == "low"
    assert res["recommended_action"] == "monitor"


def test_compliance_reviewer_pii_detected() -> None:
    handler = get_handler("compliance_reviewer")
    res = asyncio.run(handler({"text": "Call me at +966500000001 or email test@x.sa", "purpose": "support"}))
    assert res["compliant"] is False
    kinds = {f["kind"] for f in res["violations"]}
    assert "ksa_phone" in kinds
    assert "email" in kinds


def test_compliance_reviewer_marketing_without_consent() -> None:
    handler = get_handler("compliance_reviewer")
    res = asyncio.run(handler({"text": "Buy now", "purpose": "marketing", "has_consent": False}))
    assert res["compliant"] is False
    types = {f["type"] for f in res["violations"]}
    assert "pdpl_violation" in types
    assert res["recommendation"] == "block_send"


def test_compliance_reviewer_marketing_with_consent_passes() -> None:
    handler = get_handler("compliance_reviewer")
    res = asyncio.run(handler({"text": "New feature update.", "purpose": "marketing", "has_consent": True}))
    assert res["compliant"] is True
    assert res["recommendation"] == "ok_to_send"
