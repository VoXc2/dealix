"""V12 Partnership OS — partner profile + fit score + motion + referral log.

Pure-local. NO fake partner names. NO white-label promise before the
3-paid-pilots threshold. NO revenue-share automation in V12.

Affiliate & Partner machine (migration 013) adds the commission ladder,
partner scoring, commission engine, compliance guard and approved
messaging library.
"""
from auto_client_acquisition.partnership_os.approved_assets import (
    disclosure_text,
    get_disclosure,
    list_assets,
)
from auto_client_acquisition.partnership_os.commission_engine import (
    CLAWBACK_WINDOW_DAYS,
    CommissionLine,
    CommissionRefused,
    calculate,
    clawback,
)
from auto_client_acquisition.partnership_os.compliance_guard import (
    ComplianceScan,
    ComplianceViolation,
    scan_partner_content,
    scan_recruitment_request,
)
from auto_client_acquisition.partnership_os.fit_score import compute_fit_score
from auto_client_acquisition.partnership_os.partner_motion import recommend_motion
from auto_client_acquisition.partnership_os.partner_profile import (
    Partner,
    PartnerType,
)
from auto_client_acquisition.partnership_os.partner_scoring import (
    PartnerScore,
    score_partner,
)
from auto_client_acquisition.partnership_os.referral_tracker import (
    Referral,
    add_referral,
    list_referrals,
    reset_referrals,
)
from auto_client_acquisition.partnership_os.tiers import (
    Tier,
    get_tier,
    ladder,
    ladder_summary,
    rate_for,
)

__all__ = [
    "CLAWBACK_WINDOW_DAYS",
    "CommissionLine",
    "CommissionRefused",
    "ComplianceScan",
    "ComplianceViolation",
    "Partner",
    "PartnerScore",
    "PartnerType",
    "Referral",
    "Tier",
    "add_referral",
    "calculate",
    "clawback",
    "compute_fit_score",
    "disclosure_text",
    "get_disclosure",
    "get_tier",
    "ladder",
    "ladder_summary",
    "list_assets",
    "list_referrals",
    "rate_for",
    "recommend_motion",
    "reset_referrals",
    "scan_partner_content",
    "scan_recruitment_request",
    "score_partner",
]
