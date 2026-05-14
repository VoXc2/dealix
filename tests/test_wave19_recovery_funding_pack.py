"""Wave 19 Recovery — Funding Pack tests.

Verify that funding-readiness artifacts exist and encode the discipline
that Dealix uses capital to accelerate proof, not to substitute it.
"""

from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent


def test_funding_pack_has_use_of_funds():
    p = REPO_ROOT / "docs/funding/USE_OF_FUNDS.md"
    assert p.exists()
    text = p.read_text(encoding="utf-8")
    assert "Capital must not fund" in text
    assert "premature full SaaS" in text
    assert "faster invoice" in text


def test_hiring_scorecards_have_no_hire_conditions():
    p = REPO_ROOT / "docs/funding/HIRING_SCORECARDS.md"
    assert p.exists()
    text = p.read_text(encoding="utf-8")
    assert "Do Not Hire If" in text
    assert "AI Ops Engineer" in text
    assert "Delivery / RevOps Operator" in text
    assert "Partnerships / GCC Growth Operator" in text


def test_first_3_hires_gates_exist():
    p = REPO_ROOT / "docs/funding/FIRST_3_HIRES.md"
    assert p.exists()
    text = p.read_text(encoding="utf-8")
    assert "Anti-Patterns" in text
    assert "Invoice #1 delivered" in text


def test_funding_memo_and_investor_qa_exist():
    memo = REPO_ROOT / "docs/funding/FUNDING_MEMO.md"
    qa = REPO_ROOT / "docs/funding/INVESTOR_QA.md"
    assert memo.exists()
    assert qa.exists()
    assert "proof before capital" in memo.read_text(encoding="utf-8").lower()
    assert "4,999 SAR/month" in qa.read_text(encoding="utf-8")
