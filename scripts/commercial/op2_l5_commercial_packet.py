#!/usr/bin/env python3
"""OP2 L5 commercial packet preparation — exact, action-bound, UNSENT.

Prepares ONE governed external-action packet for the strongest live economic
relationship (iMini / Jannie, founder-income lane) using the canonical
``deallix.commercial.external_execution_gate`` primitives. It computes both:

  * ACTION_HASH   = sha256(action_type|target|environment|payload)[0:16]
  * packet_integrity_sha256 (tamper/version checksum)

and then evaluates the packet against a *deny-by-default* authority snapshot to
prove it remains BLOCKED until the founder grants exact-action L5 approval.

This tool NEVER sends. It has no provider client. It only emits a preparation
artifact for founder decision.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

OUT_PATH = REPO_ROOT / "data" / "commercial" / "op2_l5_imini_packet_v1.json"
RELATIONSHIP_REF = "rel-imini-001"
DESTINATION = "founder_gmail_thread:imini_jannie"
ENVIRONMENT = "founder_income_lane"
ACTION_ID = "op2-imini-counter-2026-09-12"
IDEMPOTENCY_KEY = "op2-imini-counter-2026-09-12-a1"
PROVIDER = "gmail"


def build_packet() -> dict[str, Any]:
    from dealix.commercial.external_execution_gate import (
        ExecutionDecision,
        ResolvedAuthoritySnapshot,
        RuntimeAuthority,
        build_external_action_packet,
        evaluate_resolved_external_action,
    )

    # NOTE: the exact body/subject are founder-authored elsewhere; this packet
    # binds to the placeholder artifact reference and records content_sha256 as
    # the canonical empty-thread marker so no unauthored prose is embedded.
    content_sha256 = "0" * 64
    expires_at = (datetime.now(UTC) + timedelta(hours=72)).isoformat()

    packet = build_external_action_packet(
        action_id=ACTION_ID,
        action_class="EMAIL_SEND",
        purpose_class="INBOUND_REPLY",
        destination=DESTINATION,
        channel="gmail",
        environment=ENVIRONMENT,
        artifact_ref="reports/founder/APPROVAL_CARD_IMINI.md#pending_exact_body",
        content_sha256=content_sha256,
        identity_or_relationship_ref=RELATIONSHIP_REF,
        consent_or_channel_eligibility_ref="two_way_email_2026-08-24",
        suppression_check_ref="op2-money-now-reconciliation-v1",
        suppression_clear=True,
        claim_evidence_refs=[RELATIONSHIP_REF, "op2-money-now-reconciliation-v1"],
        sender_identity_ref="founder_gmail_identity",
        opt_out_mechanism_ref="thread_reply_stop",
        risk_class="MEDIUM",
        exact_scope="one reply inside the existing iMini/Jannie two-way email thread; no new outbound",
        expires_at=expires_at,
        provider=PROVIDER,
        idempotency_key=IDEMPOTENCY_KEY,
    )

    # Deny-by-default authority snapshot proves the packet is fail-closed.
    deny_snapshot = ResolvedAuthoritySnapshot(
        source_ref="op2:pre_approval_deny",
        resolved_at=datetime.now(UTC).isoformat(),
        approval={
            "approval_id": "op2-pre-approval",
            "action_hash": packet.action_hash,
            "exact_scope": packet.exact_scope,
            "authority_class": "L5_FOUNDER_EXACT_ACTION",
            "approval_state": "PENDING",
            "approval_state_ref": "president_approval_packet:imini_824a9d8b3caae92d",
            "state_checked_at": datetime.now(UTC).isoformat(),
            "expires_at": expires_at,
            "evidence_refs": [RELATIONSHIP_REF],
        },
        runtime=RuntimeAuthority(external_send=False),
        identity_or_relationship_ref=RELATIONSHIP_REF,
        consent_or_channel_eligibility_ref="two_way_email_2026-08-24",
        suppression_check_ref="op2-money-now-reconciliation-v1",
        suppression_clear=True,
        claim_evidence_refs=[RELATIONSHIP_REF],
        sender_identity_ref="founder_gmail_identity",
        opt_out_mechanism_ref="thread_reply_stop",
    )

    decision = evaluate_resolved_external_action(packet, authority=deny_snapshot)

    return {
        "schema": "dealix.op2-l5-commercial-packet.v1",
        "generated_at": datetime.now(UTC).isoformat(),
        "lane": "OP2",
        "relationship_ref": RELATIONSHIP_REF,
        "note": "UNSENT preparation artifact. No provider call is made by this tool.",
        "packet": packet.model_dump(),
        "action_hash": packet.action_hash,
        "packet_integrity_sha256": packet.packet_integrity_sha256,
        "pre_approval_decision": decision.model_dump(),
        "l5_executed": 0,
    }


def render(result: dict[str, Any]) -> str:
    lines = [
        "DEALIX_OP2_L5_PACKET=OK",
        f"TARGET={result['relationship_ref']}",
        f"ACTION_HASH={result['action_hash']}",
        f"PACKET_INTEGRITY_SHA256={result['packet_integrity_sha256']}",
        f"PRE_APPROVAL_ALLOWED={result['pre_approval_decision']['provider_execution_allowed']}",
        f"PRE_APPROVAL_REASONS={'; '.join(result['pre_approval_decision']['reasons'])}",
    ]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Prepare the OP2 iMini L5 packet (unsent)")
    parser.add_argument("--write", action="store_true", help=f"write {OUT_PATH}")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    result = build_packet()
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(render(result))
    if args.write:
        OUT_PATH.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"WROTE {OUT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
