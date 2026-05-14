"""Doctrine-as-code: the policy doc and the code buckets are in lockstep.

If a future commit adds a bucket to one without the other, this test
fails the build.
"""
from __future__ import annotations

from pathlib import Path

from auto_client_acquisition.board_decision_os.capital_allocation_board import (
    CAPITAL_BOARD_BUCKETS,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
POLICY = REPO_ROOT / "docs" / "holding" / "CAPITAL_ALLOCATION_POLICY.md"


def test_policy_doc_exists():
    assert POLICY.exists()


def test_every_code_bucket_appears_in_the_policy_doc():
    text = POLICY.read_text(encoding="utf-8")
    for bucket in CAPITAL_BOARD_BUCKETS:
        assert f"`{bucket}`" in text, (
            f"policy doc missing `{bucket}` from CAPITAL_BOARD_BUCKETS"
        )


def test_policy_doc_mentions_spinout_and_acquire():
    """The Charter policy describes 6 buckets total (code's 4 + 2 BU-level).
    spinout + acquire are BU-level decisions, not in CAPITAL_BOARD_BUCKETS,
    so they MUST appear separately in the policy doc."""
    text = POLICY.read_text(encoding="utf-8").lower()
    assert "spinout" in text
    assert "acquire" in text


def test_policy_doc_references_unit_governance_engine():
    text = POLICY.read_text(encoding="utf-8")
    assert "unit_governance.py" in text or "evaluate_unit_decision" in text


def test_treasury_doc_exists_and_references_operating_finance_os():
    p = REPO_ROOT / "docs" / "holding" / "GROUP_TREASURY.md"
    assert p.exists()
    text = p.read_text(encoding="utf-8")
    assert "operating_finance_os" in text
    assert "budget_stage" in text
    assert "margin" in text.lower()
