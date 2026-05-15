"""Enterprise Control Plane — rollback is approval-gated.

Check #5 of the verify contract: a Control Plane rollback cannot
finalize without a human-granted approval ticket.
"""

from __future__ import annotations

import pytest

from auto_client_acquisition.approval_center.approval_store import ApprovalStore
from auto_client_acquisition.institutional_control_os.run_registry import (
    RUN_PAUSED,
    RUN_ROLLBACK_PENDING,
    RUN_ROLLED_BACK,
    RUN_RUNNING,
    RunRegistryError,
    clear_run_registry_for_tests,
    finalize_rollback,
    pause_run,
    register_run,
    request_rollback,
    resume_run,
)


@pytest.fixture(autouse=True)
def _isolated():
    clear_run_registry_for_tests()
    yield
    clear_run_registry_for_tests()


def test_register_run_starts_running():
    run = register_run(tenant_id="t1", workflow_id="lead_intake")
    assert run.state == RUN_RUNNING
    assert run.tenant_id == "t1"


def test_pause_and_resume_run():
    run = register_run(tenant_id="t1", workflow_id="wf")
    paused = pause_run(run.run_id, reason="manual hold")
    assert paused.state == RUN_PAUSED
    resumed = resume_run(run.run_id)
    assert resumed.state == RUN_RUNNING


def test_rollback_request_creates_pending_ticket():
    store = ApprovalStore()
    run = register_run(tenant_id="t1", workflow_id="wf")
    ticket = request_rollback(
        run.run_id, requested_by="founder", reason="bad output", approval_store=store,
    )
    assert ticket.action_type == "rollback"
    assert ticket.tenant_id == "t1"
    assert ticket.run_id == run.run_id
    assert run.state == RUN_ROLLBACK_PENDING
    # The ticket is in the tenant's pending queue.
    assert any(t.approval_id == ticket.approval_id for t in store.list_pending(tenant_id="t1"))


def test_rollback_cannot_finalize_without_approval():
    store = ApprovalStore()
    run = register_run(tenant_id="t1", workflow_id="wf")
    request_rollback(run.run_id, requested_by="founder", reason="x", approval_store=store)
    with pytest.raises(RunRegistryError, match="rollback_not_approved"):
        finalize_rollback(run.run_id, approval_store=store)


def test_rollback_finalizes_after_approval():
    store = ApprovalStore()
    run = register_run(tenant_id="t1", workflow_id="wf")
    ticket = request_rollback(
        run.run_id, requested_by="founder", reason="x", approval_store=store,
    )
    store.approve(ticket.approval_id, who="founder")
    final = finalize_rollback(run.run_id, approval_store=store)
    assert final.state == RUN_ROLLED_BACK


def test_rollback_rejected_ticket_still_blocks_finalize():
    store = ApprovalStore()
    run = register_run(tenant_id="t1", workflow_id="wf")
    ticket = request_rollback(
        run.run_id, requested_by="founder", reason="x", approval_store=store,
    )
    store.reject(ticket.approval_id, who="founder", reason="not warranted")
    with pytest.raises(RunRegistryError, match="rollback_not_approved"):
        finalize_rollback(run.run_id, approval_store=store)
