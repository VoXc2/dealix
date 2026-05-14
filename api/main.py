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
from api.routers import (
    admin_tenants,
    auth,
    compliance_status,
    cost_tracking,
    customer_usage,
    customer_webhooks,
    enterprise_pmo,
    jobs,
    nps,
    pdpl,
    pdpl_dsar,
    referral_program,
    revenue_metrics,
    saudi_prospect_search,
    sector_intel,
    service_setup,
    tenant_theming,
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
# Wave 14 — Canonical Trust MVP + Retainer Engine (Phase 2)
from api.routers import friction_log as friction_log_router
from api.routers import value_os as value_os_router
# 90-day commercial activation — Wave 14B
from api.routers import data_os as data_os_router
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
    yield
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
    # Wave 7 W7.5 — Tenant theming: GET tenant theme.css + POST admin theme update
    app.include_router(tenant_theming.router)
    # Wave 7 W7.2 — Sector Intelligence (R4 productization)
    app.include_router(sector_intel.router)
    # Wave 7 W7.3 — Admin tenants: CRUD for tenant management (R6 enabler)
    app.include_router(admin_tenants.router)
    # Wave 8 W8.1 — Bespoke AI Service Setup intake (R5 productization)
    app.include_router(service_setup.router)
    # Wave 8 W8.3 — Customer-facing usage dashboard
    app.include_router(customer_usage.router)
    # Wave 9 W9.1 — Enterprise PMO (R7 productization)
    app.include_router(enterprise_pmo.router)
    # Wave 9 W9.6 — Live compliance status (PDPL+ZATCA posture, public read-only)
    app.include_router(compliance_status.router)
    # Wave 9 W9.8 — Saudi B2B prospect search (read-only public + PDPL-safe view)
    app.include_router(saudi_prospect_search.router)
    # Wave 9 W9.9 — PDPL DSAR (data subject access/rectify/port/erase)
    app.include_router(pdpl_dsar.router)
    # Wave 11 W11.2 — Cost tracking (per-tier + admin summary)
    app.include_router(cost_tracking.router)
    # Wave 12 W12.1 — Customer-side webhook subscriptions (Dealix→customer)
    app.include_router(customer_webhooks.router)
    # Wave 13 W13.7 — Revenue metrics dashboard (MRR/ARR/NRR/churn/cohort)
    app.include_router(revenue_metrics.router)
    # Wave 13 W13.13 — Customer referral program (5K SAR per closed deal)
    app.include_router(referral_program.router)
    # Wave 13 W13.4 — NPS survey + detractor intervention
    app.include_router(nps.router)
    # Wave 14 — Canonical Trust MVP + Retainer Engine (Phase 2)
    app.include_router(friction_log_router.router)
    app.include_router(value_os_router.router)
    # Wave 14B — Commercial activation: CSV upload for the Data Pack offer
    app.include_router(data_os_router.router)

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
