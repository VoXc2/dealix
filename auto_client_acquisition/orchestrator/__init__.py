"""
Agent Orchestrator — runs the 11 AI agents as workflows, not stubs.

Public API:
    from auto_client_acquisition.orchestrator import (
        AgentTask, TaskQueue, Orchestrator,
        AutonomyMode, ApprovalGate, BudgetLimit,
    )
"""

from auto_client_acquisition.orchestrator.operating_company_contract import (
    DEFAULT_OPERATING_COMPANY_CONTRACT,
    GOVERNED_ACCELERATION_CHAIN,
)
from auto_client_acquisition.orchestrator.policies import (
    AutonomyMode,
    BudgetLimit,
    Policy,
    default_policy,
    requires_approval,
)
from auto_client_acquisition.orchestrator.postgres_state import (
    PostgresTaskQueue,
    PostgresWorkflowRunStore,
)
from auto_client_acquisition.orchestrator.queue import (
    AgentTask,
    JsonTaskQueue,
    TaskQueue,
    TaskStatus,
)
from auto_client_acquisition.orchestrator.runtime import (
    InMemoryWorkflowRunStore,
    JsonWorkflowRunStore,
    Orchestrator,
    WorkflowDefinition,
    WorkflowStep,
)

__all__ = [
    "DEFAULT_OPERATING_COMPANY_CONTRACT",
    "GOVERNED_ACCELERATION_CHAIN",
    "AgentTask",
    "AutonomyMode",
    "BudgetLimit",
    "InMemoryWorkflowRunStore",
    "JsonTaskQueue",
    "JsonWorkflowRunStore",
    "Orchestrator",
    "Policy",
    "PostgresTaskQueue",
    "PostgresWorkflowRunStore",
    "TaskQueue",
    "TaskStatus",
    "WorkflowDefinition",
    "WorkflowStep",
    "default_policy",
    "requires_approval",
]
