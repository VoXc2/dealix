"""Referral program persistence — Wave 14D.1.

JSONL-backed store matching the SQL schema in db/migrations/010_referral_program.sql.
Same persistence pattern as friction_log, value_ledger, capital_ledger,
renewal_scheduler. When Postgres lands later, swap _path()-based JSONL for
the corresponding SQL via asyncpg with NO API change.

Tables modelled:
  referral_codes      → ReferralCode dataclass
  referrals           → Referral dataclass
  referral_payouts    → ReferralPayout dataclass
"""
from __future__ import annotations

import hashlib
import json
import os
import secrets
import threading
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from enum import StrEnum
from pathlib import Path
from typing import Any
from uuid import uuid4


class ReferralStatus(StrEnum):
    PENDING = "pending"
    REDEEMED = "redeemed"
    INVOICE_PAID = "invoice_paid"
    CREDIT_ISSUED = "credit_issued"
    DECLINED = "declined"
    CLAWED_BACK = "clawed_back"


# Refund window during which an issued credit can be reclaimed.
CLAWBACK_WINDOW_DAYS = 30


REFERRER_CREDIT_SAR = 5000
REFERRED_DISCOUNT_PCT = 50

_CODES_PATH_DEFAULT = "var/referral-codes.jsonl"
_REFERRALS_PATH_DEFAULT = "var/referrals.jsonl"
_PAYOUTS_PATH_DEFAULT = "var/referral-payouts.jsonl"

_lock = threading.Lock()


def _resolve(env_var: str, default_rel: str) -> Path:
    p = Path(os.environ.get(env_var, default_rel))
    if not p.is_absolute():
        p = Path(__file__).resolve().parent.parent.parent / p
    return p


def _codes_path() -> Path:
    return _resolve("DEALIX_REFERRAL_CODES_PATH", _CODES_PATH_DEFAULT)


def _referrals_path() -> Path:
    return _resolve("DEALIX_REFERRALS_PATH", _REFERRALS_PATH_DEFAULT)


def _payouts_path() -> Path:
    return _resolve("DEALIX_REFERRAL_PAYOUTS_PATH", _PAYOUTS_PATH_DEFAULT)


def _ensure_dir(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def _hash_email(email: str) -> str:
    return hashlib.sha256((email or "").strip().lower().encode("utf-8")).hexdigest()[:16]


def _generate_code(referrer_id: str) -> str:
    """REF-XXXXXXXX where the suffix encodes referrer_id hash for traceability."""
    seed = hashlib.sha256(
        (referrer_id + secrets.token_hex(8)).encode("utf-8")
    ).hexdigest()[:8].upper()
    return f"REF-{seed}"


@dataclass
class ReferralCode:
    code: str = ""
    referrer_id: str = ""
    referrer_email_hash: str = ""
    plan_required: str = "managed_revenue_ops_starter"
    credit_sar: int = REFERRER_CREDIT_SAR
    discount_pct: int = REFERRED_DISCOUNT_PCT
    valid_until: str = ""
    is_revoked: bool = False
    created_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class Referral:
    referral_id: str = field(default_factory=lambda: f"rfl_{uuid4().hex[:12]}")
    code: str = ""
    referrer_id: str = ""
    referred_id: str = ""
    referred_email_hash: str = ""
    status: str = ReferralStatus.PENDING.value
    referred_invoice_id: str = ""
    referred_first_amount_sar: int = 0
    declined_reason: str = ""
    created_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    redeemed_at: str = ""
    paid_at: str = ""
    credit_issued_at: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class ReferralPayout:
    payout_id: str = field(default_factory=lambda: f"pay_{uuid4().hex[:12]}")
    referral_id: str = ""
    credit_sar: int = 0
    applied_to_invoice_id: str = ""
    applied_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    notes: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


# ── Persistence helpers ──────────────────────────────────────────────


def _append(path: Path, payload: dict[str, Any], *, stream_id: str) -> None:
    _ensure_dir(path)
    with _lock:
        with path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(payload, ensure_ascii=False) + "\n")
    from auto_client_acquisition.persistence.operational_stream_mirror import mirror_append

    eid = str(
        payload.get("code")
        or payload.get("referral_id")
        or payload.get("payout_id")
        or payload.get("schedule_id")
        or ""
    )
    mirror_append(stream_id=stream_id, payload=payload, event_id=eid or None)


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


def _rewrite(path: Path, items: list[dict[str, Any]]) -> None:
    _ensure_dir(path)
    with _lock:
        path.write_text(
            "\n".join(json.dumps(i, ensure_ascii=False) for i in items) + ("\n" if items else ""),
            encoding="utf-8",
        )


# ── Public API ───────────────────────────────────────────────────────


def create_referral_code(
    *,
    referrer_id: str,
    referrer_email: str = "",
    plan_required: str = "managed_revenue_ops_starter",
    credit_sar: int = REFERRER_CREDIT_SAR,
    discount_pct: int = REFERRED_DISCOUNT_PCT,
    valid_until: str = "",
) -> ReferralCode:
    if not referrer_id:
        raise ValueError("referrer_id is required")
    code = ReferralCode(
        code=_generate_code(referrer_id),
        referrer_id=referrer_id,
        referrer_email_hash=_hash_email(referrer_email),
        plan_required=plan_required,
        credit_sar=int(credit_sar),
        discount_pct=int(discount_pct),
        valid_until=valid_until,
    )
    _append(_codes_path(), code.to_dict(), stream_id="referral_store_codes")
    return code


def lookup_code(code: str) -> ReferralCode | None:
    code = (code or "").strip().upper()
    if not code:
        return None
    for row in _read_all(_codes_path()):
        if row.get("code") == code and not row.get("is_revoked", False):
            return ReferralCode(**row)
    return None


def revoke_code(code: str) -> bool:
    code = (code or "").strip().upper()
    rows = _read_all(_codes_path())
    found = False
    for row in rows:
        if row.get("code") == code:
            row["is_revoked"] = True
            found = True
    if found:
        _rewrite(_codes_path(), rows)
    return found


def list_codes_by_referrer(referrer_id: str) -> list[ReferralCode]:
    return [
        ReferralCode(**r) for r in _read_all(_codes_path())
        if r.get("referrer_id") == referrer_id and not r.get("is_revoked", False)
    ]


def redeem_referral(
    *,
    code: str,
    referred_id: str,
    referred_email: str = "",
) -> Referral:
    """Redeem a referral code. Idempotent: if a Referral already exists for
    (code, referred_id) it is returned unchanged."""
    if not referred_id:
        raise ValueError("referred_id is required")
    rc = lookup_code(code)
    if rc is None:
        raise ValueError(f"invalid or revoked code: {code}")
    if rc.referrer_id == referred_id:
        raise ValueError("self-referral not allowed")

    # Idempotency check.
    for row in _read_all(_referrals_path()):
        if row.get("code") == rc.code and row.get("referred_id") == referred_id:
            return Referral(**row)

    referral = Referral(
        code=rc.code,
        referrer_id=rc.referrer_id,
        referred_id=referred_id,
        referred_email_hash=_hash_email(referred_email),
        status=ReferralStatus.REDEEMED.value,
        redeemed_at=datetime.now(timezone.utc).isoformat(),
    )
    _append(_referrals_path(), referral.to_dict(), stream_id="referral_store_referrals")
    return referral


def get_referral(referral_id: str) -> Referral | None:
    for row in _read_all(_referrals_path()):
        if row.get("referral_id") == referral_id:
            return Referral(**row)
    return None


def list_referrals(
    *,
    referrer_id: str | None = None,
    referred_id: str | None = None,
    status: str | None = None,
) -> list[Referral]:
    out: list[Referral] = []
    for row in _read_all(_referrals_path()):
        if referrer_id and row.get("referrer_id") != referrer_id:
            continue
        if referred_id and row.get("referred_id") != referred_id:
            continue
        if status and row.get("status") != status:
            continue
        out.append(Referral(**row))
    return out


def mark_invoice_paid(
    *,
    referral_id: str,
    invoice_id: str,
    amount_sar: int,
) -> Referral | None:
    rows = _read_all(_referrals_path())
    updated: Referral | None = None
    for row in rows:
        if row.get("referral_id") == referral_id:
            row["status"] = ReferralStatus.INVOICE_PAID.value
            row["referred_invoice_id"] = invoice_id
            row["referred_first_amount_sar"] = int(amount_sar)
            row["paid_at"] = datetime.now(timezone.utc).isoformat()
            updated = Referral(**row)
            break
    if updated:
        _rewrite(_referrals_path(), rows)
    return updated


def issue_credit(
    *,
    referral_id: str,
    credit_sar: int | None = None,
    applied_to_invoice_id: str = "",
    notes: str = "",
) -> ReferralPayout | None:
    referral = get_referral(referral_id)
    if referral is None:
        return None
    # DOCTRINE — no credit before the referred invoice is paid. A merely
    # REDEEMED referral has produced no revenue yet, so no payout issues.
    if referral.status != ReferralStatus.INVOICE_PAID.value:
        return None

    code_obj = lookup_code(referral.code)
    sar = int(credit_sar if credit_sar is not None else (code_obj.credit_sar if code_obj else REFERRER_CREDIT_SAR))
    payout = ReferralPayout(
        referral_id=referral_id,
        credit_sar=sar,
        applied_to_invoice_id=applied_to_invoice_id,
        notes=notes,
    )
    _append(_payouts_path(), payout.to_dict(), stream_id="referral_store_payouts")

    # Update referral status.
    rows = _read_all(_referrals_path())
    for row in rows:
        if row.get("referral_id") == referral_id:
            row["status"] = ReferralStatus.CREDIT_ISSUED.value
            row["credit_issued_at"] = payout.applied_at
            break
    _rewrite(_referrals_path(), rows)
    return payout


def clawback_credit(
    *,
    referral_id: str,
    reason: str = "refund",
    requested_at: str = "",
) -> ReferralPayout | None:
    """Reverse an issued credit within the 30-day refund window.

    DOCTRINE — a payout is only ever reclaimed, never silently kept on a
    refunded deal. The clawback:
      - requires the referral to be in CREDIT_ISSUED status,
      - is rejected if the refund request falls outside
        ``CLAWBACK_WINDOW_DAYS`` from when the credit was issued,
      - writes a negative-amount ``ReferralPayout`` row (audit trail) and
        transitions the referral to CLAWED_BACK.

    Returns the reversal payout, or None when no clawback is performed.
    """
    referral = get_referral(referral_id)
    if referral is None:
        return None
    if referral.status != ReferralStatus.CREDIT_ISSUED.value:
        return None

    issued_at = referral.credit_issued_at
    if issued_at:
        try:
            issued_dt = datetime.fromisoformat(issued_at)
        except ValueError:
            issued_dt = None
        if issued_dt is not None:
            req = (requested_at or datetime.now(timezone.utc).isoformat())
            try:
                req_dt = datetime.fromisoformat(req)
            except ValueError:
                req_dt = datetime.now(timezone.utc)
            if (req_dt - issued_dt).days > CLAWBACK_WINDOW_DAYS:
                return None

    # Sum the credits that were issued so we reverse the exact amount.
    issued_total = sum(
        int(p.get("credit_sar", 0))
        for p in _read_all(_payouts_path())
        if p.get("referral_id") == referral_id and int(p.get("credit_sar", 0)) > 0
    )
    reversal = ReferralPayout(
        referral_id=referral_id,
        credit_sar=-issued_total,
        notes=f"clawback: {reason[:200]}",
    )
    _append(_payouts_path(), reversal.to_dict(), stream_id="referral_store_payouts")

    rows = _read_all(_referrals_path())
    for row in rows:
        if row.get("referral_id") == referral_id:
            row["status"] = ReferralStatus.CLAWED_BACK.value
            break
    _rewrite(_referrals_path(), rows)
    return reversal


def decline_referral(*, referral_id: str, reason: str) -> Referral | None:
    rows = _read_all(_referrals_path())
    updated: Referral | None = None
    for row in rows:
        if row.get("referral_id") == referral_id:
            row["status"] = ReferralStatus.DECLINED.value
            row["declined_reason"] = reason[:256]
            updated = Referral(**row)
            break
    if updated:
        _rewrite(_referrals_path(), rows)
    return updated


def clear_for_test() -> None:
    for p in (_codes_path(), _referrals_path(), _payouts_path()):
        if p.exists():
            with _lock:
                p.write_text("", encoding="utf-8")


__all__ = [
    "CLAWBACK_WINDOW_DAYS",
    "REFERRED_DISCOUNT_PCT",
    "REFERRER_CREDIT_SAR",
    "Referral",
    "ReferralCode",
    "ReferralPayout",
    "ReferralStatus",
    "clawback_credit",
    "clear_for_test",
    "create_referral_code",
    "decline_referral",
    "get_referral",
    "issue_credit",
    "list_codes_by_referrer",
    "list_referrals",
    "lookup_code",
    "mark_invoice_paid",
    "redeem_referral",
    "revoke_code",
]
