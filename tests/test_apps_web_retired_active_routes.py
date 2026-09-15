from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_retired_active_routes_redirect_at_page_level() -> None:
    expected = {
        "apps/web/app/landing/page.tsx": 'permanentRedirect("/")',
        "apps/web/app/value-engine/page.tsx": 'permanentRedirect("/cases")',
        "apps/web/app/signup/page.tsx": 'permanentRedirect("/book")',
    }
    for path, redirect in expected.items():
        text = _read(path)
        assert redirect in text
        for stale in ("299", "799", "شهر كامل", "12000", "15600", "ZATCA جاهز", "PDPL أص"):
            assert stale not in text


def test_retired_active_routes_have_http_level_redirects() -> None:
    config = _read("apps/web/next.config.js")
    required = {
        "/landing": "/",
        "/value-engine": "/cases",
        "/signup": "/book",
    }
    for source, destination in required.items():
        rule = f'{{ source: "{source}", destination: "{destination}", permanent: true }}'
        assert rule in config
