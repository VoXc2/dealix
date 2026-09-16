from api.routers.founder_command_room import FOUNDER_ACTIONS, OFFER_LADDER
from api.routers.revenue import NEGOTIATION_TEMPLATES_AR


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
