from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def _assert_selfhost_sha_only(rel: str) -> None:
    source = _read(rel)
    assert "ARG GIT_SHA=unknown" in source
    assert "RAILWAY_GIT_COMMIT_SHA" not in source
    assert "VERCEL_GIT_COMMIT_SHA" not in source


def test_api_runtime_image_bakes_selfhost_exact_sha_only() -> None:
    _assert_selfhost_sha_only("Dockerfile")


def test_web_runtime_image_bakes_selfhost_exact_sha_only() -> None:
    _assert_selfhost_sha_only("apps/web/Dockerfile")
