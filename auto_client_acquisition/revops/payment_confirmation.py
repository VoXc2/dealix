"""Payment confirmation checklist — manual evidence only (no live gateway)."""
from __future__ import annotations

from typing import Any


def payment_confirmation_checklist(
    *,
    payment_evidence_present: bool,
    amount_sar: int | None,
) -> dict[str, Any]:
    ok = bool(payment_evidence_present and amount_sar and amount_sar > 0)
    return {
        "schema_version": 1,
        "confirmation_ready": ok,
        "required_fields": [
            "payment_evidence_reference",
            "actual_amount_sar_gt_0",
        ],
        "blocked_without": [] if ok else ["payment_evidence_or_amount_missing"],
        "action_mode": "manual_log_only",
    }
