from __future__ import annotations

import json
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "dealix/config/commercial_reset_2026_09_12.yaml"
FRESH_POLICY = ROOT / "config/company/fresh_market_execution_policy.json"
ARCHITECTURE_DOC = ROOT / "docs/architecture/DEALIX_AGENTIC_HOLDING_SECTOR_MESH.md"
PLAYBOOK = ROOT / "docs/commercial/COMMERCIAL_RESET_AGENT_PLAYBOOK_2026_09_12.md"
SKILL = ROOT / "skills/hermes/dealix-commercial-reset/SKILL.md"
MASTER = ROOT / "prompts/company/DEALIX_COMMERCIAL_RESET_AGENT_MASTER_PROMPT_2026_09_12.md"

LEGACY_OWNER_ALIASES = {
    "dealix-pm",
    "dealix-sales",
    "dealix-delivery",
    "dealix-engineer",
    "dealix-content",
}


def _load() -> dict:
    data = yaml.safe_load(CONFIG.read_text(encoding="utf-8"))
    assert isinstance(data, dict)
    return data


def _fresh_policy() -> dict:
    data = json.loads(FRESH_POLICY.read_text(encoding="utf-8"))
    assert isinstance(data, dict)
    return data


def test_commercial_reset_files_exist() -> None:
    for path in (CONFIG, FRESH_POLICY, ARCHITECTURE_DOC, PLAYBOOK, SKILL, MASTER):
        assert path.is_file(), f"missing commercial-reset artifact: {path}"


def test_entry_diagnostic_is_free_and_cardless() -> None:
    data = _load()
    entry = data["entry_offer"]
    assert entry["price_public"] == "FREE"
    assert entry["card_required"] is False
    assert data["pricing"]["public_fixed_prices"] is False
    assert data["pricing"]["customer_specific_only"] is True


def test_commercial_reset_uses_agentic_holding_not_fixed_five() -> None:
    data = _load()
    fresh = _fresh_policy()
    architecture = data["architecture"]
    assert architecture["model"] == "agentic_holding_sector_company_mesh"
    assert fresh["architecture"]["model"] == architecture["model"]
    assert architecture["legacy_fixed_five_permanent_agents"] == "deprecated"
    assert fresh["architecture"]["legacy_fixed_five_permanent_agents"] == "deprecated"
    assert set(architecture["legacy_owner_aliases"]) == LEGACY_OWNER_ALIASES
    assert len(architecture["group_roles"]) >= 20
    assert len(architecture["sector_role_templates"]) >= 20
    assert {"lead", "scout", "operator", "verifier"} <= set(architecture["arm_pod_roles"])


def test_runtime_is_lazy_resource_governed_and_orphan_free() -> None:
    data = _load()
    fresh = _fresh_policy()
    architecture = data["architecture"]
    assert architecture["runtime_workers"] == "lazy_resource_governed"
    assert architecture["orphan_agents_allowed"] is False
    assert architecture["repo_writers"] == "isolated_worktrees"
    assert fresh["execution"]["resource_aware_concurrency_governor"] is True
    assert fresh["execution"]["legacy_global_deep_wip_max_3"] == "deprecated"


def test_external_material_effects_default_closed() -> None:
    data = _load()
    autonomy = data["autonomy"]
    assert autonomy["external_send"] is False
    assert autonomy["public_publish"] is False
    assert autonomy["payment_or_spend"] is False
    assert autonomy["production_mutation"] is False
    assert autonomy["dns_db_secret_mutation"] is False


def test_email_contract_is_consent_aware_and_draft_only() -> None:
    data = _load()
    contract = data["email_draft_contract"]
    assert contract["defaults"]["send"] is False
    assert contract["defaults"]["safe_to_send"] is False
    assert "cold_whatsapp" in contract["forbidden"]
    assert "scraped_contact_as_consent" in contract["forbidden"]
    assert "DOCUMENTED_OPT_IN" in contract["allowed_contexts"]


def test_proposal_contract_blocks_overclaim_and_fixed_price_authority() -> None:
    data = _load()
    forbidden = set(data["proposal_contract"]["forbidden"])
    assert {
        "fabricated_roi",
        "fabricated_customer_proof",
        "guaranteed_outcome",
        "public_fixed_price_as_authority",
        "blanket_compliance_claim",
        "government_access_claim",
    } <= forbidden


def test_money_now_campaigns_present_with_sources() -> None:
    data = _load()
    campaigns = {row["id"]: row for row in data["campaigns"]}
    assert campaigns["SAUDI_AI_ADOPTION"]["status"] == "MONEY_NOW"
    assert campaigns["FATOORA_WAVE_25"]["status"] == "MONEY_NOW"
    assert campaigns["OPERATIONS_AUTOMATION"]["status"] == "MONEY_NOW"
    for campaign in campaigns.values():
        assert campaign["source"].startswith("https://")
        assert campaign["evidence"].strip()


def test_function_routing_covers_commercial_closed_loop() -> None:
    data = _load()
    routing = data["commercial_function_routing"]
    for function in (
        "MARKET_INTELLIGENCE",
        "OPPORTUNITY_SCORING",
        "DIAGNOSTIC",
        "DISCOVERY",
        "SOLUTION_DESIGN",
        "PROPOSAL_DRAFT",
        "PRICING_PREP",
        "GOVERNANCE_REVIEW",
        "DELIVERY",
        "PROOF",
        "ENGINEERING",
        "CONTENT",
        "SELF_IMPROVEMENT",
    ):
        assert function in routing
        assert routing[function]["group_role"]
        assert routing[function]["sector_role"]
        assert routing[function]["arm_role"]


def test_playbook_and_prompt_preserve_truth_firewall_and_holding() -> None:
    combined = "\n".join(
        path.read_text(encoding="utf-8") for path in (PLAYBOOK, SKILL, MASTER)
    )
    assert "Agentic Holding" in combined
    for phrase in (
        "Research != Relationship",
        "Public contact != Consent",
        "Draft != Sent",
        "Quote != Invoice",
        "Invoice != Payment",
        "Delivery != Customer Value",
    ):
        assert phrase in combined


def test_pricing_bands_are_explicitly_internal_only() -> None:
    data = _load()
    pricing = data["pricing"]
    assert pricing["internal_reference_bands_sar"]
    warning = pricing["warning"].lower()
    assert "internal" in warning
    assert "not public pricing" in warning
    assert "not doctrine" in warning
