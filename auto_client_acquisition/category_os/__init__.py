"""Category OS — ownership score, content coverage, language adoption."""

from __future__ import annotations

from auto_client_acquisition.category_os.category_score import (
    CategoryOwnershipSignals,
    compute_category_ownership_score,
)
from auto_client_acquisition.category_os.content_signal import (
    CONTENT_ENGINE_PILLAR_IDS,
    CONTENT_ENGINE_PILLARS,
    content_pillar_coverage_score,
)
from auto_client_acquisition.category_os.language_adoption import (
    AVOIDED_POSITIONING_TERMS,
    PREFERRED_CATEGORY_TERMS,
    avoided_term_hits,
    language_adoption_index,
    preferred_term_hits,
)

__all__ = [
    "AVOIDED_POSITIONING_TERMS",
    "CONTENT_ENGINE_PILLARS",
    "CONTENT_ENGINE_PILLAR_IDS",
    "PREFERRED_CATEGORY_TERMS",
    "CategoryOwnershipSignals",
    "avoided_term_hits",
    "compute_category_ownership_score",
    "content_pillar_coverage_score",
    "language_adoption_index",
    "preferred_term_hits",
]
