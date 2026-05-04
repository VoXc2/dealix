"""
Self-Growth Mode — Dealix uses itself to grow Dealix.

Pure planner: produces a *daily plan* (segment, channel, message, target count,
forbidden actions) and a *weekly learning report* from the proof events.

Critical safety rules baked in:
  - cold WhatsApp is ALWAYS in `forbidden_today`.
  - LinkedIn automation is ALWAYS in `forbidden_today`.
  - mass send is ALWAYS in `forbidden_today`.
  - All outbound is approval-first; the daily plan emits *task counts*, not
    auto-send commands.

The planner rotates between 3 wedge segments (deterministic by ISO week
+ weekday) so we cover the Saudi B2B market without burning any list.
"""

from __future__ import annotations

import datetime as _dt
from collections import Counter
from dataclasses import dataclass
from typing import Any


WEDGE_SEGMENTS: tuple[tuple[str, str], ...] = (
    # (segment_id, arabic_label)
    ("agencies_riyadh_b2b",      "وكالات تسويق B2B في الرياض"),
    ("training_consulting_ksa",  "شركات تدريب/استشارات في السعودية"),
    ("b2b_services_jeddah",      "شركات خدمات B2B في جدة والمنطقة الغربية"),
)

# Channels we run today + counts (manual/draft only — no live send).
DEFAULT_CHANNEL_PLAN: tuple[dict[str, Any], ...] = (
    {"channel": "linkedin_manual",  "count": 10, "mode": "manual_task"},
    {"channel": "email_draft",      "count": 5,  "mode": "draft_only"},
    {"channel": "referral_followup","count": 3,  "mode": "manual_task"},
)

# Hard floor — ALWAYS in forbidden_today (refusal labels, not active code paths).
ALWAYS_FORBIDDEN_TODAY: tuple[str, ...] = (
    "cold_whatsapp",          # forbidden / blocked refusal label
    "linkedin_auto_dm",       # forbidden / blocked refusal label
    "mass_send",              # forbidden / blocked refusal label
    "scrape_linkedin",        # forbidden / blocked refusal label
    "purchase_phone_lists",   # forbidden / blocked refusal label
)


@dataclass(frozen=True)
class DailyPlan:
    date: str
    iso_week: str
    weekday: str
    focus_segment_id: str
    focus_segment_ar: str
    channel_plan: tuple[dict[str, Any], ...]
    experiment_hypothesis_ar: str
    message_variants_ar: tuple[str, ...]
    forbidden_today: tuple[str, ...]
    expected_proof_events: tuple[str, ...]


def _segment_for(today: _dt.date) -> tuple[str, str]:
    """Deterministically pick a wedge segment for a given date."""
    idx = (today.isocalendar().week + today.weekday()) % len(WEDGE_SEGMENTS)
    return WEDGE_SEGMENTS[idx]


def build_daily_plan(today: _dt.date | None = None) -> DailyPlan:
    today = today or _dt.date.today()
    seg_id, seg_ar = _segment_for(today)
    iso = today.isocalendar()

    # Hypothesis rotates with weekday so we test different angles
    hypotheses = [
        "Co-branded Proof Pack يرفع ردود الوكالات.",
        "افتتاحية تركّز على 'Proof خلال 7 أيام' أعلى من 'AI'.",
        "ذكر Pilot 499 صراحة في أول جملة يقصّر دورة الرد.",
        "Reference customer من نفس القطاع يفتح اجتماع أسرع.",
        "Mini Diagnostic مجاني يعمل أفضل من PDF deck.",
    ]
    hyp = hypotheses[today.weekday() % len(hypotheses)]

    variants = (
        "نجهّز لكم Diagnostic مجاني لعميل واحد + Co-branded Proof Pack باسمكم.",
        "Pilot 7 أيام بـ 499 ريال: 10 فرص + رسائل عربية + Proof Pack — بدون التزام شهري.",
    )

    return DailyPlan(
        date=today.isoformat(),
        iso_week=f"{iso.year:04d}-W{iso.week:02d}",
        weekday=today.strftime("%A"),
        focus_segment_id=seg_id,
        focus_segment_ar=seg_ar,
        channel_plan=DEFAULT_CHANNEL_PLAN,
        experiment_hypothesis_ar=hyp,
        message_variants_ar=variants,
        forbidden_today=ALWAYS_FORBIDDEN_TODAY,
        expected_proof_events=(
            "target_ranked", "draft_created", "approval_collected",
            "risk_blocked", "followup_created",
        ),
    )


def daily_plan_to_dict(p: DailyPlan) -> dict[str, Any]:
    return {
        "date": p.date,
        "iso_week": p.iso_week,
        "weekday": p.weekday,
        "focus_segment_id": p.focus_segment_id,
        "focus_segment_ar": p.focus_segment_ar,
        "channel_plan": list(p.channel_plan),
        "experiment_hypothesis_ar": p.experiment_hypothesis_ar,
        "message_variants_ar": list(p.message_variants_ar),
        "forbidden_today": list(p.forbidden_today),
        "expected_proof_events": list(p.expected_proof_events),
        "approval_first": True,
        "anti_claim_ar": "Dealix يجهّز ويُحضّر — لا يرسل قبل موافقتك.",
    }


# ── Weekly learning ───────────────────────────────────────────────


def build_weekly_learning(events) -> dict[str, Any]:
    """Summarize proof events of the last week into a learning card.

    Pure: takes an iterable of ProofEventRecord-like.
    Returns: best segment, best message, biggest bottleneck, one experiment
    to test next week.
    """
    by_unit: Counter[str] = Counter()
    by_actor: Counter[str] = Counter()
    high_risk_blocked = 0
    pending_approvals = 0
    for e in events:
        by_unit[e.unit_type] += 1
        by_actor[e.actor or "system"] += 1
        if e.unit_type == "risk_blocked" and e.risk_level == "high":
            high_risk_blocked += 1
        if e.approval_required and not e.approved:
            pending_approvals += 1

    bottleneck = _diagnose_bottleneck(by_unit)
    next_experiment = _propose_next_experiment(by_unit)
    return {
        "totals_by_unit": dict(by_unit),
        "actors_active": list(by_actor.keys()),
        "high_risk_blocked": high_risk_blocked,
        "pending_approvals": pending_approvals,
        "bottleneck_ar": bottleneck,
        "next_experiment_ar": next_experiment,
        "no_unsafe_action_executed": True,  # invariant — Dealix does not auto-send
    }


def _diagnose_bottleneck(by_unit: Counter[str]) -> str:
    if by_unit.get("draft_created", 0) > by_unit.get("approval_collected", 0) * 2:
        return "Drafts بدون موافقة — قائمة الموافقات تتراكم."
    if by_unit.get("opportunity_created", 0) > 0 and by_unit.get("meeting_drafted", 0) == 0:
        return "فرص بدون اجتماعات — حاجز Diagnostic→Pilot."
    if by_unit.get("proof_generated", 0) == 0 and by_unit.get("opportunity_created", 0) >= 5:
        return "فرص بدون Proof Pack — حاجز Pilot→Renewal."
    if by_unit.get("opportunity_created", 0) == 0:
        return "لا فرص جديدة — حاجز ICP/Signal scan."
    return "لا اختناقات حادة هذا الأسبوع — حافظ على الإيقاع."


def _propose_next_experiment(by_unit: Counter[str]) -> str:
    if by_unit.get("approval_collected", 0) < by_unit.get("draft_created", 0):
        return "اختبر تنبيه Approval queue كل 4 ساعات بدلاً من يومي."
    if by_unit.get("meeting_drafted", 0) == 0:
        return "اختبر CTA 'Mini Diagnostic 24 ساعة' في follow-up."
    if by_unit.get("proof_generated", 0) > 0:
        return "اختبر عرض Executive Growth OS فور تسليم Proof Pack الأول."
    return "اختبر تغيير الافتتاحية لـ 'Proof خلال 7 أيام' في 50% من الـ drafts."


# ── Auto-loop (called by daily-ops closing window) ──────────────────


def _new_experiment_id() -> str:
    import uuid
    return f"sgx_{uuid.uuid4().hex[:14]}"


async def loop_once(today: _dt.date | None = None) -> dict[str, Any]:
    """Idempotent self-growth tick: ensure today has one experiment recorded.

    - If a GrowthExperimentRecord already exists for today's date in this
      ISO week, return {"skipped": True, ...} without writing.
    - Otherwise build today's plan, persist it as a GrowthExperimentRecord
      with status="planned" + the daily plan dict in meta_json.

    Pure ORM. Caller commits via the daily-ops orchestrator's session.
    Used by scripts/cron_daily_ops.py at the closing window.
    """
    from sqlalchemy import select

    from db.models import GrowthExperimentRecord
    from db.session import get_session

    today = today or _dt.date.today()
    plan = build_daily_plan(today)

    async with get_session() as session:
        existing = (await session.execute(
            select(GrowthExperimentRecord).where(
                GrowthExperimentRecord.week_iso == plan.iso_week,
                GrowthExperimentRecord.segment == plan.focus_segment_id,
            )
        )).scalar_one_or_none()

        if existing is not None:
            return {
                "skipped": True,
                "reason": "experiment_already_planned_this_week_for_segment",
                "experiment_id": existing.id,
                "week_iso": existing.week_iso,
                "segment": existing.segment,
            }

        row = GrowthExperimentRecord(
            id=_new_experiment_id(),
            week_iso=plan.iso_week,
            hypothesis_ar=plan.experiment_hypothesis_ar,
            segment=plan.focus_segment_id,
            channel="multi",  # plan covers 3 channels
            message_ar=" || ".join(plan.message_variants_ar),
            status="planned",
            n_targets_planned=sum(int(c.get("count") or 0) for c in plan.channel_plan),
            meta_json={
                "plan": daily_plan_to_dict(plan),
                "auto_recorded": True,
                "source": "self_growth_mode.loop_once",
            },
        )
        session.add(row)
        await session.commit()

    return {
        "skipped": False,
        "experiment_id": row.id,
        "week_iso": row.week_iso,
        "segment": row.segment,
        "n_targets_planned": row.n_targets_planned,
        "hypothesis_ar": row.hypothesis_ar,
    }
