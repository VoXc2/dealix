"""DealixOrchestrator — wires the agent registry, the task queue, the
policy layer and the evidence ledger into one governed surface.

Every automation trigger evaluates policy first: high-risk actions are
enqueued as ``awaiting_approval`` AND raised as an ApprovalRequest — they
never execute without a founder. Every trigger writes an evidence event.
"""

from __future__ import annotations

from auto_client_acquisition.dealix_orchestrator.automations import (
    AUTOMATIONS,
    run_automation,
)
from auto_client_acquisition.dealix_orchestrator.policy import (
    HIGH_RISK_ACTIONS,
    STAGE_ORDER,
    can_auto_send,
    claim_has_source,
    requires_approval,
    stage_transition_allowed,
)
from auto_client_acquisition.dealix_orchestrator.runtime import (
    get_default_task_queue,
    reset_default_task_queue,
)

__all__ = [
    "AUTOMATIONS",
    "HIGH_RISK_ACTIONS",
    "STAGE_ORDER",
    "can_auto_send",
    "claim_has_source",
    "get_default_task_queue",
    "requires_approval",
    "reset_default_task_queue",
    "run_automation",
    "stage_transition_allowed",
]
