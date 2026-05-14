"""Every entry in `data/group_risk_register.json` has every required field.
The annual report (PR12) and the audit committee depend on the schema
being complete.
"""
from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
REGISTER = REPO_ROOT / "data" / "group_risk_register.json"
DOC = REPO_ROOT / "docs" / "holding" / "GROUP_RISK_REGISTER.md"

REQUIRED = ("id", "category", "risk", "likelihood", "impact", "mitigation", "status", "owner")
VALID_CATEGORIES = {"commercial", "operational", "regulatory", "agentic_ai"}
VALID_LIKELIHOODS = {"low", "med", "high"}
VALID_IMPACTS = {"low", "med", "high", "critical"}
VALID_STATUSES = {"open", "mitigated", "closed"}


def test_register_file_exists_and_doc_exists():
    assert REGISTER.exists()
    assert DOC.exists()


def test_register_has_at_least_top_10_risks():
    data = json.loads(REGISTER.read_text(encoding="utf-8"))
    assert len(data.get("risks") or []) >= 10


def test_every_risk_has_required_fields():
    data = json.loads(REGISTER.read_text(encoding="utf-8"))
    for i, r in enumerate(data.get("risks") or []):
        for key in REQUIRED:
            assert key in r and r[key] is not None and r[key] != "", (
                f"risk[{i}] (id={r.get('id')}) missing/empty: {key}"
            )


def test_categories_are_in_allowed_set():
    data = json.loads(REGISTER.read_text(encoding="utf-8"))
    for r in (data.get("risks") or []):
        assert r["category"] in VALID_CATEGORIES, (
            f"risk id={r['id']} unknown category {r['category']!r}"
        )


def test_likelihood_impact_status_are_in_allowed_sets():
    data = json.loads(REGISTER.read_text(encoding="utf-8"))
    for r in (data.get("risks") or []):
        assert r["likelihood"] in VALID_LIKELIHOODS
        assert r["impact"] in VALID_IMPACTS
        assert r["status"] in VALID_STATUSES


def test_doc_lists_all_four_categories():
    text = DOC.read_text(encoding="utf-8")
    for cat in ("Commercial", "Operational", "Regulatory", "Agentic-AI"):
        assert cat in text, f"GROUP_RISK_REGISTER.md missing category: {cat}"


def test_doc_references_annual_report_section_8():
    text = DOC.read_text(encoding="utf-8")
    assert "annual report" in text.lower()
    assert "Section 8" in text or "section 8" in text


def test_audit_and_compliance_docs_exist():
    """PR15 ships the companion governance docs as a set."""
    assert (REPO_ROOT / "docs" / "holding" / "HOLDING_COMPLIANCE.md").exists()
    assert (REPO_ROOT / "docs" / "holding" / "INTERNAL_AUDIT.md").exists()
    assert (REPO_ROOT / "docs" / "holding" / "BOARD_OF_DIRECTORS.md").exists()
    assert (REPO_ROOT / "docs" / "holding" / "BOARD_CHARTER.md").exists()
    assert (REPO_ROOT / "docs" / "holding" / "HOLDING_INVESTMENT_MEMO.md").exists()
