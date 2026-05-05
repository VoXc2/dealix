"""Tests for the SQLAlchemy-backed proof ledger.

Uses sqlite:///:memory: through SQLAlchemy — same code path Postgres
will run, but no live DB required for CI. The file-backed ledger remains
the default; these tests exercise the opt-in Postgres backend and the
factory switch.
"""
from __future__ import annotations

import pytest

# Skip the whole module if SQLAlchemy + sqlite cannot stand up an
# in-memory engine — guarantees this file is a no-op on minimal envs.
sa = pytest.importorskip("sqlalchemy")
try:
    _engine = sa.create_engine("sqlite:///:memory:", future=True)
    _engine.connect().close()
except Exception as exc:  # pragma: no cover — defensive, env-only
    pytest.skip(f"sqlite in-memory engine unavailable: {exc}", allow_module_level=True)


from auto_client_acquisition.proof_ledger import (
    FileProofLedger,
    PostgresProofLedger,
    ProofEvent,
    ProofEventType,
    RevenueWorkUnit,
    RevenueWorkUnitType,
    get_default_ledger,
)
from auto_client_acquisition.proof_ledger import factory as ledger_factory


@pytest.fixture
def pg_ledger() -> PostgresProofLedger:
    """Fresh in-memory Postgres-style ledger per test."""
    engine = sa.create_engine("sqlite:///:memory:", future=True)
    return PostgresProofLedger(engine=engine)


def test_record_event_then_list_events_returns_it(pg_ledger: PostgresProofLedger) -> None:
    stored = pg_ledger.record(ProofEvent(
        event_type=ProofEventType.LEAD_INTAKE,
        customer_handle="ACME-Saudi-Co",
        summary_ar="عميل جديد.",
        summary_en="New lead intake.",
        consent_for_publication=False,
    ))
    assert stored.id.startswith("evt_")

    events = pg_ledger.list_events()
    assert len(events) == 1
    assert events[0].id == stored.id
    assert events[0].customer_handle == "ACME-Saudi-Co"
    assert events[0].event_type == ProofEventType.LEAD_INTAKE.value


def test_pii_in_summary_is_redacted_on_insert(pg_ledger: PostgresProofLedger) -> None:
    """Same redaction-on-write contract as FileProofLedger."""
    pg_ledger.record(ProofEvent(
        event_type=ProofEventType.DELIVERY_TASK_COMPLETED,
        customer_handle="ACME",
        summary_ar="تواصل عبر ali@example.sa أو +966501234567",
        summary_en="Reach out at ali@example.sa or +966501234567",
        consent_for_publication=False,
    ))

    [ev] = pg_ledger.list_events()
    # The redacted variants must NOT contain raw PII.
    assert "ali@example.sa" not in ev.redacted_summary_ar
    assert "ali@example.sa" not in ev.redacted_summary_en
    assert "501234567" not in ev.redacted_summary_ar
    assert "501234567" not in ev.redacted_summary_en
    # And the redacted fields must be populated (not empty).
    assert ev.redacted_summary_ar
    assert ev.redacted_summary_en


def test_list_events_filters_by_customer_handle(pg_ledger: PostgresProofLedger) -> None:
    pg_ledger.record(ProofEvent(
        event_type=ProofEventType.LEAD_INTAKE,
        customer_handle="ACME-A",
    ))
    pg_ledger.record(ProofEvent(
        event_type=ProofEventType.LEAD_INTAKE,
        customer_handle="BravoCo",
    ))
    pg_ledger.record(ProofEvent(
        event_type=ProofEventType.PILOT_OFFERED,
        customer_handle="ACME-A",
    ))

    only_acme = pg_ledger.list_events(customer_handle="ACME-A")
    assert len(only_acme) == 2
    assert all(e.customer_handle == "ACME-A" for e in only_acme)

    only_bravo = pg_ledger.list_events(customer_handle="BravoCo")
    assert len(only_bravo) == 1
    assert only_bravo[0].customer_handle == "BravoCo"


def test_list_events_filters_by_event_type(pg_ledger: PostgresProofLedger) -> None:
    pg_ledger.record(ProofEvent(
        event_type=ProofEventType.LEAD_INTAKE,
        customer_handle="ACME",
    ))
    pg_ledger.record(ProofEvent(
        event_type=ProofEventType.PILOT_OFFERED,
        customer_handle="ACME",
    ))
    pilots = pg_ledger.list_events(event_type=ProofEventType.PILOT_OFFERED.value)
    assert len(pilots) == 1
    assert pilots[0].event_type == ProofEventType.PILOT_OFFERED.value


def test_record_unit_then_list_units_returns_it(pg_ledger: PostgresProofLedger) -> None:
    stored = pg_ledger.record_unit(RevenueWorkUnit(
        unit_type=RevenueWorkUnitType.OPPORTUNITY_CREATED,
        customer_handle="ACME",
        quantity=3,
        description="3 qualified opportunities created.",
    ))
    assert stored.id.startswith("rwu_")

    units = pg_ledger.list_units(customer_handle="ACME")
    assert len(units) == 1
    assert units[0].quantity == 3
    assert units[0].unit_type == RevenueWorkUnitType.OPPORTUNITY_CREATED.value


def test_factory_returns_file_ledger_by_default(monkeypatch: pytest.MonkeyPatch) -> None:
    """Default backend must remain ``FileProofLedger`` — Postgres is opt-in."""
    ledger_factory.reset_default_ledger()
    # Ensure the env override is absent and settings reads the default.
    monkeypatch.delenv("PROOF_LEDGER_BACKEND", raising=False)

    # Patch the settings reader to return a stub with the default value
    # so we don't depend on global ``settings`` cached state.
    class _Stub:
        proof_ledger_backend = "file"

    monkeypatch.setattr(
        ledger_factory,
        "_backend_name",
        lambda: _Stub.proof_ledger_backend,
    )

    led = get_default_ledger()
    assert isinstance(led, FileProofLedger)
    ledger_factory.reset_default_ledger()


def test_factory_returns_postgres_ledger_when_settings_say_postgres(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    ledger_factory.reset_default_ledger()

    class _Stub:
        proof_ledger_backend = "postgres"

    monkeypatch.setattr(
        ledger_factory,
        "_backend_name",
        lambda: _Stub.proof_ledger_backend,
    )

    led = get_default_ledger()
    assert isinstance(led, PostgresProofLedger)

    # Calling again returns the same singleton so writes accumulate.
    again = get_default_ledger()
    assert again is led

    ledger_factory.reset_default_ledger()


def test_factory_falls_back_to_file_for_unknown_backend(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Misconfigured envs must not silently data-loss into a non-existent backend."""
    ledger_factory.reset_default_ledger()

    class _Stub:
        proof_ledger_backend = "totally-bogus"

    monkeypatch.setattr(
        ledger_factory,
        "_backend_name",
        lambda: _Stub.proof_ledger_backend,
    )

    led = get_default_ledger()
    assert isinstance(led, FileProofLedger)
    ledger_factory.reset_default_ledger()
