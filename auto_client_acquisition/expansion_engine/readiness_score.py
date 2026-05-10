"""Wave 12.5 §33.2.5 — Expansion Readiness Score.

Numeric composite score (0.0 - 1.0) that drives the next-best-offer
decision. The formula combines:
- Proof signals: count + max evidence level + customer approvals
- Customer engagement: payment history + delivery success + support health
- Friction signals: support tickets + remaining pain (drag down)
- Budget fit: tier match score

Hard rule (Article 8): when source data is missing/zero, returns
score=0.0 + ready=False with explicit `blockers` list. Never invents
positive signals.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

from auto_client_acquisition.proof_engine.evidence import EvidenceLevel


@dataclass(frozen=True, slots=True)
class ExpansionReadinessScore:
    """Composite readiness for upsell recommendation."""

    score: float                # 0.0 - 1.0
    ready: bool                 # score >= 0.6 AND no critical blockers
    proof_signal_score: float   # 0.0 - 1.0
    engagement_score: float     # 0.0 - 1.0
    friction_score: float       # 0.0 - 1.0 (higher = MORE friction = bad)
    budget_fit_score: float     # 0.0 - 1.0
    is_estimate: bool           # always True (Article 8 — never claim certainty)
    blockers: tuple[str, ...] = field(default_factory=tuple)
    notes: tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True, slots=True)
class NextBestOffer:
    """Recommended next offer based on customer pain + readiness."""

    offer_key: Literal[
        "data_to_revenue_pack",
        "managed_growth_ops",
        "support_os",
        "executive_command_center",
        "agency_partner_os",
        "no_recommendation_yet",
    ]
    offer_name_ar: str
    offer_name_en: str
    rationale_ar: str
    rationale_en: str
    confidence: float           # 0.0 - 1.0
    action_mode: Literal[
        "suggest_only",         # too early — founder considers but doesn't act
        "draft_only",           # founder drafts message, doesn't send
        "approval_required",    # ready — founder approves before send
    ]
    is_estimate: bool = True


def compute_readiness_score(
    *,
    proof_event_count: int = 0,
    max_evidence_level: int = 0,
    customer_approved_proof_count: int = 0,
    public_proof_count: int = 0,
    payment_history_paid_count: int = 0,
    delivery_sessions_complete_count: int = 0,
    support_tickets_open: int = 0,
    support_tickets_critical: int = 0,
    days_since_last_engagement: int = 30,
    customer_health_bucket: str = "unknown",
    budget_tier_match_score: float = 0.5,
    remaining_pain_score: float = 0.5,
) -> ExpansionReadinessScore:
    """Compute the expansion readiness score from real signals.

    All inputs default to "no data" — caller passes what's available.
    Article 8: when most inputs are zero, score is low and `blockers`
    explains why.

    Args:
        proof_event_count: Total proof events recorded for this customer.
        max_evidence_level: Highest L0-L5 reached (int).
        customer_approved_proof_count: Subset where approval_status == approved.
        public_proof_count: Subset at L4+ with consent_public.
        payment_history_paid_count: Number of confirmed payments.
        delivery_sessions_complete_count: Completed service sessions.
        support_tickets_open: Currently-open tickets.
        support_tickets_critical: Subset with priority p0/p1.
        days_since_last_engagement: How recently they responded.
        customer_health_bucket: From Engine 8 (expansion_ready / healthy /
            stable / at_risk / critical / blocked / unknown).
        budget_tier_match_score: 0-1 — how well their budget fits next tier.
        remaining_pain_score: 0-1 — pain remaining after current service
            (HIGH = more pain = more upsell rationale; counterbalanced by
            friction).

    Returns:
        ExpansionReadinessScore with explicit blockers.
    """
    blockers: list[str] = []
    notes: list[str] = []

    # Proof signal — strongest gate (Article 8)
    if proof_event_count == 0:
        proof_signal_score = 0.0
        blockers.append("no_proof_events_recorded")
    else:
        # Weighted: customer-approved counts most, then evidence level
        approved_weight = min(1.0, customer_approved_proof_count / 3.0)  # 3+ = max
        level_weight = max_evidence_level / 5.0  # L5 = max
        count_weight = min(1.0, proof_event_count / 5.0)  # 5+ = max
        proof_signal_score = round(
            0.5 * approved_weight + 0.3 * level_weight + 0.2 * count_weight, 3,
        )
        if max_evidence_level < EvidenceLevel.L3_CUSTOMER_APPROVED:
            blockers.append(f"max_evidence_below_L3 (current=L{max_evidence_level})")
        if customer_approved_proof_count == 0:
            blockers.append("no_customer_approved_proof")

    # Engagement — payment + delivery + recency
    if payment_history_paid_count == 0:
        engagement_score = 0.0
        blockers.append("no_paid_history")
    else:
        pay_weight = min(1.0, payment_history_paid_count / 3.0)
        deliv_weight = min(1.0, delivery_sessions_complete_count / 2.0)
        recency_weight = max(0.0, 1.0 - (days_since_last_engagement / 60.0))  # decay over 60d
        engagement_score = round(
            0.4 * pay_weight + 0.3 * deliv_weight + 0.3 * recency_weight, 3,
        )
        if days_since_last_engagement > 30:
            notes.append(f"engagement_stale ({days_since_last_engagement}d since last)")

    # Friction — penalty applied to overall (higher = worse)
    if support_tickets_critical > 0:
        friction_score = min(1.0, 0.5 + 0.2 * support_tickets_critical)
        blockers.append(f"{support_tickets_critical}_critical_support_tickets_open")
    elif support_tickets_open > 5:
        friction_score = min(1.0, 0.3 + 0.05 * support_tickets_open)
        notes.append(f"{support_tickets_open}_support_tickets_open (non-critical)")
    else:
        friction_score = 0.1 + 0.05 * support_tickets_open

    # Customer health bucket — direct mapping
    health_bonus = {
        "expansion_ready": 0.2,
        "healthy": 0.1,
        "stable": 0.0,
        "at_risk": -0.2,
        "critical": -0.4,
        "blocked": -0.6,
        "unknown": -0.1,
    }.get(customer_health_bucket, -0.1)

    # Budget fit (clamp 0-1)
    budget_fit_score = max(0.0, min(1.0, budget_tier_match_score))

    # Composite formula:
    # 35% proof + 30% engagement + 25% budget_fit + 10% pain_residual
    # MINUS friction penalty (up to 0.4)
    # PLUS health bonus (-0.6 to +0.2)
    raw_score = (
        0.35 * proof_signal_score
        + 0.30 * engagement_score
        + 0.25 * budget_fit_score
        + 0.10 * remaining_pain_score
        - 0.4 * friction_score
        + health_bonus
    )
    final_score = max(0.0, min(1.0, raw_score))

    # Ready threshold: score >= 0.6 AND no critical blockers
    has_critical_blocker = any(
        b.startswith("no_proof_events") or
        b.startswith("no_paid_history") or
        b.startswith("no_customer_approved_proof") or
        "critical_support_tickets" in b
        for b in blockers
    )
    ready = final_score >= 0.6 and not has_critical_blocker

    return ExpansionReadinessScore(
        score=round(final_score, 3),
        ready=ready,
        proof_signal_score=proof_signal_score,
        engagement_score=engagement_score,
        friction_score=round(friction_score, 3),
        budget_fit_score=round(budget_fit_score, 3),
        is_estimate=True,
        blockers=tuple(blockers),
        notes=tuple(notes),
    )


def recommend_next_offer(
    *,
    readiness: ExpansionReadinessScore,
    primary_pain: Literal[
        "dormant_data", "follow_up_gap", "support_chaos",
        "executive_visibility", "agency_proof_gap", "unknown",
    ] = "unknown",
) -> NextBestOffer:
    """Map readiness + pain → concrete offer.

    Pain → Offer mapping (from plan §32.3.10):
        dormant_data        → Data-to-Revenue Pack
        follow_up_gap       → Managed Growth Ops
        support_chaos       → Support OS
        executive_visibility → Executive Command Center
        agency_proof_gap    → Agency Partner OS
        unknown             → no_recommendation_yet (founder must clarify)

    Action mode (Article 8):
        not ready (score < 0.6) → suggest_only (founder considers)
        ready but score < 0.8   → draft_only (founder drafts)
        ready + score >= 0.8    → approval_required (proceed)
    """
    # Pain → offer
    pain_to_offer = {
        "dormant_data": ("data_to_revenue_pack", "Data-to-Revenue Pack",
                         "تحويل البيانات الخاملة إلى فرص"),
        "follow_up_gap": ("managed_growth_ops", "Managed Growth Ops Monthly",
                          "متابعة منظَّمة للفرص"),
        "support_chaos": ("support_os", "Support OS",
                          "تنظيم الدعم وتحسين تجربة العميل"),
        "executive_visibility": ("executive_command_center",
                                 "Executive Command Center",
                                 "رؤية إدارة شاملة للنمو والمخاطر"),
        "agency_proof_gap": ("agency_partner_os", "Agency Partner OS",
                             "بناء proof للوكالات لزيادة الاحتفاظ"),
        "unknown": ("no_recommendation_yet", "No recommendation yet",
                    "تحتاج توضيح مصدر الألم قبل الاقتراح"),
    }
    offer_key, name_en, rationale_ar = pain_to_offer.get(
        primary_pain, pain_to_offer["unknown"],
    )

    # Readiness → action mode (Article 8 — gated)
    if not readiness.ready:
        action_mode: Literal["suggest_only", "draft_only", "approval_required"] = "suggest_only"
        rat_ar_suffix = "غير جاهز للتوصية الآن — راجع blockers."
        rat_en_suffix = "Not yet ready — review blockers."
    elif readiness.score < 0.8:
        action_mode = "draft_only"
        rat_ar_suffix = "جاهز ولكن أقل من ممتاز — جهّز مسوّدة وانتظر."
        rat_en_suffix = "Ready but below peak — draft and hold."
    else:
        action_mode = "approval_required"
        rat_ar_suffix = "جاهز جداً — اقترح بعد موافقة المؤسس."
        rat_en_suffix = "Strong readiness — propose after founder approval."

    # Confidence proportional to readiness score
    confidence = readiness.score

    return NextBestOffer(
        offer_key=offer_key,  # type: ignore[arg-type]
        offer_name_ar=name_en,  # English name is universal in product surface
        offer_name_en=name_en,
        rationale_ar=f"{rationale_ar} — {rat_ar_suffix}",
        rationale_en=f"score={readiness.score:.2f} · {rat_en_suffix}",
        confidence=confidence,
        action_mode=action_mode,
        is_estimate=True,
    )
