"""Weekly CEO Review — 45 minutes, 11 questions, exactly 5 decisions.

The review turns the founder from "someone who builds" into "a CEO who
runs a revenue system". It must end with five concrete decisions.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any

from auto_client_acquisition.revenue_assurance_os.root_cause import diagnose

# (English, Arabic) — asked every week.
CEO_QUESTIONS: tuple[tuple[str, str], ...] = (
    ("What brought leads?", "ما الذي جلب leads؟"),
    ("What brought meetings?", "ما الذي جلب meetings؟"),
    ("What brought paid intent?", "ما الذي جلب paid intent؟"),
    ("Where did the funnel stop?", "أين توقف funnel؟"),
    ("What was the most common objection?", "ما أكثر objection؟"),
    ("What was the most common support question?", "ما أكثر support question؟"),
    ("Which affiliate sent bad leads?", "أي affiliate أرسل leads سيئة؟"),
    ("Which partner sent good leads?", "أي partner أرسل leads جيدة؟"),
    ("Which claims were blocked?", "أي claims تم حظرها؟"),
    ("Which workflow repeated?", "أي workflow تكرر؟"),
    ("Do we build or not?", "هل نبني أم لا؟"),
)

# The five decisions the review must produce.
REQUIRED_DECISIONS: tuple[tuple[str, str], ...] = (
    ("double_down", "Double down on what works"),
    ("fix_bottleneck", "Fix the funnel bottleneck"),
    ("kill_channel", "Kill a channel that does not work"),
    ("improve_asset", "Improve a sales or proof asset"),
    ("build_or_no_build", "Build / No-build decision"),
)


@dataclass(frozen=True, slots=True)
class CeoReview:
    week_label: str
    generated_at: str
    questions: tuple[tuple[str, str], ...]
    required_decisions: tuple[tuple[str, str], ...]
    bottleneck: dict[str, Any] | None = None
    notes: dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _week_label(now: datetime | None = None) -> str:
    now = now or datetime.now(timezone.utc)
    iso = now.isocalendar()
    return f"{iso.year}-W{iso.week:02d}"


def build_ceo_review(
    *,
    funnel_counts: dict[str, int] | None = None,
    week_label: str | None = None,
) -> CeoReview:
    """Assemble the weekly CEO Review scaffold.

    When ``funnel_counts`` is provided, the funnel bottleneck and its
    root-cause diagnosis are pre-filled so question 4 starts answered.
    """
    bottleneck = diagnose(funnel_counts).to_dict() if funnel_counts else None
    return CeoReview(
        week_label=week_label or _week_label(),
        generated_at=datetime.now(timezone.utc).isoformat(),
        questions=CEO_QUESTIONS,
        required_decisions=REQUIRED_DECISIONS,
        bottleneck=bottleneck,
    )


__all__ = [
    "CEO_QUESTIONS",
    "REQUIRED_DECISIONS",
    "CeoReview",
    "build_ceo_review",
]
