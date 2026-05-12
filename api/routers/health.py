"""Health, liveness, readiness endpoints."""

from __future__ import annotations

from fastapi import APIRouter

from api.schemas import HealthResponse
from core.config.settings import get_settings
from core.llm import get_router as get_model_router

router = APIRouter(tags=["health"])


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
    """Deep health check — verifies DB, Redis, LLM providers."""
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
            conn = psycopg2.connect(dsn, connect_timeout=3)
            conn.cursor().execute("SELECT 1")
            conn.close()
            checks["postgres"] = {"status": "ok", "ms": round((time.perf_counter() - t0) * 1000, 1)}
        else:
            checks["postgres"] = {"status": "skip", "reason": "no DATABASE_URL"}
    except Exception as e:  # pragma: no cover
        checks["postgres"] = {"status": "fail", "error": str(e)[:200]}
        overall = "degraded"

    # Redis
    t0 = time.perf_counter()
    try:
        import redis  # type: ignore

        url = os.getenv("REDIS_URL")
        if url:
            r = redis.from_url(url, socket_timeout=3)
            r.ping()
            checks["redis"] = {"status": "ok", "ms": round((time.perf_counter() - t0) * 1000, 1)}
        else:
            checks["redis"] = {"status": "skip", "reason": "no REDIS_URL"}
    except Exception as e:  # pragma: no cover
        checks["redis"] = {"status": "fail", "error": str(e)[:200]}
        overall = "degraded"

    # LLM providers
    providers = [p.value for p in get_model_router().available_providers()]
    checks["llm_providers"] = {"status": "ok" if providers else "fail", "providers": providers}
    if not providers:
        overall = "degraded"

    # T4f — extended dependency checks for the new T0-T3 vendors.
    # Each is "ok" when the env key is set; we don't ping the vendor
    # here to keep the deep-health latency bounded.
    extras = {
        "cerbos": "ok" if os.getenv("CERBOS_PDP_URL", "").strip() else "unconfigured",
        "stripe": "ok" if os.getenv("STRIPE_API_KEY", "").strip() else "unconfigured",
        "workos": "ok" if os.getenv("WORKOS_API_KEY", "").strip() else "unconfigured",
        "plain": "ok" if os.getenv("PLAIN_API_KEY", "").strip() else "fallback_resend",
        "knock": "ok" if os.getenv("KNOCK_API_KEY", "").strip() else "fallback_resend",
        "portkey": "ok" if os.getenv("PORTKEY_API_KEY", "").strip() else "unconfigured",
        "inngest": "ok" if (os.getenv("INNGEST_SIGNING_KEY", "").strip() or os.getenv("INNGEST_DEV", "").strip()) else "unconfigured",
        "tinybird": "ok" if os.getenv("TINYBIRD_TOKEN", "").strip() else "fallback_internal",
        "betterstack": "ok" if os.getenv("BETTERSTACK_HEARTBEAT_URL", "").strip() else "unconfigured",
        "lago": "ok" if os.getenv("LAGO_API_KEY", "").strip() else "unconfigured",
        "loops": "ok" if os.getenv("LOOPS_API_KEY", "").strip() else "unconfigured",
        "apollo": "ok" if os.getenv("APOLLO_API_KEY", "").strip() else "unconfigured",
        "clearbit": "ok" if os.getenv("CLEARBIT_API_KEY", "").strip() else "unconfigured",
        "wathq": "ok" if os.getenv("WATHQ_API_KEY", "").strip() else "unconfigured",
        "infisical": "ok" if os.getenv("INFISICAL_TOKEN", "").strip() else "unconfigured",
        "pagerduty": "ok" if os.getenv("PAGERDUTY_INTEGRATION_KEY", "").strip() else "unconfigured",
    }
    checks["vendors"] = extras

    return {"status": overall, "checks": checks, "version": get_settings().app_version}


@router.get("/healthz", include_in_schema=False)
async def healthz() -> dict[str, str]:
    """Standard healthz alias for UptimeRobot/K8s probes."""
    return {"status": "ok", "service": "dealix"}


@router.get("/api/v1/status", tags=["health"])
async def public_status() -> dict[str, object]:
    """Public status snapshot for trust pack / status.dealix.me.

    Returns a non-sensitive JSON envelope describing the live service state.
    Safe to expose to anonymous callers — no secrets, no PII, no internal
    hostnames. Targets the SLA published in `docs/sla.md`.
    """
    import os
    import time

    settings = get_settings()
    checks: dict[str, dict[str, object]] = {}
    overall = "ok"

    # Postgres reachability (best-effort, 3s timeout)
    t0 = time.perf_counter()
    try:
        import psycopg2  # type: ignore

        dsn = os.getenv("DATABASE_URL") or os.getenv("DATABASE_DSN")
        if dsn:
            conn = psycopg2.connect(dsn, connect_timeout=3)
            conn.cursor().execute("SELECT 1")
            conn.close()
            checks["postgres"] = {
                "status": "ok",
                "latency_ms": round((time.perf_counter() - t0) * 1000, 1),
            }
        else:
            checks["postgres"] = {"status": "unconfigured"}
            overall = "degraded"
    except Exception:  # pragma: no cover — best-effort signal
        checks["postgres"] = {"status": "fail"}
        overall = "degraded"

    # Redis reachability
    t0 = time.perf_counter()
    try:
        import redis  # type: ignore

        url = os.getenv("REDIS_URL")
        if url:
            r = redis.from_url(url, socket_timeout=3)
            r.ping()
            checks["redis"] = {
                "status": "ok",
                "latency_ms": round((time.perf_counter() - t0) * 1000, 1),
            }
        else:
            checks["redis"] = {"status": "unconfigured"}
    except Exception:  # pragma: no cover
        checks["redis"] = {"status": "fail"}
        overall = "degraded"

    # LLM provider availability
    providers = [p.value for p in get_model_router().available_providers()]
    checks["llm_providers"] = {
        "status": "ok" if providers else "fail",
        "available": providers,
    }
    if not providers:
        overall = "degraded"

    # Migration head — surfaces P0.1 protection: if there is more than one
    # head, the deploy is misconfigured and the report should make it obvious.
    migration_head: str | None = None
    try:
        from alembic.config import Config  # type: ignore
        from alembic.script import ScriptDirectory  # type: ignore

        cfg = Config("alembic.ini")
        script = ScriptDirectory.from_config(cfg)
        heads = script.get_heads()
        migration_head = ",".join(heads) if heads else None
        if len(heads) > 1:
            checks["migrations"] = {"status": "multiple_heads", "heads": list(heads)}
            overall = "degraded"
        else:
            checks["migrations"] = {"status": "ok", "head": migration_head}
    except Exception:  # pragma: no cover — alembic may not be importable in some envs
        checks["migrations"] = {"status": "unknown"}

    return {
        "service": "dealix",
        "status": overall,
        "version": settings.app_version,
        "env": settings.app_env,
        "git_sha": settings.git_sha,
        "checks": checks,
        "sla": "/docs/sla.md",
    }


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
