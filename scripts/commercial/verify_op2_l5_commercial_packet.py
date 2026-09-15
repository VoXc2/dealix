#!/usr/bin/env python3
"""Verify a runtime OP2 iMini packet is exact-body-bound, unsent and fail-closed."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

DEFAULT_PACKET = Path("/opt/dealix/control/receipts/commercial/op2_l5_imini_packet_latest.json")
PASS = "DEALIX_OP2_L5_PACKET_VERDICT=PASS"
FAIL = "DEALIX_OP2_L5_PACKET_VERDICT=FAIL"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--packet", default=str(DEFAULT_PACKET))
    args = parser.parse_args()
    packet_path = Path(args.packet).expanduser().resolve()
    errors: list[str] = []
    try:
        payload = json.loads(packet_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(FAIL)
        print(f"  - unreadable runtime packet: {exc}")
        return 1

    if payload.get("schema") != "dealix.op2-l5-commercial-packet.v2":
        errors.append("unexpected schema")
    if payload.get("l5_executed") != 0:
        errors.append("l5_executed must be 0")
    if payload.get("body_persisted") is not False:
        errors.append("body_persisted must be false")
    if payload.get("provider_call_executed") is not False:
        errors.append("provider_call_executed must be false")
    content_hash = str(payload.get("content_sha256") or "")
    if len(content_hash) != 64 or content_hash == "0" * 64:
        errors.append("content_sha256 must be an exact non-placeholder SHA-256")
    if not payload.get("gmail_message_id") or not payload.get("gmail_thread_id"):
        errors.append("Gmail message/thread identity is required")

    decision = payload.get("pre_approval_decision") or {}
    if decision.get("provider_execution_allowed") is not False:
        errors.append("pre-approval decision must not allow provider execution")
    if decision.get("approval_valid") is not False:
        errors.append("pre-approval approval must be invalid")

    packet = payload.get("packet") or {}
    action_hash = str(payload.get("action_hash") or "")
    if packet.get("action_hash") != action_hash:
        errors.append("packet.action_hash must match top-level action_hash")
    if packet.get("purpose_class") != "INBOUND_REPLY":
        errors.append("purpose_class must remain INBOUND_REPLY")
    if packet.get("content_sha256") != content_hash:
        errors.append("packet content hash must match top-level content hash")
    if not packet.get("idempotency_key") or packet.get("idempotency_key") == "op2-imini-counter-2026-09-12-a1":
        errors.append("idempotency must be derived from current exact scope")

    print(PASS if not errors else FAIL)
    for error in errors:
        print(f"  - {error}")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
