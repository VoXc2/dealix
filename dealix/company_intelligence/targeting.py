"""Evidence-first targeting intelligence for the canonical Opportunity Graph.

This module is intentionally persistence-neutral. It does not create a CRM,
vector database, scheduler, agent, or external-send authority. It transforms
source-attributed evidence into two separate outputs:

1. Target Value: how economically attractive the account/problem is.
2. Actionability: whether a specific channel action is presently eligible.

Truth firewall:
    research != relationship
    public contact != consent
    draft != sent
    quote != invoice != payment
    high target value != send authority
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from enum import StrEnum
from hashlib import sha256
from typing import Iterable, Sequence
from urllib.parse import urlparse
import re
import unicodedata


class EvidenceTier(StrEnum):
    DIRECT_INTERACTION = "A_direct_interaction"
    FIRST_PARTY_OFFICIAL = "B_first_party_official"
    LICENSED_ENRICHMENT = "C_licensed_enrichment"
    OPEN_WEB_ARCHIVE = "D_open_web_archive"
    SOCIAL_CHATTER = "E_social_chatter"


class RelationshipState(StrEnum):
    UNKNOWN = "unknown"
    RESEARCH_ONLY = "research_only"
    KNOWN = "known"
    WARM = "warm"
    INBOUND = "inbound"
    ACTIVE_CONVERSATION = "active_conversation"


class ConsentState(StrEnum):
    UNKNOWN = "unknown"
    NOT_REQUIRED_FOR_INTERNAL_RESEARCH = "not_required_for_internal_research"
    OPTED_IN = "opted_in"
    OPTED_OUT = "opted_out"
    SUPPRESSED = "suppressed"


class ChannelEligibility(StrEnum):
    BLOCKED = "blocked"
    DRAFT_ONLY = "draft_only"
    INBOUND_ONLY = "inbound_only"
    TEMPLATE_ELIGIBLE = "template_eligible"
    CALLBACK_REQUESTED = "callback_requested"
    ELIGIBLE = "eligible"


class SignalFamily(StrEnum):
    EXECUTION_FRAGMENTATION = "execution_fragmentation"
    REVENUE_LEAKAGE = "revenue_leakage"
    GOVERNANCE_PROOF_PRESSURE = "governance_proof_pressure"
    GROWTH_TRANSITION = "growth_transition"
    PROCUREMENT_B2G = "procurement_b2g"
    TECHNOLOGY_TRANSITION = "technology_transition"
    CUSTOMER_EXPERIENCE_PRESSURE = "customer_experience_pressure"
    PARTNER_FIT = "partner_fit"


class PriorityBand(StrEnum):
    P0 = "P0"
    P1 = "P1"
    P2 = "P2"
    DEFER = "DEFER"


@dataclass(frozen=True)
class EvidenceItem:
    source_id: str
    source_url: str
    tier: EvidenceTier
    observed_at: datetime
    claim: str
    confidence: float
    expires_at: datetime | None = None

    def __post_init__(self) -> None:
        if not self.source_id.strip():
            raise ValueError("source_id is required")
        if not self.claim.strip():
            raise ValueError("claim is required")
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be in [0,1]")

    @property
    def stale(self) -> bool:
        return bool(self.expires_at and datetime.now(UTC) > self.expires_at)


@dataclass(frozen=True)
class TargetValueFeatures:
    icp_saudi_fit: float
    problem_evidence: float
    why_now_trigger: float
    offer_fit: float
    buyer_or_partner_route: float
    proofability: float
    expected_economic_value: float
    evidence_confidence: float
    semantic_fit: float | None = None

    def __post_init__(self) -> None:
        values = (
            self.icp_saudi_fit,
            self.problem_evidence,
            self.why_now_trigger,
            self.offer_fit,
            self.buyer_or_partner_route,
            self.proofability,
            self.expected_economic_value,
            self.evidence_confidence,
        )
        if any(not 0.0 <= value <= 1.0 for value in values):
            raise ValueError("target value features must be in [0,1]")
        if self.semantic_fit is not None and not 0.0 <= self.semantic_fit <= 1.0:
            raise ValueError("semantic_fit must be in [0,1]")


@dataclass(frozen=True)
class Actionability:
    relationship: RelationshipState = RelationshipState.UNKNOWN
    consent: ConsentState = ConsentState.UNKNOWN
    email: ChannelEligibility = ChannelEligibility.BLOCKED
    whatsapp: ChannelEligibility = ChannelEligibility.INBOUND_ONLY
    voice: ChannelEligibility = ChannelEligibility.INBOUND_ONLY
    suppressed: bool = False

    def can_execute_live(self, channel: str) -> bool:
        """Return eligibility only; this is never approval/authority itself."""
        if self.suppressed or self.consent in {ConsentState.OPTED_OUT, ConsentState.SUPPRESSED}:
            return False
        state = {
            "email": self.email,
            "whatsapp": self.whatsapp,
            "voice": self.voice,
        }.get(channel)
        return state == ChannelEligibility.ELIGIBLE


@dataclass(frozen=True)
class TargetDossier:
    company_id: str
    company_name: str
    canonical_domain: str
    signal_family: SignalFamily
    why_them: str
    why_now: str
    problem_hypothesis: str
    business_cost_hypothesis: str
    offer_route: str
    proof_baseline: str
    evidence: tuple[EvidenceItem, ...]
    features: TargetValueFeatures
    actionability: Actionability
    active_thread_or_opportunity: bool = False

    @property
    def dossier_id(self) -> str:
        material = "|".join(
            [self.company_id, self.canonical_domain, self.signal_family.value]
        )
        return f"target_{sha256(material.encode('utf-8')).hexdigest()[:16]}"


@dataclass(frozen=True)
class TargetScore:
    total: float
    priority_band: PriorityBand
    raw_components: dict[str, float]
    stale_evidence_count: int
    eligible_for_draft: bool
    hold_reasons: tuple[str, ...]


_WEIGHTS: dict[str, float] = {
    "icp_saudi_fit": 15.0,
    "problem_evidence": 20.0,
    "why_now_trigger": 20.0,
    "offer_fit": 10.0,
    "buyer_or_partner_route": 10.0,
    "proofability": 10.0,
    "expected_economic_value": 10.0,
    "evidence_confidence": 5.0,
}


def priority_band(score: float) -> PriorityBand:
    if score >= 85.0:
        return PriorityBand.P0
    if score >= 70.0:
        return PriorityBand.P1
    if score >= 55.0:
        return PriorityBand.P2
    return PriorityBand.DEFER


def score_target(dossier: TargetDossier) -> TargetScore:
    """Score target value while keeping actionability separate.

    semantic_fit can refine the ICP feature by at most 10% of that feature's
    contribution. It is deliberately unable to dominate explicit evidence.
    """
    features = dossier.features
    components = {
        key: getattr(features, key) * weight
        for key, weight in _WEIGHTS.items()
    }

    if features.semantic_fit is not None:
        # Small bounded refinement of the ICP component; no new weighting owner.
        base = components["icp_saudi_fit"]
        components["icp_saudi_fit"] = min(
            _WEIGHTS["icp_saudi_fit"],
            base * 0.90 + features.semantic_fit * _WEIGHTS["icp_saudi_fit"] * 0.10,
        )

    total = round(sum(components.values()), 2)
    stale_count = sum(1 for item in dossier.evidence if item.stale)
    holds = list(pre_draft_hold_reasons(dossier))
    return TargetScore(
        total=total,
        priority_band=priority_band(total),
        raw_components={key: round(value, 2) for key, value in components.items()},
        stale_evidence_count=stale_count,
        eligible_for_draft=not holds,
        hold_reasons=tuple(holds),
    )


def pre_draft_hold_reasons(dossier: TargetDossier) -> tuple[str, ...]:
    """Enforce the canonical evidence-first pre-draft gate."""
    holds: list[str] = []
    required_text = {
        "why_them": dossier.why_them,
        "why_now": dossier.why_now,
        "problem_hypothesis": dossier.problem_hypothesis,
        "business_cost_hypothesis": dossier.business_cost_hypothesis,
        "offer_route": dossier.offer_route,
        "proof_baseline": dossier.proof_baseline,
    }
    for field_name, value in required_text.items():
        if not value.strip():
            holds.append(f"missing_{field_name}")

    if not dossier.company_id.strip():
        holds.append("unresolved_company")
    if not dossier.canonical_domain.strip():
        holds.append("missing_canonical_domain")
    if not dossier.evidence:
        holds.append("missing_evidence")
    elif not any(not item.stale and item.confidence >= 0.5 for item in dossier.evidence):
        holds.append("no_fresh_credible_evidence")

    if dossier.active_thread_or_opportunity:
        holds.append("duplicate_active_thread_or_opportunity")
    if dossier.actionability.suppressed:
        holds.append("suppressed")
    if dossier.actionability.consent in {ConsentState.OPTED_OUT, ConsentState.SUPPRESSED}:
        holds.append("opted_out_or_suppressed")

    return tuple(sorted(set(holds)))


def normalize_domain(value: str) -> str:
    """Normalize a company website/domain into a deterministic lookup key."""
    raw = value.strip().lower()
    if not raw:
        return ""
    if "://" not in raw:
        raw = "https://" + raw
    parsed = urlparse(raw)
    host = (parsed.hostname or "").lower().rstrip(".")
    if host.startswith("www."):
        host = host[4:]
    return host


def normalize_company_name(value: str) -> str:
    """Normalize Arabic/English company names without erasing semantic text."""
    text = unicodedata.normalize("NFKC", value).casefold().strip()
    text = re.sub(r"[\W_]+", " ", text, flags=re.UNICODE)
    tokens = [token for token in text.split() if token]
    common_suffixes = {
        "llc", "ltd", "limited", "company", "co", "inc", "corp",
        "شركة", "مؤسسة", "ذ", "م", "محدودة",
    }
    while tokens and tokens[-1] in common_suffixes:
        tokens.pop()
    return " ".join(tokens)


def deterministic_entity_key(*, domain: str, legal_name: str) -> str:
    normalized_domain = normalize_domain(domain)
    normalized_name = normalize_company_name(legal_name)
    if normalized_domain:
        return f"domain:{normalized_domain}"
    if normalized_name:
        return f"name:{normalized_name}"
    raise ValueError("domain or legal_name is required")


def fuzzy_name_similarity(left: str, right: str) -> float:
    """Return 0..1 similarity, using RapidFuzz when present with safe fallback."""
    a = normalize_company_name(left)
    b = normalize_company_name(right)
    if not a or not b:
        return 0.0
    try:
        from rapidfuzz.fuzz import ratio  # type: ignore
    except ImportError:
        from difflib import SequenceMatcher
        return SequenceMatcher(None, a, b).ratio()
    return ratio(a, b) / 100.0


def possible_duplicate(
    *,
    left_domain: str,
    left_name: str,
    right_domain: str,
    right_name: str,
    fuzzy_threshold: float = 0.92,
) -> bool:
    """Conservative duplicate candidate detector.

    Exact canonical domain match is strong evidence. Fuzzy name similarity only
    raises a candidate; callers must hold ambiguous merges for review.
    """
    left_host = normalize_domain(left_domain)
    right_host = normalize_domain(right_domain)
    if left_host and right_host and left_host == right_host:
        return True
    return fuzzy_name_similarity(left_name, right_name) >= fuzzy_threshold


@dataclass(frozen=True)
class CommercialOutcome:
    dossier_id: str
    real_interaction: bool = False
    qualified_problem: bool = False
    quote_created: bool = False
    payment_verified: bool = False
    outcome_delivered: bool = False
    proof_validated: bool = False
    founder_minutes: float = 0.0
    cost_sar: float = 0.0

    def __post_init__(self) -> None:
        if self.founder_minutes < 0 or self.cost_sar < 0:
            raise ValueError("founder_minutes and cost_sar must be non-negative")
        # Economic truth is sequential: later claims require earlier evidence.
        chain = [
            self.real_interaction,
            self.qualified_problem,
            self.quote_created,
            self.payment_verified,
            self.outcome_delivered,
            self.proof_validated,
        ]
        seen_false = False
        for value in chain:
            if not value:
                seen_false = True
            elif seen_false:
                raise ValueError("commercial outcome stages cannot skip evidence")


def rank_dossiers(dossiers: Iterable[TargetDossier]) -> list[tuple[TargetDossier, TargetScore]]:
    scored = [(dossier, score_target(dossier)) for dossier in dossiers]
    return sorted(
        scored,
        key=lambda item: (
            item[1].eligible_for_draft,
            item[1].total,
            -item[1].stale_evidence_count,
        ),
        reverse=True,
    )


def evidence_expiry(*, observed_at: datetime, tier: EvidenceTier) -> datetime:
    """Default recency policy; callers may provide stricter source-specific TTLs."""
    days = {
        EvidenceTier.DIRECT_INTERACTION: 90,
        EvidenceTier.FIRST_PARTY_OFFICIAL: 45,
        EvidenceTier.LICENSED_ENRICHMENT: 60,
        EvidenceTier.OPEN_WEB_ARCHIVE: 30,
        EvidenceTier.SOCIAL_CHATTER: 14,
    }[tier]
    return observed_at + timedelta(days=days)


def outcome_learning_row(
    *,
    dossier: TargetDossier,
    score: TargetScore,
    outcome: CommercialOutcome,
) -> dict[str, object]:
    """Canonical Proof/Learning attribution row; no vanity metrics."""
    if outcome.dossier_id != dossier.dossier_id:
        raise ValueError("outcome does not belong to dossier")
    return {
        "dossier_id": dossier.dossier_id,
        "company_id": dossier.company_id,
        "signal_family": dossier.signal_family.value,
        "target_value_score": score.total,
        "priority_band": score.priority_band.value,
        "relationship_state": dossier.actionability.relationship.value,
        "real_interaction": outcome.real_interaction,
        "qualified_problem": outcome.qualified_problem,
        "quote_created": outcome.quote_created,
        "payment_verified": outcome.payment_verified,
        "outcome_delivered": outcome.outcome_delivered,
        "proof_validated": outcome.proof_validated,
        "founder_minutes": outcome.founder_minutes,
        "cost_sar": outcome.cost_sar,
    }
