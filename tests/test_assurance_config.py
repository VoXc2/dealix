"""Assurance System — config loader tests."""
from __future__ import annotations

from auto_client_acquisition.assurance_os.config_loader import load_config


def test_all_three_yaml_files_load() -> None:
    cfg = load_config()
    assert cfg.loaded_ok, cfg.errors
    assert cfg.errors is None


def test_approval_policy_structure() -> None:
    ap = load_config().approval_policy
    assert ap["version"] == 1
    assert "whatsapp" in ap["channels"]
    # whatsapp must never be auto-approvable
    assert ap["channels"]["whatsapp"]["max_auto_approve_risk"] is None
    assert ap["hard_rules"]["high_risk_auto_send_allowed"] is False
    assert ap["hard_rules"]["affiliate_payout_before_payment_allowed"] is False


def test_stage_transitions_ten_rung_ladder() -> None:
    st = load_config().stage_transitions
    keys = [r["key"] for r in st["ladder"]]
    assert keys == [
        "attention", "lead", "qualified", "meeting", "scope",
        "invoice", "paid", "delivered", "upsell", "referral",
    ]
    # every rung is mapped (upsell may map to an empty list)
    assert set(st["rung_to_journey_stage"].keys()) == set(keys)
    assert st["hard_gates"]["no_revenue_before"] == "payment_confirmed"


def test_claim_policy_has_eleven_non_negotiables() -> None:
    cp = load_config().claim_policy
    assert len(cp["non_negotiables"]) == 11
    ids = {n["id"] for n in cp["non_negotiables"]}
    assert "no_guaranteed_outcomes" in ids
    assert cp["claim_requires_source"] is True
    assert "refund" in cp["escalation_triggers"]
