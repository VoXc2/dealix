"""Static contracts for the browser-facing SaaS signup and dashboard journey."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def test_signup_loads_canonical_plans_and_establishes_session() -> None:
    source = _read("apps/web/app/signup/page.tsx")

    assert 'apiUrl("/api/v1/onboarding/plans")' in source
    assert 'apiUrl("/api/v1/onboarding/signup")' in source
    assert 'apiUrl("/api/v1/auth/login")' in source
    assert "persistSession(tokens" in source
    assert "signup.tenant_slug" in source
    assert "const plans = [" not in source
    assert 'id: "scale"' not in source
    assert 'price: "199"' not in source
    assert 'price: "599"' not in source


def test_login_and_dashboard_use_canonical_runtime_api() -> None:
    login = _read("apps/web/app/login/page.tsx")
    dashboard = _read("apps/web/app/[tenant]/dashboard/page.tsx")
    entry = _read("apps/web/app/dashboard/page.tsx")

    assert 'apiUrl("/api/v1/auth/login")' in login
    assert "persistSession(data" in login
    assert 'authenticatedFetch("/api/v1/customer/dashboard/")' in dashboard
    assert 'authenticatedFetch("/api/v1/auth/me")' in entry
    assert '"x-tenant-id"' not in dashboard.lower()
    assert "profile.tenant_id" in entry


def test_customer_dashboard_router_is_registered_and_tenant_derived() -> None:
    customer_domain = _read("api/routers/domains/customers/__init__.py")
    customer_dashboard = _read("api/routers/customer/dashboard.py")

    assert (
        "from api.routers.customer import dashboard as customer_dashboard_router"
        in customer_domain
    )
    assert "customer_dashboard_router.router" in customer_domain
    assert 'prefix="/api/v1/customer/dashboard"' in customer_dashboard
    assert '@router.get("/", response_model=DashboardOut)' in customer_dashboard
    assert "current_user: UserRecord = Depends(get_current_user)" in customer_dashboard
    assert "tenant_id = current_user.tenant_id" in customer_dashboard
    assert "UserRecord.tenant_id == tenant_id" in customer_dashboard
    assert "LeadRecord.tenant_id == tenant_id" in customer_dashboard
    assert "DealRecord.tenant_id == tenant_id" in customer_dashboard
    assert "InvoiceRecord.tenant_id == tenant_id" in customer_dashboard
    assert "get_active_subscription_for_tenant(tenant_id)" in customer_dashboard
    assert "plan.name_en if plan else tenant.plan" in customer_dashboard
    assert '"type": "warning"' in customer_dashboard
    assert '"label": "Review invoice"' in customer_dashboard
    assert "TaskRecord.tenant_id" not in customer_dashboard
    assert "X-Tenant-ID" not in customer_dashboard
    assert "Math.random" not in customer_dashboard


def test_invite_delivery_has_a_browser_redemption_route() -> None:
    onboarding = _read("api/routers/onboarding.py")
    accept_page = _read("apps/web/app/accept-invite/page.tsx")

    assert 'web_base_url = os.getenv("DEALIX_WEB_URL", "https://dealix.me")' in onboarding
    assert 'apiUrl("/api/v1/auth/invite/accept")' in accept_page
    assert 'new URLSearchParams(window.location.search).get("token")' in accept_page
    assert 'window.history.replaceState({}, document.title, "/accept-invite")' in accept_page
    assert "persistSession(tokens, { email })" in accept_page
    assert 'router.replace("/dashboard")' in accept_page
    assert "localStorage.setItem" not in accept_page


def test_runtime_helper_rotates_refresh_tokens_single_flight() -> None:
    source = _read("apps/web/lib/runtime-api.ts")

    assert 'apiUrl("/api/v1/auth/refresh")' in source
    assert "body: JSON.stringify({ refresh_token: refreshToken })" in source
    assert "persistSession(tokens, user)" in source
    assert "if (firstResponse.status !== 401) return firstResponse;" in source
    assert "let refreshInFlight: Promise<string | null> | null = null;" in source
    assert "async function rotateSessionSingleFlight()" in source
    assert "refreshInFlight = rotateSession().finally" in source
    assert "const rotatedAccessToken = await rotateSessionSingleFlight()" in source
    assert "clearSession()" in source
    assert "X-API-Key" not in source
    assert "ADMIN_API" not in source


def test_browser_api_calls_stay_same_origin_behind_rewrite() -> None:
    runtime = _read("apps/web/lib/runtime-api.ts")
    config = _read("apps/web/next.config.js")

    assert 'if (typeof window !== "undefined") return normalizedPath;' in runtime
    assert 'source: "/api/v1/:path*"' in config
    assert "destination: `${dealixApiBase}/api/v1/:path*`" in config
    assert "NEXT_PUBLIC_DEALIX_API_BASE" in config
    assert 'source: "/signup"' in config
    assert 'destination: "/book"' in config


def test_runtime_helper_preserves_session_compatibility() -> None:
    source = _read("apps/web/lib/runtime-api.ts")

    assert "NEXT_PUBLIC_DEALIX_API_BASE" in source
    assert "NEXT_PUBLIC_API_URL" in source
    assert "dealix_access_token" in source
    assert "dealix_refresh_token" in source
    assert "JSON.stringify(tokens.access_token)" in source
    assert "JSON.stringify(tokens.refresh_token)" in source


def test_vercel_frontend_contract_is_explicit_and_secret_free() -> None:
    config = json.loads(_read("apps/web/vercel.json"))
    env_example = _read("apps/web/.env.example")

    assert config["framework"] == "nextjs"
    assert "NEXT_PUBLIC_DEALIX_API_BASE=https://api.dealix.me" in env_example
    assert "NEXT_PUBLIC_API_URL=https://api.dealix.me" in env_example
    assert "APP_SECRET_KEY" not in env_example
    assert "ADMIN_API_KEYS" not in env_example
    assert "NEXT_PUBLIC_DEALIX_ADMIN_API_KEY" not in env_example
    assert "API_KEYS=" not in env_example


def test_backend_exposes_only_audited_browser_customer_path() -> None:
    onboarding = _read("api/routers/onboarding.py")
    middleware = _read("api/security/api_key.py")

    assert 'SELF_SERVE_PLAN_SLUGS = ("free", "starter", "growth")' in onboarding
    assert '@router.get("/plans"' in onboarding
    assert '"tenant_slug": result["tenant"].slug' in onboarding
    assert '"/api/v1/customer/dashboard/",' in middleware
    assert '"/api/v1/customer/",' not in middleware
    assert "Do not broaden this to /api/v1/customer/" in middleware
    assert "current_user=Depends(get_current_user)" in onboarding
    assert "current_user=Depends(require_tenant_admin)" in onboarding
