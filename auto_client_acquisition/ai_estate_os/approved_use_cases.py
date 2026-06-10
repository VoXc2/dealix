"""Approved AI use cases registry (slugs)."""

from __future__ import annotations

APPROVED_USE_CASE_SLUGS: frozenset[str] = frozenset(
    {
        "internal_draft_assist",
        "ranked_accounts",
        "governed_summaries",
    },
)


def use_case_approved(slug: str) -> bool:
    return slug.strip() in APPROVED_USE_CASE_SLUGS


__all__ = ["APPROVED_USE_CASE_SLUGS", "use_case_approved"]
