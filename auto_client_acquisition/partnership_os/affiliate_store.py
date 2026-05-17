"""Affiliate & Partner machine persistence — JSONL store.

Mirrors the JSONL store pattern of ``value_ledger`` / ``friction_log`` /
``renewal_scheduler``. Each record type lives in its own JSONL file,
path-overridable via a ``DEALIX_*_PATH`` env var. The SQLAlchemy
``*Record`` models in ``db/models.py`` (migration 013) are the eventual
relational home; this store keeps the machine runnable and testable
before a live Postgres is wired in.

Doctrine notes:
  - contact emails are stored HASHED only (``contact_email_hash``) — no
    raw PII ever touches disk (non-negotiable #6);
  - all records carry a stable id + ``created_at`` UTC.
"""

from __future__ import annotations

import hashlib
import json
import os
import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import uuid4

_lock = threading.RLock()

# (env var, default relative path) per record type.
_FILES: dict[str, tuple[str, str]] = {
    "partners": ("DEALIX_AFFILIATE_PARTNERS_PATH", "var/affiliate-partners.jsonl"),
    "links": ("DEALIX_AFFILIATE_LINKS_PATH", "var/affiliate-links.jsonl"),
    "referrals": ("DEALIX_AFFILIATE_REFERRALS_PATH", "var/affiliate-referrals.jsonl"),
    "commissions": ("DEALIX_AFFILIATE_COMMISSIONS_PATH", "var/affiliate-commissions.jsonl"),
    "payouts": ("DEALIX_AFFILIATE_PAYOUTS_PATH", "var/affiliate-payouts.jsonl"),
    "compliance": ("DEALIX_AFFILIATE_COMPLIANCE_PATH", "var/affiliate-compliance.jsonl"),
}

_REPO_ROOT = Path(__file__).resolve().parent.parent.parent


def _path(kind: str) -> Path:
    env_var, default = _FILES[kind]
    p = Path(os.environ.get(env_var, default))
    if not p.is_absolute():
        p = _REPO_ROOT / p
    return p


def now_iso() -> str:
    """Return the current UTC time as an ISO 8601 string."""
    return datetime.now(timezone.utc).isoformat()


def new_id(prefix: str) -> str:
    """Return a stable short id with ``prefix``."""
    return f"{prefix}_{uuid4().hex[:12]}"


def hash_email(email: str) -> str:
    """Return a stable non-reversible hash of an email (no raw PII stored)."""
    return hashlib.sha256(email.strip().lower().encode()).hexdigest()[:32]


def _append(kind: str, record: dict[str, Any]) -> dict[str, Any]:
    path = _path(kind)
    with _lock:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(record, ensure_ascii=False) + "\n")
    return record


def _read_all(kind: str) -> list[dict[str, Any]]:
    path = _path(kind)
    if not path.exists():
        return []
    out: list[dict[str, Any]] = []
    with _lock:
        with path.open("r", encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    out.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    return out


def _rewrite(kind: str, records: list[dict[str, Any]]) -> None:
    path = _path(kind)
    with _lock:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as fh:
            for rec in records:
                fh.write(json.dumps(rec, ensure_ascii=False) + "\n")


# ── Generic CRUD ────────────────────────────────────────────────────

def insert(kind: str, record: dict[str, Any]) -> dict[str, Any]:
    """Insert a record into the ``kind`` stream. Returns the record."""
    if kind not in _FILES:
        raise ValueError(f"unknown record kind: {kind!r}")
    return _append(kind, record)


def get(kind: str, record_id: str) -> dict[str, Any] | None:
    """Return the latest (non-deleted) version of a record by id."""
    found: dict[str, Any] | None = None
    for rec in _read_all(kind):
        if rec.get("id") == record_id:
            found = rec
    if found is not None and found.get("deleted_at"):
        return None
    return found


def list_records(kind: str, **filters: Any) -> list[dict[str, Any]]:
    """Return the latest version of every non-deleted record in ``kind``.

    Optional keyword filters do an equality match on top-level fields.
    """
    latest: dict[str, dict[str, Any]] = {}
    for rec in _read_all(kind):
        rid = rec.get("id")
        if rid is not None:
            latest[rid] = rec
    out: list[dict[str, Any]] = []
    for rec in latest.values():
        if rec.get("deleted_at"):
            continue
        if all(rec.get(k) == v for k, v in filters.items()):
            out.append(rec)
    return out


def update(kind: str, record_id: str, patch: dict[str, Any]) -> dict[str, Any] | None:
    """Apply ``patch`` to a record and append the new version. Returns it."""
    current = get(kind, record_id)
    if current is None:
        return None
    updated = {**current, **patch, "id": record_id}
    return _append(kind, updated)


def clear_for_test() -> None:
    """Truncate every affiliate JSONL file. Test-only helper."""
    for kind in _FILES:
        path = _path(kind)
        if path.exists():
            with _lock:
                path.write_text("", encoding="utf-8")


__all__ = [
    "clear_for_test",
    "get",
    "hash_email",
    "insert",
    "list_records",
    "new_id",
    "now_iso",
    "update",
]
