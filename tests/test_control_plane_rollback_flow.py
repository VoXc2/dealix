"""Approval-first rollback flow tests."""

from __future__ import annotations

import pytest

from auto_client_acquisition.control_plane_os.repositories import InMemoryControlPlaneRepository


def test_control_plane_rollback_requires_approval() -> None:
    repo = InMemoryControlPlaneRepository()
    run = repo.register_workflow_run(
        tenant_id="tenant-a",
        workflow_id="revenue_os_workflow",
        customer_id="cust-1",
    )
    ticket = repo.request_rollback(
        tenant_id="tenant-a",
        run_id=run.run_id,
        requested_by="operator",
        reason="undo risky action",
    )

    with pytest.raises(PermissionError, match="requires granted approval"):
        repo.finalize_rollback(
            tenant_id="tenant-a",
            run_id=run.run_id,
            ticket_id=ticket.ticket_id,
            actor="control-plane",
        )

    repo.grant_approval(tenant_id="tenant-a", ticket_id=ticket.ticket_id, granted_by="sami")
    rolled_back = repo.finalize_rollback(
        tenant_id="tenant-a",
        run_id=run.run_id,
        ticket_id=ticket.ticket_id,
        actor="control-plane",
    )
    assert rolled_back.state == "rolled_back"
    assert repo.list_oversight_queue(tenant_id="tenant-a") == ()
