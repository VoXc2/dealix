"""Proof Pack v2 — fourteen canonical sections."""

from __future__ import annotations

from collections.abc import Mapping

PROOF_PACK_V2_SECTIONS: tuple[str, ...] = (
    "executive_summary",
    "problem",
    "inputs",
    "source_passports",
    "work_completed",
    "outputs",
    "quality_scores",
    "governance_decisions",
    "blocked_risks",
    "value_metrics",
    "limitations",
    "recommended_next_step",
    "retainer_expansion_path",
    "capital_assets_created",
)


def proof_pack_v2_sections_complete(
    content_by_section: Mapping[str, str],
) -> tuple[bool, tuple[str, ...]]:
    missing = [
        k for k in PROOF_PACK_V2_SECTIONS if not (content_by_section.get(k) or "").strip()
    ]
    return not missing, tuple(missing)
