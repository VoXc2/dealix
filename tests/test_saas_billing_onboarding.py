"""Phase 1 SaaS billing and onboarding endpoint tests."""
from __future__ import annotations

import uuid

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from api.security.jwt import create_access_token
from db.models import RoleRecord, TenantRecord, UserRecord
from db.models_subscription import PlanRecord
from db.session import get_session


async def _create_plan(session: AsyncSession, slug: str, name_en: str, monthly: float, yearly: float) -> PlanRecord:
    plan = PlanRecord(
        id=f"pl_{slug}",
        name_ar=f"خطة {slug}",
        name_en=name_en,
        slug=slug,
        price_sar_monthly=monthly,
        price_sar_yearly=yearly,
        yearly_discount_pct=10.0,
        max_users=5,
        max_leads_per_month=1000,
        max_storage_gb=10.0,
        max_api_calls_per_month=10000,
        features={"crm": True, "projects": slug != "free"},
        is_public=True,
        is_custom=False,
        sort_order=1 if slug == "starter" else 2 if slug == "growth" else 0,
    )
    session.add(plan)
    await session.flush()
    return plan


async def _create_tenant_user(session: AsyncSession, tenant_id: str, user_id: str, email: str) -> tuple[TenantRecord, UserRecord]:
    tenant = TenantRecord(
        id=tenant_id,
        name="Test Tenant",
        slug=f"test-tenant-{tenant_id[:6]}",
        plan="starter",
        status="active",
        timezone="Asia/Riyadh",
        locale="ar",
        currency="SAR",
        max_users=5,
        max_leads_per_month=1000,
        features={"crm": True, "projects": True},
    )
    role = RoleRecord(
        id=f"rol_{uuid.uuid4().hex[:12]}",
        tenant_id=tenant_id,
        name="owner",
        permissions=["*:*"],
        description="Owner role",
        is_system=True,
    )
    user = UserRecord(
        id=user_id,
        tenant_id=tenant_id,
        role_id=role.id,
        email=email,
        name="Test Owner",
        hashed_password="not-used",
        is_active=True,
        is_verified=True,
    )
    session.add_all([tenant, role, user])
    await session.flush()
    return tenant, user


@pytest.mark.asyncio
async def test_self_serve_onboarding_is_disabled_by_default(async_client, monkeypatch):
    monkeypatch.delenv("DEALIX_SELF_SERVE_SIGNUP_ENABLED", raising=False)

    plans_response = await async_client.get("/api/v1/onboarding/plans")
    assert plans_response.status_code == 404, plans_response.text

    signup_response = await async_client.post(
        "/api/v1/onboarding/signup",
        json={
            "email": "blocked@example.com",
            "password": "s3cureP@ssword",
            "name": "Blocked User",
            "company_name": "Blocked Company",
            "plan_slug": "free",
            "billing_cycle": "monthly",
        },
    )
    assert signup_response.status_code == 404, signup_response.text


@pytest.mark.asyncio
async def test_self_serve_env_cannot_override_source_authority(async_client, monkeypatch):
    monkeypatch.setenv("DEALIX_SELF_SERVE_SIGNUP_ENABLED", "true")
    plans_response = await async_client.get("/api/v1/onboarding/plans")
    assert plans_response.status_code == 404, plans_response.text
    signup_response = await async_client.post(
        "/api/v1/onboarding/signup",
        json={
            "email": "still-blocked@example.com",
            "password": "s3cureP@ssword",
            "name": "Blocked User",
            "company_name": "Blocked Company",
            "plan_slug": "free",
            "billing_cycle": "monthly",
        },
    )
    assert signup_response.status_code == 404, signup_response.text


@pytest.mark.asyncio
async def test_existing_tenant_can_complete_wizard(async_client):
    tenant_id = f"tnt_{uuid.uuid4().hex[:12]}"
    user_id = f"usr_{uuid.uuid4().hex[:12]}"
    async with get_session() as session:
        await _create_tenant_user(
            session,
            tenant_id=tenant_id,
            user_id=user_id,
            email="wizard@testsaas.local",
        )

    token = create_access_token(
        user_id=user_id,
        tenant_id=tenant_id,
        role="owner",
    )
    auth_header = {"Authorization": f"Bearer {token}"}
    wizard_response = await async_client.post(
        "/api/v1/onboarding/wizard",
        json={
            "sector": "technology",
            "company_size": "medium",
            "phone": "+966501234567",
            "website": "https://testsaas.local",
        },
        headers=auth_header,
    )
    assert wizard_response.status_code == 200, wizard_response.text
    assert wizard_response.json()["status"] == "completed"


@pytest.mark.asyncio
async def test_billing_subscribe_upgrade_invoice_and_cancel_endpoints(async_client):
    tenant_id = f"tnt_{uuid.uuid4().hex[:12]}"
    user_id = f"usr_{uuid.uuid4().hex[:12]}"
    invoice_id: str
    token: str

    async with get_session() as session:
        starter_plan = await _create_plan(session, slug="starter", name_en="Starter", monthly=199.0, yearly=1990.0)
        growth_plan = await _create_plan(session, slug="growth", name_en="Growth", monthly=499.0, yearly=4990.0)
        await _create_tenant_user(session, tenant_id=tenant_id, user_id=user_id, email="billing@testsaas.local")

    token = create_access_token(
        user_id=user_id,
        tenant_id=tenant_id,
        role="owner",
    )
    auth_header = {"Authorization": f"Bearer {token}"}

    subscribe_response = await async_client.post(
        "/api/v1/billing/subscribe",
        json={"plan_slug": "starter", "billing_cycle": "monthly", "seat_count": 3},
        headers=auth_header,
    )
    assert subscribe_response.status_code == 200, subscribe_response.text
    subscription = subscribe_response.json()
    assert subscription["plan_id"] == starter_plan.id
    assert subscription["billing_cycle"] == "monthly"
    assert subscription["seat_count"] == 3

    upgrade_response = await async_client.post(
        "/api/v1/billing/upgrade",
        json={"plan_slug": "growth", "billing_cycle": "yearly"},
        headers=auth_header,
    )
    assert upgrade_response.status_code == 200, upgrade_response.text
    upgraded = upgrade_response.json()
    assert upgraded["plan_id"] == growth_plan.id
    assert upgraded["billing_cycle"] == "yearly"
    assert upgraded["mrr_sar"] > subscription["mrr_sar"]

    invoices_response = await async_client.get(
        "/api/v1/billing/invoices",
        headers=auth_header,
    )
    assert invoices_response.status_code == 200, invoices_response.text
    invoices = invoices_response.json()
    assert isinstance(invoices, list)
    assert len(invoices) >= 1
    invoice = invoices[0]
    assert invoice["total_sar"] > 0
    invoice_id = invoice["id"]

    pay_response = await async_client.post(
        f"/api/v1/billing/invoices/{invoice_id}/pay",
        headers=auth_header,
    )
    assert pay_response.status_code == 200, pay_response.text
    pay_payload = pay_response.json()
    assert pay_payload["invoice_id"] == invoice_id
    assert pay_payload["payment_url"].startswith("https://sandbox.moyasar.com/invoices/")

    cancel_response = await async_client.post(
        "/api/v1/billing/cancel",
        json={"immediate": True},
        headers=auth_header,
    )
    assert cancel_response.status_code == 200, cancel_response.text
    assert cancel_response.json()["status"] == "cancelled"


@pytest.mark.asyncio
async def test_billing_subscription_and_features_and_invite(async_client):
    tenant_id = f"tnt_{uuid.uuid4().hex[:12]}"
    user_id = f"usr_{uuid.uuid4().hex[:12]}"

    async with get_session() as session:
        starter_plan = await _create_plan(session, slug="starter", name_en="Starter", monthly=199.0, yearly=1990.0)
        await _create_tenant_user(session, tenant_id=tenant_id, user_id=user_id, email="features@testsaas.local")

    token = create_access_token(
        user_id=user_id,
        tenant_id=tenant_id,
        role="owner",
    )
    auth_header = {"Authorization": f"Bearer {token}"}

    subscribe_response = await async_client.post(
        "/api/v1/billing/subscribe",
        json={"plan_slug": "starter", "billing_cycle": "monthly", "seat_count": 2},
        headers=auth_header,
    )
    assert subscribe_response.status_code == 200, subscribe_response.text
    subscription = subscribe_response.json()
    assert subscription["plan_id"] == starter_plan.id

    subscription_response = await async_client.get(
        "/api/v1/billing/subscription",
        headers=auth_header,
    )
    assert subscription_response.status_code == 200, subscription_response.text
    assert subscription_response.json()["id"] == subscription["id"]

    features_response = await async_client.get(
        "/api/v1/billing/features",
        headers=auth_header,
    )
    assert features_response.status_code == 200, features_response.text
    features_payload = features_response.json()
    assert isinstance(features_payload, dict)
    assert features_payload.get("crm") is True
    assert features_payload.get("projects") is True

    invite_response = await async_client.post(
        "/api/v1/onboarding/invite",
        json={"email": "member@testsaas.local", "role_name": "viewer"},
        headers=auth_header,
    )
    assert invite_response.status_code == 200, invite_response.text
    invite_payload = invite_response.json()
    assert invite_payload["user_id"].startswith("usr_")
    assert isinstance(invite_payload["invite_url"], str)
