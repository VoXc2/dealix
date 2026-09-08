#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONFIG = ROOT / "config" / "company" / "strategy_execution_orchestrator_v1.json"
ECONOMICS = ROOT / "config" / "company" / "economic_truth_metrics_v1.json"


def fail(message: str) -> None:
    raise SystemExit(f"DEALIX_STRATEGY_ORCHESTRATOR_VERIFY=FAIL: {message}")


def _load(path: Path) -> dict:
    if not path.is_file():
        fail(f"config missing: {path.name}")
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        fail(f"config must be an object: {path.name}")
    return data


def _verify_economic_truth(data: dict) -> None:
    if data.get("north_star") != "CASH_READY_AUTONOMOUS_DEALIX_COMPANY":
        fail("economic north star drift")
    if data.get("owner") != "strategy_execution_orchestrator_v1":
        fail("economic metrics must stay owned by the strategy orchestrator")

    principles = data.get("principles") or {}
    for key in (
        "unknown_is_not_zero",
        "no_fabricated_denominators",
        "historical_pass_is_not_current_proof",
        "research_is_not_relationship",
        "public_contact_is_not_consent",
        "draft_is_not_sent",
        "quote_is_not_payment",
        "invoice_is_not_payment",
        "synthetic_is_not_customer_proof",
    ):
        if principles.get(key) is not True:
            fail(f"economic truth principle missing: {key}")

    required_metrics = {
        "production_exact_release_parity",
        "real_interactions",
        "qualified_problems",
        "customer_specific_quotes",
        "verified_payments",
        "verified_cash_sar",
        "time_to_first_verified_value",
        "gross_margin_per_project",
        "runtime_cost_per_delivered_outcome",
        "founder_minutes_per_paid_outcome",
        "customer_validated_proofs",
        "repeatable_paid_cycles",
    }
    metrics = data.get("metrics") or []
    ids = {str(item.get("id")) for item in metrics if isinstance(item, dict)}
    if ids != required_metrics:
        fail(f"economic metric drift: {sorted(ids)}")
    for item in metrics:
        if not item.get("source") or not item.get("truth_guard"):
            fail(f"economic metric lacks evidence guard: {item.get('id')}")

    later = {str(item.get("id")): item for item in (data.get("later_stage_metrics") or [])}
    for metric_id in ("logo_retention", "net_revenue_retention"):
        item = later.get(metric_id)
        if not item or not item.get("available_when") or not item.get("truth_guard"):
            fail(f"later-stage metric must remain evidence gated: {metric_id}")


def main() -> int:
    data = _load(CONFIG)
    economics = _load(ECONOMICS)

    if data.get("north_star") != "CASH_READY_AUTONOMOUS_DEALIX_COMPANY":
        fail("north star drift")

    law = data.get("one_company_law") or {}
    for key in (
        "company_machine_count",
        "opportunity_graph_count",
        "approval_authority_count",
        "proof_model_count",
        "consent_authority_count",
        "scheduler_count",
        "model_router_count",
    ):
        if law.get(key) != 1:
            fail(f"{key} must equal 1")

    agents = law.get("permanent_agents") or []
    expected_agents = [
        "dealix-pm",
        "dealix-sales",
        "dealix-delivery",
        "dealix-engineer",
        "dealix-content",
    ]
    if agents != expected_agents:
        fail("permanent-agent law drift")

    portfolios = set((data.get("portfolios") or {}).keys())
    if portfolios != {"TRUST", "MONEY_NOW", "COMPOUNDING"}:
        fail("portfolio set drift")

    wip = data.get("wip_limits") or {}
    if int(wip.get("top_actions_per_cycle", 99)) > 3:
        fail("top-actions WIP exceeds 3")
    if int(wip.get("active_venture_experiments", 99)) > 2:
        fail("venture WIP exceeds 2")
    if int(wip.get("capability_benchmarks", 99)) > 1:
        fail("capability benchmark WIP exceeds 1")
    if int(wip.get("material_approval_packets", 99)) > 1:
        fail("material approval WIP exceeds 1")

    authority = data.get("material_authority") or {}
    if not authority or any(value is not False for value in authority.values()):
        fail("material authority must remain all-false")

    build_law = data.get("build_buy_partner_law") or []
    if build_law != ["REUSE_CANONICAL", "OFFICIAL_API", "QUALIFIED_PARTNER", "BUILD"]:
        fail("build/buy/partner law drift")

    strategies = data.get("strategies") or []
    if not strategies:
        fail("strategies missing")
    ids = [str(item.get("id")) for item in strategies]
    if len(ids) != len(set(ids)):
        fail("duplicate strategy id")
    for item in strategies:
        if item.get("portfolio") not in portfolios:
            fail(f"unknown portfolio for {item.get('id')}")
        if item.get("promotion_authority") != "none":
            fail(f"strategy {item.get('id')} gained promotion authority")
        if not item.get("owner") or not item.get("action"):
            fail(f"strategy {item.get('id')} missing owner/action")

    ventures = data.get("venture_candidates") or []
    for item in ventures:
        if item.get("build_allowed_without_paid_pain") is not False:
            fail(f"venture {item.get('id')} allows premature build")

    oss = data.get("oss_admission") or []
    for item in oss:
        if item.get("automatic_install") is not False:
            fail(f"OSS {item.get('id')} enables automatic installation")
        if not item.get("source"):
            fail(f"OSS {item.get('id')} missing source")

    _verify_economic_truth(economics)

    print("DEALIX_STRATEGY_ORCHESTRATOR_VERIFY=PASS")
    print("ONE_COMPANY_LAW=PASS")
    print("PORTFOLIOS_EXACT=PASS")
    print("WIP_LIMITS=PASS")
    print("MATERIAL_AUTHORITY_ALL_FALSE=PASS")
    print("VENTURE_BUILD_GUARD=PASS")
    print("OSS_AUTOINSTALL_FALSE=PASS")
    print("ECONOMIC_TRUTH_METRICS=PASS")
    print("NO_PREMATURE_SAAS_METRICS=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
