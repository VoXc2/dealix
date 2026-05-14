"""Canonical Adoption OS — wraps customer_success.health_score for the
Wave 2 adoption signal and adds a deterministic retainer-readiness gate.
"""
from auto_client_acquisition.adoption_os.adoption_score import (
    AdoptionScore,
    compute,
)
from auto_client_acquisition.adoption_os.retainer_readiness import (
    RetainerReadiness,
    evaluate,
)

__all__ = [
    "AdoptionScore",
    "RetainerReadiness",
    "compute",
    "evaluate",
]
