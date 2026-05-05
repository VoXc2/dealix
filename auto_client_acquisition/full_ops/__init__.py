"""V12 Full-Ops — unified WorkItem layer.

Translates the 3 existing task-like schemas (``AgentTask`` from
``orchestrator``, ``ApprovalRequest`` from ``approval_center``,
``JourneyAdvanceRequest`` from ``customer_loop``) into a single
``WorkItem`` shape so the Daily Command Center can show one queue per
OS without each consumer caring about the underlying schema.

This module is **a translator, never a replacement** — it does not
mutate or supersede the existing schemas.
"""
from auto_client_acquisition.full_ops.adapters import (
    from_agent_task,
    from_approval_request,
    from_journey_state,
)
from auto_client_acquisition.full_ops.prioritizer import prioritize
from auto_client_acquisition.full_ops.work_item import (
    ActionMode,
    OSType,
    Priority,
    WorkItem,
    WorkItemStatus,
)
from auto_client_acquisition.full_ops.work_queue import WorkQueue, get_default_queue

__all__ = [
    "ActionMode",
    "OSType",
    "Priority",
    "WorkItem",
    "WorkItemStatus",
    "WorkQueue",
    "from_agent_task",
    "from_approval_request",
    "from_journey_state",
    "get_default_queue",
    "prioritize",
]
