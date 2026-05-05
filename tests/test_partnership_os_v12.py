"""V12 Phase 8 — Partnership OS tests."""
from __future__ import annotations

import pytest
from httpx import ASGITransport, AsyncClient

from auto_client_acquisition.partnership_os import (
    Partner,
    compute_fit_score,
    recommend_motion,
    reset_referrals,
)


# ─────────────── Pure-function tests ────────────


def test_fit_score_high_for_aligned_partner() -> None:
    p = Partner(
        partner_id="p1",
        placeholder_name="Partner-A",
        partner_type="sales_consultant",
        sector="b2b_services",
        region="riyadh",
    )
    score = compute_fit_score(
        partner=p,
        customer_segment="b2b_services",
        serves_b2b=True,
        has_existing_customers=True,
        saudi_market_focus=True,
    )
    assert score >= 80


def test_fit_score_low_for_misaligned_partner() -> None:
    p = Partner(
        partner_id="p2",
        placeholder_name="Partner-B",
        partner_type="consulting_firm",
        sector="manufacturing",
        region="paris",
    )
    score = compute_fit_score(
        partner=p,
        customer_segment="b2b_services",
        serves_b2b=False,
        has_existing_customers=False,
        saudi_market_focus=False,
    )
    assert score < 60


def test_motion_no_white_label_before_3_paid_pilots() -> None:
    p = Partner(
        partner_id="p3", placeholder_name="Partner-C",
        partner_type="sales_consultant", sector="b2b_services", region="riyadh",
    )
    motion = recommend_motion(
        partner=p, fit_score=95, paid_pilots_count=2, has_referral_data=True,
    )
    # Even with high fit + referral data, must not be white_label until 3 pilots
    assert motion.motion != "white_label_with_revenue_share"


def test_motion_no_revenue_share_without_referral_data() -> None:
    p = Partner(
        partner_id="p4", placeholder_name="Partner-D",
        partner_type="sales_consultant", sector="b2b_services", region="riyadh",
    )
    motion = recommend_motion(
        partner=p, fit_score=95, paid_pilots_count=5, has_referral_data=False,
    )
    assert "revenue_share" not in motion.motion


def test_motion_white_label_only_when_fully_qualified() -> None:
    p = Partner(
        partner_id="p5", placeholder_name="Partner-E",
        partner_type="sales_consultant", sector="b2b_services", region="riyadh",
    )
    motion = recommend_motion(
        partner=p, fit_score=95, paid_pilots_count=5, has_referral_data=True,
    )
    assert motion.motion == "white_label_with_revenue_share"


def test_motion_low_fit_returns_no_fit_blocked() -> None:
    p = Partner(
        partner_id="p6", placeholder_name="Partner-F",
        partner_type="consulting_firm", sector="other", region="other",
    )
    motion = recommend_motion(partner=p, fit_score=20)
    assert motion.motion == "no_fit"
    assert motion.blocked is True


# ─────────────── Router tests ────────────


@pytest.mark.asyncio
async def test_status() -> None:
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.get("/api/v1/partnership-os/status")
    assert r.status_code == 200
    body = r.json()
    assert body["service"] == "partnership_os"
    assert body["hard_gates"]["no_white_label_before_3_paid_pilots"] is True
    assert body["hard_gates"]["no_exclusivity"] is True


@pytest.mark.asyncio
async def test_fit_score_endpoint() -> None:
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.post(
            "/api/v1/partnership-os/fit-score",
            json={
                "partner_id": "partner_test",
                "placeholder_name": "Partner-A",
                "partner_type": "sales_consultant",
                "sector": "b2b_services",
                "region": "riyadh",
                "customer_segment": "b2b_services",
                "paid_pilots_count": 0,
                "has_referral_data": False,
            },
        )
    body = r.json()
    assert body["score"] >= 70
    # Without 3 paid pilots → not white-label
    assert body["motion"] != "white_label_with_revenue_share"


@pytest.mark.asyncio
async def test_intro_draft_is_draft_only() -> None:
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.post(
            "/api/v1/partnership-os/intro-draft",
            json={
                "partner_placeholder_name": "Partner-A",
                "customer_placeholder": "Customer-Slot-A",
            },
        )
    body = r.json()
    assert body["action_mode"] == "draft_only"
    assert body["send_method"] == "manual_only"


@pytest.mark.asyncio
async def test_log_referral() -> None:
    from api.main import app

    reset_referrals()
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.post(
            "/api/v1/partnership-os/log-referral",
            json={
                "partner_id": "partner_test",
                "customer_placeholder": "Customer-Slot-A",
            },
        )
    body = r.json()
    assert body["referral"]["partner_id"] == "partner_test"
    assert body["total_for_partner"] == 1
