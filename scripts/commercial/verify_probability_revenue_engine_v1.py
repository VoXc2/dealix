#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONTRACT = ROOT / "config/commercial/probability_revenue_engine_v1.json"
RUNNER = ROOT / "scripts/commercial/run_probability_revenue_engine_v1.py"

EXPECTED_AGENTS = {
    "dealix-pm",
    "dealix-sales",
    "dealix-delivery",
    "dealix-engineer",
    "dealix-content",
}

FALSE_AUTHORITY_KEYS = {
    "external_send",
    "public_publish",
    "paid_spend",
    "payment_execution",
    "production_mutation",
    "dns_mutation",
    "db_mutation",
    "secret_mutation",
    "identity_mutation",
}

REQUIRED_TRUTH = {
    "research != relationship",
    "public_contact != consent",
    "draft != sent",
    "quote != invoice",
    "invoice != payment",
    "unknown_probability != evidence",
}

REQUIRED_ROUTES = {
    "PRIME",
    "BUILD_DIRECT",
    "CONFIGURE_ADAPT",
    "INTEGRATE_EXISTING_PRODUCT",
    "QUALIFIED_PARTNER",
    "SUBCONTRACT_PACKAGE",
    "DISCLOSED_REFERRAL",
    "RESEARCH_ONLY",
    "DECLINE_DEFER",
}


def main() -> int:
    data = json.loads(CONTRACT.read_text(encoding="utf-8"))
    runner = RUNNER.read_text(encoding="utf-8")

    assert data["north_star"] == "CASH_READY_AUTONOMOUS_DEALIX_COMPANY"
    assert data["authority"]["autonomy_level"] == 4
    assert data["authority"]["mode"] == "draft-only"

    for key in FALSE_AUTHORITY_KEYS:
        assert data["authority"].get(key) is False, f"material authority must remain false: {key}"

    assert set(data["owners"].values()) == EXPECTED_AGENTS
    assert REQUIRED_TRUTH.issubset(set(data["truth_firewall"]))
    assert set(data["route_options"]) == REQUIRED_ROUTES

    ceilings = data["capacity_ceiling_per_operating_day"]
    assert ceilings["raw_signal_refresh"] >= ceilings["verified_relevant_signals"]
    assert ceilings["verified_relevant_signals"] >= ceilings["account_hypotheses"]
    assert ceilings["account_hypotheses"] >= ceilings["buying_committee_maps"]
    assert ceilings["buying_committee_maps"] >= ceilings["personalized_diagnostic_drafts"]
    assert ceilings["deep_commercial_wip"] <= 3
    assert ceilings["material_action_packets"] <= 1

    allocation = data["allocation_policy"]
    assert 0 <= allocation["exploration_share"] <= 1
    assert 0 <= allocation["exploitation_share"] <= 1
    assert abs(
        allocation["exploration_share"] + allocation["exploitation_share"] - 1.0
    ) < 1e-9
    assert allocation["minimum_real_observations_before_exploitation"] >= 1
    assert "suppression" in allocation["prohibited_overrides"]
    assert "opt_out" in allocation["prohibited_overrides"]
    assert "channel_ineligibility" in allocation["prohibited_overrides"]

    assert data["unknown_probability_policy"] == "UNKNOWN_NOT_EVIDENCE_BACKED"
    assert "verified_payment" in data["real_outcome_updates"]
    assert "permissioned_customer_proof" in data["real_outcome_updates"]

    # Runtime enforcement must match the contract rather than merely documenting it.
    assert "effective_limit = min(requested_limit, raw_signal_ceiling)" in runner
    assert "deep_wip_evidence_ready" in runner
    assert "EV_BLOCKED_EVIDENCE_GAP" in runner
    assert 'flags["source_present"] and flags["source_attributable"]' in runner
    assert '"evidence_ref_count": len(evidence_refs)' in runner

    print("DEALIX_PROBABILITY_REVENUE_ENGINE_VERIFY=PASS")
    print(f"RAW_SIGNAL_CAPACITY={ceilings['raw_signal_refresh']}")
    print(f"DEEP_COMMERCIAL_WIP={ceilings['deep_commercial_wip']}")
    print("DEEP_WIP_EVIDENCE_GATE=ENFORCED")
    print("RUNTIME_VOLUME_CEILING=ENFORCED")
    print("EXTERNAL_SEND_AUTHORITY=false")
    print("L5_EXECUTED=NONE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
