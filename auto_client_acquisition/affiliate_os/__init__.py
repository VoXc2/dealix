"""Affiliate OS — governed affiliate program.

Doctrine (enforced by tests, not just docs):

* No affiliate copy may promise guaranteed outcomes — every asset clears the
  governance_os claim guards before approval.
* A commission accrues ONLY against an invoice with payment-confirmation
  evidence. No paid invoice, no commission.
* A payout is released ONLY after a human approves it via the Approval Center.

Persistence is JSONL + in-memory (no PII; placeholder identifiers only),
mirroring partnership_os. The public surface stays stable when a Postgres
backend lands later.
"""

from auto_client_acquisition.affiliate_os.affiliate_profile import (
    Affiliate,
    AffiliateApplication,
    AffiliateType,
)
from auto_client_acquisition.affiliate_os.affiliate_store import (
    AFFILIATE_OPS_TENANT,
    get_affiliate,
    list_affiliates,
    set_status,
    submit_application,
)
from auto_client_acquisition.affiliate_os.asset_registry import (
    ApprovedAsset,
    AssetReviewResult,
    AssetSubmission,
    list_approved_assets,
    review_asset_copy,
)
from auto_client_acquisition.affiliate_os.commission_engine import (
    Commission,
    calculate_commission,
    get_commission,
    list_commissions,
)
from auto_client_acquisition.affiliate_os.fit_score import compute_affiliate_fit_score
from auto_client_acquisition.affiliate_os.payout_gate import (
    PayoutRecord,
    approve_payout,
    finalize_payout,
    list_payouts,
    request_payout,
)
from auto_client_acquisition.affiliate_os.referral_links import (
    AffiliateLink,
    build_tracking_url,
    create_affiliate_link,
    list_links,
    lookup_link,
)

__all__ = [
    "AFFILIATE_OPS_TENANT",
    "Affiliate",
    "AffiliateApplication",
    "AffiliateLink",
    "AffiliateType",
    "ApprovedAsset",
    "AssetReviewResult",
    "AssetSubmission",
    "Commission",
    "PayoutRecord",
    "approve_payout",
    "build_tracking_url",
    "calculate_commission",
    "compute_affiliate_fit_score",
    "create_affiliate_link",
    "finalize_payout",
    "get_affiliate",
    "get_commission",
    "list_affiliates",
    "list_approved_assets",
    "list_commissions",
    "list_links",
    "list_payouts",
    "lookup_link",
    "request_payout",
    "review_asset_copy",
    "set_status",
    "submit_application",
]
