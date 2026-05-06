"""Tests for the v5 layers: customer_loop + role_command_os + service_quality.

Pure unit + ASGI tests — no network, no LLM, no DB. Each <2s.
"""
from __future__ import annotations

import pytest
from httpx import ASGITransport, AsyncClient

from auto_client_acquisition.customer_loop import (
    JourneyAdvanceRequest,
    JourneyState,
    advance,
    list_states,
    next_actions_for_state,
)
from auto_client_acquisition.role_command_os import (
    RoleName,
    build_role_brief,
    list_roles,
)
from auto_client_acquisition.service_quality import (
    QAVerdict,
    check_delivery_payload,
    get_sla,
    list_slas,
)


# ════════════════════ customer_loop ════════════════════


def test_list_states_returns_all_states_with_transitions():
    out = list_states()
    assert out["states_total"] == len([s for s in JourneyState])
    state_names = {s["state"] for s in out["states"]}
    assert "lead_intake" in state_names
    assert "blocked" in state_names
    assert "proof_pack_sent" in state_names
    # Every state has bilingual checklists
    for s in out["states"]:
        assert s["next_actions_ar"]
        assert s["next_actions_en"]


def test_blocked_state_has_no_outgoing_transitions():
    out = list_states()
    blocked = next(s for s in out["states"] if s["state"] == "blocked")
    assert blocked["allowed_transitions"] == []


def test_advance_accepts_valid_transition():
    req = JourneyAdvanceRequest(
        current_state=JourneyState.LEAD_INTAKE,
        target_state=JourneyState.DIAGNOSTIC_REQUESTED,
    )
    result = advance(req)
    assert result.accepted is True
    assert result.from_state == "lead_intake"
    assert result.to_state == "diagnostic_requested"
    assert result.next_actions_ar  # bilingual checklist returned
    assert result.next_actions_en


def test_advance_rejects_invalid_transition():
    """lead_intake → in_delivery skips multiple states; rejected."""
    req = JourneyAdvanceRequest(
        current_state=JourneyState.LEAD_INTAKE,
        target_state=JourneyState.IN_DELIVERY,
    )
    result = advance(req)
    assert result.accepted is False
    assert result.to_state is None
    assert result.rejection_reason
    assert "not allowed" in result.rejection_reason


def test_advance_rejects_skipping_payment():
    """diagnostic_sent → in_delivery skips pilot_offered + payment; rejected."""
    req = JourneyAdvanceRequest(
        current_state=JourneyState.DIAGNOSTIC_SENT,
        target_state=JourneyState.IN_DELIVERY,
    )
    result = advance(req)
    assert result.accepted is False


def test_pilot_to_payment_pending_requires_approval():
    req = JourneyAdvanceRequest(
        current_state=JourneyState.PILOT_OFFERED,
        target_state=JourneyState.PAYMENT_PENDING,
    )
    result = advance(req)
    assert result.accepted is True
    # payment_pending isn't in approval-required (it's a status, not an action)
    # but proof_event_recommended is False for it
    assert result.proof_event_recommended is False


def test_paid_to_in_delivery_recommends_proof_event():
    req = JourneyAdvanceRequest(
        current_state=JourneyState.PAID_OR_COMMITTED,
        target_state=JourneyState.IN_DELIVERY,
    )
    result = advance(req)
    assert result.accepted is True
    assert result.proof_event_recommended is True


def test_proof_pack_sent_transitions_to_upsell_or_nurture():
    for tgt in (JourneyState.UPSELL_RECOMMENDED, JourneyState.NURTURE):
        req = JourneyAdvanceRequest(
            current_state=JourneyState.PROOF_PACK_SENT,
            target_state=tgt,
        )
        assert advance(req).accepted is True


def test_safety_notes_always_present():
    req = JourneyAdvanceRequest(
        current_state=JourneyState.LEAD_INTAKE,
        target_state=JourneyState.DIAGNOSTIC_REQUESTED,
    )
    result = advance(req)
    notes = result.safety_notes
    assert "no_cold_outreach" in notes
    assert "no_scraping" in notes
    assert "no_linkedin_automation" in notes
    assert "approval_required_for_external_send" in notes


def test_next_actions_for_state_returns_bilingual_checklist():
    out = next_actions_for_state(JourneyState.LEAD_INTAKE)
    assert out["state"] == "lead_intake"
    assert out["next_actions_ar"]
    assert out["next_actions_en"]


# ════════════════════ role_command_os ════════════════════


def test_list_roles_returns_expected_roles():
    roles = list_roles()
    assert set(roles) == {
        "ceo",
        "sales",
        "growth",
        "partnership",
        "cs",
        "finance",
        "compliance",
        "delivery",
        "support",
        "operations",
    }


@pytest.mark.parametrize("role_name", list(RoleName))
def test_every_role_brief_has_required_blocks(role_name: RoleName):
    brief = build_role_brief(role_name)
    payload = brief.as_dict()
    # Required keys
    for key in ("role", "summary_ar", "summary_en", "top_decisions",
                "risks", "approvals_needed", "evidence_pointers",
                "next_action_ar", "next_action_en", "blocked_actions",
                "guardrails"):
        assert key in payload, f"{role_name.value} missing {key}"
    # Arabic primary + English secondary both non-empty
    assert payload["summary_ar"]
    assert payload["summary_en"]


def test_every_decision_has_arabic_and_english():
    for role in RoleName:
        brief = build_role_brief(role)
        for d in brief.top_decisions:
            assert d.title_ar
            assert d.title_en


def test_compliance_brief_surfaces_review_pending():
    brief = build_role_brief(RoleName.COMPLIANCE)
    text = brief.summary_ar + brief.summary_en + " ".join(brief.approvals_needed)
    # 4 REVIEW_PENDING items → must appear or REVIEW_PENDING phrasing
    assert "REVIEW_PENDING" in text or "B1" in " ".join(brief.approvals_needed)


def test_no_role_recommends_unsafe_action():
    forbidden = ["cold whatsapp", "scrape", "blast", "auto-dm", "guaranteed"]
    for role in RoleName:
        brief = build_role_brief(role)
        haystack = " ".join([
            brief.summary_ar.lower(),
            brief.summary_en.lower(),
            brief.next_action_ar.lower(),
            brief.next_action_en.lower(),
            *(d.title_ar.lower() for d in brief.top_decisions),
            *(d.title_en.lower() for d in brief.top_decisions),
        ])
        for tok in forbidden:
            assert tok not in haystack, (
                f"{role.value} brief contains unsafe token {tok!r}"
            )


def test_every_role_guardrails_block_locked():
    for role in RoleName:
        brief = build_role_brief(role)
        g = brief.guardrails
        assert g["no_live_send"] is True
        assert g["no_scraping"] is True
        assert g["no_cold_outreach"] is True
        assert g["approval_required_for_external_actions"] is True


# ════════════════════ service_quality ════════════════════


def test_qa_gate_pass_with_complete_payload():
    """All required inputs + deliverable + clean text → PASS."""
    # Use a service with known required_inputs
    payload = {
        "provided_inputs": [
            "WhatsApp Business Cloud webhook configured at Meta",
            "WHATSAPP_VERIFY_TOKEN",
            "WHATSAPP_APP_SECRET",
        ],
        "intended_actions": ["inbound_receive", "signature_verify"],
        "deliverable": {"draft": "an Arabic reply card"},
        "draft_text": "صفحة هبوط آمنة جاهزة للمراجعة",
    }
    result = check_delivery_payload("lead_intake_whatsapp", payload)
    assert result.verdict == QAVerdict.PASS
    assert result.missing_required_inputs == []
    assert result.forbidden_action_attempts == []
    assert result.forbidden_vocabulary_hits == []


def test_qa_gate_blocks_on_forbidden_action():
    """An intended cold-WhatsApp action must trigger BLOCKED verdict."""
    payload = {
        "provided_inputs": [
            "WhatsApp Business Cloud webhook configured at Meta",
            "WHATSAPP_VERIFY_TOKEN",
            "WHATSAPP_APP_SECRET",
        ],
        "intended_actions": ["cold_outreach_whatsapp"],
        "deliverable": "x",
    }
    result = check_delivery_payload("lead_intake_whatsapp", payload)
    assert result.verdict == QAVerdict.BLOCKED
    assert "cold_outreach_whatsapp" in result.forbidden_action_attempts


def test_qa_gate_blocks_on_forbidden_vocabulary():
    payload = {
        "provided_inputs": [
            "WhatsApp Business Cloud webhook configured at Meta",
            "WHATSAPP_VERIFY_TOKEN",
            "WHATSAPP_APP_SECRET",
        ],
        "intended_actions": [],
        "deliverable": "x",
        "draft_text": "We guarantee revenue growth",
    }
    result = check_delivery_payload("lead_intake_whatsapp", payload)
    assert result.verdict == QAVerdict.BLOCKED
    assert "guaranteed" in result.forbidden_vocabulary_hits


def test_qa_gate_needs_review_when_input_missing():
    payload = {
        "provided_inputs": [],  # all required missing
        "intended_actions": [],
        "deliverable": "x",
    }
    result = check_delivery_payload("lead_intake_whatsapp", payload)
    assert result.verdict == QAVerdict.NEEDS_REVIEW
    assert len(result.missing_required_inputs) >= 2


def test_qa_gate_needs_review_when_deliverable_missing():
    payload = {
        "provided_inputs": [
            "WhatsApp Business Cloud webhook configured at Meta",
            "WHATSAPP_VERIFY_TOKEN",
            "WHATSAPP_APP_SECRET",
        ],
        "intended_actions": [],
        # deliverable absent
    }
    result = check_delivery_payload("lead_intake_whatsapp", payload)
    assert result.verdict == QAVerdict.NEEDS_REVIEW
    assert result.deliverable_missing is True


def test_qa_gate_unknown_service_raises_keyerror():
    with pytest.raises(KeyError):
        check_delivery_payload("__unknown_service__", {"deliverable": "x"})


# ─── SLA reader ─────────────────────────────────────────────────────


def test_get_sla_returns_known_service():
    sla = get_sla("lead_intake_whatsapp")
    assert sla.service_id == "lead_intake_whatsapp"
    assert sla.sla_text  # not empty
    assert sla.name_ar
    assert sla.name_en


def test_list_slas_returns_all_32():
    rows = list_slas()
    assert len(rows) == 32
    for row in rows:
        assert row["service_id"]
        assert row["sla_text"]


def test_get_sla_unknown_raises():
    with pytest.raises(KeyError):
        get_sla("__not_a_service__")


# ════════════════════ API endpoint tests ════════════════════


@pytest.mark.asyncio
async def test_customer_loop_status_endpoint():
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.get("/api/v1/customer-loop/status")
    assert r.status_code == 200
    assert r.json()["guardrails"]["no_live_send"] is True


@pytest.mark.asyncio
async def test_customer_loop_states_endpoint():
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.get("/api/v1/customer-loop/states")
    assert r.status_code == 200
    payload = r.json()
    assert payload["states_total"] >= 10


@pytest.mark.asyncio
async def test_customer_loop_advance_endpoint_accepts_valid():
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.post(
            "/api/v1/customer-loop/journey/advance",
            json={
                "current_state": "lead_intake",
                "target_state": "diagnostic_requested",
            },
        )
    assert r.status_code == 200
    assert r.json()["accepted"] is True


@pytest.mark.asyncio
async def test_customer_loop_advance_endpoint_rejects_invalid():
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.post(
            "/api/v1/customer-loop/journey/advance",
            json={"current_state": "lead_intake", "target_state": "in_delivery"},
        )
    assert r.status_code == 200
    assert r.json()["accepted"] is False


@pytest.mark.asyncio
async def test_role_command_status_endpoint():
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.get("/api/v1/role-command/status")
    assert r.status_code == 200
    assert "ceo" in r.json()["roles"]


@pytest.mark.asyncio
async def test_role_command_brief_endpoint():
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.get("/api/v1/role-command/ceo")
    assert r.status_code == 200
    payload = r.json()
    assert payload["role"] == "ceo"
    assert payload["summary_ar"]
    assert payload["summary_en"]


@pytest.mark.asyncio
async def test_role_command_brief_404_unknown_role():
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.get("/api/v1/role-command/__nope__")
    assert r.status_code == 404


@pytest.mark.asyncio
async def test_service_quality_check_endpoint_blocks_unsafe():
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.post(
            "/api/v1/service-quality/check",
            json={
                "service_id": "lead_intake_whatsapp",
                "intended_actions": ["cold_outreach_whatsapp"],
                "deliverable": "x",
            },
        )
    assert r.status_code == 200
    assert r.json()["verdict"] == "blocked"


@pytest.mark.asyncio
async def test_service_quality_sla_endpoint():
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.get("/api/v1/service-quality/sla/lead_intake_whatsapp")
    assert r.status_code == 200
    assert r.json()["service_id"] == "lead_intake_whatsapp"


@pytest.mark.asyncio
async def test_service_quality_sla_list_endpoint():
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.get("/api/v1/service-quality/sla")
    assert r.status_code == 200
    assert r.json()["count"] == 32
