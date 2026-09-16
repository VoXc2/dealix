from __future__ import annotations

from core.config.deployment_identity import resolve_deployment_git_sha


def test_configured_selfhost_sha_is_authoritative() -> None:
    env = {"GIT_SHA": "env-sha", "RAILWAY_GIT_COMMIT_SHA": "legacy", "VERCEL_GIT_COMMIT_SHA": "legacy-v"}
    assert resolve_deployment_git_sha("configured-exact-sha", environ=env) == "configured-exact-sha"


def test_generic_git_sha_is_used_when_configured_value_missing() -> None:
    assert resolve_deployment_git_sha(environ={"GIT_SHA": "selfhost-exact-sha"}) == "selfhost-exact-sha"


def test_retired_provider_identity_cannot_regain_authority() -> None:
    env = {"RAILWAY_GIT_COMMIT_SHA": "railway-exact-sha", "VERCEL_GIT_COMMIT_SHA": "vercel-exact-sha"}
    assert resolve_deployment_git_sha(environ=env) == "unknown"


def test_missing_identity_fails_closed_to_unknown() -> None:
    assert resolve_deployment_git_sha("unknown", environ={}) == "unknown"
