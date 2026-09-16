import asyncio

from api.routers.founder_command_room import FOUNDER_ACTIONS, OFFER_LADDER
from api.routers.revenue import NEGOTIATION_TEMPLATES_AR, negotiation_respond


def test_founder_actions_are_review_only_not_standing_external_authority():
    assert FOUNDER_ACTIONS
    for action in FOUNDER_ACTIONS:
        assert action["authority"] == "review_only"
        assert action["external_execution_allowed"] is False
        assert action["action_bound_approval_required"] is True


def test_revenue_command_pilot_has_customer_specific_duration_authority():
    pilot = next(item for item in OFFER_LADDER if item["name"] == "Revenue Command Pilot")
    assert pilot["duration_authority"] == "customer_specific_after_qualified_discovery"
    assert pilot["public_fixed_duration_authority"] is False
    assert "30 يوم" not in pilot["detail"]


def test_negotiation_runtime_contract_never_authorizes_external_send():
    for objection_type in NEGOTIATION_TEMPLATES_AR:
        payload = asyncio.run(negotiation_respond({"objection_type": objection_type, "company_name": "اختبار"}))
        assert payload["approval_required"] is True
        assert payload["requires_action_bound_approval"] is True
        assert payload["external_send_allowed"] is False
        assert payload["send_status"] == "queued_for_human_approval"
        assert payload["channel_policy"] == "action_bound_human_final_send_only"


def test_negotiation_copy_remains_evidence_bounded():
    rendered = "\n".join(NEGOTIATION_TEMPLATES_AR.values())
    for forbidden in (
        "الوحيد بالعربي الخليجي", "متوافق PDPL", "+ Mada",
        "خطة Q3", "نرسل لكم one-pager", "نتابع بعد 3 أيام",
    ):
        assert forbidden not in rendered
    assert "ما ندّعي تفوقاً أو توافقاً أو وسيلة دفع بدون دليل حالي" in rendered
    assert "ما نعد بموعد غير مثبت" in rendered
    assert "موافقة محددة على الرسالة والقناة والمستلم" in rendered


def test_decision_maker_draft_copy_and_runtime_boundary_remain_fail_closed():
    result = asyncio.run(negotiation_respond({
        "objection_type": "decision_maker_unavailable",
        "company_name": "شركة اختبار",
    }))
    assert result["approval_required"] is True
    assert result["requires_action_bound_approval"] is True
    assert result["external_send_allowed"] is False
    assert result["send_status"] == "queued_for_human_approval"
    assert result["channel_policy"] == "action_bound_human_final_send_only"
    assert "لا يعني إرسالها" in result["response_ar"]
    assert "موافقة محددة" in result["response_ar"]


def test_offer_ladder_orders_discovery_before_quote_before_pilot_without_default_duration():
    names = [item["name"] for item in OFFER_LADDER]
    discovery = next(i for i, name in enumerate(names) if "Qualified Discovery" in name)
    quote = next(i for i, name in enumerate(names) if "Customer-Specific Quote" in name)
    pilot = names.index("Revenue Command Pilot")
    assert discovery < quote < pilot
    pilot_detail = OFFER_LADDER[pilot]["detail"]
    assert "customer" in pilot_detail.lower() or "خاصة بالعميل" in pilot_detail
    assert "30" not in pilot_detail
