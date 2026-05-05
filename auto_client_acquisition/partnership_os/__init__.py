"""V12 Partnership OS — partner profile + fit score + motion + referral log.

Pure-local. NO fake partner names. NO white-label promise before the
3-paid-pilots threshold. NO revenue-share automation in V12.
"""
from auto_client_acquisition.partnership_os.fit_score import compute_fit_score
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
    "Partner",
    "PartnerType",
    "Referral",
    "add_referral",
    "compute_fit_score",
    "list_referrals",
    "recommend_motion",
    "reset_referrals",
]
