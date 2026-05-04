"""Invoice-draft DTO — programmatic interface that mirrors what
``scripts/dealix_invoice.py`` accepts on the CLI.

This module DOES NOT call Moyasar. It builds a typed dict the
operator can hand off to the CLI (or a future authenticated admin
endpoint) for actual creation.
"""
from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from auto_client_acquisition.finance_os.pricing_catalog import get_pricing_tier
from pydantic import BaseModel, ConfigDict, Field


class InvoiceDraft(BaseModel):
    """One invoice draft ready for the admin CLI to materialize."""

    model_config = ConfigDict(extra="forbid")

    tier_id: str
    customer_email: str
    amount_sar: float
    description_ar: str
    description_en: str
    customer_handle: str = ""
    callback_url: str | None = None
    metadata: dict[str, str] = Field(default_factory=dict)
    approval_status: str = "approval_required"
    safety_notes: list[str] = Field(default_factory=lambda: [
        "no_live_charge_unless_explicit_founder_approval",
        "moyasar_test_mode_default",
        "manual_send_only",
    ])
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    def to_cli_args(self) -> list[str]:
        """Render arguments compatible with scripts/dealix_invoice.py."""
        args = [
            "--email", self.customer_email,
            "--amount-sar", f"{self.amount_sar:g}",
            "--description", self.description_ar or self.description_en,
        ]
        if self.customer_handle:
            args += ["--customer-handle", self.customer_handle]
        if self.callback_url:
            args += ["--callback-url", self.callback_url]
        return args


def draft_invoice(
    tier_id: str,
    customer_email: str,
    customer_handle: str = "",
    callback_url: str | None = None,
    metadata: dict[str, str] | None = None,
) -> InvoiceDraft:
    """Build an InvoiceDraft using a known pricing tier.

    The price is read from the pricing_catalog — never overridden
    by callers, so the founder's ladder stays the source of truth.
    """
    tier = get_pricing_tier(tier_id)
    if tier["pricing_basis"] == "free":
        raise ValueError(
            f"tier {tier_id!r} is free — no invoice needed"
        )

    md = dict(metadata or {})
    md.setdefault("tier_id", tier_id)
    md.setdefault("created_by", "finance_os.draft_invoice")

    return InvoiceDraft(
        tier_id=tier_id,
        customer_email=customer_email,
        customer_handle=customer_handle,
        amount_sar=float(tier["price_sar"]),
        description_ar=tier["description_ar"],
        description_en=tier["description_en"],
        callback_url=callback_url,
        metadata=md,
    )
