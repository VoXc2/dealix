"""Postgres control-ledger adapter behavior."""

from __future__ import annotations

import pytest

from auto_client_acquisition.control_plane_os.postgres_ledger import PostgresControlLedger
from auto_client_acquisition.control_plane_os.schemas import ControlEvent


def test_falls_back_to_jsonl_when_database_url_missing(tmp_path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DEALIX_CONTROL_LEDGER_PATH", str(tmp_path / "control.jsonl"))
    ledger = PostgresControlLedger(database_url="")
    assert ledger.enabled is False

    event = ControlEvent(
        id="evt_1",
        tenant_id="tenant_a",
        event_type="workflow.registered",
        source_module="test",
        actor="tester",
        run_id="run_1",
    )
    ledger.append(event)
    rows = ledger.list_events(tenant_id="tenant_a", run_id="run_1", limit=10)
    assert len(rows) == 1
    assert rows[0].id == "evt_1"
