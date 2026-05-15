"""Policy-edit approval flow tests for control plane."""

from __future__ import annotations

import pytest

from auto_client_acquisition.control_plane_os import (
    ApprovalGateError,
    ControlPlaneRepository,
    PolicyEditRequest,
)


def test_policy_edit_finalize_requires_granted_ticket() -> None:
    repo = ControlPlaneRepository()
    run = repo.register_run(tenant_id="tenant-a", workflow_id="wf-policy", actor="governor")
    ticket = repo.request_policy_edit(
        PolicyEditRequest(
            tenant_id="tenant-a",
            run_id=run.run_id,
            policy_id="pricing-guard",
            actor="governor",
            change={"max_discount": 5},
        ),
    )

    with pytest.raises(ApprovalGateError):
        repo.finalize_policy_edit(
            tenant_id="tenant-a",
            run_id=run.run_id,
            ticket_id=ticket.ticket_id,
            actor="governor",
        )

    repo.grant_approval(tenant_id="tenant-a", ticket_id=ticket.ticket_id, actor="founder")
    finalized = repo.finalize_policy_edit(
        tenant_id="tenant-a",
        run_id=run.run_id,
        ticket_id=ticket.ticket_id,
        actor="governor",
    )
    assert finalized.state == "running"

    event_types = [event.event_type for event in repo.trace_run(tenant_id="tenant-a", run_id=run.run_id)]
    assert "policy_edit_requested" in event_types
    assert "policy_edit_finalized" in event_types
