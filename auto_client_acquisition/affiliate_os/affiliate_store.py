"""Affiliate OS — affiliate profile persistence (JSONL).

Same JSONL pattern as partnership_os/referral_store.py. When Postgres lands
the public functions stay identical and the backend swaps underneath.

Audit: every intake and status decision is recorded to the customer-scoped
audit ledger under the placeholder tenant ``dealix_affiliate_ops``.
"""

from __future__ import annotations

import json
import os
import threading
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from auto_client_acquisition.affiliate_os.affiliate_profile import (
    Affiliate,
    AffiliateApplication,
)
from auto_client_acquisition.affiliate_os.fit_score import compute_affiliate_fit_score
from auto_client_acquisition.affiliate_os.rules_loader import tier_for_score
from auto_client_acquisition.auditability_os.audit_event import (
    AuditEventKind,
    record_event,
)

AFFILIATE_OPS_TENANT = "dealix_affiliate_ops"

_AFFILIATES_PATH_DEFAULT = "var/affiliates.jsonl"
_lock = threading.Lock()


def _resolve(env_var: str, default_rel: str) -> Path:
    p = Path(os.environ.get(env_var, default_rel))
    if not p.is_absolute():
        p = Path(__file__).resolve().parent.parent.parent / p
    return p


def _affiliates_path() -> Path:
    return _resolve("DEALIX_AFFILIATES_PATH", _AFFILIATES_PATH_DEFAULT)


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


def _rewrite(path: Path, items: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with _lock:
        path.write_text(
            "\n".join(json.dumps(i, ensure_ascii=False) for i in items)
            + ("\n" if items else ""),
            encoding="utf-8",
        )


def submit_application(application: AffiliateApplication) -> Affiliate:
    """Intake an affiliate application. Idempotent on affiliate_id — a second
    submission with the same id returns the already-persisted profile."""
    existing = get_affiliate(application.affiliate_id)
    if existing is not None:
        return existing

    score = compute_affiliate_fit_score(application=application)
    affiliate = Affiliate(
        affiliate_id=application.affiliate_id,
        placeholder_name=application.placeholder_name,
        affiliate_type=application.affiliate_type,
        audience_segment=application.audience_segment,
        region=application.region,
        promo_channel=application.promo_channel,
        status="pending",
        fit_score=score,
        tier=tier_for_score(score),
    )
    _append(_affiliates_path(), affiliate.model_dump())
    record_event(
        customer_id=AFFILIATE_OPS_TENANT,
        kind=AuditEventKind.GOVERNANCE_DECISION,
        actor="affiliate_os",
        decision="affiliate_application_received",
        policy_checked="affiliate_intake",
        summary=f"affiliate {affiliate.affiliate_id} fit={score} tier={affiliate.tier}",
        source_refs=[affiliate.affiliate_id],
    )
    return affiliate


def get_affiliate(affiliate_id: str) -> Affiliate | None:
    """Latest profile state for an affiliate (last write wins)."""
    found: Affiliate | None = None
    for row in _read_all(_affiliates_path()):
        if row.get("affiliate_id") == affiliate_id:
            found = Affiliate(**row)
    return found


def list_affiliates(*, status: str | None = None) -> list[Affiliate]:
    """All affiliates, deduplicated to the latest state per affiliate_id."""
    latest: dict[str, Affiliate] = {}
    for row in _read_all(_affiliates_path()):
        aid = row.get("affiliate_id")
        if aid:
            latest[aid] = Affiliate(**row)
    out = list(latest.values())
    if status:
        out = [a for a in out if a.status == status]
    return out


def set_status(
    *,
    affiliate_id: str,
    status: str,
    reason: str = "",
) -> Affiliate | None:
    """Transition an affiliate to approved/rejected. Only pending affiliates
    may transition; returns None if the affiliate is missing."""
    affiliate = get_affiliate(affiliate_id)
    if affiliate is None:
        return None
    if status not in ("approved", "rejected"):
        raise ValueError(f"unsupported affiliate status: {status!r}")
    if affiliate.status != "pending":
        return affiliate

    affiliate.status = status  # type: ignore[assignment]
    affiliate.decided_at = datetime.now(UTC).isoformat()
    if status == "rejected":
        affiliate.rejected_reason = reason[:256]
    _append(_affiliates_path(), affiliate.model_dump())
    record_event(
        customer_id=AFFILIATE_OPS_TENANT,
        kind=AuditEventKind.APPROVAL,
        actor="founder",
        decision=f"affiliate_{status}",
        policy_checked="affiliate_status_decision",
        summary=f"affiliate {affiliate_id} -> {status}",
        source_refs=[affiliate_id],
    )
    return affiliate


def clear_for_test() -> None:
    path = _affiliates_path()
    if path.exists():
        with _lock:
            path.write_text("", encoding="utf-8")


__all__ = [
    "AFFILIATE_OPS_TENANT",
    "clear_for_test",
    "get_affiliate",
    "list_affiliates",
    "set_status",
    "submit_application",
]
