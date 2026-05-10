"""Wave 12.6 §33.2.6 — Tenant isolation tests.

Validates the OWASP API1:2023 BOLA defense:
- resolve_tenant_context: 5 priority levels (test override → JWT →
  header → API key prefix → subdomain), no-tenant → raise
- assert_tenant_match: blocks cross-tenant access, allows super_admin
- filter_tenant_scoped_list: defensive list filter

Pure-function tests. Loaded via importlib to bypass api/security
init cascade (sandbox python-jose issue per Wave 11 §31).
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

# Bypass api/security/__init__.py and api/middleware/__init__.py
# (the latter has no eager imports, but for parity with ssrf_guard
# we load directly).
_REPO_ROOT = Path(__file__).resolve().parents[1]
_TENANT_PATH = _REPO_ROOT / "api" / "middleware" / "tenant_isolation.py"
_spec = importlib.util.spec_from_file_location("tenant_isolation", _TENANT_PATH)
_tenant = importlib.util.module_from_spec(_spec)
sys.modules["tenant_isolation"] = _tenant
_spec.loader.exec_module(_tenant)

CrossTenantAccessDenied = _tenant.CrossTenantAccessDenied
TenantContext = _tenant.TenantContext
assert_tenant_match = _tenant.assert_tenant_match
filter_tenant_scoped_list = _tenant.filter_tenant_scoped_list
resolve_tenant_context = _tenant.resolve_tenant_context


# ─────────────────────────────────────────────────────────────────────
# resolve_tenant_context (6 tests)
# ─────────────────────────────────────────────────────────────────────


def test_resolve_test_override_highest_priority() -> None:
    """test_override beats every other source."""
    ctx = resolve_tenant_context(
        jwt_claim_tenant_id="from_jwt",
        header_tenant_id="from_header",
        api_key="apikey_from_key_xyz",
        host="from_subdomain.api.dealix.me",
        test_override="explicit_test",
    )
    assert ctx.tenant_id == "explicit_test"
    assert ctx.source == "test_override"


def test_resolve_jwt_beats_header_and_apikey() -> None:
    """JWT claim wins over header and API key."""
    ctx = resolve_tenant_context(
        jwt_claim_tenant_id="acme",
        header_tenant_id="other",
        api_key="apikey_other2_xxx",
    )
    assert ctx.tenant_id == "acme"
    assert ctx.source == "jwt"


def test_resolve_header_when_no_jwt() -> None:
    """X-Tenant-ID header used when JWT absent."""
    ctx = resolve_tenant_context(header_tenant_id="acme_real_estate")
    assert ctx.tenant_id == "acme_real_estate"
    assert ctx.source == "header"


def test_resolve_api_key_prefix_parses_tenant() -> None:
    """API key like apikey_<tenant>_<random> → tenant extracted."""
    ctx = resolve_tenant_context(api_key="apikey_acme_real_estate_xyz789")
    assert ctx.tenant_id == "acme_real_estate"
    assert ctx.source == "api_key"


def test_resolve_subdomain_when_only_host() -> None:
    """Subdomain extracted from host header."""
    ctx = resolve_tenant_context(host="acme.api.dealix.me")
    assert ctx.tenant_id == "acme"
    assert ctx.source == "subdomain"


def test_resolve_no_tenant_raises_unless_super_admin() -> None:
    """No tenant info + not super admin → CrossTenantAccessDenied."""
    with pytest.raises(CrossTenantAccessDenied):
        resolve_tenant_context()

    # Super admin doesn't need tenant
    ctx = resolve_tenant_context(is_super_admin=True, user_id="founder")
    assert ctx.is_super_admin is True
    assert ctx.tenant_id == "__super_admin__"


# ─────────────────────────────────────────────────────────────────────
# assert_tenant_match (5 tests)
# ─────────────────────────────────────────────────────────────────────


def test_assert_tenant_match_passes_on_same_tenant() -> None:
    """Same tenant → no raise."""
    assert_tenant_match(
        request_tenant="acme", object_tenant="acme",
        object_type="lead", object_id="lead_001",
    )  # no raise


def test_assert_tenant_match_blocks_cross_tenant() -> None:
    """Different tenants → raise."""
    with pytest.raises(CrossTenantAccessDenied) as excinfo:
        assert_tenant_match(
            request_tenant="acme", object_tenant="khaleej",
            object_type="lead", object_id="lead_002",
        )
    assert excinfo.value.request_tenant == "acme"
    assert excinfo.value.object_tenant == "khaleej"


def test_assert_tenant_match_allows_super_admin() -> None:
    """Super admin reads across tenants → no raise."""
    assert_tenant_match(
        request_tenant="__super_admin__",
        object_tenant="acme",  # different from request
        object_type="proof_event", object_id="pe_001",
        is_super_admin=True,
    )  # no raise


def test_assert_tenant_match_blocks_empty_tenant() -> None:
    """Article 8: empty tenant on either side → block (no silent fallback)."""
    with pytest.raises(CrossTenantAccessDenied):
        assert_tenant_match(
            request_tenant="", object_tenant="acme",
            object_type="lead", object_id="lead_003",
        )
    with pytest.raises(CrossTenantAccessDenied):
        assert_tenant_match(
            request_tenant="acme", object_tenant="",
            object_type="lead", object_id="lead_004",
        )


def test_cross_tenant_exception_carries_audit_data() -> None:
    """Exception attributes carry audit info."""
    try:
        assert_tenant_match(
            request_tenant="acme", object_tenant="khaleej",
            object_type="proof_event", object_id="pe_999",
        )
    except CrossTenantAccessDenied as exc:
        assert exc.request_tenant == "acme"
        assert exc.object_tenant == "khaleej"
        assert exc.object_type == "proof_event"
        assert exc.object_id == "pe_999"
        assert "Cross-tenant" in str(exc)


# ─────────────────────────────────────────────────────────────────────
# filter_tenant_scoped_list (4 tests)
# ─────────────────────────────────────────────────────────────────────


def test_filter_excludes_other_tenants() -> None:
    """List is filtered to only items matching request_tenant."""
    items = [
        {"id": "a1", "tenant_id": "acme"},
        {"id": "k1", "tenant_id": "khaleej"},
        {"id": "a2", "tenant_id": "acme"},
        {"id": "x1", "tenant_id": "other"},
    ]
    filtered = filter_tenant_scoped_list(items, request_tenant="acme")
    assert len(filtered) == 2
    assert all(i["tenant_id"] == "acme" for i in filtered)


def test_filter_super_admin_returns_all() -> None:
    """Super admin sees the full list."""
    items = [
        {"id": "a1", "tenant_id": "acme"},
        {"id": "k1", "tenant_id": "khaleej"},
    ]
    full = filter_tenant_scoped_list(items, request_tenant="any", is_super_admin=True)
    assert len(full) == 2


def test_filter_excludes_items_without_tenant_attr() -> None:
    """Items without tenant_id attribute → excluded (Article 8 — unknown
    ownership = blocked)."""
    items = [
        {"id": "a1", "tenant_id": "acme"},
        {"id": "noown"},  # missing tenant_id
        "totally not a dict",  # weird type
    ]
    filtered = filter_tenant_scoped_list(items, request_tenant="acme")
    assert len(filtered) == 1
    assert filtered[0]["id"] == "a1"


def test_filter_supports_dataclass_objects() -> None:
    """Works on dataclass / object instances with tenant_id attribute."""
    from dataclasses import dataclass

    @dataclass
    class Lead:
        id: str
        tenant_id: str

    items = [Lead(id="a1", tenant_id="acme"), Lead(id="k1", tenant_id="khaleej")]
    filtered = filter_tenant_scoped_list(items, request_tenant="acme")
    assert len(filtered) == 1
    assert filtered[0].id == "a1"


# ─────────────────────────────────────────────────────────────────────
# API key + subdomain edge cases (3 tests)
# ─────────────────────────────────────────────────────────────────────


def test_api_key_with_short_format_returns_none() -> None:
    """API key without enough segments → falls through to next resolver."""
    # Only 2 segments → not enough for tenant extraction
    with pytest.raises(CrossTenantAccessDenied):
        resolve_tenant_context(api_key="apikey_short")


def test_subdomain_reserved_names_skipped() -> None:
    """api/www/dealix subdomains are reserved — fall through."""
    with pytest.raises(CrossTenantAccessDenied):
        resolve_tenant_context(host="api.dealix.me")
    with pytest.raises(CrossTenantAccessDenied):
        resolve_tenant_context(host="www.dealix.me")


def test_subdomain_extracts_with_port() -> None:
    """Host with port → port stripped before tenant extraction."""
    ctx = resolve_tenant_context(host="acme.api.dealix.me:8080")
    assert ctx.tenant_id == "acme"


# ─────────────────────────────────────────────────────────────────────
# Total: 18 tests (6 resolve + 5 assert_match + 4 filter_list + 3 edge)
# ─────────────────────────────────────────────────────────────────────
