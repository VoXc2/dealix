"""Claim policy — doctrine reason integrity + free-text claim scanning."""

from __future__ import annotations

import pytest

from auto_client_acquisition.policy_config import load_policy
from auto_client_acquisition.policy_config.claim_guard import (
    claim_is_publishable,
    scan_claim,
)
from auto_client_acquisition.safe_send_gateway import doctrine

_BASE_CODES = (
    "no_cold_whatsapp",
    "no_linkedin_automation",
    "no_scraping",
    "no_bulk_outreach",
    "no_guaranteed_sales_claims",
    "no_fake_proof",
    "external_action_requires_approval",
)


def test_all_seven_doctrine_codes_present_and_bilingual() -> None:
    codes = load_policy("claim_policy")["codes"]
    for code in _BASE_CODES:
        spec = codes[code]
        assert spec["non_negotiable"] is True
        assert spec["ar"].strip()
        assert spec["en"].strip()


def test_dropping_a_code_from_config_hard_fails_not_silently_passes(monkeypatch) -> None:
    """Config can never silently remove a guard — a missing code must raise."""
    full = load_policy("claim_policy")
    crippled = {**full, "codes": {k: v for k, v in full["codes"].items() if k != "no_scraping"}}
    monkeypatch.setattr(doctrine, "load_policy", lambda _name: crippled)
    with pytest.raises(ValueError, match="doctrine_codes_missing:no_scraping"):
        doctrine.enforce_doctrine_non_negotiables(request_scraping=True)


def test_doctrine_still_raises_on_violation() -> None:
    with pytest.raises(ValueError, match="doctrine_violations"):
        doctrine.enforce_doctrine_non_negotiables(request_cold_whatsapp=True)


def test_scan_claim_flags_guaranteed_revenue() -> None:
    findings = scan_claim("our agents deliver guaranteed revenue for clients")
    blocked = {f.keyword for f in findings if f.severity == "blocked_without_source"}
    assert "guaranteed revenue" in blocked
    assert claim_is_publishable("guaranteed revenue") is False


def test_sourced_claim_is_publishable_but_topic_still_needs_approval() -> None:
    text = "our security review process is documented"
    assert claim_is_publishable(text, has_source=True) is True
    severities = {f.severity for f in scan_claim(text, has_source=True)}
    assert "requires_approval" in severities  # "security" topic


def test_neutral_copy_has_no_findings() -> None:
    assert scan_claim("we help teams organise their pipeline") == ()
