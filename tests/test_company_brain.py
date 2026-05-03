"""Company Brain — sanity tests."""

from __future__ import annotations

import asyncio

from auto_client_acquisition.customer_ops import (
    BrainSource,
    build_company_brain,
    build_demo_company_brain,
)


def test_demo_brain_has_all_keys() -> None:
    b = build_demo_company_brain("cust_demo")
    expected = {
        "customer_id", "source", "company_name", "website", "sector", "city",
        "offer", "icp", "language_preference", "tone_preference",
        "approved_channels", "blocked_channels", "consent_records",
        "current_service", "open_decisions", "proof_summary",
        "past_objections", "next_best_actions",
    }
    assert expected.issubset(set(b.keys()))
    assert b["source"] == BrainSource.DEMO.value


def test_demo_brain_blocked_channels_include_cold_whatsapp() -> None:
    b = build_demo_company_brain()
    assert "cold_whatsapp" in b["blocked_channels"]
    assert "linkedin_automation" in b["blocked_channels"]
    assert "purchased_lists_whatsapp" in b["blocked_channels"]


def test_demo_brain_proof_summary_exists() -> None:
    b = build_demo_company_brain()
    assert "proof_summary" in b
    assert "rwus_emitted" in b["proof_summary"]


def test_demo_brain_default_language_and_tone_are_saudi_friendly() -> None:
    b = build_demo_company_brain()
    assert b["language_preference"] == "ar"
    assert b["tone_preference"] == "professional_khaliji"


def test_demo_brain_next_actions_are_safe_only() -> None:
    b = build_demo_company_brain()
    nbas = b["next_best_actions"]
    assert nbas, "must have at least one next best action"
    # No NBA should suggest cold whatsapp / automation
    for a in nbas:
        title = (a.get("title_ar") or "") + " " + (a.get("title_en") or "")
        low = title.lower()
        assert "cold" not in low and "بارد" not in low
        assert "blast" not in low and "بالكوم" not in low


def test_build_company_brain_no_session_falls_back_to_demo() -> None:
    b = asyncio.run(build_company_brain("cust_unknown_for_test", session=None))
    assert b["customer_id"] == "cust_unknown_for_test"
    assert b["source"] == BrainSource.DEMO.value


def test_build_company_brain_rejects_empty_id() -> None:
    import pytest
    with pytest.raises(ValueError):
        asyncio.run(build_company_brain("", session=None))
