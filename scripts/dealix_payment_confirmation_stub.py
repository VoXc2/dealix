#!/usr/bin/env python3
"""Wave 6 Phase 5 — manual payment confirmation stub.

State machine for one prospect's payment lifecycle. Writes to
docs/wave6/live/payment_state.json (gitignored).

Hard rules:
- Cannot mark `payment_confirmed` without `evidence_note` >= 5 chars
- Cannot mark `delivery_kickoff_ready` without payment_confirmed OR
  written_commitment_received
- NEVER calls Moyasar live API
- NEVER claims revenue from invoice_intent or payment_pending
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

LIVE_DIR = Path("docs/wave6/live")
LIVE_PATH = LIVE_DIR / "payment_state.json"

VALID_STATES = (
    "invoice_intent_created",
    "payment_pending",
    "evidence_received",
    "payment_confirmed",
    "written_commitment_received",
    "delivery_kickoff_ready",
    "refunded",
    "voided",
)

# Allowed transitions
_TRANSITIONS: dict[str, set[str]] = {
    "(none)": {"invoice_intent_created"},
    "invoice_intent_created": {"payment_pending", "voided"},
    "payment_pending": {"evidence_received", "voided"},
    "evidence_received": {"payment_confirmed", "voided"},
    "payment_confirmed": {"delivery_kickoff_ready", "refunded"},
    "written_commitment_received": {"delivery_kickoff_ready"},
    "delivery_kickoff_ready": {"refunded"},
    "refunded": set(),
    "voided": set(),
}


def _load(path: Path) -> dict[str, Any]:
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {"state": "(none)", "history": []}


def _save(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _can_transition(current: str, target: str) -> bool:
    return target in _TRANSITIONS.get(current, set())


def cmd_invoice_intent(state: dict, args) -> tuple[bool, str]:
    if state["state"] != "(none)":
        return (False, f"already_at_state:{state['state']}")
    if not args.customer or not args.amount_sar or not args.service_type:
        return (False, "customer + amount-sar + service-type required")
    state["state"] = "invoice_intent_created"
    state["customer_handle"] = args.customer
    state["amount_sar"] = float(args.amount_sar)
    state["amount_halalah"] = int(round(float(args.amount_sar) * 100))
    state["service_type"] = args.service_type
    state["history"].append({
        "at": _now(),
        "action": "invoice_intent_created",
        "amount_sar": float(args.amount_sar),
    })
    return (True, "invoice_intent_created (NOT revenue)")


def cmd_send_payment_link(state: dict, args) -> tuple[bool, str]:
    if not _can_transition(state["state"], "payment_pending"):
        return (False, f"cannot transition {state['state']}->payment_pending")
    state["state"] = "payment_pending"
    state["history"].append({
        "at": _now(),
        "action": "payment_link_sent",
        "method": "manual_bank_transfer",
    })
    return (True, "payment_pending (still NOT revenue)")


def cmd_upload_evidence(state: dict, args) -> tuple[bool, str]:
    if not _can_transition(state["state"], "evidence_received"):
        return (False, f"cannot transition {state['state']}->evidence_received")
    if not args.evidence_note or len(args.evidence_note.strip()) < 5:
        return (False, "evidence_note must be at least 5 chars")
    state["state"] = "evidence_received"
    state["evidence_note"] = args.evidence_note.strip()
    state["evidence_kind"] = args.evidence_kind or "transfer_reference"
    state["history"].append({
        "at": _now(),
        "action": "evidence_received",
        "evidence_kind": state["evidence_kind"],
    })
    return (True, "evidence_received (still NOT final until confirmed)")


def cmd_confirm(state: dict, args) -> tuple[bool, str]:
    if not _can_transition(state["state"], "payment_confirmed"):
        return (False, f"cannot transition {state['state']}->payment_confirmed")
    if not state.get("evidence_note") or len(state["evidence_note"]) < 5:
        return (False, "cannot confirm without evidence_note (>=5 chars)")
    if not args.confirmed_by:
        return (False, "confirmed-by required")
    state["state"] = "payment_confirmed"
    state["confirmed_by"] = args.confirmed_by
    state["confirmed_at"] = _now()
    state["is_revenue"] = True
    state["history"].append({
        "at": _now(),
        "action": "payment_confirmed",
        "confirmed_by": args.confirmed_by,
    })
    return (True, "payment_confirmed = REVENUE")


def cmd_written_commitment(state: dict, args) -> tuple[bool, str]:
    """Alternative path: signed contract instead of payment confirmation."""
    if state["state"] not in ("(none)", "invoice_intent_created", "payment_pending"):
        return (False, f"cannot accept commitment from state:{state['state']}")
    if not args.commitment_kind:
        return (False, "commitment-kind required")
    state["state"] = "written_commitment_received"
    state["commitment_kind"] = args.commitment_kind
    state["signed_at"] = _now()
    state["history"].append({
        "at": _now(),
        "action": "written_commitment_received",
        "commitment_kind": args.commitment_kind,
    })
    return (True, "written_commitment_received (proceed with delivery)")


def cmd_kickoff_ready(state: dict, args) -> tuple[bool, str]:
    if state["state"] not in ("payment_confirmed", "written_commitment_received"):
        return (False, "must be payment_confirmed OR written_commitment_received")
    if not _can_transition(state["state"], "delivery_kickoff_ready"):
        return (False, f"cannot transition {state['state']}->delivery_kickoff_ready")
    state["state"] = "delivery_kickoff_ready"
    state["history"].append({
        "at": _now(),
        "action": "delivery_kickoff_ready",
    })
    return (True, "delivery_kickoff_ready — Phase 6 unlocked")


def cmd_refund(state: dict, args) -> tuple[bool, str]:
    if state["state"] not in ("payment_confirmed", "delivery_kickoff_ready"):
        return (False, "can only refund after payment_confirmed")
    if not args.refund_note:
        return (False, "refund-note required")
    state["state"] = "refunded"
    state["refund_note"] = args.refund_note
    state["history"].append({
        "at": _now(),
        "action": "refunded",
        "refund_note": args.refund_note,
    })
    return (True, "refunded (terminal)")


_ACTIONS = {
    "invoice-intent": cmd_invoice_intent,
    "send-payment-link": cmd_send_payment_link,
    "upload-evidence": cmd_upload_evidence,
    "confirm": cmd_confirm,
    "written-commitment": cmd_written_commitment,
    "kickoff-ready": cmd_kickoff_ready,
    "refund": cmd_refund,
}


def main() -> int:
    p = argparse.ArgumentParser(description="Wave 6 manual payment confirmation stub")
    p.add_argument("--action", required=True, choices=list(_ACTIONS.keys()))
    p.add_argument("--customer", default=None)
    p.add_argument("--amount-sar", default=None)
    p.add_argument("--service-type", default=None)
    p.add_argument("--evidence-note", default=None)
    p.add_argument("--evidence-kind", default=None,
                   choices=[None, "bank_screenshot", "transfer_reference", "email_receipt"])
    p.add_argument("--confirmed-by", default=None)
    p.add_argument("--commitment-kind", default=None,
                   choices=[None, "signed_service_agreement", "email_commitment"])
    p.add_argument("--refund-note", default=None)
    p.add_argument("--out-path", default=str(LIVE_PATH))
    args = p.parse_args()

    out = Path(args.out_path)
    state = _load(out)
    handler = _ACTIONS[args.action]
    ok, msg = handler(state, args)
    if not ok:
        print(f"REJECTED: {msg}", file=sys.stderr)
        return 1

    _save(out, state)
    print(f"OK: {msg}")
    print(f"  state: {state['state']}")
    print(f"  is_revenue: {state.get('is_revenue', False)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
