"""Tests for scripts/daily_routine.py — output shape and honesty.

These tests import the module directly (not via subprocess) so the test
suite stays fast and deterministic. The module unit-tests its pure
helpers; the integration smoke (full subprocess invocation of the
verifier) is exercised by the CI workflow itself.
"""
from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import patch

import pytest

import importlib.util
import sys

_DAILY_PATH = Path(__file__).resolve().parents[1] / "scripts" / "daily_routine.py"
_spec = importlib.util.spec_from_file_location("daily_routine_mod", _DAILY_PATH)
daily = importlib.util.module_from_spec(_spec)
assert _spec.loader is not None
_spec.loader.exec_module(daily)
sys.modules["daily_routine_mod"] = daily


def _fake_verifier_payload(failing: list[str] | None = None) -> dict:
    systems = []
    failing = set(failing or [])
    names = [
        "Doctrine", "Offer Ladder", "Revenue Engine", "Data OS",
        "Governance OS", "Proof OS", "Value OS", "Capital OS",
        "Retainer Engine", "Trust Pack", "Evidence Control Plane",
        "Agent Safety", "GCC Expansion", "Funding Pack", "Open Doctrine",
        "Founder Command Center", "Partner Motion",
        "First Invoice Motion", "Continuous Routine",
    ]
    top8 = {
        "Doctrine", "Offer Ladder", "Revenue Engine", "Data OS",
        "Governance OS", "Proof OS", "Founder Command Center",
        "Partner Motion",
    }
    for name in names:
        is_fail = name in failing
        systems.append({
            "name": name,
            "in_top_eight": name in top8,
            "passed": not is_fail,
            "score": 4 if not is_fail else 0,
            "missing": ["something missing"] if is_fail else [],
        })
    return {
        "overall_pass": not failing,
        "ceo_complete": not any(s in top8 for s in failing),
        "systems": systems,
    }


def test_bottleneck_sentence_picks_top_eight_failing_first():
    payload = _fake_verifier_payload(failing=["Partner Motion", "GCC Expansion"])
    sentence = daily._bottleneck_sentence(payload)
    assert "Partner Motion" in sentence
    assert "top-8" in sentence


def test_bottleneck_sentence_when_overall_pass():
    payload = _fake_verifier_payload(failing=None)
    sentence = daily._bottleneck_sentence(payload)
    assert "PASS" in sentence


def test_compute_deltas_no_prior_row():
    payload = _fake_verifier_payload(failing=None)
    deltas = daily._compute_deltas(payload, prev_row=None)
    assert deltas["vs_date"] is None
    assert deltas["system_score_changes"] == []
    assert deltas["overall_pass_changed"] is False


def test_compute_deltas_with_score_changes():
    today = _fake_verifier_payload(failing=None)
    prev = {
        "date": "2026-05-13",
        "overall_pass": False,
        "ceo_complete": False,
        "system_scores": {s["name"]: 0 for s in today["systems"]},
    }
    deltas = daily._compute_deltas(today, prev_row=prev)
    assert deltas["vs_date"] == "2026-05-13"
    assert deltas["overall_pass_changed"] is True
    assert deltas["ceo_complete_changed"] is True
    assert len(deltas["system_score_changes"]) == 19
    for ch in deltas["system_score_changes"]:
        assert ch["from"] == 0
        assert ch["to"] == 4


def test_market_motion_status_reads_real_files_honestly():
    """The function never mutates; it only reads `count` keys."""
    out = daily._market_motion_status()
    assert "partner_outreach" in out
    assert "first_invoice" in out
    # Either the file exists and count is an int, or it doesn't.
    for key in ("partner_outreach", "first_invoice"):
        entry = out[key]
        if entry["file_present"]:
            assert isinstance(entry["count"], int)
            assert entry["count"] >= 0


def test_markdown_brief_contains_required_sections():
    today = _fake_verifier_payload(failing=["Partner Motion"])
    payload = {
        "date": "2026-05-14",
        "generated_at": "2026-05-14T03:00:00+00:00",
        "bottleneck": daily._bottleneck_sentence(today),
        "verifier": today,
        "deltas": daily._compute_deltas(today, prev_row=None),
        "market_motion": {
            "partner_outreach": {"file_present": True, "count": 0},
            "first_invoice": {"file_present": True, "count": 0},
        },
        "founder_brief": {},
    }
    md = daily._markdown_brief(payload)
    assert "# Dealix Daily Brief — 2026-05-14" in md
    assert "Today's CEO bottleneck:" in md
    assert "Master Verifier" in md
    assert "Day-over-Day Deltas" in md
    assert "Market Motion" in md
    assert "Partner outreach sent" in md
    assert "Partner Motion" in md  # bottleneck system name surfaces


def test_run_daily_writes_outputs(tmp_path, monkeypatch):
    """End-to-end: stub the verifier subprocess, run the routine, check outputs."""
    fake_payload = _fake_verifier_payload(failing=["Partner Motion"])

    def fake_run_json(cmd):
        return fake_payload

    monkeypatch.setattr(daily, "_run_json", fake_run_json)
    monkeypatch.setattr(daily, "STATE_DIR", tmp_path / "_state")
    monkeypatch.setattr(daily, "HISTORY_PATH", tmp_path / "_state" / "history.jsonl")
    monkeypatch.setattr(daily, "FOUNDER_BRIEF", tmp_path / "absent.py")

    payload = daily.run_daily(target_date="2026-05-14")
    assert payload["date"] == "2026-05-14"
    json_path = tmp_path / "_state" / "daily_routine_2026-05-14.json"
    md_path = tmp_path / "_state" / "daily_brief_2026-05-14.md"
    assert json_path.exists()
    assert md_path.exists()
    # Parses cleanly.
    json.loads(json_path.read_text())
    md = md_path.read_text()
    assert "Today's CEO bottleneck:" in md
    # History row appended.
    assert (tmp_path / "_state" / "history.jsonl").exists()
