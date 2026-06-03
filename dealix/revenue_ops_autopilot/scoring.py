"""Deterministic lead scoring aligned with Founder Operating Order."""

from __future__ import annotations

from typing import Any

from dealix.revenue_ops_autopilot.schemas import LeadStage

_DM_KEYWORDS = (
    "founder",
    "ceo",
    "coo",
    "cro",
    "chief",
    "head of ops",
    "operations director",
    "vp sales",
    "مدير عام",
    "الرئيس التنفيذي",
    "رئيس عمليات",
)

_STUDENT_HINTS = (
    "student",
    "fresh graduate",
    "job seeker",
    "بحث عن وظيفة",
    "طالب",
)


def compute_lead_score(fields: dict[str, Any]) -> tuple[int, dict[str, int]]:
    """Returns (total, breakdown) using rubric §8."""
    bd: dict[str, int] = {}
    role = str(fields.get("role") or fields.get("title") or "").lower()
    company = str(fields.get("company") or "").strip().lower()
    industry = str(fields.get("industry") or "").lower()
    country = str(fields.get("country") or fields.get("region") or "").lower()
    ai_usage = str(fields.get("ai_usage") or fields.get("ai") or "").lower()
    urgency = str(fields.get("urgency") or "").lower()
    budget = str(fields.get("budget_range") or fields.get("budget") or "").lower()
    pain = str(fields.get("pain") or fields.get("message") or "").lower()
    notes = str(fields.get("notes") or "").lower()
    source = str(fields.get("source") or "").lower()

    blob = " ".join((role, industry, notes, pain, source))

    if any(k in role for k in _DM_KEYWORDS):
        bd["decision_maker"] = 4
    elif any(k in blob for k in _DM_KEYWORDS):
        bd["decision_maker_context"] = 2

    if company and company not in {"", "personal", "-", "n/a"}:
        bd["b2b_company"] = 3
    elif not company.strip():
        bd["no_company"] = -4

    crm_signals = ("crm", "salesforce", "hubspot", "zoho", "pipeline", "deals")
    if any(sig in blob for sig in crm_signals + ("pipeline process",)):
        bd["crm_workflow"] = 3

    ai_signals = (
        "ai",
        "llm",
        "automation",
        "agent",
        "chatgpt",
        " الذكاء الاصطناعي",
        "أتمتة",
    )
    if any(sig in blob or sig in ai_usage for sig in ai_signals):
        bd["uses_or_plans_ai"] = 3

    gcc = ("saudi", "ksa", "gcc", "uae", "dubai", "qatar", "bahrain", "kuwait", "عمان")
    if any(g in country for g in gcc) or "السعودية" in blob:
        bd["gcc"] = 2

    if any(u in urgency for u in ("30", "ثلاثين", "شهر", "اسبوعين", "two week", "asap")):
        bd["urgency_30d"] = 2

    budget_pos = ("5000", "5k", "10000", "10k", "15000", "15k", "سار", "sar", "riyal")
    if any(b in budget for b in budget_pos):
        bd["budget_5k_plus"] = 2

    partner_hit = ("partner", "agency", "consultant", "implementation", "referral")
    if any(k in blob for k in partner_hit):
        bd["partner_angle"] = 2

    if any(s in blob for s in _STUDENT_HINTS):
        bd["student_seeker"] = -3

    vague = len(pain.split()) < 4 and len(blob) < 40
    if vague and bd.get("b2b_company", 0) <= 0:
        bd["vague_curiosity"] = -3
    elif vague:
        bd["vague_curiosity"] = -2

    unclear_workflow = not bd.get("crm_workflow") and not bd.get("uses_or_plans_ai")
    if unclear_workflow and bd.get("b2b_company", 0) > 0:
        bd["unclear_workflow_pain"] = -2

    total = sum(bd.values())
    return total, bd


def suggested_stage_from_score(
    *,
    score: int,
    is_partner_candidate: bool = False,
) -> LeadStage:
    from dealix.revenue_ops_autopilot.config_loader import routing_thresholds

    th = routing_thresholds()
    if is_partner_candidate:
        return "partner_candidate"
    if score >= th["qualified_a_min"]:
        return "qualified_A"
    if score >= th["qualified_b_min"]:
        return "qualified_B"
    if score >= th["nurture_min"]:
        return "nurture"
    # Archive / ignore (< 6)
    return "closed_lost"
