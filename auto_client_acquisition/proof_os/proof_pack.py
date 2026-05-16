"""Proof Pack v2 surface for Revenue / Client OS (canonical sections).

Exposes ``assemble()`` — the Day 5 Proof Pack builder for the 7-Day Revenue
Intelligence Sprint. It fills the 14 canonical sections from sprint inputs,
scores completeness (with a governance penalty), and bands the result.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import asdict, dataclass, field
from typing import Any

from auto_client_acquisition.proof_architecture_os.proof_pack_v2 import (
    PROOF_PACK_V2_SECTIONS,
    proof_pack_v2_sections_complete,
)
from auto_client_acquisition.proof_os.proof_score import (
    proof_pack_score_with_governance_penalty,
    proof_strength_band,
)


def build_empty_proof_pack_v2() -> dict[str, str]:
    return dict.fromkeys(PROOF_PACK_V2_SECTIONS, "")


def merge_proof_pack_v2(base: Mapping[str, str], updates: Mapping[str, str]) -> dict[str, str]:
    out = build_empty_proof_pack_v2()
    out.update({k: (base.get(k) or "").strip() for k in PROOF_PACK_V2_SECTIONS})
    for k, v in updates.items():
        if k in PROOF_PACK_V2_SECTIONS:
            out[k] = str(v).strip()
    return out


@dataclass(frozen=True, slots=True)
class ProofPack:
    """An assembled 14-section Proof Pack with deterministic scoring."""

    engagement_id: str
    customer_id: str
    sections: dict[str, str]
    score: int
    tier: str
    sections_complete: bool
    missing_sections: tuple[str, ...] = field(default_factory=tuple)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self) | {"missing_sections": list(self.missing_sections)}


def _describe_passport(source_passport: Any) -> str:
    if source_passport is None:
        return "No Source Passport on file — AI use is gated until a passport is signed."
    sid = getattr(source_passport, "source_id", "?")
    owner = getattr(source_passport, "owner", "?")
    stype = getattr(source_passport, "source_type", "?")
    return f"Source Passport {sid} — owner: {owner}, type: {stype}."


def _describe_governance(governance_events: Sequence[Mapping[str, Any]]) -> tuple[str, str, bool]:
    """Return (decisions_text, blocked_risks_text, governance_blocked)."""
    if not governance_events:
        return ("No governed drafts in this engagement.", "No governance blocks recorded.", False)
    lines = [
        f"{e.get('decision', '?')}: {e.get('count', 0)}" for e in governance_events
    ]
    blocked = any(
        str(e.get("decision", "")).lower() in {"block", "blocked"} for e in governance_events
    )
    blocked_text = (
        "One or more drafts were blocked by governance — see governance decisions log."
        if blocked
        else "No governance blocks recorded."
    )
    return ("; ".join(lines), blocked_text, blocked)


def _describe_value(value_events: Sequence[Mapping[str, Any]]) -> str:
    if not value_events:
        return "No value events recorded yet — outcomes measured at handoff (estimates carry ~)."
    return f"{len(value_events)} value event(s) recorded; tiers per Value Ledger."


def assemble(
    *,
    engagement_id: str,
    customer_id: str,
    source_passport: Any = None,
    dq_score: float = 0.0,
    value_events: Sequence[Mapping[str, Any]] | None = None,
    governance_events: Sequence[Mapping[str, Any]] | None = None,
    work_completed: str = "",
    problem: str = "",
    outputs_summary: str = "",
    next_step: str = "",
) -> ProofPack:
    """Assemble a 14-section Proof Pack from sprint inputs (Day 5)."""
    gov_events = list(governance_events or [])
    decisions_text, blocked_text, gov_blocked = _describe_governance(gov_events)

    sections = build_empty_proof_pack_v2()
    sections["executive_summary"] = (
        f"7-Day Revenue Intelligence Sprint for {customer_id} (engagement {engagement_id})."
    )
    sections["problem"] = problem or "(provided in kickoff)"
    sections["inputs"] = work_completed or "Customer-supplied account data."
    sections["source_passports"] = _describe_passport(source_passport)
    sections["work_completed"] = work_completed or "10-step sprint executed."
    sections["outputs"] = outputs_summary or "Ranked accounts + governance-reviewed drafts."
    sections["quality_scores"] = f"Data Quality Score: {dq_score}."
    sections["governance_decisions"] = decisions_text
    sections["blocked_risks"] = blocked_text
    sections["value_metrics"] = _describe_value(list(value_events or []))
    sections["limitations"] = (
        "Estimates carry a ~ prefix; figures are observed-in-workflow "
        "unless cross-checked with a source reference."
    )
    sections["recommended_next_step"] = next_step or "Founder review and handoff."
    sections["retainer_expansion_path"] = (
        "Managed Revenue Ops eligibility evaluated at handoff (adoption + proof gates)."
    )
    sections["capital_assets_created"] = (
        "See Capital Ledger registration for this engagement."
    )

    score = proof_pack_score_with_governance_penalty(sections, governance_blocked=gov_blocked)
    complete, missing = proof_pack_v2_sections_complete(sections)
    return ProofPack(
        engagement_id=engagement_id,
        customer_id=customer_id,
        sections=sections,
        score=score,
        tier=proof_strength_band(score),
        sections_complete=complete,
        missing_sections=missing,
    )


__all__ = [
    "PROOF_PACK_V2_SECTIONS",
    "ProofPack",
    "assemble",
    "build_empty_proof_pack_v2",
    "merge_proof_pack_v2",
    "proof_pack_v2_sections_complete",
]
