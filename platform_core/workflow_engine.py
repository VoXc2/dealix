"""Workflow engine facade — deterministic stages + approval flow markers.

The canonical workflow runs the fixed stage order INTAKE..HANDOFF. The
approval flow is a separate four-step ladder that is deliberately left
incomplete until a human approves (doctrine: no external action without
approval).
"""

from __future__ import annotations

from auto_client_acquisition.workflow_os.approval_flow import (
    APPROVAL_FLOW_STEPS,
    approval_flow_complete,
)
from auto_client_acquisition.workflow_os.workflow_model import (
    WORKFLOW_STAGE_ORDER,
    WorkflowStage,
)

__all__ = [
    "APPROVAL_FLOW_STEPS",
    "WORKFLOW_STAGE_ORDER",
    "WorkflowStage",
    "approval_flow_complete",
]
