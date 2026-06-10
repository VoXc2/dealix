"""Evidence CSV — placeholder rows excluded from revenue truth."""

from __future__ import annotations

from datetime import date

from dealix.commercial_ops.evidence_csv import (
    count_evidence_events,
    is_placeholder_evidence_row,
    real_evidence_rows,
)


def test_template_notes_are_placeholders():
    row = {
        "company": "",
        "notes": "template_funnel_seed — not a deal",
        "event_type": "payment_received",
    }
    assert is_placeholder_evidence_row(row)


def test_real_company_not_placeholder():
    row = {
        "company": "Agency Alpha",
        "notes": "warm intro",
        "event_type": "invoice_sent",
    }
    assert not is_placeholder_evidence_row(row)


def test_count_evidence_excludes_placeholders():
    rows = [
        {
            "event_date": "2026-05-17",
            "event_type": "payment_received",
            "company": "",
            "notes": "template_funnel_seed",
        },
        {
            "event_date": "2026-05-17",
            "event_type": "invoice_sent",
            "company": "Real Co",
            "notes": "demo",
        },
    ]
    all_counts = count_evidence_events(rows, on_date=date(2026, 5, 17))
    real_counts = count_evidence_events(
        rows, on_date=date(2026, 5, 17), exclude_placeholders=True
    )
    assert all_counts["today_total"] == 2
    assert real_counts["today_total"] == 1
    assert len(real_evidence_rows(rows)) == 1
