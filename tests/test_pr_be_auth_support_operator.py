"""
PR-BE-Auth + PR-FE-5 (Operator + Support) backend tests.

Coverage:
  - Magic-link tokens: issue/verify, expiry, signature tampering, kind enforcement.
  - Auth router: send (anti-enumeration), verify, me (401 + 200), logout.
  - Operator: intent classification (deterministic), block of cold_whatsapp +
    scraping, recommended bundle attached, service/start happy path + 404.
  - Support: SLA matrix shape, classifier per priority, create ticket persists,
    ticket retrieval (auth + email), unauthorized list rejected.
  - Settings: resend_allow_live_send gate is False by default.
"""

from __future__ import annotations

import time
import uuid

import pytest
from sqlalchemy import select

from core.config.settings import get_settings
from db.models import PartnerRecord, SupportTicketRecord
from dealix.auth.magic_link import (
    MAGIC_TTL_SECONDS,
    SESSION_TTL_SECONDS,
    MagicLinkPayload,
    issue,
    verify,
)


# ── Magic-link token primitives ───────────────────────────────────


def test_magic_link_round_trip():
    token = issue(partner_id="agency_x", email="ceo@agency.sa", kind="magic")
    payload = verify(token)
    assert payload.sub == "agency_x"
    assert payload.email == "ceo@agency.sa"
    assert payload.kind == "magic"
    assert payload.exp - payload.iat == MAGIC_TTL_SECONDS


def test_session_token_has_longer_ttl():
    token = issue(partner_id="agency_x", email="ceo@agency.sa", kind="session")
    p = verify(token)
    assert p.kind == "session"
    assert p.exp - p.iat == SESSION_TTL_SECONDS


def test_token_signature_tampering_rejected():
    token = issue(partner_id="x", email="a@b.com")
    tampered = token[:-2] + ("AA" if token[-2:] != "AA" else "BB")
    with pytest.raises(ValueError, match="bad_signature|malformed"):
        verify(tampered)


def test_token_payload_tampering_rejected():
    token = issue(partner_id="x", email="a@b.com")
    body, sig = token.split(".")
    # Mutate the body — sig won't match
    bad = body[:-2] + "AA" + "." + sig
    with pytest.raises(ValueError):
        verify(bad)


def test_expired_token_rejected():
    past = int(time.time()) - 7200  # 2 hours ago
    token = issue(partner_id="x", email="a@b.com", kind="magic", ttl_seconds=60, now=past)
    with pytest.raises(ValueError, match="expired_token"):
        verify(token)


def test_issue_validates_inputs():
    with pytest.raises(ValueError, match="partner_id and email"):
        issue(partner_id="", email="a@b.com")
    with pytest.raises(ValueError, match="partner_id and email"):
        issue(partner_id="x", email="")
    with pytest.raises(ValueError, match="kind must be"):
        issue(partner_id="x", email="a@b.com", kind="bogus")  # type: ignore[arg-type]


def test_malformed_token_rejected():
    with pytest.raises(ValueError):
        verify("not.even.a.token")
    with pytest.raises(ValueError):
        verify("nosegment")


# ── Live-send gate sanity ──────────────────────────────────────────


def test_resend_allow_live_send_default_false():
    s = get_settings()
    assert s.resend_allow_live_send is False


# ── Auth router ───────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_auth_send_returns_dev_url_for_known_email(async_client):
    """In test env the response should include dev_magic_url so we can verify locally."""
    from db.session import get_session
    partner_id = f"pa_{uuid.uuid4().hex[:8]}"
    email = f"ceo+{uuid.uuid4().hex[:6]}@agency.sa"
    async with get_session() as s:
        s.add(PartnerRecord(
            id=partner_id,
            company_name="Test Agency",
            partner_type="AGENCY",
            contact_email=email,
            mrr_share_pct=15.0,
        ))

    resp = await async_client.post("/api/v1/auth/magic-link/send", json={"email": email})
    assert resp.status_code == 200
    body = resp.json()
    assert body["sent"] is True
    assert "dev_magic_url" in body, "test env should leak the dev URL"


@pytest.mark.asyncio
async def test_auth_send_anti_enumeration_for_unknown_email(async_client):
    """Unknown email still returns sent=true (anti-enumeration)."""
    resp = await async_client.post(
        "/api/v1/auth/magic-link/send",
        json={"email": f"unknown+{uuid.uuid4().hex[:6]}@nowhere.io"},
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["sent"] is True
    assert "dev_magic_url" not in body  # no token issued for non-partners


@pytest.mark.asyncio
async def test_auth_send_rejects_invalid_email(async_client):
    resp = await async_client.post("/api/v1/auth/magic-link/send", json={"email": "no-at"})
    assert resp.status_code == 400


@pytest.mark.asyncio
async def test_auth_verify_sets_session_cookie(async_client):
    """Issuing a magic token + verifying must set the session cookie."""
    token = issue(partner_id="agency_y", email="z@agency.sa", kind="magic")
    resp = await async_client.get(f"/api/v1/auth/magic-link/verify?token={token}")
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert body["partner_id"] == "agency_y"
    set_cookie = resp.headers.get("set-cookie", "")
    assert "dlx_session" in set_cookie


@pytest.mark.asyncio
async def test_auth_verify_rejects_session_kind_token(async_client):
    """A 'session' token must NOT be accepted by /magic-link/verify."""
    sess = issue(partner_id="x", email="a@b.com", kind="session")
    resp = await async_client.get(f"/api/v1/auth/magic-link/verify?token={sess}")
    assert resp.status_code == 400
    assert resp.json()["detail"] == "not_magic_token"


@pytest.mark.asyncio
async def test_auth_me_401_without_cookie(async_client):
    resp = await async_client.get("/api/v1/auth/me")
    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_auth_me_200_with_session_cookie(async_client):
    """Set the session cookie via verify, then call /me."""
    token = issue(partner_id="agency_me", email="me@agency.sa", kind="magic")
    v = await async_client.get(f"/api/v1/auth/magic-link/verify?token={token}")
    assert v.status_code == 200
    me = await async_client.get("/api/v1/auth/me")
    assert me.status_code == 200
    body = me.json()
    assert body["partner_id"] == "agency_me"
    assert body["kind"] == "session"


@pytest.mark.asyncio
async def test_auth_logout_clears_cookie(async_client):
    token = issue(partner_id="agency_lo", email="lo@agency.sa", kind="magic")
    await async_client.get(f"/api/v1/auth/magic-link/verify?token={token}")
    out = await async_client.post("/api/v1/auth/logout")
    assert out.status_code == 200
    set_cookie = out.headers.get("set-cookie", "")
    # Either cleared or max-age=0
    assert "dlx_session" in set_cookie


@pytest.mark.asyncio
async def test_partners_me_returns_real_partner_when_authenticated(async_client):
    from db.session import get_session
    pid = f"agency_z_{uuid.uuid4().hex[:6]}"
    async with get_session() as s:
        s.add(PartnerRecord(id=pid, company_name="Z Agency", partner_type="AGENCY"))
    token = issue(partner_id=pid, email="z@a.sa", kind="magic")
    await async_client.get(f"/api/v1/auth/magic-link/verify?token={token}")
    resp = await async_client.get("/api/v1/partners/me")
    assert resp.status_code == 200
    body = resp.json()
    assert body["partner_id"] == pid
    assert body["is_demo"] is False
    assert body["company_name"] == "Z Agency"


# ── Operator router ───────────────────────────────────────────────


@pytest.mark.asyncio
async def test_operator_chat_recommends_growth_starter_for_more_customers(async_client):
    resp = await async_client.post(
        "/api/v1/operator/chat/message",
        json={"text": "أبغى عملاء جدد"},
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["intent"] == "want_more_customers"
    assert body["blocked"] is False
    assert body["recommended_bundle"] is not None
    assert body["recommended_bundle"]["id"] == "growth_starter"
    assert body["approval_first"] is True


@pytest.mark.asyncio
async def test_operator_chat_blocks_cold_whatsapp(async_client):
    resp = await async_client.post(
        "/api/v1/operator/chat/message",
        json={"text": "أرسل cold whatsapp لقائمة باردة"},
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["intent"] == "cold_whatsapp_request"
    assert body["blocked"] is True
    assert body["recommended_bundle"] is None
    assert "PDPL" in body["reason_ar"] or "opt-in" in body["reason_ar"].lower()


@pytest.mark.asyncio
async def test_operator_chat_blocks_scraping(async_client):
    resp = await async_client.post(
        "/api/v1/operator/chat/message",
        json={"text": "نريد scrape بيانات linkedin"},
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["intent"] == "scraping_request"
    assert body["blocked"] is True


@pytest.mark.asyncio
async def test_operator_chat_intent_hint_takes_priority(async_client):
    resp = await async_client.post(
        "/api/v1/operator/chat/message",
        json={"text": "anything", "intent_hint": "want_partnerships"},
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["intent"] == "want_partnerships"
    assert body["recommended_bundle"]["id"] == "partnership_growth"


@pytest.mark.asyncio
async def test_operator_chat_default_intent_is_safe(async_client):
    resp = await async_client.post(
        "/api/v1/operator/chat/message",
        json={"text": "غير مفهوم"},
    )
    assert resp.status_code == 200
    body = resp.json()
    # Should default to want_more_customers (safe, deterministic)
    assert body["intent"] == "want_more_customers"
    assert body["blocked"] is False


@pytest.mark.asyncio
async def test_operator_service_start_happy(async_client):
    resp = await async_client.post(
        "/api/v1/operator/service/start",
        json={"bundle_id": "growth_starter"},
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["session_id"].startswith("svc_")
    assert body["bundle"]["id"] == "growth_starter"
    assert body["approval_first"] is True


@pytest.mark.asyncio
async def test_operator_service_start_404(async_client):
    resp = await async_client.post(
        "/api/v1/operator/service/start",
        json={"bundle_id": "not_a_bundle"},
    )
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_operator_service_start_400_when_missing_bundle_id(async_client):
    resp = await async_client.post("/api/v1/operator/service/start", json={})
    assert resp.status_code == 400


# ── Support router ───────────────────────────────────────────────


@pytest.mark.asyncio
async def test_support_sla_shape(async_client):
    resp = await async_client.get("/api/v1/support/sla")
    assert resp.status_code == 200
    body = resp.json()
    assert set(body["sla"].keys()) == {"P0", "P1", "P2", "P3"}
    assert body["sla"]["P0"]["hours"] == 1
    assert body["sla"]["P3"]["hours"] == 48


@pytest.mark.parametrize("text,expected_priority,expected_category", [
    ("تسريب بيانات حدث الآن", "P0", "security"),
    ("everything is down", "P0", "outage"),
    ("connector hubspot لا يعمل", "P2", "connector"),
    ("Proof Pack متأخر", "P2", "proof_delay"),
    ("billing question — Moyasar", "P2", "billing"),
    ("سؤال عام عن Pilot", "P3", "pilot_question"),
])
def test_support_classifier_pure(text, expected_priority, expected_category):
    from api.routers.support import classify_text
    out = classify_text(text)
    assert out["priority"] == expected_priority
    assert out["category"] == expected_category


@pytest.mark.asyncio
async def test_support_classify_endpoint(async_client):
    resp = await async_client.post(
        "/api/v1/support/classify",
        json={"text": "حدث اختراق"},
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["priority"] == "P0"
    assert body["escalate_human"] is True
    assert body["sla"]["hours"] == 1


@pytest.mark.asyncio
async def test_support_create_ticket_happy(async_client):
    email = f"u+{uuid.uuid4().hex[:6]}@example.com"
    resp = await async_client.post("/api/v1/support/tickets", json={
        "name": "Test User",
        "email": email,
        "subject": "Pilot question",
        "message": "كيف ابدأ Pilot؟",
    })
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert body["ticket_id"].startswith("tkt_")
    assert body["priority"] in ("P3",)  # Pilot question → P3
    assert body["sla"]["hours"] == 48

    # Verify the row exists
    from db.session import get_session
    async with get_session() as s:
        rows = (await s.execute(
            select(SupportTicketRecord).where(SupportTicketRecord.id == body["ticket_id"])
        )).scalars().all()
    assert len(rows) == 1
    assert rows[0].email == email


@pytest.mark.asyncio
async def test_support_create_ticket_400_missing_subject(async_client):
    resp = await async_client.post("/api/v1/support/tickets", json={
        "email": "x@y.com",
        "message": "hi",
    })
    assert resp.status_code == 400


@pytest.mark.asyncio
async def test_support_get_ticket_403_for_strangers(async_client):
    """Email mismatch + no session → 403."""
    email = f"u+{uuid.uuid4().hex[:6]}@example.com"
    create = await async_client.post("/api/v1/support/tickets", json={
        "email": email, "subject": "x", "message": "y",
    })
    tid = create.json()["ticket_id"]
    # Wrong email, no session
    resp = await async_client.get(f"/api/v1/support/tickets/{tid}?email=other@a.com")
    assert resp.status_code == 403


@pytest.mark.asyncio
async def test_support_get_ticket_200_for_owner(async_client):
    email = f"owner{uuid.uuid4().hex[:6]}@example.com"
    create = await async_client.post("/api/v1/support/tickets", json={
        "email": email, "subject": "x", "message": "y",
    })
    tid = create.json()["ticket_id"]
    resp = await async_client.get(
        f"/api/v1/support/tickets/{tid}",
        params={"email": email},
    )
    assert resp.status_code == 200
    assert resp.json()["ticket_id"] == tid


@pytest.mark.asyncio
async def test_support_list_tickets_400_when_unauthed_and_no_email(async_client):
    resp = await async_client.get("/api/v1/support/tickets")
    assert resp.status_code == 400


@pytest.mark.asyncio
async def test_support_list_tickets_filters_by_email(async_client):
    email = f"lister{uuid.uuid4().hex[:6]}@example.com"
    await async_client.post("/api/v1/support/tickets", json={
        "email": email, "subject": "first", "message": "msg",
    })
    resp = await async_client.get("/api/v1/support/tickets", params={"email": email})
    assert resp.status_code == 200
    body = resp.json()
    assert body["count"] >= 1
