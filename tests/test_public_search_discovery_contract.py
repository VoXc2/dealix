from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ROBOTS = ROOT / "apps/web/app/robots.ts"
HOME = ROOT / "apps/web/app/page.tsx"
NEXT_CONFIG = ROOT / "apps/web/next.config.js"
SITEMAP = ROOT / "apps/web/app/sitemap.ts"


def test_chatgpt_search_crawler_is_allowed_without_enabling_training_bot() -> None:
    robots = ROBOTS.read_text(encoding="utf-8-sig")
    assert 'userAgent: "OAI-SearchBot"' in robots
    assert 'userAgent: "GPTBot", disallow: ["/"]' in robots
    assert '"/_next/"' not in robots
    for private_path in ("/control-plane", "/agents", "/approvals", "/sandbox", "/self-evolving", "/api/", "/healthz"):
        assert private_path in robots


def test_public_structured_data_does_not_fallback_to_personal_founder_email() -> None:
    home = HOME.read_text(encoding="utf-8")
    assert "sami.assiri11@gmail.com" not in home
    assert "NEXT_PUBLIC_FOUNDER_EMAIL" not in home
    assert "NEXT_PUBLIC_COMPANY_CONTACT_EMAIL" in home
    assert "companyContactEmail ? { email: companyContactEmail } : {}" in home


def test_legacy_search_and_demo_agent_routes_retire_to_canonical_public_surfaces() -> None:
    config = NEXT_CONFIG.read_text(encoding="utf-8")
    assert '{ source: "/trust-center.html", destination: "/safety", permanent: true }' in config
    assert '{ source: "/agents", destination: "/dealix-os", permanent: true }' in config
    assert '{ source: "/ai-team.html", destination: "/dealix-os", permanent: true }' in config


def test_sitemap_does_not_publish_internal_proof_or_operator_surfaces() -> None:
    sitemap = SITEMAP.read_text(encoding="utf-8")
    for private_path in ("/proof-vault", "/control-plane", "/approvals", "/self-evolving", "/agents"):
        assert private_path not in sitemap
