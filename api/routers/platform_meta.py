"""Public platform metadata, Railway health probes, and GTM surface registry.

This router is imported early in api.main. Keep these probes dependency-light
so Railway can safely determine whether the API is alive even if optional routers,
database integrations, or third-party providers are degraded.
"""

from __future__ import annotations

from fastapi import APIRouter

from core.config.deployment_identity import resolve_deployment_git_sha
from core.config.settings import get_settings
from dealix.commercial_ops.gtm_public_surfaces import build_gtm_public_surfaces_snapshot

router = APIRouter(tags=["platform"])


def _deployment_git_sha() -> str:
    settings = get_settings()
    return resolve_deployment_git_sha(settings.git_sha)


@router.get("/health", include_in_schema=False)
async def health() -> dict[str, object]:
    """Fast public liveness endpoint for Railway, UptimeRobot, and smoke tests."""
    settings = get_settings()
    return {
        "status": "ok",
        "service": "dealix-api",
        "version": settings.app_version,
        "env": settings.app_env,
        "git_sha": _deployment_git_sha(),
    }


@router.get("/healthz", include_in_schema=False)
async def healthz(deep: bool = False) -> dict[str, object]:
    """Standard Railway/Kubernetes-compatible health alias.

    By default returns a tiny low-latency payload for liveness probes.
    Pass ?deep=1 to get the full dependency-check payload (same shape as
    /health/deep) — used by post-deploy smoke checks.
    """
    if deep:
        from api.routers.health import health_deep

        return await health_deep()
    # Minimal liveness payload — version/identity live at /version (see
    # test_health_deep::test_healthz_default_is_simple, which pins this shape).
    return {"status": "ok", "service": "dealix"}


@router.get("/ready", include_in_schema=False)
async def ready() -> dict[str, str]:
    """Dependency-light readiness probe."""
    return {"status": "ready"}


@router.get("/live", include_in_schema=False)
async def live() -> dict[str, str]:
    """Dependency-light liveness probe."""
    return {"status": "alive"}


@router.get("/version")
async def version() -> dict[str, object]:
    """Deploy identity for probes, partners, and status pages."""
    settings = get_settings()
    return {
        "service": "dealix-api",
        "status": "ok",
        "version": settings.app_version,
        "env": settings.app_env,
        "git_sha": _deployment_git_sha(),
        "health": "/healthz",
        "docs": "/docs" if settings.app_env != "production" else None,
        "meta": "/api/v1/meta",
    }


@router.get("/api/v1/meta")
async def platform_meta() -> dict[str, object]:
    """GTM trust layer: surfaces registry + canonical links."""
    settings = get_settings()
    surfaces = build_gtm_public_surfaces_snapshot()
    return {
        "service": settings.app_name,
        "version": settings.app_version,
        "env": settings.app_env,
        "git_sha": _deployment_git_sha(),
        "surfaces": surfaces,
        "canonical_links": {
            "healthz": "/healthz",
            "health": "/health",
            "ready": "/ready",
            "live": "/live",
            "openapi": "/openapi.json" if settings.app_env != "production" else None,
            "commercial_map": "/api/v1/commercial-map",
            "revenue_os_catalog": "/api/v1/revenue-os/catalog",
        },
    }
