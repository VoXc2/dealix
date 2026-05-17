"""Full Ops 2.0 — multi-step outreach sequence engine.

A *sequence* is a named, ordered list of steps. Each step carries a
day-offset (relative to the enrollment date), a purpose and a template
key. The engine computes which step is due next for a given lead's
enrollment — it does NOT send anything.

DOCTRINE — sequences only PREPARE drafts. Every step whose channel
sends externally still has ``requires_approval=True`` and must route
through founder approval before any message leaves the system. There
is no auto-send path in this module.

Pure-function core. NO LLM. NO I/O. NO external send.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, timezone


@dataclass(frozen=True)
class SequenceStep:
    """One step in an outreach sequence."""

    step_number: int
    day_offset: int          # days after enrollment this step becomes due
    channel: str             # email_warm / linkedin_manual / phone_task ...
    purpose: str             # short purpose label
    template_key: str        # key the draft renderer resolves
    requires_approval: bool = True  # DOCTRINE — external steps need approval


@dataclass(frozen=True)
class OutreachSequence:
    """A named, ordered sequence of steps."""

    name: str
    description: str
    steps: tuple[SequenceStep, ...]


# ── The named sequences ──────────────────────────────────────────
# Channels stay within the doctrine-allowed set: warm email, manual
# LinkedIn (human-only), phone tasks. NO cold WhatsApp. NO LinkedIn
# automation — `linkedin_manual` means a human acts after approval.
SEQUENCES: dict[str, OutreachSequence] = {
    "warm_linkedin": OutreachSequence(
        name="warm_linkedin",
        description="Warm LinkedIn touch sequence (manual, human-sent).",
        steps=(
            SequenceStep(1, 0, "linkedin_manual", "connect", "li_connect"),
            SequenceStep(2, 3, "linkedin_manual", "value_share", "li_value_share"),
            SequenceStep(3, 8, "email_warm", "proof_offer", "email_proof_offer"),
            SequenceStep(4, 15, "phone_task", "soft_call", "phone_soft_call"),
        ),
    ),
    "proof_pack_download": OutreachSequence(
        name="proof_pack_download",
        description="Follow-up after a Proof Pack download.",
        steps=(
            SequenceStep(1, 0, "email_warm", "thank_you", "email_proof_thanks"),
            SequenceStep(2, 2, "email_warm", "context_question", "email_proof_question"),
            SequenceStep(3, 6, "email_warm", "diagnostic_offer", "email_diagnostic_offer"),
            SequenceStep(4, 12, "phone_task", "qualification_call", "phone_qualify"),
        ),
    ),
    "partner": OutreachSequence(
        name="partner",
        description="Partner / affiliate nurture sequence.",
        steps=(
            SequenceStep(1, 0, "email_warm", "partner_intro", "email_partner_intro"),
            SequenceStep(2, 4, "email_warm", "partner_proof", "email_partner_proof"),
            SequenceStep(3, 10, "phone_task", "partner_fit_call", "phone_partner_fit"),
        ),
    ),
    "webinar": OutreachSequence(
        name="webinar",
        description="Webinar registration to attendance to follow-up.",
        steps=(
            SequenceStep(1, 0, "email_warm", "confirm_registration", "email_webinar_confirm"),
            SequenceStep(2, 5, "email_warm", "reminder", "email_webinar_reminder"),
            SequenceStep(3, 8, "email_warm", "recording_followup", "email_webinar_recording"),
            SequenceStep(4, 12, "phone_task", "post_webinar_call", "phone_webinar_followup"),
        ),
    ),
}


def list_sequences() -> list[dict[str, object]]:
    """Return all sequences as plain dicts (for the router)."""
    return [_sequence_to_dict(s) for s in SEQUENCES.values()]


def get_sequence(name: str) -> OutreachSequence | None:
    """Look up a sequence by name (case-insensitive)."""
    return SEQUENCES.get((name or "").strip().lower())


def _sequence_to_dict(seq: OutreachSequence) -> dict[str, object]:
    return {
        "name": seq.name,
        "description": seq.description,
        "step_count": len(seq.steps),
        "steps": [
            {
                "step_number": s.step_number,
                "day_offset": s.day_offset,
                "channel": s.channel,
                "purpose": s.purpose,
                "template_key": s.template_key,
                "requires_approval": s.requires_approval,
            }
            for s in seq.steps
        ],
    }


def _parse_date(value: str) -> date | None:
    """Parse an ISO date or datetime string into a date. None on failure."""
    raw = (value or "").strip()
    if not raw:
        return None
    try:
        return datetime.fromisoformat(raw).date()
    except ValueError:
        try:
            return date.fromisoformat(raw)
        except ValueError:
            return None


@dataclass(frozen=True)
class NextStepResult:
    """Outcome of computing the next pending step for a lead."""

    sequence: str
    lead_id: str
    has_pending_step: bool
    next_step: dict[str, object] | None
    completed_steps: int
    total_steps: int
    reason_en: str
    reason_ar: str


def compute_next_step(
    *,
    sequence_name: str,
    lead_id: str,
    enrolled_on: str,
    completed_steps: int = 0,
    as_of: str | None = None,
) -> NextStepResult:
    """Compute the next pending step for a lead in a sequence.

    A step is *pending* when its ``day_offset`` has elapsed since
    ``enrolled_on`` and it has not yet been completed. ``completed_steps``
    is the count of steps already prepared/approved for this lead.

    DOCTRINE — the returned step is a DRAFT instruction only. The
    ``requires_approval`` flag on the step is always honored; nothing
    here sends a message.
    """
    seq = get_sequence(sequence_name)
    if seq is None:
        return NextStepResult(
            sequence=sequence_name,
            lead_id=lead_id,
            has_pending_step=False,
            next_step=None,
            completed_steps=completed_steps,
            total_steps=0,
            reason_en=f"Unknown sequence '{sequence_name}'.",
            reason_ar=f"تسلسل غير معروف '{sequence_name}'.",
        )

    enrolled = _parse_date(enrolled_on)
    if enrolled is None:
        return NextStepResult(
            sequence=seq.name,
            lead_id=lead_id,
            has_pending_step=False,
            next_step=None,
            completed_steps=completed_steps,
            total_steps=len(seq.steps),
            reason_en="Invalid or missing enrollment date.",
            reason_ar="تاريخ التسجيل غير صالح أو مفقود.",
        )

    today = _parse_date(as_of) if as_of else datetime.now(timezone.utc).date()
    if today is None:
        today = datetime.now(timezone.utc).date()

    elapsed_days = (today - enrolled).days
    done = max(0, int(completed_steps))

    if done >= len(seq.steps):
        return NextStepResult(
            sequence=seq.name,
            lead_id=lead_id,
            has_pending_step=False,
            next_step=None,
            completed_steps=done,
            total_steps=len(seq.steps),
            reason_en="Sequence complete — all steps prepared.",
            reason_ar="اكتمل التسلسل — جميع الخطوات جُهّزت.",
        )

    candidate = seq.steps[done]
    if elapsed_days < candidate.day_offset:
        wait = candidate.day_offset - elapsed_days
        return NextStepResult(
            sequence=seq.name,
            lead_id=lead_id,
            has_pending_step=False,
            next_step=None,
            completed_steps=done,
            total_steps=len(seq.steps),
            reason_en=f"Next step not yet due — {wait} day(s) remaining.",
            reason_ar=f"الخطوة التالية غير مستحقة — يتبقى {wait} يوم.",
        )

    return NextStepResult(
        sequence=seq.name,
        lead_id=lead_id,
        has_pending_step=True,
        next_step={
            "step_number": candidate.step_number,
            "day_offset": candidate.day_offset,
            "channel": candidate.channel,
            "purpose": candidate.purpose,
            "template_key": candidate.template_key,
            "requires_approval": candidate.requires_approval,
            "prepare_only": True,
        },
        completed_steps=done,
        total_steps=len(seq.steps),
        reason_en="Step is due — prepare a draft for founder approval.",
        reason_ar="الخطوة مستحقة — جهّز مسوّدة لموافقة المؤسس.",
    )


__all__ = [
    "NextStepResult",
    "OutreachSequence",
    "SEQUENCES",
    "SequenceStep",
    "compute_next_step",
    "get_sequence",
    "list_sequences",
]
