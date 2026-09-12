"""Contracts for the OP2 iMini L5 commercial packet (unsent preparation)."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKET = ROOT / "data" / "commercial" / "op2_l5_imini_packet_v1.json"


def _load_module():
    path = ROOT / "scripts" / "commercial" / "op2_l5_commercial_packet.py"
    spec = importlib.util.spec_from_file_location("op2_l5_packet", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


packet_builder = _load_module()


def _payload() -> dict:
    return json.loads(PACKET.read_text(encoding="utf-8"))


def test_packet_is_fail_closed_before_approval() -> None:
    payload = _payload()
    decision = payload["pre_approval_decision"]
    assert decision["provider_execution_allowed"] is False
    assert decision["approval_valid"] is False
    assert payload["l5_executed"] == 0


def test_packet_hash_matches_canonical_recomputation() -> None:
    from dealix.commercial.external_execution_gate import (
        ExternalActionPacket,
        recompute_action_hash,
        recompute_packet_integrity,
    )

    payload = _payload()
    packet = ExternalActionPacket(**payload["packet"])
    assert recompute_action_hash(packet) == payload["action_hash"] == packet.action_hash
    assert recompute_packet_integrity(packet) == packet.packet_integrity_sha256


def test_packet_targets_only_the_existing_thread() -> None:
    payload = _payload()
    assert payload["relationship_ref"] == "rel-imini-001"
    assert payload["packet"]["purpose_class"] == "INBOUND_REPLY"
    assert payload["packet"]["action_class"] == "EMAIL_SEND"
    assert payload["packet"]["provider"] == "gmail"


def test_builder_is_deterministic_in_target_and_class() -> None:
    rebuilt = packet_builder.build_packet()
    stored = _payload()
    assert rebuilt["packet"]["destination"] == stored["packet"]["destination"]
    assert rebuilt["packet"]["action_class"] == stored["packet"]["action_class"]
    assert rebuilt["packet"]["purpose_class"] == stored["packet"]["purpose_class"]
