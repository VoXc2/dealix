from __future__ import annotations

import json
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]
CONFIG = ROOT / "dealix/config/commercial_reset_2026_09_12.yaml"
FRESH_POLICY = ROOT / "config/company/fresh_market_execution_policy.json"
ARCHITECTURE_DOC = ROOT / "docs/architecture/DEALIX_AGENTIC_HOLDING_SECTOR_MESH.md"
PLAYBOOK = ROOT / "docs/commercial/COMMERCIAL_RESET_AGENT_PLAYBOOK_2026_09_12.md"
SKILL = ROOT / "skills/hermes/dealix-commercial-reset/SKILL.md"
MASTER = ROOT / "prompts/company/DEALIX_COMMERCIAL_RESET_AGENT_MASTER_PROMPT_2026_09_12.md"
PACKET = ROOT / "scripts/commercial/commercial_reset_agent_packet.py"

EXPECTED_LEGACY_ALIASES = {
    "dealix-pm",
    "dealix-sales",
    "dealix-delivery",
    "dealix-engineer",
    "dealix-content",
}
EXPECTED_MONEY_NOW = {
    "SAUDI_AI_ADOPTION",
    "FATOORA_WAVE_25",
    "OPERATIONS_AUTOMATION",
}
EXPECTED_ARM_ROLES = {"lead", "scout", "operator", "verifier"}


def verify() -> dict[str, object]:
    files = [CONFIG, FRESH_POLICY, ARCHITECTURE_DOC, PLAYBOOK, SKILL, MASTER, PACKET]
    missing = [str(path.relative_to(ROOT)) for path in files if not path.is_file()]
    if missing:
        return {"verdict": "FAIL", "reason": "missing_files", "missing": missing}

    data = yaml.safe_load(CONFIG.read_text(encoding="utf-8"))
    policy = json.loads(FRESH_POLICY.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or not isinstance(policy, dict):
        return {"verdict": "FAIL", "reason": "authority_not_mapping"}

    failures: list[str] = []
    if data.get("entry_offer", {}).get("price_public") != "FREE":
        failures.append("diagnostic_not_free")
    if data.get("entry_offer", {}).get("card_required") is not False:
        failures.append("diagnostic_card_required")

    pricing = data.get("pricing", {})
    if pricing.get("public_fixed_prices") is not False:
        failures.append("public_fixed_pricing_enabled")
    if pricing.get("customer_specific_only") is not True:
        failures.append("customer_specific_pricing_disabled")

    architecture = data.get("architecture", {})
    policy_architecture = policy.get("architecture", {})
    if architecture.get("model") != "agentic_holding_sector_company_mesh":
        failures.append("commercial_reset_not_agentic_holding")
    if policy_architecture.get("model") != architecture.get("model"):
        failures.append("architecture_policy_mismatch")
    if architecture.get("legacy_fixed_five_permanent_agents") != "deprecated":
        failures.append("legacy_five_agent_invariant_restored")
    if policy_architecture.get("legacy_fixed_five_permanent_agents") != "deprecated":
        failures.append("fresh_policy_legacy_five_not_deprecated")
    if architecture.get("runtime_workers") != "lazy_resource_governed":
        failures.append("runtime_workers_not_resource_governed")
    if architecture.get("orphan_agents_allowed") is not False:
        failures.append("orphan_agents_allowed")
    if set(architecture.get("legacy_owner_aliases", {})) != EXPECTED_LEGACY_ALIASES:
        failures.append("legacy_alias_compatibility_drift")
    if len(architecture.get("group_roles", [])) < 20:
        failures.append("group_role_catalog_too_small")
    if len(architecture.get("sector_role_templates", [])) < 20:
        failures.append("sector_role_catalog_too_small")
    if not EXPECTED_ARM_ROLES <= set(architecture.get("arm_pod_roles", [])):
        failures.append("arm_pod_roles_missing")
    if policy.get("execution", {}).get("resource_aware_concurrency_governor") is not True:
        failures.append("resource_governor_disabled")
    if policy.get("execution", {}).get("legacy_global_deep_wip_max_3") != "deprecated":
        failures.append("legacy_deep_wip_restored")

    autonomy = data.get("autonomy", {})
    for field in (
        "external_send",
        "public_publish",
        "payment_or_spend",
        "production_mutation",
        "dns_db_secret_mutation",
    ):
        if autonomy.get(field) is not False:
            failures.append(f"unsafe_autonomy:{field}")

    money_now = {
        row.get("id")
        for row in data.get("campaigns", [])
        if isinstance(row, dict) and row.get("status") == "MONEY_NOW"
    }
    if not EXPECTED_MONEY_NOW <= money_now:
        failures.append("money_now_campaign_drift")
    for row in data.get("campaigns", []):
        if not isinstance(row, dict) or not str(row.get("source", "")).startswith("https://"):
            failures.append("campaign_missing_source")
            break

    combined = "\n".join(path.read_text(encoding="utf-8") for path in (PLAYBOOK, SKILL, MASTER))
    if "Agentic Holding" not in combined:
        failures.append("agentic_holding_missing_from_agent_docs")
    for phrase in (
        "Research != Relationship",
        "Public contact != Consent",
        "Draft != Sent",
        "Quote != Invoice",
        "Invoice != Payment",
        "Delivery != Customer Value",
    ):
        if phrase not in combined:
            failures.append(f"truth_firewall_missing:{phrase}")

    return {
        "verdict": "FAIL" if failures else "PASS",
        "commercial_reset": data.get("name"),
        "authority_date": data.get("version"),
        "architecture": architecture.get("model"),
        "legacy_five_agent_invariant": architecture.get("legacy_fixed_five_permanent_agents"),
        "legacy_owner_aliases": sorted(architecture.get("legacy_owner_aliases", {})),
        "logical_group_roles": len(architecture.get("group_roles", [])),
        "sector_role_templates": len(architecture.get("sector_role_templates", [])),
        "arm_pod_roles": architecture.get("arm_pod_roles", []),
        "runtime_workers": architecture.get("runtime_workers"),
        "money_now": sorted(money_now),
        "free_diagnostic": data.get("entry_offer", {}).get("price_public") == "FREE",
        "public_fixed_prices": pricing.get("public_fixed_prices"),
        "external_send": autonomy.get("external_send"),
        "failures": failures,
    }


def main() -> int:
    receipt = verify()
    print(json.dumps(receipt, ensure_ascii=False, indent=2))
    print(f"DEALIX_COMMERCIAL_RESET_AGENT_FACTORY={receipt['verdict']}")
    return 0 if receipt["verdict"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
