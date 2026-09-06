#!/usr/bin/env python3
"""Fail-closed source verifier for Dealix Telegram Proof Plane V1."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONTRACT = ROOT / "data/ops/telegram_proof_plane_v1.json"
BUILDER = ROOT / "scripts/ops/build_telegram_founder_proof.py"


class VerificationError(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationError(message)


def main() -> int:
    require(CONTRACT.is_file(), "missing Telegram proof-plane contract")
    require(BUILDER.is_file(), "missing Telegram proof builder")

    payload = json.loads(CONTRACT.read_text(encoding="utf-8"))
    require(payload.get("schema") == "dealix.telegram-proof-plane.v1", "schema drift")
    require(payload.get("canonical_owner") == "existing_dealix_company_machine", "canonical owner drift")

    channel = payload.get("channel", {})
    require(channel.get("id") == "telegram_openclaw", "channel drift")
    require(channel.get("role") == "founder_proof_projection_not_truth_store", "Telegram became truth owner")
    require(channel.get("one_owner") is True, "one-owner control missing")
    require(channel.get("groups_enabled") is False, "Telegram groups must remain disabled")
    require(channel.get("callback_payload") == "opaque_token_only", "callback data must be opaque")
    require(int(channel.get("callback_data_max_bytes", 0)) <= 64, "Telegram callback limit drift")
    require(int(channel.get("message_max_chars", 99999)) < int(channel.get("telegram_api_message_limit_chars", 0)), "message safety margin missing")

    durable = payload.get("durable_proof", {})
    require(durable.get("output_root") == "/opt/dealix/control/proof/telegram-founder", "proof root drift")
    require(durable.get("evidence_digest_algorithm") == "sha256", "digest drift")
    require(durable.get("hash_chain") is True, "hash chain missing")
    require(durable.get("tamper_evident_not_nonrepudiation") is True, "hash-chain claim too strong")
    require(durable.get("evidence_content_embedded") is False, "raw evidence must not be embedded")

    require(payload.get("proof_sections") == ["MONEY", "DECISIONS", "RISKS", "APPROVALS", "NEXT_ACTION"], "Founder brief drift")

    approval = payload.get("approval_transport", {})
    for key in (
        "action_bound",
        "server_side_pending_state_required",
        "opaque_callback_token_required",
        "exact_action_fingerprint_required",
        "expiry_required",
        "one_time_decision_required",
        "founder_identity_revalidation_required",
        "preconditions_revalidated_before_execution",
        "stale_packet_fails_closed",
        "callback_must_not_embed_target_sha_config_or_secret",
    ):
        require(approval.get(key) is True, f"approval guard missing: {key}")
    require(approval.get("approval_is_not_execution_proof") is True, "approval/proof truth weakened")
    require(approval.get("telegram_decision_does_not_self_grant_l5") is True, "Telegram self-authority forbidden")

    security = payload.get("security", {})
    for key in (
        "raw_secrets_in_telegram",
        "raw_customer_data_in_telegram",
        "raw_founder_telegram_id_in_receipt",
        "symlink_evidence_allowed",
        "group_or_world_writable_evidence_allowed",
        "network_send_in_builder",
        "production_mutation_in_builder",
        "l5_execution_in_builder",
    ):
        require(security.get(key) is False, f"security guard weakened: {key}")

    builder = BUILDER.read_text(encoding="utf-8")
    required_markers = (
        "TELEGRAM_SENT=false",
        "L5_EXECUTED=false",
        "previous_envelope_sha256",
        "envelope_sha256",
        "trace_id",
        "source_sha",
        "evidence_digest",
        "callback_data_max_bytes",
        "/opt/dealix/control/proof/telegram-founder",
    )
    for marker in required_markers:
        require(marker in builder or marker in CONTRACT.read_text(encoding="utf-8"), f"builder/contract marker missing: {marker}")

    forbidden_markers = (
        "api.telegram.org",
        "sendMessage",
        "requests.post",
        "httpx.post",
        "subprocess.run([\"git\", \"push\"",
        "railway up",
        "gh pr merge",
    )
    for marker in forbidden_markers:
        require(marker not in builder, f"builder contains forbidden side effect: {marker}")

    truth = payload.get("truth", {})
    for key in (
        "telegram_message_is_not_truth_store",
        "telegram_delivery_is_not_execution_proof",
        "approval_click_is_not_execution_proof",
        "durable_receipt_required_for_execution_claim",
        "hash_chain_is_tamper_evidence_only",
        "historical_receipt_is_not_current_proof",
    ):
        require(truth.get(key) is True, f"truth firewall missing: {key}")

    print("TELEGRAM_PROOF_PLANE_V1_PASS")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except VerificationError as exc:
        print(f"TELEGRAM_PROOF_PLANE_V1_FAIL: {exc}")
        raise SystemExit(1)
