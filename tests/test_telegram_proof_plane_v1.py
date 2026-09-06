from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "data/ops/telegram_proof_plane_v1.json"
BUILDER = ROOT / "scripts/ops/build_telegram_founder_proof.py"


def _load_builder():
    spec = importlib.util.spec_from_file_location("telegram_proof_builder", BUILDER)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_contract_keeps_telegram_as_projection_only():
    data = json.loads(CONTRACT.read_text(encoding="utf-8"))
    assert data["schema"] == "dealix.telegram-proof-plane.v1"
    assert data["canonical_owner"] == "existing_dealix_company_machine"
    assert data["channel"]["role"] == "founder_proof_projection_not_truth_store"
    assert data["truth"]["telegram_message_is_not_truth_store"] is True
    assert data["truth"]["telegram_delivery_is_not_execution_proof"] is True
    assert data["truth"]["approval_click_is_not_execution_proof"] is True
    assert data["truth"]["durable_receipt_required_for_execution_claim"] is True


def test_telegram_limits_and_opaque_callback_contract():
    data = json.loads(CONTRACT.read_text(encoding="utf-8"))
    channel = data["channel"]
    assert channel["message_max_chars"] < channel["telegram_api_message_limit_chars"]
    assert channel["callback_data_max_bytes"] <= 64
    assert channel["callback_payload"] == "opaque_token_only"
    approval = data["approval_transport"]
    assert approval["callback_must_not_embed_target_sha_config_or_secret"] is True
    assert approval["server_side_pending_state_required"] is True
    assert approval["preconditions_revalidated_before_execution"] is True


def test_builder_redacts_common_secret_shapes():
    builder = _load_builder()
    sample = "AUTHORIZATION: Bearer abcdefghijklmnop OPENAI_API_KEY=sk-secretsecretsecret"
    redacted = builder.redact(sample)
    assert "sk-secret" not in redacted
    assert "abcdefghijklmnop" not in redacted
    assert "[REDACTED]" in redacted


def test_canonical_bytes_are_order_independent_for_objects():
    builder = _load_builder()
    a = {"b": 2, "a": {"z": False, "x": [1, "y"]}}
    b = {"a": {"x": [1, "y"], "z": False}, "b": 2}
    assert builder.canonical_bytes(a) == builder.canonical_bytes(b)


def test_previous_envelope_integrity_is_recomputed(tmp_path: Path):
    builder = _load_builder()
    out = tmp_path / "proof"
    out.mkdir()
    core = {
        "specversion": "1.0",
        "id": "proof_0123456789abcdef",
        "source": "dealix://test",
        "type": "com.dealix.founder.proof.v1",
        "subject": "test",
    }
    digest = builder.sha256_hex(builder.canonical_bytes(core))
    payload = {**core, "envelope_sha256": digest}
    previous = out / "proof_0123456789abcdef.json"
    previous.write_text(json.dumps(payload), encoding="utf-8")
    (out / "LATEST").write_text(previous.name + "\n", encoding="utf-8")
    assert builder.read_previous_digest(out) == digest

    payload["subject"] = "tampered"
    previous.write_text(json.dumps(payload), encoding="utf-8")
    with pytest.raises(builder.ProofError, match="integrity"):
        builder.read_previous_digest(out)


def test_contract_keeps_l5_false_by_default():
    data = json.loads(CONTRACT.read_text(encoding="utf-8"))
    approval = data["approval_transport"]
    assert approval["telegram_decision_does_not_self_grant_l5"] is True
    security = data["security"]
    assert security["network_send_in_builder"] is False
    assert security["production_mutation_in_builder"] is False
    assert security["l5_execution_in_builder"] is False


def test_one_owner_hardening_target_is_explicit_but_separately_activated():
    data = json.loads(CONTRACT.read_text(encoding="utf-8"))
    target = data["openclaw_hardening_target"]
    assert target["one_owner_dm_policy"] == "allowlist"
    assert target["explicit_numeric_allow_from"] is True
    assert target["commands_owner_allow_from_exact_founder"] is True
    assert target["tools_elevated"] is False
    assert target["inline_buttons"] == "dm"
    assert target["activation_requires_separate_runtime_change"] is True
