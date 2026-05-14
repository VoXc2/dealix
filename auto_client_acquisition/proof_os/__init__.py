"""Proof OS — canonical proof pack checks (delegates to proof_architecture_os)."""

from auto_client_acquisition.proof_os.proof_pack import (
    PROOF_PACK_V2_SECTIONS,
    build_empty_proof_pack_v2,
    merge_proof_pack_v2,
    proof_pack_v2_sections_complete,
)
from auto_client_acquisition.proof_os.proof_score import (
    proof_pack_completeness_score,
    proof_pack_score_with_governance_penalty,
    proof_strength_band,
)

__all__ = [
    "PROOF_PACK_V2_SECTIONS",
    "build_empty_proof_pack_v2",
    "merge_proof_pack_v2",
    "proof_pack_completeness_score",
    "proof_pack_score_with_governance_penalty",
    "proof_pack_v2_sections_complete",
    "proof_strength_band",
]
