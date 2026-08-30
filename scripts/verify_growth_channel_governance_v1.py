#!/usr/bin/env python3
"""Fail-closed verifier for Dealix search/AI-search and direct-marketing policy."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data/commercial/growth_channel_governance_v1.json"


def fail(message: str) -> None:
    raise SystemExit(f"DEALIX_GROWTH_CHANNEL_GOVERNANCE=FAIL\nFAIL: {message}")


def load_policy() -> dict:
    if not POLICY.exists():
        fail("policy contract missing")
    payload = json.loads(POLICY.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        fail("policy must be a JSON object")
    return payload


def validate_policy(payload: dict) -> None:
    if payload.get("schema") != "dealix.growth-channel-governance.v1":
        fail("schema drift")
    if payload.get("status") != "POLICY_CONTRACT_NO_CHANNEL_ACTIVATION":
        fail("policy may not claim live channel activation")

    search = payload.get("search_and_ai_visibility", {})
    for key in (
        "seo_fundamentals_remain_authoritative",
        "original_non_commodity_content_required",
        "search_console_is_read_only",
        "genai_search_console_reporting_when_available",
        "search_signal_requires_downstream_business_evidence",
    ):
        if search.get(key) is not True:
            fail(f"search policy drift: {key}")
    for key in (
        "special_geo_or_aeo_hack_subsystem_allowed",
        "scaled_low_value_ai_content_allowed",
        "missing_genai_report_means_zero_visibility",
        "rank_or_impression_is_demand_truth",
        "ai_overview_or_ai_mode_visibility_is_revenue",
    ):
        if search.get(key) is not False:
            fail(f"search truth boundary drift: {key}")

    marketing = payload.get("direct_marketing", {})
    for key in (
        "direct_marketing_requires_consent",
        "consent_must_be_documented_for_future_verification",
        "consent_requires_clear_specific_purpose",
        "consent_record_requires_time_and_method",
        "separate_consent_per_processing_purpose",
        "advertising_or_awareness_without_prior_interaction_requires_consent",
        "sender_identity_must_be_clear",
        "opt_out_mechanism_required",
        "opt_out_must_be_easy_and_free",
        "withdrawal_requires_stop_without_undue_delay",
        "suppression_overrides_campaign_or_sequence",
    ):
        if marketing.get(key) is not True:
            fail(f"direct-marketing governance drift: {key}")
    for key in (
        "prior_interaction_auto_grants_direct_marketing_consent",
        "public_contact_auto_grants_consent",
        "relationship_auto_grants_marketing_consent",
    ):
        if marketing.get(key) is not False:
            fail(f"consent inference must remain blocked: {key}")

    boundaries = payload.get("channel_boundaries", {})
    if boundaries.get("founder_linkedin") != "MANUAL_NATIVE":
        fail("founder LinkedIn boundary drift")
    if boundaries.get("whatsapp") != "INBOUND_OR_KNOWN_CONSENTED_ONLY":
        fail("WhatsApp boundary drift")
    for key in ("public_publish_default", "external_send_default", "paid_spend_default"):
        if boundaries.get(key) is not False:
            fail(f"channel default must remain false: {key}")

    truth = payload.get("truth_firewall", {})
    if not truth or not all(value is False for value in truth.values()):
        fail("growth truth firewall drift")

    expected_receipts = {
        "identity_or_relationship_ref",
        "consent_or_channel_eligibility_ref",
        "purpose_ref",
        "suppression_check_ref",
        "claim_evidence_refs",
        "approval_or_execution_authority_ref",
        "idempotency_key",
        "provider_receipt",
    }
    if set(payload.get("required_receipts_for_any_future_live_send", [])) != expected_receipts:
        fail("future live-send receipt contract drift")

    authority = payload.get("authority", {})
    if not authority or not all(value is False for value in authority.values()):
        fail("policy must grant zero live authority")


def main() -> int:
    validate_policy(load_policy())
    print("DEALIX_GROWTH_CHANNEL_GOVERNANCE=PASS")
    print("AI_SEARCH=SEO_FOUNDATIONS_EVIDENCE_FIRST")
    print("SEARCH_CONSOLE=READ_ONLY")
    print("GENAI_REPORT_ABSENCE=NOT_ZERO_VISIBILITY")
    print("DIRECT_MARKETING=DOCUMENTED_PURPOSE_SPECIFIC_CONSENT")
    print("PUBLIC_CONTACT_CONSENT_INFERENCE=BLOCKED")
    print("OPT_OUT_AND_WITHDRAWAL=REQUIRED")
    print("FOUNDER_LINKEDIN=MANUAL_NATIVE")
    print("WHATSAPP=INBOUND_OR_KNOWN_CONSENTED_ONLY")
    print("LIVE_SEND_PUBLISH_SPEND_AUTHORITY=ALL_FALSE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
