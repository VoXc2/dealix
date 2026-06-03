"""Governance OS — draft text and intake gates."""

from __future__ import annotations

from auto_client_acquisition.governance_os import audit_draft_text, intake_violations_for_source


def test_audit_draft_detects_scraping_word() -> None:
    assert any("scraping" in x for x in audit_draft_text("We will do scraping for leads"))


def test_intake_blocks_scraping_tier1() -> None:
    v = intake_violations_for_source("scraping")
    assert v and any("blocked" in x.lower() or "blocked_source" in x for x in v)


def test_intake_allows_warm_intro() -> None:
    assert intake_violations_for_source("warm_intro") == []


def test_intake_unknown_source_flagged() -> None:
    v = intake_violations_for_source("not_a_real_tier1_enum_value")
    assert any("unknown_tier1" in x for x in v)
