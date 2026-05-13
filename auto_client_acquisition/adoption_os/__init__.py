"""Dealix Adoption OS — scoring and friction logging."""

from __future__ import annotations

from auto_client_acquisition.adoption_os.adoption_score import (
    ADOPTION_WEIGHTS,
    AdoptionComponents,
    AdoptionTier,
    classify_adoption,
    compute_adoption_score,
)
from auto_client_acquisition.adoption_os.friction_log import (
    FrictionEvent,
    FrictionLog,
    FrictionType,
)

__all__ = [
    "ADOPTION_WEIGHTS",
    "AdoptionComponents",
    "AdoptionTier",
    "classify_adoption",
    "compute_adoption_score",
    "FrictionEvent",
    "FrictionLog",
    "FrictionType",
]
