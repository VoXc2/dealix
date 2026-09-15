from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "data/commercial/governed_channel_runtime_v1.json"
REGISTRY = ROOT / "data/commercial/channel_readiness_registry.json"
VERIFIER = ROOT / "scripts/verify_governed_channel_runtime_v1.py"


def _contract() -> dict:
    return json.loads(CONTRACT.read_text(encoding="utf-8"))


def _registry() -> dict:
    return json.loads(REGISTRY.read_text(encoding="utf-8"))


def test_governed_channel_runtime_verifier_passes() -> None:
    result = subprocess.run(
        [sys.executable, str(VERIFIER)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "GOVERNED_CHANNEL_RUNTIME_V1_PASS" in result.stdout


def test_material_external_effects_default_deny() -> None:
    effects = _contract()["global_external_effects_default"]
    assert effects
    assert all(value is False for value in effects.values())


def test_five_canonical_agents_only() -> None:
    service_model = _contract()["service_model"]
    assert service_model["permanent_agent_count"] == 5
    assert set(service_model["canonical_agents"]) == {
        "dealix-pm",
        "dealix-sales",
        "dealix-delivery",
        "dealix-engineer",
        "dealix-content",
    }


def test_social_and_messaging_boundaries_are_fail_closed() -> None:
    channels = _contract()["channels"]
    assert "unbounded_cold_bulk_email" in channels["email"]["blocked"]
    assert "send_after_opt_out" in channels["email"]["blocked"]
    assert "scraping" in channels["founder_linkedin"]["blocked"]
    assert "bot_dms" in channels["founder_linkedin"]["blocked"]
    assert "cold_whatsapp" in channels["whatsapp"]["blocked"]
    assert "bulk_unsolicited_whatsapp" in channels["whatsapp"]["blocked"]
    assert "public_publish_without_official_capability_and_authority" in channels["instagram_facebook_threads_x"]["blocked"]


def test_research_cannot_manufacture_commercial_truth() -> None:
    rules = _contract()["state_rules"]
    assert rules["research_cannot_promote_relationship"] is True
    assert rules["public_data_cannot_promote_consent"] is True
    assert rules["raw_engagement_cannot_promote_opportunity"] is True
    assert rules["payment_truth_requires_payment_evidence"] is True


def test_channel_eligibility_is_deterministic_and_fail_closed() -> None:
    registry = _registry()
    gate = registry["channel_eligibility_contract"]
    required = set(gate["required_inputs"])
    assert {
        "tenant",
        "account",
        "recipient_or_audience",
        "channel",
        "purpose",
        "relationship_basis",
        "consent_evidence_when_required",
        "suppression_state",
        "sender_identity",
        "provider_capability",
        "policy_state",
        "fresh_until",
    } <= required
    assert gate["score_or_public_contact_may_override"] is False
    assert gate["deny_precedence"][0] == "SUPPRESSED_OR_OPTED_OUT"
    assert "ELIGIBLE_PENDING_ACTION_AUTHORITY" in gate["decision"]


def test_expanded_channel_registry_preserves_safe_roles() -> None:
    channels = _registry()["channels"]
    assert {
        "website",
        "founder_linkedin",
        "dealix_linkedin_page",
        "instagram",
        "facebook",
        "threads",
        "youtube",
        "tiktok",
        "x",
        "snapchat",
        "pinterest",
        "google_business_profile",
        "email",
        "whatsapp",
        "sms",
        "voice",
        "rcs",
        "calendar",
        "telegram_founder",
    } <= set(channels)
    assert "cold_whatsapp" in channels["whatsapp"]["automation_blocked"]
    assert "cold_bulk_sms" in channels["sms"]["automation_blocked"]
    assert "cold_autodialing" in channels["voice"]["automation_blocked"]
    assert "cold_promotional_blast" in channels["rcs"]["automation_blocked"]
    assert "bot_dms" in channels["founder_linkedin"]["automation_blocked"]
    assert "fake_reviews" in channels["google_business_profile"]["automation_blocked"]


def test_renderer_or_scheduler_cannot_become_truth_owner() -> None:
    policy = _registry()["distribution_renderer_policy"]
    assert policy["canonical_truth_owner"] == "DEALIX_COMPANY_MACHINE"
    assert set(policy["metricool_or_equivalent_may_not_be"]) == {
        "crm",
        "consent_owner",
        "opportunity_truth",
        "proof_owner",
        "economic_truth",
    }
    assert policy["public_publish_still_action_bound"] is True


def test_official_social_provider_readiness_is_explicit_and_fail_closed() -> None:
    registry = _registry()
    contract = registry["official_provider_contract"]
    assert contract["authority"] == "READINESS_ONLY_NO_SEND_PUBLISH_OR_SPEND"
    assert contract["runtime_truth"]["provider_connected_is_not_publish_authority"] is True

    channels = registry["channels"]
    linkedin = channels["dealix_linkedin_page"]
    assert "w_organization_social" in linkedin["required_capabilities"]
    assert linkedin["public_publish_gate"].startswith("EXACT_ACTION_BOUND")

    facebook = channels["facebook"]
    assert {
        "dealix_page_identity", "page_access_token_outside_repo",
        "page_role_or_task_CREATE_CONTENT", "pages_show_list",
        "pages_read_engagement", "pages_manage_posts",
    } <= set(facebook["required_capabilities"])
    assert facebook["public_publish_gate"].startswith("EXACT_ACTION_BOUND")

    tiktok = channels["tiktok"]
    assert "approved_video.publish_scope" in tiktok["required_capabilities"]
    assert "audit_pass_before_public_direct_post" in tiktok["activation_evidence_required"]
    assert tiktok["ai_content_contract"]["provider_field"] == "post_info.is_aigc"

    youtube = channels["youtube"]
    assert "oauth_scope_youtube.upload" in youtube["required_capabilities"]
    assert youtube["ai_content_contract"]["provider_field"] == "status.containsSyntheticMedia"

    x = channels["x"]
    assert "tweet.write" in x["required_capabilities"]
    assert x["cost_contract"]["spend_default"] is False
    assert x["cost_contract"]["credit_purchase_requires_separate_authority"] is True

    gbp = channels["google_business_profile"]
    assert {
        "verified_business_profile", "valid_google_cloud_project",
        "business_profile_api_access", "oauth2_authorized_account",
        "authorized_location_access", "local_posts_api_for_automated_posts",
    } <= set(gbp["required_capabilities"])
    assert gbp["public_publish_gate"].startswith("EXACT_ACTION_BOUND")
