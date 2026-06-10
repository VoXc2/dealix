"""Five-level proof taxonomy — activity through operating capability."""

from __future__ import annotations

# (level_id, internal_slug) — narrative in docs/proof_architecture/ENTERPRISE_PROOF_ARCHITECTURE.md
PROOF_LEVELS: tuple[tuple[int, str], ...] = (
    (1, "activity"),
    (2, "output"),
    (3, "quality"),
    (4, "business_value"),
    (5, "operating_capability"),
)


def proof_level_valid(level: int) -> bool:
    return level in {lid for lid, _ in PROOF_LEVELS}


def proof_level_opens_retainer_path(level: int) -> bool:
    """Level 5 — operating capability — is the narrative gate for sustainable retainers."""
    return level == 5
