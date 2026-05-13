"""Proof Pack v2 — 14-section structure with Source Passports + Blocked Risks + Limitations."""

from __future__ import annotations

from dataclasses import dataclass


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
    "retainer_or_expansion_path",
    "capital_assets_created",
)


@dataclass(frozen=True)
class ProofPackV2:
    engagement_id: str
    sections: frozenset[str]

    def missing_sections(self) -> tuple[str, ...]:
        return tuple(s for s in PROOF_PACK_V2_SECTIONS if s not in self.sections)

    def is_complete(self) -> bool:
        return not self.missing_sections()
