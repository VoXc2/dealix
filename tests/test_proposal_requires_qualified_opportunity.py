"""No proposal without a qualified opportunity that carries a product mapping,
pain category, and success metric."""
import _loaders as L


def test_proposal_eval_cases():
    cases = [c for c in L.load_jsonl("data/evals/commercial_safety_cases.jsonl") if c["kind"] == "proposal"]
    assert cases
    for c in cases:
        res = L.evaluate_proposal(c["input"])
        got = "pass" if res["ok"] else "fail"
        assert got == c["expect"], f"{c['case_id']}: expected {c['expect']} got {got} {res['reasons']}"
        if c["expect"] == "fail":
            assert c["reason_code"] in res["reasons"]


def test_unqualified_opportunity_blocks_proposal():
    assert not L.evaluate_proposal({"qualified": False, "product_match": None, "pain_category": "lead_leakage"})["ok"]


def test_qualified_without_mapping_blocks_proposal():
    res = L.evaluate_proposal({"qualified": True, "product_match": None, "pain_category": "lead_leakage"})
    assert "missing_product_match" in res["reasons"]


def test_real_proposals_reference_qualified_mapped_opportunities():
    opps = {o["opp_id"]: o for o in L.load_jsonl("data/commercial/opportunities.jsonl")}
    ids = L.catalog_ids()
    for pr in L.load_jsonl("data/commercial/proposals.jsonl"):
        opp = opps[pr["opp_id"]]
        assert opp["qualified"] is True, f"{pr['proposal_id']} on unqualified opp"
        assert pr["product_match"] in ids
        assert pr["success_metric"] and pr["scope_clarity"] is True
        assert pr["includes_out_of_scope"] is True
