from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def _assert_railway_sha_baked(rel: str) -> None:
    source = _read(rel)
    assert "ARG RAILWAY_GIT_COMMIT_SHA=\"\"" in source
    assert "RAILWAY_GIT_COMMIT_SHA=${RAILWAY_GIT_COMMIT_SHA}" in source
    assert "ARG GIT_SHA=unknown" in source


def test_api_runtime_image_bakes_railway_immutable_sha() -> None:
    _assert_railway_sha_baked("Dockerfile")


def test_web_runtime_image_bakes_railway_immutable_sha() -> None:
    _assert_railway_sha_baked("apps/web/Dockerfile")
