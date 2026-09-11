from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "config" / "company" / "dealix_meta_operating_system_v2.json"
VERIFY = ROOT / "scripts" / "commercial" / "verify_dealix_meta_operating_system_v2.py"
META_RUNTIME = ROOT / "scripts" / "commercial" / "run_dealix_meta_control_v2.py"
COMMAND_ROOM = ROOT / "scripts" / "commercial" / "run_dealix_command_room_v1.py"
MASTER = ROOT / "scripts" / "commercial" / "run_dealix_master_company_cycle_v1.py"
BINDING = ROOT / "config" / "company" / "dealix_master_prompt_binding_v1.json"

CANONICAL_AGENTS = {
    "dealix-pm",
    "dealix-sales",
    "dealix-delivery",
    "dealix-engineer",
    "dealix-content",
}


def load() -> dict:
    return json.loads(CONFIG.read_text(encoding="utf-8"))


def test_v2_verifier_passes() -> None:
    result = subprocess.run(
        [sys.executable, str(VERIFY)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "DEALIX_META_OPERATING_SYSTEM_V2=PASS" in result.stdout
    assert "UNIVERSAL_L5=false" in result.stdout


def test_exact_five_agents_and_deep_wip_three() -> None:
    data = load()
    assert set(data["permanent_agents"]) == CANONICAL_AGENTS
    assert len(data["permanent_agents"]) == 5
    assert data["deep_wip_max"] == 3
    assert "PERMANENT_AGENTS == 5" in data["invariants"]
    assert "DEEP_WIP <= 3" in data["invariants"]


def test_economic_dispatcher_is_normalized_and_balanced() -> None:
    data = load()["economic_dispatcher"]
    assert data["normalization"] == {"min": 0.0, "max": 1.0}
    assert abs(sum(data["value_weights"].values()) - 1.0) < 1e-9
    assert abs(sum(data["execution_drag_weights"].values()) - 1.0) < 1e-9
    assert data["drag_floor"] == 0.20
    assert data["score_is_decision_aid_not_truth"] is True


def test_business_truth_state_machines_are_not_collapsed() -> None:
    machines = load()["state_machines"]
    opportunity = machines["opportunity"]
    financial = machines["financial"]
    production = machines["production"]
    assert opportunity.index("QUOTED") < opportunity.index("PAYMENT_PENDING") < opportunity.index("PAID")
    assert financial.index("INVOICE") < financial.index("PAYMENT_VERIFIED") < financial.index("CASH_AVAILABLE")
    assert production[-1] == "PRODUCTION_GREEN"
    assert production.index("HEALTHY") < production.index("RELEASE_PARITY_PROVEN")
    assert machines["illegal_transition_action"] == "BLOCK"


def test_identity_runtime_and_l5_boundaries_fail_closed() -> None:
    data = load()
    assert data["identity"]["separate_agent_and_workload_identity"] is True
    assert data["identity"]["spiffe_spire"]["auto_install"] is False
    assert data["runtime_control"]["runtime_policy_required"] is True
    assert data["runtime_control"]["prompt_policy_only_is_sufficient"] is False
    assert data["a2a"]["agent_card_is_authority"] is False
    assert data["l5"] == {
        "universal_authority": False,
        "exact_action_bound": True,
        "material_effects_default": False,
    }


def test_master_binding_points_to_v2_control() -> None:
    binding = json.loads(BINDING.read_text(encoding="utf-8"))
    assert binding["meta_control_ref"] == "config/company/dealix_meta_operating_system_v2.json"
    assert binding["meta_control_verifier_ref"] == "scripts/commercial/verify_dealix_meta_operating_system_v2.py"
    assert binding["meta_control_runtime_ref"] == "scripts/commercial/run_dealix_meta_control_v2.py"
    assert binding["meta_control_precedence"] == "OVERRIDES_CONFLICTING_LOWER_LEVEL_OPERATING_LOGIC"


def test_command_room_requires_meta_control_before_agents() -> None:
    text = COMMAND_ROOM.read_text(encoding="utf-8")
    assert "META_CONTROL = ROOT" in text
    assert "COMMAND_ROOM=BLOCKED_META_CONTROL_V2" in text
    assert "DEALIX_META_CONTROL_BOUND" in text
    assert "DEALIX_PERMANENT_AGENT_ID" in text
    assert "DEALIX_UNIVERSAL_L5" in text
    assert "META_CONTROL_BOUND_TO_ALL_EXECUTED_AGENT_LANES=true" in text
    for agent in CANONICAL_AGENTS:
        assert agent in text


def test_master_cycle_binds_same_meta_sha_and_disables_material_effects() -> None:
    text = MASTER.read_text(encoding="utf-8")
    assert 'env["DEALIX_META_CONTROL_BOUND"] = "1"' in text
    assert 'env["DEALIX_UNIVERSAL_L5"] = "0"' in text
    assert 'env["DEALIX_EXTERNAL_SEND"] = "0"' in text
    assert 'env["PUBLIC_PUBLISH"] = "0"' in text
    assert 'env["PAYMENT_EXECUTION"] = "0"' in text
    assert 'env["PRODUCTION_MUTATION"] = "0"' in text


def test_runtime_receipt_does_not_overclaim_future_controls() -> None:
    text = META_RUNTIME.read_text(encoding="utf-8")
    assert "LOCAL_RUNTIME_DERIVED_NOT_CRYPTOGRAPHICALLY_ATTESTED" in text
    assert "PARTIAL_EXISTING_ADAPTERS_NOT_UNIVERSALLY_PROVEN" in text
    assert "DECLARED_CONTRACT_NOT_UNIVERSALLY_PROVEN" in text
    assert "TARGET_ARCHITECTURE_NOT_CLAIMED_ACTIVE" in text
    assert "TRIGGERED_FUTURE_OPTION_NOT_ACTIVE" in text
    assert "EXTERNAL_EFFECTS=NONE_BY_META_CONTROL" in text
