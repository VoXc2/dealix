"""Wave 19 Recovery — P0 commercial motion marker tests.

These tests enforce that the founder-completion artifacts described in the
Wave 19 Recovery sprint are present on disk. They do NOT claim outreach was
sent or invoice issued — only that the runbooks, logs, and markers exist.
Honest counts inside the JSON logs are checked separately.
"""

import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent


def test_investor_one_pager_exists():
    p = REPO_ROOT / "docs/sales-kit/INVESTOR_ONE_PAGER.md"
    assert p.exists(), "Investor one-pager missing under docs/sales-kit/"
    text = p.read_text(encoding="utf-8")
    assert "4,999 SAR/month" in text
    assert "25,000 SAR" in text
    assert "No scraping" in text
    assert "Dealix Promise API" in text


def test_founder_command_center_status_marker_exists():
    p = REPO_ROOT / "data/founder_command_center_status.json"
    assert p.exists(), "Founder Command Center deploy marker missing"
    data = json.loads(p.read_text(encoding="utf-8"))
    assert data["deployment_marker"] is True
    assert "Partner Motion" in data["required_cards"]
    assert "Invoice #1" in data["required_cards"]


def test_anchor_partner_outreach_doc_exists():
    p = REPO_ROOT / "docs/sales-kit/ANCHOR_PARTNER_OUTREACH.md"
    assert p.exists()
    text = p.read_text(encoding="utf-8")
    assert "English Draft" in text
    assert "Arabic Draft" in text
    assert "Governed AI operations" in text


def test_anchor_partner_pipeline_exists():
    p = REPO_ROOT / "data/anchor_partner_pipeline.json"
    assert p.exists()
    data = json.loads(p.read_text(encoding="utf-8"))
    archetypes = {a["archetype"] for a in data["partner_archetypes"]}
    assert "Big 4 / Assurance Partner" in archetypes
    assert "SAMA / Regulated Technology Processor" in archetypes


def test_partner_outreach_log_starts_honest():
    p = REPO_ROOT / "data/partner_outreach_log.json"
    assert p.exists()
    data = json.loads(p.read_text(encoding="utf-8"))
    # Honest baseline: no outreach claimed until one is actually sent.
    assert data["outreach_sent_count"] == len(data["entries"])
    if data["outreach_sent_count"] == 0:
        assert data["ceo_complete"] is False


def test_first_invoice_unlock_runbook_exists():
    p = REPO_ROOT / "docs/ops/FIRST_INVOICE_UNLOCK.md"
    assert p.exists()
    text = p.read_text(encoding="utf-8")
    assert "Register a Capital Asset" in text
    assert "No celebration tweets" in text
    assert "Proof Pack" in text


def test_first_invoice_log_starts_honest():
    p = REPO_ROOT / "data/first_invoice_log.json"
    assert p.exists()
    data = json.loads(p.read_text(encoding="utf-8"))
    assert data["invoice_sent_count"] == len(data["entries"])
    assert data["invoice_paid_count"] <= data["invoice_sent_count"]
    if data["invoice_sent_count"] == 0:
        assert data["ceo_complete"] is False
