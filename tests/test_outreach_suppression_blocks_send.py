"""A recipient on the suppression list can never be send-ready, even when the
draft is otherwise perfect and approved."""
import _loaders as L


def test_suppressed_recipient_fails_gate():
    fb, sup = L.forbidden(), L.suppression()
    suppressed_domain = next(iter(sup))
    d = {
        "draft_type": "first_touch", "subject": "تشخيص", "body": "نص. إيقاف: ردّ «إيقاف».",
        "personalization_score": "P2", "company": "Blocked", "prospect_id": "x",
        "sector": "marketing_agencies", "pain_hypothesis": "lead_leakage",
        "offer_match": "DLX-L1", "evidence_level": "assumed", "risk_level": "low",
        "opt_out": {"included": True}, "approval_status": "approved",
        "send_status": "not_sent", "recipient_domain": suppressed_domain,
    }
    res = L.gate_draft(d, fb, sup)
    assert "suppressed" in res["reasons"]
    assert not L.is_send_ready(d, fb, sup, "RAMP_READY")


def test_suppressed_eval_case_present():
    cases = {c["case_id"]: c for c in L.load_jsonl("data/evals/gtm_draft_eval_cases.jsonl")}
    c = cases["GD-FAIL-SUPPRESSED"]
    fb, sup = L.forbidden(), L.suppression()
    assert "suppressed" in L.gate_draft(c["draft"], fb, sup)["reasons"]


def test_suppression_mirrors_match():
    canon = L.suppression("data/outreach/suppression_list.jsonl")
    mirror = L.suppression("data/prospects/suppression_list.jsonl")
    assert canon == mirror, "prospects suppression mirror drifted from canonical outreach list"
