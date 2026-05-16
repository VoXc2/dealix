#!/usr/bin/env python3
"""Dealix First-5 Market Events OS.

Purpose:
- Move from internal readiness to external market evidence.
- Keep actions limited to real market events:
  sent -> reply -> meeting -> scope/pilot intro -> invoice -> paid.
- Produce the 7 KPI counters requested by leadership.

This script NEVER sends externally. It only prepares drafts and logs events.
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import sys
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_TRACKER = REPO_ROOT / "docs" / "ops" / "pipeline_tracker.csv"
DEFAULT_QUEUE_OUT = REPO_ROOT / "docs" / "ops" / "first5_warm_queue.csv"
DEFAULT_DRAFTS_OUT = REPO_ROOT / "docs" / "ops" / "first5_personalized_messages.md"
DEFAULT_EVENTS = REPO_ROOT / "docs" / "ops" / "market_events_log.csv"

SLICE_BIG4_ASSURANCE = "big4_assurance"
SLICE_REGULATED_PROCESSOR = "regulated_processor"
SLICE_VC_PLATFORM = "vc_platform"
SLICE_OTHER = "other"


@dataclass(frozen=True)
class Contact:
    lead_id: str
    name: str
    company: str
    role: str
    segment: str
    channel: str
    sent_at: str
    notes: str
    slice_name: str


EVENT_TO_LEVEL = {
    "sent": "L4_exposure",
    "replied_interested": "L4_signal",
    "replied_send_more": "L4_signal",
    "replied_case_study_requested": "L4_signal",
    "replied_english_requested": "L4_signal",
    "replied_pricing_requested": "L4_signal",
    "replied_declined": "L4_signal",
    "no_response_logged": "L4_signal",
    "meeting_booked": "L4_signal",
    "used_in_meeting": "L5",
    "scope_requested": "L6",
    "pilot_intro_requested": "L6",
    "invoice_sent": "L7_candidate",
    "invoice_paid": "L7_revenue_confirmed",
}


def _now_iso() -> str:
    return dt.datetime.now(dt.UTC).isoformat(timespec="seconds")


def _normalize(value: str) -> str:
    return (value or "").strip().lower()


def classify_slice(segment: str, role: str, company: str, notes: str) -> str:
    haystack = " ".join(
        [
            _normalize(segment),
            _normalize(role),
            _normalize(company),
            _normalize(notes),
        ]
    )
    if any(k in haystack for k in ("big4", "big 4", "assurance", "audit", "ey", "kpmg", "pwc", "deloitte")):
        return SLICE_BIG4_ASSURANCE
    if any(
        k in haystack
        for k in (
            "fintech",
            "bank",
            "processor",
            "payments",
            "payment",
            "bnpl",
            "regulat",
            "insurance",
            "sama",
        )
    ):
        return SLICE_REGULATED_PROCESSOR
    if any(k in haystack for k in ("vc", "venture", "portfolio", "platform", "accelerator", "studio")):
        return SLICE_VC_PLATFORM
    return SLICE_OTHER


def load_contacts(tracker_path: Path) -> list[Contact]:
    if not tracker_path.exists():
        raise SystemExit(f"tracker not found: {tracker_path}")

    with tracker_path.open(encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        rows = [dict(row) for row in reader]

    contacts: list[Contact] = []
    for row in rows:
        slice_name = classify_slice(
            segment=row.get("segment", ""),
            role=row.get("role", ""),
            company=row.get("company", ""),
            notes=row.get("notes", ""),
        )
        contacts.append(
            Contact(
                lead_id=(row.get("id") or "").strip(),
                name=(row.get("lead_name") or "").strip(),
                company=(row.get("company") or "").strip(),
                role=(row.get("role") or "").strip(),
                segment=(row.get("segment") or "").strip(),
                channel=(row.get("channel") or "").strip(),
                sent_at=(row.get("sent_at") or "").strip(),
                notes=(row.get("notes") or "").strip(),
                slice_name=slice_name,
            )
        )
    return contacts


def select_first5(contacts: list[Contact], pool_limit: int = 20, count: int = 5) -> list[Contact]:
    if count <= 0:
        return []

    prioritized = [
        c
        for c in contacts[:pool_limit]
        if not c.sent_at and c.lead_id and c.name and c.company
    ]
    if len(prioritized) <= count:
        return prioritized
    return prioritized[:count]


def _angle_label(slice_name: str) -> str:
    if slice_name == SLICE_BIG4_ASSURANCE:
        return "Big 4 / Assurance client segment"
    if slice_name == SLICE_REGULATED_PROCESSOR:
        return "Regulated processor client segment"
    if slice_name == SLICE_VC_PLATFORM:
        return "VC / Platform client segment"
    return "one client segment"


def build_message(contact: Contact) -> str:
    angle = _angle_label(contact.slice_name)
    return (
        f"Hi {contact.name},\n"
        "I am building Dealix, a governed AI operations company starting in Saudi Arabia.\n"
        "This is not an AI automation resale motion.\n"
        "The angle is a governed AI operations diagnostic for clients already experimenting with AI "
        "but lacking source clarity, approval boundaries, evidence trails, proof of value, and agent identity controls.\n"
        f"Would it be useful to compare this against one {angle} you already see asking about AI governance?\n"
        "Best,\n"
        "Sami"
    )


def write_first5_queue(path: Path, selected: list[Contact]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "lead_id",
                "lead_name",
                "company",
                "role",
                "segment",
                "slice",
                "channel",
                "outcome",
                "founder_confirmed",
                "source_ref",
                "notes",
            ],
        )
        writer.writeheader()
        for c in selected:
            writer.writerow(
                {
                    "lead_id": c.lead_id,
                    "lead_name": c.name,
                    "company": c.company,
                    "role": c.role,
                    "segment": c.segment,
                    "slice": c.slice_name,
                    "channel": c.channel or "manual",
                    "outcome": "draft_ready",
                    "founder_confirmed": "false",
                    "source_ref": "",
                    "notes": "",
                }
            )


def write_drafts(path: Path, selected: list[Contact]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines: list[str] = []
    lines.append("# First 5 warm messages (manual send only)")
    lines.append("")
    lines.append(f"_Generated at: {_now_iso()}_")
    lines.append("")
    lines.append("Rules:")
    lines.append("- Send 5 only, no batch beyond first 5.")
    lines.append("- Log `sent` only after the real send.")
    lines.append("- Ask for one segment angle, not general partnership.")
    lines.append("- No attachments unless requested.")
    lines.append("")
    for idx, c in enumerate(selected, start=1):
        lines.append(f"## Contact {idx} — {c.name} ({c.company})")
        lines.append(f"- Lead ID: `{c.lead_id}`")
        lines.append(f"- Slice: `{c.slice_name}`")
        lines.append(f"- Channel: `{c.channel or 'manual'}`")
        lines.append("")
        lines.append("Subject: Governed AI operations — one client segment angle")
        lines.append("")
        lines.append("```text")
        lines.append(build_message(c))
        lines.append("```")
        lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def _ensure_events_file(path: Path) -> None:
    if path.exists():
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "event_at",
                "lead_id",
                "lead_name",
                "company",
                "slice",
                "event_type",
                "evidence_level",
                "source_ref",
                "founder_confirmed",
                "notes",
            ],
        )
        writer.writeheader()


def _load_events(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(encoding="utf-8") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def append_event(
    events_path: Path,
    tracker_path: Path,
    lead_id: str,
    event_type: str,
    source_ref: str,
    notes: str,
    founder_confirmed: bool,
) -> None:
    if event_type not in EVENT_TO_LEVEL:
        raise SystemExit(f"unsupported event_type={event_type!r}")
    if event_type == "sent" and not founder_confirmed:
        raise SystemExit("sent requires --confirm (do not log sent before real send)")

    contacts = load_contacts(tracker_path)
    target = next((c for c in contacts if c.lead_id == lead_id), None)
    if not target:
        raise SystemExit(f"lead_id={lead_id!r} not found in tracker")

    _ensure_events_file(events_path)
    with events_path.open("a", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "event_at",
                "lead_id",
                "lead_name",
                "company",
                "slice",
                "event_type",
                "evidence_level",
                "source_ref",
                "founder_confirmed",
                "notes",
            ],
        )
        writer.writerow(
            {
                "event_at": _now_iso(),
                "lead_id": target.lead_id,
                "lead_name": target.name,
                "company": target.company,
                "slice": target.slice_name,
                "event_type": event_type,
                "evidence_level": EVENT_TO_LEVEL[event_type],
                "source_ref": source_ref,
                "founder_confirmed": "true" if founder_confirmed else "false",
                "notes": notes,
            }
        )


def summarize_events(events: list[dict[str, str]]) -> dict[str, int | str]:
    sent_count = sum(1 for e in events if e.get("event_type") == "sent")
    reply_count = sum(1 for e in events if (e.get("event_type") or "").startswith("replied_"))
    meeting_booked_count = sum(1 for e in events if e.get("event_type") == "meeting_booked")
    l5_count = sum(1 for e in events if e.get("event_type") == "used_in_meeting")
    l6_count = sum(
        1 for e in events if e.get("event_type") in ("scope_requested", "pilot_intro_requested")
    )
    invoice_sent_count = sum(1 for e in events if e.get("event_type") == "invoice_sent")
    paid_proof_count = sum(1 for e in events if e.get("event_type") == "invoice_paid")

    if sent_count < 5:
        next_action = "Send remaining messages until 5 total."
    elif reply_count == 0:
        next_action = "Log first no_response and move to second slice."
    elif reply_count > 0 and meeting_booked_count == 0:
        next_action = "Convert interested reply into a 30-minute meeting."
    elif meeting_booked_count > 0 and l6_count == 0:
        next_action = "Push meeting outcome to scope_requested or pilot_intro_requested."
    elif invoice_sent_count > 0 and paid_proof_count == 0:
        next_action = "Follow manual payment confirmation to close paid proof."
    else:
        next_action = "Keep execution focused on documented external events only."

    ceo_summary = f"{sent_count} sent، {reply_count} replies، next action: {next_action}"
    return {
        "sent_count": sent_count,
        "reply_count": reply_count,
        "meeting_booked_count": meeting_booked_count,
        "l5_count": l5_count,
        "l6_count": l6_count,
        "invoice_sent_count": invoice_sent_count,
        "paid_proof_count": paid_proof_count,
        "ceo_summary": ceo_summary,
    }


def cmd_prepare_first5(args: argparse.Namespace) -> int:
    contacts = load_contacts(args.tracker)
    selected = select_first5(contacts, pool_limit=args.pool_limit, count=args.count)
    if not selected:
        print("No unsent contacts available in selected pool.")
        return 1

    write_first5_queue(args.queue_out, selected)
    write_drafts(args.drafts_out, selected)
    print(f"OK: selected {len(selected)} contacts from first {args.pool_limit}")
    print(f"queue: {args.queue_out}")
    print(f"drafts: {args.drafts_out}")
    for c in selected:
        print(f"- id={c.lead_id} {c.name} @ {c.company} [{c.slice_name}]")
    return 0


def cmd_record(args: argparse.Namespace) -> int:
    append_event(
        events_path=args.events,
        tracker_path=args.tracker,
        lead_id=args.id,
        event_type=args.event,
        source_ref=args.source_ref,
        notes=args.notes or "",
        founder_confirmed=args.confirm,
    )
    level = EVENT_TO_LEVEL[args.event]
    print(f"OK: recorded event={args.event} lead_id={args.id} level={level}")
    return 0


def cmd_summary(args: argparse.Namespace) -> int:
    events = _load_events(args.events)
    summary = summarize_events(events)
    if args.json:
        print(json.dumps(summary, indent=2, ensure_ascii=False))
    else:
        print("First 5 Market Events KPI")
        print("-------------------------")
        print(f"Sent count: {summary['sent_count']}")
        print(f"Reply count: {summary['reply_count']}")
        print(f"Meeting booked count: {summary['meeting_booked_count']}")
        print(f"L5 count: {summary['l5_count']}")
        print(f"L6 count: {summary['l6_count']}")
        print(f"Invoice sent count: {summary['invoice_sent_count']}")
        print(f"Paid proof count: {summary['paid_proof_count']}")
        print("")
        print(f"CEO: {summary['ceo_summary']}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Dealix first5 market events OS")
    sub = parser.add_subparsers(dest="cmd", required=True)

    prep = sub.add_parser("prepare-first5", help="Select first 5 and generate drafts")
    prep.add_argument("--tracker", type=Path, default=DEFAULT_TRACKER)
    prep.add_argument("--queue-out", type=Path, default=DEFAULT_QUEUE_OUT)
    prep.add_argument("--drafts-out", type=Path, default=DEFAULT_DRAFTS_OUT)
    prep.add_argument("--pool-limit", type=int, default=20)
    prep.add_argument("--count", type=int, default=5)
    prep.set_defaults(func=cmd_prepare_first5)

    record = sub.add_parser("record", help="Record a real market event")
    record.add_argument("--tracker", type=Path, default=DEFAULT_TRACKER)
    record.add_argument("--events", type=Path, default=DEFAULT_EVENTS)
    record.add_argument("--id", required=True, help="Lead ID from pipeline tracker")
    record.add_argument("--event", required=True, choices=sorted(EVENT_TO_LEVEL))
    record.add_argument("--source-ref", required=True, help="Evidence reference")
    record.add_argument("--notes", help="Optional notes")
    record.add_argument(
        "--confirm",
        action="store_true",
        help="Required when event=sent; confirms founder performed real send",
    )
    record.set_defaults(func=cmd_record)

    summary = sub.add_parser("summary", help="Render KPI7 summary")
    summary.add_argument("--events", type=Path, default=DEFAULT_EVENTS)
    summary.add_argument("--json", action="store_true")
    summary.set_defaults(func=cmd_summary)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    sys.exit(main())
