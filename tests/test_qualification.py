"""Sales qualification scorer — deterministic decision tree."""
from __future__ import annotations

from auto_client_acquisition.sales_os.qualification import (
    QualificationVerdict as Decision,
    qualify,
)


def _all_yes() -> dict:
    return dict(
        pain_clear=True, owner_present=True, data_available=True,
        accepts_governance=True, has_budget=True, wants_safe_methods=True,
        proof_path_visible=True, retainer_path_visible=True,
    )


def test_full_yes_accepts():
    r = qualify(**_all_yes())
    assert r.decision == Decision.ACCEPT
    assert r.score == 100
    assert "revenue_intelligence_sprint" in r.recommended_offer or "data_to_revenue" in r.recommended_offer


def test_cold_whatsapp_request_rejected():
    args = _all_yes()
    args["raw_request_text"] = "We want cold WhatsApp automation to blast leads"
    r = qualify(**args)
    assert r.decision == Decision.REJECT
    assert any("whatsapp" in v for v in r.doctrine_violations)


def test_arabic_guarantee_rejected():
    args = _all_yes()
    args["raw_request_text"] = "نريد ضمان المبيعات في 30 يوم"
    r = qualify(**args)
    assert r.decision == Decision.REJECT
    assert any("guaranteed_sales" in v for v in r.doctrine_violations)


def test_scraping_rejected():
    args = _all_yes()
    args["raw_request_text"] = "Can you scrape LinkedIn for us?"
    r = qualify(**args)
    assert r.decision == Decision.REJECT


def test_missing_data_diagnostic_only():
    args = _all_yes()
    args["data_available"] = False
    args["owner_present"] = False
    r = qualify(**args)
    # Score around 70 — DIAGNOSTIC_ONLY territory
    assert r.decision in {Decision.DIAGNOSTIC_ONLY, Decision.REFRAME}


def test_low_score_refer_out():
    r = qualify(
        pain_clear=False, owner_present=False, data_available=False,
        accepts_governance=True, has_budget=False, wants_safe_methods=True,
        proof_path_visible=False, retainer_path_visible=False,
    )
    assert r.decision in {Decision.REJECT, Decision.REFER_OUT}


def test_no_safe_methods_adds_doctrine_flag():
    args = _all_yes()
    args["wants_safe_methods"] = False
    r = qualify(**args)
    # When wants_safe_methods=False without explicit doctrine text, we soft-flag
    assert r.decision == Decision.REJECT
    assert "declined_safe_methods" in r.doctrine_violations
