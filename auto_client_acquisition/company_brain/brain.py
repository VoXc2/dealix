"""CompanyBrain — composes service activation, role briefs, daily loop,
weekly scorecard, reliability matrix, and agent governance into one
structured snapshot of the company. No LLM, no network."""
from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class CompanyBrain(BaseModel):
    """A read-only snapshot of the company state, composed from
    existing signals. Used by founder dashboards + role briefs +
    public-facing system overview."""

    model_config = ConfigDict(extra="forbid")

    schema_version: int = 1
    generated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    company_name: str = "Dealix"
    mission_ar: str = (
        "نمكّن الأعمال السعوديّة من تشغيل عمليّاتها التجاريّة بأمان "
        "وكفاءة عبر منصّة آمنة قابلة للقياس."
    )
    mission_en: str = (
        "We help Saudi B2B businesses run their revenue operations "
        "with safety, accountability, and measurable outcomes."
    )
    services_summary: dict[str, int] = Field(default_factory=dict)
    agents_summary: dict[str, int] = Field(default_factory=dict)
    current_priorities: list[str] = Field(default_factory=list)
    health_overall: str = "unknown"
    promotion_candidates: list[str] = Field(default_factory=list)
    guardrails: dict[str, bool] = Field(default_factory=lambda: {
        "no_live_send": True,
        "no_scraping": True,
        "no_cold_outreach": True,
        "approval_required_for_external_actions": True,
    })

    def as_dict(self) -> dict[str, Any]:
        return self.model_dump(mode="json")


def _safe(fn, default):
    try:
        return fn()
    except BaseException:
        return default


def _services_summary() -> dict[str, int]:
    from auto_client_acquisition.self_growth_os import service_activation_matrix
    return service_activation_matrix.counts()


def _agents_summary() -> dict[str, int]:
    """Count agents per autonomy level."""
    from auto_client_acquisition.agent_governance import list_agents
    by_level: dict[str, int] = {}
    for spec in list_agents():
        level = str(spec.get("max_autonomy", "unknown")) if isinstance(spec, dict) else str(getattr(spec, "max_autonomy", "unknown"))
        by_level[level] = by_level.get(level, 0) + 1
    return by_level


def _current_priorities() -> list[str]:
    from auto_client_acquisition.self_growth_os import daily_growth_loop
    loop = daily_growth_loop.build_today()
    out: list[str] = []
    for d in (loop.get("decisions") or [])[:3]:
        title = (
            d.get("title_ar")
            or d.get("title")
            or d.get("title_en")
            or ""
        )
        if title:
            out.append(str(title)[:120])
    return out


def _health_overall() -> str:
    from auto_client_acquisition.reliability_os import build_health_matrix
    return str(build_health_matrix().get("overall_status", "unknown"))


def _promotion_candidates() -> list[str]:
    from auto_client_acquisition.self_growth_os import service_activation_matrix
    cands = service_activation_matrix.candidates_for_promotion() or []
    return [getattr(c, "service_id", str(c)) for c in cands[:3]]


def build_company_brain() -> CompanyBrain:
    """Compose the company brain from currently-shipped signals.

    Defensive: any failing component degrades to its default rather
    than crashing the whole snapshot. Callers can rely on a result
    every time."""
    return CompanyBrain(
        services_summary=_safe(_services_summary, default={}),
        agents_summary=_safe(_agents_summary, default={}),
        current_priorities=_safe(_current_priorities, default=[]),
        health_overall=_safe(_health_overall, default="unknown"),
        promotion_candidates=_safe(_promotion_candidates, default=[]),
    )
