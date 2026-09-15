#!/usr/bin/env python3
"""Fail-closed verifier for Dealix governed omnichannel runtime v1."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / "data/commercial/governed_channel_runtime_v1.json"


class VerificationError(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationError(message)


def load_json(path: Path) -> dict:
    require(path.exists(), f"missing required file: {path.relative_to(ROOT)}")
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def require_repo_file(relative_path: str, label: str) -> Path:
    require(bool(relative_path), f"missing {label} path")
    path = ROOT / relative_path
    require(path.is_file(), f"missing {label}: {relative_path}")
    return path


def main() -> int:
    contract = load_json(CONTRACT_PATH)

    require(contract.get("schema") == "dealix.governed-channel-runtime.v1", "wrong schema")

    authority = contract.get("authority_model", {})
    registry_rel = authority.get("canonical_channel_registry")
    require(
        registry_rel == "data/commercial/channel_readiness_registry.json",
        "wrong canonical channel registry",
    )
    registry = load_json(ROOT / registry_rel)
    require(
        registry.get("schema") == "dealix.channel-readiness-registry.v2",
        "channel registry schema drift",
    )

    forbidden_parallel = {
        "parallel_company_os",
        "parallel_company_brain",
        "parallel_crm",
        "parallel_opportunity_graph",
        "parallel_approval_center",
        "parallel_proof_ledger",
        "parallel_scheduler",
        "parallel_agent_fleet",
        "parallel_model_router",
    }
    for key in forbidden_parallel:
        require(authority.get(key) is False, f"{key} must remain false")

    effects = contract.get("global_external_effects_default", {})
    required_effects = {
        "email_send",
        "whatsapp_send",
        "linkedin_member_dm",
        "linkedin_connection",
        "social_publish",
        "paid_spend",
        "payment_or_refund",
        "tender_submission",
        "legal_commitment",
        "merge_main",
        "production_mutation",
        "dns_db_secret_mutation",
    }
    require(required_effects <= set(effects), "missing material external-effect controls")
    for key in required_effects:
        require(effects[key] is False, f"material effect must default deny: {key}")

    truth = set(contract.get("truth_firewall", []))
    require(
        {
            "research_is_not_relationship",
            "public_contact_is_not_consent",
            "engagement_is_not_buyer_intent",
            "draft_is_not_sent",
            "invoice_is_not_payment",
            "synthetic_is_not_customer_proof",
        }
        <= truth,
        "truth firewall incomplete",
    )

    state_rules = contract.get("state_rules", {})
    for key in (
        "research_cannot_promote_relationship",
        "public_data_cannot_promote_consent",
        "raw_engagement_cannot_promote_opportunity",
        "relationship_truth_must_come_from_canonical_relationship_owner",
        "payment_truth_requires_payment_evidence",
        "proof_truth_requires_customer_or_source_evidence",
    ):
        require(state_rules.get(key) is True, f"state rule must be true: {key}")

    gates = set(contract.get("dispatch_gates", []))
    require(
        {
            "canonical_real_interaction_or_purpose_specific_consent",
            "suppression_and_opt_out_check",
            "sender_or_channel_health",
            "official_channel_capability",
            "approved_identity_and_credentials_outside_repo",
            "content_brand_claims_and_policy_qa",
            "action_bound_approval",
            "durable_idempotency_key",
            "provider_effect_receipt",
            "delivery_or_failure_receipt",
        }
        <= gates,
        "dispatch gates incomplete",
    )

    channels = contract.get("channels", {})
    for required_channel in (
        "email",
        "founder_linkedin",
        "dealix_linkedin_page",
        "whatsapp",
        "instagram_facebook_threads_x",
        "youtube_tiktok",
        "website_chat",
        "slack_telegram_founder",
    ):
        require(required_channel in channels, f"missing channel policy: {required_channel}")

    email_blocked = set(channels["email"].get("blocked", []))
    require(
        "unbounded_cold_bulk_email" in email_blocked,
        "email bulk cold send must be blocked",
    )
    require("send_after_opt_out" in email_blocked, "email send-after-opt-out must be blocked")
    require(
        "live_send_without_action_bound_authority" in email_blocked,
        "email live send must be authority-bound",
    )

    linkedin_blocked = set(channels["founder_linkedin"].get("blocked", []))
    require(
        {"scraping", "bot_connections", "bot_dms", "mass_member_messaging"}
        <= linkedin_blocked,
        "LinkedIn member automation boundary weakened",
    )

    whatsapp_blocked = set(channels["whatsapp"].get("blocked", []))
    require(
        {"cold_whatsapp", "bulk_unsolicited_whatsapp", "purchased_lists", "suppressed_contact"}
        <= whatsapp_blocked,
        "WhatsApp consent boundary weakened",
    )

    roster = contract.get("service_model", {})
    expected_agents = {
        "dealix-pm",
        "dealix-sales",
        "dealix-delivery",
        "dealix-engineer",
        "dealix-content",
    }
    require(roster.get("permanent_agent_count") == 5, "permanent agent count must remain five")
    require(set(roster.get("canonical_agents", [])) == expected_agents, "canonical agent roster drift")

    oss = contract.get("open_source_intake", {})
    require(
        oss.get("do_not_install_duplicate_agent_framework") is True,
        "duplicate agent framework guard missing",
    )
    require(
        oss.get("do_not_install_duplicate_scheduler_or_workflow_engine") is True,
        "duplicate scheduler guard missing",
    )
    require(
        oss.get("prefer_existing_opentelemetry_sentry_langfuse_n8n_stack") is True,
        "existing stack preference missing",
    )

    # Cross-check current canonical registry so a new contract cannot silently
    # weaken already-established platform-specific restrictions.
    registry_channels = registry.get("channels", {})
    reg_linkedin = set(registry_channels.get("founder_linkedin", {}).get("automation_blocked", []))
    require(
        {"scraping", "bot_connections", "bot_dms"} <= reg_linkedin,
        "canonical LinkedIn registry weakened",
    )
    reg_whatsapp = set(registry_channels.get("whatsapp", {}).get("automation_blocked", []))
    require(
        {"cold_whatsapp", "bulk_unsolicited_whatsapp", "purchased_lists"} <= reg_whatsapp,
        "canonical WhatsApp registry weakened",
    )
    reg_email = set(registry_channels.get("email", {}).get("automation_blocked", []))
    require(
        {"unbounded_cold_bulk_email", "send_after_opt_out"} <= reg_email,
        "canonical email registry weakened",
    )

    provider_contract = registry.get("official_provider_contract", {})
    require(
        provider_contract.get("authority") == "READINESS_ONLY_NO_SEND_PUBLISH_OR_SPEND",
        "social provider contract must remain readiness-only",
    )
    provider_truth = provider_contract.get("runtime_truth", {})
    require(
        provider_truth.get("provider_connected_is_not_publish_authority") is True,
        "provider connectivity must not become publish authority",
    )

    org_linkedin = registry_channels.get("dealix_linkedin_page", {})
    require(
        "w_organization_social" in set(org_linkedin.get("required_capabilities", [])),
        "LinkedIn organization publish permission contract missing",
    )
    facebook = registry_channels.get("facebook", {})
    require(
        {
            "dealix_page_identity", "page_access_token_outside_repo",
            "page_role_or_task_CREATE_CONTENT", "pages_show_list",
            "pages_read_engagement", "pages_manage_posts",
        } <= set(facebook.get("required_capabilities", [])),
        "Facebook Page publish capability contract incomplete",
    )
    require(
        str(facebook.get("public_publish_gate", "")).startswith("EXACT_ACTION_BOUND"),
        "Facebook Page public publish must remain action-bound",
    )
    tiktok = registry_channels.get("tiktok", {})
    require(
        {"approved_video.publish_scope", "target_user_authorization"}
        <= set(tiktok.get("required_capabilities", [])),
        "TikTok direct-post capability contract incomplete",
    )
    require(
        "audit_pass_before_public_direct_post" in set(tiktok.get("activation_evidence_required", [])),
        "TikTok public-post audit gate missing",
    )
    youtube = registry_channels.get("youtube", {})
    require(
        {"oauth_scope_youtube.upload", "videos.insert"}
        <= set(youtube.get("required_capabilities", [])),
        "YouTube upload capability contract incomplete",
    )
    require(
        youtube.get("ai_content_contract", {}).get("provider_field") == "status.containsSyntheticMedia",
        "YouTube synthetic-media disclosure contract missing",
    )
    x_channel = registry_channels.get("x", {})
    require(
        {"oauth_user_context", "tweet.write", "sufficient_api_credits_or_approved_cost_budget"}
        <= set(x_channel.get("required_capabilities", [])),
        "X user-write or cost authority contract incomplete",
    )
    require(
        x_channel.get("cost_contract", {}).get("spend_default") is False,
        "X paid API use must default deny",
    )
    gbp = registry_channels.get("google_business_profile", {})
    require(
        {
            "verified_business_profile", "valid_google_cloud_project",
            "business_profile_api_access", "oauth2_authorized_account",
            "authorized_location_access", "local_posts_api_for_automated_posts",
        } <= set(gbp.get("required_capabilities", [])),
        "Google Business Profile API/OAuth/location capability contract incomplete",
    )
    require(
        str(gbp.get("public_publish_gate", "")).startswith("EXACT_ACTION_BOUND"),
        "Google Business Profile public post must remain action-bound",
    )

    # Slack is allowed only as a bounded transport into the existing Company
    # Autopilot. The contract must point to source-controlled implementation and
    # keep all material authorities disabled until an end-to-end runtime receipt
    # is verified.
    slack = contract.get("slack_founder_bridge", {})
    require(
        slack.get("status") == "SOURCE_CONTROLLED_PENDING_RUNTIME_E2E_RECEIPT",
        "Slack bridge must remain pending runtime end-to-end receipt",
    )
    require(slack.get("transport") == "SLACK_SOCKET_MODE", "Slack bridge transport drift")
    require(slack.get("framework") == "slack-bolt==1.30.0", "Slack Bolt pin drift")

    slack_paths = {
        "adapter": "scripts/ops/dealix_slack_founder_bridge.py",
        "dedicated_requirements": "scripts/ops/requirements-slack-founder.txt",
        "installer": "scripts/ops/install_slack_founder_bridge_v2.sh",
        "receipt_verifier": "scripts/ops/verify_slack_founder_bridge_receipt.py",
        "policy_tests": "tests/test_slack_founder_bridge_policy_v2.py",
    }
    for key, expected in slack_paths.items():
        require(slack.get(key) == expected, f"Slack {key} path drift")
        require_repo_file(expected, f"Slack {key}")

    require(
        slack.get("canonical_runner") == "/opt/dealix/control/bin/dealix_company_autopilot.sh",
        "Slack bridge must invoke canonical Company Autopilot only",
    )
    for key in (
        "arbitrary_shell",
        "arbitrary_agent_prompt_execution",
        "customer_outreach_authority",
        "public_publish_authority",
        "payment_authority",
        "merge_authority",
        "production_mutation_authority",
    ):
        require(slack.get(key) is False, f"Slack bridge authority must remain false: {key}")
    for key in (
        "founder_and_channel_allowlist_required",
        "duplicate_event_idempotency_required",
        "activation_requires_runtime_credentials_outside_git",
        "activation_requires_end_to_end_receipt",
    ):
        require(slack.get(key) is True, f"Slack bridge guard must remain true: {key}")
    require(
        slack.get("default_install_mode") == "INSTALL_ONLY_NOT_ACTIVATED",
        "Slack installer must default to install-only",
    )

    req_path = require_repo_file(slack_paths["dedicated_requirements"], "Slack requirements")
    req_lines = [
        line.strip()
        for line in req_path.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]
    require(req_lines == ["slack-bolt==1.30.0"], "Slack dependency surface must stay isolated and pinned")

    acceptance = contract.get("acceptance", {})
    require(
        acceptance.get("live_send_activation_requires_separate_action_bound_change") is True,
        "live-send activation must require a separate action-bound change",
    )
    require(
        acceptance.get("slack_policy_tests") == slack_paths["policy_tests"],
        "Slack policy test acceptance drift",
    )
    require(
        acceptance.get("slack_receipt_verifier") == slack_paths["receipt_verifier"],
        "Slack receipt verifier acceptance drift",
    )
    require(
        acceptance.get("slack_installer") == slack_paths["installer"],
        "Slack installer acceptance drift",
    )
    require(
        acceptance.get("slack_runtime_activation_requires_end_to_end_receipt") is True,
        "Slack runtime activation must require end-to-end receipt",
    )

    print("GOVERNED_CHANNEL_RUNTIME_V1_PASS")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except VerificationError as exc:
        print(f"GOVERNED_CHANNEL_RUNTIME_V1_FAIL: {exc}")
        raise SystemExit(1)
