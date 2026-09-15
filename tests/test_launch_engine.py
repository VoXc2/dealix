"""Tests for the Dealix launch engine (scripts/dealix_launch_engine.py).

Fast unit tests over the pure reporting/verdict helpers — they do NOT run
the full subprocess pipeline (that's an integration concern), so they stay
quick and don't depend on the auth/crypto import chain.

Doctrine-relevant invariants:
- A hard check failure (doctrine/imports) → BLOCKED verdict.
- Only soft (founder) gaps → NEEDS-FOUNDER, never a false "READY".
- The rendered index always carries the bilingual value disclaimer and the
  "no external send / no charge" governance banner.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts import dealix_launch_engine as engine
from scripts.dealix_launch_engine import (
    DISCLAIMER,
    FAIL,
    PASS,
    WARN,
    _csv_rows,
    _verdict,
    render_index,
)


def test_verdict_blocked_on_hard_fail():
    checks = [
        {"name": "Core OS modules import", "status": FAIL, "hard": True},
        {"name": "Launch docs", "status": PASS},
    ]
    verdict, _ = _verdict(checks)
    assert "BLOCKED" in verdict


def test_verdict_needs_founder_on_soft_warn_only():
    checks = [
        {"name": "Doctrine guards (8)", "status": PASS, "hard": True},
        {"name": "Warm contacts loaded", "status": WARN},
    ]
    verdict, _ = _verdict(checks)
    assert "NEEDS-FOUNDER" in verdict


def test_verdict_ready_when_all_green():
    checks = [
        {"name": "Doctrine guards (8)", "status": PASS, "hard": True},
        {"name": "Launch docs", "status": PASS},
    ]
    verdict, _ = _verdict(checks)
    assert "READY" in verdict


def test_non_hard_fail_still_blocks():
    # Any FAIL (even non-hard) must not be reported as launch-ready.
    checks = [{"name": "Frontend build", "status": FAIL}]
    verdict, _ = _verdict(checks)
    assert "BLOCKED" in verdict


def test_render_index_has_disclaimer_and_governance_banner():
    gens = [{"name": "Daily call sheet", "status": PASS, "file": "02_call_sheet.md"}]
    checks = [{"name": "Doctrine guards (8)", "status": PASS, "hard": True, "detail": "9 passed"}]
    md = render_index(Path("/tmp/bundle"), "2026-06-07", gens, checks)
    assert DISCLAIMER in md
    assert "No external send" in md
    assert "Verdict" in md


def test_csv_rows_counts_template(tmp_path):
    csv = tmp_path / "wl.csv"
    csv.write_text(
        "name,role,company,sector,relationship,city,linkedin_url,notes\n"
        "Sami,COO,Acme,b2b_services,warm,Riyadh,,met at LEAP\n"
        ",,,,,,,\n",  # empty template row — must not be counted
        encoding="utf-8",
    )
    assert _csv_rows(csv) == 1


def test_csv_rows_missing_file_is_zero(tmp_path):
    assert _csv_rows(tmp_path / "nope.csv") == 0


def test_canonical_approvals_remove_manual_csv_blocker(monkeypatch):
    monkeypatch.setattr(engine, "_load_canonical_approvals", lambda: [{"company_name": "iMini"}])
    check = engine._relationship_readiness(None)
    assert check["status"] == engine.PASS
    assert "Company OS" in check["detail"]
    assert "CSV" in check["detail"]


def test_no_canonical_relationship_is_hold_not_fake_ready(monkeypatch, tmp_path):
    monkeypatch.setattr(engine, "_load_canonical_approvals", lambda: [])
    check = engine._relationship_readiness(None)
    assert check["status"] == engine.WARN
    assert "HOLD/NO_ELIGIBLE_OUTBOUND" in check["detail"]

    legacy = tmp_path / "warm.csv"
    legacy.write_text(
        "name,role,company,sector,relationship,city,linkedin_url,notes\n"
        "Sami,COO,Acme,b2b,warm,Riyadh,,legacy import\n",
        encoding="utf-8",
    )
    check = engine._relationship_readiness(legacy)
    assert check["status"] == engine.WARN
    assert "import-only" in check["detail"]


def test_warm_csv_default_is_optional_not_template_authority(monkeypatch, tmp_path):
    monkeypatch.setattr(engine, "REPO", tmp_path)
    (tmp_path / "data").mkdir()
    (tmp_path / "data" / "warm_list.csv.template").write_text("name,company\n", encoding="utf-8")
    assert engine._warm_csv(None) is None
