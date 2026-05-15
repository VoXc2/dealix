"""Operational Fabric OS — Systems 26-35 foundation contracts."""

from auto_client_acquisition.operational_fabric_os.agent_mesh import AgentDescriptor, AgentMesh
from auto_client_acquisition.operational_fabric_os.assurance_contracts import (
    AssuranceContract,
    AssuranceEvaluation,
    evaluate_contract,
)
from auto_client_acquisition.operational_fabric_os.business_value_engine import (
    ValueSnapshot,
    WorkflowValueInput,
    compute_value_snapshot,
    workflow_has_measurable_kpis,
)
from auto_client_acquisition.operational_fabric_os.control_plane import (
    WorkflowControlState,
    append_checkpoint,
    create_workflow,
    observe_workflow,
    reroute_workflow,
    rollback_workflow,
    stop_workflow,
    update_workflow_policy,
)
from auto_client_acquisition.operational_fabric_os.human_ai_model import (
    DelegationRequest,
    OversightDecision,
    evaluate_human_ai_request,
)
from auto_client_acquisition.operational_fabric_os.operational_memory_graph import (
    OperationalMemoryGraph,
)
from auto_client_acquisition.operational_fabric_os.org_simulation import (
    SimulationResult,
    SimulationSpec,
    replay_supported,
    run_release_simulation,
)
from auto_client_acquisition.operational_fabric_os.runtime_safety import (
    RuntimeSafetyPolicy,
    RuntimeSafetyState,
    activate_kill_switch,
    isolate_agent,
    register_execution,
    rollback_permitted,
)
from auto_client_acquisition.operational_fabric_os.sandbox_engine import (
    SandboxExecutionPlan,
    promote_from_canary,
    sandbox_gate,
)
from auto_client_acquisition.operational_fabric_os.self_evolving_fabric import (
    EvolutionCycleInput,
    OptimizationProposal,
    continuous_optimization_ready,
    recommend_evolution,
)

__all__ = [
    "AgentDescriptor",
    "AgentMesh",
    "AssuranceContract",
    "AssuranceEvaluation",
    "DelegationRequest",
    "EvolutionCycleInput",
    "OperationalMemoryGraph",
    "OptimizationProposal",
    "OversightDecision",
    "RuntimeSafetyPolicy",
    "RuntimeSafetyState",
    "SandboxExecutionPlan",
    "SimulationResult",
    "SimulationSpec",
    "ValueSnapshot",
    "WorkflowControlState",
    "WorkflowValueInput",
    "activate_kill_switch",
    "append_checkpoint",
    "compute_value_snapshot",
    "continuous_optimization_ready",
    "create_workflow",
    "evaluate_contract",
    "evaluate_human_ai_request",
    "isolate_agent",
    "observe_workflow",
    "promote_from_canary",
    "recommend_evolution",
    "register_execution",
    "replay_supported",
    "reroute_workflow",
    "rollback_permitted",
    "rollback_workflow",
    "run_release_simulation",
    "sandbox_gate",
    "stop_workflow",
    "update_workflow_policy",
    "workflow_has_measurable_kpis",
]
