"""Rollback flow tests for control-plane approval gating."""

from __future__ import annotations

import pytest

from auto_client_acquisition.control_plane_os import (
    ApprovalGateError,
    ControlPlaneRepository,
    RollbackRequest,
)


def test_rollback_requires_approval_before_finalize() -> None:
    repo = ControlPlaneRepository()
    run = repo.register_run(tenant_id="tenant-a", workflow_id="wf-sales", actor="ops")
    ticket = repo.request_rollback(
        RollbackRequest(
            tenant_id="tenant-a",
            run_id=run.run_id,
            actor="ops",
            reason="customer complaint",
        ),
    )

    with pytest.raises(ApprovalGateError):
        repo.finalize_rollback(
            tenant_id="tenant-a",
            run_id=run.run_id,
            ticket_id=ticket.ticket_id,
            actor="ops",
        )

    repo.grant_approval(tenant_id="tenant-a", ticket_id=ticket.ticket_id, actor="founder")
    finalized = repo.finalize_rollback(
        tenant_id="tenant-a",
        run_id=run.run_id,
        ticket_id=ticket.ticket_id,
        actor="ops",
    )
    assert finalized.state == "rolled_back"

    event_types = [event.event_type for event in repo.trace_run(tenant_id="tenant-a", run_id=run.run_id)]
    assert "rollback_requested" in event_types
    assert "approval_granted" in event_types
    assert "rollback_finalized" in event_types
