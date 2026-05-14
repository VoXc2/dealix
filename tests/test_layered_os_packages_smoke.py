"""Smoke: layered proof/value/capital packages import cleanly."""

from __future__ import annotations

from auto_client_acquisition.capital_os.capital_ledger import CapitalLedgerEvent, capital_ledger_event_valid
from auto_client_acquisition.proof_os.proof_pack import build_empty_proof_pack_v2, proof_pack_v2_sections_complete
from auto_client_acquisition.value_os.value_ledger import ValueLedgerEvent, value_ledger_event_valid


def test_proof_os_empty_pack_incomplete() -> None:
    ok, missing = proof_pack_v2_sections_complete(build_empty_proof_pack_v2())
    assert not ok
    assert "executive_summary" in missing


def test_value_ledger_event_roundtrip() -> None:
    e = ValueLedgerEvent(
        value_event_id="v1",
        project_id="p",
        client_id="c",
        value_type="observed",
        metric="accounts_ranked",
        before=0,
        after=10,
        evidence="sprint_output",
        confidence="medium",
        limitations="internal_only",
    )
    assert value_ledger_event_valid(e)


def test_capital_ledger_event_roundtrip() -> None:
    e = CapitalLedgerEvent(
        capital_event_id="k1",
        project_id="p",
        client_id="c",
        asset_type="knowledge",
        title="ICP rubric",
        description="Sector fit checklist",
        evidence="deliverable_hash",
    )
    assert capital_ledger_event_valid(e)
