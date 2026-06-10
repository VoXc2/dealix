"""Dominance execution OS — scorecard, proof→retainer, readiness, holding."""

from __future__ import annotations

from auto_client_acquisition.dominance_os.dominance_scorecard import (
    DominanceScorecard,
    recommend_dominance_focus,
)
from auto_client_acquisition.dominance_os.enterprise_readiness import (
    EnterpriseReadinessLevel,
    infer_enterprise_readiness_level,
)
from auto_client_acquisition.dominance_os.holding_sequence import (
    HOLDING_SEQUENCE_STEP_IDS,
    holding_sequence_progress,
)
from auto_client_acquisition.dominance_os.proof_to_retainer import (
    PostProofDecision,
    ProductizationGateInputs,
    ProofStrengthInputs,
    RetainerEligibilityInputs,
    compute_proof_strength_score,
    is_retainer_eligible,
    passes_productization_gate,
    proof_usable_for_sales,
    recommend_post_proof_decision,
)
from auto_client_acquisition.dominance_os.standardization_path import (
    StandardizationStep,
    max_standardization_step_reached,
)

__all__ = [
    "HOLDING_SEQUENCE_STEP_IDS",
    "DominanceScorecard",
    "EnterpriseReadinessLevel",
    "PostProofDecision",
    "ProductizationGateInputs",
    "ProofStrengthInputs",
    "RetainerEligibilityInputs",
    "StandardizationStep",
    "compute_proof_strength_score",
    "holding_sequence_progress",
    "infer_enterprise_readiness_level",
    "is_retainer_eligible",
    "max_standardization_step_reached",
    "passes_productization_gate",
    "proof_usable_for_sales",
    "recommend_dominance_focus",
    "recommend_post_proof_decision",
]
