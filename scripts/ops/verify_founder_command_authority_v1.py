#!/usr/bin/env python3
"""Fail-closed verifier for Dealix founder command authority v1."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONTRACT = ROOT / "data/ops/founder_command_authority_v1.json"


class VerificationError(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationError(message)


def main() -> int:
    require(CONTRACT.is_file(), "missing founder command authority contract")
    payload = json.loads(CONTRACT.read_text(encoding="utf-8"))

    require(payload.get("schema") == "dealix.founder-command-authority.v1", "schema drift")
    require(payload.get("canonical_owner") == "existing_dealix_company_machine", "canonical owner drift")

    command = payload.get("founder_command", {})
    require(command.get("primary_channel") == "telegram_openclaw", "Telegram/OpenClaw must remain primary")
    require(command.get("gateway") == "openclaw", "gateway drift")
    require(command.get("transport") == "telegram_dm_pairing", "Telegram transport drift")
    require(command.get("runtime_role") == "founder_command_gateway_not_truth_owner", "runtime ownership drift")
    posture = set(command.get("required_posture", []))
    require(
        {
            "exact_founder_owner_identity",
            "dm_pairing_only",
            "groups_disabled_by_default",
            "gateway_loopback_only",
            "unknown_identity_denied",
            "secretrefs_for_secret_bearing_fields",
            "durable_evidence_receipts",
        } <= posture,
        "Telegram/OpenClaw posture incomplete",
    )
    require(command.get("founder_brief_sections") == ["MONEY", "DECISIONS", "RISKS", "APPROVALS", "NEXT_ACTION"], "founder brief drift")

    slack = payload.get("optional_channels", {}).get("slack", {})
    require(slack.get("status") == "OPTIONAL_DORMANT_CAPABILITY", "Slack must remain optional/dormant")
    for key in (
        "launch_dependency",
        "required_for_founder_command",
        "required_for_company_machine",
        "required_for_customer_delivery",
        "activation_requested",
        "token_request_allowed_without_new_founder_decision",
    ):
        require(slack.get(key) is False, f"Slack authority drift: {key}")

    guards = payload.get("architecture_guards", {})
    for key, value in guards.items():
        require(value is False, f"architecture guard weakened: {key}")

    effects = payload.get("external_effect_defaults", {})
    required_effects = {
        "customer_send",
        "public_publish",
        "paid_spend",
        "payment_or_refund",
        "legal_or_contract_commitment",
        "main_merge",
        "production_mutation",
        "dns_db_secret_mutation",
    }
    require(required_effects <= set(effects), "external-effect controls incomplete")
    for key in required_effects:
        require(effects[key] is False, f"external effect must default deny: {key}")

    acceptance = payload.get("activation_acceptance", {})
    for key in (
        "telegram_owner_configured",
        "telegram_unknown_identity_denied",
        "telegram_gateway_loopback_only",
        "telegram_groups_disabled_by_default",
        "openclaw_secretref_audit_required",
        "current_vps_runtime_receipt_required",
    ):
        require(acceptance.get(key) is True, f"missing Telegram/OpenClaw acceptance: {key}")
    require(acceptance.get("slack_runtime_receipt_required") is False, "Slack receipt must not gate launch")
    require(acceptance.get("slack_credentials_required") is False, "Slack credentials must not gate launch")

    truth = payload.get("truth", {})
    require(truth.get("command_message_is_not_execution_proof") is True, "command/proof truth weakened")
    require(truth.get("receipt_required_for_execution_claim") is True, "receipt requirement missing")
    require(truth.get("historical_receipt_is_not_current_runtime_proof") is True, "historical receipt truth weakened")
    require(truth.get("missing_current_receipt") == "UNKNOWN_NOT_EVIDENCE_BACKED", "unknown semantic drift")

    print("FOUNDER_COMMAND_AUTHORITY_V1_PASS")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except VerificationError as exc:
        print(f"FOUNDER_COMMAND_AUTHORITY_V1_FAIL: {exc}")
        raise SystemExit(1)
