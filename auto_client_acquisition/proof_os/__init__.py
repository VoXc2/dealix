"""Canonical Proof OS — single assembler that composes Dealix outputs into
a 14-section Proof Pack with a deterministic proof_score.

Wraps existing proof_engine + proof_ledger + value_os + capital_os + data_os
+ governance_os.
"""
from auto_client_acquisition.proof_os.proof_pack import (
    ProofPack,
    assemble,
    classify_tier,
    compute_proof_score,
)

__all__ = [
    "ProofPack",
    "assemble",
    "classify_tier",
    "compute_proof_score",
]
