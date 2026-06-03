"""Commercial evidence events — CSV tracker + optional API sync."""

from __future__ import annotations

import csv
import json
import os
from collections import Counter
from datetime import UTC, date, datetime, timedelta
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from dealix.commercial_ops.paths import EVIDENCE_TRACKER_CSV

COMMERCIAL_EVIDENCE_TYPES: frozenset[str] = frozenset(
    {
        "message_sent_manual",
        "reply_received",
        "demo_booked",
        "scope_requested",
        "invoice_sent",
        "payment_received",
        "proof_pack_delivered",
        "partner_intro_created",
        "referral_requested",
    }
)

PLACEHOLDER_COMPANIES: frozenset[str] = frozenset(
    {
        "",
        "founder_launch_day",
        "dealix soft launch",
        "dealix founder commercial day",
    }
)


def is_placeholder_evidence_row(row: dict[str, str]) -> bool:
    """Template / operating rows — excluded from first-paid and funnel KPI truth."""
    company = (row.get("company") or "").strip().lower()
    if not company or company in PLACEHOLDER_COMPANIES:
        return True
    notes = (row.get("notes") or "").strip().lower()
    if notes.startswith("template_"):
        return True
    return False


def real_evidence_rows(rows: list[dict[str, str]] | None = None) -> list[dict[str, str]]:
    data = rows if rows is not None else load_evidence_rows()
    return [r for r in data if not is_placeholder_evidence_row(r)]


def load_evidence_rows(path: Path | None = None) -> list[dict[str, str]]:
    p = path or EVIDENCE_TRACKER_CSV
    if not p.is_file():
        return []
    with p.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def count_evidence_events(
    rows: list[dict[str, str]] | None = None,
    *,
    on_date: date | None = None,
    since_days: int | None = None,
    exclude_placeholders: bool = False,
) -> dict[str, Any]:
    """Count events for today, rolling week, and by type."""
    data = rows if rows is not None else load_evidence_rows()
    if exclude_placeholders:
        data = real_evidence_rows(data)
    today = on_date or datetime.now(UTC).date()
    week_start = today - timedelta(days=6)

    today_counts: Counter[str] = Counter()
    week_counts: Counter[str] = Counter()
    all_time: Counter[str] = Counter()

    for row in data:
        et = (row.get("event_type") or "").strip()
        if not et:
            continue
        raw_date = (row.get("event_date") or "").strip()[:10]
        try:
            ed = date.fromisoformat(raw_date) if raw_date else None
        except ValueError:
            ed = None

        all_time[et] += 1
        if ed == today:
            today_counts[et] += 1
        if ed is not None and week_start <= ed <= today:
            week_counts[et] += 1

    return {
        "date": today.isoformat(),
        "today_total": sum(today_counts.values()),
        "week_total": sum(week_counts.values()),
        "today_by_type": dict(today_counts),
        "week_by_type": dict(week_counts),
        "all_time_by_type": dict(all_time),
    }


def scope_requested_within_days(days: int, rows: list[dict[str, str]] | None = None) -> bool:
    data = rows if rows is not None else load_evidence_rows()
    cutoff = datetime.now(UTC).date() - timedelta(days=days)
    for row in data:
        if (row.get("event_type") or "").strip() != "scope_requested":
            continue
        raw = (row.get("event_date") or "").strip()[:10]
        try:
            if date.fromisoformat(raw) >= cutoff:
                return True
        except ValueError:
            continue
    return False


def _write_evidence_rows(rows: list[dict[str, str]], path: Path | None = None) -> None:
    p = path or EVIDENCE_TRACKER_CSV
    if not rows:
        return
    fieldnames = list(rows[0].keys())
    for row in rows:
        for k in row:
            if k not in fieldnames:
                fieldnames.append(k)
    if "synced_api" not in fieldnames:
        fieldnames.append("synced_api")
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def sync_rows_to_api(
    rows: list[dict[str, str]] | None = None,
    *,
    api_base: str | None = None,
    admin_key: str | None = None,
    only_unsynced: bool = True,
    mark_csv: bool = True,
) -> dict[str, Any]:
    """POST rows to /api/v1/evidence/events (admin). Optionally marks synced_api=1 in CSV."""
    base = (api_base or os.environ.get("DEALIX_API_BASE") or "").rstrip("/")
    key = admin_key or os.environ.get("DEALIX_ADMIN_API_KEY") or os.environ.get("DEALIX_API_KEY") or ""
    if not base or not key:
        return {"status": "skipped", "reason": "missing_api_base_or_key", "synced": 0}

    data = rows if rows is not None else load_evidence_rows()
    synced = 0
    errors: list[str] = []

    for row in data:
        et = (row.get("event_type") or "").strip()
        if et not in COMMERCIAL_EVIDENCE_TYPES:
            continue
        if only_unsynced and (row.get("synced_api") or "").lower() in {"1", "true", "yes"}:
            continue
        company = (row.get("company") or "").strip()
        summary = (row.get("notes") or "").strip() or f"{et} · {company or 'n/a'}"
        payload = {
            "event_type": et,
            "summary": summary[:500],
            "entity_type": "commercial_tracker",
            "entity_id": (row.get("event_id") or "").strip() or et,
        }
        req = Request(
            f"{base}/api/v1/evidence/events",
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "X-Admin-API-Key": key,
            },
            method="POST",
        )
        try:
            with urlopen(req, timeout=15) as resp:  # noqa: S310
                if 200 <= resp.status < 300:
                    synced += 1
                    if mark_csv:
                        row["synced_api"] = "1"
        except (HTTPError, URLError, TimeoutError) as exc:
            errors.append(f"{et}:{exc}")
            if len(errors) >= 5:
                break

    if mark_csv and synced and data is rows:
        _write_evidence_rows(data)

    return {"status": "ok" if not errors else "partial", "synced": synced, "errors": errors}


def pull_events_from_api(
    *,
    api_base: str | None = None,
    admin_key: str | None = None,
    path: Path | None = None,
    limit: int = 100,
) -> dict[str, Any]:
    """Append API evidence events not already in CSV (by entity_id + event_type)."""
    base = (api_base or os.environ.get("DEALIX_API_BASE") or "").rstrip("/")
    key = admin_key or os.environ.get("DEALIX_ADMIN_API_KEY") or os.environ.get("DEALIX_API_KEY") or ""
    if not base or not key:
        return {"status": "skipped", "reason": "missing_api_base_or_key", "appended": 0}

    req = Request(
        f"{base}/api/v1/evidence/events?limit={limit}",
        headers={"X-Admin-API-Key": key},
        method="GET",
    )
    try:
        with urlopen(req, timeout=20) as resp:  # noqa: S310
            payload = json.loads(resp.read().decode("utf-8"))
    except (HTTPError, URLError, TimeoutError, json.JSONDecodeError) as exc:
        return {"status": "error", "reason": str(exc), "appended": 0}

    events = payload if isinstance(payload, list) else payload.get("events") or payload.get("items") or []
    rows = load_evidence_rows(path)
    existing = {
        (
            (r.get("event_type") or "").strip(),
            (r.get("event_id") or "").strip() or (r.get("notes") or "").strip()[:80],
        )
        for r in rows
    }
    appended = 0
    today = datetime.now(UTC).date().isoformat()
    for ev in events:
        if not isinstance(ev, dict):
            continue
        et = (ev.get("event_type") or "").strip()
        if et not in COMMERCIAL_EVIDENCE_TYPES and not et.startswith("founder_"):
            continue
        eid = (ev.get("id") or ev.get("entity_id") or "").strip()
        key_tuple = (et, eid)
        if key_tuple in existing:
            continue
        raw_ts = (ev.get("created_at") or ev.get("timestamp") or "")[:10]
        rows.append(
            {
                "event_id": eid,
                "event_date": raw_ts or today,
                "event_type": et,
                "company": "",
                "contact": "",
                "motion": "",
                "offer_id": "",
                "owner": "api_pull",
                "source_channel": "autopilot",
                "notes": (ev.get("summary") or "")[:200],
                "next_action": "",
                "next_action_date": "",
                "war_room_status": "",
                "synced_api": "1",
            }
        )
        existing.add(key_tuple)
        appended += 1

    if appended:
        _write_evidence_rows(rows, path)
    return {"status": "ok", "appended": appended}
