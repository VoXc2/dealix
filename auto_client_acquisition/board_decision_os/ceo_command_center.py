"""CEO Command Center — canonical surfaces for weekly board-style review."""

from __future__ import annotations

from auto_client_acquisition.board_decision_os.schemas import CEOSignals, CEOTopDecision

CEO_COMMAND_CENTER_SURFACES: tuple[str, ...] = (
    "top_5_decisions",
    "revenue_quality",
    "proof_strength",
    "retainer_opportunities",
    "client_risks",
    "productization_queue",
    "governance_risks",
    "bad_revenue_to_reject",
    "business_unit_maturity",
    "venture_signals",
)


def ceo_command_center_coverage_score(surfaces_tracked: frozenset[str]) -> int:
    if not CEO_COMMAND_CENTER_SURFACES:
        return 0
    n = sum(1 for s in CEO_COMMAND_CENTER_SURFACES if s in surfaces_tracked)
    return (n * 100) // len(CEO_COMMAND_CENTER_SURFACES)


def build_top_decisions(signals: CEOSignals, *, limit: int = 5) -> list[CEOTopDecision]:
    """Return up to `limit` decisions sorted by fixed priority rules (v1)."""
    candidates: list[CEOTopDecision] = []

    if signals.bad_revenue_unsafe_channel or signals.cold_whatsapp_automation_request:
        candidates.append(
            CEOTopDecision(
                priority=1,
                decision="REJECT_BAD_REVENUE",
                target="unsafe_channel_request",
                reason_ar="طلب قناة أو أتمتة غير آمنة أو محظورة حسب سياسة Dealix.",
                reason_en="Unsafe or prohibited channel/automation per Dealix policy.",
            )
        )

    if (
        signals.proof_score >= 80
        and signals.adoption_score >= 70
        and signals.monthly_workflow_exists
    ):
        candidates.append(
            CEOTopDecision(
                priority=2,
                decision="OFFER_RETAINER",
                target="top_client_motion",
                reason_ar="دليل قوي وتبنٍ جيد وتكرار شهري في سير العمل.",
                reason_en="Strong proof, adoption, and recurring monthly workflow.",
            )
        )

    if signals.approval_friction_clients >= 4:
        candidates.append(
            CEOTopDecision(
                priority=3,
                decision="BUILD_MVP",
                target="Approval Center",
                reason_ar="احتكاك موافقات متكرر عبر عدة عملاء.",
                reason_en="Repeated approval friction across multiple clients.",
            )
        )

    if signals.sprint_repeat_sales >= 3 and signals.sprint_avg_proof >= 80:
        candidates.append(
            CEOTopDecision(
                priority=4,
                decision="RAISE_PRICE",
                target="Revenue Intelligence Sprint",
                reason_ar="تكرار بيع وتسليم مع دليل متوسط مرتفع.",
                reason_en="Repeat sales with high average proof score.",
            )
        )

    if signals.repeated_sector_pattern:
        candidates.append(
            CEOTopDecision(
                priority=5,
                decision="CREATE_PLAYBOOK",
                target="sector_pattern",
                reason_ar="نمط قطاع متكرر يستحق playbook موحّد.",
                reason_en="Repeated sector pattern warrants a unified playbook.",
            )
        )

    candidates.sort(key=lambda d: (d.priority, d.decision))
    return candidates[:limit]
