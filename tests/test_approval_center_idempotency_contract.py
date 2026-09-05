from __future__ import annotations

from pathlib import Path

import pytest

from auto_client_acquisition.approval_center.approval_store import ApprovalStore
from auto_client_acquisition.approval_center.postgres_store import PostgresApprovalStore
from auto_client_acquisition.approval_center.schemas import ApprovalRequest


def _request(*, approval_id: str = "apr_same", object_id: str = "lead_1") -> ApprovalRequest:
    return ApprovalRequest(
        approval_id=approval_id,
        object_type="lead",
        object_id=object_id,
        action_type="draft_email",
        action_mode="approval_required",
        channel="email",
        summary_en="idempotency contract",
        proof_impact="acceptance:approval-idempotency",
    )


@pytest.mark.parametrize("backend", ["memory", "postgres"])
def test_duplicate_approval_id_replays_identical_contract_and_rejects_substitution(
    backend: str,
    tmp_path: Path,
) -> None:
    if backend == "memory":
        store = ApprovalStore()
    else:
        store = PostgresApprovalStore(
            database_url=f"sqlite:///{tmp_path / 'approval-idempotency.sqlite3'}",
            create_tables=True,
        )

    first = store.create(_request())
    replay = store.create(_request())
    assert replay.approval_id == first.approval_id
    assert replay.object_id == "lead_1"

    with pytest.raises(ValueError, match="approval_idempotency_conflict:apr_same"):
        store.create(_request(object_id="lead_2"))

    durable = store.get("apr_same")
    assert durable is not None
    assert durable.object_id == "lead_1"


@pytest.mark.parametrize("backend", ["memory", "postgres"])
def test_founder_rule_create_cannot_substitute_existing_approval_id(
    backend: str,
    tmp_path: Path,
) -> None:
    if backend == "memory":
        store = ApprovalStore()
    else:
        store = PostgresApprovalStore(
            database_url=f"sqlite:///{tmp_path / 'approval-founder-idempotency.sqlite3'}",
            create_tables=True,
        )

    store.create(_request())
    with pytest.raises(ValueError, match="approval_idempotency_conflict:apr_same"):
        store.create_with_founder_rules(_request(object_id="lead_2"))

    durable = store.get("apr_same")
    assert durable is not None
    assert durable.object_id == "lead_1"
