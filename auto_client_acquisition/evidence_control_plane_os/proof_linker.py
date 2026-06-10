"""Proof Pack v3 section slugs — evidence-backed proof."""

from __future__ import annotations

from collections.abc import Mapping

PROOF_PACK_V3_SECTIONS: tuple[str, ...] = (
    "executive_summary",
    "problem",
    "source_evidence",
    "ai_run_evidence",
    "governance_evidence",
    "human_review_evidence",
    "output_evidence",
    "value_evidence",
    "blocked_risk_evidence",
    "limitations",
    "recommended_next_action",
)


def proof_pack_v3_sections_complete(
    content_by_section: Mapping[str, str],
) -> tuple[bool, tuple[str, ...]]:
    missing = [k for k in PROOF_PACK_V3_SECTIONS if not (content_by_section.get(k) or "").strip()]
    return not missing, tuple(missing)
