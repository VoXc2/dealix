"""Dealix platform scale systems — governed, observable, and resilient by default."""

from auto_client_acquisition.platform.accountability import (
    AuditRecord,
    explain_action,
    list_audit_events,
    record_audit_event,
)
from auto_client_acquisition.platform.adaptive_orchestration import (
    OrchestrationDecision,
    choose_orchestration_variant,
)
from auto_client_acquisition.platform.agent_governance import (
    AgentGovernanceStatus,
    assess_agent_governance,
)
from auto_client_acquisition.platform.agent_lifecycle import AgentLifecycleState, lifecycle_transition_allowed
from auto_client_acquisition.platform.agent_registry import (
    AgentRegistration,
    get_agent,
    list_agents,
    register_agent,
    rollback_agent,
    suspend_agent,
)
from auto_client_acquisition.platform.executive_os import (
    ExecutiveInsightPack,
    build_executive_insight_pack,
)
from auto_client_acquisition.platform.memory_governance import MemoryRecord, MemorySensitivity
from auto_client_acquisition.platform.org_intelligence import OrgIntelligenceReport, build_org_intelligence
from auto_client_acquisition.platform.runtime_governance import (
    RuntimeActionRequest,
    RuntimeActionResult,
    govern_action,
)
from auto_client_acquisition.platform.scale_control_plane import (
    PlatformReadinessSnapshot,
    run_platform_readiness_snapshot,
)
from auto_client_acquisition.platform.self_evolving_core import (
    SelfEvolvingCoreReport,
    run_self_evolving_core,
)
from auto_client_acquisition.platform.workflow_registry import (
    WorkflowRegistration,
    get_workflow,
    list_workflows,
    register_workflow,
    rollback_workflow,
)

__all__ = [
    'AgentGovernanceStatus',
    'AgentLifecycleState',
    'AgentRegistration',
    'AuditRecord',
    'ExecutiveInsightPack',
    'MemoryRecord',
    'MemorySensitivity',
    'OrchestrationDecision',
    'OrgIntelligenceReport',
    'PlatformReadinessSnapshot',
    'RuntimeActionRequest',
    'RuntimeActionResult',
    'SelfEvolvingCoreReport',
    'WorkflowRegistration',
    'assess_agent_governance',
    'build_executive_insight_pack',
    'build_org_intelligence',
    'choose_orchestration_variant',
    'explain_action',
    'get_agent',
    'get_workflow',
    'govern_action',
    'lifecycle_transition_allowed',
    'list_agents',
    'list_audit_events',
    'list_workflows',
    'record_audit_event',
    'register_agent',
    'register_workflow',
    'rollback_agent',
    'rollback_workflow',
    'run_platform_readiness_snapshot',
    'run_self_evolving_core',
    'suspend_agent',
]
