"""Tests for daily P0 agency target rotation."""

from __future__ import annotations

from datetime import date

from dealix.commercial_ops.targeting_rotation import (
    apply_rotation_touch_dates,
    select_daily_p0_targets,
)


def _row(
    company: str,
    *,
    priority: str = "high",
    status: str = "not_contacted",
    next_action_date: str = "",
    segment: str = "agency_wedge",
) -> dict[str, str]:
    return {
        "company": company,
        "contact": f"contact@{company}",
        "priority": priority,
        "status": status,
        "next_action_date": next_action_date,
        "segment": segment,
        "motion": "A",
    }


def test_selects_top_n_by_priority_and_status() -> None:
    rows = [
        _row("LowCo", priority="low", status="not_contacted"),
        _row("HighA", priority="high", status="not_contacted"),
        _row("HighB", priority="high", status="replied"),
    ]
    picked = select_daily_p0_targets(rows, top_n=2, on_date=date(2026, 5, 17))
    names = [r["company"] for r in picked]
    assert "HighA" in names
    assert "HighB" in names
    assert "LowCo" not in names


def test_cooldown_skips_recent_touch() -> None:
    rows = [
        _row("Fresh", status="not_contacted", next_action_date=""),
        _row("Touched", status="message_drafted", next_action_date="2026-05-16"),
    ]
    picked = select_daily_p0_targets(
        rows, top_n=10, cooldown_days=3, on_date=date(2026, 5, 17)
    )
    names = {r["company"] for r in picked}
    assert "Fresh" in names
    assert "Touched" not in names


def test_no_duplicate_companies_same_day() -> None:
    rows = [_row(f"Agency{i}") for i in range(20)]
    picked = select_daily_p0_targets(rows, top_n=10, on_date=date(2026, 5, 17))
    companies = [r["company"] for r in picked]
    assert len(companies) == len(set(companies))
    assert len(picked) == 10


def test_apply_rotation_touch_dates() -> None:
    rows = [_row("A"), _row("B")]
    selected = [rows[0]]
    updated = apply_rotation_touch_dates(rows, selected, on_date=date(2026, 5, 17))
    a = next(r for r in updated if r["company"] == "A")
    b = next(r for r in updated if r["company"] == "B")
    assert a["next_action_date"] == "2026-05-17"
    assert a["status"] == "message_drafted"
    assert b.get("next_action_date", "") != "2026-05-17"
