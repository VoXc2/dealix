#!/usr/bin/env python3
"""Wave 6 Phase 6 — delivery session kickoff.

Reads the payment_state.json and starts a delivery session ONLY if
state == payment_confirmed OR written_commitment_received. Otherwise
returns BLOCKED_WAITING_PAYMENT.
"""
from __future__ import annotations

import argparse
import json
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

LIVE_DIR = Path("docs/wave6/live")

VALID_STATES = (
    "waiting_inputs",
    "diagnostic_in_progress",
    "drafts_ready",
    "approval_needed",
    "delivery_ready",
    "proof_pending",
    "delivered",
)

VALID_SERVICES = (
    "7_day_revenue_proof_sprint",
    "data_to_revenue_pack",
    "managed_revenue_ops",
    "executive_command_center",
    "diagnostic_only",
)


def _can_kickoff(payment_state: dict) -> tuple[bool, str]:
    s = payment_state.get("state", "(none)")
    if s in ("payment_confirmed", "delivery_kickoff_ready"):
        return (True, "payment_confirmed")
    if s == "written_commitment_received":
        return (True, "written_commitment_received")
    return (False, f"BLOCKED_WAITING_PAYMENT (current={s})")


def build_session(*, company: str, service: str, payment_state: dict) -> dict[str, Any]:
    sid = f"sess_{uuid.uuid4().hex[:10]}"
    return {
        "session_id": sid,
        "company": company,
        "service_type": service,
        "state": "waiting_inputs",
        "started_at": datetime.now(timezone.utc).isoformat(),
        "payment_basis": payment_state.get("state"),
        "amount_sar": payment_state.get("amount_sar"),
        "is_revenue_basis": payment_state.get("is_revenue", False),
        "deliverables": [],
        "approvals_needed": [],
        "proof_event_ids": [],
        "next_step": {
            "action": "collect_inputs_for_diagnostic",
            "owner": "csm_or_founder",
        },
        "safety_summary": "no_live_send_no_live_charge_approval_first",
    }


def render_markdown(session: dict, payment_state: dict) -> str:
    lines = []
    lines.append(f"# Delivery Session — {session['company']}")
    lines.append("")
    lines.append(f"**Session ID:** `{session['session_id']}`")
    lines.append(f"**Service:** {session['service_type']}")
    lines.append(f"**State:** `{session['state']}`")
    lines.append(f"**Payment basis:** `{session['payment_basis']}`")
    lines.append(f"**Started at:** {session['started_at']}")
    lines.append("")
    lines.append("## Lifecycle states")
    for s in VALID_STATES:
        marker = "→" if s == session["state"] else " "
        lines.append(f"- {marker} `{s}`")
    lines.append("")
    lines.append("## Next step")
    lines.append(f"- Action: **{session['next_step']['action']}**")
    lines.append(f"- Owner: {session['next_step']['owner']}")
    lines.append("")
    lines.append(f"## Hard rules (Article 4)")
    lines.append(f"- {session['safety_summary']}")
    return "\n".join(lines)


def main() -> int:
    p = argparse.ArgumentParser(description="Wave 6 delivery kickoff")
    p.add_argument("--company", required=True)
    p.add_argument("--service", required=True)
    p.add_argument("--payment-state-file", default=str(LIVE_DIR / "payment_state.json"))
    p.add_argument("--out-md", default=None)
    p.add_argument("--out-json", default=None)
    args = p.parse_args()

    if args.service not in VALID_SERVICES:
        print(f"REFUSING: invalid service: {args.service}", file=sys.stderr)
        return 2

    payment_path = Path(args.payment_state_file)
    if not payment_path.exists():
        print(f"BLOCKED_WAITING_PAYMENT: no payment_state.json at {payment_path}", file=sys.stderr)
        return 1
    payment_state = json.loads(payment_path.read_text(encoding="utf-8"))

    ok, reason = _can_kickoff(payment_state)
    if not ok:
        print(f"BLOCKED_WAITING_PAYMENT: {reason}", file=sys.stderr)
        return 1

    session = build_session(
        company=args.company, service=args.service, payment_state=payment_state,
    )

    out_md = Path(args.out_md) if args.out_md else LIVE_DIR / "delivery_session.md"
    out_json = Path(args.out_json) if args.out_json else LIVE_DIR / "delivery_session.json"
    out_md.parent.mkdir(parents=True, exist_ok=True)
    out_md.write_text(render_markdown(session, payment_state), encoding="utf-8")
    out_json.write_text(json.dumps(session, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"OK: kickoff allowed (basis={reason})")
    print(f"  session_id: {session['session_id']}")
    print(f"  state: {session['state']}")
    print(f"  next_step: {session['next_step']['action']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
