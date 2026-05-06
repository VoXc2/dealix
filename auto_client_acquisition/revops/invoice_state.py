"""Invoice state labels — draft vs commitment vs paid reference."""
from __future__ import annotations

from typing import Any, Literal

InvoiceState = Literal["draft", "pending_manual_send", "awaiting_payment", "paid_reference_logged"]


def describe_invoice_state(*, has_draft: bool, payment_reference_logged: bool) -> dict[str, Any]:
    """Map booleans to a single state for RevOps displays."""
    if payment_reference_logged:
        state: InvoiceState = "paid_reference_logged"
    elif has_draft:
        state = "awaiting_payment"
    else:
        state = "draft"

    return {
        "schema_version": 1,
        "state": state,
        "counts_as_revenue": payment_reference_logged,
        "notes_ar": (
            "مسودة الفاتورة ليست إيراداً حتى يُسجَّل الدفع بمرجع واضح."
        ),
        "notes_en": "A draft invoice is not revenue until payment is logged with evidence.",
    }
