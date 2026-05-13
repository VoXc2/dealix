"""Dealix Command & Control OS — runs Dealix in real time.

Companion docs live under ``docs/command_control/``. These modules are
the typed surfaces of the Command Model: the Command Center decision
shape, control metrics, governance and data-access vocabularies, the
agent control plane, audit trail records, proof scoring, capital
recording, productization gating, and enterprise readiness mapping.

All modules are dependency-free and side-effect-free.
"""

from __future__ import annotations

from auto_client_acquisition.command_control_os.agent_control_plane import (
    AgentControlPlane,
    AutonomyDecision,
)
from auto_client_acquisition.command_control_os.audit_trail import (
    AuditEvent,
    AuditTrail,
)
from auto_client_acquisition.command_control_os.capital_command import (
    CapitalAssetRecord,
    CapitalType,
    EngagementCapitalSummary,
    engagement_strategically_complete,
)
from auto_client_acquisition.command_control_os.command_center import (
    CommandDecision,
    CommandDecisionType,
    CommandPriority,
    DecisionLog,
)
from auto_client_acquisition.command_control_os.control_metrics import (
    ControlMetricsSnapshot,
    NORTH_STAR,
    SUPPORTING_METRICS,
)
from auto_client_acquisition.command_control_os.data_access_governance import (
    DataAccessDecision,
    DataAccessRequest,
    evaluate_data_access,
)
from auto_client_acquisition.command_control_os.enterprise_readiness import (
    READINESS_LEVELS,
    ReadinessLevel,
    ReadinessRequirement,
    can_sell_level,
)
from auto_client_acquisition.command_control_os.governance_command import (
    GovernanceCommandQuestion,
    GovernanceCommandRecord,
    REQUIRED_GOVERNANCE_QUESTIONS,
)
from auto_client_acquisition.command_control_os.productization_command import (
    ProductizationCandidate,
    ProductizationGate,
    ProductizationStep,
    evaluate_productization,
)
from auto_client_acquisition.command_control_os.proof_command import (
    ProofDecisionTier,
    ProofScoreInputs,
    classify_proof_score,
    compute_proof_score,
)

__all__ = [
    "AgentControlPlane",
    "AutonomyDecision",
    "AuditEvent",
    "AuditTrail",
    "CapitalAssetRecord",
    "CapitalType",
    "EngagementCapitalSummary",
    "engagement_strategically_complete",
    "CommandDecision",
    "CommandDecisionType",
    "CommandPriority",
    "DecisionLog",
    "ControlMetricsSnapshot",
    "NORTH_STAR",
    "SUPPORTING_METRICS",
    "DataAccessDecision",
    "DataAccessRequest",
    "evaluate_data_access",
    "READINESS_LEVELS",
    "ReadinessLevel",
    "ReadinessRequirement",
    "can_sell_level",
    "GovernanceCommandQuestion",
    "GovernanceCommandRecord",
    "REQUIRED_GOVERNANCE_QUESTIONS",
    "ProductizationCandidate",
    "ProductizationGate",
    "ProductizationStep",
    "evaluate_productization",
    "ProofDecisionTier",
    "ProofScoreInputs",
    "classify_proof_score",
    "compute_proof_score",
]
