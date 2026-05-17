"""Partner/Affiliate lifecycle — Full Ops 2.0.

Models the partner journey as explicit stages and tiers, plus a
FORBIDDEN-CLAIMS guard for partner-submitted marketing copy.

Pure-function core. NO LLM. NO external send. Every payout decision
here is advisory — actual credit issuance is gated by
`referral_store.issue_credit` / `clawback_credit` which enforce the
`invoice_paid` precondition independently.

Doctrine constraints honored here:
  - NO payout before `invoice_paid` (payout eligibility is computed,
    never executed).
  - NO external send (forbidden-claims guard only flags copy).
  - Every claim needs a source (the disclosure constant requires
    partners to point to documented proof).
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum, StrEnum


class PartnerStage(StrEnum):
    """The explicit partner lifecycle stages, in order."""

    APPLY = "apply"
    SCORE = "score"
    APPROVE = "approve"
    TRAIN = "train"
    TRACK = "track"
    REVIEW = "review"
    PAY = "pay"


# Ordered stage progression — index used for forward-only transitions.
_STAGE_ORDER: tuple[PartnerStage, ...] = (
    PartnerStage.APPLY,
    PartnerStage.SCORE,
    PartnerStage.APPROVE,
    PartnerStage.TRAIN,
    PartnerStage.TRACK,
    PartnerStage.REVIEW,
    PartnerStage.PAY,
)


class PartnerTier(IntEnum):
    """Partner tiers 0-4."""

    APPLICANT = 0
    APPROVED_AFFILIATE = 1
    QUALIFIED_REFERRAL_PARTNER = 2
    STRATEGIC_PARTNER = 3
    IMPLEMENTATION_PARTNER = 4


TIER_LABELS: dict[int, dict[str, str]] = {
    0: {"en": "Applicant", "ar": "متقدّم"},
    1: {"en": "Approved Affiliate", "ar": "مسوّق معتمد"},
    2: {"en": "Qualified Referral Partner", "ar": "شريك إحالة مؤهَّل"},
    3: {"en": "Strategic Partner", "ar": "شريك استراتيجي"},
    4: {"en": "Implementation Partner", "ar": "شريك تنفيذ"},
}


# ── Forbidden claims + disclosure ─────────────────────────────────
# Partners must NOT publish these. They overstate the product, imply
# guarantees, or describe behaviour the platform deliberately refuses.
FORBIDDEN_CLAIMS: tuple[str, ...] = (
    "dealix guarantees revenue",
    "guarantees revenue",
    "guarantees compliance",
    "guaranteed results",
    "replaces your sales team",
    "replace your sales team",
    "sends ai messages automatically",
    "sends messages automatically",
    "auto-sends messages",
    "can use your data without approval",
    "uses your data without approval",
    "no human needed",
)

# FTC-style disclosure partners must attach to any promotional content.
FTC_DISCLOSURE_TEXT_EN: str = (
    "Disclosure: I am a Dealix partner and may earn a commission if you "
    "purchase through my referral. Dealix does not guarantee revenue or "
    "compliance outcomes; results depend on your own data and process. "
    "All claims must reference documented Dealix proof."
)
FTC_DISCLOSURE_TEXT_AR: str = (
    "إفصاح: أنا شريك لدى Dealix وقد أحصل على عمولة عند الشراء عبر إحالتي. "
    "لا تضمن Dealix أي إيراد أو نتيجة امتثال؛ النتائج تعتمد على بياناتكم "
    "وعملياتكم. كل ادعاء يجب أن يستند إلى إثبات موثّق من Dealix."
)


@dataclass
class ClaimScanResult:
    """Outcome of scanning partner-submitted copy for forbidden claims."""

    is_clean: bool
    flagged_claims: list[str]
    requires_review: bool
    reason_en: str
    reason_ar: str


def flag_forbidden_claims(copy: str) -> ClaimScanResult:
    """Scan partner-submitted marketing copy for forbidden claims.

    Pure function. Case-insensitive substring match. Does NOT block a
    send (it never sends) — it flags copy that must be rejected or
    rewritten before any human approves external use.
    """
    text = (copy or "").lower()
    flagged = sorted({c for c in FORBIDDEN_CLAIMS if c in text})
    if flagged:
        return ClaimScanResult(
            is_clean=False,
            flagged_claims=flagged,
            requires_review=True,
            reason_en=(
                "Copy contains forbidden claims and cannot be published. "
                "Rewrite to remove overstated/guarantee language."
            ),
            reason_ar=(
                "النص يحتوي ادعاءات ممنوعة ولا يمكن نشره. "
                "أعد الصياغة لإزالة عبارات الضمان أو المبالغة."
            ),
        )
    return ClaimScanResult(
        is_clean=True,
        flagged_claims=[],
        requires_review=False,
        reason_en="No forbidden claims detected.",
        reason_ar="لا توجد ادعاءات ممنوعة.",
    )


@dataclass
class StageTransition:
    """Result of evaluating a partner stage transition."""

    allowed: bool
    from_stage: PartnerStage
    to_stage: PartnerStage
    reason_en: str
    reason_ar: str


def next_stage(stage: PartnerStage) -> PartnerStage | None:
    """Return the next stage in the lifecycle, or None at the end."""
    idx = _STAGE_ORDER.index(stage)
    if idx + 1 >= len(_STAGE_ORDER):
        return None
    return _STAGE_ORDER[idx + 1]


def can_advance(
    *,
    from_stage: PartnerStage,
    to_stage: PartnerStage,
    fit_score: int = 0,
    trained: bool = False,
    has_clean_compliance: bool = True,
) -> StageTransition:
    """Decide whether a partner may move between lifecycle stages.

    Forward-only. Key gates:
      - SCORE -> APPROVE requires fit_score >= 40.
      - APPROVE -> TRAIN requires fit_score >= 40 and clean compliance.
      - TRAIN -> TRACK requires `trained` to be True.
      - any -> PAY requires clean compliance.
    """
    src = _STAGE_ORDER.index(from_stage)
    dst = _STAGE_ORDER.index(to_stage)
    if dst != src + 1:
        return StageTransition(
            allowed=False,
            from_stage=from_stage,
            to_stage=to_stage,
            reason_en="Only forward, single-step stage transitions are allowed.",
            reason_ar="يُسمح فقط بالانتقال خطوة واحدة للأمام بين المراحل.",
        )
    if to_stage == PartnerStage.APPROVE and fit_score < 40:
        return StageTransition(
            allowed=False,
            from_stage=from_stage,
            to_stage=to_stage,
            reason_en="Fit score below 40 — partner cannot be approved.",
            reason_ar="درجة المطابقة أقل من 40 — لا يمكن اعتماد الشريك.",
        )
    if to_stage == PartnerStage.TRAIN and (
        fit_score < 40 or not has_clean_compliance
    ):
        return StageTransition(
            allowed=False,
            from_stage=from_stage,
            to_stage=to_stage,
            reason_en="Training requires an approved, compliant partner.",
            reason_ar="التدريب يتطلّب شريكاً معتمداً وملتزماً.",
        )
    if to_stage == PartnerStage.TRACK and not trained:
        return StageTransition(
            allowed=False,
            from_stage=from_stage,
            to_stage=to_stage,
            reason_en="Partner must complete training before tracking referrals.",
            reason_ar="يجب إكمال التدريب قبل تتبّع الإحالات.",
        )
    if to_stage == PartnerStage.PAY and not has_clean_compliance:
        return StageTransition(
            allowed=False,
            from_stage=from_stage,
            to_stage=to_stage,
            reason_en="Compliance violation flag blocks payout stage.",
            reason_ar="علامة مخالفة الامتثال تمنع مرحلة الدفع.",
        )
    return StageTransition(
        allowed=True,
        from_stage=from_stage,
        to_stage=to_stage,
        reason_en="Transition allowed.",
        reason_ar="الانتقال مسموح.",
    )


# ── Payout rules ──────────────────────────────────────────────────
# Commission percentage by referral motion. Strategic-partner deals
# carry a band (15-20%); the conservative floor is used unless a
# founder-approved higher rate is supplied.
PAYOUT_RATES: dict[str, dict[str, float]] = {
    # affiliate lead -> paid diagnostic
    "affiliate_lead": {"min_pct": 5.0, "max_pct": 5.0},
    # warm qualified intro -> paid diagnostic
    "warm_qualified_intro": {"min_pct": 10.0, "max_pct": 10.0},
    # strategic partner deal
    "strategic_partner_deal": {"min_pct": 15.0, "max_pct": 20.0},
}

# Refund window during which a paid commission can be clawed back.
CLAWBACK_WINDOW_DAYS: int = 30


@dataclass
class PayoutDecision:
    """Advisory payout decision. Never executes a payout."""

    eligible: bool
    motion: str
    commission_pct: float
    commission_sar: int
    reason_en: str
    reason_ar: str


def compute_payout(
    *,
    motion: str,
    deal_amount_sar: int,
    invoice_paid: bool,
    is_duplicate: bool = False,
    is_self_referral: bool = False,
    compliance_violation: bool = False,
    approved_pct: float | None = None,
) -> PayoutDecision:
    """Compute an advisory partner commission for a referred deal.

    DOCTRINE — hard gates (any one blocks the payout):
      - `invoice_paid` must be True (no payout before invoice paid).
      - duplicate referral blocked.
      - self-referral blocked.
      - compliance violation flag blocked.

    `approved_pct`, when supplied, must fall within the motion's band;
    otherwise the conservative `min_pct` floor is used.
    """
    rate = PAYOUT_RATES.get(motion)
    if rate is None:
        return PayoutDecision(
            eligible=False,
            motion=motion,
            commission_pct=0.0,
            commission_sar=0,
            reason_en=f"Unknown payout motion '{motion}'.",
            reason_ar=f"حركة دفع غير معروفة '{motion}'.",
        )

    if not invoice_paid:
        return PayoutDecision(
            eligible=False,
            motion=motion,
            commission_pct=0.0,
            commission_sar=0,
            reason_en="No payout before invoice_paid.",
            reason_ar="لا دفع قبل سداد الفاتورة.",
        )
    if is_self_referral:
        return PayoutDecision(
            eligible=False,
            motion=motion,
            commission_pct=0.0,
            commission_sar=0,
            reason_en="Self-referral — payout blocked.",
            reason_ar="إحالة ذاتية — الدفع محظور.",
        )
    if is_duplicate:
        return PayoutDecision(
            eligible=False,
            motion=motion,
            commission_pct=0.0,
            commission_sar=0,
            reason_en="Duplicate referral — payout blocked.",
            reason_ar="إحالة مكرّرة — الدفع محظور.",
        )
    if compliance_violation:
        return PayoutDecision(
            eligible=False,
            motion=motion,
            commission_pct=0.0,
            commission_sar=0,
            reason_en="Compliance violation flag — payout blocked.",
            reason_ar="علامة مخالفة امتثال — الدفع محظور.",
        )

    pct = rate["min_pct"]
    if approved_pct is not None and rate["min_pct"] <= approved_pct <= rate["max_pct"]:
        pct = approved_pct
    commission = int(round(max(0, deal_amount_sar) * pct / 100.0))
    return PayoutDecision(
        eligible=True,
        motion=motion,
        commission_pct=pct,
        commission_sar=commission,
        reason_en="Payout eligible — pending founder approval.",
        reason_ar="مؤهَّل للدفع — بانتظار موافقة المؤسس.",
    )


__all__ = [
    "CLAWBACK_WINDOW_DAYS",
    "FORBIDDEN_CLAIMS",
    "FTC_DISCLOSURE_TEXT_AR",
    "FTC_DISCLOSURE_TEXT_EN",
    "PAYOUT_RATES",
    "TIER_LABELS",
    "ClaimScanResult",
    "PartnerStage",
    "PartnerTier",
    "PayoutDecision",
    "StageTransition",
    "can_advance",
    "compute_payout",
    "flag_forbidden_claims",
    "next_stage",
]
