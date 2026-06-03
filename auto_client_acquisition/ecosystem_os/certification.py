"""Certification ladder — market control through assessed levels."""

from __future__ import annotations

CERTIFICATION_LEVELS: tuple[tuple[int, str], ...] = (
    (1, "dealix_aware"),
    (2, "dealix_operator"),
    (3, "dealix_implementer"),
    (4, "dealix_certified_partner"),
    (5, "dealix_strategic_partner"),
)


def certification_level_valid(level: int) -> bool:
    return level in {lid for lid, _ in CERTIFICATION_LEVELS}


def certification_slug_for_level(level: int) -> str | None:
    for lid, slug in CERTIFICATION_LEVELS:
        if lid == level:
            return slug
    return None
