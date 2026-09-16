from api.routers.founder_command_room import FOUNDER_ACTIONS, OFFER_LADDER
from api.routers.revenue import NEGOTIATION_TEMPLATES_AR, negotiation_respond


def test_founder_command_room_has_no_fixed_pilot_duration_or_standing_l5_action():
    rendered = repr({"actions": FOUNDER_ACTIONS, "offers": OFFER_LADDER})
    assert "30 يوم" not in rendered
    assert "إرسال 5 رسائل" not in rendered
    assert "توقيع اتفاقية" not in rendered
    assert "ضبط سجلات DNS" not in rendered
    assert "دمج PR" not in rendered
    assert "مدة ومعايير قبول خاصة بالعميل" in rendered
    assert "action-bound approval" in rendered
    assert "Source Green is not Production Green" in rendered


def test_negotiation_templates_are_evidence_bounded_and_draft_only():
    rendered = "\n".join(NEGOTIATION_TEMPLATES_AR.values())
    for forbidden in (
        "الوحيد بالعربي الخليجي",
        "متوافق PDPL",
        "+ Mada",
        "خطة Q3",
        "نرسل لكم one-pager",
        "نتابع بعد 3 أيام",
    ):
        assert forbidden not in rendered
    assert "ما ندّعي تفوقاً أو توافقاً أو وسيلة دفع بدون دليل حالي" in rendered
    assert "ما نعد بموعد غير مثبت" in rendered
    assert "موافقة محددة على الرسالة والقناة والمستلم" in rendered


async def test_negotiation_endpoint_is_draft_only_and_requires_human_approval():
    result = await negotiation_respond({
        "objection_type": "decision_maker_unavailable",
        "company_name": "شركة اختبار",
    })
    assert result["approval_required"] is True
    assert result["send_status"] == "queued_for_human_approval"
    assert result["channel_policy"] == "human_final_send_only_during_first_30_days"
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
