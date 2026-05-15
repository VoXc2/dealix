"""Planner agent — deterministic keyword routing.

Inspired by AutoGen's planner. Pure local: maps goal keywords to a
canonical agent set. ComplianceGuardAgent is ALWAYS appended — the
veto agent runs on every plan.
"""
from __future__ import annotations

from auto_client_acquisition.ai_workforce_v10.schemas import PlannerOutput

_KEYWORD_MAP: tuple[tuple[tuple[str, ...], list[str]], ...] = (
    (
        ("lead", "leads", "intake", "qualify", "qualification"),
        ["CompanyBrainAgent", "SalesStrategistAgent", "SaudiCopyAgent"],
    ),
    (
        ("growth", "scaling", "scale", "expand"),
        ["MarketRadarAgent", "SalesStrategistAgent"],
    ),
    (
        ("delivery", "deliver", "execution", "fulfill"),
        ["DeliveryFactoryAgent", "ServiceQualityAgent"],
    ),
    (
        ("brand", "content", "copy", "post"),
        ["SaudiCopyAgent", "DesignOpsAgent"],
    ),
    (
        ("partner", "partnership", "alliance"),
        ["PartnerScoutAgent", "SalesStrategistAgent"],
    ),
    (
        ("risk", "audit", "compliance"),
        ["ComplianceGuardAgent", "RiskAuditorAgent"],
    ),
)


def _match(text: str) -> list[str]:
    seen: list[str] = []
    lc = text.lower()
    for keywords, agents in _KEYWORD_MAP:
        if any(k in lc for k in keywords):
            for a in agents:
                if a not in seen:
                    seen.append(a)
    return seen


def run_planner(
    goal_ar: str,
    goal_en: str,
    available_agents: list[str] | None = None,
) -> PlannerOutput:
    """Pick agents for the goal. ComplianceGuardAgent is always last."""
    pool = list(available_agents or [])
    keyword_text = f"{goal_ar} {goal_en}"
    matched = _match(keyword_text)

    # Default fallback: minimal triage trio
    if not matched:
        matched = ["CompanyBrainAgent", "SalesStrategistAgent"]

    # If a pool was supplied, intersect; otherwise trust the matched set.
    if pool:
        matched = [m for m in matched if m in pool]

    # ComplianceGuardAgent is always appended — never skipped.
    if "ComplianceGuardAgent" not in matched:
        matched.append("ComplianceGuardAgent")

    rationale_ar = (
        f"تم اختيار {len(matched)} وكيل بناءً على كلمات الهدف. "
        "ComplianceGuardAgent دائم لضمان عدم الإرسال المباشر."
    )
    rationale_en = (
        f"Selected {len(matched)} agents from goal keywords; "
        "ComplianceGuardAgent always included as final veto."
    )
    plan = [{"step": i + 1, "agent_id": a} for i, a in enumerate(matched)]

    return PlannerOutput(
        assigned_agents=matched,
        task_plan=plan,
        rationale_ar=rationale_ar,
        rationale_en=rationale_en,
    )
