"""Postgres persistence helpers for enterprise control-plane tables."""

from __future__ import annotations

import json
from typing import Any

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from auto_client_acquisition.control_plane_os.repositories import (
    ApprovalTicket,
    ControlEvent,
    WorkflowRun,
)


def workflow_run_insert_statement(run: WorkflowRun) -> tuple[str, dict[str, Any]]:
    sql = """
    INSERT INTO workflow_runs (
      run_id, tenant_id, workflow_id, customer_id, state, correlation_id,
      parent_run_id, current_step, attached_policy_ids, metadata, registered_at, updated_at
    ) VALUES (
      :run_id, :tenant_id, :workflow_id, :customer_id, :state, :correlation_id,
      :parent_run_id, :current_step, CAST(:attached_policy_ids AS JSONB),
      CAST(:metadata AS JSONB), :registered_at, :updated_at
    )
    """
    params = {
        "run_id": run.run_id,
        "tenant_id": run.tenant_id,
        "workflow_id": run.workflow_id,
        "customer_id": run.customer_id,
        "state": run.state,
        "correlation_id": run.correlation_id,
        "parent_run_id": run.parent_run_id,
        "current_step": run.current_step,
        "attached_policy_ids": json.dumps(list(run.attached_policy_ids)),
        "metadata": json.dumps(run.metadata),
        "registered_at": run.registered_at,
        "updated_at": run.updated_at,
    }
    return sql, params


def control_event_insert_statement(event: ControlEvent) -> tuple[str, dict[str, Any]]:
    sql = """
    INSERT INTO control_events (
      id, tenant_id, event_type, source_module, actor, subject_type, subject_id,
      run_id, correlation_id, decision, occurred_at, payload, redacted
    ) VALUES (
      :id, :tenant_id, :event_type, :source_module, :actor, :subject_type, :subject_id,
      :run_id, :correlation_id, :decision, :occurred_at, CAST(:payload AS JSONB), :redacted
    )
    """
    params = {
        "id": event.id,
        "tenant_id": event.tenant_id,
        "event_type": event.event_type,
        "source_module": event.source_module,
        "actor": event.actor,
        "subject_type": event.subject_type,
        "subject_id": event.subject_id,
        "run_id": event.run_id,
        "correlation_id": event.correlation_id,
        "decision": event.decision,
        "occurred_at": event.occurred_at,
        "payload": json.dumps(event.payload),
        "redacted": event.redacted,
    }
    return sql, params


def approval_ticket_insert_statement(ticket: ApprovalTicket) -> tuple[str, dict[str, Any]]:
    sql = """
    INSERT INTO approval_tickets (
      ticket_id, tenant_id, action_type, description, requested_by, source_module,
      subject_type, subject_id, run_id, state, granted_by, rejected_by, reason, metadata,
      created_at, resolved_at
    ) VALUES (
      :ticket_id, :tenant_id, :action_type, :description, :requested_by, :source_module,
      :subject_type, :subject_id, :run_id, :state, :granted_by, :rejected_by, :reason,
      CAST(:metadata AS JSONB), :created_at, :resolved_at
    )
    """
    params = {
        "ticket_id": ticket.ticket_id,
        "tenant_id": ticket.tenant_id,
        "action_type": ticket.action_type,
        "description": ticket.description,
        "requested_by": ticket.requested_by,
        "source_module": ticket.source_module,
        "subject_type": ticket.subject_type,
        "subject_id": ticket.subject_id,
        "run_id": ticket.run_id,
        "state": ticket.state,
        "granted_by": ticket.granted_by,
        "rejected_by": ticket.rejected_by,
        "reason": ticket.reason,
        "metadata": json.dumps(ticket.metadata),
        "created_at": ticket.created_at,
        "resolved_at": ticket.resolved_at,
    }
    return sql, params


class PostgresControlLedger:
    """Thin repository that persists control-plane objects using SQLAlchemy session."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def register_workflow_run(self, run: WorkflowRun) -> None:
        sql, params = workflow_run_insert_statement(run)
        await self._session.execute(text(sql), params)

    async def record_control_event(self, event: ControlEvent) -> None:
        sql, params = control_event_insert_statement(event)
        await self._session.execute(text(sql), params)

    async def create_approval_ticket(self, ticket: ApprovalTicket) -> None:
        sql, params = approval_ticket_insert_statement(ticket)
        await self._session.execute(text(sql), params)

    async def flush(self) -> None:
        await self._session.commit()


__all__ = [
    "PostgresControlLedger",
    "approval_ticket_insert_statement",
    "control_event_insert_statement",
    "workflow_run_insert_statement",
]
