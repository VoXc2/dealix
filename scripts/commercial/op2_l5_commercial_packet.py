#!/usr/bin/env python3
"""Prepare an exact-body, action-bound iMini Gmail reply packet without sending.

The exact draft body is accepted only at runtime from stdin or a local file.
Raw body text is never included in stdout or the persisted packet. The packet
binds the exact destination, subject/body hash, Gmail message/thread IDs, and
caller evidence refs to fresh deterministic action/idempotency identity.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

CONTROL_OUTPUT = Path("/opt/dealix/control/receipts/commercial/op2_l5_imini_packet_latest.json")
RELATIONSHIP_REF = "rel-imini-001"
DEFAULT_DESTINATION = "influencers-project@imini.com"
ENVIRONMENT = "founder_income_lane"
PROVIDER = "gmail"
MAX_BODY_BYTES = 200_000


def _required(value: str, *, field: str) -> str:
    cleaned = str(value or "").strip()
    if not cleaned:
        raise ValueError(f"{field} is required")
    return cleaned


def _evidence_refs(values: list[str]) -> list[str]:
    cleaned = [_required(value, field="evidence_ref") for value in values]
    if not cleaned:
        raise ValueError("at least one evidence_ref is required")
    return sorted(set(cleaned))


def build_packet(
    *,
    body: str,
    subject: str,
    message_id: str,
    thread_id: str,
    evidence_refs: list[str],
    destination: str = DEFAULT_DESTINATION,
    ttl_hours: int = 72,
    now: datetime | None = None,
) -> dict[str, Any]:
    from dealix.commercial.external_execution_gate import (
        ResolvedAuthoritySnapshot,
        RuntimeAuthority,
        build_external_action_packet,
        canonical_content_sha256,
        evaluate_resolved_external_action,
    )

    destination = _required(destination, field="destination")
    subject = _required(subject, field="subject")
    message_id = _required(message_id, field="message_id")
    thread_id = _required(thread_id, field="thread_id")
    evidence_refs = _evidence_refs(evidence_refs)
    if not body or not body.strip():
        raise ValueError("exact message body is required")
    if len(body.encode("utf-8")) > MAX_BODY_BYTES:
        raise ValueError("message body exceeds bounded runtime input")
    if ttl_hours <= 0 or ttl_hours > 72:
        raise ValueError("ttl_hours must be between 1 and 72")

    content_hash = canonical_content_sha256(
        destination=destination,
        subject=subject,
        body=body,
    )
    if content_hash == "0" * 64:
        raise ValueError("zero placeholder content hash is forbidden")

    binding = json.dumps(
        {
            "destination": destination,
            "content_sha256": content_hash,
            "message_id": message_id,
            "thread_id": thread_id,
            "evidence_refs": evidence_refs,
            "relationship_ref": RELATIONSHIP_REF,
        },
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    binding_sha = hashlib.sha256(binding.encode("utf-8")).hexdigest()
    action_id = f"op2-imini-{binding_sha[:20]}"
    idempotency_key = f"gmail-reply-{binding_sha[:32]}"

    current = (now or datetime.now(UTC)).astimezone(UTC)
    expires_at = (current + timedelta(hours=ttl_hours)).isoformat()
    message_ref = f"gmail_message:{message_id}"
    thread_ref = f"gmail_thread:{thread_id}"
    claim_refs = sorted(set([RELATIONSHIP_REF, message_ref, thread_ref, *evidence_refs]))
    eligibility_ref = f"{thread_ref}:two_way_relationship"
    suppression_ref = "op2-money-now-reconciliation-v1"
    sender_ref = "founder_gmail_identity"
    opt_out_ref = f"{thread_ref}:reply_stop"

    packet = build_external_action_packet(
        action_id=action_id,
        action_class="EMAIL_SEND",
        purpose_class="INBOUND_REPLY",
        destination=destination,
        channel="gmail",
        environment=ENVIRONMENT,
        artifact_ref=f"gmail:draft:{message_id}:thread:{thread_id}",
        content_sha256=content_hash,
        identity_or_relationship_ref=RELATIONSHIP_REF,
        consent_or_channel_eligibility_ref=eligibility_ref,
        suppression_check_ref=suppression_ref,
        suppression_clear=True,
        claim_evidence_refs=claim_refs,
        sender_identity_ref=sender_ref,
        opt_out_mechanism_ref=opt_out_ref,
        risk_class="MEDIUM",
        exact_scope=(
            f"one reply to {destination} inside Gmail thread {thread_id}, "
            f"bound to draft/message {message_id}; no new outbound target"
        ),
        expires_at=expires_at,
        provider=PROVIDER,
        idempotency_key=idempotency_key,
    )

    deny_snapshot = ResolvedAuthoritySnapshot(
        source_ref=f"op2:pre_approval_deny:{binding_sha[:16]}",
        resolved_at=current.isoformat(),
        approval={
            "approval_id": f"pending-{binding_sha[:20]}",
            "action_hash": packet.action_hash,
            "exact_scope": packet.exact_scope,
            "authority_class": "L5_FOUNDER_EXACT_ACTION",
            "approval_state": "PENDING",
            "approval_state_ref": f"op2:pending:{action_id}",
            "state_checked_at": current.isoformat(),
            "expires_at": expires_at,
            "evidence_refs": claim_refs,
        },
        runtime=RuntimeAuthority(external_send=False, connector_write=False),
        identity_or_relationship_ref=RELATIONSHIP_REF,
        consent_or_channel_eligibility_ref=eligibility_ref,
        suppression_check_ref=suppression_ref,
        suppression_clear=True,
        claim_evidence_refs=claim_refs,
        sender_identity_ref=sender_ref,
        opt_out_mechanism_ref=opt_out_ref,
    )
    decision = evaluate_resolved_external_action(packet, authority=deny_snapshot)

    return {
        "schema": "dealix.op2-l5-commercial-packet.v2",
        "generated_at": current.isoformat(),
        "lane": "OP2",
        "relationship_ref": RELATIONSHIP_REF,
        "gmail_message_id": message_id,
        "gmail_thread_id": thread_id,
        "content_sha256": content_hash,
        "binding_sha256": binding_sha,
        "body_persisted": False,
        "provider_call_executed": False,
        "note": "UNSENT/PENDING metadata only; exact body is not persisted by this tool.",
        "packet": packet.model_dump(),
        "action_hash": packet.action_hash,
        "packet_integrity_sha256": packet.packet_integrity_sha256,
        "pre_approval_decision": decision.model_dump(),
        "l5_executed": 0,
    }


def render(result: dict[str, Any]) -> str:
    return "\n".join(
        [
            "DEALIX_OP2_L5_PACKET=OK",
            f"TARGET={result['relationship_ref']}",
            f"GMAIL_MESSAGE_ID={result['gmail_message_id']}",
            f"GMAIL_THREAD_ID={result['gmail_thread_id']}",
            f"CONTENT_SHA256={result['content_sha256']}",
            f"ACTION_HASH={result['action_hash']}",
            f"PACKET_INTEGRITY_SHA256={result['packet_integrity_sha256']}",
            f"PRE_APPROVAL_ALLOWED={result['pre_approval_decision']['provider_execution_allowed']}",
            "RAW_BODY_PERSISTED=false",
            "PROVIDER_CALL_EXECUTED=false",
        ]
    )


def _read_runtime_body(args: argparse.Namespace) -> str:
    if args.body_stdin:
        return sys.stdin.read()
    body_path = Path(args.body_file).expanduser().resolve()
    if body_path.is_relative_to(REPO_ROOT.resolve()):
        raise ValueError("body-file must be outside the Git repository")
    return body_path.read_text(encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Prepare an exact-body iMini Gmail L5 packet (UNSENT)")
    body = parser.add_mutually_exclusive_group(required=True)
    body.add_argument("--body-stdin", action="store_true", help="read exact body from stdin")
    body.add_argument("--body-file", help="read exact body from a local non-repo file")
    parser.add_argument("--subject", required=True)
    parser.add_argument("--message-id", required=True)
    parser.add_argument("--thread-id", required=True)
    parser.add_argument("--evidence-ref", action="append", default=[], help="repeatable exact evidence reference")
    parser.add_argument("--destination", default=DEFAULT_DESTINATION)
    parser.add_argument("--ttl-hours", type=int, default=72)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--write", action="store_true", help="write sanitized metadata to control receipts")
    parser.add_argument("--output", default=str(CONTROL_OUTPUT))
    args = parser.parse_args()

    try:
        result = build_packet(
            body=_read_runtime_body(args),
            subject=args.subject,
            message_id=args.message_id,
            thread_id=args.thread_id,
            evidence_refs=args.evidence_ref,
            destination=args.destination,
            ttl_hours=args.ttl_hours,
        )
    except (OSError, ValueError) as exc:
        parser.error(str(exc))

    print(json.dumps(result, indent=2, ensure_ascii=False) if args.json else render(result))
    if args.write:
        output = Path(args.output).expanduser().resolve()
        if output.is_relative_to(REPO_ROOT.resolve()):
            parser.error("sanitized packet output must be outside the Git repository")
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"WROTE_SANITIZED_METADATA={output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
