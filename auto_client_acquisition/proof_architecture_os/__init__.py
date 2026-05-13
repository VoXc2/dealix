"""Dealix Enterprise Proof & Value Architecture OS.

Companion doc: ``docs/proof_architecture/PROOF_ARCHITECTURE_DOCTRINE.md``.
"""

from __future__ import annotations

from auto_client_acquisition.proof_architecture_os.case_safe_summary import (
    CaseSafeProofSummary,
    redact_to_case_safe,
)
from auto_client_acquisition.proof_architecture_os.proof_dashboard import (
    ProofDashboardSnapshot,
)
from auto_client_acquisition.proof_architecture_os.proof_level import (
    PROOF_LEVELS,
    ProofLevel,
)
from auto_client_acquisition.proof_architecture_os.proof_pack_v2 import (
    PROOF_PACK_V2_SECTIONS,
    ProofPackV2,
)
from auto_client_acquisition.proof_architecture_os.proof_score_v2 import (
    PROOF_SCORE_V2_WEIGHTS,
    ProofComponentsV2,
    compute_proof_score_v2,
)
from auto_client_acquisition.proof_architecture_os.roi_discipline import (
    ROILevel,
    ROIRecord,
)
from auto_client_acquisition.proof_architecture_os.value_ledger import (
    ValueEvent,
    ValueLedger,
)

__all__ = [
    "CaseSafeProofSummary",
    "redact_to_case_safe",
    "ProofDashboardSnapshot",
    "PROOF_LEVELS",
    "ProofLevel",
    "PROOF_PACK_V2_SECTIONS",
    "ProofPackV2",
    "PROOF_SCORE_V2_WEIGHTS",
    "ProofComponentsV2",
    "compute_proof_score_v2",
    "ROILevel",
    "ROIRecord",
    "ValueEvent",
    "ValueLedger",
]
