"""Proof Pack Standard — re-exports v2 pack + score."""

from __future__ import annotations

from auto_client_acquisition.proof_architecture_os.proof_pack_v2 import (
    PROOF_PACK_V2_SECTIONS,
    ProofPackV2,
)
from auto_client_acquisition.proof_architecture_os.proof_score_v2 import (
    PROOF_SCORE_V2_WEIGHTS,
    ProofComponentsV2,
    compute_proof_score_v2,
)

__all__ = [
    "PROOF_PACK_V2_SECTIONS",
    "ProofPackV2",
    "PROOF_SCORE_V2_WEIGHTS",
    "ProofComponentsV2",
    "compute_proof_score_v2",
]
