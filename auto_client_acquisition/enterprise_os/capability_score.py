"""Enterprise facade — same DCI as Intelligence OS (client capability product)."""

from __future__ import annotations

from auto_client_acquisition.intelligence_os.capability_index import (
    CapabilityScores,
    compute_dci,
)

compute_dealix_capability_score = compute_dci

__all__ = ["CapabilityScores", "compute_dci", "compute_dealix_capability_score"]
