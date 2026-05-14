"""The M&A playbook enumerates the required artifact for each stage.
If a future commit drops a required artifact, this test fails.
"""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PLAYBOOK = REPO_ROOT / "docs" / "holding" / "MA_PLAYBOOK.md"
THESIS = REPO_ROOT / "docs" / "holding" / "ACQUISITION_THESIS.md"
ONBOARDING = REPO_ROOT / "docs" / "holding" / "SUBSIDIARY_ONBOARDING.md"


def test_all_three_lifecycle_docs_exist():
    for p in (PLAYBOOK, THESIS, ONBOARDING):
        assert p.exists(), f"missing: {p}"


def test_playbook_lists_six_stages():
    text = PLAYBOOK.read_text(encoding="utf-8")
    for stage in (
        "Stage 1 — Thesis",
        "Stage 2 — Screen",
        "Stage 3 — Diligence",
        "Stage 4 — Letter of Intent",
        "Stage 5 — Close",
        "Stage 6 — Post-Close",
    ):
        assert stage in text, f"M&A playbook missing: {stage}"


def test_playbook_close_stage_requires_charter_and_capital_asset():
    text = PLAYBOOK.read_text(encoding="utf-8")
    # Stage 5 specifically requires registering the BU + capital asset.
    assert "register_business_unit.py" in text
    assert "Capital Asset" in text
    assert "Doctrine adoption" in text or "DOCTRINE_ADOPTION_CHECKLIST" in text


def test_acquisition_thesis_lists_four_criteria_and_non_criteria():
    text = THESIS.read_text(encoding="utf-8")
    for criterion in (
        "Doctrine compatibility",
        "Evidence inheritability",
        "Sector fit",
        "Capital fit",
    ):
        assert criterion in text
    assert "Non-Criteria" in text or "do **not**" in text or "do not" in text.lower()


def test_subsidiary_onboarding_lists_30_60_90_milestones():
    text = ONBOARDING.read_text(encoding="utf-8")
    assert "Day 0" in text
    assert "1–30" in text or "1-30" in text or "30" in text
    assert "31–60" in text or "31-60" in text or "60" in text
    assert "61–90" in text or "61-90" in text or "90" in text
    assert "Trust Pack" in text
    assert "Capital Asset" in text
    assert "Proof Pack" in text


def test_onboarding_blocks_external_action_before_day_30_gates():
    text = ONBOARDING.read_text(encoding="utf-8")
    assert "Forbidden" in text
    assert "external action" in text.lower() or "may not" in text.lower()


def test_bu_kill_rules_match_test_exists():
    """Companion safety: the parity test file must exist (PR14)."""
    p = REPO_ROOT / "tests" / "test_bu_kill_rules_match_unit_governance.py"
    assert p.exists()
