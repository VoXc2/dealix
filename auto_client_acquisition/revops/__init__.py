"""V12.5 Beast — RevOps full layer.

Extends RX revenue_pipeline with:
  - InvoiceState (draft/sent/paid/refunded/voided lifecycle)
  - PaymentConfirmation (manual evidence record)
  - Margin (delivery cost + support cost → gross margin estimate)
  - FinanceBrief (single-call founder-facing finance snapshot)

Pure-local. No external API. No DB. Reuses
``revenue_pipeline.RevenuePipeline`` as the source of truth for
which leads are paid vs committed.
"""
from auto_client_acquisition.revops.finance_brief import (
    FinanceBrief,
    build_finance_brief,
)
from auto_client_acquisition.revops.invoice_state import (
    InvoiceState,
    InvoiceStatus,
    create_invoice_draft,
    transition_invoice,
)
from auto_client_acquisition.revops.margin import (
    MarginSnapshot,
    compute_margin,
)
from auto_client_acquisition.revops.payment_confirmation import (
    PaymentConfirmation,
    PaymentMethod,
    record_payment_confirmation,
)

__all__ = [
    "FinanceBrief",
    "InvoiceState",
    "InvoiceStatus",
    "MarginSnapshot",
    "PaymentConfirmation",
    "PaymentMethod",
    "build_finance_brief",
    "compute_margin",
    "create_invoice_draft",
    "record_payment_confirmation",
    "transition_invoice",
]
