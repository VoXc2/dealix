"""Release identity contract for the public web health endpoint."""

from pathlib import Path


ROUTE = (
    Path(__file__).resolve().parents[2]
    / "apps"
    / "web"
    / "app"
    / "healthz"
    / "route.ts"
)


def test_healthz_prefers_selfhost_immutable_release_identity_sources() -> None:
    source = ROUTE.read_text(encoding="utf-8")
    ordered = [
        "DEALIX_RELEASE_SHA",
        "NEXT_PUBLIC_GIT_SHA",
        "GIT_SHA",
    ]
    positions = [source.index(name) for name in ordered]
    assert positions == sorted(positions)
    assert "RAILWAY_GIT_COMMIT_SHA" not in source
    assert "VERCEL_GIT_COMMIT_SHA" not in source
    assert "git_sha: gitSha" in source
