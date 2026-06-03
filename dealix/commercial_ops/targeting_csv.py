"""Agency wedge target list — CSV seed for War Room."""

from __future__ import annotations

import csv
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from dealix.commercial_ops.paths import AGENCY_TARGETS_CSV

TARGET_FIELDS = (
    "company",
    "contact",
    "segment",
    "pain_hypothesis",
    "channel",
    "motion",
    "offer_id",
    "status",
    "next_action",
    "next_action_date",
    "priority",
    "notes",
)


def load_targets(path: Path | None = None) -> list[dict[str, str]]:
    p = path or AGENCY_TARGETS_CSV
    if not p.is_file():
        return []
    with p.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def build_war_room_today(
    targets: list[dict[str, str]] | None = None,
    *,
    top_n: int = 10,
) -> dict[str, Any]:
    """Rank targets for today's War Room (no scraping)."""
    rows = targets if targets is not None else load_targets()
    active_statuses = {
        "not_contacted",
        "message_drafted",
        "approved_to_send",
        "sent_manual",
        "replied",
        "meeting_booked",
    }

    def score_row(r: dict[str, str]) -> tuple[int, str]:
        st = (r.get("status") or "not_contacted").strip()
        pr = (r.get("priority") or "medium").strip().lower()
        pr_rank = {"high": 3, "medium": 2, "low": 1}.get(pr, 2)
        st_rank = 2 if st in active_statuses else 1
        return (pr_rank * 10 + st_rank, r.get("company") or "")

    candidates = [r for r in rows if (r.get("status") or "") != "closed_lost"]
    candidates.sort(key=score_row, reverse=True)
    top = candidates[:top_n]

    today = datetime.now(UTC).date().isoformat()
    follow_ups = [
        r
        for r in candidates
        if (r.get("status") or "") in {"sent_manual", "replied", "message_drafted", "approved_to_send"}
    ][:5]

    return {
        "generated_at": datetime.now(UTC).isoformat(),
        "motion": "A",
        "icp": "agency_wedge",
        "today": today,
        "targets": {
            "top_n": top_n,
            "items": top,
        },
        "follow_ups_due": follow_ups,
        "daily_quotas": {
            "approved_touches": 10,
            "follow_ups": 5,
            "partner_conversations": 1,
            "evidence_events_minimum": 1,
        },
        "policy": {
            "external_send_requires_approval": True,
            "no_cold_whatsapp": True,
            "no_linkedin_auto_send": True,
        },
    }
