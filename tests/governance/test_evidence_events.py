"""B1 — Evidence Events append-only ledger doctrine tests."""
from __future__ import annotations

import pytest

from auto_client_acquisition.evidence_control_plane_os.evidence_ledger import (
    EvidenceEvent,
    FileEvidenceLedger,
    PostgresEvidenceLedger,
    get_default_evidence_ledger,
    reset_default_evidence_ledger,
)


@pytest.fixture(autouse=True)
def isolated_ledger(tmp_path, monkeypatch):
    monkeypatch.setenv(
        "DEALIX_EVIDENCE_LEDGER_PATH", str(tmp_path / "evidence_ledger.jsonl")
    )
    monkeypatch.delenv("EVIDENCE_LEDGER_BACKEND", raising=False)
    monkeypatch.delenv("DEALIX_EVIDENCE_LEDGER_SECRET", raising=False)
    reset_default_evidence_ledger()
    yield
    reset_default_evidence_ledger()


def _event(**overrides) -> EvidenceEvent:
    base = {
        "event_type": "proof_artifact",
        "source": "proof_pack:pp_123",
        "summary": "Sprint delivered",
        "actor": "founder",
    }
    base.update(overrides)
    return EvidenceEvent(**base)


def test_append_only_no_mutation_method() -> None:
    """The ledger exposes no update or delete code path."""
    for cls in (FileEvidenceLedger, PostgresEvidenceLedger):
        for forbidden in ("update", "delete", "remove", "edit", "patch"):
            assert not hasattr(cls, forbidden), (
                f"{cls.__name__} must not expose a {forbidden!r} method"
            )


def test_source_is_mandatory() -> None:
    """An evidence event with an empty source is rejected at schema level."""
    with pytest.raises(Exception):
        EvidenceEvent(event_type="x", source="", summary="y", actor="founder")


def test_actor_is_mandatory() -> None:
    with pytest.raises(Exception):
        EvidenceEvent(event_type="x", source="src", summary="y", actor="")


def test_pii_redaction_in_summary() -> None:
    """An email in the summary must not survive into the stored record."""
    ledger = FileEvidenceLedger()
    stored = ledger.append(
        _event(summary="contact attacker@example.com about the proof")
    )
    assert "attacker@example.com" not in stored.summary
    fetched = ledger.get(stored.id)
    assert fetched is not None
    assert "attacker@example.com" not in fetched.summary


def test_signature_verification_round_trip() -> None:
    """A stored event verifies against its own recomputed signature."""
    ledger = FileEvidenceLedger()
    stored = ledger.append(_event())
    assert ledger.verify(stored) is True


def test_signature_verification_postgres() -> None:
    ledger = PostgresEvidenceLedger(database_url="sqlite:///:memory:")
    stored = ledger.append(_event())
    assert ledger.verify(stored) is True
    fetched = ledger.get(stored.id)
    assert fetched is not None
    assert fetched.id == stored.id


def test_list_events_newest_first_and_filters() -> None:
    ledger = FileEvidenceLedger()
    ledger.append(_event(event_type="a", source="src_a"))
    ledger.append(_event(event_type="b", source="src_b"))
    rows = ledger.list_events()
    assert len(rows) == 2
    only_a = ledger.list_events(event_type="a")
    assert len(only_a) == 1
    assert only_a[0].event_type == "a"
    by_source = ledger.list_events(source="src_b")
    assert len(by_source) == 1


def test_default_ledger_factory_is_file_by_default() -> None:
    ledger = get_default_evidence_ledger()
    assert isinstance(ledger, FileEvidenceLedger)
