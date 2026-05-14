"""Tests for scripts/weekly_ceo_review.py — output shape and discipline."""
from __future__ import annotations

import importlib.util
import json
from datetime import date
from pathlib import Path

import pytest


_WEEKLY_PATH = Path(__file__).resolve().parents[1] / "scripts" / "weekly_ceo_review.py"
_spec = importlib.util.spec_from_file_location("weekly_ceo_review_mod", _WEEKLY_PATH)
weekly = importlib.util.module_from_spec(_spec)
assert _spec.loader is not None
_spec.loader.exec_module(weekly)


def _fake_verifier(failing: list[str] | None = None) -> dict:
    failing = set(failing or [])
    names = [
        "Doctrine", "Offer Ladder", "Revenue Engine", "Data OS",
        "Governance OS", "Proof OS", "Founder Command Center",
        "Partner Motion", "First Invoice Motion",
    ]
    top8 = {
        "Doctrine", "Offer Ladder", "Revenue Engine", "Data OS",
        "Governance OS", "Proof OS", "Founder Command Center",
        "Partner Motion",
    }
    systems = [
        {
            "name": n,
            "in_top_eight": n in top8,
            "passed": n not in failing,
            "score": 4 if n not in failing else 0,
            "missing": ["x"] if n in failing else [],
        }
        for n in names
    ]
    return {
        "overall_pass": not failing,
        "ceo_complete": not any(s in top8 for s in failing),
        "systems": systems,
    }


def test_isoweek_label_format():
    label = weekly._isoweek_label(date(2026, 5, 14))
    assert label.startswith("2026-W")


def test_week_bounds_monday_to_sunday():
    start, end = weekly._week_bounds("2026-W20")
    assert start.weekday() == 0  # Monday
    assert end.weekday() == 6   # Sunday
    assert (end - start).days == 6


def test_weekly_deltas_with_score_changes():
    rows = [
        {
            "date": "2026-05-11",
            "overall_pass": False,
            "ceo_complete": False,
            "system_scores": {"Partner Motion": 0, "Offer Ladder": 4},
        },
        {
            "date": "2026-05-14",
            "overall_pass": False,
            "ceo_complete": True,
            "system_scores": {"Partner Motion": 4, "Offer Ladder": 4},
        },
    ]
    deltas = weekly._weekly_deltas(rows)
    assert deltas["first_date"] == "2026-05-11"
    assert deltas["last_date"] == "2026-05-14"
    assert any(
        c["system"] == "Partner Motion" and c["from"] == 0 and c["to"] == 4
        for c in deltas["system_score_changes"]
    )
    assert deltas["ceo_complete_first"] is False
    assert deltas["ceo_complete_last"] is True


def test_top_three_next_actions_when_no_outreach_or_invoice():
    payload = _fake_verifier(failing=["Partner Motion"])
    market = {
        "partner_outreach": {"total": 0, "in_week": 0},
        "first_invoice":    {"total": 0, "in_week": 0},
    }
    actions = weekly._top_three_next_actions(payload, market)
    assert any("partner outreach" in a.lower() for a in actions)
    assert any("invoice" in a.lower() for a in actions)
    assert len(actions) <= 3


def test_top_three_next_actions_when_market_motion_active():
    payload = _fake_verifier(failing=None)
    market = {
        "partner_outreach": {"total": 3, "in_week": 1},
        "first_invoice":    {"total": 1, "in_week": 0},
    }
    actions = weekly._top_three_next_actions(payload, market)
    assert any("PASS" in a or "defend" in a.lower() for a in actions)


def test_markdown_review_has_all_required_sections():
    payload = {
        "week_label": "2026-W20",
        "week_start": "2026-05-11",
        "week_end": "2026-05-17",
        "generated_at": "2026-05-14T03:00:00+00:00",
        "verifier": _fake_verifier(failing=["Partner Motion"]),
        "deltas": {
            "system_score_changes": [{"system": "Partner Motion", "from": 0, "to": 4}],
            "first_date": "2026-05-11",
            "last_date": "2026-05-14",
            "overall_pass_first": False, "overall_pass_last": False,
            "ceo_complete_first": False, "ceo_complete_last": True,
        },
        "market_activity": {
            "partner_outreach": {"total": 1, "in_week": 1},
            "first_invoice":    {"total": 0, "in_week": 0},
            "capital_assets":   {"total": 0, "in_week": 0},
        },
        "next_three_actions": [
            "Send one anchor partner outreach.",
            "Open invoice motion.",
            "Lift Partner Motion.",
        ],
    }
    md = weekly._markdown_review(payload)
    assert "# Dealix Weekly CEO Review — 2026-W20" in md
    assert "Verifier State" in md
    assert "Week-over-Week Score Changes" in md
    assert "Market Motion" in md
    assert "Top 3 Actions Next Week" in md
    assert "Partner outreach sent" in md


def test_run_weekly_writes_outputs(tmp_path, monkeypatch):
    """End-to-end: stub the verifier subprocess, run the review."""
    monkeypatch.setattr(weekly, "_run_verifier_json", lambda: _fake_verifier(failing=["Partner Motion"]))
    monkeypatch.setattr(weekly, "STATE_DIR", tmp_path)
    monkeypatch.setattr(weekly, "HISTORY_PATH", tmp_path / "history.jsonl")
    # No history → deltas empty.
    payload = weekly.run_weekly(week_label="2026-W20")
    assert payload["week_label"] == "2026-W20"
    md = (tmp_path / "weekly_review_2026-W20.md").read_text()
    assert "2026-W20" in md
    json.loads((tmp_path / "weekly_review_2026-W20.json").read_text())
