#!/usr/bin/env python3
"""Fail-closed verifier for Dealix founder command authority v1."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONTRACT = ROOT / "data/ops/founder_command_authority_v1.json"
ACCEPTANCE = ROOT / "scripts/ops/accept_founder_command_authority_v1.sh"
UNKNOWN = "UNKNOWN_NOT_EVIDENCE_BACKED"
VERIFIED = "VERIFIED"


class VerificationError(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationError(message)


def verify_acceptance_source() -> None:
    require(ACCEPTANCE.is_file(), "missing read-only Founder Control runtime acceptance")
    text = ACCEPTANCE.read_text(encoding="utf-8")
    for marker in (
        "BLOCKED_EXPECTED_SHA_REQUIRED",
        "BLOCKED_HEAD_MISMATCH",
        "dealix.founder-command-runtime-receipt.v1",
        "L4_READ_ONLY_RUNTIME_ACCEPTANCE",
        "/opt/dealix/control/proof/founder-command/",
        "telegram_dm_admission_contains_non_owner",
        "telegram_token_file_permissions_not_0600",
        "port_18789_loopback_only",
        'oc_args("secrets", "audit", "--check")',
        "openclaw_secretref_audit",
        "secrets_audit=",
        "secret_values_printed=false",
        "owner_raw_id_printed=false",
    ):
        require(marker in text, f"runtime acceptance missing safety marker: {marker}")

    for marker in (
        'oc_args("config", "set"',
        'oc_args("gateway", "restart"',
        'oc_args("gateway", "install"',
        'oc_args("pairing", "approve"',
        'oc_args("doctor", "--fix"',
    ):
        require(marker not in text, f"runtime acceptance contains forbidden mutation: {marker}")


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
    require(
        command.get("founder_brief_sections") == ["MONEY", "DECISIONS", "RISKS", "APPROVALS", "NEXT_ACTION"],
        "founder brief drift",
    )

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

    requirements = payload.get("activation_requirements", {})
    for key in (
        "telegram_owner_identity_required",
        "telegram_unknown_identity_deny_required",
        "telegram_gateway_loopback_required",
        "telegram_groups_disabled_by_default_required",
        "openclaw_secretref_audit_required",
        "current_vps_runtime_receipt_required",
    ):
        require(requirements.get(key) is True, f"missing Telegram/OpenClaw activation requirement: {key}")
    require(requirements.get("slack_runtime_receipt_required") is False, "Slack receipt must not gate launch")
    require(requirements.get("slack_credentials_required") is False, "Slack credentials must not gate launch")

    runtime = payload.get("runtime_evidence", {})
    runtime_status = runtime.get("status")
    require(runtime_status in {UNKNOWN, VERIFIED}, "invalid runtime evidence status")
    evidence_keys = (
        "telegram_owner_identity",
        "telegram_unknown_identity_deny",
        "telegram_gateway_loopback",
        "telegram_groups_disabled_by_default",
        "openclaw_secretref_audit",
    )
    if runtime_status == UNKNOWN:
        for key in evidence_keys:
            require(runtime.get(key) == UNKNOWN, f"unverified runtime field must remain UNKNOWN: {key}")
        require(runtime.get("receipt_ref") is None, "unknown runtime must not cite a receipt")
        require(runtime.get("source_sha") is None, "unknown runtime must not claim a source SHA")
    else:
        for key in evidence_keys:
            require(runtime.get(key) == VERIFIED, f"verified runtime missing proof state: {key}")
        require(bool(runtime.get("receipt_ref")), "verified runtime requires receipt_ref")
        require(bool(runtime.get("source_sha")), "verified runtime requires source_sha")

    truth = payload.get("truth", {})
    require(truth.get("command_message_is_not_execution_proof") is True, "command/proof truth weakened")
    require(truth.get("receipt_required_for_execution_claim") is True, "receipt requirement missing")
    require(truth.get("historical_receipt_is_not_current_runtime_proof") is True, "historical receipt truth weakened")
    require(truth.get("requirements_are_not_runtime_evidence") is True, "requirements/runtime truth weakened")
    require(truth.get("missing_current_receipt") == UNKNOWN, "unknown semantic drift")

    verify_acceptance_source()

    print("FOUNDER_COMMAND_AUTHORITY_V1_PASS")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except VerificationError as exc:
        print(f"FOUNDER_COMMAND_AUTHORITY_V1_FAIL: {exc}")
        raise SystemExit(1)
