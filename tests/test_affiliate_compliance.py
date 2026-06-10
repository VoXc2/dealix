"""Affiliate / partner messaging compliance."""

from __future__ import annotations

from dealix.revenue_ops_autopilot.affiliate_compliance import (
    has_affiliate_disclosure,
    scan_affiliate_message,
)


def test_blocks_misleading_guarantee():
    s = scan_affiliate_message(
        "Dealix تضمن لك نمو الإيراد وتؤتمت كل مبيعاتك تلقائياً بدون تدخل.",
    )
    assert s.blocked is True
    assert not s.allowed


def test_disclosure_detection():
    assert has_affiliate_disclosure("محتوى ترويجي · إفصاح شراكة مع Dealix")
    assert not has_affiliate_disclosure("نص تسويقي بدون إفصاح")


def test_partner_apply_api_blocks_bad_message():
    from fastapi.testclient import TestClient

    from api.main import app

    cli = TestClient(app)
    r = cli.post(
        "/api/v1/public/partner-apply",
        json={
            "name": "Bad Partner",
            "email": "bad@example.com",
            "company": "Co",
            "partner_type": "referral",
            "message": "Dealix تضمن لك نمو الإيراد 100%",
            "consent": True,
        },
    )
    assert r.status_code == 422
    assert r.json()["detail"]["reason"] == "affiliate_compliance_blocked"


def test_targeting_today_endpoint(monkeypatch):
    monkeypatch.setenv("ADMIN_API_KEYS", "dev")
    from fastapi.testclient import TestClient

    from api.main import app

    cli = TestClient(app)
    r = cli.get(
        "/api/v1/ops-autopilot/targeting/today",
        headers={"X-Admin-API-Key": "dev"},
        params={"top_n": 3},
    )
    assert r.status_code == 200, r.text
    assert "targets" in r.json()


def test_marketing_calendar_patch(monkeypatch):
    monkeypatch.setenv("ADMIN_API_KEYS", "dev")
    from fastapi.testclient import TestClient

    from api.main import app

    cli = TestClient(app)
    headers = {"X-Admin-API-Key": "dev"}
    listed = cli.get("/api/v1/ops-autopilot/marketing/calendar", headers=headers)
    assert listed.status_code == 200
    items = listed.json().get("items") or []
    if not items:
        created = cli.post(
            "/api/v1/ops-autopilot/marketing/calendar",
            headers=headers,
            json={
                "scheduled_date": "2026-06-01",
                "channel": "linkedin",
                "title_ar": "اختبار",
                "body_draft_ar": "نص اختبار محكوم",
            },
        )
        assert created.status_code == 200
        slot_id = created.json()["item"]["id"]
    else:
        slot_id = items[0]["id"]
    patched = cli.patch(
        f"/api/v1/ops-autopilot/marketing/calendar/{slot_id}",
        headers=headers,
        json={"status": "approved"},
    )
    assert patched.status_code == 200
    assert patched.json()["item"]["status"] == "approved"
