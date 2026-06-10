"""Dealix compliance modules — VAT, regulatory, and governance."""

from dealix.compliance.vat_engine import (
    VATResult,
    VATEngine,
    Invoice,
    InvoiceLine,
)

__all__ = [
    "Invoice",
    "InvoiceLine",
    "VATResult",
    "VATEngine",
]
