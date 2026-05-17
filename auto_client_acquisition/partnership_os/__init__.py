"""V12 Partnership OS — partner profile + fit score + motion + referral log.

Pure-local. NO fake partner names. NO white-label promise before the
3-paid-pilots threshold. NO revenue-share automation in V12.

Full Ops 2.0 adds the explicit partner/affiliate lifecycle, a
forbidden-claims guard and advisory payout rules (see
``partner_lifecycle``).
"""
from auto_client_acquisition.partnership_os.fit_score import compute_fit_score
from auto_client_acquisition.partnership_os.partner_lifecycle import (
    CLAWBACK_WINDOW_DAYS,
    FORBIDDEN_CLAIMS,
    FTC_DISCLOSURE_TEXT_AR,
    FTC_DISCLOSURE_TEXT_EN,
    PAYOUT_RATES,
    TIER_LABELS,
    ClaimScanResult,
    PartnerStage,
    PartnerTier,
    PayoutDecision,
    StageTransition,
    can_advance,
    compute_payout,
    flag_forbidden_claims,
    next_stage,
)
from auto_client_acquisition.partnership_os.partner_motion import recommend_motion
from auto_client_acquisition.partnership_os.partner_profile import (
    Partner,
    PartnerType,
)
from auto_client_acquisition.partnership_os.referral_tracker import (
    Referral,
    add_referral,
    list_referrals,
    reset_referrals,
)

__all__ = [
    "CLAWBACK_WINDOW_DAYS",
    "FORBIDDEN_CLAIMS",
    "FTC_DISCLOSURE_TEXT_AR",
    "FTC_DISCLOSURE_TEXT_EN",
    "PAYOUT_RATES",
    "TIER_LABELS",
    "ClaimScanResult",
    "Partner",
    "PartnerStage",
    "PartnerTier",
    "PartnerType",
    "PayoutDecision",
    "Referral",
    "StageTransition",
    "add_referral",
    "can_advance",
    "compute_fit_score",
    "compute_payout",
    "flag_forbidden_claims",
    "list_referrals",
    "next_stage",
    "recommend_motion",
    "reset_referrals",
]
