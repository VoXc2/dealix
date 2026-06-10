"""
Agent Orchestrator — runs the 11 AI agents as workflows, not stubs.

Public API:
    from auto_client_acquisition.orchestrator import (
        AgentTask, TaskQueue, Orchestrator,
        AutonomyMode, ApprovalGate, BudgetLimit,
    )
"""

from auto_client_acquisition.orchestrator.policies import (
    AutonomyMode,
    BudgetLimit,
    Policy,
    default_policy,
    requires_approval,
)
from auto_client_acquisition.orchestrator.queue import (
    AgentTask,
    TaskQueue,
    TaskStatus,
)
from auto_client_acquisition.orchestrator.runtime import (
    Orchestrator,
    WorkflowDefinition,
    WorkflowStep,
)

__all__ = [
    "AgentTask",
    "AutonomyMode",
    "BudgetLimit",
    "Orchestrator",
    "Policy",
    "TaskQueue",
    "TaskStatus",
    "WorkflowDefinition",
    "WorkflowStep",
    "default_policy",
    "requires_approval",
]
