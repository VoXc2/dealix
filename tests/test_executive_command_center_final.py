"""Phase 2 — Executive Command Center 8-field card schema tests."""
from __future__ import annotations

import pytest
from httpx import ASGITransport, AsyncClient

from auto_client_acquisition.executive_command_center.card_schema import (
    DecisionCard,
    card_keys,
    to_card_dict,
)


def test_card_keys_returns_8_fields() -> None:
    keys = card_keys()
    assert len(keys) == 8
    expected = {
        "signal", "why_now", "recommended_action", "risk",
        "impact", "owner", "action_mode", "proof_link",
    }
    assert set(keys) == expected


def test_to_card_dict_round_trip() -> None:
    card = to_card_dict(
        signal="hiring_sales_rep at NewCo",
        why_now="company expanding, drafts ready",
        recommended_action="approve the WhatsApp draft",
        risk="if delayed, lead goes cold within 48h",
        impact="opens 30-min discovery call",
        owner="founder",
        action_mode="approval_required",
        proof_link="leadops:lops_xxx",
    )
    for key in card_keys():
        assert key in card
    assert card["action_mode"] == "approval_required"
    assert card["proof_link"] == "leadops:lops_xxx"


def test_decision_card_action_mode_validation() -> None:
    """action_mode must be one of the valid literals."""
    from pydantic import ValidationError
    with pytest.raises(ValidationError):
        DecisionCard(
            signal="x", why_now="x", recommended_action="x",
            risk="x", impact="x", owner="founder",
            action_mode="invalid_mode_xyz",  # type: ignore[arg-type]
        )


def test_decision_card_extra_forbid() -> None:
    """Extra fields must be rejected."""
    from pydantic import ValidationError
    with pytest.raises(ValidationError):
        DecisionCard(
            signal="x", why_now="x", recommended_action="x",
            risk="x", impact="x", owner="founder",
            action_mode="draft_only",
            unknown_field="X",  # type: ignore[call-arg]
        )


def test_decision_card_proof_link_optional() -> None:
    """proof_link can be None (internal-only events)."""
    card = DecisionCard(
        signal="x", why_now="x", recommended_action="x",
        risk="x", impact="x", owner="founder",
        action_mode="draft_only",
        proof_link=None,
    )
    assert card.proof_link is None


@pytest.mark.asyncio
async def test_ecc_decisions_use_8_field_schema_when_data_exists() -> None:
    """If approvals are queued, today_3_decisions cards include all 8 fields."""
    from auto_client_acquisition.approval_center import approval_store
    from auto_client_acquisition.approval_center.schemas import ApprovalRequest

    # Seed an approval scoped to this customer
    handle = "ecc-8field-test"
    req = ApprovalRequest(
        approval_id="apv_8field_001",
        object_type="outreach_draft",
        object_id="obj_8field",
        action_type="send_whatsapp",
        action_mode="approval_required",
        channel="whatsapp",
        summary_ar=f"رسالة معتمدة لعميل {handle}",
        summary_en="Approved message for customer",
        risk_level="high",
        proof_impact=f"leadops:{handle}_lead_001",
    )
    approval_store.get_default_approval_store().create(req)

    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.get(f"/api/v1/executive-command-center/{handle}")
    assert r.status_code == 200
    decisions = r.json()["view"]["today_3_decisions"]
    assert len(decisions) >= 1
    for d in decisions:
        for required in ("signal", "why_now", "recommended_action",
                         "risk", "impact", "owner", "action_mode"):
            assert required in d, f"missing field: {required}"
        assert d["action_mode"] in (
            "suggest_only", "draft_only", "approval_required",
            "approved_manual", "blocked",
        )


@pytest.mark.asyncio
async def test_ecc_status_still_works() -> None:
    """Phase 2 changes must not break existing status endpoint."""
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.get("/api/v1/executive-command-center/status")
    assert r.status_code == 200
    body = r.json()
    assert body["section_count"] == 15


@pytest.mark.asyncio
async def test_ecc_full_view_still_returns_15_sections() -> None:
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.get("/api/v1/executive-command-center/15-section-test")
    view = r.json()["view"]
    expected = [
        "executive_summary", "full_ops_score", "today_3_decisions",
        "revenue_radar", "sales_pipeline", "growth_radar",
        "partnership_radar", "support_inbox", "delivery_operations",
        "finance_state", "proof_ledger", "risks_compliance",
        "approval_center", "whatsapp_decision_preview",
    ]
    for sec in expected:
        assert sec in view
