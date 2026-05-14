from pathlib import Path


def test_open_doctrine_exists():
    readme = Path("open-doctrine/README.md")
    eleven = Path("open-doctrine/11_NON_NEGOTIABLES.md")
    mapping = Path("open-doctrine/CONTROL_MAPPING.md")
    for p in (readme, eleven, mapping):
        assert p.exists(), f"missing: {p}"
    text = eleven.read_text()
    assert "Source Passport before AI use" in text
    assert "No scraping" in text
    assert "No cold WhatsApp" in text
    assert "Capital Asset registration before invoice" in text
