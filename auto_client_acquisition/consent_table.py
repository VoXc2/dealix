"""V14 Phase K4 — per-channel × per-purpose consent table (default-deny).

Closes the registry gap for `consent_required_send`: the existing
`customer_inbox_v10.consent_status.check_consent()` is a single
boolean per conversation. This module upgrades the schema so a
single contact can have explicit consent for, e.g., transactional
email but NOT marketing WhatsApp — without conflating the two.

Design (kept deliberately small, no DB):

  - Append-only JSON-Lines store at $DEALIX_CONSENT_TABLE_PATH
    (default: `var/consent-table.jsonl`, gitignored).
  - Every record is one of:
      kind="grant"   — explicit consent for (channel, purpose) pair
      kind="revoke"  — revoke consent for (channel, purpose) pair
                       (revoke is permanent under PDPL Article 5)
  - `is_consented(contact, channel, purpose)` walks the records
    newest-first; first revoke wins; first grant after a revoke
    requires a brand-new explicit grant (PDPL: opt-out is permanent).
  - Default-deny: absence of any record means NO consent.

This module is the persistence layer. Callers (whatsapp_safe_send,
routing_policy, outreach_drafts) query it before any external send.

Hard rules:
  - Default-deny on absent record (PDPL Article 5)
  - Revoke is permanent and overrides earlier grants for the same
    (channel, purpose) pair
  - Storage file is gitignored — consent records never leak to repo
  - Best-effort I/O: failures are swallowed and treated as "no consent"
    (default-deny again)
"""
from __future__ import annotations

import json
import os
import threading
from collections.abc import Iterable
from dataclasses import dataclass
from datetime import UTC, datetime, timezone
from pathlib import Path
from typing import Any, Literal

# ─── Channels + purposes (deliberate enumerations) ───
ALLOWED_CHANNELS = frozenset({
    "whatsapp", "email", "linkedin", "phone", "sms",
})
ALLOWED_PURPOSES = frozenset({
    "transactional",   # invoice, receipt, support reply
    "marketing",       # newsletter, promo, cross-sell
    "delivery_update", # 7-day pilot status messages
    "support",         # helpdesk replies inside an open ticket
    "follow_up",       # post-pilot check-in within 30 days
})

_DEFAULT_PATH = "var/consent-table.jsonl"
_lock = threading.Lock()


def _path() -> Path:
    p = Path(os.environ.get("DEALIX_CONSENT_TABLE_PATH", _DEFAULT_PATH))
    if not p.is_absolute():
        p = Path(__file__).resolve().parent.parent / p
    return p


def _ensure_dir(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


@dataclass(frozen=True)
class ConsentRecord:
    """One row in the consent table."""

    contact_id: str       # anonymized handle / email / msisdn
    channel: str          # one of ALLOWED_CHANNELS
    purpose: str          # one of ALLOWED_PURPOSES
    kind: Literal["grant", "revoke"]
    occurred_at: str      # ISO 8601 UTC
    source: str = "manual"  # form_submission / api / explicit_email / etc.
    proof_url: str = ""   # link to original consent capture, if any


def _validate(channel: str, purpose: str) -> None:
    if channel not in ALLOWED_CHANNELS:
        raise ValueError(
            f"unknown channel {channel!r}; allowed: {sorted(ALLOWED_CHANNELS)}"
        )
    if purpose not in ALLOWED_PURPOSES:
        raise ValueError(
            f"unknown purpose {purpose!r}; allowed: {sorted(ALLOWED_PURPOSES)}"
        )


def grant(
    *,
    contact_id: str,
    channel: str,
    purpose: str,
    source: str = "form_submission",
    proof_url: str = "",
    occurred_at: str | None = None,
) -> ConsentRecord:
    """Record an explicit consent grant for (channel, purpose)."""
    _validate(channel, purpose)
    rec = ConsentRecord(
        contact_id=contact_id,
        channel=channel,
        purpose=purpose,
        kind="grant",
        occurred_at=occurred_at or datetime.now(UTC).isoformat(),
        source=source,
        proof_url=proof_url,
    )
    _append(rec)
    return rec


def revoke(
    *,
    contact_id: str,
    channel: str,
    purpose: str,
    source: str = "list_unsubscribe_header",
    occurred_at: str | None = None,
) -> ConsentRecord:
    """Permanent revocation. Overrides any earlier grant for the same
    (channel, purpose) pair. PDPL: opt-out is permanent."""
    _validate(channel, purpose)
    rec = ConsentRecord(
        contact_id=contact_id,
        channel=channel,
        purpose=purpose,
        kind="revoke",
        occurred_at=occurred_at or datetime.now(UTC).isoformat(),
        source=source,
    )
    _append(rec)
    return rec


def _append(rec: ConsentRecord) -> bool:
    """Persist one record. Best-effort — returns False on I/O failure."""
    try:
        path = _path()
        _ensure_dir(path)
        with _lock, path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(rec.__dict__, ensure_ascii=False) + "\n")
        return True
    except Exception:
        return False


def _all_records() -> list[ConsentRecord]:
    """Read every record from the store. Empty list if file missing or unreadable.
    Returns records in chronological insertion order (oldest first)."""
    path = _path()
    if not path.exists():
        return []
    out: list[ConsentRecord] = []
    try:
        with path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    d = json.loads(line)
                    out.append(ConsentRecord(**d))
                except Exception:  # noqa: S112 - skip malformed ledger line
                    continue
    except Exception:
        return []
    return out


def records_for(contact_id: str) -> list[ConsentRecord]:
    """All records for one contact, oldest first."""
    return [r for r in _all_records() if r.contact_id == contact_id]


def is_consented(
    *,
    contact_id: str,
    channel: str,
    purpose: str,
) -> bool:
    """Default-deny consent gate.

    Walks the contact's records newest-first. First record that
    matches (channel, purpose) wins:
      - grant  → True
      - revoke → False (permanent)
    No matching record → False (default-deny).
    """
    if not contact_id or channel not in ALLOWED_CHANNELS or purpose not in ALLOWED_PURPOSES:
        return False  # malformed input → default-deny
    records = records_for(contact_id)
    for rec in reversed(records):  # newest first
        if rec.channel == channel and rec.purpose == purpose:
            return rec.kind == "grant"
    return False  # no record → default-deny


def stats() -> dict[str, Any]:
    """Aggregate stats for the consent table (founder dashboard surface)."""
    records = _all_records()
    by_kind: dict[str, int] = {}
    by_channel: dict[str, int] = {}
    by_purpose: dict[str, int] = {}
    contacts: set[str] = set()
    for r in records:
        by_kind[r.kind] = by_kind.get(r.kind, 0) + 1
        by_channel[r.channel] = by_channel.get(r.channel, 0) + 1
        by_purpose[r.purpose] = by_purpose.get(r.purpose, 0) + 1
        contacts.add(r.contact_id)
    return {
        "total_records": len(records),
        "unique_contacts": len(contacts),
        "by_kind": by_kind,
        "by_channel": by_channel,
        "by_purpose": by_purpose,
        "store_path": str(_path()),
        "store_exists": _path().exists(),
    }
