"""Wave 6 Phase 8 — demo outcome logger tests."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

SCRIPT = Path("scripts/dealix_demo_outcome.py")


def _run(args: list[str]):
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        capture_output=True, text=True,
    )


def test_script_exists() -> None:
    assert SCRIPT.exists()


def test_log_interested(tmp_path) -> None:
    out = tmp_path / "outcomes.jsonl"
    r = _run([
        "--prospect-handle", "prospect-1",
        "--sector", "real_estate",
        "--outcome", "interested",
        "--next-action", "send Calendly link",
        "--out-path", str(out),
    ])
    assert r.returncode == 0
    line = out.read_text(encoding="utf-8").strip()
    rec = json.loads(line)
    assert rec["outcome"] == "interested"
    assert rec["is_revenue"] is False


def test_log_pilot_requested_not_revenue(tmp_path) -> None:
    """pilot_requested ≠ revenue."""
    out = tmp_path / "outcomes.jsonl"
    r = _run([
        "--prospect-handle", "prospect-2",
        "--sector", "agencies",
        "--outcome", "pilot_requested",
        "--next-action", "send pilot brief",
        "--out-path", str(out),
    ])
    assert r.returncode == 0
    rec = json.loads(out.read_text(encoding="utf-8").strip())
    assert rec["is_revenue"] is False


def test_log_paid_requires_evidence(tmp_path) -> None:
    out = tmp_path / "outcomes.jsonl"
    r = _run([
        "--prospect-handle", "prospect-3",
        "--sector", "services",
        "--outcome", "paid",
        "--next-action", "kickoff Sprint",
        "--out-path", str(out),
    ])
    assert r.returncode == 1
    assert "evidence-note" in r.stderr


def test_log_paid_with_evidence(tmp_path) -> None:
    out = tmp_path / "outcomes.jsonl"
    r = _run([
        "--prospect-handle", "prospect-4",
        "--sector", "consulting",
        "--outcome", "paid",
        "--next-action", "kickoff Sprint",
        "--evidence-note", "BANK-TXN-99887 confirmed 2026-05-08",
        "--out-path", str(out),
    ])
    assert r.returncode == 0
    rec = json.loads(out.read_text(encoding="utf-8").strip())
    assert rec["is_revenue"] is True
    assert "BANK-TXN-99887" in rec["evidence_note"]


def test_email_redacted_from_notes(tmp_path) -> None:
    out = tmp_path / "outcomes.jsonl"
    _run([
        "--prospect-handle", "prospect-5",
        "--sector", "training",
        "--outcome", "follow_up",
        "--next-action", "email back at sami@example.com",
        "--notes", "phone +966500000000 too",
        "--out-path", str(out),
    ])
    rec = json.loads(out.read_text(encoding="utf-8").strip())
    blob = json.dumps(rec)
    assert "sami@example.com" not in blob
    assert "+966500000000" not in blob
    assert "[EMAIL]" in blob or "[PHONE]" in blob


def test_invalid_outcome_blocked(tmp_path) -> None:
    out = tmp_path / "outcomes.jsonl"
    r = _run([
        "--prospect-handle", "prospect-6",
        "--sector", "real_estate",
        "--outcome", "made_up_outcome",
        "--next-action", "x",
        "--out-path", str(out),
    ])
    assert r.returncode != 0


def test_invalid_sector_blocked(tmp_path) -> None:
    out = tmp_path / "outcomes.jsonl"
    r = _run([
        "--prospect-handle", "prospect-7",
        "--sector", "spaceship_dealer",
        "--outcome", "interested",
        "--next-action", "x",
        "--out-path", str(out),
    ])
    assert r.returncode == 1


def test_append_only(tmp_path) -> None:
    """Multiple logs all append, none overwrite."""
    out = tmp_path / "outcomes.jsonl"
    for i in range(3):
        _run([
            "--prospect-handle", f"prospect-{i}",
            "--sector", "real_estate",
            "--outcome", "interested",
            "--next-action", "send link",
            "--out-path", str(out),
        ])
    lines = out.read_text(encoding="utf-8").strip().split("\n")
    assert len(lines) == 3


def test_gitignore_includes_demo_outcomes() -> None:
    """The live/ dir is gitignored, so demo_outcomes.jsonl is too."""
    gitignore = Path(".gitignore").read_text(encoding="utf-8")
    assert "docs/wave6/live/" in gitignore
