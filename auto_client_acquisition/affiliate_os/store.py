"""Affiliate OS persistence — JSONL-backed store.

Same pattern as ``partnership_os/referral_store.py`` and
``evidence_control_plane_os/evidence_object.py``: JSONL files keyed by
env-var paths, swappable for Postgres later with NO API change.

Three streams:
  affiliates           → Affiliate dataclass
  affiliate_commissions → Commission dataclass (from commission.py)
  affiliate_payouts    → AffiliatePayout dataclass
"""
from __future__ import annotations

import hashlib
import json
import os
import threading
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime, timezone
from pathlib import Path
from typing import Any
from uuid import uuid4

from auto_client_acquisition.affiliate_os.commission import Commission

_AFFILIATES_PATH_DEFAULT = "var/affiliates.jsonl"
_COMMISSIONS_PATH_DEFAULT = "var/affiliate-commissions.jsonl"
_PAYOUTS_PATH_DEFAULT = "var/affiliate-payouts.jsonl"

_lock = threading.Lock()


def _resolve(env_var: str, default_rel: str) -> Path:
    p = Path(os.environ.get(env_var, default_rel))
    if not p.is_absolute():
        p = Path(__file__).resolve().parent.parent.parent / p
    return p


def _affiliates_path() -> Path:
    return _resolve("DEALIX_AFFILIATES_PATH", _AFFILIATES_PATH_DEFAULT)


def _commissions_path() -> Path:
    return _resolve("DEALIX_AFFILIATE_COMMISSIONS_PATH", _COMMISSIONS_PATH_DEFAULT)


def _payouts_path() -> Path:
    return _resolve("DEALIX_AFFILIATE_PAYOUTS_PATH", _PAYOUTS_PATH_DEFAULT)


def _hash_email(email: str) -> str:
    return hashlib.sha256((email or "").strip().lower().encode("utf-8")).hexdigest()[:16]


def _now() -> str:
    return datetime.now(UTC).isoformat()


# ── Dataclasses ──────────────────────────────────────────────────────


@dataclass
class Affiliate:
    affiliate_id: str = field(default_factory=lambda: f"aff_{uuid4().hex[:12]}")
    handle: str = ""
    email_hash: str = ""
    partner_type: str = "affiliate_marketer"
    application_score: int = 0
    application_recommendation: str = "needs_review"
    status: str = "pending"  # pending | active | paused | rejected
    approval_id: str = ""
    created_at: str = field(default_factory=_now)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class AffiliatePayout:
    payout_id: str = field(default_factory=lambda: f"apo_{uuid4().hex[:12]}")
    commission_id: str = ""
    affiliate_id: str = ""
    amount_sar: float = 0.0
    approval_id: str = ""
    paid_at: str = field(default_factory=_now)
    notes: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


# ── Persistence helpers ──────────────────────────────────────────────


def _append(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with _lock, path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(payload, ensure_ascii=False) + "\n")


def _read_all(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    out: list[dict[str, Any]] = []
    with _lock, path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return out


def _rewrite(path: Path, items: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with _lock:
        path.write_text(
            "\n".join(json.dumps(i, ensure_ascii=False) for i in items)
            + ("\n" if items else ""),
            encoding="utf-8",
        )


# ── Affiliates ───────────────────────────────────────────────────────


def register_affiliate(
    *,
    handle: str,
    email: str = "",
    partner_type: str = "affiliate_marketer",
    application_score: int = 0,
    application_recommendation: str = "needs_review",
    approval_id: str = "",
) -> Affiliate:
    """Register an affiliate in ``pending`` status. Activation is a
    separate, approval-gated step — registration never auto-activates."""
    if not handle:
        raise ValueError("handle is required")
    affiliate = Affiliate(
        handle=handle,
        email_hash=_hash_email(email),
        partner_type=partner_type,
        application_score=application_score,
        application_recommendation=application_recommendation,
        approval_id=approval_id,
        status="pending",
    )
    _append(_affiliates_path(), affiliate.to_dict())
    return affiliate


def get_affiliate(affiliate_id: str) -> Affiliate | None:
    for row in _read_all(_affiliates_path()):
        if row.get("affiliate_id") == affiliate_id:
            return Affiliate(**row)
    return None


def list_affiliates(status: str | None = None) -> list[Affiliate]:
    out: list[Affiliate] = []
    for row in _read_all(_affiliates_path()):
        if status and row.get("status") != status:
            continue
        out.append(Affiliate(**row))
    return out


def set_affiliate_status(affiliate_id: str, status: str) -> Affiliate | None:
    if status not in {"pending", "active", "paused", "rejected"}:
        raise ValueError(f"invalid affiliate status: {status}")
    rows = _read_all(_affiliates_path())
    updated: Affiliate | None = None
    for row in rows:
        if row.get("affiliate_id") == affiliate_id:
            row["status"] = status
            updated = Affiliate(**row)
            break
    if updated:
        _rewrite(_affiliates_path(), rows)
    return updated


# ── Commissions ──────────────────────────────────────────────────────


def save_commission(commission: Commission) -> Commission:
    """Persist a freshly computed commission."""
    _append(_commissions_path(), commission.to_dict())
    return commission


def get_commission(commission_id: str) -> Commission | None:
    for row in _read_all(_commissions_path()):
        if row.get("commission_id") == commission_id:
            return Commission(**row)
    return None


def list_commissions(
    *,
    status: str | None = None,
    affiliate_id: str | None = None,
) -> list[Commission]:
    out: list[Commission] = []
    for row in _read_all(_commissions_path()):
        if status and row.get("status") != status:
            continue
        if affiliate_id and row.get("affiliate_id") != affiliate_id:
            continue
        out.append(Commission(**row))
    return out


def update_commission(
    commission_id: str,
    *,
    status: str | None = None,
    approval_id: str | None = None,
    eligibility_reasons: list[str] | None = None,
    notes: str | None = None,
) -> Commission | None:
    """Patch a stored commission. Returns the updated record or None."""
    rows = _read_all(_commissions_path())
    updated: Commission | None = None
    for row in rows:
        if row.get("commission_id") == commission_id:
            if status is not None:
                row["status"] = status
            if approval_id is not None:
                row["approval_id"] = approval_id
            if eligibility_reasons is not None:
                row["eligibility_reasons"] = list(eligibility_reasons)
            if notes is not None:
                row["notes"] = notes
            row["updated_at"] = _now()
            updated = Commission(**row)
            break
    if updated:
        _rewrite(_commissions_path(), rows)
    return updated


# ── Payouts ──────────────────────────────────────────────────────────


def record_payout(
    *,
    commission_id: str,
    affiliate_id: str,
    amount_sar: float,
    approval_id: str,
    notes: str = "",
) -> AffiliatePayout:
    """Record a confirmed payout. Callers must verify the ApprovalRequest
    is approved BEFORE calling this — the store does not approve anything."""
    if not approval_id:
        raise ValueError("approval_id is required — payout needs an approved request")
    payout = AffiliatePayout(
        commission_id=commission_id,
        affiliate_id=affiliate_id,
        amount_sar=float(amount_sar),
        approval_id=approval_id,
        notes=notes,
    )
    _append(_payouts_path(), payout.to_dict())
    return payout


def list_payouts(affiliate_id: str | None = None) -> list[AffiliatePayout]:
    out: list[AffiliatePayout] = []
    for row in _read_all(_payouts_path()):
        if affiliate_id and row.get("affiliate_id") != affiliate_id:
            continue
        out.append(AffiliatePayout(**row))
    return out


def clear_for_test() -> None:
    for p in (_affiliates_path(), _commissions_path(), _payouts_path()):
        if p.exists():
            with _lock:
                p.write_text("", encoding="utf-8")


__all__ = [
    "Affiliate",
    "AffiliatePayout",
    "clear_for_test",
    "get_affiliate",
    "get_commission",
    "list_affiliates",
    "list_commissions",
    "list_payouts",
    "record_payout",
    "register_affiliate",
    "save_commission",
    "set_affiliate_status",
    "update_commission",
]
