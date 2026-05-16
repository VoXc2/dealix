"""Market Motion OS for founder-led warm outreach.

Deterministic, audit-first helpers for:
- first-5 personalized outreach drafts (manual send only),
- response classification,
- evidence-level assignment (L4-L7),
- sequence validation (no fake traction/revenue),
- compact board decision from real signals.
"""

from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from datetime import UTC, datetime
from enum import StrEnum
from pathlib import Path


class MarketEvent(StrEnum):
    SENT = "sent"
    REPLIED_INTERESTED = "replied_interested"
    SEND_MORE_INFO = "send_more_info"
    ASKS_FOR_CASE_STUDY = "asks_for_case_study"
    ASKS_FOR_PDF = "asks_for_pdf"
    ASKS_FOR_ENGLISH = "asks_for_english"
    ASKS_FOR_SCOPE = "asks_for_scope"
    MEETING_BOOKED = "meeting_booked"
    USED_IN_MEETING = "used_in_meeting"
    PILOT_INTRO_REQUESTED = "pilot_intro_requested"
    NO_RESPONSE_AFTER_FOLLOW_UP = "no_response_after_follow_up"
    INVOICE_SENT = "invoice_sent"
    INVOICE_PAID = "invoice_paid"


class EvidenceLevel(StrEnum):
    L4_EXTERNAL_EXPOSURE = "L4"
    L5_USED_IN_MEETING = "L5"
    L6_MARKET_PULL = "L6"
    L7_REVENUE = "L7"


class BoardDecision(StrEnum):
    CONTINUE = "continue"
    REVISE_MESSAGE = "revise_message"
    TEST_BATCH_2 = "test_batch_2"
    BUILD_PDF = "build_pdf"
    PREPARE_SCOPE = "prepare_scope"


@dataclass(frozen=True)
class OutreachDraft:
    contact_id: str
    name: str
    role: str
    company: str
    sector: str
    personalized_line: str
    message_en: str
    message_ar: str


@dataclass(frozen=True)
class MarketMotionEvent:
    contact_id: str
    event: MarketEvent
    occurred_at: str
    source_ref: str
    note: str = ""

    def to_dict(self) -> dict[str, str]:
        return {
            "contact_id": self.contact_id,
            "event": self.event.value,
            "occurred_at": self.occurred_at,
            "source_ref": self.source_ref,
            "note": self.note,
        }

    @classmethod
    def from_dict(cls, payload: dict[str, str]) -> "MarketMotionEvent":
        return cls(
            contact_id=(payload.get("contact_id") or "").strip(),
            event=MarketEvent((payload.get("event") or "").strip()),
            occurred_at=(payload.get("occurred_at") or "").strip(),
            source_ref=(payload.get("source_ref") or "").strip(),
            note=(payload.get("note") or "").strip(),
        )


@dataclass(frozen=True)
class MarketMotionScoreboard:
    sent_count: int
    reply_rate: float
    meeting_rate: float
    l5_count: int
    l6_count: int
    invoice_sent_count: int
    invoice_paid_count: int
    reply_count: int
    meeting_count: int
    no_response_count: int
    asks_for_scope_count: int
    asks_for_pdf_count: int
    board_decision: BoardDecision


def _now_utc_iso() -> str:
    return datetime.now(UTC).isoformat()


def evidence_level_for_event(event: MarketEvent) -> EvidenceLevel | None:
    mapping = {
        MarketEvent.SENT: EvidenceLevel.L4_EXTERNAL_EXPOSURE,
        MarketEvent.USED_IN_MEETING: EvidenceLevel.L5_USED_IN_MEETING,
        MarketEvent.ASKS_FOR_SCOPE: EvidenceLevel.L6_MARKET_PULL,
        MarketEvent.PILOT_INTRO_REQUESTED: EvidenceLevel.L6_MARKET_PULL,
        MarketEvent.INVOICE_SENT: EvidenceLevel.L7_REVENUE,
        MarketEvent.INVOICE_PAID: EvidenceLevel.L7_REVENUE,
    }
    return mapping.get(event)


def _is_reply_event(event: MarketEvent) -> bool:
    return event in {
        MarketEvent.REPLIED_INTERESTED,
        MarketEvent.SEND_MORE_INFO,
        MarketEvent.ASKS_FOR_CASE_STUDY,
        MarketEvent.ASKS_FOR_PDF,
        MarketEvent.ASKS_FOR_ENGLISH,
        MarketEvent.ASKS_FOR_SCOPE,
        MarketEvent.MEETING_BOOKED,
        MarketEvent.USED_IN_MEETING,
        MarketEvent.PILOT_INTRO_REQUESTED,
        MarketEvent.INVOICE_SENT,
        MarketEvent.INVOICE_PAID,
    }


def _build_personalized_line(company: str, role: str, sector: str) -> str:
    return (
        f"Given your role at {company} as {role} in {sector}, "
        "I thought one client segment might be relevant."
    )


def _build_personalized_line_ar(company: str, role: str, sector: str) -> str:
    return (
        f"بحكم دورك في {company} كـ{role} وقطاع {sector}، "
        "أعتقد أن هناك شريحة عميل واحدة تستحق المقارنة."
    )


def build_first5_drafts_from_csv(csv_path: Path, *, limit: int = 5) -> list[OutreachDraft]:
    if limit <= 0:
        raise ValueError("limit must be > 0")
    if not csv_path.exists():
        raise FileNotFoundError(f"warm list CSV not found: {csv_path}")

    with csv_path.open("r", encoding="utf-8", newline="") as handle:
        rows = [r for r in csv.DictReader(handle) if (r.get("name") or "").strip()]

    drafts: list[OutreachDraft] = []
    for idx, row in enumerate(rows[:limit], start=1):
        name = (row.get("name") or "").strip() or f"Contact {idx}"
        role = (row.get("role") or "").strip() or "Role"
        company = (row.get("company") or "").strip() or "Company"
        sector = (row.get("sector") or "").strip() or "Sector"
        contact_id = f"{company}-{name}".lower().replace(" ", "-")
        line_en = _build_personalized_line(company=company, role=role, sector=sector)
        line_ar = _build_personalized_line_ar(company=company, role=role, sector=sector)

        message_en = (
            f"Hi {name},\n\n"
            "I’m building Dealix, a governed AI operations company starting in Saudi Arabia.\n\n"
            "This is not generic AI automation.\n\n"
            "The angle is a governed AI operations diagnostic for clients already experimenting "
            "with AI but lacking source clarity, approval boundaries, evidence trails, "
            "proof of value, and agent identity controls.\n\n"
            f"{line_en}\n\n"
            "Would it be useful to compare this against one client segment you already see "
            "asking about AI governance or AI-driven revenue operations?"
        )
        message_ar = (
            f"هلا {name}،\n\n"
            "أبني Dealix كشركة تشغيل ذكاء اصطناعي محكوم في السوق السعودي.\n\n"
            "هذا ليس بيع أتمتة عامة.\n\n"
            "التركيز هو تشخيص تشغيل ذكاء اصطناعي محكوم للعملاء الذين يجرّبون AI "
            "لكن تنقصهم وضوح المصادر وحدود الموافقة ومسار الأدلة وقياس القيمة "
            "وضبط هوية الوكلاء.\n\n"
            f"{line_ar}\n\n"
            "هل يفيدك أن نقارن هذا على شريحة عميل واحدة ترون لديها استخدام AI "
            "بدون حوكمة أو إثبات كافٍ؟"
        )
        drafts.append(
            OutreachDraft(
                contact_id=contact_id,
                name=name,
                role=role,
                company=company,
                sector=sector,
                personalized_line=line_en,
                message_en=message_en,
                message_ar=message_ar,
            )
        )
    return drafts


def render_first5_markdown(drafts: list[OutreachDraft]) -> str:
    lines: list[str] = []
    lines.append("# Warm list first 5 — governed market motion")
    lines.append("")
    lines.append(f"_Generated: {_now_utc_iso()}_")
    lines.append("")
    lines.append("Rules:")
    lines.append("- Manual send only (no automation).")
    lines.append("- One short personalized line per contact.")
    lines.append("- One question only.")
    lines.append("- Log `sent` only after external send happened.")
    lines.append("")
    for idx, draft in enumerate(drafts, start=1):
        lines.append(f"## {idx}. {draft.name} — {draft.role} @ {draft.company}")
        lines.append(f"- contact_id: `{draft.contact_id}`")
        lines.append(f"- sector: `{draft.sector}`")
        lines.append("")
        lines.append("### English")
        lines.append("```")
        lines.append(draft.message_en)
        lines.append("```")
        lines.append("")
        lines.append("### العربية")
        lines.append("```")
        lines.append(draft.message_ar)
        lines.append("```")
        lines.append("")
        lines.append("- sent: [ ]")
        lines.append("- reply: [ ]")
        lines.append("- next step: [ ]")
        lines.append("")
        lines.append("---")
        lines.append("")
    return "\n".join(lines)


def read_events(ledger_path: Path) -> list[MarketMotionEvent]:
    if not ledger_path.exists():
        return []
    events: list[MarketMotionEvent] = []
    with ledger_path.open("r", encoding="utf-8") as handle:
        for raw in handle:
            line = raw.strip()
            if not line:
                continue
            events.append(MarketMotionEvent.from_dict(json.loads(line)))
    return events


def validate_new_event(existing: list[MarketMotionEvent], new_event: MarketMotionEvent) -> None:
    if not new_event.contact_id:
        raise ValueError("contact_id is required")
    if not new_event.source_ref:
        raise ValueError("source_ref is required for auditability")
    if not new_event.occurred_at:
        raise ValueError("occurred_at is required")

    by_contact = [e for e in existing if e.contact_id == new_event.contact_id]
    seen = {e.event for e in by_contact}

    if new_event.event != MarketEvent.SENT and MarketEvent.SENT not in seen:
        raise ValueError("cannot log non-sent event before sent")
    if new_event.event == MarketEvent.USED_IN_MEETING and MarketEvent.MEETING_BOOKED not in seen:
        raise ValueError("used_in_meeting requires meeting_booked first")
    if new_event.event == MarketEvent.INVOICE_SENT and MarketEvent.ASKS_FOR_SCOPE not in seen:
        raise ValueError("invoice_sent requires asks_for_scope first")
    if new_event.event == MarketEvent.INVOICE_PAID and MarketEvent.INVOICE_SENT not in seen:
        raise ValueError("invoice_paid requires invoice_sent first")


def append_event(ledger_path: Path, event: MarketMotionEvent) -> None:
    existing = read_events(ledger_path)
    validate_new_event(existing, event)
    ledger_path.parent.mkdir(parents=True, exist_ok=True)
    with ledger_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(event.to_dict(), ensure_ascii=False) + "\n")


def build_scoreboard(events: list[MarketMotionEvent]) -> MarketMotionScoreboard:
    sent = [e for e in events if e.event == MarketEvent.SENT]
    sent_contacts = {e.contact_id for e in sent}
    if not sent_contacts:
        return MarketMotionScoreboard(
            sent_count=0,
            reply_rate=0.0,
            meeting_rate=0.0,
            l5_count=0,
            l6_count=0,
            invoice_sent_count=0,
            invoice_paid_count=0,
            reply_count=0,
            meeting_count=0,
            no_response_count=0,
            asks_for_scope_count=0,
            asks_for_pdf_count=0,
            board_decision=BoardDecision.CONTINUE,
        )

    replied_contacts = {
        e.contact_id for e in events
        if e.contact_id in sent_contacts and _is_reply_event(e.event)
    }
    meeting_contacts = {e.contact_id for e in events if e.event == MarketEvent.MEETING_BOOKED}

    l5_count = sum(1 for e in events if evidence_level_for_event(e.event) == EvidenceLevel.L5_USED_IN_MEETING)
    l6_count = sum(1 for e in events if evidence_level_for_event(e.event) == EvidenceLevel.L6_MARKET_PULL)
    invoice_sent_count = sum(1 for e in events if e.event == MarketEvent.INVOICE_SENT)
    invoice_paid_count = sum(1 for e in events if e.event == MarketEvent.INVOICE_PAID)
    no_response_count = sum(1 for e in events if e.event == MarketEvent.NO_RESPONSE_AFTER_FOLLOW_UP)
    asks_for_scope_count = sum(1 for e in events if e.event == MarketEvent.ASKS_FOR_SCOPE)
    asks_for_pdf_count = sum(1 for e in events if e.event == MarketEvent.ASKS_FOR_PDF)

    reply_count = len(replied_contacts)
    sent_count = len(sent_contacts)
    meeting_count = len(meeting_contacts)
    reply_rate = reply_count / sent_count if sent_count else 0.0
    meeting_rate = meeting_count / sent_count if sent_count else 0.0

    decision = board_decision(
        sent_count=sent_count,
        reply_count=reply_count,
        meeting_count=meeting_count,
        no_response_count=no_response_count,
        asks_for_scope_count=asks_for_scope_count,
        asks_for_pdf_count=asks_for_pdf_count,
    )

    return MarketMotionScoreboard(
        sent_count=sent_count,
        reply_rate=reply_rate,
        meeting_rate=meeting_rate,
        l5_count=l5_count,
        l6_count=l6_count,
        invoice_sent_count=invoice_sent_count,
        invoice_paid_count=invoice_paid_count,
        reply_count=reply_count,
        meeting_count=meeting_count,
        no_response_count=no_response_count,
        asks_for_scope_count=asks_for_scope_count,
        asks_for_pdf_count=asks_for_pdf_count,
        board_decision=decision,
    )


def board_decision(
    *,
    sent_count: int,
    reply_count: int,
    meeting_count: int,  # reserved for future tuning
    no_response_count: int,
    asks_for_scope_count: int,
    asks_for_pdf_count: int,
) -> BoardDecision:
    del meeting_count  # explicitly not used yet

    if asks_for_scope_count > 0:
        return BoardDecision.PREPARE_SCOPE
    if asks_for_pdf_count >= 2:
        return BoardDecision.BUILD_PDF
    if sent_count >= 5 and reply_count == 0 and no_response_count >= sent_count:
        return BoardDecision.TEST_BATCH_2
    if sent_count >= 5 and sent_count > 0 and (reply_count / sent_count) < 0.2:
        return BoardDecision.REVISE_MESSAGE
    return BoardDecision.CONTINUE


__all__ = [
    "BoardDecision",
    "EvidenceLevel",
    "MarketEvent",
    "MarketMotionEvent",
    "MarketMotionScoreboard",
    "OutreachDraft",
    "append_event",
    "board_decision",
    "build_first5_drafts_from_csv",
    "build_scoreboard",
    "evidence_level_for_event",
    "read_events",
    "render_first5_markdown",
    "validate_new_event",
]
