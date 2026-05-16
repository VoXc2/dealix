"""Governed Value Decisions ledger — the North Star metric."""

from __future__ import annotations

import importlib

import pytest


@pytest.fixture()
def ledger(tmp_path, monkeypatch):
    """Reload the ledger module bound to an isolated tmp JSONL path."""
    path = tmp_path / "governed-decisions.jsonl"
    monkeypatch.setenv("DEALIX_GOVERNED_DECISIONS_PATH", str(path))
    import auto_client_acquisition.governed_value_os.decisions_ledger as mod

    return importlib.reload(mod)


def _valid_kwargs(**over):
    base = dict(
        summary="Follow up 7 high-value accounts",
        decision_kind="revenue_followup",
        source_ref="crm_export_2026_05",
        approval_ref="approval_center:appr_001",
        evidence_refs=("evt_l4_001",),
        value_estimate_sar=12000.0,
    )
    base.update(over)
    return base


def test_record_and_count(ledger) -> None:
    assert ledger.count_decisions() == 0
    d = ledger.record_decision(**_valid_kwargs())
    assert d.decision_id.startswith("gvd_")
    assert d.is_estimate is True
    assert ledger.count_decisions() == 1
    assert ledger.list_decisions()[-1].summary.startswith("Follow up")


def test_rejects_missing_source(ledger) -> None:
    with pytest.raises(ValueError, match="source_ref"):
        ledger.record_decision(**_valid_kwargs(source_ref="  "))


def test_rejects_missing_approval(ledger) -> None:
    with pytest.raises(ValueError, match="approval_ref"):
        ledger.record_decision(**_valid_kwargs(approval_ref=""))


def test_rejects_missing_evidence(ledger) -> None:
    with pytest.raises(ValueError, match="evidence_refs"):
        ledger.record_decision(**_valid_kwargs(evidence_refs=()))
    with pytest.raises(ValueError, match="evidence_refs"):
        ledger.record_decision(**_valid_kwargs(evidence_refs=("", "  ")))


def test_rejects_negative_value(ledger) -> None:
    with pytest.raises(ValueError, match="value_estimate_sar"):
        ledger.record_decision(**_valid_kwargs(value_estimate_sar=-1.0))


def test_multiple_decisions_preserve_evidence_tuple(ledger) -> None:
    ledger.record_decision(**_valid_kwargs(evidence_refs=("a", "b")))
    ledger.record_decision(**_valid_kwargs(summary="Stop a risky workflow"))
    decisions = ledger.list_decisions()
    assert len(decisions) == 2
    assert decisions[0].evidence_refs == ("a", "b")
    assert isinstance(decisions[1].evidence_refs, tuple)
