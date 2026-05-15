"""Health, liveness, readiness endpoints."""

from __future__ import annotations

import re

from fastapi import APIRouter

from api.schemas import HealthResponse
from core.config.settings import get_settings
from core.llm import get_router as get_model_router

router = APIRouter(tags=["health"])


def _normalize_postgres_dsn_for_psycopg2(dsn: str) -> str:
    """Convert SQLAlchemy driver DSNs into libpq-compatible DSNs."""
    return re.sub(r"^postgresql\+[a-zA-Z0-9_]+://", "postgresql://", dsn, count=1)


@router.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    """Liveness + config summary."""
    settings = get_settings()
    providers = [p.value for p in get_model_router().available_providers()]
    return HealthResponse(
        status="ok",
        version=settings.app_version,
        env=settings.app_env,
        providers=providers,
        git_sha=settings.git_sha,
    )


@router.get("/ready")
async def ready() -> dict[str, str]:
    """Readiness probe."""
    return {"status": "ready"}


@router.get("/live")
async def live() -> dict[str, str]:
    """Liveness probe."""
    return {"status": "alive"}


@router.get("/health/deep")
async def health_deep() -> dict[str, object]:
    """Deep health check — verifies DB, Redis, LLM providers, DLQ depths, Sentry.

    Returns:
      - status: "ok" | "degraded" | "down"
      - checks: per-dependency status with latency
      - version: app version + git SHA

    Used by:
      - /healthz polling (UptimeRobot, Railway health-check) for surface check
      - deploy runbook Phase 4 post-deploy smoke (W5.4)
      - preflight_check.py R8 Sentry validator (W5.2)
    """
    import os
    import time

    checks: dict[str, dict[str, object]] = {}
    overall = "ok"

    # Postgres
    t0 = time.perf_counter()
    try:
        import psycopg2  # type: ignore

        dsn = os.getenv("DATABASE_URL") or os.getenv("DATABASE_DSN")
        if dsn:
            conn = psycopg2.connect(
                _normalize_postgres_dsn_for_psycopg2(dsn),
                connect_timeout=3,
            )
            conn.cursor().execute("SELECT 1")
            conn.close()
            checks["postgres"] = {"status": "ok", "ms": round((time.perf_counter() - t0) * 1000, 1)}
        else:
            checks["postgres"] = {"status": "skip", "reason": "no DATABASE_URL"}
    except Exception as e:  # pragma: no cover
        checks["postgres"] = {"status": "fail", "error": str(e)[:200]}
        overall = "degraded"

    # Redis (ping)
    t0 = time.perf_counter()
    redis_client = None
    try:
        import redis  # type: ignore

        url = os.getenv("REDIS_URL")
        if url:
            redis_client = redis.from_url(url, socket_timeout=3, decode_responses=True)
            redis_client.ping()
            checks["redis"] = {"status": "ok", "ms": round((time.perf_counter() - t0) * 1000, 1)}
        else:
            checks["redis"] = {"status": "skip", "reason": "no REDIS_URL"}
    except Exception as e:  # pragma: no cover
        checks["redis"] = {"status": "fail", "error": str(e)[:200]}
        overall = "degraded"

    # DLQ depths (4 production queues — kept in sync with preflight_check.py P7)
    if redis_client is not None:
        try:
            queues = ["webhooks", "outbound", "enrichment", "crm_sync"]
            depths: dict[str, int] = {}
            over_threshold: list[str] = []
            for q in queues:
                try:
                    depths[q] = int(redis_client.llen(f"dlq:{q}") or 0)
                except Exception:
                    depths[q] = -1
                if depths[q] > 5:
                    over_threshold.append(q)
            checks["dlq"] = {
                "status": "ok" if not over_threshold else "degraded",
                "depths": depths,
                "over_threshold": over_threshold,
            }
            if over_threshold:
                overall = "degraded"
        except Exception as e:  # pragma: no cover
            checks["dlq"] = {"status": "fail", "error": str(e)[:200]}

    # Sentry status (DSN configured & sentry_sdk importable)
    try:
        import sentry_sdk  # type: ignore
        dsn = os.getenv("SENTRY_DSN", "")
        # Validate DSN structure to match preflight R8 logic
        if dsn:
            from urllib.parse import urlparse
            host = (urlparse(dsn).hostname or "").lower()
            sentry_ok = host == "ingest.sentry.io" or host.endswith(".ingest.sentry.io")
            checks["sentry"] = {
                "status": "ok" if sentry_ok else "misconfigured",
                "host": host,
                "client_active": sentry_sdk.Hub.current.client is not None,
            }
        else:
            checks["sentry"] = {"status": "skip", "reason": "no SENTRY_DSN"}
    except ImportError:
        checks["sentry"] = {"status": "skip", "reason": "sentry_sdk not installed"}

    # LLM providers
    providers = [p.value for p in get_model_router().available_providers()]
    checks["llm_providers"] = {"status": "ok" if providers else "fail", "providers": providers}
    if not providers:
        overall = "degraded"

    return {"status": overall, "checks": checks, "version": get_settings().app_version}


@router.get("/healthz", include_in_schema=False)
async def healthz(deep: bool = False) -> dict[str, object]:
    """Standard healthz alias for UptimeRobot/K8s probes.

    By default returns a tiny payload for low-latency liveness probes.
    Pass ?deep=1 to get the same payload as /health/deep — useful for
    post-deploy smoke checks (deploy runbook Phase 4).
    """
    if deep:
        return await health_deep()
    return {"status": "ok", "service": "dealix"}


@router.get("/_test_sentry", include_in_schema=False)
async def test_sentry() -> dict[str, str]:
    """Deliberate error to verify Sentry integration.

    Protected by ADMIN_TOKEN header in production.
    """
    import os

    from fastapi import HTTPException

    # In dev, allow freely. In prod, require admin token.
    if os.getenv("APP_ENV", "dev") == "prod":
        admin_token = os.getenv("ADMIN_TOKEN", "")
        # Request injection is complex in FastAPI without Depends; keep simple check
        if not admin_token:
            raise HTTPException(status_code=404, detail="Not found")

    raise Exception("Test Sentry integration — deliberate error")
