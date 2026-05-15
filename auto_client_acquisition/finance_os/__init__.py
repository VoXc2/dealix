"""Finance OS v5 — pricing catalog + invoice-draft helper + guardrails.

Wraps existing infra:
  - ``dealix/payments/moyasar.py`` (no live charge added here)
  - ``scripts/dealix_invoice.py`` admin CLI (no replacement; this is
    just a programmatic invoice-draft DTO so other modules can build
    a draft without shelling out)

Hard rules:
  - ``MOYASAR_ALLOW_LIVE_CHARGE`` does NOT exist and is NOT added.
  - All ``draft_invoice()`` results carry ``approval_status=approval_required``.
  - Pricing-catalog 499 SAR Pilot stays the first-payment offer until
    Decision Pack S1 is signed (after customer #5).
"""
from auto_client_acquisition.finance_os.guardrails import (
    finance_guardrails,
    is_live_charge_allowed,
)
from auto_client_acquisition.finance_os.invoice_draft import (
    InvoiceDraft,
    draft_invoice,
)
from auto_client_acquisition.finance_os.pricing_catalog import (
    PricingTier,
    get_pricing_tier,
    pricing_catalog,
)

__all__ = [
    "InvoiceDraft",
    "PricingTier",
    "draft_invoice",
    "finance_guardrails",
    "get_pricing_tier",
    "is_live_charge_allowed",
    "pricing_catalog",
]
