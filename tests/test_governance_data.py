"""Integration tests: the REAL governance data must satisfy the hard rules."""

import safety_gate as sg
from conftest import load_json, load_jsonl


def test_real_approval_queue_passes_safety_gate(company_os):
    queue = load_json(company_os / "governance" / "approval_queue.json")
    suppressed = sg.load_suppression(company_os / "governance" / "suppression_list.json")
    findings = sg.check_outbound_items(queue, suppressed)
    critical = [f for f in findings if f["severity"] == "CRITICAL"]
    assert not critical, f"Real approval queue has critical violations: {critical}"


def test_every_outreach_item_requires_approval(company_os):
    queue = load_json(company_os / "governance" / "approval_queue.json")
    for item in queue:
        if item.get("type") == "outreach_message":
            assert item.get("requires_approval") is True, item.get("id")


def test_pricing_and_payment_items_require_approval_and_high_risk(company_os):
    queue = load_json(company_os / "governance" / "approval_queue.json")
    for item in queue:
        if item.get("type") in {"pricing_offer", "payment_handoff", "contract"}:
            assert item.get("requires_approval") is True, item.get("id")
            assert item.get("risk") == "high", item.get("id")


def test_ledger_has_no_unapproved_executed_actions(company_os):
    ledger = load_jsonl(company_os / "governance" / "ai_action_ledger.jsonl")
    for entry in ledger:
        # An action requiring approval must not be recorded as approved=True
        # unless a human approved it. Drafts (approved=False) are fine.
        if entry.get("requires_approval") and entry.get("approved"):
            assert entry.get("action") not in {"sent_message", "processed_payment"}, entry


def test_suppression_entries_are_permanent(company_os):
    data = load_json(company_os / "governance" / "suppression_list.json")
    for e in data["entries"]:
        assert e.get("reason") in data["suppression_reasons"], e
        assert e.get("permanent") is True, e
