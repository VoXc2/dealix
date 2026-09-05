"""Tests for the Unified Command Room (scripts/dealix_unified_command_room.py).

Guards the doctrine: read-only, stdlib-only, never sends; and the operational
promise: every panel degrades gracefully when its source is missing. The
founder-facing commercial path must remain quote-only and free of retired fixed
price authority.
"""
from __future__ import annotations

import importlib.util
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "dealix_unified_command_room.py"


def _load_module():
    spec = importlib.util.spec_from_file_location("dealix_unified_command_room", SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_builds_with_no_sources(tmp_path: Path) -> None:
    """With no outreach log and no CRM, the room still renders valid HTML."""
    mod = _load_module()
    out = tmp_path / "index.html"
    doc = mod.build(
        log=tmp_path / "missing.csv",       # falls back to the tracked template
        crm_path=tmp_path / "missing_crm.csv",
        out=out,
        write=True,
    )
    assert out.exists()
    assert doc.lstrip().startswith("<!DOCTYPE html>")
    assert "غرفة القيادة الموحّدة" in doc
    # All major panels present even on empty inputs.
    for marker in ("Funnel", "Pipeline by stage", "Follow-ups due", "Commercial path", "Article 13"):
        assert marker in doc


def test_commercial_path_is_quote_only_and_contains_no_retired_price_ladder() -> None:
    mod = _load_module()
    rendered = repr(mod.OFFER_LADDER)
    assert len(mod.OFFER_LADDER) == 6
    assert "Customer-Specific Quote" in rendered
    assert "Revenue Command Pilot" in rendered
    assert "Invoice ≠ Payment" in rendered
    for retired in (
        "Micro Sprint",
        "Data Pack",
        "Managed Ops",
        "Transformation Diagnostic Sprint",
        "Custom Enterprise System",
        "499 SAR",
        "1,500 SAR",
        "2,999",
        "4,999",
        "7,500",
        "25,000",
        "100,000",
    ):
        assert retired not in rendered


def test_crm_summary_keeps_won_separate_from_verified_paid() -> None:
    mod = _load_module()
    rows = [
        {"company": "A", "status": "needs_review", "deal_value_sar": "10000", "probability": "20"},
        {"company": "B", "status": "won", "deal_value_sar": "12500", "probability": "100"},
        {"company": "C", "status": "lost", "deal_value_sar": "5000", "probability": "0"},
        {"company": "D", "status": "replied", "deal_value_sar": "8000", "probability": "50"},
        {
            "company": "E",
            "status": "won",
            "deal_value_sar": "4000",
            "probability": "100",
            "payment_status": "verified",
            "payment_evidence_id": "pay_receipt_123",
        },
    ]
    summary = mod.crm_summary(rows)
    assert summary["won"] == 2
    assert summary["paid"] == 1
    assert summary["total"] == 5
    # Open pipeline excludes won + lost: 10000 + 8000.
    assert summary["pipeline_value"] == 18000
    # Weighted: 10000*0.2 + 8000*0.5 = 2000 + 4000.
    assert summary["weighted_value"] == 6000


def test_followups_due_and_priority(tmp_path: Path) -> None:
    mod = _load_module()
    rows = [
        {"company": "Past", "status": "replied", "next_followup_date": "2020-01-01",
         "deal_value_sar": "5000", "probability": "40"},
        {"company": "Future", "status": "replied", "next_followup_date": "2999-01-01",
         "deal_value_sar": "9000", "probability": "80"},
        {"company": "Won", "status": "won", "next_followup_date": "2020-01-01",
         "deal_value_sar": "1000", "probability": "100"},
    ]
    due = mod.followups_due(rows, today="2026-06-28")
    due_names = {r["company"] for r in due}
    assert "Past" in due_names          # overdue, still open
    assert "Future" not in due_names    # not due yet
    assert "Won" not in due_names       # closed, excluded

    top = mod.priority_actions(rows, limit=1)
    assert top and top[0]["company"] == "Future"  # highest weighted open value


def test_doctrine_no_send_stdlib_only() -> None:
    """The script must not contain any send/network surface."""
    src = SCRIPT.read_text(encoding="utf-8")
    banned = ("import requests", "import urllib.request", "urlopen", "httpx",
              "smtplib", "twilio", "green-api", ".send(", "def send")
    for token in banned:
        assert token not in src, f"doctrine violation: {token!r} found in command room"
