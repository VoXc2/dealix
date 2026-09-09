"""Future SaaS billing router: keep its tenant/money safety tested without exposing self-serve launch actions.

Current first-launch commercial authority is quote-only after qualified discovery,
with no public/self-serve checkout. ``api.routers.billing`` remains useful future
SaaS code. The production launch app intentionally preserves only read-only
existing-tenant billing views (subscription, invoices, features) while excluding
public plan discovery and all subscription/payment mutations.
"""

from __future__ import annotations

import uuid

import pytest
import pytest_asyncio
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from api.routers import billing
from api.security.auth_deps import get_current_user
from db.models import Base
from db.models_subscription import (
    FeatureFlagRecord,
    InvoiceRecord,
    PlanRecord,
    SubscriptionRecord,
)
from db.session import get_db as get_db_session

TENANT_A = "tnt_buyer"
TENANT_B = "tnt_victim"


class _User:
    def __init__(self, tenant_id: str | None) -> None:
        self.id = f"usr_{uuid.uuid4().hex[:8]}"
        self.tenant_id = tenant_id
        self.email = "buyer@example.com"
        self.name = "Buyer"
        self.system_role = "member"


@pytest_asyncio.fixture
async def db_session() -> AsyncSession:
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(
            Base.metadata.create_all,
            tables=[
                PlanRecord.__table__,
                SubscriptionRecord.__table__,
                InvoiceRecord.__table__,
                FeatureFlagRecord.__table__,
            ],
        )
    factory = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    async with factory() as session:
        yield session
    await engine.dispose()


@pytest_asyncio.fixture
async def seeded(db_session):
    plan = PlanRecord(
        id="pln_starter",
        slug="starter",
        name_en="Starter",
        name_ar="المبتدئ",
        price_sar_monthly=299.0,
        is_public=True,
        is_custom=False,
        sort_order=1,
        features={"crm": True},
    )
    victim_invoice = InvoiceRecord(
        id="inv_victim",
        tenant_id=TENANT_B,
        invoice_number="INV-VICTIM-001",
        status="open",
        total_sar=25000.0,
    )
    db_session.add_all([plan, victim_invoice])
    await db_session.commit()
    return {"plan": plan, "victim_invoice": victim_invoice}


def _isolated_billing_app(db_session: AsyncSession, tenant_id: str | None = TENANT_A) -> FastAPI:
    app = FastAPI()
    app.include_router(billing.router)
    app.dependency_overrides[get_db_session] = lambda: db_session
    app.dependency_overrides[get_current_user] = lambda: _User(tenant_id)
    return app


@pytest_asyncio.fixture
async def client(db_session, monkeypatch):
    monkeypatch.setenv("API_KEYS", "")
    monkeypatch.setenv("ADMIN_API_KEYS", "")
    app = _isolated_billing_app(db_session)
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac


READ_ONLY_LAUNCH_ROUTES = [
    ("GET", "/api/v1/billing/subscription"),
    ("GET", "/api/v1/billing/invoices"),
    ("GET", "/api/v1/billing/features"),
]

BLOCKED_SELF_SERVE_ROUTES = [
    ("GET", "/api/v1/billing/plans"),
    ("POST", "/api/v1/billing/subscribe"),
    ("POST", "/api/v1/billing/upgrade"),
    ("POST", "/api/v1/billing/cancel"),
    ("POST", "/api/v1/billing/invoices/{invoice_id}/pay"),
]


def test_launch_app_preserves_read_only_existing_tenant_billing_views() -> None:
    from api.main import app

    mounted = {
        (method.upper(), path)
        for path, operations in app.openapi()["paths"].items()
        for method in operations
    }
    for route in READ_ONLY_LAUNCH_ROUTES:
        assert route in mounted


def test_launch_app_blocks_self_serve_billing_and_payment_mutations() -> None:
    """Quote-only launch must not expose public/self-serve billing actions."""
    from api.main import app

    mounted = {
        (method.upper(), path)
        for path, operations in app.openapi()["paths"].items()
        for method in operations
    }
    for route in BLOCKED_SELF_SERVE_ROUTES:
        assert route not in mounted


def test_isolated_billing_router_schema_builds() -> None:
    app = FastAPI()
    app.include_router(billing.router)
    schema = app.openapi()
    assert "/api/v1/billing/subscription" in schema["paths"]
    assert "SubscriptionOut" in schema["components"]["schemas"]


@pytest.mark.asyncio
async def test_invoice_list_shows_only_the_callers_tenant(client, seeded):
    resp = await client.get("/api/v1/billing/invoices")
    assert resp.status_code == 200, resp.text
    numbers = [row["invoice_number"] for row in resp.json()]
    assert "INV-VICTIM-001" not in numbers


@pytest.mark.asyncio
async def test_paying_another_tenants_invoice_is_refused(client, seeded):
    resp = await client.post("/api/v1/billing/invoices/inv_victim/pay")
    assert resp.status_code == 404, resp.text


@pytest.mark.asyncio
async def test_a_user_with_no_tenant_is_refused(db_session, seeded, monkeypatch):
    monkeypatch.setenv("API_KEYS", "")
    app = _isolated_billing_app(db_session, tenant_id=None)
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        resp = await ac.get("/api/v1/billing/invoices")
    assert resp.status_code == 400, resp.text


@pytest.mark.asyncio
async def test_subscribe_prices_from_the_plan_record(client, seeded):
    resp = await client.post(
        "/api/v1/billing/subscribe",
        json={"plan_slug": "starter", "billing_cycle": "monthly", "seat_count": 2},
    )
    assert resp.status_code == 200, resp.text
    assert resp.json()["plan_id"] == "pln_starter"


@pytest.mark.asyncio
async def test_subscribing_to_an_unknown_plan_is_refused(client, seeded):
    resp = await client.post(
        "/api/v1/billing/subscribe",
        json={"plan_slug": "does-not-exist", "billing_cycle": "monthly"},
    )
    assert resp.status_code == 404, resp.text


@pytest.mark.asyncio
async def test_pay_invoice_sends_customer_to_absolute_return_url(
    db_session, seeded, monkeypatch
):
    monkeypatch.setenv("API_KEYS", "")
    monkeypatch.setenv("APP_URL", "https://api.dealix.me")

    own_invoice = InvoiceRecord(
        id="inv_own",
        tenant_id=TENANT_A,
        invoice_number="INV-OWN-001",
        status="open",
        total_sar=299.0,
    )
    db_session.add(own_invoice)
    await db_session.commit()

    captured: dict[str, object] = {}

    async def _fake_link(req):
        captured["callback_url"] = req.callback_url
        captured["amount_halalas"] = req.amount_halalas

        class _Link:
            invoice_id = "inv_moyasar"
            payment_url = "https://moyasar.test/pay/abc"

        return _Link()

    monkeypatch.setattr(billing, "create_moyasar_payment_link", _fake_link)
    app = _isolated_billing_app(db_session)
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        resp = await ac.post("/api/v1/billing/invoices/inv_own/pay")

    assert resp.status_code == 200, resp.text
    callback = str(captured["callback_url"])
    assert callback == "https://api.dealix.me/checkout/return"
    assert "/webhooks/" not in callback
    assert captured["amount_halalas"] == 29900
