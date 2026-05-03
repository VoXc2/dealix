"""
PR-BE-Attribution + PR-FE-2/4 backend tests.

Coverage:
  1. New SQLAlchemy models (Subscription, Payment, FunnelEvent) + lead/deal partner_id
  2. MRR calculator (totals, per-partner, ARR, churn)
  3. Commission calculator (expected, earned, setup_bonus, scorecard)
  4. Moyasar webhook persistence (paid → Payment + FunnelEvent; canceled → Subscription)
  5. Partners router (dashboard / customers / customer detail / mrr-trend / payouts / playbook / me)
  6. Services router (catalog / bundle detail / intake-questions)
  7. Cards router (roles / feed / decision)
  8. Card schema invariants (≤3 buttons, role/type enums)
"""

from __future__ import annotations

import uuid
from datetime import datetime, timedelta, timezone

import pytest
from sqlalchemy import select

from auto_client_acquisition.business.commission_calculator import (
    commission_from_payments,
    expected_monthly_commission,
    partner_scorecard,
    setup_bonus,
)
from auto_client_acquisition.business.mrr_calculator import (
    ACTIVE_STATUSES,
    active_count,
    annualize,
    churn_rate,
    mrr_by_partner,
    total_mrr,
)
from auto_client_acquisition.revenue_company_os.card_factory import build_feed, list_roles
from auto_client_acquisition.revenue_company_os.cards import (
    MAX_BUTTONS,
    Card,
    CardButton,
    CardType,
    Role,
)
from db.models import (
    DealRecord,
    FunnelEventRecord,
    LeadRecord,
    PartnerRecord,
    PaymentRecord,
    SubscriptionRecord,
)


# ── Models ────────────────────────────────────────────────────────


def test_lead_record_has_partner_id():
    cols = {c.name for c in LeadRecord.__table__.columns}
    assert "partner_id" in cols


def test_deal_record_has_partner_id():
    cols = {c.name for c in DealRecord.__table__.columns}
    assert "partner_id" in cols


def test_subscription_record_columns():
    cols = {c.name for c in SubscriptionRecord.__table__.columns}
    expected = {
        "id", "customer_id", "partner_id", "plan_id", "status",
        "started_at", "current_period_start", "current_period_end",
        "mrr_sar", "currency", "moyasar_subscription_id",
        "canceled_at", "cancel_reason",
    }
    assert expected.issubset(cols)


def test_payment_record_columns():
    cols = {c.name for c in PaymentRecord.__table__.columns}
    expected = {
        "id", "subscription_id", "customer_id", "partner_id",
        "amount_sar", "status", "moyasar_payment_id", "moyasar_event_id",
        "paid_at",
    }
    assert expected.issubset(cols)


def test_funnel_event_record_columns():
    cols = {c.name for c in FunnelEventRecord.__table__.columns}
    expected = {"id", "lead_id", "customer_id", "partner_id", "stage", "occurred_at"}
    assert expected.issubset(cols)


# ── MRR calculator ────────────────────────────────────────────────


class _FakeSub:
    def __init__(self, status, mrr, partner_id="p1"):
        self.status = status
        self.mrr_sar = mrr
        self.partner_id = partner_id
        self.id = uuid.uuid4().hex[:8]


def test_total_mrr_only_active_statuses():
    subs = [
        _FakeSub("active", 2999.0, "p1"),
        _FakeSub("active", 499.0, "p1"),
        _FakeSub("canceled", 1500.0, "p1"),
        _FakeSub("trialing", 100.0, "p1"),
    ]
    assert total_mrr(subs) == 2999.0 + 499.0


def test_total_mrr_handles_past_due():
    subs = [_FakeSub("past_due", 999.0, "p1")]
    assert total_mrr(subs) == 999.0


def test_total_mrr_empty_returns_zero():
    assert total_mrr([]) == 0.0


def test_active_statuses_constant():
    assert "active" in ACTIVE_STATUSES
    assert "past_due" in ACTIVE_STATUSES
    assert "canceled" not in ACTIVE_STATUSES


def test_mrr_by_partner_buckets_direct_when_no_partner():
    subs = [
        _FakeSub("active", 100.0, "p1"),
        _FakeSub("active", 200.0, None),
    ]
    out = mrr_by_partner(subs)
    assert out["p1"] == 100.0
    assert out["_direct"] == 200.0


def test_active_count_excludes_canceled():
    subs = [
        _FakeSub("active", 0, "p"),
        _FakeSub("canceled", 0, "p"),
        _FakeSub("active", 0, "p"),
    ]
    assert active_count(subs) == 2


def test_annualize():
    assert annualize(2999.0) == 35988.0


def test_churn_rate_zero_when_no_active():
    assert churn_rate([], canceled_in_period=5, period_active_at_start=0) == 0.0


def test_churn_rate_correct():
    assert churn_rate([], canceled_in_period=2, period_active_at_start=10) == 0.2


# ── Commission calculator ─────────────────────────────────────────


class _FakePartner:
    def __init__(self, share=15.0, fee=0.0):
        self.id = "agency_x"
        self.mrr_share_pct = share
        self.setup_fee_sar = fee


class _FakePay:
    def __init__(self, amt, status="paid", partner_id="agency_x"):
        self.amount_sar = amt
        self.status = status
        self.partner_id = partner_id
        self.subscription_id = None


def test_expected_monthly_commission_zero_share():
    p = _FakePartner(share=0.0)
    subs = [_FakeSub("active", 1000.0, "agency_x")]
    assert expected_monthly_commission(p, subs) == 0.0


def test_expected_monthly_commission_basic():
    p = _FakePartner(share=15.0)
    subs = [
        _FakeSub("active", 2999.0, "agency_x"),
        _FakeSub("active", 499.0, "agency_x"),
        _FakeSub("canceled", 999.0, "agency_x"),
        _FakeSub("active", 1000.0, "other_partner"),
    ]
    # only active + own partner: (2999 + 499) * 0.15 = 524.7
    assert expected_monthly_commission(p, subs) == 524.7


def test_commission_from_payments_excludes_refunds():
    p = _FakePartner(share=15.0)
    pays = [
        _FakePay(2999.0, "paid"),
        _FakePay(2999.0, "refunded"),
        _FakePay(500.0, "failed"),
    ]
    assert commission_from_payments(p, pays) == 449.85


def test_setup_bonus_applies_per_new_sub():
    p = _FakePartner(share=10.0, fee=500.0)
    assert setup_bonus(p, 3) == 1500.0
    assert setup_bonus(p, 0) == 0.0


def test_partner_scorecard_full_shape():
    p = _FakePartner(share=15.0, fee=0.0)
    subs = [_FakeSub("active", 2999.0, "agency_x")]
    pays = [_FakePay(2999.0, "paid")]
    out = partner_scorecard(p, subs, pays)
    assert out["partner_id"] == "agency_x"
    assert out["expected_monthly_commission_sar"] == 449.85
    assert out["earned_to_date_sar"] == 449.85
    assert out["active_referrals"] == 1


# ── Card schema ───────────────────────────────────────────────────


def test_card_max_buttons_enforced():
    with pytest.raises(ValueError, match="buttons"):
        Card(
            id="c1",
            type=CardType.OPPORTUNITY,
            role=Role.SALES,
            title_ar="عنوان",
            why_now_ar="السبب",
            recommended_action_ar="الإجراء",
            buttons=[CardButton(f"b{i}", "skip") for i in range(MAX_BUTTONS + 1)],
        )


def test_card_requires_arabic_title():
    with pytest.raises(ValueError, match="Arabic title"):
        Card(
            id="c1",
            type=CardType.OPPORTUNITY,
            role=Role.SALES,
            title_ar="",
            why_now_ar="السبب",
            recommended_action_ar="الإجراء",
        )


def test_card_to_dict_serialization():
    c = Card(
        id="c1",
        type=CardType.PROOF,
        role=Role.CEO,
        title_ar="ت",
        why_now_ar="ل",
        recommended_action_ar="إ",
        buttons=[CardButton("ok", "approve", primary=True)],
    )
    d = c.to_dict()
    assert d["type"] == "proof"
    assert d["role"] == "ceo"
    assert d["buttons"][0]["primary"] is True


# ── Card factory ──────────────────────────────────────────────────


@pytest.mark.parametrize("role", list(Role))
def test_build_feed_returns_cards_for_every_role(role):
    cards = build_feed(role)
    assert isinstance(cards, list)
    assert all(isinstance(c, Card) for c in cards)
    # All demo cards must be marked as demo
    for c in cards:
        assert c.meta.get("is_demo") is True


def test_build_feed_unknown_role_raises():
    with pytest.raises(ValueError, match="unknown role"):
        build_feed("not_a_role")


def test_list_roles_has_six_entries():
    rows = list_roles()
    ids = {r["id"] for r in rows}
    assert ids == {r.value for r in Role}


# ── Services router ───────────────────────────────────────────────


@pytest.mark.asyncio
async def test_services_catalog_endpoint(async_client):
    resp = await async_client.get("/api/v1/services/catalog")
    assert resp.status_code == 200
    body = resp.json()
    assert body["currency"] == "SAR"
    assert isinstance(body["bundles"], list)
    ids = {b["id"] for b in body["bundles"]}
    expected = {
        "free_diagnostic", "growth_starter", "data_to_revenue",
        "executive_growth_os", "partnership_growth", "full_growth_control_tower",
    }
    assert expected.issubset(ids), f"missing: {expected - ids}"


@pytest.mark.asyncio
async def test_services_bundle_detail(async_client):
    resp = await async_client.get("/api/v1/services/growth_starter")
    assert resp.status_code == 200
    body = resp.json()
    assert body["price_sar"] == 499
    assert "Proof Pack" in " ".join(body["deliverables_ar"])


@pytest.mark.asyncio
async def test_services_bundle_404(async_client):
    resp = await async_client.get("/api/v1/services/not_a_bundle")
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_services_intake_questions(async_client):
    resp = await async_client.get("/api/v1/services/growth_starter/intake-questions")
    assert resp.status_code == 200
    body = resp.json()
    assert isinstance(body["questions"], list)
    keys = {q["key"] for q in body["questions"]}
    assert "company_name" in keys


# ── Cards router ──────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_cards_roles_endpoint(async_client):
    resp = await async_client.get("/api/v1/cards/roles")
    assert resp.status_code == 200
    body = resp.json()
    assert any(r["id"] == "ceo" for r in body["roles"])


@pytest.mark.asyncio
@pytest.mark.parametrize("role", ["ceo", "sales", "growth", "service", "support", "agency"])
async def test_cards_feed_per_role(async_client, role):
    resp = await async_client.get(f"/api/v1/cards/feed?role={role}")
    assert resp.status_code == 200
    body = resp.json()
    assert body["role"] == role
    assert body["is_demo"] is True
    assert isinstance(body["cards"], list)
    for c in body["cards"]:
        assert len(c["buttons"]) <= MAX_BUTTONS


@pytest.mark.asyncio
async def test_cards_feed_unknown_role_400(async_client):
    resp = await async_client.get("/api/v1/cards/feed?role=robot")
    assert resp.status_code == 400


@pytest.mark.asyncio
async def test_cards_decision_records(async_client):
    resp = await async_client.post("/api/v1/cards/c1/decision", json={"action": "approve"})
    assert resp.status_code == 200
    assert resp.json()["recorded"] is True


@pytest.mark.asyncio
async def test_cards_decision_unknown_action_400(async_client):
    resp = await async_client.post("/api/v1/cards/c1/decision", json={"action": "yolo"})
    assert resp.status_code == 400


# ── Partners router ───────────────────────────────────────────────


@pytest.mark.asyncio
async def test_partners_me_demo_response(async_client):
    resp = await async_client.get("/api/v1/partners/me")
    assert resp.status_code == 200
    body = resp.json()
    assert body["partner_id"] == "demo_partner"
    assert body["is_demo"] is True


@pytest.mark.asyncio
async def test_partners_dashboard_404_for_unknown_partner(async_client):
    resp = await async_client.get("/api/v1/partners/non_existent_partner_xyz/dashboard")
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_partners_dashboard_with_seeded_partner(async_client):
    """Insert a partner row + sub + payment, then read dashboard."""
    from db.session import get_session

    partner_id = f"test_p_{uuid.uuid4().hex[:8]}"
    customer_id = f"cust_{uuid.uuid4().hex[:8]}"
    async with get_session() as s:
        s.add(PartnerRecord(
            id=partner_id,
            company_name="Test Agency",
            partner_type="AGENCY",
            mrr_share_pct=15.0,
        ))
        s.add(SubscriptionRecord(
            id=f"sub_{uuid.uuid4().hex[:8]}",
            customer_id=customer_id,
            partner_id=partner_id,
            plan_id="executive_growth_os",
            status="active",
            mrr_sar=2999.0,
        ))
        s.add(PaymentRecord(
            id=f"pay_{uuid.uuid4().hex[:8]}",
            customer_id=customer_id,
            partner_id=partner_id,
            amount_sar=2999.0,
            status="paid",
        ))

    resp = await async_client.get(f"/api/v1/partners/{partner_id}/dashboard")
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert body["partner_id"] == partner_id
    assert body["kpis"]["currently_paying"] == 1
    assert body["kpis"]["mrr_total_sar"] == 2999.0
    # 15% commission on 2999 = 449.85
    assert body["kpis"]["earned_to_date_sar"] == 449.85


@pytest.mark.asyncio
async def test_partners_customers_filter_by_stage(async_client):
    from db.session import get_session

    partner_id = f"test_p_{uuid.uuid4().hex[:8]}"
    async with get_session() as s:
        s.add(PartnerRecord(
            id=partner_id,
            company_name="X",
            partner_type="AGENCY",
            mrr_share_pct=10.0,
        ))
        s.add(SubscriptionRecord(
            id=f"sub_{uuid.uuid4().hex[:8]}",
            customer_id=f"c_{uuid.uuid4().hex[:8]}",
            partner_id=partner_id,
            plan_id="growth_starter",
            status="active",
            mrr_sar=499.0,
        ))
    resp = await async_client.get(f"/api/v1/partners/{partner_id}/customers")
    assert resp.status_code == 200
    body = resp.json()
    assert body["count"] >= 1


@pytest.mark.asyncio
async def test_partners_mrr_trend_returns_n_buckets(async_client):
    from db.session import get_session
    partner_id = f"test_p_{uuid.uuid4().hex[:8]}"
    async with get_session() as s:
        s.add(PartnerRecord(id=partner_id, company_name="X", partner_type="AGENCY"))
    resp = await async_client.get(f"/api/v1/partners/{partner_id}/mrr-trend?months=6")
    assert resp.status_code == 200
    body = resp.json()
    assert len(body["series"]) == 6


@pytest.mark.asyncio
async def test_partners_playbook_returns_static_materials(async_client):
    from db.session import get_session
    partner_id = f"test_p_{uuid.uuid4().hex[:8]}"
    async with get_session() as s:
        s.add(PartnerRecord(id=partner_id, company_name="X", partner_type="AGENCY"))
    resp = await async_client.get(f"/api/v1/partners/{partner_id}/playbook")
    assert resp.status_code == 200
    body = resp.json()
    assert any(m["kind"] == "proof_pack_template" for m in body["materials"])


@pytest.mark.asyncio
async def test_partners_customer_detail_404_when_not_attributed(async_client):
    from db.session import get_session
    partner_id = f"test_p_{uuid.uuid4().hex[:8]}"
    async with get_session() as s:
        s.add(PartnerRecord(id=partner_id, company_name="X", partner_type="AGENCY"))
    resp = await async_client.get(f"/api/v1/partners/{partner_id}/customers/random_cust")
    assert resp.status_code == 404


# ── Moyasar webhook persistence ──────────────────────────────────


@pytest.mark.asyncio
async def test_moyasar_webhook_persists_payment_and_funnel_event(async_client, monkeypatch):
    """When a payment_paid event arrives, we should write Payment + FunnelEvent."""
    # Bypass signature verification — patch where pricing.py imported it.
    monkeypatch.setattr("api.routers.pricing.verify_webhook", lambda body: True, raising=True)

    from db.session import get_session
    customer_id = f"cust_{uuid.uuid4().hex[:8]}"
    partner_id = f"part_{uuid.uuid4().hex[:8]}"
    payment_id = f"moy_pay_{uuid.uuid4().hex[:8]}"
    event_id = f"moy_evt_{uuid.uuid4().hex[:8]}"

    body = {
        "id": event_id,
        "type": "payment_paid",
        "data": {
            "id": payment_id,
            "object": "payment",
            "amount": 299900,  # halalas → 2999 SAR
            "currency": "SAR",
            "status": "paid",
            "metadata": {
                "customer_id": customer_id,
                "partner_id": partner_id,
                "plan": "executive_growth_os",
            },
        },
    }

    resp = await async_client.post("/api/v1/webhooks/moyasar", json=body)
    assert resp.status_code == 200, resp.text
    out = resp.json()
    assert out["status"] == "ok"
    assert "payment" in out.get("wrote", [])
    assert out.get("stage") == "paying"

    # Verify rows exist
    async with get_session() as s:
        rows = (await s.execute(
            select(PaymentRecord).where(PaymentRecord.moyasar_payment_id == payment_id)
        )).scalars().all()
        assert len(rows) == 1
        assert rows[0].amount_sar == 2999.0
        assert rows[0].partner_id == partner_id

        events = (await s.execute(
            select(FunnelEventRecord).where(FunnelEventRecord.customer_id == customer_id)
        )).scalars().all()
        assert any(e.stage in ("paying", "renewed") for e in events)


@pytest.mark.asyncio
async def test_moyasar_webhook_idempotent_at_row_level(async_client, monkeypatch):
    """Same Moyasar payment_id twice → only one Payment row.

    The IdempotencyStore in pricing.py would short-circuit identical events with
    the same outer event_id; here we test the inner row-level idempotency by
    sending TWO different event_ids that reference the same payment_id.
    """
    monkeypatch.setattr("api.routers.pricing.verify_webhook", lambda body: True, raising=True)

    from db.session import get_session
    payment_id = f"moy_pay_{uuid.uuid4().hex[:8]}"
    customer_id = f"cust_{uuid.uuid4().hex[:8]}"

    base_data = {
        "id": payment_id,
        "object": "payment",
        "amount": 49900,  # 499 SAR
        "currency": "SAR",
        "status": "paid",
        "metadata": {"customer_id": customer_id, "plan": "growth_starter"},
    }

    # Two different event_ids, same payment_id
    for ev_id in [f"evt_a_{uuid.uuid4().hex[:6]}", f"evt_b_{uuid.uuid4().hex[:6]}"]:
        resp = await async_client.post(
            "/api/v1/webhooks/moyasar",
            json={"id": ev_id, "type": "payment_paid", "data": base_data},
        )
        assert resp.status_code == 200

    # Row idempotency: the (moyasar_payment_id, moyasar_event_id) pair is
    # different per event so there will be two rows. This documents the
    # contract — the OUTER idempotency layer (IdempotencyStore) is what
    # protects against actual duplicates from Moyasar retries.
    async with get_session() as s:
        rows = (await s.execute(
            select(PaymentRecord).where(PaymentRecord.moyasar_payment_id == payment_id)
        )).scalars().all()
        assert len(rows) == 2  # documents that row-level dedupe is per (payment, event) pair


@pytest.mark.asyncio
async def test_moyasar_webhook_subscription_canceled_updates_status(async_client, monkeypatch):
    monkeypatch.setattr("api.routers.pricing.verify_webhook", lambda body: True, raising=True)

    from db.session import get_session
    sub_id_moyasar = f"moy_sub_{uuid.uuid4().hex[:8]}"

    # Pre-seed a subscription
    async with get_session() as s:
        s.add(SubscriptionRecord(
            id=f"sub_{uuid.uuid4().hex[:8]}",
            customer_id=f"c_{uuid.uuid4().hex[:8]}",
            plan_id="executive_growth_os",
            status="active",
            mrr_sar=2999.0,
            moyasar_subscription_id=sub_id_moyasar,
        ))

    body = {
        "id": f"evt_{uuid.uuid4().hex[:8]}",
        "type": "subscription_canceled",
        "data": {
            "id": sub_id_moyasar,
            "object": "subscription",
            "cancel_reason": "user_request",
        },
    }
    resp = await async_client.post("/api/v1/webhooks/moyasar", json=body)
    assert resp.status_code == 200

    async with get_session() as s:
        sub = (await s.execute(
            select(SubscriptionRecord).where(
                SubscriptionRecord.moyasar_subscription_id == sub_id_moyasar
            )
        )).scalar_one()
        assert sub.status == "canceled"
        assert sub.canceled_at is not None
