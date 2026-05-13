"""Dealix Institutional-Grade Governance & Control OS.

Companion docs live under ``docs/institutional_control/``. Typed
surfaces for the institutional governance stack: source passport
enforcement, runtime governance evaluation chain, agent control plane,
audit trail with coverage targets, proof score with institutional
weights, governance coverage metrics with 100%-required thresholds,
and the incident-response taxonomy.
"""

from __future__ import annotations

from auto_client_acquisition.institutional_control_os.agent_control_plane import (
    InstitutionalAgentCard,
    evaluate_institutional_agent,
)
from auto_client_acquisition.institutional_control_os.audit_trail import (
    AUDIT_COVERAGE_TARGETS,
    AuditCoverageReport,
    InstitutionalAuditEvent,
    evaluate_audit_coverage,
)
from auto_client_acquisition.institutional_control_os.control_metrics import (
    INSTITUTIONAL_THRESHOLDS,
    InstitutionalControlSnapshot,
    evaluate_institutional_controls,
)
from auto_client_acquisition.institutional_control_os.governance_runtime import (
    GovernanceRuntimeQuestion,
    REQUIRED_RUNTIME_QUESTIONS,
    RuntimeEvaluationRecord,
)
from auto_client_acquisition.institutional_control_os.incident_response import (
    INCIDENT_RESPONSE_STEPS,
    IncidentRecord,
    IncidentSeverity,
    IncidentType,
    incident_must_create_change,
)
from auto_client_acquisition.institutional_control_os.proof_governance import (
    INSTITUTIONAL_PROOF_WEIGHTS,
    InstitutionalProofComponents,
    ProofDecisionTier,
    compute_institutional_proof_score,
)
from auto_client_acquisition.institutional_control_os.source_passport import (
    enforce_source_passport_use,
)

__all__ = [
    "InstitutionalAgentCard",
    "evaluate_institutional_agent",
    "AUDIT_COVERAGE_TARGETS",
    "AuditCoverageReport",
    "InstitutionalAuditEvent",
    "evaluate_audit_coverage",
    "INSTITUTIONAL_THRESHOLDS",
    "InstitutionalControlSnapshot",
    "evaluate_institutional_controls",
    "GovernanceRuntimeQuestion",
    "REQUIRED_RUNTIME_QUESTIONS",
    "RuntimeEvaluationRecord",
    "INCIDENT_RESPONSE_STEPS",
    "IncidentRecord",
    "IncidentSeverity",
    "IncidentType",
    "incident_must_create_change",
    "INSTITUTIONAL_PROOF_WEIGHTS",
    "InstitutionalProofComponents",
    "ProofDecisionTier",
    "compute_institutional_proof_score",
    "enforce_source_passport_use",
]
