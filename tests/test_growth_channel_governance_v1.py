from __future__ import annotations

from scripts.verify_growth_channel_governance_v1 import load_policy, validate_policy


def test_growth_channel_policy_is_fail_closed() -> None:
    validate_policy(load_policy())


def test_ai_search_policy_remains_evidence_first_and_read_only() -> None:
    search = load_policy()["search_and_ai_visibility"]
    assert search["seo_fundamentals_remain_authoritative"] is True
    assert search["original_non_commodity_content_required"] is True
    assert search["search_console_is_read_only"] is True
    assert search["special_geo_or_aeo_hack_subsystem_allowed"] is False
    assert search["scaled_low_value_ai_content_allowed"] is False
    assert search["missing_genai_report_means_zero_visibility"] is False
    assert search["rank_or_impression_is_demand_truth"] is False
    assert search["ai_overview_or_ai_mode_visibility_is_revenue"] is False


def test_direct_marketing_never_infers_consent() -> None:
    marketing = load_policy()["direct_marketing"]
    assert marketing["direct_marketing_requires_consent"] is True
    assert marketing["consent_must_be_documented_for_future_verification"] is True
    assert marketing["consent_requires_clear_specific_purpose"] is True
    assert marketing["consent_record_requires_time_and_method"] is True
    assert marketing["separate_consent_per_processing_purpose"] is True
    assert marketing["prior_interaction_auto_grants_direct_marketing_consent"] is False
    assert marketing["public_contact_auto_grants_consent"] is False
    assert marketing["relationship_auto_grants_marketing_consent"] is False
    assert marketing["sender_identity_must_be_clear"] is True
    assert marketing["opt_out_mechanism_required"] is True
    assert marketing["withdrawal_requires_stop_without_undue_delay"] is True


def test_channel_policy_grants_no_live_authority() -> None:
    payload = load_policy()
    assert payload["status"] == "POLICY_CONTRACT_NO_CHANNEL_ACTIVATION"
    assert all(value is False for value in payload["authority"].values())
    assert all(value is False for value in payload["truth_firewall"].values())
    assert payload["channel_boundaries"]["founder_linkedin"] == "MANUAL_NATIVE"
    assert payload["channel_boundaries"]["whatsapp"] == "INBOUND_OR_KNOWN_CONSENTED_ONLY"
    assert payload["channel_boundaries"]["external_send_default"] is False
    assert payload["channel_boundaries"]["public_publish_default"] is False
    assert payload["channel_boundaries"]["paid_spend_default"] is False
