#!/usr/bin/env python3
"""Generate first-5 personalized warm messages and truthful logging payloads.

This script prepares local files only. It never sends any external message.
"""
from __future__ import annotations

import argparse
import csv
import json
from dataclasses import dataclass
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]

BASE_ANGLE_TEMPLATE = """Hi {name},

I’m building Dealix, a governed AI operations company starting in Saudi Arabia.

This is not an AI automation resale motion.

The angle is a governed AI operations diagnostic for clients already experimenting with AI but lacking source clarity, approval boundaries, evidence trails, proof of value, and agent identity controls.

Would it be useful to compare this against one client segment you already see asking about AI governance or AI-driven revenue operations?

Best,
Sami"""

FOLLOW_UP_TEMPLATES = {
    "reply_interested": (
        "Thanks for the interest. Happy to share a short diagnostic scope with the evidence "
        "levels and approval gates so you can review before any next step."
    ),
    "send_more_info": (
        "Absolutely. I will send a concise one-pager covering scope, governance controls, "
        "expected diagnostic outputs, and example proof artifacts."
    ),
    "asks_for_case_study": (
        "Great question. I can share a sanitized case-style summary showing baseline signals, "
        "governed actions, and measured outcomes without exposing private client data."
    ),
    "asks_for_scope": (
        "Scope is a governed diagnostic focused on source clarity, approval boundaries, "
        "evidence trail quality, and revenue-ops readiness. No external automation is executed."
    ),
    "no_response_follow_up": (
        "Quick follow-up in case this got buried. If AI governance + revenue operations is "
        "relevant for your segment, I can send a short draft scope for review."
    ),
}


@dataclass(frozen=True)
class ContactMessage:
    contact_id: str
    audience_type: str
    suggested_channel: str
    subject: str
    message_body: str
    why_this_contact: str
    expected_next_action: str
    message_variant: str


def _pick_channel(audience_type: str) -> str:
    normalized = audience_type.strip().lower()
    if normalized in {"investor", "advisor"}:
        return "email"
    if normalized in {"operator", "founder"}:
        return "linkedin_dm"
    return "email"


def _build_subject(company: str) -> str:
    return f"Governed AI Ops diagnostic for {company}"


def _why_this_contact(role: str, sector: str, notes: str) -> str:
    role_text = role.strip() or "operator"
    sector_text = sector.strip() or "business services"
    note_text = notes.strip() or "warm relationship and governance interest"
    return f"Role fit ({role_text}) in {sector_text}; context: {note_text}"


def _to_message(row: dict[str, str]) -> ContactMessage:
    name = (row.get("name") or "").strip() or "there"
    company = (row.get("company") or "").strip() or "your company"
    role = (row.get("role") or "").strip()
    sector = (row.get("sector") or "").strip()
    notes = (row.get("notes") or "").strip()
    audience_type = (row.get("audience_type") or "operator").strip().lower()
    contact_id = (row.get("contact_id") or "").strip() or "unknown_contact"
    subject = _build_subject(company)
    body = BASE_ANGLE_TEMPLATE.format(name=name)
    return ContactMessage(
        contact_id=contact_id,
        audience_type=audience_type,
        suggested_channel=_pick_channel(audience_type),
        subject=subject,
        message_body=body,
        why_this_contact=_why_this_contact(role=role, sector=sector, notes=notes),
        expected_next_action="founder_manual_send_then_wait_for_reply_or_classify_no_response",
        message_variant="market_proof_activation_v1",
    )


def _load_contacts(csv_path: Path) -> list[dict[str, str]]:
    with csv_path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        return [row for row in reader if (row.get("contact_id") or "").strip()]


def _prepared_not_sent_payload(messages: list[ContactMessage]) -> list[dict[str, str | bool]]:
    return [
        {
            "contact_id": msg.contact_id,
            "audience_type": msg.audience_type,
            "channel": msg.suggested_channel,
            "outcome": "prepared_not_sent",
            "evidence_level": "L2",
            "message_variant": msg.message_variant,
            "sent_at": "",
            "founder_confirmed": False,
            "next_action": "wait_for_reply_or_classify_no_response",
        }
        for msg in messages
    ]


def _post_send_template_payload(messages: list[ContactMessage]) -> list[dict[str, str | bool]]:
    return [
        {
            "contact_id": msg.contact_id,
            "audience_type": msg.audience_type,
            "channel": "email",
            "outcome": "sent",
            "evidence_level": "L4",
            "message_variant": msg.message_variant,
            "sent_at": "YYYY-MM-DD",
            "founder_confirmed": True,
            "next_action": "wait_for_reply_or_classify_no_response",
        }
        for msg in messages
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate first 5 personalized warm-list messages")
    parser.add_argument("--csv", default="data/warm_list.csv", help="Input warm list CSV")
    parser.add_argument(
        "--out-dir",
        default="data/outreach",
        help="Output directory for first-5 files",
    )
    parser.add_argument("--limit", type=int, default=5, help="How many contacts to output")
    args = parser.parse_args()

    csv_path = (REPO_ROOT / args.csv).resolve()
    if not csv_path.exists():
        print(f"ERROR: missing csv -> {csv_path}")
        print("Run: python3 scripts/seed_warm_contacts.py --force")
        return 1

    contacts = _load_contacts(csv_path)
    first_messages = [_to_message(row) for row in contacts[: args.limit]]
    if len(first_messages) < args.limit:
        print(f"ERROR: only {len(first_messages)} contacts available; need at least {args.limit}")
        return 1

    out_dir = (REPO_ROOT / args.out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    first5_records = [
        {
            "contact_id": msg.contact_id,
            "audience_type": msg.audience_type,
            "suggested_channel": msg.suggested_channel,
            "subject": msg.subject,
            "message_body": msg.message_body,
            "why_this_contact": msg.why_this_contact,
            "expected_next_action": msg.expected_next_action,
            "message_variant": msg.message_variant,
        }
        for msg in first_messages
    ]

    prepared_not_sent = _prepared_not_sent_payload(first_messages)
    post_send_template = _post_send_template_payload(first_messages)

    first5_path = out_dir / "warm_list_first5_personalized.json"
    prepared_path = out_dir / "warm_list_first5_prepared_not_sent.json"
    post_send_path = out_dir / "warm_list_first5_post_send_template.json"
    follow_up_path = out_dir / "warm_list_follow_up_templates.json"

    first5_path.write_text(json.dumps(first5_records, ensure_ascii=False, indent=2), encoding="utf-8")
    prepared_path.write_text(json.dumps(prepared_not_sent, ensure_ascii=False, indent=2), encoding="utf-8")
    post_send_path.write_text(json.dumps(post_send_template, ensure_ascii=False, indent=2), encoding="utf-8")
    follow_up_path.write_text(json.dumps(FOLLOW_UP_TEMPLATES, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"OK: wrote first5 -> {first5_path}")
    print(f"OK: wrote not-sent ledger -> {prepared_path}")
    print(f"OK: wrote post-send template -> {post_send_path}")
    print(f"OK: wrote follow-up templates -> {follow_up_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
