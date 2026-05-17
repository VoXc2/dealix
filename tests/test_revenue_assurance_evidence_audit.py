"""Evidence Ledger Audit — integrity checks over sampled value events."""

from __future__ import annotations

import pytest

from auto_client_acquisition.revenue_assurance_os.evidence_audit import audit_evidence
from auto_client_acquisition.value_os.value_ledger import add_event, clear_for_test


@pytest.fixture(autouse=True)
def _isolated_ledger(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("VALUE_LEDGER_BACKEND", "jsonl")
    monkeypatch.setenv("DEALIX_VALUE_LEDGER_PATH", str(tmp_path / "value_ledger.jsonl"))
    clear_for_test()


def test_empty_ledger_passes_vacuously() -> None:
    result = audit_evidence(sample_size=20)
    assert result.sampled == 0
    assert result.passed is True


def test_clean_event_has_no_findings() -> None:
    add_event(
        customer_id="acme",
        kind="invoice_paid",
        amount=4999.0,
        tier="verified",
        source_ref="inv-001",
    )
    result = audit_evidence(sample_size=20)
    assert result.sampled == 1
    assert result.findings == ()
    assert result.passed is True


def test_raw_pii_in_notes_is_flagged() -> None:
    add_event(
        customer_id="acme",
        kind="lead_captured",
        amount=0.0,
        tier="estimated",
        notes="follow up — call 0501234567",
    )
    result = audit_evidence(sample_size=20)
    issues = {f.issue for f in result.findings}
    assert "raw_pii_in_notes" in issues
