#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_PATH = ROOT / "config" / "company" / "dealix_operating_constitution.json"

EXPECTED_AGENTS = [
    "dealix-pm",
    "dealix-sales",
    "dealix-delivery",
    "dealix-engineer",
    "dealix-content",
]
EXPECTED_PORTFOLIOS = ["TRUST", "MONEY_NOW", "COMPOUNDING"]
CURRENT_SEED_WEDGES = [
    "REVENUE_COMMAND_AND_AI_COMPANY_OS",
    "GOVERNED_AI_EXECUTION",
    "SAUDI_MARKET_ACCESS_PARTNER_AND_B2G_INTELLIGENCE",
]
REQUIRED_ONE_COMPANY = {
    "ONE_COMPANY_MACHINE",
    "ONE_COMPANY_BRAIN",
    "ONE_PORTFOLIO",
    "ONE_OPPORTUNITY_GRAPH",
    "ONE_PROCESS_GRAPH",
    "ONE_APPROVAL_AUTHORITY",
    "ONE_CONSENT_AUTHORITY",
    "ONE_POLICY_MODEL",
    "ONE_PROOF_LEDGER",
    "ONE_ECONOMIC_MODEL",
    "ONE_CANONICAL_SCHEDULER",
    "ONE_MODEL_ROUTER",
    "ONE_DEV_FACTORY",
    "ONE_LEARNING_FACTORY",
    "ONE_OBSERVABILITY_MODEL",
    "ONE_AGENT_IDENTITY_MODEL",
}
REQUIRED_TRUTH = {
    "Research != Relationship",
    "Public Contact != Consent",
    "Signal != Opportunity",
    "Draft != Sent",
    "Quote != Invoice",
    "Invoice != Payment",
    "Payment Request != Verified Cash",
    "PR Merge != Production Green",
    "Historical PASS != Current Exact-Head PASS",
    "Model Output != Authority",
    "Unknown = UNKNOWN_NOT_EVIDENCE_BACKED",
}
REQUIRED_MATERIAL = {
    "MERGE_MAIN",
    "PRODUCTION_DEPLOY_OR_REDEPLOY",
    "DNS_MUTATION",
    "PRODUCTION_DB_OR_SCHEMA_MUTATION",
    "SECRET_OR_IDENTITY_MUTATION",
    "EXTERNAL_CUSTOMER_SEND",
    "PUBLIC_PUBLISH",
    "PAID_SPEND",
    "PAYMENT_OR_REFUND",
    "BINDING_QUOTE_CONTRACT_OR_TENDER",
    "LIVE_VOICE_ACTIVATION",
}
REQUIRED_COMMERCIAL_STAGES = {
    "OFFICIAL_OR_ECONOMIC_SIGNAL",
    "EVIDENCE",
    "ACCOUNT_INTELLIGENCE",
    "CHANNEL_ELIGIBILITY",
    "REAL_INTERACTION",
    "QUALIFIED_PROBLEM",
    "EXECUTION_DIAGNOSTIC",
    "DISCOVERY",
    "SOLUTION_ROUTE",
    "CUSTOMER_SPECIFIC_SOLUTION",
    "CUSTOMER_SPECIFIC_QUOTE",
    "VERIFIED_PAYMENT_OR_START_AUTHORITY",
    "PROJECT_CELL",
    "GOVERNED_DELIVERY",
    "CUSTOMER_ACCEPTANCE",
    "CUSTOMER_VALIDATED_PROOF",
    "LEARNING",
    "REPEATABILITY",
}
REQUIRED_ENGINES = {
    "CORE_CASH_ENGINE",
    "RECURRING_REVENUE_ENGINE",
    "PRODUCTIZED_SERVICE_ENGINE",
    "DATA_AND_INTELLIGENCE_ENGINE",
    "SOFTWARE_AND_API_ENGINE",
    "PARTNER_AND_CHANNEL_ENGINE",
    "EDUCATION_MEDIA_AND_IP_ENGINE",
    "B2G_AND_REGULATED_ENTERPRISE_ENGINE",
    "VENTURE_AND_ASSET_ENGINE",
}
REQUIRED_TOOL_STATES = {
    "ADOPT",
    "INTEGRATE",
    "HARVEST",
    "WATCH",
    "REJECT_DUPLICATE",
    "BLOCKED",
}


def _list(data: dict[str, Any], key: str) -> list[Any]:
    value = data.get(key)
    return value if isinstance(value, list) else []


def _forbids_deep_building_every_researched_arm(items: set[str]) -> bool:
    """Require the explicit doctrine, independent of grammar/inflection.

    The canonical constitution currently says "deep-build every researched arm
    before buyer evidence". Older verifier text looked only for the different
    phrase "deep-building every researched arm", which falsely rejected the
    valid constitution. Keep the guard strict on the three semantic elements:
    deep-build prohibition + every + researched arm.
    """
    for item in items:
        normalized = " ".join(item.replace("-", " ").split())
        if "every researched arm" not in normalized:
            continue
        if any(token in normalized for token in ("deep build", "deep building")):
            return True
    return False


def verify(data: dict[str, Any]) -> list[str]:
    failures: list[str] = []

    def require(condition: bool, code: str) -> None:
        if not condition:
            failures.append(code)

    require(data.get("status") == "CANONICAL_PERMANENT_OPERATING_CONSTITUTION", "STATUS")
    require(data.get("constitution_version") == "2.0-fast-compression", "CONSTITUTION_VERSION")
    require(data.get("effective_date") == "2026-09-10", "EFFECTIVE_DATE")
    require(data.get("north_star") == "CASH_READY_AUTONOMOUS_DEALIX_COMPANY", "NORTH_STAR")
    require(data.get("optimize_for") == "Verified Economic Movement / Founder Minutes / Cost / Risk", "OPTIMIZATION")

    agents = _list(data, "permanent_agents")
    require(agents == EXPECTED_AGENTS, "PERMANENT_AGENTS_EXACT")
    require(len(set(agents)) == 5, "PERMANENT_AGENTS_UNIQUE")

    portfolios = _list(data, "portfolios")
    require(portfolios == EXPECTED_PORTFOLIOS, "PORTFOLIOS_EXACT")

    one_company = set(str(x) for x in _list(data, "one_company_law"))
    require(REQUIRED_ONE_COMPANY <= one_company, "ONE_COMPANY_LAW")

    compression = data.get("compression_law", {})
    require(isinstance(compression, dict), "COMPRESSION_LAW")
    if isinstance(compression, dict):
        require(compression.get("compress_time") is True, "COMPRESS_TIME")
        require(compression.get("compress_truth") is False, "NEVER_COMPRESS_TRUTH")
        require(compression.get("parallel_lanes_allowed") is True, "PARALLEL_LANES")
        require(compression.get("prerequisite_gates_may_not_be_bypassed") is True, "NO_GATE_BYPASS")
        require(compression.get("deep_wip_max") == 3, "DEEP_WIP_MAX")

    engines = set(str(x) for x in _list(data, "strategic_engines"))
    require(REQUIRED_ENGINES <= engines, "STRATEGIC_ENGINES")

    arm_registry = data.get("arm_registry", {})
    require(isinstance(arm_registry, dict), "ARM_REGISTRY")
    if isinstance(arm_registry, dict):
        require(arm_registry.get("path") == "config/company/dealix_arm_registry.json", "ARM_REGISTRY_PATH")
        require(arm_registry.get("deep_wip_max") == 3, "ARM_REGISTRY_WIP")
        require(arm_registry.get("sell_before_build") is True, "SELL_BEFORE_BUILD")
        require(arm_registry.get("customer_pull_before_saas") is True, "CUSTOMER_PULL_BEFORE_SAAS")
        require(arm_registry.get("no_new_permanent_agent_per_arm") is True, "NO_AGENT_PER_ARM")
        require(arm_registry.get("no_duplicate_company_system_per_arm") is True, "NO_DUPLICATE_SYSTEM_PER_ARM")

    truth = set(str(x) for x in _list(data, "truth_firewall"))
    require(REQUIRED_TRUTH <= truth, "TRUTH_FIREWALL")

    commercial_loop = set(str(x) for x in _list(data, "canonical_commercial_loop"))
    require(REQUIRED_COMMERCIAL_STAGES <= commercial_loop, "COMMERCIAL_LOOP")

    wedges = _list(data, "active_gtm_wedges")
    require(data.get("active_gtm_wedge_limit") == 3, "ACTIVE_GTM_WEDGE_LIMIT")
    require(1 <= len(wedges) <= int(data.get("active_gtm_wedge_limit", 0) or 0), "ACTIVE_GTM_WIP")
    require(len(set(str(x) for x in wedges)) == len(wedges), "ACTIVE_GTM_WEDGES_UNIQUE")
    require(all(isinstance(x, str) and x.strip() for x in wedges), "ACTIVE_GTM_WEDGES_VALID")

    allocation = data.get("opportunity_allocation", {})
    require(isinstance(allocation, dict), "OPPORTUNITY_ALLOCATION")
    if isinstance(allocation, dict):
        require(allocation.get("top_active_actions_per_cycle") == 3, "TOP_ACTION_WIP")
        require(allocation.get("diagnostic_wip_limit") == 3, "DIAGNOSTIC_WIP")
        require(allocation.get("capability_benchmark_limit") == 1, "OSS_BENCHMARK_WIP")
        require(allocation.get("live_project_cell_limit") == 2, "PROJECT_CELL_WIP")

    recurring = data.get("low_touch_recurring_law", {})
    require(isinstance(recurring, dict), "LOW_TOUCH_RECURRING_LAW")
    if isinstance(recurring, dict):
        require(recurring.get("permission_safe_data_only") is True, "PERMISSION_SAFE_DATA")
        require(recurring.get("no_customer_data_reuse_without_authority") is True, "NO_DATA_REUSE_WITHOUT_AUTHORITY")

    moat = data.get("data_moat", {})
    require(isinstance(moat, dict), "DATA_MOAT")
    if isinstance(moat, dict):
        graphs = set(str(x) for x in moat.get("graphs", []) if isinstance(x, str))
        require({"COMPANY_GRAPH", "OPPORTUNITY_GRAPH", "PROCESS_GRAPH", "PROOF_GRAPH", "POLICY_GRAPH", "ECONOMIC_GRAPH", "LEARNING_GRAPH"} <= graphs, "DATA_MOAT_GRAPHS")

    partner_first = data.get("regulated_and_partner_first_law", {})
    require(isinstance(partner_first, dict), "REGULATED_PARTNER_FIRST")
    if isinstance(partner_first, dict):
        require(partner_first.get("no_certification_claim_without_evidence") is True, "NO_FALSE_CERTIFICATION")
        require(partner_first.get("no_government_access_claim_without_evidence") is True, "NO_FALSE_GOV_ACCESS")

    agent_control = data.get("interoperability_and_agent_control", {})
    require(isinstance(agent_control, dict), "AGENT_CONTROL")
    if isinstance(agent_control, dict):
        require(agent_control.get("no_unbounded_shell_or_prod_admin") is True, "NO_UNBOUNDED_AGENT_ADMIN")
        require(bool(str(agent_control.get("mcp", "")).strip()), "MCP_BOUNDARY")
        require(bool(str(agent_control.get("a2a", "")).strip()), "A2A_BOUNDARY")

    channel = data.get("channel_policy", {})
    require(isinstance(channel, dict), "CHANNEL_POLICY")
    if isinstance(channel, dict):
        email = channel.get("email", {})
        wa = channel.get("whatsapp", {})
        linkedin = channel.get("linkedin", {})
        require(isinstance(email, dict) and email.get("bulk_unsolicited_allowed") is False, "EMAIL_NO_BULK_UNSOLICITED")
        require(isinstance(wa, dict) and wa.get("cold_blending_or_blasts_allowed") is False, "WHATSAPP_NO_COLD_BLAST")
        require(isinstance(wa, dict) and wa.get("discovered_number_is_permission") is False, "WHATSAPP_DISCOVERY_NOT_PERMISSION")
        require(isinstance(wa, dict) and wa.get("requires_number_provided_and_opt_in") is True, "WHATSAPP_OPT_IN")
        require(isinstance(linkedin, dict) and linkedin.get("mass_automation_allowed") is False, "LINKEDIN_NO_MASS_AUTOMATION")

    autonomy = data.get("autonomy", {})
    require(isinstance(autonomy, dict), "AUTONOMY")
    if isinstance(autonomy, dict):
        require(autonomy.get("L4") == "repository execute", "L4")
        require(autonomy.get("L5") == "material/external exact-action-bound only", "L5")

    material = set(str(x) for x in _list(data, "material_actions_requiring_exact_current_authority"))
    require(REQUIRED_MATERIAL <= material, "MATERIAL_ACTIONS")

    proof = data.get("proof_law", {})
    require(isinstance(proof, dict), "PROOF_LAW")
    if isinstance(proof, dict):
        require(proof.get("activity_is_not_revenue") is True, "ACTIVITY_NOT_REVENUE")
        require(proof.get("quote_is_not_payment") is True, "QUOTE_NOT_PAYMENT")
        require(proof.get("internal_or_synthetic_proof_is_not_customer_proof") is True, "SYNTHETIC_NOT_CUSTOMER_PROOF")

    productization = data.get("productization_law", {})
    require(isinstance(productization, dict), "PRODUCTIZATION_LAW")
    if isinstance(productization, dict):
        require(productization.get("service_first") is True, "SERVICE_FIRST")
        require(productization.get("build_requires_paid_pain_or_evidence") is True, "EVIDENCE_GATED_BUILD")
        require(productization.get("repeatability_precedes_saas") is True, "REPEATABILITY_BEFORE_SAAS")

    tool_states = set(str(x) for x in _list(data, "tool_admission_states"))
    require(REQUIRED_TOOL_STATES <= tool_states, "TOOL_ADMISSION_STATES")

    forbidden = {str(x).lower() for x in _list(data, "forbidden_shortcuts")}
    require(any("cold whatsapp" in x for x in forbidden), "FORBID_COLD_WHATSAPP")
    require(any("mass linkedin" in x for x in forbidden), "FORBID_MASS_LINKEDIN")
    require(any("fake" in x and "proof" in x for x in forbidden), "FORBID_FAKE_PROOF")
    require(any("parallel company os" in x for x in forbidden), "FORBID_PARALLEL_OS")
    require(any("one permanent agent per business arm" in x for x in forbidden), "FORBID_AGENT_PER_ARM")
    require(_forbids_deep_building_every_researched_arm(forbidden), "FORBID_UNBOUNDED_ARM_BUILD")

    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify Dealix permanent operating constitution")
    parser.add_argument("--path", default=str(DEFAULT_PATH))
    args = parser.parse_args()
    path = Path(args.path)

    if not path.is_file():
        print(f"DEALIX_OPERATING_CONSTITUTION_VERIFY=FAIL missing={path}")
        return 2
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"DEALIX_OPERATING_CONSTITUTION_VERIFY=FAIL parse={type(exc).__name__}")
        return 2
    if not isinstance(data, dict):
        print("DEALIX_OPERATING_CONSTITUTION_VERIFY=FAIL root_not_object")
        return 2

    failures = verify(data)
    if failures:
        print("DEALIX_OPERATING_CONSTITUTION_VERIFY=FAIL " + ",".join(failures))
        return 2

    print("DEALIX_OPERATING_CONSTITUTION_VERIFY=PASS")
    print(f"CONSTITUTION_VERSION={data['constitution_version']}")
    print(f"NORTH_STAR={data['north_star']}")
    print("PERMANENT_AGENTS=5")
    print("PORTFOLIOS=TRUST,MONEY_NOW,COMPOUNDING")
    print(f"ACTIVE_GTM_WEDGES={len(_list(data, 'active_gtm_wedges'))}")
    print("DEEP_WIP_MAX=3")
    print("L5=EXACT_ACTION_BOUND_ONLY")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())