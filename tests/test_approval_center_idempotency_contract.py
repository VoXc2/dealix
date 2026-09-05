from __future__ import annotations

from pathlib import Path

import pytest

from auto_client_acquisition.approval_center.approval_store import ApprovalStore
from auto_client_acquisition.approval_center.postgres_store import PostgresApprovalStore
from auto_client_acquisition.approval_center.schemas import (
    ApprovalRequest,
    ApprovalStatus,
)


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


def _store(backend: str, tmp_path: Path, suffix: str):
    if backend == "memory":
        return ApprovalStore()
    return PostgresApprovalStore(
        database_url=f"sqlite:///{tmp_path / suffix}",
        create_tables=True,
    )


@pytest.mark.parametrize("backend", ["memory", "postgres"])
def test_duplicate_approval_id_replays_identical_contract_and_rejects_substitution(
    backend: str,
    tmp_path: Path,
) -> None:
    store = _store(backend, tmp_path, "approval-idempotency.sqlite3")

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
    store = _store(backend, tmp_path, "approval-founder-idempotency.sqlite3")

    store.create(_request())
    with pytest.raises(ValueError, match="approval_idempotency_conflict:apr_same"):
        store.create_with_founder_rules(_request(object_id="lead_2"))

    durable = store.get("apr_same")
    assert durable is not None
    assert durable.object_id == "lead_1"


@pytest.mark.parametrize("backend", ["memory", "postgres"])
@pytest.mark.parametrize(
    "status",
    [ApprovalStatus.APPROVED, ApprovalStatus.REJECTED, ApprovalStatus.EXPIRED],
)
def test_create_rejects_caller_supplied_transitioned_status(
    backend: str,
    status: ApprovalStatus,
    tmp_path: Path,
) -> None:
    store = _store(backend, tmp_path, f"approval-pretransition-{status.value}.sqlite3")
    req = _request(approval_id=f"apr_{status.value}")
    req.status = status

    with pytest.raises(
        ValueError,
        match=rf"approval_creation_status_not_allowed:apr_{status.value}:{status.value}",
    ):
        store.create(req)

    assert store.get(f"apr_{status.value}") is None


@pytest.mark.parametrize("backend", ["memory", "postgres"])
def test_founder_rule_create_rejects_caller_supplied_approved_status(
    backend: str,
    tmp_path: Path,
) -> None:
    store = _store(backend, tmp_path, "approval-founder-preapproved.sqlite3")
    req = _request(approval_id="apr_preapproved_founder")
    req.status = ApprovalStatus.APPROVED
    req.action_mode = "approved_execute"

    with pytest.raises(
        ValueError,
        match="approval_creation_status_not_allowed:apr_preapproved_founder:approved",
    ):
        store.create_with_founder_rules(req)

    assert store.get("apr_preapproved_founder") is None
