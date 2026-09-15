from pathlib import Path


def test_legacy_static_commercial_pages_are_retired() -> None:
    expectations = {
        "ai-team.html": ("/dealix-os", "https://dealix.me/dealix-os"),
        "workflow.html": ("/pricing", "https://dealix.me/pricing"),
        "services.html": ("/services", "https://dealix.me/services"),
        "customer-portal.html": ("/cases", "https://dealix.me/cases"),
    }
    for name, (target, canonical) in expectations.items():
        text = Path("landing", name).read_text(encoding="utf-8")
        assert "DEALIX_RETIRED_PUBLIC_SURFACE" in text
        assert 'name="robots" content="noindex,nofollow"' in text
        assert f'content="0; url={target}"' in text
        assert f'href="{canonical}"' in text


def test_next_redirects_retire_legacy_commercial_urls_at_http_level() -> None:
    text = Path("apps/web/next.config.js").read_text(encoding="utf-8")
    required = {
        '/ai-team.html': '/dealix-os',
        '/workflow.html': '/pricing',
        '/services.html': '/services',
        '/pricing.html': '/pricing',
        '/customer-portal.html': '/cases',
    }
    for source, destination in required.items():
        assert f'{{ source: "{source}", destination: "{destination}", permanent: true }}' in text


def test_retired_pages_do_not_reintroduce_old_fixed_price_or_fixed_agent_claims() -> None:
    chunks = [
        Path("landing", name).read_text(encoding="utf-8")
        for name in ("ai-team.html", "workflow.html", "services.html")
    ]
    text = " ".join(chunks)
    for stale in ("499 SAR", "1,500 SAR", "2,500 SAR", "30-day Revenue Command Pilot", "5 وكلاء AI"):
        assert stale not in text
