"""Deal Desk OS v0 — draft-only deal closure requests (approval-first)."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Any, Literal
from uuid import uuid4

DealDeskStatus = Literal["draft", "pending_approval", "approved", "rejected"]


@dataclass
class DealDeskRequest:
    request_id: str
    company: str
    offer_tier: str
    amount_sar: float
    objection_tags: list[str]
    status: DealDeskStatus
    notes: str
    created_at: str
    requires_founder_approval: bool = True

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


_STORE: dict[str, DealDeskRequest] = {}


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def create_deal_desk_request(
    *,
    company: str,
    offer_tier: str,
    amount_sar: float,
    objection_tags: list[str] | None = None,
    notes: str = "",
) -> DealDeskRequest:
    """Create a draft deal desk request — never auto-executes externally."""
    req = DealDeskRequest(
        request_id=str(uuid4()),
        company=company.strip(),
        offer_tier=offer_tier.strip(),
        amount_sar=float(amount_sar),
        objection_tags=list(objection_tags or []),
        status="draft",
        notes=notes.strip(),
        created_at=_now_iso(),
        requires_founder_approval=True,
    )
    _STORE[req.request_id] = req
    return req


def submit_for_approval(request_id: str) -> DealDeskRequest:
    req = _require(request_id)
    if req.status != "draft":
        raise ValueError("only_draft_can_submit")
    req.status = "pending_approval"
    return req


def record_approval(request_id: str, *, approved: bool, approver_note: str = "") -> DealDeskRequest:
    req = _require(request_id)
    if req.status != "pending_approval":
        raise ValueError("not_pending_approval")
    req.status = "approved" if approved else "rejected"
    if approver_note:
        req.notes = f"{req.notes}\n[approval] {approver_note}".strip()
    return req


def get_request(request_id: str) -> DealDeskRequest | None:
    return _STORE.get(request_id)


def list_requests(*, status: DealDeskStatus | None = None) -> list[DealDeskRequest]:
    rows = list(_STORE.values())
    if status is None:
        return sorted(rows, key=lambda r: r.created_at, reverse=True)
    return [r for r in rows if r.status == status]


def objection_intelligence_hints(tags: list[str]) -> list[str]:
    """Static hints for objection tags — no external send."""
    hints: list[str] = []
    mapping = {
        "price": "اربط العرض بقيمة موثقة (L3+) و pilot 499 SAR",
        "timing": "اقترح sprint قصير مع exit واضح",
        "trust": "قدّم Trust pack + PDPL checklist",
        "competitor": "ركز على Revenue Memory و approval-first",
    }
    for tag in tags:
        key = tag.strip().lower()
        if key in mapping:
            hints.append(mapping[key])
    return hints


def _require(request_id: str) -> DealDeskRequest:
    req = _STORE.get(request_id)
    if req is None:
        raise KeyError(request_id)
    return req


def reset_store_for_tests() -> None:
    _STORE.clear()
