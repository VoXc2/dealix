"""Cold drafts must carry an opt-out. Missing opt-out fails the gate; every
production cold draft includes one."""
import _loaders as L


def _base():
    return {
        "draft_type": "first_touch", "subject": "تشخيص", "body": "نص",
        "personalization_score": "P2", "company": "X", "prospect_id": "x",
        "sector": "marketing_agencies", "pain_hypothesis": "lead_leakage",
        "offer_match": "DLX-L1", "evidence_level": "assumed", "risk_level": "low",
        "approval_status": "pending", "send_status": "not_sent",
    }


def test_missing_optout_fails():
    fb, sup = L.forbidden(), L.suppression()
    d = _base(); d["opt_out"] = {"included": False}
    assert "missing_unsubscribe" in L.gate_draft(d, fb, sup)["reasons"]


def test_present_optout_passes():
    fb, sup = L.forbidden(), L.suppression()
    d = _base(); d["opt_out"] = {"included": True, "method": "reply_stop"}
    assert "missing_unsubscribe" not in L.gate_draft(d, fb, sup)["reasons"]


def test_all_production_cold_drafts_have_optout():
    for d in L.load_jsonl("data/outreach/drafts.jsonl"):
        if d["draft_type"] in L.COLD_TYPES:
            assert (d.get("opt_out") or {}).get("included") is True, d["draft_id"]
