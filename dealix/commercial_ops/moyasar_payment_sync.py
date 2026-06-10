"""Post-Moyasar webhook: HubSpot sync + evidence ledger (best-effort, no invented CRM)."""

from __future__ import annotations

import logging
from typing import Any

log = logging.getLogger(__name__)

_PAID_STATUSES = frozenset({"paid", "captured", "payment_paid", "invoice_paid"})


def _is_paid(payment: dict[str, Any], event_type: str) -> bool:
    status = str(payment.get("status") or "").lower()
    et = str(event_type or "").lower()
    return status in _PAID_STATUSES or et in _PAID_STATUSES or "paid" in et


def _metadata(payment: dict[str, Any]) -> dict[str, Any]:
    raw = payment.get("metadata")
    return raw if isinstance(raw, dict) else {}


def sync_paid_payment_to_hubspot(
    *,
    payment: dict[str, Any],
    event_type: str,
) -> dict[str, Any]:
    """Sync funnel lead to HubSpot when payment is confirmed (skipped if not configured)."""
    if not _is_paid(payment, event_type):
        return {"skipped": True, "reason": "not_paid_status"}

    meta = _metadata(payment)
    lead_id = str(meta.get("lead_id") or "").strip()
    email = str(meta.get("email") or payment.get("source", {}).get("email") or "").strip()
    company = str(meta.get("company") or meta.get("company_name") or "").strip()

    from dealix.revenue_ops_autopilot.crm_bridge import sync_lead_to_hubspot
    from dealix.revenue_ops_autopilot.schemas import FunnelLeadRecord
    from dealix.revenue_ops_autopilot.store import get_autopilot_store

    store = get_autopilot_store()
    record: FunnelLeadRecord | None = None
    if lead_id:
        record = store.get_lead(lead_id)
    if record is None and email:
        for lead in store.list_leads():
            if (lead.email or "").lower() == email.lower():
                record = lead
                break

    if record is None:
        record = FunnelLeadRecord(
            id=lead_id or f"pay_{email or company or 'unknown'}",
            company=company or email or "Unknown",
            email=email,
            stage="invoice_paid",
            source="moyasar_webhook",
        )
    else:
        record = record.model_copy(update={"stage": "invoice_paid"})

    try:
        out = sync_lead_to_hubspot(record, store=store)
        return {"hubspot": out, "lead_id": record.id}
    except Exception as exc:
        log.warning("moyasar_hubspot_sync_failed lead=%s error=%s", record.id, exc)
        return {"hubspot": {"synced": False, "reason": str(exc)}, "lead_id": record.id}


def append_payment_evidence(
    *,
    payment: dict[str, Any],
    event_type: str,
) -> dict[str, Any]:
    """Append payment_received to commercial evidence CSV when paid."""
    if not _is_paid(payment, event_type):
        return {"skipped": True, "reason": "not_paid_status"}

    meta = _metadata(payment)
    company = str(meta.get("company") or meta.get("company_name") or "").strip()
    email = str(meta.get("email") or "").strip()
    plan = str(meta.get("plan") or "diagnostic").strip()
    amount_halalas = int(payment.get("amount") or 0)
    amount_sar = amount_halalas / 100 if amount_halalas else 0

    if not company and not email:
        return {"skipped": True, "reason": "no_company_or_email_in_metadata"}

    from dealix.commercial_ops.evidence_append import append_evidence_row

    try:
        row = append_evidence_row(
            event_type="payment_received",
            company=company or email,
            contact=email,
            motion="A",
            offer_id=plan,
            source_channel="moyasar_webhook",
            notes=f"moyasar paid {amount_sar:.2f} SAR plan={plan}",
            war_room_status="invoice_paid",
        )
        return {"evidence": row}
    except Exception as exc:
        log.warning("moyasar_evidence_append_failed error=%s", exc)
        return {"skipped": True, "reason": str(exc)}


def process_moyasar_payment_side_effects(
    *,
    payment: dict[str, Any],
    event_type: str,
) -> dict[str, Any]:
    """HubSpot + evidence after successful payment persist."""
    hub = sync_paid_payment_to_hubspot(payment=payment, event_type=event_type)
    ev = append_payment_evidence(payment=payment, event_type=event_type)
    return {"hubspot_sync": hub, "evidence": ev}
