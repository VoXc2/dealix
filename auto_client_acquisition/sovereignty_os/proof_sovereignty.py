"""Proof Sovereignty — required sections + completeness check.

See ``docs/sovereignty/PROOF_SOVEREIGNTY.md``. The sovereignty edition
adds ``limitations`` as a required section beyond the endgame proof
pack shape.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class SovereignProofRule(str, Enum):
    NO_PROOF_NO_CLAIM = "no_proof_no_claim"
    NO_PROOF_NO_RETAINER_PUSH = "no_proof_no_retainer_push"
    NO_PROOF_NO_PUBLIC_CASE = "no_proof_no_public_case"


PROOF_PACK_REQUIRED_SECTIONS: tuple[str, ...] = (
    "problem",
    "inputs",
    "work_completed",
    "metrics",
    "before_after",
    "ai_outputs",
    "governance_events",
    "business_value",
    "risks",
    "limitations",
    "recommended_next_step",
)


@dataclass(frozen=True)
class SovereignProofPack:
    """Sovereign-edition proof pack.

    Producers populate ``sections`` with the names that have content.
    """

    engagement_id: str
    sections: frozenset[str]
    has_score: bool
    has_evidence_quality: bool
    has_governance_confidence: bool
    has_retainer_linkage: bool
    case_safe_version_available: bool

    def missing_sections(self) -> tuple[str, ...]:
        return tuple(s for s in PROOF_PACK_REQUIRED_SECTIONS if s not in self.sections)


def proof_pack_complete(pack: SovereignProofPack) -> tuple[bool, tuple[str, ...]]:
    """Return ``(complete, reasons)``.

    A pack is complete when every required section is present and the
    sovereignty dimensions (score, evidence quality, governance
    confidence, retainer linkage) are populated.
    """

    reasons: list[str] = []
    missing = pack.missing_sections()
    if missing:
        reasons.append("missing_sections:" + ",".join(missing))
    if not pack.has_score:
        reasons.append("missing_score")
    if not pack.has_evidence_quality:
        reasons.append("missing_evidence_quality")
    if not pack.has_governance_confidence:
        reasons.append("missing_governance_confidence")
    if not pack.has_retainer_linkage:
        reasons.append("missing_retainer_linkage")
    return (not reasons, tuple(reasons))
