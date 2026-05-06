"""V12.5 RevOps — single-call finance brief for the founder.

Composes:
  - revenue_truth from RX (what's actually paid vs committed vs pipeline)
  - payment confirmations count
  - average margin estimate (if any margins recorded)
  - data_status (insufficient_data / live)
  - bilingual founder action recommendation

Pure function. Read-only. Returns 200 always.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class FinanceBrief:
    cash_collected_sar: int
    commitments_open_sar: int
    pipeline_value_sar: int
    paid_pilots_count: int
    committed_count: int
    payment_confirmations_count: int
    invoice_drafts_count: int
    avg_margin_pct: float | None
    data_status: str  # "insufficient_data" | "live"
    blockers: list[str] = field(default_factory=list)
    next_action_ar: str = ""
    next_action_en: str = ""


def build_finance_brief(
    *,
    pipeline_summary: dict[str, Any],
    payment_confirmations_count: int = 0,
    invoice_drafts_count: int = 0,
    margins: list[float] | None = None,
    pipeline_value_sar: int = 0,
) -> FinanceBrief:
    """Compose a finance brief from explicit inputs.

    ``pipeline_summary`` comes from
    ``revenue_pipeline.RevenuePipeline.summary()``.
    ``margins`` is a list of margin_pct from recent MarginSnapshots.
    """
    cash = pipeline_summary.get("total_revenue_sar", 0)
    paid = pipeline_summary.get("paid", 0)
    committed = pipeline_summary.get("commitments", 0)

    # Commitments_open_sar is "we have signed intent but no cash yet"
    # We approximate by 499 * (committed - paid) since pilot price is fixed
    commitments_open = max(0, (committed - paid) * 499)

    avg_margin = None
    if margins:
        avg_margin = sum(margins) / len(margins)

    blockers: list[str] = []
    if paid == 0:
        blockers.append("no_paid_pilot_yet")
    if committed == 0:
        blockers.append("no_written_commitment_yet")
    if cash == 0 and committed == 0:
        blockers.append("no_revenue_or_commitment_in_pipeline")

    if cash > 0:
        data_status = "live"
        next_ar = f"تأكّد من margin (revenue={cash} SAR، margin% الحالي={avg_margin if avg_margin is not None else 'unknown'})"
        next_en = f"Validate margin (revenue={cash} SAR, current margin%={avg_margin if avg_margin is not None else 'unknown'})"
    elif committed > 0:
        data_status = "insufficient_data"  # commitment ≠ revenue yet
        next_ar = "تابع الدفع لتحويل commitment إلى revenue"
        next_en = "Follow up on payment to convert commitment to revenue."
    else:
        data_status = "insufficient_data"
        next_ar = "ابدأ Phase E — لا revenue ولا commitments بعد"
        next_en = "Start Phase E — no revenue or commitments yet."

    return FinanceBrief(
        cash_collected_sar=cash,
        commitments_open_sar=commitments_open,
        pipeline_value_sar=pipeline_value_sar,
        paid_pilots_count=paid,
        committed_count=committed,
        payment_confirmations_count=payment_confirmations_count,
        invoice_drafts_count=invoice_drafts_count,
        avg_margin_pct=avg_margin,
        data_status=data_status,
        blockers=blockers,
        next_action_ar=next_ar,
        next_action_en=next_en,
    )
