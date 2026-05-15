"""Operational Dominance registry for Systems 26-35 and /platform/* contracts."""

from __future__ import annotations

import importlib
from dataclasses import dataclass


@dataclass(frozen=True)
class PlatformContract:
    system_id: int
    system_name: str
    platform_path: str
    module_path: str
    symbol: str


PLATFORM_CONTRACTS: tuple[PlatformContract, ...] = (
    PlatformContract(26, "organizational_control_plane", "/platform/control_plane", "auto_client_acquisition.operational_fabric_os.control_plane", "create_workflow"),
    PlatformContract(26, "organizational_control_plane", "/platform/operational_routing", "auto_client_acquisition.operational_fabric_os.control_plane", "reroute_workflow"),
    PlatformContract(26, "organizational_control_plane", "/platform/state_coordination", "auto_client_acquisition.operational_fabric_os.control_plane", "append_checkpoint"),
    PlatformContract(26, "organizational_control_plane", "/platform/global_orchestration", "auto_client_acquisition.operational_fabric_os.control_plane", "observe_workflow"),
    PlatformContract(27, "agent_mesh_infrastructure", "/platform/agent_mesh", "auto_client_acquisition.operational_fabric_os.agent_mesh", "AgentMesh"),
    PlatformContract(27, "agent_mesh_infrastructure", "/platform/agent_discovery", "auto_client_acquisition.operational_fabric_os.agent_mesh", "AgentMesh"),
    PlatformContract(27, "agent_mesh_infrastructure", "/platform/capability_registry", "auto_client_acquisition.operational_fabric_os.agent_mesh", "AgentDescriptor"),
    PlatformContract(27, "agent_mesh_infrastructure", "/platform/inter_agent_protocols", "auto_client_acquisition.operational_fabric_os.agent_mesh", "AgentDescriptor"),
    PlatformContract(27, "agent_mesh_infrastructure", "/platform/agent_routing", "auto_client_acquisition.operational_fabric_os.agent_mesh", "AgentMesh"),
    PlatformContract(28, "assurance_contract_engine", "/platform/assurance_contracts", "auto_client_acquisition.operational_fabric_os.assurance_contracts", "AssuranceContract"),
    PlatformContract(28, "assurance_contract_engine", "/platform/execution_contracts", "auto_client_acquisition.operational_fabric_os.assurance_contracts", "evaluate_contract"),
    PlatformContract(28, "assurance_contract_engine", "/platform/rollback_contracts", "auto_client_acquisition.operational_fabric_os.assurance_contracts", "evaluate_contract"),
    PlatformContract(28, "assurance_contract_engine", "/platform/governance_contracts", "auto_client_acquisition.operational_fabric_os.assurance_contracts", "evaluate_contract"),
    PlatformContract(29, "enterprise_sandbox_engine", "/platform/sandbox", "auto_client_acquisition.operational_fabric_os.sandbox_engine", "sandbox_gate"),
    PlatformContract(29, "enterprise_sandbox_engine", "/platform/simulation", "auto_client_acquisition.operational_fabric_os.sandbox_engine", "SandboxExecutionPlan"),
    PlatformContract(29, "enterprise_sandbox_engine", "/platform/canary_rollouts", "auto_client_acquisition.operational_fabric_os.sandbox_engine", "promote_from_canary"),
    PlatformContract(29, "enterprise_sandbox_engine", "/platform/replay_engine", "auto_client_acquisition.operational_fabric_os.sandbox_engine", "SandboxExecutionPlan"),
    PlatformContract(30, "operational_memory_graph", "/platform/org_graph", "auto_client_acquisition.operational_fabric_os.operational_memory_graph", "OperationalMemoryGraph"),
    PlatformContract(30, "operational_memory_graph", "/platform/dependency_graph", "auto_client_acquisition.operational_fabric_os.operational_memory_graph", "OperationalMemoryGraph"),
    PlatformContract(30, "operational_memory_graph", "/platform/relationship_engine", "auto_client_acquisition.operational_fabric_os.operational_memory_graph", "OperationalMemoryGraph"),
    PlatformContract(30, "operational_memory_graph", "/platform/context_graph", "auto_client_acquisition.operational_fabric_os.operational_memory_graph", "OperationalMemoryGraph"),
    PlatformContract(31, "enterprise_safety_engine", "/platform/runtime_safety", "auto_client_acquisition.operational_fabric_os.runtime_safety", "register_execution"),
    PlatformContract(31, "enterprise_safety_engine", "/platform/circuit_breakers", "auto_client_acquisition.operational_fabric_os.runtime_safety", "RuntimeSafetyState"),
    PlatformContract(31, "enterprise_safety_engine", "/platform/kill_switches", "auto_client_acquisition.operational_fabric_os.runtime_safety", "activate_kill_switch"),
    PlatformContract(31, "enterprise_safety_engine", "/platform/execution_limits", "auto_client_acquisition.operational_fabric_os.runtime_safety", "RuntimeSafetyPolicy"),
    PlatformContract(32, "organizational_simulation_engine", "/platform/org_simulation", "auto_client_acquisition.operational_fabric_os.org_simulation", "run_release_simulation"),
    PlatformContract(32, "organizational_simulation_engine", "/platform/workflow_simulation", "auto_client_acquisition.operational_fabric_os.org_simulation", "SimulationSpec"),
    PlatformContract(32, "organizational_simulation_engine", "/platform/failure_simulation", "auto_client_acquisition.operational_fabric_os.org_simulation", "SimulationSpec"),
    PlatformContract(32, "organizational_simulation_engine", "/platform/load_simulation", "auto_client_acquisition.operational_fabric_os.org_simulation", "SimulationSpec"),
    PlatformContract(33, "human_ai_operating_model", "/platform/human_ai_operating_model", "auto_client_acquisition.operational_fabric_os.human_ai_model", "evaluate_human_ai_request"),
    PlatformContract(33, "human_ai_operating_model", "/platform/escalation", "auto_client_acquisition.operational_fabric_os.human_ai_model", "OversightDecision"),
    PlatformContract(33, "human_ai_operating_model", "/platform/delegation", "auto_client_acquisition.operational_fabric_os.human_ai_model", "DelegationRequest"),
    PlatformContract(33, "human_ai_operating_model", "/platform/approval_center", "auto_client_acquisition.operational_fabric_os.human_ai_model", "evaluate_human_ai_request"),
    PlatformContract(34, "business_value_engine", "/platform/value_engine", "auto_client_acquisition.operational_fabric_os.business_value_engine", "compute_value_snapshot"),
    PlatformContract(34, "business_value_engine", "/platform/roi_tracking", "auto_client_acquisition.operational_fabric_os.business_value_engine", "ValueSnapshot"),
    PlatformContract(34, "business_value_engine", "/platform/impact_analysis", "auto_client_acquisition.operational_fabric_os.business_value_engine", "ValueSnapshot"),
    PlatformContract(34, "business_value_engine", "/platform/efficiency_metrics", "auto_client_acquisition.operational_fabric_os.business_value_engine", "workflow_has_measurable_kpis"),
    PlatformContract(35, "self_evolving_enterprise_fabric", "/platform/self_evolving_fabric", "auto_client_acquisition.operational_fabric_os.self_evolving_fabric", "recommend_evolution"),
    PlatformContract(35, "self_evolving_enterprise_fabric", "/platform/meta_learning", "auto_client_acquisition.operational_fabric_os.self_evolving_fabric", "recommend_evolution"),
    PlatformContract(35, "self_evolving_enterprise_fabric", "/platform/meta_orchestration", "auto_client_acquisition.operational_fabric_os.self_evolving_fabric", "EvolutionCycleInput"),
    PlatformContract(35, "self_evolving_enterprise_fabric", "/platform/continuous_optimization", "auto_client_acquisition.operational_fabric_os.self_evolving_fabric", "continuous_optimization_ready"),
)


def contract_count() -> int:
    return len(PLATFORM_CONTRACTS)


def contracts_by_system() -> dict[int, list[PlatformContract]]:
    out: dict[int, list[PlatformContract]] = {}
    for contract in PLATFORM_CONTRACTS:
        out.setdefault(contract.system_id, []).append(contract)
    return out


def validate_contract_bindings() -> tuple[bool, tuple[str, ...]]:
    errors: list[str] = []
    for contract in PLATFORM_CONTRACTS:
        try:
            module = importlib.import_module(contract.module_path)
        except Exception as exc:
            errors.append(f"import_failed:{contract.platform_path}:{exc}")
            continue
        if not hasattr(module, contract.symbol):
            errors.append(f"missing_symbol:{contract.platform_path}:{contract.symbol}")
    return (not errors, tuple(errors))


def operational_dominance_status() -> dict[str, object]:
    grouped = contracts_by_system()
    bindings_ok, errors = validate_contract_bindings()
    systems: list[dict[str, object]] = []
    for system_id in sorted(grouped.keys()):
        contracts = grouped[system_id]
        systems.append(
            {
                "system_id": system_id,
                "system_name": contracts[0].system_name,
                "contracts": [c.platform_path for c in contracts],
                "contract_count": len(contracts),
            }
        )
    return {
        "systems_total": len(grouped),
        "contracts_total": contract_count(),
        "bindings_ok": bindings_ok,
        "errors": list(errors),
        "systems": systems,
    }
