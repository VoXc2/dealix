#!/usr/bin/env python3
"""Verify the OP2 L5 commercial packet stays unsent and fail-closed.

Prints: DEALIX_OP2_L5_PACKET_VERDICT=PASS|FAIL
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
PACKET_PATH = REPO_ROOT / "data" / "commercial" / "op2_l5_imini_packet_v1.json"
VERDICT_PASS = "DEALIX_OP2_L5_PACKET_VERDICT=PASS"
VERDICT_FAIL = "DEALIX_OP2_L5_PACKET_VERDICT=FAIL"


def main() -> int:
    errors: list[str] = []
    if not PACKET_PATH.exists():
        print(VERDICT_FAIL)
        print(f"  - missing {PACKET_PATH}")
        return 1
    try:
        payload = json.loads(PACKET_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(VERDICT_FAIL)
        print(f"  - invalid json: {exc}")
        return 1

    if payload.get("schema") != "dealix.op2-l5-commercial-packet.v1":
        errors.append("unexpected schema")
    if payload.get("l5_executed") != 0:
        errors.append("l5_executed must be 0")

    decision = payload.get("pre_approval_decision") or {}
    if decision.get("provider_execution_allowed") is not False:
        errors.append("pre-approval decision must not allow provider execution")
    if decision.get("approval_valid") is not False:
        errors.append("pre-approval approval must be invalid")

    action_hash = str(payload.get("action_hash") or "")
    if len(action_hash) != 16 or any(ch not in "0123456789abcdef" for ch in action_hash):
        errors.append("action_hash must be a 16-char lowercase hex digest")

    packet = payload.get("packet") or {}
    if packet.get("action_hash") != action_hash:
        errors.append("packet.action_hash must match top-level action_hash")
    if packet.get("purpose_class") != "INBOUND_REPLY":
        errors.append("purpose_class must be INBOUND_REPLY (no new outbound)")

    print(VERDICT_PASS if not errors else VERDICT_FAIL)
    for err in errors:
        print(f"  - {err}")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
