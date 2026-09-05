"""Real-PostgreSQL concurrency proof for the canonical Approval Center.

Skipped unless ``DEALIX_TEST_POSTGRES_URL`` points to an explicitly isolated
acceptance database. Never aim this suite at production.
"""

from __future__ import annotations

import os
from concurrent.futures import ThreadPoolExecutor
from uuid import uuid4

import pytest
from sqlalchemy import create_engine

from auto_client_acquisition.approval_center.postgres_store import (
    ApprovalCenterSnapshotORM,
    PostgresApprovalStore,
    _ApprovalStoreBase,
)
from auto_client_acquisition.approval_center.schemas import ApprovalRequest
from auto_client_acquisition.persistence.db_sync_url import sync_sqlalchemy_url

_RAW_URL = os.environ.get("DEALIX_TEST_POSTGRES_URL", "").strip()
_ISOLATED = os.environ.get("DEALIX_APPROVAL_ACCEPTANCE_DB_ISOLATED", "0") == "1"
pytestmark = pytest.mark.skipif(
    not (_RAW_URL and _ISOLATED),
    reason="requires an explicitly isolated PostgreSQL acceptance database",
)


def _request(approval_id: str, lead_id: str) -> ApprovalRequest:
    return ApprovalRequest(
        approval_id=approval_id,
        object_type="concurrency_probe",
        object_id=f"obj:{approval_id}",
        action_type="follow_up_task",
        action_mode="approval_required",
        channel="dashboard",
        summary_en="isolated concurrency probe",
        risk_level="low",
        proof_impact="acceptance:approval-center-concurrency",
        action_id=f"action:{approval_id}",
        lead_id=lead_id,
        audit_ref="isolated-test-database",
        proof_target=f"proof:{approval_id}",
    )


@pytest.fixture()
def isolated_postgres_url() -> str:
    assert _RAW_URL
    url = sync_sqlalchemy_url(_RAW_URL)
    assert url.startswith("postgresql"), "DEALIX_TEST_POSTGRES_URL must be PostgreSQL"
    engine = create_engine(url, future=True, pool_pre_ping=True)
    _ApprovalStoreBase.metadata.drop_all(engine)
    _ApprovalStoreBase.metadata.create_all(engine)
    yield url
    _ApprovalStoreBase.metadata.drop_all(engine)
    engine.dispose()


def test_multi_worker_unique_creates_have_no_lost_updates(
    isolated_postgres_url: str,
) -> None:
    run_id = uuid4().hex[:12]
    count = 24

    def _create(index: int) -> str:
        store = PostgresApprovalStore(
            database_url=isolated_postgres_url,
            create_tables=False,
        )
        approval_id = f"apr_concurrent_{run_id}_{index:02d}"
        return store.create(_request(approval_id, f"lead_{index:02d}")).approval_id

    with ThreadPoolExecutor(max_workers=8) as pool:
        created = list(pool.map(_create, range(count)))

    assert len(set(created)) == count
    restarted = PostgresApprovalStore(
        database_url=isolated_postgres_url,
        create_tables=False,
    )
    history = restarted.list_history(limit=100)
    assert {row.approval_id for row in history} == set(created)


def test_multi_worker_conflicting_id_has_one_winner(
    isolated_postgres_url: str,
) -> None:
    approval_id = f"apr_conflict_{uuid4().hex[:12]}"

    def _attempt(index: int) -> tuple[str, str]:
        store = PostgresApprovalStore(
            database_url=isolated_postgres_url,
            create_tables=False,
        )
        try:
            row = store.create(_request(approval_id, f"lead_{index:02d}"))
            return "ok", str(row.lead_id)
        except ValueError as exc:
            assert "approval_idempotency_conflict" in str(exc)
            return "conflict", f"lead_{index:02d}"

    with ThreadPoolExecutor(max_workers=8) as pool:
        outcomes = list(pool.map(_attempt, range(16)))

    winners = [lead_id for status, lead_id in outcomes if status == "ok"]
    assert winners
    stored = PostgresApprovalStore(
        database_url=isolated_postgres_url,
        create_tables=False,
    ).get(approval_id)
    assert stored is not None
    assert stored.lead_id in winners
    assert len([row for row in stored.edit_history if row.get("action") == "approve"]) == 0

    with create_engine(isolated_postgres_url, future=True).connect() as conn:
        rows = conn.execute(
            ApprovalCenterSnapshotORM.__table__.select()
        ).fetchall()
    assert len(rows) == 1
