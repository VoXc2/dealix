"""Affiliate OS — evidence-gated commission accrual.

Hard rule: a referral becomes a commission ONLY when the referred deal's
invoice has a recorded payment confirmation (evidence). A draft invoice, a
verbal yes, or an unpaid invoice produce no commission. The source of truth
for "is this invoice paid?" is revops.payment_confirmation — invoice_state.py
is a pure state machine with no registry to query.
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

from auto_client_acquisition.affiliate_os.affiliate_store import (
    AFFILIATE_OPS_TENANT,
    get_affiliate,
)
from auto_client_acquisition.affiliate_os.referral_links import lookup_link
from auto_client_acquisition.affiliate_os.rules_loader import commission_rate_for_tier
from auto_client_acquisition.auditability_os.audit_event import (
    AuditEventKind,
    record_event,
)

_COMMISSIONS_PATH_DEFAULT = "var/affiliate-commissions.jsonl"
_lock = threading.Lock()


def _resolve(env_var: str, default_rel: str) -> Path:
    p = Path(os.environ.get(env_var, default_rel))
    if not p.is_absolute():
        p = Path(__file__).resolve().parent.parent.parent / p
    return p


def _commissions_path() -> Path:
    return _resolve("DEALIX_AFFILIATE_COMMISSIONS_PATH", _COMMISSIONS_PATH_DEFAULT)


class Commission(BaseModel):
    model_config = ConfigDict(extra="forbid")

    commission_id: str
    affiliate_id: str
    referral_code: str
    invoice_id: str
    deal_amount_sar: int
    commission_rate: float
    commission_amount_sar: int
    evidence_reference: str
    status: Literal["accrued"] = "accrued"
    created_at: str


def _append(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with _lock:
        with path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(payload, ensure_ascii=False) + "\n")


def _read_all(path: Path) -> list[dict[str, Any]]:
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


def _invoice_is_paid(invoice_id: str) -> tuple[bool, str]:
    """Return (paid, evidence_reference). Paid iff a payment confirmation
    exists for this invoice_id."""
    try:
        from auto_client_acquisition.revops.payment_confirmation import (
            list_confirmations,
        )
    except Exception:  # noqa: BLE001
        return False, ""
    for conf in list_confirmations():
        if getattr(conf, "invoice_id", "") == invoice_id:
            return True, getattr(conf, "evidence_reference", "")
    return False, ""


def calculate_commission(
    *,
    affiliate_id: str,
    referral_code: str,
    invoice_id: str,
    deal_amount_sar: int,
) -> Commission | None:
    """Accrue a commission for a referred, PAID deal.

    Returns None (no commission) when any gate fails: unknown/unapproved
    affiliate, invalid/revoked/mismatched link, or — the hard gate — no
    payment confirmation for the invoice.
    """
    affiliate = get_affiliate(affiliate_id)
    if affiliate is None or affiliate.status != "approved":
        return None

    link = lookup_link(referral_code)
    if link is None or link.is_revoked or link.affiliate_id != affiliate_id:
        return None

    # Idempotency — one commission per invoice.
    for row in _read_all(_commissions_path()):
        if row.get("invoice_id") == invoice_id:
            return Commission(**row)

    paid, evidence = _invoice_is_paid(invoice_id)
    if not paid:
        record_event(
            customer_id=AFFILIATE_OPS_TENANT,
            kind=AuditEventKind.GOVERNANCE_DECISION,
            actor="affiliate_os",
            decision="commission_blocked_no_evidence",
            policy_checked="commission_requires_invoice_paid",
            summary=f"invoice {invoice_id} has no payment confirmation",
            source_refs=[affiliate_id, referral_code, invoice_id],
        )
        return None

    rate = commission_rate_for_tier(affiliate.tier)
    commission = Commission(
        commission_id=f"acm_{uuid4().hex[:12]}",
        affiliate_id=affiliate_id,
        referral_code=referral_code,
        invoice_id=invoice_id,
        deal_amount_sar=int(deal_amount_sar),
        commission_rate=rate,
        commission_amount_sar=round(int(deal_amount_sar) * rate),
        evidence_reference=evidence,
        created_at=datetime.now(UTC).isoformat(),
    )
    _append(_commissions_path(), commission.model_dump())
    record_event(
        customer_id=AFFILIATE_OPS_TENANT,
        kind=AuditEventKind.OUTPUT_DELIVERED,
        actor="affiliate_os",
        decision="commission_accrued",
        policy_checked="commission_requires_invoice_paid",
        summary=(
            f"commission {commission.commission_id} "
            f"{commission.commission_amount_sar} SAR for {affiliate_id}"
        ),
        source_refs=[affiliate_id, referral_code, invoice_id],
        output_refs=[commission.commission_id],
    )
    return commission


def get_commission(commission_id: str) -> Commission | None:
    for row in _read_all(_commissions_path()):
        if row.get("commission_id") == commission_id:
            return Commission(**row)
    return None


def list_commissions(
    *,
    affiliate_id: str | None = None,
    invoice_id: str | None = None,
) -> list[Commission]:
    out: list[Commission] = []
    for row in _read_all(_commissions_path()):
        if affiliate_id and row.get("affiliate_id") != affiliate_id:
            continue
        if invoice_id and row.get("invoice_id") != invoice_id:
            continue
        out.append(Commission(**row))
    return out


def clear_for_test() -> None:
    path = _commissions_path()
    if path.exists():
        with _lock:
            path.write_text("", encoding="utf-8")


__all__ = [
    "Commission",
    "calculate_commission",
    "clear_for_test",
    "get_commission",
    "list_commissions",
]
