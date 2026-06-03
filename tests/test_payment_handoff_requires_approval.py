"""No payment send without founder approval."""
from _util import decide, load_jsonl, DATA


def test_payment_send_without_approval_is_rejected():
    assert decide({"type": "payment_handoff", "send_enabled": True, "approved": False}) == "reject"


def test_payment_send_with_approval_is_allowed():
    assert decide({"type": "payment_handoff", "send_enabled": True, "approved": True}) == "allow"


def test_payment_draft_not_sent_is_allowed():
    # dry-run draft awaiting approval is fine
    assert decide({"type": "payment_handoff", "send_enabled": False, "approved": False}) == "allow"


def test_committed_payment_handoffs_are_safe():
    handoffs = load_jsonl(DATA / "payments" / "payment_handoffs.jsonl")
    assert handoffs, "expected seed payment handoffs"
    for p in handoffs:
        assert p.get("approval_required") is True, f"{p.get('id')} must require approval"
        assert not (p.get("send_enabled") and not p.get("approved")), f"{p.get('id')} sends without approval"
        assert p.get("dry_run") is True, f"{p.get('id')} must default dry_run=true"
        link = p.get("payment_link_ref")
        assert link is None or str(link).startswith("portal://"), f"{p.get('id')} link must be a portal ref"
