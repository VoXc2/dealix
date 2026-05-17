"""Trigger-based automations.

Each automation maps a business event to an agent action. The dispatcher
evaluates the policy layer, enqueues an AgentTask, raises an
ApprovalRequest for high-risk actions, and writes an evidence event.
No automation can bypass approval — that is asserted by the governance
boundary test.
"""

from __future__ import annotations

from typing import Any, Callable

from auto_client_acquisition.approval_center import ApprovalRequest, create_approval
from auto_client_acquisition.dealix_orchestrator.policy import requires_approval
from auto_client_acquisition.dealix_orchestrator.runtime import get_default_task_queue
from auto_client_acquisition.evidence_control_plane_os.event_store import (
    record_evidence_event,
)

# automation name → (agent_id, action, entity_type)
_AUTOMATION_SPECS: dict[str, tuple[str, str, str]] = {
    "on_lead": ("prospecting", "qualify_lead", "lead"),
    "on_qualified": ("outreach", "first_outreach", "lead"),
    "on_booking": ("meeting", "prepare_meeting_brief", "booking"),
    "on_scope": ("deal_coach", "scope_send", "opportunity"),
    "on_payment": ("customer_success", "open_onboarding", "opportunity"),
    "on_support": ("customer_success", "triage_support_ticket", "support_ticket"),
    "on_customer_success": ("customer_success", "upsell_recommendation", "account"),
}


def _dispatch(
    *,
    automation: str,
    entity_id: str,
    payload: dict[str, Any] | None = None,
    tenant_id: str | None = None,
) -> dict[str, Any]:
    if automation not in _AUTOMATION_SPECS:
        raise ValueError(f"unknown automation: {automation}")
    agent_id, action, entity_type = _AUTOMATION_SPECS[automation]
    needs_approval = requires_approval(action)

    queue = get_default_task_queue()
    task = queue.enqueue(
        customer_id=tenant_id or "public",
        agent_id=agent_id,
        action_type=action,
        payload=payload or {},
        requires_approval=needs_approval,
        approval_reason=f"high_risk_action:{action}" if needs_approval else None,
    )

    approval_id: str | None = None
    if needs_approval:
        approval = create_approval(
            ApprovalRequest(
                object_type=entity_type,
                object_id=entity_id,
                action_type=action,
                action_mode="approval_required",
                risk_level="high",
                summary_en=f"Automation '{automation}' wants to run '{action}'",
                summary_ar="إجراء آلي يحتاج موافقة",
                proof_impact=f"orchestrator:{automation}",
            )
        )
        approval_id = approval.approval_id

    record_evidence_event(
        event_type=f"automation_{automation}",
        entity_type=entity_type,
        entity_id=entity_id,
        actor="dealix_orchestrator",
        action=action,
        summary_en=f"Automation '{automation}' triggered action '{action}'",
        approval_id=approval_id,
        tenant_id=tenant_id,
    )

    return {
        "automation": automation,
        "agent_id": agent_id,
        "action": action,
        "task_id": task.task_id,
        "task_status": task.status,
        "requires_approval": needs_approval,
        "approval_id": approval_id,
    }


def _make_handler(name: str) -> Callable[..., dict[str, Any]]:
    def handler(
        *,
        entity_id: str,
        payload: dict[str, Any] | None = None,
        tenant_id: str | None = None,
    ) -> dict[str, Any]:
        return _dispatch(
            automation=name, entity_id=entity_id, payload=payload, tenant_id=tenant_id
        )

    handler.__name__ = name
    return handler


AUTOMATIONS: dict[str, Callable[..., dict[str, Any]]] = {
    name: _make_handler(name) for name in _AUTOMATION_SPECS
}


def run_automation(
    name: str,
    *,
    entity_id: str,
    payload: dict[str, Any] | None = None,
    tenant_id: str | None = None,
) -> dict[str, Any]:
    """Run a named automation. Raises ValueError on an unknown name."""
    if name not in AUTOMATIONS:
        raise ValueError(f"unknown automation: {name}")
    return AUTOMATIONS[name](entity_id=entity_id, payload=payload, tenant_id=tenant_id)
