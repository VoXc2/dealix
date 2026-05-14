from pathlib import Path


def test_gcc_expansion_preserves_saudi_beachhead():
    p = Path("docs/gcc-expansion/GCC_EXPANSION_THESIS.md")
    assert p.exists()
    text = p.read_text()
    assert "Saudi-first commercially" in text
    assert "Saudi Arabia remains the commercial beachhead" in text
    assert "not launching broadly across the GCC before Invoice #1" in text
