"""Daily finance brief — cash, commitments, costs, margin sketch."""
from __future__ import annotations

from datetime import UTC, date, datetime
from typing import Any

from auto_client_acquisition.revops.margin import MarginInputs, estimate_margin
from auto_client_acquisition.revops.revenue_truth import build_revops_truth_snapshot
from auto_client_acquisition.revenue_pipeline.pipeline import get_default_pipeline


def build_finance_brief(
    *,
    delivery_hours_month: float = 0.0,
    support_hours_month: float = 0.0,
    refund_risk_factor: float = 0.0,
) -> dict[str, Any]:
    """Compose finance-facing snapshot from default pipeline + hour estimates."""
    pipe = get_default_pipeline()
    summary = pipe.summary()
    truth = build_revops_truth_snapshot(summary)

    margin = estimate_margin(
        MarginInputs(
            revenue_sar=int(summary.get("total_revenue_sar", 0)),
            delivery_hours=delivery_hours_month,
            support_hours=support_hours_month,
            refund_risk_factor=refund_risk_factor,
        )
    )

    today = date.today().isoformat()
    return {
        "schema_version": 1,
        "generated_at": datetime.now(UTC).isoformat(),
        "period_label": "rolling_in_memory_store",
        "cash_collected_today": "unknown_without_ledger",
        "cash_collected_month": int(summary.get("total_revenue_sar", 0)),
        "commitments_open": int(summary.get("commitments", 0)),
        "invoice_drafts_pending": "see_finance_os_invoice_draft",
        "payment_confirmations_needed": 0 if truth["payment_evidence_is_revenue"] else 1,
        "delivery_cost_estimate_sar": margin.get("delivery_cost_sar"),
        "support_cost_estimate_sar": margin.get("support_cost_sar"),
        "gross_margin_estimate": margin,
        "refund_risk": refund_risk_factor,
        "revenue_truth": truth,
        "hard_gates": {
            "no_live_charge": True,
            "draft_invoice_not_revenue": True,
        },
        "next_action_ar": f"حدّث مراجع الدفع الفعلية لليوم {today} إن وُجدت",
        "next_action_en": f"Log real payment references for {today} when cash lands.",
    }
