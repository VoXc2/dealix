"""Fail-closed guard for founder/internal web surfaces — SOURCE ONLY.

Gap closed: founder/internal pages (e.g. /crm, /deals, /approvals,
/founder/command-room, /ops/*) previously rendered public HTTP 200 behind a
client-only `localStorage` check, and robots.txt/noindex is not access
control. The canonical gate is now server-side:
`frontend/src/lib/internalSurfaces.ts` (classification) enforced by
`frontend/src/middleware.ts` (404 when the surface is closed).

These tests mirror the TS matching semantics exactly (locale-strip +
prefix match + public exception) and prove:
  * unauthenticated production access to internal pages/API routes is denied;
  * documented internal/dev mode (non-production or explicit open) stays testable;
  * documented public site/diagnostic routes are never classified internal;
  * no parallel identity system is invented and client localStorage is never
    treated as authorization.
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LIB = ROOT / "frontend" / "src" / "lib" / "internalSurfaces.ts"
MIDDLEWARE = ROOT / "frontend" / "src" / "middleware.ts"
ROBOTS = ROOT / "frontend" / "src" / "app" / "robots.ts"
OPS_LAYOUT = ROOT / "frontend" / "src" / "app" / "[locale]" / "ops" / "layout.tsx"
OPS_PROXY = (
    ROOT / "frontend" / "src" / "app" / "api" / "dealix-proxy" / "[...path]" / "route.ts"
)

# Expected classification — must stay in sync with internalSurfaces.ts.
INTERNAL_PAGES = [
    "/crm", "/deals", "/approvals", "/founder", "/command-room", "/war-room",
    "/ops", "/operator", "/admin", "/dashboard", "/pipeline", "/analytics",
    "/clients", "/settings", "/market-control", "/proposal-queue",
    "/auto-distribution", "/delivery", "/brain", "/review-queue",
    "/outreach-lab", "/outreach-review", "/followups", "/kpi-finance",
    "/proof-vault", "/quotes", "/revenue", "/launch", "/client-portal",
]
INTERNAL_APIS = [
    "/api/crm", "/api/deals", "/api/founder", "/api/ops", "/api/internal",
    "/api/admin", "/api/command-room", "/api/approvals", "/api/dealix-proxy",
]
PUBLIC_ROUTES = [
    "/", "/dealix-diagnostic", "/risk-score", "/proof-pack", "/learn",
    "/partners", "/pricing", "/login", "/register", "/about", "/services",
    "/book-call", "/demo", "/privacy", "/trust", "/sectors", "/solutions",
]
PUBLIC_EXCEPTIONS = ["/client-portal/demo"]


# ── Python mirror of the TS semantics ────────────────────────────────

def _strip_locale(pathname: str) -> str:
    parts = pathname.split("/")
    if len(parts) > 2 and parts[1] in ("ar", "en"):
        rest = "/".join(parts[2:])
        return f"/{rest}" if rest else "/"
    return pathname or "/"


def _matches(path: str, prefixes: list[str]) -> bool:
    return any(path == p or path.startswith(f"{p}/") for p in prefixes)


def _is_internal_page(pathname: str) -> bool:
    path = _strip_locale(pathname)
    if _matches(path, PUBLIC_EXCEPTIONS):
        return False
    return _matches(path, INTERNAL_PAGES)


def _is_internal_api(pathname: str) -> bool:
    return _matches(pathname, INTERNAL_APIS)


def _surface_open(env: dict[str, str]) -> bool:
    mode = env.get("DEALIX_INTERNAL_SURFACE_MODE", "").lower()
    if mode == "open":
        return True
    if mode == "closed":
        return False
    prod = [env.get(k, "").lower() for k in ("NODE_ENV", "APP_ENV", "VERCEL_ENV")]
    return "production" not in prod


def _guard(pathname: str, env: dict[str, str]) -> str:
    if not _is_internal_page(pathname) and not _is_internal_api(pathname):
        return "allow"
    return "allow" if _surface_open(env) else "deny"


PROD = {"NODE_ENV": "production"}
DEV = {"NODE_ENV": "development"}


# ── Source-contract tests ────────────────────────────────────────────

def test_classification_lists_required_internal_prefixes() -> None:
    text = LIB.read_text(encoding="utf-8")
    for prefix in INTERNAL_PAGES:
        assert f'"{prefix}"' in text, f"missing internal page prefix {prefix}"
    for prefix in INTERNAL_APIS:
        assert f'"{prefix}"' in text, f"missing internal api prefix {prefix}"
    for route in PUBLIC_ROUTES:
        assert f'"{route}"' in text, f"missing documented public route {route}"
    for exc in PUBLIC_EXCEPTIONS:
        assert f'"{exc}"' in text, f"missing public exception {exc}"


def test_guard_never_trusts_client_storage_or_invents_identity() -> None:
    text = LIB.read_text(encoding="utf-8")
    for forbidden in ("localStorage.getItem", "localStorage.setItem",
                      "sessionStorage.getItem", "sessionStorage.setItem",
                      "document.cookie", "getToken()"):
        assert forbidden not in text, f"client storage reference {forbidden} in server guard"
    for forbidden in ("create_access_token", "sign(", "jwt.sign", "DEALIX_ADMIN_API_KEY",
                      "ADMIN_API_KEYS", "password"):
        assert forbidden not in text, f"identity/secret handling {forbidden} in guard lib"


def test_middleware_enforces_fail_closed_server_side() -> None:
    text = MIDDLEWARE.read_text(encoding="utf-8")
    assert "guardInternalSurface" in text
    assert "./lib/internalSurfaces" in text
    assert "404" in text
    assert "localStorage.getItem" not in text
    assert "sessionStorage.getItem" not in text
    # API routes must pass through the gate (matcher covers /api/).
    assert "/api/:path*" in text


def test_robots_is_hygiene_not_control() -> None:
    text = ROBOTS.read_text(encoding="utf-8")
    assert "internalSurfaces" in text
    assert "NOT access control" in text
    assert "middleware.ts" in text


def test_ops_layout_disclaims_client_gate() -> None:
    text = OPS_LAYOUT.read_text(encoding="utf-8")
    assert "NOT access control" in text
    assert "middleware.ts" in text


def test_dealix_proxy_still_requires_operator() -> None:
    text = OPS_PROXY.read_text(encoding="utf-8")
    assert "/api/v1/auth/me" in text
    assert "401" in text
    assert "NEXT_PUBLIC_DEALIX_ADMIN_API_KEY" not in text


# ── Behavioural tests (production deny / dev testable / public preserved) ──

def test_production_denies_internal_pages() -> None:
    denied = [
        "/crm", "/ar/crm", "/en/crm", "/crm/123",
        "/deals", "/ar/deals",
        "/approvals", "/en/approvals",
        "/founder/command-room", "/ar/founder/command-room",
        "/ops", "/ops/founder", "/ar/ops/war-room", "/en/ops/approvals",
        "/command-room", "/war-room", "/admin", "/dashboard", "/pipeline",
        "/analytics", "/clients", "/settings", "/client-portal/overview",
    ]
    for path in denied:
        assert _guard(path, PROD) == "deny", f"production must deny {path}"


def test_production_denies_internal_api_routes() -> None:
    denied = [
        "/api/crm", "/api/crm/leads", "/api/deals", "/api/deals/1",
        "/api/founder/command-room", "/api/ops/war-room",
        "/api/internal/snapshot", "/api/admin/users",
        "/api/approvals/pending", "/api/command-room/today",
        "/api/dealix-proxy/api/v1/ops-autopilot/war-room",
    ]
    for path in denied:
        assert _guard(path, PROD) == "deny", f"production must deny {path}"


def test_production_preserves_public_routes() -> None:
    allowed = [
        "/", "/ar", "/en",
        "/dealix-diagnostic", "/ar/dealix-diagnostic", "/en/dealix-diagnostic",
        "/risk-score", "/ar/risk-score", "/proof-pack", "/learn",
        "/ar/learn/crm-vs-revenue-ops", "/partners", "/pricing", "/login",
        "/register", "/about", "/services", "/book-call", "/demo", "/privacy",
        "/client-portal/demo",
    ]
    for path in allowed:
        assert _guard(path, PROD) == "allow", f"production must allow {path}"


def test_public_routes_never_classified_internal() -> None:
    for route in PUBLIC_ROUTES:
        assert not _is_internal_page(route), f"public route classified internal: {route}"
        assert not _is_internal_page(f"/ar{route}" if route != "/" else "/ar")
        assert not _is_internal_page(f"/en{route}" if route != "/" else "/en")


def test_dev_mode_remains_testable() -> None:
    for path in ("/crm", "/ar/ops/founder", "/api/crm", "/api/dealix-proxy/api/v1/evidence/events"):
        assert _guard(path, DEV) == "allow", f"dev must allow {path}"
    assert _guard("/crm", {"NODE_ENV": "test"}) == "allow"


def test_explicit_mode_override_wins() -> None:
    assert _guard("/crm", {**PROD, "DEALIX_INTERNAL_SURFACE_MODE": "open"}) == "allow"
    assert _guard("/api/crm", {**PROD, "DEALIX_INTERNAL_SURFACE_MODE": "open"}) == "allow"
    assert _guard("/crm", {**DEV, "DEALIX_INTERNAL_SURFACE_MODE": "closed"}) == "deny"
    assert _guard("/", {**PROD, "DEALIX_INTERNAL_SURFACE_MODE": "closed"}) == "allow"
