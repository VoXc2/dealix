"""
FastAPI application entry point.
نقطة دخول تطبيق FastAPI.
"""

from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from api.middleware import (
    AuditLogMiddleware,
    ETagMiddleware,
    RateLimitHeadersMiddleware,
    RequestIDMiddleware,
    SecurityHeadersMiddleware,
)

# ── Domain router aggregators (replaces 80+ flat imports) ─────────
from api.routers.domains import admin as admin_domain
from api.routers.domains import agents as agents_domain
from api.routers.domains import analytics as analytics_domain
from api.routers.domains import compliance as compliance_domain
from api.routers.domains import customers as customers_domain
from api.routers.domains import deprecated as deprecated_domain
from api.routers.domains import sales as sales_domain
from api.routers.domains import webhooks as webhooks_domain
from api.routers import audit_logs as audit_logs_router
from api.routers import llm_usage as llm_usage_router
from api.routers import whatsapp_admin as whatsapp_admin_router
from api.routers import (
    auth,
    billing,
    customer,
    jobs,
    onboarding,
    partners,
    pdpl,
    sso,
    support,
    trial,
    zatca,
)
# Wave 12.7 — Intelligence Layer + Expansion Engine routers
from api.routers import expansion_engine as expansion_engine_router
from api.routers import intelligence_layer as intelligence_layer_router
# Wave 13 — Full Ops Productization routers
from api.routers import bottleneck_radar as bottleneck_radar_router
from api.routers import business_metrics_board as business_metrics_board_router
from api.routers import customer_success_scores as customer_success_scores_router
from api.routers import deliverables as deliverables_router
from api.routers import integration_capability as integration_capability_router
from api.routers import service_catalog as service_catalog_router
from api.security import APIKeyMiddleware, setup_rate_limit
from core.config.settings import get_settings
from core.errors import AICompanyError
from core.logging import configure_logging, get_logger


def _validate_production_secrets(settings: "Settings") -> None:  # type: ignore[name-defined]
    """
    Fail fast if production is started with insecure defaults.
    يرفض تشغيل الإنتاج بإعدادات غير آمنة.
    """
    if not settings.is_production:
        return
    secret_val = settings.app_secret_key.get_secret_value()
    if secret_val in ("change-me", "CHANGE_ME_to_64_byte_hex", "", "changeme"):
        raise RuntimeError(
            "SECURITY: APP_SECRET_KEY is set to the default placeholder. "
            "Generate a real key: python -c \"import secrets; print(secrets.token_hex(32))\""
        )
    jwt_val = settings.jwt_secret_key.get_secret_value()
    if "change-me" in jwt_val or len(jwt_val) < 32:
        raise RuntimeError(
            "SECURITY: JWT_SECRET_KEY is insecure in production. "
            "Generate a real key: python -c \"import secrets; print(secrets.token_hex(32))\""
        )
    import os
    if not os.getenv("API_KEYS", "").strip():
        raise RuntimeError(
            "SECURITY: API_KEYS is empty in production. "
            "Set a comma-separated list of secret API keys."
        )
    if not os.getenv("ADMIN_API_KEYS", "").strip():
        raise RuntimeError(
            "SECURITY: ADMIN_API_KEYS is empty in production. "
            "Set a comma-separated list of admin API keys for /api/v1/admin/* endpoints."
        )
    if not os.getenv("DATABASE_URL", "").strip() and not os.getenv("DATABASE_DSN", "").strip():
        raise RuntimeError(
            "INFRA: DATABASE_URL (or DATABASE_DSN) is empty in production. "
            "Set a Postgres connection string."
        )
    if not (
        os.getenv("ANTHROPIC_API_KEY", "").strip()
        or os.getenv("OPENAI_API_KEY", "").strip()
    ):
        raise RuntimeError(
            "LLM: at least one of ANTHROPIC_API_KEY or OPENAI_API_KEY must be set in production."
        )


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    """App startup/shutdown hook."""
    configure_logging()
    log = get_logger(__name__)
    settings = get_settings()

    # ── Security: fail fast on insecure production config ───────
    _validate_production_secrets(settings)

    log.info(
        "app_startup",
        app=settings.app_name,
        version=settings.app_version,
        env=settings.app_env,
    )
    # Production observability pre-flight (warn but never fail).
    if settings.is_production:
        import os
        if not os.getenv("SENTRY_DSN", "").strip():
            log.warning(
                "observability_misconfigured",
                missing="SENTRY_DSN",
                impact="production_errors_will_not_be_captured",
            )
    # Auto-create tables ONLY in development/test — in staging/production
    # run `alembic upgrade head` instead (init_db create_all is excluded).
    if settings.app_env in ("development", "test"):
        try:
            from db.session import init_db
            await init_db()
            log.info("db_init_complete")
        except Exception as exc:
            log.warning("db_init_skipped", error=str(exc))
    else:
        log.info("db_init_skipped", reason="use_alembic_migrations")

    # BetterStack heartbeat — runs only when BETTERSTACK_HEARTBEAT_URL is set.
    import asyncio as _asyncio

    from dealix.integrations.betterstack import heartbeat_loop

    heartbeat_stop = _asyncio.Event()
    heartbeat_task = _asyncio.create_task(
        heartbeat_loop(heartbeat_stop), name="betterstack_heartbeat"
    )

    yield

    heartbeat_stop.set()
    try:
        await _asyncio.wait_for(heartbeat_task, timeout=5)
    except _asyncio.TimeoutError:
        heartbeat_task.cancel()
    log.info("app_shutdown")


def create_app() -> FastAPI:
    """FastAPI factory."""
    settings = get_settings()

    _OPENAPI_TAGS = [
        {"name": "Sales", "description": "Lead intake, pipeline, outreach, pricing, revenue."},
        {"name": "Customers", "description": "Customer success, CRM, portals, inbox, support."},
        {"name": "Agents", "description": "LLM gateway, AI workforce, observability, safety, delivery."},
        {"name": "Admin", "description": "Health, config, founder ops, roles, diagnostics."},
        {"name": "Compliance", "description": "PDPL, security, privacy, data quality, reliability."},
        {"name": "Analytics", "description": "Growth, company brain, GTM, market intelligence, radar."},
        {"name": "Webhooks", "description": "Inbound/outbound webhooks — WhatsApp, HubSpot, n8n."},
        {"name": "Deprecated", "description": "Legacy versioned endpoints (v3/v6/v7/v10/v11) — to be removed in v2.0."},
        {"name": "root", "description": "Root discovery endpoint."},
    ]

    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description=(
            "Multi-agent AI platform for the Saudi Arabian market.\n\n"
            "**Phase 8**: Auto Client Acquisition — intake, ICP match, "
            "pain extraction, qualification, CRM sync, booking, proposals.\n\n"
            "**Phase 9**: Autonomous Growth — sector intel, content, distribution, "
            "enrichment, competitor analysis, market research.\n\n"
            "**Phase 10 / v3**: Autonomous Saudi Revenue OS — revenue memory, "
            "safe agent runtime, market radar, compliance OS, revenue science, "
            "and Sami Personal Strategic Operator."
        ),
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        lifespan=lifespan,
        openapi_tags=_OPENAPI_TAGS,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origin_list,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
        allow_headers=["Authorization", "X-API-Key", "X-Request-ID", "Content-Type", "Accept"],
    )
    app.add_middleware(SecurityHeadersMiddleware)
    app.add_middleware(RateLimitHeadersMiddleware)
    app.add_middleware(ETagMiddleware)
    app.add_middleware(AuditLogMiddleware)
    app.add_middleware(RequestIDMiddleware)
    app.add_middleware(APIKeyMiddleware)
    setup_rate_limit(app)

    try:
        from dealix.observability import instrument_fastapi, setup_sentry, setup_tracing

        setup_sentry()
        setup_tracing(service_name=settings.app_name, version=settings.app_version)
        instrument_fastapi(app)
    except Exception:  # pragma: no cover
        pass

    @app.exception_handler(AICompanyError)
    async def ai_company_error_handler(_: Request, exc: AICompanyError) -> JSONResponse:
        return JSONResponse(
            status_code=400,
            content={"error": exc.__class__.__name__, "detail": str(exc)},
        )

    # ── Routers registered by domain (replaces 90 flat app.include_router calls) ─
    _DOMAIN_GROUPS = [
        admin_domain,
        sales_domain,
        customers_domain,
        agents_domain,
        compliance_domain,
        analytics_domain,
        webhooks_domain,
        deprecated_domain,
    ]
    for domain in _DOMAIN_GROUPS:
        for router in domain.get_routers():
            app.include_router(router)

    # ── Enterprise additions ───────────────────────────────────────
    app.include_router(auth.router, prefix="/api/v1")
    app.include_router(jobs.router, prefix="/api/v1")
    app.include_router(zatca.router)
    app.include_router(pdpl.router)
    # Trial + partner-deal capture (self-prefixed). Unblocks GTM motion
    # while Moyasar KYC is pending — see docs/product/CORE_WORKFLOWS.md.
    app.include_router(trial.router)
    app.include_router(partners.router)
    # Customer portal data plane (summary/subscription/invoices/team).
    app.include_router(customer.router)
    # Self-serve onboarding (start/integrations/dpa/finalize).
    app.include_router(onboarding.router)
    # International billing (Stripe). Inert without STRIPE_API_KEY.
    app.include_router(billing.router)
    # Customer-facing audit log + CSV export.
    app.include_router(audit_logs_router.router)
    # Customer support — Plain ticketing with Resend email fallback.
    app.include_router(support.router)
    # Enterprise SSO (WorkOS). 503 sso_disabled without env keys.
    app.include_router(sso.router)
    # WhatsApp template admin (Meta-approved templates).
    app.include_router(whatsapp_admin_router.router)
    # LLM usage / cost dashboard data (per-tenant).
    app.include_router(llm_usage_router.router)

    # ── Wave 12.7 — Intelligence Layer + Expansion Engine ─────────
    # Both routers self-prefix /api/v1/intelligence and /api/v1/expansion-engine.
    app.include_router(intelligence_layer_router.router)
    app.include_router(expansion_engine_router.router)

    # ── Wave 13 — Full Ops Productization ─────────────────────────
    # Self-prefix /api/v1/services. Registry-only; no live actions.
    app.include_router(service_catalog_router.router)
    # Self-prefix /api/v1/deliverables. State-machine-gated.
    app.include_router(deliverables_router.router)
    # Self-prefix /api/v1/customer-success. 5-score read-only.
    app.include_router(customer_success_scores_router.router)
    # Self-prefix /api/v1/bottleneck-radar. Read-only.
    app.include_router(bottleneck_radar_router.router)
    # Self-prefix /api/v1/integrations. Truth registry; no live actions.
    app.include_router(integration_capability_router.router)
    # Self-prefix /api/v1/metrics. Read-only; tenant-isolated for {handle}.
    app.include_router(business_metrics_board_router.router)

    @app.get("/", tags=["root"])
    async def root() -> dict[str, object]:
        return {
            "name": settings.app_name,
            "version": settings.app_version,
            "status": "operational",
            "env": settings.app_env,
            "docs": "/docs",
            "health": "/health",
            "v3_command_center": "/api/v1/v3/command-center/snapshot",
            "personal_operator_daily_brief": "/api/v1/personal-operator/daily-brief",
            "personal_operator_launch_report": "/api/v1/personal-operator/launch-report",
            "business_pricing": "/api/v1/business/pricing",
            "decision_passport_golden_chain": "/api/v1/decision-passport/golden-chain",
            "decision_passport_evidence_levels": "/api/v1/decision-passport/evidence-levels",
            "revenue_os_catalog": "/api/v1/revenue-os/catalog",
        }

    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn

    settings = get_settings()
    uvicorn.run(
        "api.main:app",
        host=settings.app_host,
        port=settings.app_port,
        reload=settings.is_development,
    )
