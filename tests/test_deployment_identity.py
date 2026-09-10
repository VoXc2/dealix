from __future__ import annotations

from core.config.deployment_identity import resolve_deployment_git_sha


def test_vercel_system_sha_overrides_stale_generic_sha() -> None:
    env = {
        "VERCEL_GIT_COMMIT_SHA": "70f060e477471ab2eb927bb34895870854427c70",
        "GIT_SHA": "8099b00",
    }

    assert (
        resolve_deployment_git_sha("8099b00", environ=env)
        == "70f060e477471ab2eb927bb34895870854427c70"
    )


def test_railway_system_sha_overrides_stale_generic_sha() -> None:
    env = {
        "RAILWAY_GIT_COMMIT_SHA": "railway-exact-sha",
        "GIT_SHA": "stale-generic-sha",
    }

    assert (
        resolve_deployment_git_sha("stale-generic-sha", environ=env)
        == "railway-exact-sha"
    )


def test_vercel_identity_wins_if_multiple_platform_markers_exist() -> None:
    env = {
        "VERCEL_GIT_COMMIT_SHA": "vercel-exact-sha",
        "RAILWAY_GIT_COMMIT_SHA": "railway-exact-sha",
    }

    assert resolve_deployment_git_sha(environ=env) == "vercel-exact-sha"


def test_railway_context_without_system_git_sha_fails_closed() -> None:
    env = {
        "RAILWAY_PROJECT_ID": "project-1",
        "RAILWAY_DEPLOYMENT_ID": "deployment-1",
        "GIT_SHA": "8099b00",
    }

    assert resolve_deployment_git_sha("8099b00", environ=env) == "unknown"


def test_vercel_context_without_system_git_sha_fails_closed() -> None:
    env = {
        "VERCEL": "1",
        "VERCEL_ENV": "production",
        "GIT_SHA": "stale-generic-sha",
    }

    assert resolve_deployment_git_sha("stale-generic-sha", environ=env) == "unknown"


def test_configured_sha_remains_valid_for_container_builds() -> None:
    assert resolve_deployment_git_sha("docker-build-sha", environ={}) == "docker-build-sha"


def test_missing_identity_fails_closed_to_unknown() -> None:
    assert resolve_deployment_git_sha("unknown", environ={}) == "unknown"
