from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "data/ops/founder_command_authority_v1.json"
VERIFIER = ROOT / "scripts/ops/verify_founder_command_authority_v1.py"
ACCEPTANCE = ROOT / "scripts/ops/accept_founder_command_authority_v1.sh"
UNKNOWN = "UNKNOWN_NOT_EVIDENCE_BACKED"


def _contract() -> dict:
    return json.loads(CONTRACT.read_text(encoding="utf-8"))


def test_founder_command_authority_verifier_passes() -> None:
    result = subprocess.run(
        [sys.executable, str(VERIFIER)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "FOUNDER_COMMAND_AUTHORITY_V1_PASS" in result.stdout


def test_telegram_openclaw_is_the_only_canonical_primary_founder_channel() -> None:
    payload = _contract()
    command = payload["founder_command"]
    assert command["primary_channel"] == "telegram_openclaw"
    assert command["transport"] == "telegram_dm_owner_allowlist"
    assert "explicit_numeric_dm_allowlist" in command["required_posture"]
    assert "dm_allowlist_exact_owner_only" in command["required_posture"]
    assert "dm_pairing_only" not in command["required_posture"]

    slack = payload["optional_channels"]["slack"]
    assert slack["status"] == "OPTIONAL_DORMANT_CAPABILITY"
    assert slack["launch_dependency"] is False
    assert slack["required_for_founder_command"] is False
    assert slack["required_for_company_machine"] is False
    assert slack["required_for_customer_delivery"] is False
    assert slack["token_request_allowed_without_new_founder_decision"] is False

    failover = payload["optional_channels"]["github_issue_vps_failover"]
    assert failover["status"] == "INTERNAL_FAILOVER_ADAPTER"
    assert failover["primary_founder_channel"] is False
    assert failover["launch_dependency"] is False
    assert failover["truth_owner"] is False
    assert failover["new_authority_system"] is False
    assert failover["same_dispatcher_and_durable_state_required"] is True
    assert failover["private_repo_required"] is True
    assert failover["founder_identity_required"] is True
    assert failover["allowlist_only"] is True
    assert failover["arbitrary_shell"] is False
    assert failover["l5_allowed"] is False
    assert failover["external_effect_authority"] is False
    assert failover["runtime_status"] == UNKNOWN


def test_founder_command_does_not_expand_material_authority() -> None:
    payload = _contract()
    assert payload["external_effect_defaults"]
    assert all(value is False for value in payload["external_effect_defaults"].values())
    assert payload["architecture_guards"]
    assert all(value is False for value in payload["architecture_guards"].values())


def test_activation_requirements_are_not_runtime_proof() -> None:
    payload = _contract()
    requirements = payload["activation_requirements"]
    assert requirements["telegram_owner_identity_required"] is True
    assert requirements["telegram_unknown_identity_deny_required"] is True
    assert requirements["telegram_gateway_loopback_required"] is True
    assert requirements["telegram_groups_disabled_by_default_required"] is True
    assert requirements["telegram_explicit_owner_allowlist_required"] is True
    assert requirements["openclaw_secretref_audit_required"] is True
    assert requirements["current_vps_runtime_receipt_required"] is True
    assert requirements["slack_runtime_receipt_required"] is False
    assert requirements["slack_credentials_required"] is False
    assert requirements["github_issue_failover_runtime_receipt_required"] is False
    assert requirements["github_issue_failover_must_share_dispatcher_state"] is True

    runtime = payload["runtime_evidence"]
    assert runtime["status"] == UNKNOWN
    assert runtime["receipt_ref"] is None
    assert runtime["source_sha"] is None
    for key in (
        "telegram_owner_identity",
        "telegram_unknown_identity_deny",
        "telegram_gateway_loopback",
        "telegram_groups_disabled_by_default",
        "openclaw_secretref_audit",
    ):
        assert runtime[key] == UNKNOWN


def test_command_messages_require_current_receipts_before_execution_claims() -> None:
    truth = _contract()["truth"]
    assert truth["primary_channel_is_telegram_openclaw"] is True
    assert truth["one_owner_prefers_explicit_numeric_allowlist"] is True
    assert truth["pairing_is_not_required_for_one_owner_runtime"] is True
    assert truth["failover_adapter_is_not_primary_founder_channel"] is True
    assert truth["failover_adapter_is_not_separate_authority"] is True
    assert truth["command_message_is_not_execution_proof"] is True
    assert truth["receipt_required_for_execution_claim"] is True
    assert truth["historical_receipt_is_not_current_runtime_proof"] is True
    assert truth["requirements_are_not_runtime_evidence"] is True
    assert truth["missing_current_receipt"] == UNKNOWN


def test_runtime_acceptance_is_exact_head_read_only_and_secret_safe() -> None:
    text = ACCEPTANCE.read_text(encoding="utf-8")
    assert "BLOCKED_EXPECTED_SHA_REQUIRED" in text
    assert "BLOCKED_HEAD_MISMATCH" in text
    assert "dealix.founder-command-runtime-receipt.v1" in text
    assert "L4_READ_ONLY_RUNTIME_ACCEPTANCE" in text
    assert "/opt/dealix/control/proof/founder-command/" in text
    assert "commands\", \"ownerAllowFrom" in text
    assert "telegram_dm_policy_not_owner_allowlist" in text
    assert "telegram_dm_allowlist_not_exact_founder" in text
    assert "telegram_token_file_permissions_not_0600" in text
    assert "port_18789_loopback_only" in text
    assert 'oc_args("secrets", "audit", "--check")' in text
    assert "openclaw_secretref_audit" in text
    assert "secrets_audit=" in text
    assert "secret_values_printed=false" in text
    assert "owner_raw_id_printed=false" in text
    assert "safe.directory=" in text
    assert "safe.directory=*" not in text
    assert "--global" not in text

    forbidden_runtime_mutations = (
        'oc_args("config", "set"',
        'oc_args("gateway", "restart"',
        'oc_args("gateway", "install"',
        'oc_args("pairing", "approve"',
        'oc_args("doctor", "--fix"',
    )
    for marker in forbidden_runtime_mutations:
        assert marker not in text


def test_runtime_acceptance_compiles_before_any_runtime_access() -> None:
    result = subprocess.run(
        ["bash", str(ACCEPTANCE)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 2, result.stdout + result.stderr
    assert "DEALIX_FOUNDER_COMMAND_ACCEPTANCE=BLOCKED_EXPECTED_SHA_REQUIRED" in result.stdout
