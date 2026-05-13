"""Dealix Client Maturity OS — AI Transformation Ladder + Maturity Score."""

from __future__ import annotations

from auto_client_acquisition.client_maturity_os.maturity_engine import (
    MATURITY_OFFER_MATRIX,
    MaturityEngineInputs,
    MaturityEngineResult,
    classify_maturity_level,
)
from auto_client_acquisition.client_maturity_os.maturity_score import (
    MATURITY_WEIGHTS,
    MaturityComponents,
    MaturityTier,
    classify_maturity_tier,
    compute_maturity_score,
)

__all__ = [
    "MATURITY_OFFER_MATRIX",
    "MaturityEngineInputs",
    "MaturityEngineResult",
    "classify_maturity_level",
    "MATURITY_WEIGHTS",
    "MaturityComponents",
    "MaturityTier",
    "classify_maturity_tier",
    "compute_maturity_score",
]
