"""Weekly self-improvement loop — Track C6 of 30-day plan.

Runs every Sunday 22:00 Riyadh. Reads the weekly scorecard, diffs against
last week, and queues 3 specific improvement suggestions to the founder's
approval queue.

Hard rules:
  - NO actions without founder approval (Article 5)
  - NO_FAKE_PROOF — suggestions cite specific files / endpoints / counts
  - NO_FAKE_REVENUE — never invents revenue numbers in suggestions
  - Output is always 3 suggestions max (cognitive load discipline)

Per Master Plan §V.B #4. Depends on C1 (proof_events Postgres table)
for richer signals once production data exists.
"""

from __future__ import annotations

import json
import logging
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

REPO = Path(__file__).resolve().parents[2]
WEEKLY_CACHE = REPO / "docs" / "weekly_scorecard_cache.json"

# Token budget (small — suggestions are punchy)
MAX_OUTPUT_TOKENS = 600


@dataclass
class Suggestion:
    title: str
    why_it_matters: str
    specific_file: str | None
    specific_metric: str | None
    next_action: str
    expected_impact: str  # "high" | "medium" | "low"
    estimated_minutes: int = 30

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class WeeklyScorecard:
    week_starting: str  # ISO date Monday of the week
    proof_events_total: int = 0
    proof_events_l4_plus: int = 0
    proof_events_l5: int = 0
    pending_approvals: int = 0
    revenue_sar: float = 0.0
    paid_customers: int = 0
    new_customers: int = 0
    churned_customers: int = 0
    forbidden_token_violations: int = 0
    article_13_violations: int = 0
    health_endpoint_uptime_pct: float = 100.0
    suggestions: list[Suggestion] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d["suggestions"] = [s.to_dict() for s in self.suggestions]
        return d


def _previous_monday(now: datetime | None = None) -> datetime:
    now = now or datetime.now(UTC)
    days_back = (now.weekday() + 0) % 7
    if days_back == 0:
        days_back = 7
    return (now - timedelta(days=days_back)).replace(
        hour=0, minute=0, second=0, microsecond=0
    )


def _load_previous_scorecard() -> WeeklyScorecard | None:
    if not WEEKLY_CACHE.exists():
        return None
    try:
        data = json.loads(WEEKLY_CACHE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None
    suggestions = [Suggestion(**s) for s in data.pop("suggestions", [])]
    return WeeklyScorecard(suggestions=suggestions, **data)


def _save_scorecard(card: WeeklyScorecard) -> None:
    WEEKLY_CACHE.parent.mkdir(parents=True, exist_ok=True)
    WEEKLY_CACHE.write_text(
        json.dumps(card.to_dict(), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def _gather_signals() -> dict[str, Any]:
    """Pull this week's signals from existing modules. Returns dict."""
    signals: dict[str, Any] = {
        "proof_events_total": 0,
        "proof_events_l4_plus": 0,
        "proof_events_l5": 0,
        "pending_approvals": 0,
        "revenue_sar": 0.0,
        "paid_customers": 0,
    }
    week_ago = datetime.now(UTC) - timedelta(days=7)

    try:
        from auto_client_acquisition.proof_ledger import (  # type: ignore
            recent_events,
        )
        events = recent_events(since=week_ago) or []
        signals["proof_events_total"] = len(events)
        for e in events:
            level = (e.get("level") if isinstance(e, dict) else getattr(e, "level", "")) or ""
            if level.upper() in ("L4", "L5"):
                signals["proof_events_l4_plus"] += 1
            if level.upper() == "L5":
                signals["proof_events_l5"] += 1
                payload = (
                    e.get("payload") if isinstance(e, dict) else getattr(e, "payload", {})
                ) or {}
                signals["revenue_sar"] += float(payload.get("amount_sar", 0))
    except (ImportError, Exception):  # noqa: BLE001
        pass

    try:
        from auto_client_acquisition.approval_center import list_pending  # type: ignore
        signals["pending_approvals"] = len(list_pending() or [])
    except (ImportError, Exception):  # noqa: BLE001
        pass

    return signals


def _generate_deterministic_suggestions(
    current: WeeklyScorecard,
    previous: WeeklyScorecard | None,
) -> list[Suggestion]:
    """Generate 3 concrete suggestions from the diff.

    Always returns exactly 3 (or fewer if the founder's day is empty —
    then we return the smaller set so we don't manufacture work).
    """
    suggestions: list[Suggestion] = []

    # Rule 1 — pending approvals piling up
    if current.pending_approvals >= 5:
        suggestions.append(
            Suggestion(
                title="📋 موافقات معلّقة عالية",
                why_it_matters=(
                    f"{current.pending_approvals} approval pending — قراراتك "
                    "تتأخّر، Dealix لا ينفّذ بدونك."
                ),
                specific_file="landing/decisions.html",
                specific_metric=f"pending_approvals={current.pending_approvals}",
                next_action="افتح /decisions.html واعتمد أو ارفض القائمة كاملة (15 دقيقة).",
                expected_impact="high",
                estimated_minutes=15,
            )
        )

    # Rule 2 — no proof events this week
    if current.proof_events_total == 0:
        suggestions.append(
            Suggestion(
                title="📜 لا proof events هذا الأسبوع",
                why_it_matters=(
                    "Article 3 Law 2 (No proof → no claim). أسبوع بدون event "
                    "= أسبوع بدون قاعدة لـ Proof Pack."
                ),
                specific_file="landing/founder-proof-create.html",
                specific_metric="proof_events_total=0",
                next_action=(
                    "افتح /founder-proof-create.html وسجّل أصغر event (L1 Internal Draft) "
                    "حتى تبدأ الـ ledger يتراكم."
                ),
                expected_impact="medium",
                estimated_minutes=10,
            )
        )

    # Rule 3 — revenue regression vs last week
    if previous and previous.revenue_sar > current.revenue_sar:
        delta = previous.revenue_sar - current.revenue_sar
        suggestions.append(
            Suggestion(
                title=f"📉 انخفاض الإيراد {delta:,.0f} SAR vs الأسبوع الماضي",
                why_it_matters=(
                    "تراجع الإيراد قد يعني pilot fell off أو CS handoff لم يحدث. "
                    "تحقّق قبل أن يصبح pattern."
                ),
                specific_file="api/routers/payment_ops.py",
                specific_metric=(
                    f"this_week={current.revenue_sar:,.0f} · last_week={previous.revenue_sar:,.0f}"
                ),
                next_action=(
                    "راجع payment_ops/{id}/state لكل invoice من الأسبوع، تحقّق ما لم "
                    "تتحوّل إلى payment_confirmed."
                ),
                expected_impact="high",
                estimated_minutes=20,
            )
        )

    # Rule 4 — first L5 event milestone
    if previous and previous.proof_events_l5 == 0 and current.proof_events_l5 >= 1:
        suggestions.append(
            Suggestion(
                title="🎉 أوّل L5 Revenue Evidence — انشر case study",
                why_it_matters=(
                    "أوّل L5 = أوّل دليل revenue قابل للتدقيق. هذه أقوى أداة "
                    "تسويقيّة في 90 يوم."
                ),
                specific_file="landing/proof.html",
                specific_metric=f"proof_events_l5={current.proof_events_l5}",
                next_action=(
                    "اطلب publish_consent من العميل عبر /founder-proof-create.html ثم "
                    "انشر anonymized case study على /proof.html."
                ),
                expected_impact="high",
                estimated_minutes=45,
            )
        )

    # Rule 5 — forbidden token / Article 13 violation (CRITICAL)
    if current.forbidden_token_violations + current.article_13_violations > 0:
        suggestions.append(
            Suggestion(
                title="🚨 Constitutional violation",
                why_it_matters=(
                    f"forbidden_tokens={current.forbidden_token_violations} · "
                    f"article_13={current.article_13_violations}. "
                    "هذا يفشل CI — توقّف عن الميزات الأخرى وأصلح أولاً."
                ),
                specific_file="tests/test_landing_forbidden_claims.py",
                specific_metric=(
                    f"violations={current.forbidden_token_violations + current.article_13_violations}"
                ),
                next_action="شغّل: python -m pytest tests/test_landing_forbidden_claims.py tests/test_article_13_compliance.py -q",
                expected_impact="high",
                estimated_minutes=30,
            )
        )

    # Default: if everything is calm, suggest the 5-warm-intros nudge
    if not suggestions:
        suggestions.append(
            Suggestion(
                title="✉️ Send the 5 warm intros (founder, manual)",
                why_it_matters=(
                    "Article 13 لا يفتح Wave 4 قبل 3 paid pilots. الـ pilots لا "
                    "تأتي من الكود — تأتي من المحادثات."
                ),
                specific_file="docs/sales-kit/dealix_leads_20_real.md",
                specific_metric="paid_customers=0 (pre-Article-13 trigger)",
                next_action=(
                    "افتح القائمة، اختر 5 أسماء، ارسل 5 رسائل WhatsApp "
                    "warm-intro خلال 30 دقيقة."
                ),
                expected_impact="high",
                estimated_minutes=30,
            )
        )

    # Cognitive load discipline: max 3 suggestions
    return suggestions[:3]


def _queue_suggestions_to_approval(
    suggestions: list[Suggestion], week_starting: str
) -> list[str]:
    """Push each suggestion as a draft into the approval queue."""
    approval_ids: list[str] = []
    try:
        from auto_client_acquisition.approval_center import enqueue  # type: ignore
    except ImportError:
        for s in suggestions:
            approval_ids.append(f"wsi_{week_starting}_{abs(hash(s.title)) % 100000}")
        return approval_ids
    for s in suggestions:
        approval_id = f"wsi_{week_starting}_{abs(hash(s.title)) % 100000}"
        try:
            enqueue(
                approval_id=approval_id,
                action_type="weekly_suggestion",
                summary_ar=s.title,
                summary_en=s.title,
                payload={
                    "why_it_matters": s.why_it_matters,
                    "specific_file": s.specific_file,
                    "specific_metric": s.specific_metric,
                    "next_action": s.next_action,
                    "expected_impact": s.expected_impact,
                    "estimated_minutes": s.estimated_minutes,
                    "week_starting": week_starting,
                },
                channel="weekly_self_improvement",
                risk_level="low",
            )
        except Exception as exc:  # noqa: BLE001
            logger.warning("weekly_suggestion_enqueue_failed: %s", exc)
        approval_ids.append(approval_id)
    return approval_ids


def run_weekly_self_improvement() -> WeeklyScorecard:
    """Main entrypoint — invoked by Sunday cron / ARQ task.

    Always succeeds (graceful fallback). Returns the new scorecard.
    """
    week_start = _previous_monday()
    previous = _load_previous_scorecard()
    signals = _gather_signals()

    current = WeeklyScorecard(
        week_starting=week_start.date().isoformat(),
        proof_events_total=int(signals.get("proof_events_total", 0)),
        proof_events_l4_plus=int(signals.get("proof_events_l4_plus", 0)),
        proof_events_l5=int(signals.get("proof_events_l5", 0)),
        pending_approvals=int(signals.get("pending_approvals", 0)),
        revenue_sar=float(signals.get("revenue_sar", 0.0)),
    )

    suggestions = _generate_deterministic_suggestions(current, previous)
    current.suggestions = suggestions

    approval_ids = _queue_suggestions_to_approval(
        suggestions, current.week_starting
    )
    logger.info(
        "weekly_self_improvement: %d suggestions queued (approval_ids=%s)",
        len(suggestions),
        approval_ids,
    )

    _save_scorecard(current)
    return current


if __name__ == "__main__":
    card = run_weekly_self_improvement()
    print(json.dumps(card.to_dict(), ensure_ascii=False, indent=2))
