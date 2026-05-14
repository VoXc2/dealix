from pathlib import Path


def test_hiring_scorecards_have_no_hire_conditions():
    p = Path("docs/funding/HIRING_SCORECARDS.md")
    assert p.exists()
    text = p.read_text()
    assert "Do Not Hire If" in text
    assert "AI Ops Engineer" in text
    assert "Delivery / RevOps Operator" in text
    assert "Partnerships / GCC Growth Operator" in text
