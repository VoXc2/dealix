from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from auto_client_acquisition.ai_workforce.canonical_delegation import CANONICAL_AGENTS
from auto_client_acquisition.orchestrator.canonical_operating_company import (
    build_canonical_operating_company_summary,
)

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "data/ops/end_to_end_company_acceptance_v1.json"
VERIFIER = ROOT / "scripts/ops/verify_end_to_end_company_acceptance_v1.py"


def _data() -> dict:
    return json.loads(CONTRACT.read_text(encoding="utf-8"))


def test_composite_verifier_passes() -> None:
    result = subprocess.run(
        [sys.executable, str(VERIFIER)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "DEALIX_END_TO_END_COMPANY_ACCEPTANCE_V1=PASS" in result.stdout


def test_lifecycle_is_complete_and_ordered() -> None:
    data = _data()
    lifecycle = data["client_lifecycle"]
    assert [row["order"] for row in lifecycle] == list(range(1, 19))
    assert lifecycle[0]["stage"] == "MARKET_SIGNAL"
    assert lifecycle[-1]["stage"] == "LEARNING_AND_PRODUCTIZATION"
    assert len({row["stage"] for row in lifecycle}) == 18


def test_all_agents_and_systems_own_real_work() -> None:
    data = _data()
    agents = set(data["canonical_agents"])
    systems = set(data["canonical_systems"])
    lifecycle = data["client_lifecycle"]
    assert {row["owner"] for row in lifecycle} == agents
    assert {system for row in lifecycle for system in row["systems"]} == systems


def test_operating_company_summary_exposes_five_canonical_agents_only() -> None:
    summary = build_canonical_operating_company_summary()
    assert summary["canonical_agents_total"] == 5
    assert set(summary["canonical_agents"]) == set(CANONICAL_AGENTS)
    assert summary["specialist_roles_total"] == 15
    assert summary["specialist_role_semantics"] == "BOUNDED_WORKLOAD_NOT_PERMANENT_AGENT"
    assert summary["legacy_agents_total_compatibility"] == 15
    assert summary["legacy_agents_total_authoritative"] is False
    assert "agents_total" not in summary


def test_low_founder_intervention_does_not_self_grant_l5() -> None:
    data = _data()
    founder = data["founder_attention_model"]
    assert founder["automatic_levels"] == ["L0", "L1", "L2", "L3", "L4"]
    assert founder["external_level"] == "L5_ACTION_BOUND"
    assert founder["may_self_grant_external_authority"] is False


def test_founder_voice_is_human_quality_without_impersonation() -> None:
    voice = _data()["founder_voice_policy"]
    assert voice["drafting_from_approved_style_profile"] is True
    assert voice["may_claim_human_founder_identity"] is False
    assert voice["may_fabricate_personal_experience"] is False
    assert voice["may_fabricate_relationship_or_memory"] is False
    assert voice["may_hide_material_automation"] is False


def test_lead_acquisition_cannot_turn_public_data_into_permission() -> None:
    policy = _data()["lead_acquisition_policy"]
    forbidden = set(policy["forbidden"])
    assert {
        "scraping",
        "cold_whatsapp",
        "mass_linkedin_automation",
        "identity_deception",
        "consent_inference_from_public_data",
    } <= forbidden


def test_connector_apps_are_adapters_not_parallel_truth_stores() -> None:
    data = _data()
    composition = data["composition_only"]
    assert composition
    assert all(value is False for value in composition.values())
    connectors = data["connector_control_plane"]
    ids = [row["id"] for row in connectors]
    assert len(ids) == len(set(ids))
    mirrors = {row["id"]: row["truth_owner"] for row in connectors}
    assert mirrors["airtable_hubspot"] is False
    assert mirrors["posthog_sentry_otel_langfuse"] is False
    assert mirrors["canva_gamma_drive"] is False


def test_telegram_openclaw_is_canonical_founder_connector_and_slack_is_not_a_launch_dependency() -> None:
    data = _data()
    founder_control = data["founder_control_contract"]
    assert founder_control["primary_channel"] == "telegram_openclaw"
    assert founder_control["slack_status"] == "OPTIONAL_DORMANT_CAPABILITY"
    assert founder_control["slack_launch_dependency"] is False
    assert founder_control["current_vps_runtime_receipt_required"] is True

    connectors = {row["id"]: row for row in data["connector_control_plane"]}
    assert "slack_telegram" not in connectors
    assert connectors["telegram_openclaw"]["owner"] == "dealix-pm"
    assert connectors["telegram_openclaw"]["role"] == "canonical_founder_command_approvals_and_receipts"
    assert connectors["telegram_openclaw"]["truth_owner"] is False
    assert connectors["telegram_openclaw"]["write_ceiling"] == "INTERNAL_ONLY"

    a2 = next(row for row in data["acceptance_levels"] if row["id"] == "A2_CHANNEL_AND_FOUNDER_CONTROL")
    assert "telegram_openclaw_e2e_receipt" in a2["evidence"]
    assert "slack_or_telegram_e2e_receipt" not in a2["evidence"]


def test_full_commercial_and_saas_claims_require_real_proof() -> None:
    data = _data()
    activation = data["activation_state"]
    assert activation["full_commercial_proof"] == "BLOCKED_UNTIL_A5_REAL_COMMERCIAL_PROOF"
    assert activation["saas_scale_claim"] == "BLOCKED_UNTIL_A6_REPEATABILITY"
