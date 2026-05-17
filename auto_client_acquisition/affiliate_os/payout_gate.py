"""Affiliate OS — three-condition payout gate.

A payout to an affiliate is released ONLY when all three hold:

1. a commission record exists for the payout;
2. the underlying invoice still has payment-confirmation evidence; and
3. a human has approved the payout via the Approval Center.

``request_payout`` opens an ApprovalRequest. ``finalize_payout`` reads the
approval state — it never approves on its own. ``approve_payout`` is the
ops convenience that approves the ApprovalRequest then finalizes.
"""

from __future__ import annotations

import json
import os
import threading
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Literal
from uuid import uuid4

from pydantic import BaseModel, ConfigDict

from auto_client_acquisition.affiliate_os.affiliate_store import AFFILIATE_OPS_TENANT
from auto_client_acquisition.affiliate_os.commission_engine import (
    _invoice_is_paid,
    get_commission,
)
from auto_client_acquisition.affiliate_os.rules_loader import min_payout_sar
from auto_client_acquisition.approval_center.approval_store import (
    get_default_approval_store,
)
from auto_client_acquisition.approval_center.schemas import (
    ApprovalRequest,
    ApprovalStatus,
)
from auto_client_acquisition.auditability_os.audit_event import (
    AuditEventKind,
    record_event,
)

_PAYOUTS_PATH_DEFAULT = "var/affiliate-payouts.jsonl"
_lock = threading.Lock()

PayoutStatus = Literal["pending_approval", "paid", "blocked"]


def _resolve(env_var: str, default_rel: str) -> Path:
    p = Path(os.environ.get(env_var, default_rel))
    if not p.is_absolute():
        p = Path(__file__).resolve().parent.parent.parent / p
    return p


def _payouts_path() -> Path:
    return _resolve("DEALIX_AFFILIATE_PAYOUTS_PATH", _PAYOUTS_PATH_DEFAULT)


class PayoutRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")

    payout_id: str
    commission_id: str
    affiliate_id: str
    amount_sar: int
    approval_id: str = ""
    status: PayoutStatus = "pending_approval"
    blocked_reason: str = ""
    created_at: str
    paid_at: str = ""


def _append(payload: dict[str, Any]) -> None:
    path = _payouts_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    with _lock:
        with path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(payload, ensure_ascii=False) + "\n")


def _read_all() -> list[dict[str, Any]]:
    path = _payouts_path()
    if not path.exists():
        return []
    out: list[dict[str, Any]] = []
    with _lock:
        with path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    out.append(json.loads(line))
                except Exception:  # noqa: BLE001
                    continue
    return out


def get_payout(payout_id: str) -> PayoutRecord | None:
    found: PayoutRecord | None = None
    for row in _read_all():
        if row.get("payout_id") == payout_id:
            found = PayoutRecord(**row)
    return found


def list_payouts(*, affiliate_id: str | None = None) -> list[PayoutRecord]:
    latest: dict[str, PayoutRecord] = {}
    for row in _read_all():
        pid = row.get("payout_id")
        if pid:
            latest[pid] = PayoutRecord(**row)
    out = list(latest.values())
    if affiliate_id:
        out = [p for p in out if p.affiliate_id == affiliate_id]
    return out


def request_payout(*, commission_id: str) -> PayoutRecord:
    """Open a payout. Verifies the commission and its invoice evidence, then
    creates a high-risk ApprovalRequest. The payout stays pending until a
    human approves — it is never auto-released."""
    now = datetime.now(UTC).isoformat()
    commission = get_commission(commission_id)
    if commission is None:
        record = PayoutRecord(
            payout_id=f"apo_{uuid4().hex[:12]}",
            commission_id=commission_id,
            affiliate_id="",
            amount_sar=0,
            status="blocked",
            blocked_reason="no_commission",
            created_at=now,
        )
        _append(record.model_dump())
        return record

    paid, _ = _invoice_is_paid(commission.invoice_id)
    if not paid:
        record = PayoutRecord(
            payout_id=f"apo_{uuid4().hex[:12]}",
            commission_id=commission_id,
            affiliate_id=commission.affiliate_id,
            amount_sar=commission.commission_amount_sar,
            status="blocked",
            blocked_reason="invoice_paid_evidence_missing",
            created_at=now,
        )
        _append(record.model_dump())
        return record

    if commission.commission_amount_sar < min_payout_sar():
        record = PayoutRecord(
            payout_id=f"apo_{uuid4().hex[:12]}",
            commission_id=commission_id,
            affiliate_id=commission.affiliate_id,
            amount_sar=commission.commission_amount_sar,
            status="blocked",
            blocked_reason="below_min_payout",
            created_at=now,
        )
        _append(record.model_dump())
        return record

    payout_id = f"apo_{uuid4().hex[:12]}"
    store = get_default_approval_store()
    req = ApprovalRequest(
        object_type="affiliate_payout",
        object_id=payout_id,
        action_type="affiliate_payout",
        action_mode="approval_required",
        risk_level="high",
        proof_target="affiliate_payout_completed",
        summary_en=(
            f"Affiliate payout {commission.commission_amount_sar} SAR "
            f"to {commission.affiliate_id} (commission {commission_id})"
        ),
        summary_ar=(
            f"دفع عمولة شريك {commission.commission_amount_sar} ريال "
            f"للشريك {commission.affiliate_id}"
        ),
    )
    store.create(req)

    record = PayoutRecord(
        payout_id=payout_id,
        commission_id=commission_id,
        affiliate_id=commission.affiliate_id,
        amount_sar=commission.commission_amount_sar,
        approval_id=req.approval_id,
        status="pending_approval",
        created_at=now,
    )
    _append(record.model_dump())
    record_event(
        customer_id=AFFILIATE_OPS_TENANT,
        kind=AuditEventKind.APPROVAL,
        actor="affiliate_os",
        decision="payout_pending_approval",
        policy_checked="payout_requires_human_approval",
        summary=f"payout {payout_id} awaiting approval {req.approval_id}",
        source_refs=[commission.affiliate_id, commission_id],
        output_refs=[payout_id],
    )
    return record


def finalize_payout(*, payout_id: str, approver: str) -> PayoutRecord | None:
    """Settle a payout IFF its ApprovalRequest is approved. If the approval
    is still pending the payout is returned unchanged — it is NOT paid."""
    payout = get_payout(payout_id)
    if payout is None:
        return None
    if payout.status != "pending_approval":
        return payout

    store = get_default_approval_store()
    req = store.get(payout.approval_id)
    if req is None or str(req.status) != ApprovalStatus.APPROVED.value:
        return payout  # hard gate — no payout without an approved request

    payout.status = "paid"
    payout.paid_at = datetime.now(UTC).isoformat()
    _append(payout.model_dump())
    record_event(
        customer_id=AFFILIATE_OPS_TENANT,
        kind=AuditEventKind.OUTPUT_DELIVERED,
        actor=approver or "founder",
        decision="payout_paid",
        policy_checked="payout_requires_human_approval",
        summary=f"payout {payout_id} settled ({payout.amount_sar} SAR)",
        source_refs=[payout.affiliate_id, payout.commission_id],
        output_refs=[payout_id],
    )
    return payout


def approve_payout(*, payout_id: str, approver: str) -> PayoutRecord | None:
    """Ops convenience: approve the underlying ApprovalRequest then finalize."""
    payout = get_payout(payout_id)
    if payout is None:
        return None
    if payout.status == "pending_approval" and payout.approval_id:
        store = get_default_approval_store()
        store.approve(payout.approval_id, approver or "founder")
    return finalize_payout(payout_id=payout_id, approver=approver)


def clear_for_test() -> None:
    path = _payouts_path()
    if path.exists():
        with _lock:
            path.write_text("", encoding="utf-8")


__all__ = [
    "PayoutRecord",
    "approve_payout",
    "clear_for_test",
    "finalize_payout",
    "get_payout",
    "list_payouts",
    "request_payout",
]
