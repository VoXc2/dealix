"""Policy edit approval gate tests."""

from __future__ import annotations

import pytest

from auto_client_acquisition.control_plane_os.repositories import InMemoryControlPlaneRepository


def test_policy_edit_requires_approval() -> None:
    repo = InMemoryControlPlaneRepository()
    ticket = repo.request_policy_edit(
        tenant_id="tenant-a",
        policy_id="policy-risk-v2",
        patch={"max_risk": 0.6},
        requested_by="platform-admin",
    )

    with pytest.raises(PermissionError, match="requires granted approval"):
        repo.finalize_policy_edit(tenant_id="tenant-a", ticket_id=ticket.ticket_id, actor="admin")

    repo.grant_approval(
        tenant_id="tenant-a",
        ticket_id=ticket.ticket_id,
        granted_by="governance-chair",
    )
    applied = repo.finalize_policy_edit(
        tenant_id="tenant-a",
        ticket_id=ticket.ticket_id,
        actor="admin",
    )
    assert applied["policy_id"] == "policy-risk-v2"
    assert applied["patch"]["max_risk"] == 0.6
