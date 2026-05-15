"""
Dealix Engine Layer — the Agentic Enterprise Platform.

Twelve governed engines that compose existing Dealix capabilities into the
"operating system for digital labor". The Governance Engine (Engine 4) is
built to production depth; the other 11 are registered, governed foundations.

See docs/agentic_operations/AGENTIC_ENTERPRISE_PLATFORM.md.
"""

from __future__ import annotations

from typing import Any

from dealix.engines.agent_runtime import AgentRuntimeEngine
from dealix.engines.base import (
    BaseEngine,
    EngineSpec,
    EngineStatus,
    PlannedCapabilityError,
)
from dealix.engines.digital_workforce import DigitalWorkforceEngine
from dealix.engines.evaluation import EvaluationEngine
from dealix.engines.evolution import EvolutionEngine
from dealix.engines.execution_engine import ExecutionEngine
from dealix.engines.executive import ExecutiveEngine
from dealix.engines.governance import GovernanceEngine
from dealix.engines.graph import GraphEngine
from dealix.engines.memory import MemoryEngine
from dealix.engines.observability_engine import ObservabilityEngine
from dealix.engines.registry import ENGINE_REGISTRY, EngineRegistry
from dealix.engines.transformation import TransformationEngine
from dealix.engines.workflow import WorkflowEngine

# engine_id -> engine class, for discovery and status reporting.
ENGINE_CLASSES: dict[str, type[BaseEngine]] = {
    "agent_runtime": AgentRuntimeEngine,
    "workflow": WorkflowEngine,
    "memory": MemoryEngine,
    "governance": GovernanceEngine,
    "executive": ExecutiveEngine,
    "graph": GraphEngine,
    "execution": ExecutionEngine,
    "evaluation": EvaluationEngine,
    "observability": ObservabilityEngine,
    "transformation": TransformationEngine,
    "digital_workforce": DigitalWorkforceEngine,
    "evolution": EvolutionEngine,
}


def all_status_reports() -> list[dict[str, Any]]:
    """Build a status report for every engine in the platform."""
    reports: list[dict[str, Any]] = []
    for spec in ENGINE_REGISTRY.all():
        engine = ENGINE_CLASSES[spec.engine_id]()
        reports.append(engine.status_report())
    return reports


__all__ = [
    "ENGINE_CLASSES",
    "ENGINE_REGISTRY",
    "AgentRuntimeEngine",
    "BaseEngine",
    "DigitalWorkforceEngine",
    "EngineRegistry",
    "EngineSpec",
    "EngineStatus",
    "EvaluationEngine",
    "EvolutionEngine",
    "ExecutionEngine",
    "ExecutiveEngine",
    "GovernanceEngine",
    "GraphEngine",
    "MemoryEngine",
    "ObservabilityEngine",
    "PlannedCapabilityError",
    "TransformationEngine",
    "WorkflowEngine",
    "all_status_reports",
]
