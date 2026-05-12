"""Unit tests for core/authz.py (T3a + T1)."""

from __future__ import annotations

import pytest

from core.authz import Principal, Resource, _static_rbac, allowed


def _p(roles, tenant_id="ten_a"):
    return Principal(id="usr_x", roles=list(roles), attr={"tenant_id": tenant_id})


def _r(kind: str, tenant_id="ten_a"):
    return Resource(kind=kind, id="rid", attr={"tenant_id": tenant_id})


def test_static_rbac_lead_read_allowed_for_viewer() -> None:
    assert _static_rbac("read", _p(["viewer"]), _r("lead")) is True


def test_static_rbac_lead_delete_only_for_admin() -> None:
    assert _static_rbac("delete", _p(["sales_rep"]), _r("lead")) is False
    assert _static_rbac("delete", _p(["admin"]), _r("lead")) is True


def test_static_rbac_cross_tenant_denied() -> None:
    assert (
        _static_rbac(
            "read",
            _p(["admin"], tenant_id="ten_a"),
            _r("lead", tenant_id="ten_b"),
        )
        is False
    )


def test_audit_log_export_requires_admin() -> None:
    assert _static_rbac("export", _p(["auditor"]), _r("audit_log")) is False
    assert _static_rbac("export", _p(["admin"]), _r("audit_log")) is True


@pytest.mark.asyncio
async def test_allowed_uses_static_when_no_pdp(monkeypatch) -> None:
    monkeypatch.delenv("CERBOS_PDP_URL", raising=False)
    assert await allowed("read", _p(["admin"]), _r("lead")) is True
    assert await allowed("delete", _p(["viewer"]), _r("lead")) is False
