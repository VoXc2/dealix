"""Partner deals must respect the margin floor, and every partner record carries
an explicit margin + floor + approval flag."""
import _loaders as L


def test_partner_eval_cases():
    cases = [c for c in L.load_jsonl("data/evals/commercial_safety_cases.jsonl") if c["kind"] == "partner"]
    assert cases
    for c in cases:
        res = L.evaluate_partner(c["input"])
        got = "pass" if res["ok"] else "fail"
        assert got == c["expect"], f"{c['case_id']}: expected {c['expect']} got {got}"


def test_below_floor_is_flagged():
    assert "below_min_margin" in L.evaluate_partner({"margin_pct": 8, "min_margin_pct": 15})["reasons"]


def test_at_or_above_floor_passes():
    assert L.evaluate_partner({"margin_pct": 15, "min_margin_pct": 15})["ok"]


def test_real_partners_respect_floor_and_require_approval():
    for pt in L.load_jsonl("data/partners/partner_opportunities.jsonl"):
        assert pt["margin_pct"] >= pt["min_margin_pct"], pt["partner_id"]
        assert pt["approval_required"] is True
