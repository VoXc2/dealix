"""Case study candidate record — internal flag only."""
from __future__ import annotations

from typing import Any


def case_study_candidate(*, sector: str, proof_theme: str) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "sector": sector,
        "theme": proof_theme,
        "status": "candidate_internal_only",
        "requires_customer_signoff": True,
    }
