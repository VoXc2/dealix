from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WEB = ROOT / "apps" / "web"


def test_sentry_uses_next15_instrumentation_files() -> None:
    server = (WEB / "instrumentation.ts").read_text(encoding="utf-8")
    client = (WEB / "instrumentation-client.ts").read_text(encoding="utf-8")
    config = (WEB / "next.config.js").read_text(encoding="utf-8")

    assert 'require("@sentry/nextjs/config")' in config
    assert "export async function register()" in server
    assert "Sentry.captureRequestError" in server
    assert "NEXT_RUNTIME" in server
    assert "Sentry.captureRouterTransitionStart" in client
    assert "Sentry.init" in client


def test_legacy_sentry_config_files_are_retired() -> None:
    for name in (
        "sentry.client.config.ts",
        "sentry.server.config.ts",
        "sentry.edge.config.ts",
    ):
        assert not (WEB / name).exists()


def test_global_error_reports_to_sentry() -> None:
    source = (WEB / "app" / "global-error.tsx").read_text(encoding="utf-8")
    assert '"use client"' in source
    assert "Sentry.captureException(error)" in source
    assert "reset" in source
