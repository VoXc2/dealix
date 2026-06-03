"""Postgres value ledger store (SQLite in CI)."""

from __future__ import annotations

import pytest

sa = pytest.importorskip("sqlalchemy")

from auto_client_acquisition.value_os.value_ledger_postgres import (
    PostgresValueLedgerStore,
)


def test_postgres_value_ledger_insert_and_list() -> None:
    eng = sa.create_engine("sqlite:///:memory:", future=True)
    store = PostgresValueLedgerStore(engine=eng)
    row = {
        "event_id": "val_test1",
        "customer_id": "t1",
        "kind": "uplift",
        "amount": 42.5,
        "tier": "estimated",
        "source_ref": "",
        "confirmation_ref": "",
        "notes": "",
        "occurred_at": "2026-05-01T12:00:00+00:00",
    }
    store.insert_event(row)
    out = store.list_events(customer_id="t1", limit=10)
    assert len(out) == 1
    assert out[0]["event_id"] == "val_test1"
    assert out[0]["amount"] == 42.5


def test_value_ledger_public_api_uses_sqlite_postgres_backend(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
) -> None:
    from auto_client_acquisition.value_os import value_ledger as vl
    from auto_client_acquisition.value_os.value_ledger_postgres import (
        reset_postgres_value_ledger_singleton_for_test,
    )

    monkeypatch.setenv("DEALIX_VALUE_LEDGER_PATH", str(tmp_path / "value.jsonl"))
    monkeypatch.setenv("VALUE_LEDGER_BACKEND", "postgres")
    monkeypatch.setenv("DEALIX_VALUE_LEDGER_SYNC_DATABASE_URL", "sqlite:///:memory:")
    reset_postgres_value_ledger_singleton_for_test()
    try:
        ev = vl.add_event(customer_id="c1", kind="k", amount=2.0, tier="estimated")
        rows = vl.list_events(customer_id="c1")
        assert any(r.event_id == ev.event_id for r in rows)
    finally:
        reset_postgres_value_ledger_singleton_for_test()
