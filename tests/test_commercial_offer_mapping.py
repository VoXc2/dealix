"""Every pain category maps to a real, well-formed catalog offer, and every
draft pitches an offer that exists in the catalog."""
import _loaders as L

PAIN_CATEGORIES = {
    "lead_leakage", "follow_up_chaos", "crm_data_disorder", "proposal_delay",
    "weak_reporting", "sales_team_inconsistency", "support_overload",
    "no_proof_case_study_system", "slow_onboarding", "weak_renewal_upsell",
}


def test_every_pain_is_mapped_to_real_offer():
    ids = L.catalog_ids()
    mappings = L.load_yaml("data/commercial/pain_to_offer.yaml")["mappings"]
    mapped = {m["pain_category"] for m in mappings}
    assert mapped == PAIN_CATEGORIES, f"unmapped pains: {PAIN_CATEGORIES ^ mapped}"
    for m in mappings:
        assert m["ladder_id"] in ids, f"{m['pain_category']} -> unknown offer {m['ladder_id']}"
        assert m["next_action"] and m["approval_required"] is True
        assert m["evidence_required"] in {"none", "assumed", "observed", "verified"}


def test_catalog_offers_are_well_formed():
    required = {"id", "name", "promise", "buyer", "pain", "deliverables",
                "timeline_days", "price_range", "scope", "out_of_scope",
                "success_metric", "requires_founder_pricing_approval"}
    for o in L.load_yaml("data/commercial/product_catalog.yaml")["offers"]:
        assert required <= set(o), f"{o.get('id')} missing {required - set(o)}"
        assert o["out_of_scope"], f"{o['id']} must declare out_of_scope"
        assert o["requires_founder_pricing_approval"] is True
        assert set(o["pain"]) <= PAIN_CATEGORIES


def test_draft_offer_match_exists_in_catalog():
    ids = L.catalog_ids()
    for d in L.load_jsonl("data/outreach/drafts.jsonl"):
        assert d["offer_match"] in ids, f"{d['draft_id']} -> unknown offer {d['offer_match']}"


def test_job_signal_offers_exist():
    ids = L.catalog_ids()
    for s in L.load_jsonl("data/signals/job_signals.jsonl"):
        assert s["mapped_offer"] in ids, f"{s['signal_id']} -> unknown offer {s['mapped_offer']}"
