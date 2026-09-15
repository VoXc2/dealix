from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_agents_surface_is_retired_to_public_os() -> None:
    page = (ROOT / "apps/web/app/agents/page.tsx").read_text(encoding="utf-8")
    redirects = (ROOT / "apps/web/next.config.js").read_text(encoding="utf-8")
    assert 'permanentRedirect("/dealix-os")' in page
    assert '{ source: "/ai-team.html", destination: "/dealix-os", permanent: true }' in redirects


def test_self_evolving_demo_proposals_are_production_internal() -> None:
    middleware = (ROOT / "apps/web/middleware.ts").read_text(encoding="utf-8")
    source = (ROOT / "apps/web/app/self-evolving/page.tsx").read_text(encoding="utf-8")
    assert '"/self-evolving"' in middleware
    assert 'prop-001' in source and 'pending_approval' in source


def test_search_render_resources_and_legacy_trust_redirect() -> None:
    robots = (ROOT / "apps/web/app/robots.ts").read_text(encoding="utf-8")
    redirects = (ROOT / "apps/web/next.config.js").read_text(encoding="utf-8")
    assert '"/_next/"' not in robots
    assert '{ source: "/trust-center.html", destination: "/safety", permanent: true }' in redirects
