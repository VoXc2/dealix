"""Source allow-list policy.

Hard guarantees:
  - Scraping sources are NEVER allowed.
  - Personal data sources are NEVER allowed.
  - Everything else passes through.
"""
from __future__ import annotations

from auto_client_acquisition.knowledge_v10.schemas import SourceType

_BLOCKED: frozenset[str] = frozenset({
    SourceType.BLOCKED_SCRAPING_SOURCE.value,
    SourceType.BLOCKED_PERSONAL_DATA_SOURCE.value,
})


def is_source_allowed(source_type: SourceType | str) -> bool:
    """Return True iff the source is on the allow-list."""
    value = source_type.value if isinstance(source_type, SourceType) else str(source_type)
    return value not in _BLOCKED
