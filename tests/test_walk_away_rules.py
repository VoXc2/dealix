"""Bad-fit clients (mass sending, guaranteed-sales demands, refusing approval,
scraping requests, no recurring leads / access / ability to pay) are
disqualified; good-fit clients pass."""
import _loaders as L


def test_fit_eval_cases():
    cases = [c for c in L.load_jsonl("data/evals/commercial_safety_cases.jsonl") if c["kind"] == "fit"]
    assert cases
    for c in cases:
        res = L.evaluate_fit(c["input"])
        got = "pass" if res["ok"] else "fail"
        assert got == c["expect"], f"{c['case_id']}: expected {c['expect']} got {got}"


def test_spam_client_is_disqualified():
    res = L.evaluate_fit({
        "recurring_leads": True, "decision_maker_access": True, "ability_to_pay": True,
        "wants_mass_sending": True, "wants_guaranteed_sales": True, "refuses_approval": True,
    })
    assert "disqualified_bad_fit" in res["reasons"]


def test_good_fit_passes():
    assert L.evaluate_fit({
        "recurring_leads": True, "decision_maker_access": True, "ability_to_pay": True,
        "wants_mass_sending": False, "wants_guaranteed_sales": False, "refuses_approval": False,
    })["ok"]


def test_segments_declare_disqualifiers():
    for seg in L.load_yaml("data/commercial/icp_segments.yaml")["segments"]:
        assert seg["disqualifiers"], f"{seg['id']} must declare disqualifiers"
