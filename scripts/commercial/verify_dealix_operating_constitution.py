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
    "SI_MSP_ERP_CRM_AI_IMPLEMENTERS",
    "FATOORA_INTEGRATION_OPERATIONS",
    "CONSTRUCTION_FM_COMMERCIAL_EXECUTION",
]
REQUIRED_ONE_COMPANY = {
    "ONE_COMPANY_MACHINE",
    "ONE_COMPANY_BRAIN",
    "ONE_OPPORTUNITY_GRAPH",
    "ONE_APPROVAL_AUTHORITY",
    "ONE_CONSENT_AUTHORITY",
    "ONE_PROOF_LEDGER",
    "ONE_ECONOMIC_MODEL",
    "ONE_CANONICAL_SCHEDULER",
    "ONE_MODEL_ROUTER",
    "ONE_DEV_FACTORY",
    "ONE_LEARNING_FACTORY",
}
REQUIRED_TRUTH = {
    "Research != Relationship",
    "Public Contact != Consent",
    "Signal != Opportunity",
    "Draft != Sent",
    "Quote != Invoice",
    "Invoice != Payment",
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


def _list(data: dict[str, Any], key: str) -> list[Any]:
    value = data.get(key)
    return value if isinstance(value, list) else []


def verify(data: dict[str, Any]) -> list[str]:
    failures: list[str] = []

    def require(condition: bool, code: str) -> None:
        if not condition:
            failures.append(code)

    require(data.get("status") == "CANONICAL_PERMANENT_OPERATING_CONSTITUTION", "STATUS")
    require(data.get("north_star") == "CASH_READY_AUTONOMOUS_DEALIX_COMPANY", "NORTH_STAR")
    require(data.get("optimize_for") == "Verified Economic Movement / Founder Minutes / Cost / Risk", "OPTIMIZATION")

    agents = _list(data, "permanent_agents")
    require(agents == EXPECTED_AGENTS, "PERMANENT_AGENTS_EXACT")
    require(len(set(agents)) == 5, "PERMANENT_AGENTS_UNIQUE")

    portfolios = _list(data, "portfolios")
    require(portfolios == EXPECTED_PORTFOLIOS, "PORTFOLIOS_EXACT")

    one_company = set(str(x) for x in _list(data, "one_company_law"))
    require(REQUIRED_ONE_COMPANY <= one_company, "ONE_COMPANY_LAW")

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
        require(allocation.get("capability_benchmark_limit") == 1, "OSS_BENCHMARK_WIP")
        require(allocation.get("live_project_cell_limit") == 2, "PROJECT_CELL_WIP")

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

    forbidden = {str(x).lower() for x in _list(data, "forbidden_shortcuts")}
    require(any("cold whatsapp" in x for x in forbidden), "FORBID_COLD_WHATSAPP")
    require(any("mass linkedin" in x for x in forbidden), "FORBID_MASS_LINKEDIN")
    require(any("fake" in x and "proof" in x for x in forbidden), "FORBID_FAKE_PROOF")
    require(any("parallel company os" in x for x in forbidden), "FORBID_PARALLEL_OS")

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
    print(f"NORTH_STAR={data['north_star']}")
    print("PERMANENT_AGENTS=5")
    print("PORTFOLIOS=TRUST,MONEY_NOW,COMPOUNDING")
    print(f"ACTIVE_GTM_WEDGES={len(_list(data, 'active_gtm_wedges'))}")
    print("L5=EXACT_ACTION_BOUND_ONLY")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
