from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "data/commercial/metricool_distribution_adapter_v1.json"


def main() -> int:
    data = json.loads(CONTRACT.read_text(encoding="utf-8"))

    assert data["schema"] == "dealix.metricool-distribution-adapter.v1"
    assert data["canonical_truth_owner"] == "DEALIX_COMPANY_MACHINE"
    assert data["default_mode"] == "DRAFT_OR_REVIEW_ONLY"

    connection = data["metricool_connection"]
    assert connection["timezone"] == "Asia/Riyadh"
    assert connection["control_plane_state"] == "CONNECTED"
    assert connection["provider_readiness"] in {"PROVIDERS_PENDING", "PROVIDERS_CONNECTED"}

    authority = data["authority"]
    assert authority["public_publish_is_material"] is True
    assert authority["public_publish_requires_action_bound_authority"] is True
    assert authority["auto_publish_default"] is False
    assert authority["paid_boost_default"] is False
    assert authority["metricool_may_self_authorize"] is False
    assert authority["metricool_may_override_channel_eligibility"] is False
    assert authority["metricool_may_override_suppression"] is False
    assert authority["metricool_may_promote_engagement_to_buyer_intent"] is False
    assert authority["metricool_may_promote_metrics_to_customer_proof"] is False

    exclusions = set(data["explicit_exclusions"])
    assert "founder_linkedin_personal_automation" in exclusions
    assert "whatsapp" in exclusions
    assert "voice" in exclusions

    blocked = set(data["blocked_operations_without_exact_material_authority"])
    assert {"auto_publish", "schedule_auto_publish", "public_post", "paid_boost"} <= blocked
    assert "connect_founder_personal_linkedin_for_automation" in blocked

    atom = data["content_atom_contract"]
    required_atom_fields = {
        "content_id",
        "source_signal_or_thesis",
        "evidence_refs",
        "claims_status",
        "language",
        "target_audience",
        "single_cta",
        "channel_variant",
        "planned_provider",
        "utm_campaign",
        "media_requirements",
        "ai_disclosure_requirement",
        "fresh_until",
    }
    assert required_atom_fields <= set(atom["required_fields"])
    assert "action_bound_publish_authority" in atom["publish_transition_requires"]

    measurement = data["measurement_contract"]
    assert measurement["metricool_metrics_are_observations_only"] is True
    assert measurement["engagement_is_not_buyer_intent"] is True
    assert measurement["click_is_not_qualified_problem"] is True
    assert measurement["lead_form_is_not_verified_revenue"] is True

    activation = data["provider_activation_gate"]
    providers = connection["provider_networks_observed"]
    if not providers:
        assert connection["provider_readiness"] == "PROVIDERS_PENDING"
        assert activation["current_verdict"] == "HOLD_PROVIDERS_PENDING"
        assert connection["provider_network_count_observed"] == 0
        assert connection["runtime_schedule_ready"] is False
        assert connection["runtime_publish_ready"] is False
        assert activation["zero_provider_network_invariant"].startswith("EMPTY_PROVIDER_NETWORKS")

    capability = data["provider_capability_contract"]
    assert "w_organization_social" in capability["linkedin_organization"]["required_capabilities"]
    assert capability["linkedin_personal"]["automation_allowed"] is False
    assert capability["tiktok"]["unaudited_client_visibility"] == "PRIVATE_ONLY"
    assert capability["youtube"]["unverified_project_visibility"] == "PRIVATE_ONLY"
    assert "account_specific_publish_permissions_verified_at_activation" in capability["meta_business"]["required_capabilities"]
    assert "user_context_write_authorization_verified" in capability["x"]["required_capabilities"]

    print("METRICOOL_DISTRIBUTION_ADAPTER_V1_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
