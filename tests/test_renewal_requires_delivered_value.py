"""Renewal/upsell drafts require delivered value (evidence_level + citations)."""
from _util import decide, load_jsonl, DATA

DELIVERED = {"client_data", "measured", "verified"}


def test_renewal_without_value_is_rejected():
    assert decide({"type": "renewal", "evidence_level": "assumption", "cites_delivered_value": []}) == "reject"
    assert decide({"type": "renewal", "evidence_level": "benchmark", "cites_delivered_value": ["x"]}) == "reject"
    assert decide({"type": "renewal", "evidence_level": "measured", "cites_delivered_value": []}) == "reject"


def test_renewal_with_value_is_allowed():
    assert decide({"type": "renewal", "evidence_level": "measured", "cites_delivered_value": ["WVR-1001"]}) == "allow"


def test_upsell_requires_value_too():
    assert decide({"type": "upsell", "evidence_level": "none", "cites_delivered_value": []}) == "reject"
    assert decide({"type": "upsell", "evidence_level": "verified", "cites_delivered_value": ["m"]}) == "allow"


def test_committed_renewals_and_upsells_cite_value():
    rows = load_jsonl(DATA / "renewals" / "renewals.jsonl") + load_jsonl(DATA / "renewals" / "upsell_opportunities.jsonl")
    assert rows, "expected seed renewals/upsells"
    for r in rows:
        assert r.get("evidence_level") in DELIVERED, f"{r.get('id')} evidence too weak"
        assert r.get("cites_delivered_value"), f"{r.get('id')} cites no delivered value"
        assert r.get("approval_required") is True, f"{r.get('id')} must require approval"
