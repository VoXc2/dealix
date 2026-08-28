"""V18 Buyability Graph — buying-group model + decision-defensibility.

Workstream A/B of #1277. Never invents a person; never infers decision
power as fact; UNKNOWN is a valid state. The buyability score is a
prioritization aid and MUST NOT alter factual qualification state.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any


class BuyingRole(StrEnum):
    ECONOMIC_BUYER = "ECONOMIC_BUYER"
    DOMAIN_BUYER = "DOMAIN_BUYER"
    TECHNICAL_BUYER = "TECHNICAL_BUYER"
    USER = "USER"
    CHAMPION = "CHAMPION"
    FINANCE = "FINANCE"
    PROCUREMENT = "PROCUREMENT"
    LEGAL = "LEGAL"
    COMPLIANCE = "COMPLIANCE"
    SECURITY = "SECURITY"
    OPERATIONS = "OPERATIONS"
    EXECUTIVE_SPONSOR = "EXECUTIVE_SPONSOR"
    HIDDEN_BUYER = "HIDDEN_BUYER"
    BLOCKER = "BLOCKER"
    UNKNOWN_STAKEHOLDER = "UNKNOWN_STAKEHOLDER"


class RoleConfidence(StrEnum):
    UNKNOWN = "UNKNOWN"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


_VALID_ROLES = frozenset(r.value for r in BuyingRole)
_VALID_CONFIDENCES = frozenset(c.value for c in RoleConfidence)


@dataclass(frozen=True, slots=True)
class BuyingGroupMember:
    """One member of a buying group, source-bound only.

    Every member requires a SOURCE and an OBSERVED_FACT. A member with no
    observed fact is not a member — it is a guess. Names are optional and
    never invented.
    """

    role: str = BuyingRole.UNKNOWN_STAKEHOLDER.value
    source: str = ""
    observed_fact: str = ""
    role_confidence: str = RoleConfidence.UNKNOWN.value
    relationship_state: str = "unknown"
    concern: str = ""
    evidence_needed: str = ""
    content_needed: str = ""
    proof_needed: str = ""
    next_action: str = ""

    def is_provenanced(self) -> bool:
        return bool(str(self.source or "").strip()) and bool(
            str(self.observed_fact or "").strip()
        )

    def to_dict(self) -> dict[str, str]:
        return {
            "role": self.role,
            "source": self.source,
            "observed_fact": self.observed_fact,
            "role_confidence": self.role_confidence,
            "relationship_state": self.relationship_state,
            "concern": self.concern,
            "evidence_needed": self.evidence_needed,
            "content_needed": self.content_needed,
            "proof_needed": self.proof_needed,
            "next_action": self.next_action,
        }


@dataclass(frozen=True, slots=True)
class BuyingGroup:
    """ACCOUNT → BUYING_GROUP → MEMBER → CONCERN → EVIDENCE → NEXT_ACTION."""

    account_id: str
    members: tuple[BuyingGroupMember, ...] = ()

    def with_member(self, member: BuyingGroupMember) -> "BuyingGroup":
        return BuyingGroup(account_id=self.account_id, members=self.members + (member,))

    def role_present(self, role: str) -> bool:
        return any(m.role == role for m in self.members)

    def known_member_count(self) -> int:
        return sum(
            1
            for m in self.members
            if m.role != BuyingRole.UNKNOWN_STAKEHOLDER.value
        )

    def unprovenanced_count(self) -> int:
        return sum(1 for m in self.members if not m.is_provenanced())

    def to_dict(self) -> dict[str, Any]:
        return {
            "account_id": self.account_id,
            "members": [m.to_dict() for m in self.members],
        }


def default_buying_group(account_id: str) -> BuyingGroup:
    """Explicit UNKNOWN state is valid; no members are invented."""
    return BuyingGroup(account_id=account_id)


def validate_member(member: BuyingGroupMember) -> list[str]:
    """Deterministic provenance validation for a buying-group member."""
    errors: list[str] = []
    if member.role not in _VALID_ROLES:
        errors.append(f"INVALID_ROLE:{member.role}")
    if member.role_confidence not in _VALID_CONFIDENCES:
        errors.append(f"INVALID_ROLE_CONFIDENCE:{member.role_confidence}")
    if not member.is_provenanced():
        errors.append("MEMBER_WITHOUT_PROVENANCE")
    return errors


# ── Decision defensibility ─────────────────────────────────────────────────

_DEFENSIBILITY_FACTORS: tuple[str, ...] = (
    "PROBLEM_FIT",
    "STAKEHOLDER_ALIGNMENT",
    "TRUST",
    "BRAND_FAMILIARITY",
    "PEER_PROOF",
    "CUSTOMER_PROOF",
    "IMPLEMENTATION_RISK",
    "SECURITY_CONFIDENCE",
    "GOVERNANCE_CONFIDENCE",
    "ECONOMIC_DEFENSIBILITY",
    "PROCUREMENT_READINESS",
    "CHANGE_BURDEN",
    "INTEGRATION_BURDEN",
    "DECISION_REVERSIBILITY",
    "HIDDEN_BUYER_GAP",
)


@dataclass(frozen=True, slots=True)
class BuyabilityAssessment:
    """Decision-defensibility result. Score ranks work; it creates NO
    qualification evidence and must never change account state."""

    account_id: str
    buyability_score: float  # 0..100 ordinal aid, not pipeline value
    top_decision_risk: str = ""
    top_hidden_buyer_gap: str = ""
    proof_needed: list[str] = field(default_factory=list)
    content_needed: list[str] = field(default_factory=list)
    next_alignment_action: str = ""
    factor_scores: dict[str, int] = field(default_factory=dict)  # 0=unknown, 1..5
    assumptions: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "account_id": self.account_id,
            "buyability_score": round(self.buyability_score, 2),
            "top_decision_risk": self.top_decision_risk,
            "top_hidden_buyer_gap": self.top_hidden_buyer_gap,
            "proof_needed": self.proof_needed,
            "content_needed": self.content_needed,
            "next_alignment_action": self.next_alignment_action,
            "factor_scores": self.factor_scores,
            "assumptions": self.assumptions,
        }


def _factor_score(evidence: str, known: bool) -> int:
    """Map a defensibility factor to 0..5. 0 means no evidence (unknown)."""
    if not known:
        return 0
    text = str(evidence or "").strip().lower()
    if not text:
        return 0
    if "weak" in text or "unknown" in text or "none" in text:
        return 1
    if "moderate" in text or "partial" in text:
        return 3
    if "strong" in text or "confirmed" in text or "documented" in text:
        return 5
    return 2


def assess_buyability(
    account_id: str,
    *,
    group: BuyingGroup | None = None,
    factor_evidence: dict[str, str] | None = None,
) -> BuyabilityAssessment:
    """Compute the buyability/decision-defensibility assessment.

    factor_evidence maps factor name → evidence text (empty/absent = unknown).
    Score = mean of known factors × 20, minus penalties for unknown
    stakeholder state and unprovenanced members. This score is ordinal aid
    only and is capped at 100.
    """
    group = group or default_buying_group(account_id)
    factor_evidence = factor_evidence or {}
    assumptions: list[str] = []
    factor_scores: dict[str, int] = {}

    known_sum = 0
    known_count = 0
    for factor in _DEFENSIBILITY_FACTORS:
        evidence = factor_evidence.get(factor, "")
        known = bool(str(evidence or "").strip())
        score = _factor_score(evidence, known)
        factor_scores[factor] = score
        if known:
            known_sum += score
            known_count += 1
    if known_count == 0:
        assumptions.append("no defensibility evidence; score reflects unknowns only")
    base = (known_sum / (5 * len(_DEFENSIBILITY_FACTORS))) * 100

    # Penalties for real gaps (evidence-based, never invented).
    unprovenanced = group.unprovenanced_count()
    if unprovenanced:
        base -= 5 * unprovenanced
        assumptions.append(f"{unprovenanced} buying-group member(s) lack provenance")
    if group.role_present(BuyingRole.HIDDEN_BUYER.value):
        base -= 10
        assumptions.append("hidden buyer identified; decision risk elevated")
    if not group.role_present(BuyingRole.ECONOMIC_BUYER.value):
        base -= 10
        assumptions.append("no economic buyer member recorded")

    score = max(0.0, min(100.0, base))

    # Top risk / hidden-buyer gap are derived from the lowest evidence factor
    # and the buying group, not fabricated.
    top_risk = ""
    lowest = 6
    for factor in _DEFENSIBILITY_FACTORS:
        fscore = factor_scores[factor]
        if fscore < lowest:
            lowest = fscore
            top_risk = factor
    if group.role_present(BuyingRole.HIDDEN_BUYER.value):
        top_risk = "HIDDEN_BUYER_GAP"

    hidden_gap = (
        "ECONOMIC_BUYER_ABSENT"
        if not group.role_present(BuyingRole.ECONOMIC_BUYER.value)
        else ""
    )
    if group.role_present(BuyingRole.HIDDEN_BUYER.value):
        hidden_gap = "HIDDEN_BUYER_VETO_RISK"

    proof_needed = [
        f for f in ("CUSTOMER_PROOF", "PEER_PROOF") if factor_scores.get(f, 0) < 3
    ]
    content_needed = [
        f for f in ("PROBLEM_FIT", "STAKEHOLDER_ALIGNMENT") if factor_scores.get(f, 0) < 3
    ]
    next_action = (
        "capture evidence for missing decision factors"
        if known_count < len(_DEFENSIBILITY_FACTORS)
        else "maintain evidence and move to qualification"
    )

    return BuyabilityAssessment(
        account_id=account_id,
        buyability_score=round(score, 2),
        top_decision_risk=top_risk,
        top_hidden_buyer_gap=hidden_gap,
        proof_needed=proof_needed,
        content_needed=content_needed,
        next_alignment_action=next_action,
        factor_scores=factor_scores,
        assumptions=assumptions,
    )
