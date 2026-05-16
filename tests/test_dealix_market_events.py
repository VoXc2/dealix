from __future__ import annotations

import csv
from pathlib import Path

from scripts.dealix_market_events import (
    SLICE_BIG4_ASSURANCE,
    SLICE_REGULATED_PROCESSOR,
    SLICE_VC_PLATFORM,
    classify_slice,
    load_contacts,
    select_first5,
    summarize_events,
)


def _write_tracker(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "id",
                "lead_name",
                "company",
                "role",
                "segment",
                "channel",
                "sent_at",
                "notes",
            ],
        )
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def test_classify_slice_keywords() -> None:
    assert (
        classify_slice(
            segment="assurance advisory",
            role="Partner",
            company="Audit House",
            notes="",
        )
        == SLICE_BIG4_ASSURANCE
    )
    assert (
        classify_slice(
            segment="fintech",
            role="CEO",
            company="Processor Co",
            notes="regulated payment flow",
        )
        == SLICE_REGULATED_PROCESSOR
    )
    assert (
        classify_slice(
            segment="platform",
            role="Venture lead",
            company="VC Studio",
            notes="portfolio support",
        )
        == SLICE_VC_PLATFORM
    )


def test_select_first5_uses_first_20_and_unsent_only(tmp_path: Path) -> None:
    tracker = tmp_path / "pipeline_tracker.csv"
    rows: list[dict[str, str]] = []
    for idx in range(1, 26):
        rows.append(
            {
                "id": str(idx),
                "lead_name": f"Lead {idx}",
                "company": f"Company {idx}",
                "role": "Founder",
                "segment": "b2b_services",
                "channel": "LinkedIn",
                "sent_at": "2026-05-16T08:00:00+00:00" if idx in (2, 4) else "",
                "notes": "",
            }
        )
    _write_tracker(tracker, rows)

    contacts = load_contacts(tracker)
    selected = select_first5(contacts, pool_limit=20, count=5)
    selected_ids = [c.lead_id for c in selected]
    assert selected_ids == ["1", "3", "5", "6", "7"]


def test_summary_kpi7_counts() -> None:
    events = [
        {"event_type": "sent"},
        {"event_type": "sent"},
        {"event_type": "replied_interested"},
        {"event_type": "meeting_booked"},
        {"event_type": "used_in_meeting"},
        {"event_type": "scope_requested"},
        {"event_type": "invoice_sent"},
        {"event_type": "invoice_paid"},
    ]
    summary = summarize_events(events)
    assert summary["sent_count"] == 2
    assert summary["reply_count"] == 1
    assert summary["meeting_booked_count"] == 1
    assert summary["l5_count"] == 1
    assert summary["l6_count"] == 1
    assert summary["invoice_sent_count"] == 1
    assert summary["paid_proof_count"] == 1
