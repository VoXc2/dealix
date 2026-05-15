"""org_consciousness_os — Organizational Consciousness & Governance.

Systems 36-45: a read-only synthesis layer that fuses signals already
produced by existing Dealix ledgers/stores (friction_log, observability,
the revenue event store, the agent registry, approval center, audit and
governance modules) into organizational awareness, reasoning, governance,
resilience, trust, value, learning, meta-orchestration, strategic
intelligence and (draft-only) self-evolution.

Doctrine posture: this module owns no persistence — it has no ``store.py``
and no ``aggregator.py`` by design. It never sends, never charges, never
executes external actions and spawns no agents. System 45 produces DRAFT
proposals only; there is no ``apply`` path. See ``schemas.DOCTRINE_POSTURE``.
"""

from __future__ import annotations

from auto_client_acquisition.org_consciousness_os.causal import build_causal_report
from auto_client_acquisition.org_consciousness_os.consciousness import (
    synthesize_consciousness,
)
from auto_client_acquisition.org_consciousness_os.learning import detect_learning_patterns
from auto_client_acquisition.org_consciousness_os.meta_orchestration import (
    recommend_meta_orchestration,
)
from auto_client_acquisition.org_consciousness_os.resilience import compute_resilience
from auto_client_acquisition.org_consciousness_os.schemas import (
    DOCTRINE_POSTURE,
    AgentAccountabilityRecord,
    CausalLink,
    CausalReasoningReport,
    EvolutionProposal,
    ExecutionHealthSignal,
    LearningFabricReport,
    LearningPattern,
    MetaOrchestrationRecommendation,
    OperationalValueSignal,
    OrgConsciousnessSnapshot,
    ResilienceSignal,
    StrategicBenchmark,
    StrategicIntelligenceReport,
    TrustSignal,
    WorkforceGovernanceReport,
)
from auto_client_acquisition.org_consciousness_os.self_evolving import (
    propose_optimizations,
)
from auto_client_acquisition.org_consciousness_os.signals import compute_execution_health
from auto_client_acquisition.org_consciousness_os.strategic import benchmark_customer
from auto_client_acquisition.org_consciousness_os.trust import compute_trust
from auto_client_acquisition.org_consciousness_os.value import compute_operational_value
from auto_client_acquisition.org_consciousness_os.workforce_governance import (
    agent_accountability,
    build_workforce_governance,
)

__all__ = [
    "DOCTRINE_POSTURE",
    "AgentAccountabilityRecord",
    "CausalLink",
    "CausalReasoningReport",
    "EvolutionProposal",
    "ExecutionHealthSignal",
    "LearningFabricReport",
    "LearningPattern",
    "MetaOrchestrationRecommendation",
    "OperationalValueSignal",
    "OrgConsciousnessSnapshot",
    "ResilienceSignal",
    "StrategicBenchmark",
    "StrategicIntelligenceReport",
    "TrustSignal",
    "WorkforceGovernanceReport",
    "agent_accountability",
    "benchmark_customer",
    "build_causal_report",
    "build_workforce_governance",
    "compute_execution_health",
    "compute_operational_value",
    "compute_resilience",
    "compute_trust",
    "detect_learning_patterns",
    "propose_optimizations",
    "recommend_meta_orchestration",
    "synthesize_consciousness",
]
