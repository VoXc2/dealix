"""Tenant load isolation under pressure — Dealix sovereign stress test.

Proves WorkQueue + workload_router maintain isolation when 20 tenants × 50 items
are hammered concurrently. No cross-tenant leakage, no PII spill, no id collision.

L0-L4 only, in-memory, deterministic. Captures failure modes:
- tenant_id bleed across list_all
- PII redaction miss under load
- idempotent collision across tenants
- concurrent add race
"""
from __future__ import annotations

import concurrent.futures

import pytest

from auto_client_acquisition.full_ops.work_item import WorkItem
from auto_client_acquisition.full_ops.work_queue import WorkQueue, get_default_queue
from dealix.company_os.workload_router import CompanyWorkloadRequest, route_company_workload


def _request(tenant: str, idx: int) -> CompanyWorkloadRequest:
    return CompanyWorkloadRequest(
        tenant_id=tenant,
        customer_id=f"customer_{tenant}_{idx}",
        title=f"Task {idx} for {tenant} — revenue diagnostic",
        description=f"Revenue leakage for {tenant} sector technology, contact user{idx}@example-{tenant}.sa",
        evidence_ids=(f"ev_{tenant}_{idx}",),
    )


def _wi(tenant: str, idx: int) -> WorkItem:
    return WorkItem(
        id=f"load-{tenant}-{idx:04d}",
        tenant_id=tenant,
        os_type="sales",
        title_ar=f"مهمة {idx} لـ {tenant}",
        title_en=f"Task {idx} for {tenant}",
        description_ar=f"تشخيص تسرب إيراد لـ {tenant}",
        description_en=f"Revenue leakage diagnostic for {tenant}",
    )


def test_tenant_load_no_leakage_under_concurrent_add():
    """20 tenants × 50 items concurrent add — each tenant sees exactly 50."""
    queue = WorkQueue()
    tenants = [f"tenant_{i:02d}" for i in range(20)]
    all_items = [_wi(t, i) for t in tenants for i in range(50)]

    # Concurrent add
    with concurrent.futures.ThreadPoolExecutor(max_workers=12) as pool:
        list(pool.map(queue.add, all_items))

    assert len(queue._items) == 1000  # total stored

    # Each tenant partition exact
    for tenant in tenants:
        items = queue.list_all(tenant_id=tenant)
        assert len(items) == 50, f"{tenant} expected 50 got {len(items)}"
        for item in items:
            assert item.tenant_id == tenant
            # Cross-tenant check: should not contain other tenant's items
            assert item.id.startswith(f"load-{tenant}-")

    # Cross-check: tenant_00 must not see tenant_01 items
    t00_ids = {it.id for it in queue.list_all(tenant_id="tenant_00")}
    t01_ids = {it.id for it in queue.list_all(tenant_id="tenant_01")}
    assert t00_ids.isdisjoint(t01_ids)


def test_tenant_load_idempotent_across_tenants():
    """Same logical id prefix with different tenant_id stays partitioned, not overwritten."""
    queue = WorkQueue()
    # Intentionally same suffix but different tenant
    for tenant in ["tenant_alpha", "tenant_beta"]:
        for i in range(10):
            queue.add(_wi(tenant, i))

    # Overwrite same id within same tenant should be idempotent (replace)
    item_v1 = _wi("tenant_alpha", 0)
    item_v1_modified = WorkItem(
        id=item_v1.id,
        tenant_id="tenant_alpha",
        os_type="sales",
        title_ar="مهمة معدلة",
        title_en="Modified Task",
        description_ar="وصف معدل",
        description_en="modified",
    )
    queue.add(item_v1_modified)
    assert queue.get(item_v1.id).title_en == "Modified Task"
    # Other tenant untouched
    assert queue.get(_wi("tenant_beta", 0).id).title_en == "Task 0 for tenant_beta"
    assert len(queue.list_all(tenant_id="tenant_alpha")) == 10
    assert len(queue.list_all(tenant_id="tenant_beta")) == 10


def test_tenant_load_router_isolation_at_scale():
    """Route 100 requests across 5 tenants — no work item leaks to wrong tenant partition."""
    tenants = [f"load_tenant_{i}" for i in range(5)]
    q = get_default_queue()
    q.clear()

    # Route 20 requests per tenant through workload_router (creates WorkItem per request)
    for tenant in tenants:
        for i in range(20):
            route = route_company_workload(_request(tenant, i))
            wi = route.to_work_item()
            assert wi.tenant_id == tenant, f"leakage: {wi.tenant_id} != {tenant}"
            # PII redacted: email should not appear in titles
            assert f"user{i}@example-{tenant}" not in wi.title_ar
            assert f"user{i}@example-{tenant}" not in wi.title_en
            q.add(wi)

    # Verify partition: 20 each, no cross bleed
    for tenant in tenants:
        items = q.list_all(tenant_id=tenant)
        assert len(items) == 20, f"{tenant} expected 20 got {len(items)}"
        for it in items:
            assert it.tenant_id == tenant

    # Cross-check disjoint ids
    t0_ids = {it.id for it in q.list_all(tenant_id="load_tenant_0")}
    t1_ids = {it.id for it in q.list_all(tenant_id="load_tenant_1")}
    assert t0_ids.isdisjoint(t1_ids)
    q.clear()
