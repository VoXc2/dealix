from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "data/commercial/metricool_distribution_adapter_v1.json"


def _contract() -> dict:
    return json.loads(CONTRACT.read_text(encoding="utf-8"))


def test_metricool_never_becomes_canonical_truth_owner() -> None:
    data = _contract()
    assert data["canonical_truth_owner"] == "DEALIX_COMPANY_MACHINE"
    assert data["authority"]["metricool_may_self_authorize"] is False
    assert data["authority"]["metricool_may_override_channel_eligibility"] is False
    assert data["authority"]["metricool_may_override_suppression"] is False


def test_public_publish_and_paid_boost_fail_closed_by_default() -> None:
    data = _contract()
    authority = data["authority"]
    blocked = set(data["blocked_operations_without_exact_material_authority"])
    assert authority["auto_publish_default"] is False
    assert authority["paid_boost_default"] is False
    assert authority["public_publish_requires_action_bound_authority"] is True
    assert {"auto_publish", "schedule_auto_publish", "public_post", "paid_boost"} <= blocked


def test_founder_personal_linkedin_is_not_an_automation_target() -> None:
    data = _contract()
    assert "founder_linkedin_personal_automation" in data["explicit_exclusions"]
    assert "connect_founder_personal_linkedin_for_automation" in set(
        data["blocked_operations_without_exact_material_authority"]
    )


def test_metricool_metrics_do_not_promote_business_truth() -> None:
    data = _contract()
    measurement = data["measurement_contract"]
    assert measurement["metricool_metrics_are_observations_only"] is True
    assert measurement["engagement_is_not_buyer_intent"] is True
    assert measurement["click_is_not_qualified_problem"] is True
    assert measurement["lead_form_is_not_verified_revenue"] is True


def test_empty_provider_inventory_stays_hold() -> None:
    data = _contract()
    connection = data["metricool_connection"]
    assert connection["control_plane_state"] == "CONNECTED"
    if not connection["provider_networks_observed"]:
        assert connection["provider_readiness"] == "PROVIDERS_PENDING"
        assert data["provider_activation_gate"]["current_verdict"] == "HOLD_PROVIDERS_PENDING"


def test_content_atom_requires_evidence_and_exact_publish_authority() -> None:
    data = _contract()
    atom = data["content_atom_contract"]
    required = set(atom["required_fields"])
    assert {"content_id", "evidence_refs", "claims_status", "single_cta", "fresh_until"} <= required
    assert "action_bound_publish_authority" in atom["publish_transition_requires"]
