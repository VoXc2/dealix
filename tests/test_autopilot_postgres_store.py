"""Autopilot Postgres snapshot store + factory backend selection."""

from __future__ import annotations

import pytest

pytest.importorskip("sqlalchemy")

from dealix.revenue_ops_autopilot.postgres_store import AutopilotPostgresStore
from dealix.revenue_ops_autopilot.schemas import FunnelLeadRecord
from dealix.revenue_ops_autopilot.store import (
    AutopilotJSONStore,
    clear_autopilot_store_singleton_for_tests,
    get_autopilot_store,
    reset_autopilot_store_for_tests,
    uid,
)


@pytest.fixture(autouse=True)
def _reset_singleton() -> None:
    clear_autopilot_store_singleton_for_tests()
    yield
    clear_autopilot_store_singleton_for_tests()


def test_get_autopilot_store_defaults_to_json(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("DEALIX_AUTOPILOT_STORE_BACKEND", raising=False)
    monkeypatch.delenv("DATABASE_URL", raising=False)
    store = get_autopilot_store()
    assert isinstance(store, AutopilotJSONStore)
    assert not isinstance(store, AutopilotPostgresStore)


def test_get_autopilot_store_postgres_backend_with_sqlite(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("DEALIX_AUTOPILOT_STORE_BACKEND", "postgres")
    monkeypatch.setenv("DATABASE_URL", "sqlite:///:memory:")
    store = get_autopilot_store()
    assert isinstance(store, AutopilotPostgresStore)


def test_postgres_backend_env_cannot_auto_create_schema(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import dealix.revenue_ops_autopilot.postgres_store as postgres_store

    seen: dict[str, bool] = {}

    class StubPostgresStore:
        def __init__(self, *, database_url: str, create_tables: bool = True) -> None:
            seen["create_tables"] = create_tables

    monkeypatch.setattr(postgres_store, "AutopilotPostgresStore", StubPostgresStore)
    monkeypatch.setenv("DEALIX_AUTOPILOT_STORE_BACKEND", "postgres")
    monkeypatch.setenv("DATABASE_URL", "sqlite:///:memory:")
    store = get_autopilot_store()
    assert isinstance(store, StubPostgresStore)
    assert seen["create_tables"] is False

def test_get_autopilot_store_does_not_fallback_or_create_on_unreachable_postgres(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("DEALIX_AUTOPILOT_STORE_BACKEND", "postgres")
    monkeypatch.setenv(
        "DATABASE_URL",
        "postgresql+asyncpg://invalid:invalid@127.0.0.1:59999/nope",
    )
    store = get_autopilot_store()
    assert isinstance(store, AutopilotPostgresStore)


def test_postgres_store_upsert_and_get_lead() -> None:
    store = AutopilotPostgresStore(database_url="sqlite:///:memory:", create_tables=True)
    lead = FunnelLeadRecord(
        id=uid("lead"),
        company="Test Co",
        name="Sami",
        email="test@example.sa",
        stage="new_lead",
    )
    store.upsert_lead(lead)
    hit = store.get_lead(lead.id)
    assert hit is not None
    assert hit.company == "Test Co"


@pytest.mark.skipif(
    not __import__("os").environ.get("DATABASE_URL", "").strip().startswith(
        ("postgresql://", "postgresql+asyncpg://", "postgresql+psycopg2://", "postgresql+psycopg://")
    ),
    reason="DATABASE_URL not set to a PostgreSQL URL",
)
def test_postgres_store_with_live_database_url(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DEALIX_AUTOPILOT_STORE_BACKEND", "postgres")
    reset_autopilot_store_for_tests()
    clear_autopilot_store_singleton_for_tests()
    store = get_autopilot_store()
    assert isinstance(store, AutopilotPostgresStore)
    lead_id = uid("lead")
    store.upsert_lead(
        FunnelLeadRecord(
            id=lead_id,
            company="Live DB Co",
            name="Probe",
            email="probe@example.sa",
            stage="qualified_A",
        )
    )
    assert store.get_lead(lead_id) is not None
