"""Agent decision gate — checklist before approving a new agent."""

from __future__ import annotations

from auto_client_acquisition.board_decision_os.schemas import AgentGateInput, AgentGateResult

_REQUIRED_FORBIDDEN = (
    "cold_whatsapp",
    "scrape",
    "send_messages",
)


def evaluate_agent_gate(inp: AgentGateInput) -> AgentGateResult:
    reasons_ar: list[str] = []
    reasons_en: list[str] = []

    forbidden_lower = [x.lower() for x in inp.forbidden_actions]
    for token in _REQUIRED_FORBIDDEN:
        if not any(token in f for f in forbidden_lower):
            reasons_ar.append(f"يجب أن تتضمن قائمة الممنوعات إشارة صريحة إلى: {token}")
            reasons_en.append(f"forbidden_actions must explicitly cover '{token}'")

    if inp.autonomy_level > 3:
        reasons_ar.append("مستوى الاستقلالية أعلى من 3 غير مسموح في MVP.")
        reasons_en.append("autonomy_level > 3 is not allowed in MVP.")

    if not inp.audit_required:
        reasons_ar.append("يجب تفعيل التدقيق (audit_required=true).")
        reasons_en.append("audit_required must be true.")

    if len(inp.allowed_tools) == 0:
        reasons_ar.append("قائمة الأدوات المسموحة فارغة.")
        reasons_en.append("allowed_tools is empty.")

    approved = len(reasons_ar) == 0
    return AgentGateResult(approved=approved, reasons_ar=reasons_ar, reasons_en=reasons_en)
