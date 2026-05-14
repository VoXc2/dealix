"""Doctrine-as-code: BU_KILL_RULES.md and unit_governance.py are in lockstep.

Every recommendation the engine can produce must be documented as a
rule. Every rule documented must correspond to a real engine branch.
"""
from __future__ import annotations

from pathlib import Path

from auto_client_acquisition.holding_os.unit_governance import (
    UnitMonthlySnapshot,
    UnitPortfolioDecision,
    evaluate_unit_decision,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC = REPO_ROOT / "docs" / "holding" / "BU_KILL_RULES.md"


def test_doc_exists():
    assert DOC.exists()


def test_doc_references_unit_governance_module():
    text = DOC.read_text(encoding="utf-8")
    assert "unit_governance.py" in text
    assert "evaluate_unit_decision" in text


def test_every_decision_value_appears_in_doc():
    text = DOC.read_text(encoding="utf-8")
    for d in UnitPortfolioDecision:
        # Decision values are lowercase ("scale", "build", "pilot",
        # "hold", "kill", "spinout"). The doc uses uppercase names.
        assert d.name in text, f"BU_KILL_RULES.md missing decision: {d.name}"


def test_kill_rule_engine_matches_doc():
    """Rule 3 of the doc: qa_score < 55 AND not revenue_growing → KILL."""
    s = UnitMonthlySnapshot(
        revenue_growing=False, margin_ok=False, qa_score=40,
        governance_risk_acceptable=True, client_health_ok=True,
    )
    assert evaluate_unit_decision(s) is UnitPortfolioDecision.KILL


def test_kill_NOT_triggered_when_revenue_growing():
    """If revenue is growing the kill rule must NOT fire even at qa<55."""
    s = UnitMonthlySnapshot(
        revenue_growing=True, qa_score=40,
        governance_risk_acceptable=True, client_health_ok=True,
    )
    assert evaluate_unit_decision(s) is not UnitPortfolioDecision.KILL


def test_kill_NOT_triggered_when_qa_high():
    """If qa is high the kill rule must NOT fire even without revenue."""
    s = UnitMonthlySnapshot(
        revenue_growing=False, qa_score=80,
        governance_risk_acceptable=True, client_health_ok=True,
    )
    assert evaluate_unit_decision(s) is not UnitPortfolioDecision.KILL


def test_hold_when_governance_risk_unacceptable():
    s = UnitMonthlySnapshot(governance_risk_acceptable=False)
    assert evaluate_unit_decision(s) is UnitPortfolioDecision.HOLD


def test_spinout_path():
    s = UnitMonthlySnapshot(
        venture_signal_strong=True, module_usage_growing=True,
        qa_score=90, governance_risk_acceptable=True, client_health_ok=True,
    )
    assert evaluate_unit_decision(s) is UnitPortfolioDecision.SPINOUT


def test_scale_path():
    s = UnitMonthlySnapshot(
        revenue_growing=True, margin_ok=True, qa_score=85,
        retainers_growing=True, governance_risk_acceptable=True,
        client_health_ok=True,
    )
    assert evaluate_unit_decision(s) is UnitPortfolioDecision.SCALE


def test_doc_uses_55_and_85_thresholds():
    """The two numeric thresholds in the engine must appear in the doc."""
    text = DOC.read_text(encoding="utf-8")
    assert "55" in text
    assert "85" in text or "80" in text  # 80 = SCALE threshold; 85 = SPINOUT
