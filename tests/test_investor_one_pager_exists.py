from pathlib import Path


def test_investor_one_pager_exists():
    p = Path("docs/sales-kit/INVESTOR_ONE_PAGER.md")
    assert p.exists()
    text = p.read_text()
    assert "4,999 SAR/month" in text
    assert "25,000 SAR" in text
    assert "No scraping" in text
    assert "Dealix Promise API" in text
