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


def test_live_metricool_observation_does_not_invent_provider_connectivity() -> None:
    data = _contract()
    connection = data["metricool_connection"]
    assert data["version"] == "2026-09-15.2"
    assert connection["provider_networks_observed"] == []
    assert connection["scheduled_posts_observed"] == 0
    assert connection["provider_readiness"] == "PROVIDERS_PENDING"
    assert data["provider_activation_gate"]["current_verdict"] == "HOLD_PROVIDERS_PENDING"



def test_zero_provider_inventory_is_explicitly_not_runtime_ready() -> None:
    data = _contract()
    connection = data["metricool_connection"]
    assert connection["provider_network_count_observed"] == 0
    assert connection["runtime_schedule_ready"] is False
    assert connection["runtime_publish_ready"] is False
    assert connection["runtime_readiness_reason"] == "zero_provider_networks_observed_no_live_channel_identity_or_permission_proof"
    assert data["provider_activation_gate"]["zero_provider_network_invariant"].startswith("EMPTY_PROVIDER_NETWORKS")


def test_provider_capability_contract_is_provider_specific_and_fail_closed() -> None:
    data = _contract()
    providers = data["provider_capability_contract"]
    linkedin = providers["linkedin_organization"]
    assert "w_organization_social" in linkedin["required_capabilities"]
    assert {"ADMINISTRATOR", "DIRECT_SPONSORED_CONTENT_POSTER", "CONTENT_ADMIN"} <= set(linkedin["eligible_page_roles"])
    assert providers["linkedin_personal"]["automation_allowed"] is False
    assert providers["tiktok"]["unaudited_client_visibility"] == "PRIVATE_ONLY"
    assert "approved_video.publish_scope" in providers["tiktok"]["required_capabilities"]
    assert providers["youtube"]["unverified_project_visibility"] == "PRIVATE_ONLY"
    assert "oauth_user_authorization" in providers["youtube"]["required_capabilities"]
    assert "account_specific_publish_permissions_verified_at_activation" in providers["meta_business"]["required_capabilities"]
    assert "user_context_write_authorization_verified" in providers["x"]["required_capabilities"]
