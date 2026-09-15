"""Static contracts for the SaaS onboarding security boundary."""

from __future__ import annotations

import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SERVICE_PATH = ROOT / "dealix" / "onboarding" / "service.py"
ROUTER_PATH = ROOT / "api" / "routers" / "onboarding.py"
INVITE_EMAIL_PATH = ROOT / "core" / "email" / "invites.py"
API_KEY_PATH = ROOT / "api" / "security" / "api_key.py"
MAIN_PATH = ROOT / "api" / "main.py"
CUSTOMERS_DOMAIN_PATH = ROOT / "api" / "routers" / "domains" / "customers" / "__init__.py"


def _source(path: Path) -> str:
    source = path.read_text(encoding="utf-8")
    ast.parse(source)
    return source


def test_signup_uses_canonical_tenant_roles() -> None:
    source = _source(SERVICE_PATH)

    assert "DEFAULT_TENANT_ROLES" in source
    assert "Role.TENANT_ADMIN.value" in source
    assert 'name="owner"' not in source
    assert 'permissions=["*:*"]' not in source


def test_team_invite_uses_single_use_invite_record() -> None:
    source = _source(SERVICE_PATH)

    assert "UserInviteRecord(" in source
    assert "create_invite_token(" in source
    assert "hash_token(invite_token)" in source
    assert "token_expires_at(invite_token)" in source
    assert 'hashed_password=""' not in source
    assert "UserRecord(" not in source.split("async def invite_team_member", 1)[1]


def test_team_invite_restricts_roles_to_tenant_rbac() -> None:
    source = _source(SERVICE_PATH)

    assert "_VALID_ROLE_NAMES = {role.value for role in Role}" in source
    assert "if role_name not in _VALID_ROLE_NAMES:" in source
    assert "RoleRecord.tenant_id == tenant_id" in source
    assert "RoleRecord.name == role_name" in source


def test_team_invite_is_admin_gated_and_has_manual_recovery() -> None:
    source = _source(ROUTER_PATH)

    assert "Depends(require_tenant_admin)" in source
    assert "await session.commit()" in source
    assert "send_email: bool = False" in source
    assert "if not send_email:" in source
    assert "await send_invite_email(" in source
    assert "manual_share_required" in source
    assert "delivery_failed_manual_share_required" in source
    assert "Nothing was sent." in source
    assert "لم يتم إرسال أي رسالة" in source


def test_self_serve_onboarding_is_explicitly_gated_and_jwt_guards_remain() -> None:
    middleware = _source(API_KEY_PATH)
    router_source = _source(ROUTER_PATH)

    assert '"/api/v1/onboarding/",' in middleware
    assert "path.startswith(PUBLIC_PREFIXES)" in middleware
    assert "SELF_SERVE_PUBLIC_SIGNUP_AUTHORITY = False" in router_source
    assert 'os.getenv("DEALIX_SELF_SERVE_SIGNUP_ENABLED", "false")' in router_source
    assert "return SELF_SERVE_PUBLIC_SIGNUP_AUTHORITY and requested" in router_source
    assert "def _require_self_serve_signup_enabled()" in router_source
    plans_section = router_source.split('@router.get("/plans"', 1)[1].split(
        '@router.post("/signup"', 1
    )[0]
    signup_section = router_source.split('@router.post("/signup"', 1)[1].split(
        '@router.post("/wizard")', 1
    )[0]
    assert "_require_self_serve_signup_enabled()" in plans_section
    assert "_require_self_serve_signup_enabled()" in signup_section
    assert "Depends(get_current_user)" not in signup_section
    assert "Depends(require_tenant_admin)" not in signup_section
    assert "current_user=Depends(get_current_user)" in router_source
    assert "current_user=Depends(require_tenant_admin)" in router_source



def test_quote_first_runtime_has_one_canonical_onboarding_router() -> None:
    main = _source(MAIN_PATH)
    customers_domain = _source(CUSTOMERS_DOMAIN_PATH)

    assert "app.include_router(onboarding_router.router)" in main
    assert "customer_onboarding_router" not in main
    assert "_LEGACY_SELF_SERVE_ONBOARDING_PATHS" not in customers_domain
    assert "onboarding.router =" not in customers_domain

def test_legacy_auth_invite_routes_are_replaced_by_canonical_safe_flow() -> None:
    source = _source(ROUTER_PATH)
    main = _source(MAIN_PATH)

    # Import order must remain auth first, onboarding second, app inclusion last.
    assert main.index("    auth,") < main.index("from api.routers import onboarding as onboarding_router")
    assert main.index("from api.routers import onboarding as onboarding_router") < main.index(
        'app.include_router(auth.router, prefix="/api/v1")'
    )
    assert "def _install_auth_invite_compatibility()" in source
    assert 'replaced_paths = {"/invite", "/invite/accept"}' in source
    assert "auth_module.router.routes = retained_routes" in source
    assert "legacy_auth_invite" in source
    assert "legacy_auth_invite_accept" in source
    assert 'name="legacy_auth_invite_compatibility"' in source
    assert 'name="legacy_auth_invite_accept_compatibility"' in source
    assert "return await _create_invite_response(" in source


def test_invite_acceptance_uses_persisted_role_and_row_lock() -> None:
    source = _source(ROUTER_PATH)
    accept_section = source.split("async def legacy_auth_invite_accept", 1)[1].split(
        "def _install_auth_invite_compatibility", 1
    )[0]

    assert ".with_for_update()" in accept_section
    assert "UserInviteRecord.token_hash == hash_token(req.token)" in accept_section
    assert "UserInviteRecord.accepted_at.is_(None)" in accept_section
    assert "UserInviteRecord.expires_at > auth_module._utcnow()" in accept_section
    assert "invite.role_id != token_role_id" in accept_section
    assert "RoleRecord.id == invite.role_id" in accept_section
    assert "RoleRecord.tenant_id == tenant_id" in accept_section
    assert "role_id=invite.role_id" in accept_section
    assert "invite.accepted_at = auth_module._utcnow()" in accept_section
    assert "role_id=token_role_id" not in accept_section


def test_invite_email_transport_is_fail_closed_by_default() -> None:
    source = _source(INVITE_EMAIL_PATH)

    assert 'os.getenv("EMAIL_ALLOW_LIVE_SEND", "false")' in source
    assert "if not live_invite_email_enabled():" in source
    blocked_section = source.split("if not live_invite_email_enabled():", 1)[1].split(
        "try:", 1
    )[0]
    assert "EmailClient" not in blocked_section
    assert "blocked_by_policy=True" in blocked_section
    assert "recipient_domain=" in blocked_section
    assert 'logger.info("invite_email_blocked_by_policy"' not in source


def test_signup_response_matches_current_verification_contract() -> None:
    service = _source(SERVICE_PATH)
    router_source = _source(ROUTER_PATH)

    assert "is_verified=True" in service
    assert '"requires_email_verification": False' in service
    assert '"requires_email_verification": result["requires_email_verification"]' in router_source
