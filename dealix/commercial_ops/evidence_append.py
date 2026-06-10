"""Append rows to commercial evidence_events_tracker.csv (governed, no auto-send)."""

from __future__ import annotations

import csv
import uuid
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from dealix.commercial_ops.evidence_csv import COMMERCIAL_EVIDENCE_TYPES, load_evidence_rows
from dealix.commercial_ops.paths import EVIDENCE_TRACKER_CSV

FIELDNAMES = [
    "event_id",
    "event_date",
    "event_type",
    "company",
    "contact",
    "motion",
    "offer_id",
    "owner",
    "source_channel",
    "notes",
    "next_action",
    "next_action_date",
    "war_room_status",
]


def has_evidence_today(
    rows: list[dict[str, str]] | None = None,
    *,
    on_date: str | None = None,
) -> bool:
    today = on_date or datetime.now(UTC).date().isoformat()
    for row in rows if rows is not None else load_evidence_rows():
        if (row.get("event_date") or "").strip()[:10] == today and (row.get("event_type") or "").strip():
            return True
    return False


def append_evidence_row(
    *,
    event_type: str,
    company: str = "",
    contact: str = "",
    motion: str = "A",
    offer_id: str = "ten_lead_audit",
    owner: str = "founder",
    source_channel: str = "manual",
    notes: str = "",
    next_action: str = "",
    next_action_date: str = "",
    war_room_status: str = "",
    event_date: str | None = None,
    event_id: str | None = None,
    path: Path | None = None,
) -> dict[str, str]:
    et = (event_type or "").strip()
    if et not in COMMERCIAL_EVIDENCE_TYPES:
        raise ValueError(f"invalid event_type: {et!r}")

    p = path or EVIDENCE_TRACKER_CSV
    rows = load_evidence_rows(p)
    row: dict[str, str] = {
        "event_id": (event_id or "").strip() or str(uuid.uuid4())[:8],
        "event_date": (event_date or datetime.now(UTC).date().isoformat()),
        "event_type": et,
        "company": (company or "").strip(),
        "contact": (contact or "").strip(),
        "motion": (motion or "A").strip(),
        "offer_id": (offer_id or "").strip(),
        "owner": (owner or "founder").strip(),
        "source_channel": (source_channel or "manual").strip(),
        "notes": (notes or "").strip()[:500],
        "next_action": (next_action or "").strip()[:200],
        "next_action_date": (next_action_date or "").strip()[:10],
        "war_room_status": (war_room_status or "").strip(),
    }

    if rows:
        fieldnames = list(rows[0].keys())
        for k in FIELDNAMES:
            if k not in fieldnames:
                fieldnames.append(k)
    else:
        fieldnames = list(FIELDNAMES)

    rows.append(row)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)

    return row


def log_founder_commercial_day_if_needed(
    *,
    verdict: str = "PASS",
    dry_run: bool = False,
) -> dict[str, Any]:
    """Record one operating evidence row after canonical founder commercial day (no fake revenue)."""
    today = datetime.now(UTC).date().isoformat()
    notes = f"FOUNDER_COMMERCIAL_DAY verdict={verdict} — War Room + digest + SOAEN"
    if dry_run:
        return {
            "appended": False,
            "date": today,
            "reason": "dry_run",
            "would_append": {
                "event_type": "scope_requested",
                "company": "Dealix Founder Commercial Day",
                "notes": notes,
            },
        }
    if has_evidence_today(on_date=today):
        return {
            "appended": False,
            "date": today,
            "reason": "evidence_already_logged_today",
        }
    row = append_evidence_row(
        event_type="scope_requested",
        company="Dealix Founder Commercial Day",
        motion="A",
        offer_id="ten_lead_audit",
        owner="founder",
        source_channel="automation",
        notes=notes,
        next_action="review P0 in /ar/ops/founder and approve touches",
        next_action_date=today,
    )
    return {"appended": True, "date": today, "row": row}


def evening_reminder_ar(*, rows: list[dict[str, str]] | None = None) -> dict[str, Any]:
    """Founder evening check — at least one evidence row today."""
    data = rows if rows is not None else load_evidence_rows()
    today = datetime.now(UTC).date().isoformat()
    ok_today = has_evidence_today(data, on_date=today)
    return {
        "date": today,
        "logged_today": ok_today,
        "reminder_ar": (
            "تم تسجيل حدث أدلة اليوم — أحسنت."
            if ok_today
            else "مساءً: سجّل حدثاً واحداً في evidence_events_tracker.csv (أو --append)."
        ),
        "tracker_path": str(EVIDENCE_TRACKER_CSV),
    }
