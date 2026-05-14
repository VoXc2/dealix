"""Certification ladder + exam components + capital minimum bundle."""

from __future__ import annotations

from auto_client_acquisition.ecosystem_os.certification import (
    CERTIFICATION_LEVELS,
    certification_level_valid,
    certification_slug_for_level,
)

CERTIFICATION_EXAM_COMPONENTS: tuple[str, ...] = (
    "knowledge_test",
    "case_simulation",
    "governance_test",
    "qa_review",
)


def certification_exam_components_complete(components_done: frozenset[str]) -> tuple[bool, tuple[str, ...]]:
    missing = [c for c in CERTIFICATION_EXAM_COMPONENTS if c not in components_done]
    return not missing, tuple(missing)


def capital_minimum_bundle_ok(
    *,
    trust_asset_delivered: bool,
    product_or_knowledge_asset_delivered: bool,
    expansion_path_documented: bool,
) -> bool:
    """Standard §12 — minimum capital outputs per engagement."""
    return (
        trust_asset_delivered
        and product_or_knowledge_asset_delivered
        and expansion_path_documented
    )
