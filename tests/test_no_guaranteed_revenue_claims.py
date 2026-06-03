"""The specific banned claims named in the brief are detected by the scanner and
are absent from real outbound copy."""
import _loaders as L


def test_arabic_guarantee_phrase_is_caught():
    fb = L.forbidden()
    sample = "عرضنا: نضمن زيادة المبيعات خلال شهر"
    assert L.find_forbidden(sample, fb), "must flag 'نضمن زيادة المبيعات'"


def test_english_10x_phrase_is_caught():
    fb = L.forbidden()
    assert L.find_forbidden("We will 10x revenue for you", fb), "must flag '10x revenue'"


def test_these_phrases_absent_from_outbound():
    fb = L.forbidden()
    for d in L.load_jsonl("data/outreach/drafts.jsonl"):
        blob = d.get("subject", "") + " " + d.get("body", "")
        assert "نضمن زيادة المبيعات" not in blob
        assert "10x" not in blob.lower()


def test_gate_marks_guarantee_draft_as_forbidden_claim():
    fb, sup = L.forbidden(), L.suppression()
    bad = {
        "draft_type": "first_touch", "subject": "عرض", "body": "نضمن زيادة المبيعات",
        "personalization_score": "P2", "company": "X", "opt_out": {"included": True},
        "prospect_id": "x", "sector": "marketing_agencies", "pain_hypothesis": "lead_leakage",
        "offer_match": "DLX-L1", "evidence_level": "assumed", "risk_level": "low",
        "approval_status": "pending", "send_status": "not_sent",
    }
    assert "forbidden_claim" in L.gate_draft(bad, fb, sup)["reasons"]
