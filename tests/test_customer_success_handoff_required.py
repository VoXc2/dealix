"""A won deal must produce a sales->delivery (customer success) handoff."""
from _util import decide, load_jsonl, DATA


def test_won_deal_without_handoff_is_rejected():
    assert decide({"deal_status": "won", "has_delivery_handoff": False}) == "reject"


def test_won_deal_with_handoff_is_allowed():
    assert decide({"deal_status": "won", "has_delivery_handoff": True}) == "allow"


def test_committed_won_deal_has_handoff():
    # PROP-1002 is founder_approved (our 'won' example) -> there must be a delivery handoff for it.
    proposals = {p["id"]: p for p in load_jsonl(DATA / "proposals" / "proposals.jsonl")}
    handoffs = load_jsonl(DATA / "delivery" / "handoffs.jsonl")
    handoff_proposal_ids = {h.get("proposal_id") for h in handoffs}
    approved = [pid for pid, p in proposals.items() if p.get("founder_approved")]
    assert approved, "expected at least one founder-approved proposal"
    for pid in approved:
        assert pid in handoff_proposal_ids, f"approved/won proposal {pid} has no delivery handoff"


def test_handoffs_reference_real_proposals():
    proposals = {p["id"] for p in load_jsonl(DATA / "proposals" / "proposals.jsonl")}
    for h in load_jsonl(DATA / "delivery" / "handoffs.jsonl"):
        ref = h.get("proposal_id")
        assert ref in proposals, f"handoff {h.get('id')} references unknown proposal {ref}"
