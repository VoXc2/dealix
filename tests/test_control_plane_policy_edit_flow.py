"""Policy-edit approval flow tests for control plane."""

from __future__ import annotations

import pytest

from auto_client_acquisition.control_plane_os.repositories import InMemoryControlPlaneRepository


def test_policy_edit_requires_approval_before_finalize(tmp_path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DEALIX_CONTROL_LEDGER_PATH", str(tmp_path / "control.jsonl"))
    repo = InMemoryControlPlaneRepository()
    ticket = repo.request_policy_edit(
        tenant_id="tenant_a",
        actor="ops_admin",
        policy_id="policy_1",
        patch={"max_actions": "4"},
    )

    with pytest.raises(ValueError, match="ticket_state_must_be_granted"):
        repo.finalize_policy_edit(tenant_id="tenant_a", actor="ops_admin", ticket_id=ticket.ticket_id)

    repo.grant_approval(tenant_id="tenant_a", ticket_id=ticket.ticket_id, actor="founder")
    patch = repo.finalize_policy_edit(tenant_id="tenant_a", actor="ops_admin", ticket_id=ticket.ticket_id)
    assert patch["max_actions"] == "4"

    trace = repo.trace_run(tenant_id="tenant_a", run_id="")
    assert any(event.event_type == "policy.edit_requested" for event in trace)
    assert any(event.event_type == "policy.edit_finalized" for event in trace)
