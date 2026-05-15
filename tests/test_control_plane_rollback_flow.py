"""Rollback approval flow tests for control plane."""

from __future__ import annotations

import pytest

from auto_client_acquisition.control_plane_os.repositories import InMemoryControlPlaneRepository


def test_rollback_does_not_finalize_without_approval(tmp_path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DEALIX_CONTROL_LEDGER_PATH", str(tmp_path / "control.jsonl"))
    repo = InMemoryControlPlaneRepository()
    run = repo.register_run(tenant_id="tenant_a", workflow_id="lead_flow", actor="system")
    ticket = repo.request_rollback(
        tenant_id="tenant_a",
        run_id=run.run_id,
        actor="ops_admin",
        reason="rollback drill",
    )

    with pytest.raises(ValueError, match="ticket_state_must_be_granted"):
        repo.finalize_rollback(
            tenant_id="tenant_a",
            run_id=run.run_id,
            actor="ops_admin",
            ticket_id=ticket.ticket_id,
        )

    repo.grant_approval(tenant_id="tenant_a", ticket_id=ticket.ticket_id, actor="founder")
    rolled = repo.finalize_rollback(
        tenant_id="tenant_a",
        run_id=run.run_id,
        actor="ops_admin",
        ticket_id=ticket.ticket_id,
    )
    assert rolled.state == "rolled_back"

    trace = repo.trace_run(tenant_id="tenant_a", run_id=run.run_id)
    event_types = {event.event_type for event in trace}
    assert "rollback.requested" in event_types
    assert "rollback.finalized" in event_types
