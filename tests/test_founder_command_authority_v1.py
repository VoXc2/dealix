from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "data/ops/founder_command_authority_v1.json"
VERIFIER = ROOT / "scripts/ops/verify_founder_command_authority_v1.py"
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


def test_telegram_openclaw_is_the_only_required_founder_command_channel() -> None:
    payload = _contract()
    assert payload["founder_command"]["primary_channel"] == "telegram_openclaw"
    slack = payload["optional_channels"]["slack"]
    assert slack["status"] == "OPTIONAL_DORMANT_CAPABILITY"
    assert slack["launch_dependency"] is False
    assert slack["required_for_founder_command"] is False
    assert slack["required_for_company_machine"] is False
    assert slack["required_for_customer_delivery"] is False
    assert slack["token_request_allowed_without_new_founder_decision"] is False


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
    assert requirements["openclaw_secretref_audit_required"] is True
    assert requirements["current_vps_runtime_receipt_required"] is True

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
    assert truth["command_message_is_not_execution_proof"] is True
    assert truth["receipt_required_for_execution_claim"] is True
    assert truth["historical_receipt_is_not_current_runtime_proof"] is True
    assert truth["requirements_are_not_runtime_evidence"] is True
    assert truth["missing_current_receipt"] == UNKNOWN
