"""Institutional Intelligence Layer systems 56–65 for Dealix."""

from __future__ import annotations

from auto_client_acquisition.institutional_intelligence_layer.blueprint import (
    REQUIRED_PLATFORM_SURFACES,
)
from auto_client_acquisition.institutional_intelligence_layer.agent_society import (
    AgentNode,
    SocietyTaskPlan,
    agent_society_governed,
)
from auto_client_acquisition.institutional_intelligence_layer.assurance_contracts import (
    AssuranceContract,
    AssuranceRuntimeInput,
    assurance_contract_allows_execution,
)
from auto_client_acquisition.institutional_intelligence_layer.control_plane import (
    RUNTIME_OPERATIONS,
    WorkflowControlState,
    control_plane_ready,
    runtime_operation_allowed,
)
from auto_client_acquisition.institutional_intelligence_layer.institutional_learning import (
    LearningSignal,
    learning_actions,
    learning_error_rate,
    learning_improvement,
)
from auto_client_acquisition.institutional_intelligence_layer.memory_fabric import (
    DecisionMemoryRecord,
    build_decision_trace,
    decision_lineage_complete,
    memory_fabric_dependency,
)
from auto_client_acquisition.institutional_intelligence_layer.meta_governance import (
    PolicyRule,
    approval_overload,
    detect_policy_conflicts,
    governance_optimization_actions,
)
from auto_client_acquisition.institutional_intelligence_layer.operating_core import (
    InstitutionalDependencySnapshot,
    infrastructure_status,
    institutional_dependency_score,
    operating_core_verdict,
)
from auto_client_acquisition.institutional_intelligence_layer.org_reasoning import (
    DependencyEdge,
    OrgReasoningInput,
    organizational_reasoning_summary,
    propagate_risk,
)
from auto_client_acquisition.institutional_intelligence_layer.resilience import (
    FailureEvent,
    chaos_readiness,
    resilience_recovery_status,
)
from auto_client_acquisition.institutional_intelligence_layer.value_engine import (
    WorkflowValueSnapshot,
    value_engine_status,
    workflow_roi,
)

SYSTEMS_56_TO_65: tuple[str, ...] = (
    "56_control_plane",
    "57_agent_society_engine",
    "58_assurance_and_safety_contracts",
    "59_institutional_memory_fabric",
    "60_organizational_reasoning_engine",
    "61_resilience_and_chaos_engine",
    "62_meta_governance_engine",
    "63_institutional_value_engine",
    "64_institutional_learning_engine",
    "65_institutional_operating_core",
)

__all__ = (
    "REQUIRED_PLATFORM_SURFACES",
    "SYSTEMS_56_TO_65",
    "AgentNode",
    "AssuranceContract",
    "AssuranceRuntimeInput",
    "DecisionMemoryRecord",
    "DependencyEdge",
    "FailureEvent",
    "InstitutionalDependencySnapshot",
    "LearningSignal",
    "OrgReasoningInput",
    "PolicyRule",
    "RUNTIME_OPERATIONS",
    "SocietyTaskPlan",
    "WorkflowControlState",
    "WorkflowValueSnapshot",
    "agent_society_governed",
    "assurance_contract_allows_execution",
    "approval_overload",
    "build_decision_trace",
    "chaos_readiness",
    "control_plane_ready",
    "decision_lineage_complete",
    "detect_policy_conflicts",
    "governance_optimization_actions",
    "infrastructure_status",
    "institutional_dependency_score",
    "learning_actions",
    "learning_error_rate",
    "learning_improvement",
    "memory_fabric_dependency",
    "operating_core_verdict",
    "organizational_reasoning_summary",
    "propagate_risk",
    "resilience_recovery_status",
    "runtime_operation_allowed",
    "value_engine_status",
    "workflow_roi",
)
