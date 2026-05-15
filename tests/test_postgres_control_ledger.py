"""Postgres control ledger statement tests."""

from __future__ import annotations

from datetime import datetime, timezone

from auto_client_acquisition.control_plane_os.postgres_ledger import (
    approval_ticket_insert_statement,
    control_event_insert_statement,
    workflow_run_insert_statement,
)
from auto_client_acquisition.control_plane_os.repositories import (
    ApprovalTicket,
    ControlEvent,
    WorkflowRun,
)


def _now() -> datetime:
    return datetime.now(timezone.utc)


def test_workflow_run_statement_includes_tenant_fields() -> None:
    run = WorkflowRun(run_id="run-1", tenant_id="tenant-a", workflow_id="wf-1", registered_at=_now(), updated_at=_now())
    sql, params = workflow_run_insert_statement(run)
    assert "workflow_runs" in sql
    assert "tenant_id" in sql
    assert params["tenant_id"] == "tenant-a"


def test_control_event_statement_includes_tenant_fields() -> None:
    event = ControlEvent(
        id="evt-1",
        tenant_id="tenant-a",
        event_type="approval.granted",
        source_module="approval_center",
        actor="sami",
        occurred_at=_now(),
    )
    sql, params = control_event_insert_statement(event)
    assert "control_events" in sql
    assert "tenant_id" in sql
    assert params["tenant_id"] == "tenant-a"


def test_approval_ticket_statement_includes_tenant_fields() -> None:
    ticket = ApprovalTicket(
        ticket_id="apt-1",
        tenant_id="tenant-a",
        action_type="rollback",
        description="rollback request",
        requested_by="ops",
        source_module="control_plane",
        created_at=_now(),
    )
    sql, params = approval_ticket_insert_statement(ticket)
    assert "approval_tickets" in sql
    assert "tenant_id" in sql
    assert params["tenant_id"] == "tenant-a"
