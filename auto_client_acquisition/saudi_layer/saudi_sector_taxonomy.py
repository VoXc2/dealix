"""Saudi sector taxonomy (minimal deterministic slugs)."""

from __future__ import annotations

SAUDI_B2B_SECTORS: frozenset[str] = frozenset(
    {
        "technology",
        "services",
        "consulting",
        "training",
        "real_estate_services",
        "logistics",
        "healthcare_services",
    },
)


def sector_known(slug: str) -> bool:
    return slug.strip().lower() in SAUDI_B2B_SECTORS


__all__ = ["SAUDI_B2B_SECTORS", "sector_known"]
