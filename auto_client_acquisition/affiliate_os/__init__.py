"""Affiliate OS — Dealix Full Ops Affiliate Network.

Tiered affiliate commission engine (Tier 1–4), eligibility gate
(payout only after invoice_paid), refund clawback, affiliate-message
compliance, and partner-application scoring.

Non-negotiables enforced:
  - commission is a DRAFT number until a founder ApprovalRequest is
    approved (Article 8 — no external action without approval);
  - no payout before the deal invoice reaches ``paid``;
  - refund inside the clawback window reverses the commission;
  - every affiliate message must carry a referral disclosure;
  - no cold WhatsApp / no guaranteed outcomes in affiliate copy.
"""
from auto_client_acquisition.affiliate_os.affiliate_compliance import (
    DISCLOSURE_AR,
    DISCLOSURE_EN,
    ComplianceResult,
    check_affiliate_message,
)
from auto_client_acquisition.affiliate_os.clawback import (
    CLAWBACK_WINDOW_DAYS,
    apply_clawback,
    should_clawback,
)
from auto_client_acquisition.affiliate_os.commission import (
    Commission,
    CommissionStatus,
    compute_commission,
)
from auto_client_acquisition.affiliate_os.eligibility import (
    DISALLOWED_LEAD_FLAGS,
    commission_eligible,
    is_disqualifying,
)
from auto_client_acquisition.affiliate_os.partner_application import (
    ApplicationScore,
    PartnerApplication,
    score_application,
)
from auto_client_acquisition.affiliate_os.tiers import (
    AffiliateTier,
    commission_rate,
    is_handoff_tier,
    tier_table,
)

__all__ = [
    "CLAWBACK_WINDOW_DAYS",
    "DISALLOWED_LEAD_FLAGS",
    "DISCLOSURE_AR",
    "DISCLOSURE_EN",
    "AffiliateTier",
    "ApplicationScore",
    "Commission",
    "CommissionStatus",
    "ComplianceResult",
    "PartnerApplication",
    "apply_clawback",
    "check_affiliate_message",
    "commission_eligible",
    "commission_rate",
    "compute_commission",
    "is_disqualifying",
    "is_handoff_tier",
    "score_application",
    "should_clawback",
    "tier_table",
]
