"""Postgres control ledger contract tests (with fallback behavior)."""

from __future__ import annotations

from auto_client_acquisition.control_plane_os import ControlEvent, PostgresControlLedger


def test_postgres_ledger_exposes_configuration_state() -> None:
    assert PostgresControlLedger().is_configured is False
    assert PostgresControlLedger("postgresql://u:p@localhost/db").is_configured is True


def test_postgres_ledger_fallback_stores_events() -> None:
    ledger = PostgresControlLedger()
    event = ledger.append(
        ControlEvent(
            tenant_id="tenant-a",
            event_type="run_registered",
            source_module="test",
            actor="tester",
            run_id="run-1",
        ),
    )
    rows = ledger.list_by_run(tenant_id="tenant-a", run_id="run-1")
    assert rows and rows[0].event_id == event.event_id
