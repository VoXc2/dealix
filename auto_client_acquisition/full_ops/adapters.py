"""V12 — translators from existing schemas → ``WorkItem``.

These adapters never replace the source schemas; they just project
them into the unified shape the Daily Command Center consumes.
"""
from __future__ import annotations

from typing import Any

from auto_client_acquisition.full_ops.work_item import (
    ActionMode,
    OSType,
    Priority,
    WorkItem,
    WorkItemStatus,
)


# ────────────────────────── helpers ──────────────────────────


def _safe(obj: Any, attr: str, default: Any = None) -> Any:
    if obj is None:
        return default
    if isinstance(obj, dict):
        return obj.get(attr, default)
    return getattr(obj, attr, default)


# ────────────────────── orchestrator AgentTask → WorkItem ──────────


_AGENT_TASK_STATUS_MAP: dict[str, WorkItemStatus] = {
    "pending": "new",
    "awaiting_approval": "needs_approval",
    "approved": "in_progress",
    "executing": "in_progress",
    "succeeded": "done",
    "failed": "blocked",
    "cancelled": "blocked",
}


def from_agent_task(
    task: Any,
    *,
    os_type: OSType = "growth",
    priority: Priority = "p2",
) -> WorkItem:
    """Translate an ``orchestrator.queue.AgentTask`` into a ``WorkItem``."""
    raw_status = str(_safe(task, "status", "pending")).lower()
    status: WorkItemStatus = _AGENT_TASK_STATUS_MAP.get(raw_status, "new")
    action_type = str(_safe(task, "action_type", "task"))
    customer_id = _safe(task, "customer_id")
    title_en = f"{action_type} (agent task)"
    title_ar = f"{action_type} (مهمّة وكيل)"
    return WorkItem.make(
        os_type=os_type,
        title_ar=title_ar,
        title_en=title_en,
        source="orchestrator.AgentTask",
        priority=priority,
        status=status,
        action_mode="approval_required",
        customer_id=customer_id,
    )


# ─────────────── approval_center ApprovalRequest → WorkItem ────────


_APPROVAL_STATUS_MAP: dict[str, WorkItemStatus] = {
    "pending": "needs_approval",
    "approved": "in_progress",
    "rejected": "blocked",
    "expired": "blocked",
    "blocked": "blocked",
}


_APPROVAL_ACTION_MODE_MAP: dict[str, ActionMode] = {
    "draft_only": "draft_only",
    "approval_required": "approval_required",
    "approved_execute": "approved_manual",
    "blocked": "blocked",
}


def from_approval_request(
    req: Any,
    *,
    os_type: OSType = "compliance",
    priority: Priority = "p1",
) -> WorkItem:
    """Translate an ``approval_center.schemas.ApprovalRequest`` → ``WorkItem``."""
    raw_status = str(_safe(req, "status", "pending")).lower()
    status: WorkItemStatus = _APPROVAL_STATUS_MAP.get(raw_status, "needs_approval")
    raw_mode = str(_safe(req, "action_mode", "approval_required")).lower()
    mode: ActionMode = _APPROVAL_ACTION_MODE_MAP.get(raw_mode, "approval_required")
    object_type = str(_safe(req, "object_type", "object"))
    object_id = str(_safe(req, "object_id", _safe(req, "approval_id", "?")))
    title_en = f"Approve {object_type} {object_id}"
    title_ar = f"اعتماد {object_type} {object_id}"
    return WorkItem.make(
        os_type=os_type,
        title_ar=title_ar,
        title_en=title_en,
        source="approval_center.ApprovalRequest",
        priority=priority,
        status=status,
        action_mode=mode,
    )


# ─────────────── customer_loop journey state → WorkItem ────────────


_JOURNEY_STAGE_TO_OS: dict[str, OSType] = {
    "lead_intake": "sales",
    "diagnostic_requested": "delivery",
    "diagnostic_drafting": "delivery",
    "diagnostic_sent": "sales",
    "pilot_offered": "sales",
    "payment_pending": "sales",
    "paid_or_committed": "delivery",
    "in_delivery": "delivery",
    "proof_pack_ready": "customer_success",
    "proof_pack_sent": "customer_success",
    "upsell_recommended": "customer_success",
    "nurture": "growth",
    "blocked": "compliance",
}


def from_journey_state(
    state: Any,
    *,
    priority: Priority = "p2",
) -> WorkItem:
    """Translate a ``customer_loop`` journey state → ``WorkItem``.

    Accepts either a ``JourneyAdvanceRequest``-shaped object or a dict
    with ``current_stage`` + ``customer_id`` keys.
    """
    stage = str(_safe(state, "current_stage", _safe(state, "stage", "lead_intake")))
    customer_id = _safe(state, "customer_id")
    os_type: OSType = _JOURNEY_STAGE_TO_OS.get(stage, "sales")
    title_en = f"Customer journey: {stage}"
    title_ar = f"رحلة العميل: {stage}"
    return WorkItem.make(
        os_type=os_type,
        title_ar=title_ar,
        title_en=title_en,
        source="customer_loop.journey",
        priority=priority,
        status="in_progress" if stage != "blocked" else "blocked",
        action_mode="approval_required",
        customer_id=customer_id,
    )
