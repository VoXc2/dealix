from pathlib import Path


def test_funding_pack_has_use_of_funds():
    p = Path("docs/funding/USE_OF_FUNDS.md")
    assert p.exists()
    text = p.read_text()
    assert "Capital must not fund" in text
    assert "premature full SaaS" in text
    assert "faster invoice" in text
