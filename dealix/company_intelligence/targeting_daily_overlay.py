"""Evidence-first overlay for the existing Daily Targeting runtime.

This module is intentionally not a scheduler, queue, CRM, graph, or sender.
It converts already-built TargetDossiers into bounded draft candidates that the
existing daily-targeting/war-room runtime can consume.

The overlay never grants live execution authority. A high target score can
produce a draft candidate only when the canonical pre-draft gate passes; the
returned record always requires downstream approval/authority and keeps live
execution false.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from dealix.company_intelligence.targeting import (
    TargetDossier,
    TargetScore,
    rank_dossiers,
)


@dataclass(frozen=True)
class DailyDraftCandidate:
    dossier_id: str
    company_id: str
    company_name: str
    canonical_domain: str
    target_value_score: float
    priority_band: str
    why_them: str
    why_now: str
    problem_hypothesis: str
    business_cost_hypothesis: str
    offer_route: str
    proof_baseline: str
    evidence_count: int
    relationship_state: str
    consent_state: str
    email_eligibility: str
    whatsapp_eligibility: str
    voice_eligibility: str
    approval_required: bool = True
    live_execution_authorized: bool = False

    def to_dict(self) -> dict[str, object]:
        return {
            "dossier_id": self.dossier_id,
            "company_id": self.company_id,
            "company_name": self.company_name,
            "canonical_domain": self.canonical_domain,
            "target_value_score": self.target_value_score,
            "priority_band": self.priority_band,
            "why_them": self.why_them,
            "why_now": self.why_now,
            "problem_hypothesis": self.problem_hypothesis,
            "business_cost_hypothesis": self.business_cost_hypothesis,
            "offer_route": self.offer_route,
            "proof_baseline": self.proof_baseline,
            "evidence_count": self.evidence_count,
            "relationship_state": self.relationship_state,
            "consent_state": self.consent_state,
            "email_eligibility": self.email_eligibility,
            "whatsapp_eligibility": self.whatsapp_eligibility,
            "voice_eligibility": self.voice_eligibility,
            "approval_required": self.approval_required,
            "live_execution_authorized": self.live_execution_authorized,
        }


def _candidate_from(dossier: TargetDossier, score: TargetScore) -> DailyDraftCandidate:
    if not score.eligible_for_draft:
        raise ValueError("held dossier cannot become a daily draft candidate")
    return DailyDraftCandidate(
        dossier_id=dossier.dossier_id,
        company_id=dossier.company_id,
        company_name=dossier.company_name,
        canonical_domain=dossier.canonical_domain,
        target_value_score=score.total,
        priority_band=score.priority_band.value,
        why_them=dossier.why_them,
        why_now=dossier.why_now,
        problem_hypothesis=dossier.problem_hypothesis,
        business_cost_hypothesis=dossier.business_cost_hypothesis,
        offer_route=dossier.offer_route,
        proof_baseline=dossier.proof_baseline,
        evidence_count=len(dossier.evidence),
        relationship_state=dossier.actionability.relationship.value,
        consent_state=dossier.actionability.consent.value,
        email_eligibility=dossier.actionability.email.value,
        whatsapp_eligibility=dossier.actionability.whatsapp.value,
        voice_eligibility=dossier.actionability.voice.value,
    )


def select_evidence_first_daily_drafts(
    dossiers: Iterable[TargetDossier],
    *,
    target_count: int = 20,
) -> list[DailyDraftCandidate]:
    """Return highest-value dossiers that pass the canonical pre-draft gate.

    ``target_count`` is a draft-capacity bound, never a send quota. Suppressed,
    stale-only, duplicate-active-thread, opted-out, or otherwise held dossiers
    are excluded by Targeting V1 before candidate creation.
    """
    if target_count < 0:
        raise ValueError("target_count must be non-negative")
    if target_count == 0:
        return []

    selected: list[DailyDraftCandidate] = []
    for dossier, score in rank_dossiers(dossiers):
        if not score.eligible_for_draft:
            continue
        selected.append(_candidate_from(dossier, score))
        if len(selected) >= target_count:
            break
    return selected


def daily_targeting_overlay_payload(
    dossiers: Iterable[TargetDossier],
    *,
    target_count: int = 20,
) -> dict[str, object]:
    """Machine-readable adapter payload for the existing targeting runtime."""
    candidates = select_evidence_first_daily_drafts(
        dossiers,
        target_count=target_count,
    )
    return {
        "mode": "targeting_v1_evidence_overlay",
        "draft_capacity": target_count,
        "selected_count": len(candidates),
        "selected": [candidate.to_dict() for candidate in candidates],
        "approval_required": True,
        "live_execution_authorized": False,
        "external_effects": "NONE",
    }
