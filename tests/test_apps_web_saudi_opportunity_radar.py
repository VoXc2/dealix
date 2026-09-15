from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RADAR = ROOT / "apps" / "web" / "app" / "saudi-opportunity-radar" / "page.tsx"
SERVICES = ROOT / "apps" / "web" / "app" / "services" / "page.tsx"
SITEMAP = ROOT / "apps" / "web" / "app" / "sitemap.ts"


def test_saudi_opportunity_radar_has_current_authorities_and_sources() -> None:
    text = RADAR.read_text(encoding="utf-8")

    required = {
        "ZATCA": "https://zatca.gov.sa/ar/MediaCenter/News/Pages/Wave25-E-invoicing.aspx",
        "CST": "https://www.cst.gov.sa/knowledge-center/reports/ai-adoption-guide-for-tech-companies",
        "NCA": "https://nca.gov.sa/ar/regulatory-documents/controls-list/ncnicc/",
        "SAMA": "https://sama.gov.sa/en-US/MediaCenter/News/pages/news-1135.aspx",
    }
    for authority, source in required.items():
        assert authority in text
        assert source in text

    assert "187,500" in text
    assert "1 فبراير 2027" in text
    assert "الأبعاد الخمسة" in text
    assert "26 مارس 2026" in text


def test_saudi_opportunity_radar_preserves_truth_and_commercial_boundaries() -> None:
    text = RADAR.read_text(encoding="utf-8")

    assert "Public signal ≠ buyer intent ≠ relationship ≠ consent ≠ pipeline ≠ revenue." in text
    assert "Research ≠ Relationship" in text
    assert "Readiness ≠ Certification" in text
    assert "Diagnostic ≠ Quote" in text
    assert "كل التشخيصات هنا مجانية" in text
    assert "Free Diagnostic — بدون بطاقة" in text
    assert "لا تمثل نفسها كمقدم Open Banking مرخص من SAMA" in text

    forbidden = [
        "guaranteed revenue",
        "guaranteed ROI",
        "SAMA licensed Dealix",
        "fixed public price",
    ]
    lowered = text.lower()
    for claim in forbidden:
        assert claim.lower() not in lowered


def test_saudi_opportunity_radar_is_wired_into_commercial_navigation() -> None:
    services = SERVICES.read_text(encoding="utf-8")
    sitemap = SITEMAP.read_text(encoding="utf-8-sig")

    assert 'href="/saudi-opportunity-radar"' in services
    assert "services_saudi_opportunity_radar" in services
    assert '{ path: "/saudi-opportunity-radar", priority: 0.9, changeFrequency: "weekly" }' in sitemap
    assert 'path: "/proof-vault"' not in sitemap


def test_saudi_opportunity_radar_does_not_link_to_internal_proof_vault() -> None:
    text = RADAR.read_text(encoding="utf-8")
    assert 'href="/proof-vault"' not in text
    assert 'href="/cases"' in text
