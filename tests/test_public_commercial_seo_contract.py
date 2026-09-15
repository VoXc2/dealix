"""SEO/GEO boundary for Dealix's reviewed public launch surfaces."""

from pathlib import Path

LANDING = Path(__file__).resolve().parents[1] / "landing"
CANONICAL_DOMAIN = "https://dealix.me"
REVIEWED_PATHS = (
    "/",
    "/diagnostic.html",
    "/proof.html",
    "/privacy.html",
    "/terms.html",
)
RETIRED_PUBLIC_PATHS = (
    "/pricing.html",
    "/services.html",
    "/trust-center.html",
    "/annual-pricing.html",
    "/start.html",
    "/sprint-sample.html",
    "/roi.html",
    "/case-study.html",
    "/case-study-pilot-example.html",
    "/compare-gong.html",
    "/compare-hubspot.html",
    "/compare-salesloft.html",
    "/verticals.html",
    "/academy.html",
    "/status.html",
    "/why-saudi-ai.html",
    "/ai-team.html",
    "/styleguide.html",
    "/dealix-beast-power.html",
    "/systems-catalog.html",
    "/agency-partner.html",
    "/partners.html",
)


def _read(name: str) -> str:
    return (LANDING / name).read_text(encoding="utf-8")


def test_robots_points_only_to_canonical_domain_sitemaps() -> None:
    robots = _read("robots.txt")
    assert f"Sitemap: {CANONICAL_DOMAIN}/sitemap.xml" in robots
    assert f"Sitemap: {CANONICAL_DOMAIN}/sitemap_dealix.xml" in robots
    assert "https://dealix.sa/" not in robots
    assert "https://dealix.ai/" not in robots


def test_robots_quarantines_retired_commercial_surfaces() -> None:
    robots = _read("robots.txt")
    for path in RETIRED_PUBLIC_PATHS:
        assert f"Disallow: {path}" in robots, path


def test_both_sitemaps_publish_only_reviewed_dealix_me_paths() -> None:
    expected_urls = {f"{CANONICAL_DOMAIN}{path}" for path in REVIEWED_PATHS}
    for name in ("sitemap.xml", "sitemap_dealix.xml"):
        sitemap = _read(name)
        assert "https://dealix.sa/" not in sitemap
        assert "https://dealix.ai/" not in sitemap
        for url in expected_urls:
            assert f"<loc>{url}</loc>" in sitemap, (name, url)
        for path in RETIRED_PUBLIC_PATHS:
            assert f"<loc>{CANONICAL_DOMAIN}{path}</loc>" not in sitemap, (name, path)


def test_compatibility_sitemap_does_not_reintroduce_alternate_legacy_domains() -> None:
    sitemap = _read("sitemap_dealix.xml")
    assert "hreflang" not in sitemap
    assert "dealix.ai" not in sitemap
    assert "dealix.sa" not in sitemap
