"""Dealix Standards OS — D-GAOS sub-standards as typed surfaces."""

from __future__ import annotations

from auto_client_acquisition.standards_os.agent_control_standard import (
    AgentCard,
    AutonomyLevel,
    InstitutionalAgentCard,
)
from auto_client_acquisition.standards_os.capability_standard import (
    DCI_AXES,
    DCIAxis,
    DCIMaturity,
    DCIReport,
)
from auto_client_acquisition.standards_os.certification import (
    CERTIFICATION_LEVELS,
    CertificationLevel,
)
from auto_client_acquisition.standards_os.data_readiness_standard import (
    DataReadinessComponents,
    DataReadinessTier,
    classify_data_readiness,
    compute_data_readiness_score,
)
from auto_client_acquisition.standards_os.governance_standard import (
    GovernanceDecision,
    GovernanceRuntimeQuestion,
    RuntimeEvaluationRecord,
)
from auto_client_acquisition.standards_os.partner_gate import (
    PartnerCovenant,
    PartnerScoreComponents,
    classify_partner_ladder,
    compute_partner_score,
    evaluate_partner_covenant,
)
from auto_client_acquisition.standards_os.proof_pack_standard import (
    PROOF_PACK_V2_SECTIONS,
    PROOF_SCORE_V2_WEIGHTS,
    ProofComponentsV2,
    ProofPackV2,
    compute_proof_score_v2,
)
from auto_client_acquisition.standards_os.qa_standard import (
    QA_DIMENSIONS,
    QADecision,
    QAResult,
    classify_qa_score,
)
from auto_client_acquisition.standards_os.source_passport_standard import (
    AllowedUse,
    SourcePassport,
    enforce_source_passport_use,
)
from auto_client_acquisition.standards_os.standards_index import (
    DEALIX_SUB_STANDARDS,
    SubStandard,
)

__all__ = [
    "AgentCard",
    "AutonomyLevel",
    "InstitutionalAgentCard",
    "DCI_AXES",
    "DCIAxis",
    "DCIMaturity",
    "DCIReport",
    "CERTIFICATION_LEVELS",
    "CertificationLevel",
    "DataReadinessComponents",
    "DataReadinessTier",
    "classify_data_readiness",
    "compute_data_readiness_score",
    "GovernanceDecision",
    "GovernanceRuntimeQuestion",
    "RuntimeEvaluationRecord",
    "PartnerCovenant",
    "PartnerScoreComponents",
    "classify_partner_ladder",
    "compute_partner_score",
    "evaluate_partner_covenant",
    "PROOF_PACK_V2_SECTIONS",
    "PROOF_SCORE_V2_WEIGHTS",
    "ProofComponentsV2",
    "ProofPackV2",
    "compute_proof_score_v2",
    "QA_DIMENSIONS",
    "QADecision",
    "QAResult",
    "classify_qa_score",
    "AllowedUse",
    "SourcePassport",
    "enforce_source_passport_use",
    "DEALIX_SUB_STANDARDS",
    "SubStandard",
]
