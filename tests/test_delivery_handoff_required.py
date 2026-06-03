"""Delivery requires a handoff and a weekly value report template."""
from _util import decide, load_jsonl, DATA


def test_delivery_without_weekly_template_is_rejected():
    assert decide({"deal_status": "in_delivery", "weekly_value_report_template": ""}) == "reject"


def test_delivery_with_weekly_template_is_allowed():
    assert decide({"deal_status": "in_delivery", "weekly_value_report_template": "reports/delivery/WEEKLY_VALUE_REPORT_QUEUE.md"}) == "allow"


def test_committed_handoffs_have_weekly_template():
    handoffs = load_jsonl(DATA / "delivery" / "handoffs.jsonl")
    assert handoffs, "expected seed delivery handoffs"
    for h in handoffs:
        assert h.get("weekly_value_report_template"), f"handoff {h.get('id')} missing weekly value report template"
        assert h.get("scope"), f"handoff {h.get('id')} missing scope"
        assert h.get("success_metric"), f"handoff {h.get('id')} missing success_metric"


def test_onboarding_links_to_handoff():
    handoff_ids = {h["id"] for h in load_jsonl(DATA / "delivery" / "handoffs.jsonl")}
    for o in load_jsonl(DATA / "delivery" / "onboarding.jsonl"):
        assert o.get("handoff_id") in handoff_ids, f"onboarding {o.get('id')} references unknown handoff"
