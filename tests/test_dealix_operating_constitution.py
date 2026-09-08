from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERIFY_PATH = ROOT / "scripts" / "commercial" / "verify_dealix_operating_constitution.py"
SPEC = importlib.util.spec_from_file_location("constitution_verify", VERIFY_PATH)
assert SPEC and SPEC.loader
MOD = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MOD)


def valid_payload() -> dict:
    return {
        "status": "CANONICAL_PERMANENT_OPERATING_CONSTITUTION",
        "north_star": "CASH_READY_AUTONOMOUS_DEALIX_COMPANY",
        "optimize_for": "Verified Economic Movement / Founder Minutes / Cost / Risk",
        "permanent_agents": MOD.EXPECTED_AGENTS,
        "portfolios": MOD.EXPECTED_PORTFOLIOS,
        "one_company_law": sorted(MOD.REQUIRED_ONE_COMPANY),
        "truth_firewall": sorted(MOD.REQUIRED_TRUTH),
        "canonical_commercial_loop": sorted(MOD.REQUIRED_COMMERCIAL_STAGES),
        "active_gtm_wedges": MOD.CURRENT_SEED_WEDGES,
        "active_gtm_wedge_limit": 3,
        "opportunity_allocation": {
            "top_active_actions_per_cycle": 3,
            "capability_benchmark_limit": 1,
            "live_project_cell_limit": 2,
        },
        "channel_policy": {
            "email": {"bulk_unsolicited_allowed": False},
            "whatsapp": {
                "cold_blending_or_blasts_allowed": False,
                "discovered_number_is_permission": False,
                "requires_number_provided_and_opt_in": True,
            },
            "linkedin": {"mass_automation_allowed": False},
        },
        "autonomy": {"L4": "repository execute", "L5": "material/external exact-action-bound only"},
        "material_actions_requiring_exact_current_authority": sorted(MOD.REQUIRED_MATERIAL),
        "proof_law": {
            "activity_is_not_revenue": True,
            "quote_is_not_payment": True,
            "internal_or_synthetic_proof_is_not_customer_proof": True,
        },
        "productization_law": {
            "service_first": True,
            "build_requires_paid_pain_or_evidence": True,
            "repeatability_precedes_saas": True,
        },
        "forbidden_shortcuts": [
            "cold WhatsApp blasting",
            "mass LinkedIn automation",
            "fake customer proof",
            "parallel Company OS / Brain / CRM / scheduler / permanent agent fleet",
        ],
    }


def test_valid_contract_passes():
    assert MOD.verify(valid_payload()) == []


def test_sixth_permanent_agent_fails():
    payload = valid_payload()
    payload["permanent_agents"] = [*MOD.EXPECTED_AGENTS, "dealix-extra"]
    assert "PERMANENT_AGENTS_EXACT" in MOD.verify(payload)


def test_fourth_gtm_wedge_fails():
    payload = valid_payload()
    payload["active_gtm_wedges"] = [*MOD.CURRENT_SEED_WEDGES, "EXTRA_WEDGE"]
    assert "ACTIVE_GTM_WIP" in MOD.verify(payload)


def test_alternative_three_wedge_policy_is_allowed():
    payload = valid_payload()
    payload["active_gtm_wedges"] = ["A", "B", "C"]
    assert MOD.verify(payload) == []


def test_whatsapp_permission_shortcut_fails():
    payload = valid_payload()
    payload["channel_policy"]["whatsapp"]["discovered_number_is_permission"] = True
    assert "WHATSAPP_DISCOVERY_NOT_PERMISSION" in MOD.verify(payload)


def test_l5_self_authority_fails():
    payload = valid_payload()
    payload["autonomy"]["L5"] = "automatic"
    assert "L5" in MOD.verify(payload)
