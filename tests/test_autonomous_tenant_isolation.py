"""Cross-tenant isolation contract for the autonomous deal endpoints.

`api/routers/autonomous.py` is mounted through a domain group. Before this
guard, `mark_paid`, `manual_payment_request` and `update_deal` had no
authentication dependency and loaded `DealRecord` by the ID in the request
body with no tenant filter — so any caller could move another tenant's deal
to `paid`, overwrite its amount, and trigger customer onboarding. `list_deals`
returned every tenant's deals.

The tenant now comes from the authenticated user and is applied to the query.
"""

from __future__ import annotations

import pytest
import pytest_asyncio
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from api.routers import autonomous
from api.security.auth_deps import get_current_user
from db.models import Base, CustomerRecord, DealRecord, LeadRecord, TaskRecord

ATTACKER_TENANT = "tenant_a"
VICTIM_TENANT = "tenant_b"
ATTACKER_LEAD = "lead_of_a"
VICTIM_LEAD = "lead_of_b"
VICTIM_DEAL = "deal_of_b"


class _User:
    def __init__(self, tenant_id: str, system_role: str = "user") -> None:
        self.id = f"user_of_{tenant_id}"
        self.tenant_id = tenant_id
        self.system_role = system_role


@pytest_asyncio.fixture
async def engine(monkeypatch):
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(
            Base.metadata.create_all,
            tables=[
                LeadRecord.__table__,
                DealRecord.__table__,
                CustomerRecord.__table__,
                TaskRecord.__table__,
            ],
        )
    factory = async_sessionmaker(engine, expire_on_commit=False)

    async with factory() as session:
        session.add_all(
            [
                LeadRecord(
                    id=ATTACKER_LEAD,
                    tenant_id=ATTACKER_TENANT,
                    source="test",
                    company_name="Attacker Tenant Company",
                ),
                LeadRecord(
                    id=VICTIM_LEAD,
                    tenant_id=VICTIM_TENANT,
                    source="test",
                    company_name="Victim Tenant Company",
                ),
                DealRecord(
                    id=VICTIM_DEAL,
                    tenant_id=VICTIM_TENANT,
                    lead_id=VICTIM_LEAD,
                    stage="payment_requested",
                    amount=1000.0,
                ),
            ]
        )
        await session.commit()

    # The router builds its own sessions via async_session_factory().
    monkeypatch.setattr(autonomous, "async_session_factory", lambda: factory)
    yield factory
    await engine.dispose()


def _client(user: _User) -> AsyncClient:
    app = FastAPI()
    app.include_router(autonomous.router)
    app.dependency_overrides[get_current_user] = lambda: user
    return AsyncClient(transport=ASGITransport(app=app), base_url="http://test")


@pytest.mark.asyncio
async def test_mark_paid_cannot_touch_another_tenants_deal(engine):
    async with _client(_User(ATTACKER_TENANT)) as client:
        response = await client.post(
            "/api/v1/payments/mark-paid",
            json={"deal_id": VICTIM_DEAL, "amount": 999999},
        )

    assert response.status_code == 410
    assert response.json()["detail"]["mutation_applied"] is False

    async with engine() as session:
        deal = await session.get(DealRecord, VICTIM_DEAL)
        assert deal.stage == "payment_requested"
        assert deal.amount == 1000.0


@pytest.mark.asyncio
async def test_mark_paid_is_quarantined_even_for_owning_tenant(engine):
    async with _client(_User(VICTIM_TENANT)) as client:
        response = await client.post(
            "/api/v1/payments/mark-paid", json={"deal_id": VICTIM_DEAL}
        )

    assert response.status_code == 410
    assert response.json()["detail"]["code"] == "BODY_ONLY_PAYMENT_STATE_FORBIDDEN"

    async with engine() as session:
        deal = await session.get(DealRecord, VICTIM_DEAL)
        assert deal.stage == "payment_requested"
        assert deal.amount == 1000.0


@pytest.mark.asyncio
async def test_update_deal_cannot_touch_another_tenants_deal(engine):
    async with _client(_User(ATTACKER_TENANT)) as client:
        response = await client.patch(
            f"/api/v1/deals/{VICTIM_DEAL}", json={"stage": "paid", "amount": 1}
        )

    assert response.status_code == 404

    async with engine() as session:
        deal = await session.get(DealRecord, VICTIM_DEAL)
        assert deal.stage == "payment_requested"


@pytest.mark.asyncio
async def test_payment_request_cannot_touch_another_tenants_deal(engine):
    async with _client(_User(ATTACKER_TENANT)) as client:
        response = await client.post(
            "/api/v1/payments/manual-request", json={"deal_id": VICTIM_DEAL}
        )

    assert response.status_code == 410
    assert response.json()["detail"]["code"] == "LEGACY_PAYMENT_REQUEST_QUARANTINED"

    async with engine() as session:
        deal = await session.get(DealRecord, VICTIM_DEAL)
        assert deal.stage == "payment_requested"


@pytest.mark.asyncio
async def test_declaring_the_victim_tenant_does_not_widen_access(engine):
    async with _client(_User(ATTACKER_TENANT)) as client:
        response = await client.post(
            "/api/v1/payments/mark-paid",
            json={"deal_id": VICTIM_DEAL, "tenant_id": VICTIM_TENANT},
        )

    assert response.status_code == 410
    assert response.json()["detail"]["mutation_applied"] is False


@pytest.mark.asyncio
async def test_created_deal_is_visible_to_its_creator(engine):
    """A deal created through the API must be readable by the same tenant.

    The create handler previously omitted tenant_id, so once the read paths
    gained a tenant predicate every newly created deal became invisible to
    everyone. Seeding the database directly would not have caught that —
    this drives the real create -> list -> patch round trip.
    """
    async with _client(_User(ATTACKER_TENANT)) as client:
        created = await client.post(
            "/api/v1/deals", json={"lead_id": ATTACKER_LEAD, "amount": 500}
        )
        assert created.status_code == 200
        deal_id = created.json()["id"]

        listed = await client.get("/api/v1/deals")
        assert deal_id in [item["id"] for item in listed.json()["items"]]

        patched = await client.patch(
            f"/api/v1/deals/{deal_id}", json={"stage": "payment_requested"}
        )
        assert patched.status_code == 200

    async with engine() as session:
        deal = await session.get(DealRecord, deal_id)
        assert deal.tenant_id == ATTACKER_TENANT


@pytest.mark.asyncio
async def test_create_deal_rejects_another_tenants_lead(engine):
    async with _client(_User(ATTACKER_TENANT)) as client:
        response = await client.post(
            "/api/v1/deals", json={"lead_id": VICTIM_LEAD, "amount": 500}
        )

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_a_created_deal_stays_invisible_to_other_tenants(engine):
    async with _client(_User(ATTACKER_TENANT)) as client:
        created = await client.post(
            "/api/v1/deals", json={"lead_id": ATTACKER_LEAD}
        )
        assert created.status_code == 200
        deal_id = created.json()["id"]

    async with _client(_User(VICTIM_TENANT)) as client:
        response = await client.patch(
            f"/api/v1/deals/{deal_id}", json={"stage": "paid"}
        )

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_super_admin_may_target_a_tenant_with_the_header(engine):
    """A super admin must name the target; the header is the canonical way."""
    admin = _User("tenant_admin_home", system_role="super_admin")

    async with _client(admin) as client:
        denied = await client.get("/api/v1/deals")
        assert denied.status_code == 403

    app = FastAPI()
    app.include_router(autonomous.router)
    app.dependency_overrides[get_current_user] = lambda: admin
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        allowed = await client.get(
            "/api/v1/deals", headers={"X-Tenant-ID": VICTIM_TENANT}
        )

    assert allowed.status_code == 200
    assert [item["id"] for item in allowed.json()["items"]] == [VICTIM_DEAL]


@pytest.mark.asyncio
async def test_listing_never_spans_tenants(engine):
    async with _client(_User(ATTACKER_TENANT)) as client:
        response = await client.get("/api/v1/deals")

    assert response.status_code == 200
    assert response.json()["items"] == []


def test_deal_routes_require_authentication():
    protected = {
        ("PATCH", "/api/v1/deals/{deal_id}"),
        ("GET", "/api/v1/deals"),
        ("POST", "/api/v1/payments/manual-request"),
        ("POST", "/api/v1/payments/mark-paid"),
        ("POST", "/api/v1/deals"),
    }
    found = {}
    for route in autonomous.router.routes:
        for method in route.methods:
            found[(method, route.path)] = {
                dep.call for dep in route.dependant.dependencies
            }

    for key in protected:
        assert key in found, f"route missing from the router: {key}"
        assert get_current_user in found[key], f"{key[0]} {key[1]} is unauthenticated"
