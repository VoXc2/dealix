"""Tests for isolated-thread Postgres revenue event store (shutdown + smoke)."""

from __future__ import annotations

import os

import pytest

from auto_client_acquisition.revenue_memory.isolated_pg_event_store import (
    shutdown_isolated_postgres_revenue_worker,
)


def test_shutdown_isolated_postgres_idempotent() -> None:
    """No worker started — shutdown must not raise."""
    shutdown_isolated_postgres_revenue_worker()
    shutdown_isolated_postgres_revenue_worker()


@pytest.mark.integration
def test_isolated_pg_append_read_roundtrip_when_env_enabled() -> None:
    """Requires Postgres with ``revenue_events`` migrated; set RUN_REVENUE_PG_ISOLATION_TEST=1."""
    if os.environ.get("RUN_REVENUE_PG_ISOLATION_TEST") != "1":
        pytest.skip("set RUN_REVENUE_PG_ISOLATION_TEST=1 with a reachable DATABASE_URL")

    from auto_client_acquisition.revenue_memory.event_store import (
        get_postgres_store,
        reset_default_store,
    )
    from auto_client_acquisition.revenue_memory.events import make_event

    reset_default_store()
    try:
        store = get_postgres_store()
        e = make_event(
            event_type="lead.created",
            customer_id="ci_isolated_pg_test",
            subject_type="account",
            subject_id="acct_ci_iso",
            payload={"source": "integration_test"},
            actor="test",
        )
        store.append(e)
        events = list(store.read_for_customer("ci_isolated_pg_test"))
        assert any(x.event_id == e.event_id for x in events)
    finally:
        reset_default_store()
