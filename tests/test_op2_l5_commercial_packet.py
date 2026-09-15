"""Contracts for exact-body, unsent OP2 iMini packet preparation."""
from __future__ import annotations

import importlib.util
import json
from datetime import UTC, datetime
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


def _load_module():
    path = ROOT / "scripts" / "commercial" / "op2_l5_commercial_packet.py"
    spec = importlib.util.spec_from_file_location("op2_l5_packet", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


packet_builder = _load_module()
NOW = datetime(2026, 9, 15, 12, 0, tzinfo=UTC)


def _build(body: str = "Synthetic draft body A") -> dict:
    return packet_builder.build_packet(
        body=body,
        subject="Synthetic iMini reply",
        message_id="msg-synthetic-001",
        thread_id="thread-synthetic-001",
        evidence_refs=["evidence://synthetic/two-way-thread", "evidence://synthetic/offer"],
        now=NOW,
    )


def test_exact_body_changes_hash_action_and_idempotency() -> None:
    first = _build("Synthetic draft body A")
    second = _build("Synthetic draft body B")
    assert first["content_sha256"] != second["content_sha256"]
    assert first["action_hash"] != second["action_hash"]
    assert first["packet"]["action_id"] != second["packet"]["action_id"]
    assert first["packet"]["idempotency_key"] != second["packet"]["idempotency_key"]


def test_packet_binds_message_thread_and_evidence_without_raw_body() -> None:
    raw = "DO_NOT_PERSIST_SYNTHETIC_BODY_9d1d"
    result = _build(raw)
    rendered = json.dumps(result, ensure_ascii=False)
    assert raw not in rendered
    assert result["gmail_message_id"] == "msg-synthetic-001"
    assert result["gmail_thread_id"] == "thread-synthetic-001"
    refs = set(result["packet"]["claim_evidence_refs"])
    assert "gmail_message:msg-synthetic-001" in refs
    assert "gmail_thread:thread-synthetic-001" in refs
    assert "evidence://synthetic/offer" in refs
    assert result["body_persisted"] is False
    assert result["provider_call_executed"] is False


def test_packet_is_fail_closed_before_exact_action_authority() -> None:
    result = _build()
    decision = result["pre_approval_decision"]
    assert decision["provider_execution_allowed"] is False
    assert decision["approval_valid"] is False
    assert result["l5_executed"] == 0
    assert result["content_sha256"] != "0" * 64


@pytest.mark.parametrize(
    "overrides",
    [
        {"body": ""},
        {"message_id": ""},
        {"thread_id": ""},
        {"evidence_refs": []},
    ],
)
def test_missing_exact_runtime_inputs_fail_closed(overrides: dict) -> None:
    args = {
        "body": "Synthetic draft body",
        "subject": "Synthetic iMini reply",
        "message_id": "msg-synthetic-001",
        "thread_id": "thread-synthetic-001",
        "evidence_refs": ["evidence://synthetic/offer"],
        "now": NOW,
    }
    args.update(overrides)
    with pytest.raises(ValueError):
        packet_builder.build_packet(**args)


def test_canonical_hash_and_integrity_recompute() -> None:
    from dealix.commercial.external_execution_gate import (
        ExternalActionPacket,
        recompute_action_hash,
        recompute_packet_integrity,
    )

    result = _build()
    packet = ExternalActionPacket(**result["packet"])
    assert recompute_action_hash(packet) == result["action_hash"]
    assert recompute_packet_integrity(packet) == result["packet_integrity_sha256"]
