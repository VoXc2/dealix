"""Platform v10 reference contracts — gap map §11."""
from __future__ import annotations

import pytest

from auto_client_acquisition.platform_v10 import (
    AuthPrincipal,
    ObjectStorageContract,
    Permission,
    RLSPolicy,
    StoredObjectRef,
    TenantContext,
    assert_same_tenant,
    require_permission,
    row_tenant_matches,
)


def test_tenant_context_strips_and_rejects_empty():
    ctx = TenantContext(tenant_id="  acme  ")
    assert ctx.tenant_id == "acme"
    with pytest.raises(ValueError):
        TenantContext(tenant_id="   ")


def test_assert_same_tenant_blocks_cross_tenant():
    ctx = TenantContext(tenant_id="t1")
    assert_same_tenant(ctx, "t1")
    with pytest.raises(PermissionError, match="cross_tenant"):
        assert_same_tenant(ctx, "t2")


def test_rls_row_tenant_matches():
    pol = RLSPolicy(table_name="leads", enforce_in_app_layer=True)
    assert row_tenant_matches(pol, "a", "a") is True
    assert row_tenant_matches(pol, "a", "b") is False
    assert row_tenant_matches(pol, None, "a") is False


def test_rls_bypass_when_not_enforced():
    pol = RLSPolicy(table_name="x", enforce_in_app_layer=False)
    assert row_tenant_matches(pol, None, "any") is True


def test_auth_require_permission():
    p = AuthPrincipal(subject="u1", tenant_id="t1", roles=("read_pipeline",))
    require_permission(p, Permission.READ_PIPELINE)
    with pytest.raises(PermissionError):
        require_permission(p, Permission.ADMIN_TENANT)


def test_stored_object_ref_roundtrip():
    ref = StoredObjectRef(bucket="proof", key="t1/p1.json", tenant_id="t1")
    d = ref.model_dump()
    assert StoredObjectRef(**d).key == "t1/p1.json"


class _DummyStore:
    def put_bytes(self, ref: StoredObjectRef, data: bytes) -> str:
        return ref.key

    def get_bytes(self, ref: StoredObjectRef) -> bytes:
        return b""

    def delete(self, ref: StoredObjectRef) -> None:
        return None


def test_object_storage_contract_protocol():
    store: ObjectStorageContract = _DummyStore()
    ref = StoredObjectRef(bucket="b", key="k", tenant_id="t")
    assert store.put_bytes(ref, b"x") == "k"
