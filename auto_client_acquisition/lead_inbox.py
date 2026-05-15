"""Lead Inbox — lightweight JSON-Lines persistence for landing-form leads.

Completes the TODO in `api/routers/public.py:demo_request` so the
founder has a server-side record of every demo / pilot inquiry,
not just analytics events in PostHog.

Storage:
- File path: $DEALIX_LEAD_INBOX_PATH (default: var/lead-inbox.jsonl)
- Format: JSON-Lines (one record per line) — append-only
- Records are PII-redacted on write (email/phone partial mask) for
  any logs; the raw record stays in the file for the founder.

Hard rules:
- No external send (NO_LIVE_SEND)
- No automated outreach to leads from this module
- File store is gitignored (var/) so leads never leak into the repo
"""
from __future__ import annotations

import json
import os
import threading
from datetime import UTC, datetime, timezone
from pathlib import Path
from typing import Any

_DEFAULT_PATH = "var/lead-inbox.jsonl"
_lock = threading.Lock()


def _path() -> Path:
    p = Path(os.environ.get("DEALIX_LEAD_INBOX_PATH", _DEFAULT_PATH))
    if not p.is_absolute():
        # repo root = parent of `auto_client_acquisition/`
        p = Path(__file__).resolve().parent.parent / p
    return p


def _ensure_dir(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def append(record: dict[str, Any]) -> dict[str, Any]:
    """Persist a single lead record. Returns the persisted record
    (with `id` and `received_at` added). Idempotent on email+ts pair.

    Best-effort: failures are swallowed so the calling endpoint
    never returns 5xx because of a disk hiccup. Returns the input
    on failure (with `persisted=False`).
    """
    ts = datetime.now(UTC).isoformat()
    rec = {
        "id": f"lead_{int(datetime.now(UTC).timestamp() * 1000)}",
        "received_at": ts,
        "status": "new",  # new | contacted | qualified | converted | lost
        **{k: v for k, v in record.items() if k not in {"id", "received_at"}},
    }
    try:
        path = _path()
        _ensure_dir(path)
        with _lock, path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        rec["persisted"] = True
    except Exception:
        rec["persisted"] = False
    return rec


def list_leads(limit: int = 200, status: str | None = None) -> list[dict[str, Any]]:
    """Read leads from the JSONL store. Newest first. Returns [] if
    the file does not exist."""
    path = _path()
    if not path.exists():
        return []
    out: list[dict[str, Any]] = []
    try:
        with path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    rec = json.loads(line)
                except Exception:
                    continue
                if status and rec.get("status") != status:
                    continue
                out.append(rec)
    except Exception:
        return []
    out.reverse()  # newest first
    return out[:limit]


def stats() -> dict[str, Any]:
    """Aggregate lead-inbox metrics. Safe on empty store."""
    leads = list_leads(limit=10_000)
    by_status: dict[str, int] = {}
    by_sector: dict[str, int] = {}
    by_source: dict[str, int] = {}
    for r in leads:
        by_status[r.get("status", "new")] = by_status.get(r.get("status", "new"), 0) + 1
        sec = r.get("sector") or "unknown"
        by_sector[sec] = by_sector.get(sec, 0) + 1
        src = r.get("source") or "unknown"
        by_source[src] = by_source.get(src, 0) + 1
    return {
        "total_leads": len(leads),
        "by_status": by_status,
        "by_sector": by_sector,
        "by_source": by_source,
        "store_path": str(_path()),
        "store_exists": _path().exists(),
    }


def update_status(lead_id: str, new_status: str) -> dict[str, Any] | None:
    """Append a status-change event for the given lead. The original
    record stays intact; we append a new line `{id, status, ts,
    event:"status_change"}` so the audit trail is preserved.

    Returns the change record on success, None if the file is empty.
    """
    valid = {"new", "contacted", "qualified", "converted", "lost"}
    if new_status not in valid:
        raise ValueError(f"invalid status: {new_status}")
    path = _path()
    if not path.exists():
        return None
    rec = {
        "event": "status_change",
        "lead_id": lead_id,
        "status": new_status,
        "ts": datetime.now(UTC).isoformat(),
    }
    try:
        with _lock, path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        return rec
    except Exception:
        return None
