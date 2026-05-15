"""Governance OS — unified policy_check facade."""

from __future__ import annotations

from auto_client_acquisition.governance_os import (
    PolicyVerdict,
    policy_check_draft,
    run_policy_check,
)
from auto_client_acquisition.revenue_os import Tier1LeadSource


def test_policy_check_draft_blocks_cold_whatsapp() -> None:
    r = policy_check_draft("We will run cold whatsapp blast for you")
    assert r.allowed is False
    assert r.verdict == PolicyVerdict.BLOCK
    assert any("cold" in x.lower() or "whatsapp" in x.lower() for x in r.issues)


def test_policy_check_draft_allows_neutral() -> None:
    r = policy_check_draft("نراجع قائمة الحسابات بعد موافقتكم على النطاق.")
    assert r.allowed is True
    assert not r.issues


def test_run_policy_check_merges_draft_and_intake() -> None:
    source = Tier1LeadSource.CRM_IMPORT.value
    r = run_policy_check(
        draft_text="This is a safe draft for review.",
        lead_source=source,
    )
    assert r.allowed is True


def test_run_policy_check_fails_on_bad_source() -> None:
    r = run_policy_check(lead_source="unknown_source_xyz")
    assert r.allowed is False
