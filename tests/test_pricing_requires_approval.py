"""Final price always needs founder approval, and a custom-scope offer can never
be sold at a starter price."""
import _loaders as L


def test_pricing_eval_cases():
    cases = [c for c in L.load_jsonl("data/evals/commercial_safety_cases.jsonl") if c["kind"] == "pricing"]
    assert cases
    for c in cases:
        res = L.evaluate_pricing(c["input"])
        got = "pass" if res["ok"] else "fail"
        assert got == c["expect"], f"{c['case_id']}: expected {c['expect']} got {got} {res['reasons']}"
        if c["expect"] == "fail":
            assert c["reason_code"] in res["reasons"]


def test_final_price_without_approval_fails():
    assert not L.evaluate_pricing({"offer_id": "DLX-L1", "final_price": 3000, "tier": "starter", "approval_status": "pending"})["ok"]


def test_final_price_with_approval_passes():
    assert L.evaluate_pricing({"offer_id": "DLX-L1", "final_price": 3000, "tier": "starter", "approval_status": "approved"})["ok"]


def test_custom_scope_at_starter_price_flagged():
    res = L.evaluate_pricing({"offer_id": "DLX-L6", "final_price": 2500, "tier": "starter", "approval_status": "approved"})
    assert "custom_scope_at_starter_price" in res["reasons"]


def test_pricing_rules_enforce_approval():
    rules = {r["id"]: r for r in L.load_yaml("data/commercial/pricing_rules.yaml")["rules"]}
    assert rules["PR-001"]["requires_approval"] is True and rules["PR-001"]["severity"] == "critical"
    assert "PR-004" in rules  # no custom scope at starter price


def test_no_proposal_has_unapproved_final_price():
    for pr in L.load_jsonl("data/commercial/proposals.jsonl"):
        if pr.get("final_price") is not None:
            assert pr["approval_status"] == "approved", pr["proposal_id"]
