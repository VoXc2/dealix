#!/usr/bin/env python3
"""Verify Dealix SaaS foundation contracts without external services.

This verifier proves repository-level SaaS foundations only. It deliberately
reports production activation gates separately because secrets, domains,
deployments, migrations, and live smoke evidence cannot be inferred from code.
"""

from __future__ import annotations

import argparse
import ast
import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class Check:
    name: str
    passed: bool
    evidence: str


def _read(root: Path, relative: str) -> str:
    path = root / relative
    source = path.read_text(encoding="utf-8")
    if path.suffix == ".py":
        ast.parse(source)
    return source


def evaluate(root: Path) -> dict[str, object]:
    models = _read(root, "db/models.py")
    subscription_models = _read(root, "db/models_subscription.py")
    auth = _read(root, "api/routers/auth.py")
    main = _read(root, "api/main.py")
    customers_domain = _read(root, "api/routers/domains/customers/__init__.py")
    api_key = _read(root, "api/security/api_key.py")
    onboarding_router = _read(root, "api/routers/onboarding.py")
    onboarding_service = _read(root, "dealix/onboarding/service.py")
    invite_email = _read(root, "core/email/invites.py")
    deploy_identity = _read(root, "core/config/deployment_identity.py")
    health_router = _read(root, "api/routers/health.py")
    platform_meta = _read(root, "api/routers/platform_meta.py")
    signup_page = _read(root, "apps/web/app/signup/page.tsx")
    login_page = _read(root, "apps/web/app/login/page.tsx")
    dashboard_page = _read(root, "apps/web/app/[tenant]/dashboard/page.tsx")
    dashboard_entry = _read(root, "apps/web/app/dashboard/page.tsx")
    pricing_page = _read(root, "apps/web/app/pricing/page.tsx")
    runtime_api = _read(root, "apps/web/lib/runtime-api.ts")
    next_config = _read(root, "apps/web/next.config.js")

    invite_section = onboarding_service.split("async def invite_team_member", 1)[1]
    checks = [
        Check(
            "tenant_model",
            "class TenantRecord" in models and "tenant_id" in models,
            "TenantRecord and tenant-scoped records exist",
        ),
        Check(
            "rbac_and_sessions",
            "class RoleRecord" in models
            and "class RefreshTokenRecord" in models
            and "DEFAULT_TENANT_ROLES" in onboarding_service,
            "RBAC, refresh sessions, and canonical role bootstrap exist",
        ),
        Check(
            "subscription_and_usage",
            all(
                token in subscription_models
                for token in (
                    "class PlanRecord",
                    "class SubscriptionRecord",
                    "class InvoiceRecord",
                    "class UsageRecord",
                )
            ),
            "plans, subscriptions, invoices, and usage metering exist",
        ),
        Check(
            "quote_first_saas_onboarding",
            '@router.post("/signup"' in onboarding_router
            and '@router.get("/plans"' in onboarding_router
            and 'os.getenv("DEALIX_SELF_SERVE_SIGNUP_ENABLED", "false")' in onboarding_router
            and "_require_self_serve_signup_enabled()" in onboarding_router
            and 'source: "/signup"' in next_config
            and 'destination: "/book"' in next_config
            and "لا سعر عام ولا Checkout عام" in pricing_page
            and "Role.TENANT_ADMIN.value" in onboarding_service
            and '"/api/v1/onboarding/",' in api_key
            and "app.include_router(onboarding_router.router)" in main
            and "customer_onboarding_router" not in main
            and "onboarding.router =" not in customers_domain,
            "SaaS tenant provisioning exists behind one canonical router, while unattended public signup stays fail-closed behind quote-first commercial authority",
        ),
        Check(
            "protected_onboarding_operations",
            "current_user=Depends(get_current_user)" in onboarding_router
            and "current_user=Depends(require_tenant_admin)" in onboarding_router,
            "wizard and invitations remain JWT/RBAC protected after API-key bypass",
        ),
        Check(
            "safe_team_invites",
            "UserInviteRecord(" in invite_section
            and "hash_token(invite_token)" in invite_section
            and 'hashed_password=""' not in invite_section
            and "Depends(require_tenant_admin)" in onboarding_router
            and "_VALID_ROLE_NAMES = {role.value for role in Role}" in onboarding_service,
            "single-use hashed invites; tenant-role constrained; no placeholder users",
        ),
        Check(
            "approval_first_invite_delivery",
            'os.getenv("EMAIL_ALLOW_LIVE_SEND", "false")' in invite_email
            and "if not live_invite_email_enabled():" in invite_email
            and "blocked_by_policy=True" in invite_email
            and "send_email: bool = False" in onboarding_router
            and "if not send_email:" in onboarding_router
            and "await send_invite_email(" in onboarding_router
            and "manual_share_required" in onboarding_router,
            "invite email requires per-action approval plus operator policy; manual fallback remains",
        ),
        Check(
            "canonical_legacy_invite",
            "def _install_auth_invite_compatibility()" in onboarding_router
            and 'replaced_paths = {"/invite", "/invite/accept"}' in onboarding_router
            and 'getattr(route_item, "path", None) in replaced_paths' in onboarding_router
            and "auth_module.router.routes = retained_routes" in onboarding_router
            and 'name="legacy_auth_invite_compatibility"' in onboarding_router
            and 'name="legacy_auth_invite_accept_compatibility"' in onboarding_router
            and main.index("    auth,")
            < main.index("from api.routers import onboarding as onboarding_router")
            < main.index('app.include_router(auth.router, prefix="/api/v1")'),
            "both legacy auth invite routes are replaced before router inclusion and delegate to the canonical flow",
        ),
        Check(
            "deployment_identity",
            "VERCEL_GIT_COMMIT_SHA" in deploy_identity
            and "RAILWAY_GIT_COMMIT_SHA" in deploy_identity
            and "GIT_SHA" in deploy_identity
            and "resolve_deployment_git_sha" in health_router
            and "resolve_deployment_git_sha" in platform_meta,
            "health and metadata prefer platform-managed deployment identity",
        ),
        Check(
            "auth_lifecycle",
            all(
                route in auth
                for route in (
                    '@router.post("/login"',
                    '@router.post("/refresh"',
                    '@router.post("/logout"',
                    '@router.post("/mfa/setup"',
                    '@router.post("/password/reset"',
                )
            ),
            "login, token rotation, logout, MFA, and password reset exist",
        ),
        Check(
            "browser_signup_session",
            'apiUrl("/api/v1/onboarding/plans")' in signup_page
            and 'apiUrl("/api/v1/onboarding/signup")' in signup_page
            and 'apiUrl("/api/v1/auth/login")' in signup_page
            and "persistSession(tokens" in signup_page
            and "signup.tenant_slug" in signup_page
            and "const plans = [" not in signup_page,
            "browser signup uses canonical plans, creates the tenant, and establishes the JWT session",
        ),
        Check(
            "browser_refresh_rotation",
            'apiUrl("/api/v1/auth/refresh")' in runtime_api
            and "body: JSON.stringify({ refresh_token: refreshToken })" in runtime_api
            and "persistSession(tokens, user)" in runtime_api
            and "async function rotateSessionSingleFlight()" in runtime_api
            and "refreshInFlight = rotateSession().finally(" in runtime_api
            and "if (firstResponse.status !== 401) return firstResponse;" in runtime_api
            and "const rotatedAccessToken = await rotateSessionSingleFlight()" in runtime_api
            and "withBearer({ ...init, cache: init.cache || \"no-store\" }, rotatedAccessToken)"
            in runtime_api,
            "browser retries one authenticated request after single-flight refresh-token rotation",
        ),
        Check(
            "browser_tenant_isolation",
            'authenticatedFetch("/api/v1/customer/dashboard/")' in dashboard_page
            and 'authenticatedFetch("/api/v1/auth/me")' in dashboard_entry
            and '"x-tenant-id"' not in dashboard_page.lower()
            and '"/api/v1/customer/dashboard/",' in api_key
            and '"/api/v1/customer/",' not in api_key,
            "only the audited dashboard path bypasses the platform key and uses JWT tenant context",
        ),
        Check(
            "frontend_api_boundary",
            "NEXT_PUBLIC_DEALIX_API_BASE" in runtime_api
            and "NEXT_PUBLIC_DEALIX_API_BASE" in next_config
            and 'source: "/api/v1/:path*"' in next_config
            and 'source: "/signup"' in next_config
            and 'destination: "/book"' in next_config
            and "X-API-Key" not in runtime_api
            and "ADMIN_API" not in runtime_api
            and 'apiUrl("/api/v1/auth/login")' in login_page,
            "Next.js uses the canonical API boundary, keeps signup active, and embeds no platform key",
        ),
        Check(
            "audit_and_pdpl",
            "class AuditLogRecord" in models
            and "class ConsentRequestRecord" in models
            and "class SuppressionRecord" in models,
            "audit, consent, and suppression records exist",
        ),
        Check(
            "billing_proof",
            "class PaymentRecord" in models
            and "class ProofReportRecord" in models,
            "payment evidence and customer proof records exist",
        ),
        Check(
            "approval_first_outbound",
            "class OutreachDraftRecord" in models
            and "class OutboundMessageRecord" in models
            and 'default="draft_only"' in models,
            "outbound is modeled through drafts and controlled execution",
        ),
    ]

    passed = all(check.passed for check in checks)
    return {
        "foundation_status": "READY" if passed else "NOT_READY",
        "production_activation_status": "HOLD_PENDING_EXACT_RUNTIME_EVIDENCE",
        "checks": [asdict(check) for check in checks],
        "operator_gates": [
            {
                "gate": "release_identity_parity",
                "action": "prove source SHA -> build identity -> running Web/API SHA on the accepted release",
            },
            {
                "gate": "tenant_database_safety",
                "action": "prove tenant migrations plus backup/restore on a disposable non-production database",
            },
            {
                "gate": "tenant_isolation_runtime",
                "action": "prove same-tenant success and cross-tenant denial on the running release, including connector/secret isolation",
            },
            {
                "gate": "commercial_activation",
                "action": "keep self-serve signup, billing execution, and payment effects disabled until current customer-specific commercial authority explicitly enables them",
            },
        ],
        "claim_boundary": (
            "READY proves repository SaaS foundations and browser journey contracts only; "
            "production-ready requires exact release identity, migration/restore proof, runtime "
            "tenant-isolation evidence, and explicit commercial activation."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    result = evaluate(args.root.resolve())
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"SaaS foundation: {result['foundation_status']}")
        for check in result["checks"]:
            mark = "PASS" if check["passed"] else "FAIL"
            print(f"[{mark}] {check['name']}: {check['evidence']}")
        print(f"Production activation: {result['production_activation_status']}")
        for gate in result["operator_gates"]:
            print(f"- #{gate['issue']}: {gate['action']}")
        print(result["claim_boundary"])

    return 0 if result["foundation_status"] == "READY" else 1


if __name__ == "__main__":
    raise SystemExit(main())
