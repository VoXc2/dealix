from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_public_legal_aliases_converge_on_single_legal_surface() -> None:
    config = (ROOT / "apps/web/next.config.js").read_text(encoding="utf-8")
    for source in ("/privacy", "/terms", "/privacy.html", "/terms.html"):
        needle = f'{{ source: "{source}", destination: "/legal", permanent: true }}'
        assert needle in config


def test_legal_surface_is_discoverable_without_duplicate_notices() -> None:
    sitemap = (ROOT / "apps/web/app/sitemap.ts").read_text(encoding="utf-8")
    assert '{ path: "/legal", priority: 0.84, changeFrequency: "monthly" }' in sitemap
    assert (ROOT / "apps/web/app/legal/page.tsx").is_file()


def test_canary_postgres_failure_emits_bounded_diagnostics() -> None:
    script = (ROOT / "scripts/ops/deploy_selfhosted_canary.sh").read_text(encoding="utf-8")
    for needle in (
        "FAIL: canary postgres readiness timeout",
        "CANARY_POSTGRES_READINESS=PASS",
        "logs --no-color --tail=120 postgres",
        "exit 66",
    ):
        assert needle in script
