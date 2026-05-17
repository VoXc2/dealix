"""Layer 4 — Evidence layer / the 7 No-Scale Conditions.

These are the hard pre-conditions for scaling (ads, affiliates, hiring,
new product). Every condition must be satisfied. A condition whose metric
is unknown is ``satisfied=None`` — which blocks scaling, because the
Assurance System will not green-light growth on missing evidence.
"""
from __future__ import annotations

from auto_client_acquisition.assurance_os.adapters import ApprovalAdapter
from auto_client_acquisition.assurance_os.models import (
    AssuranceInputs,
    HealthScore,
    NoScaleCondition,
)


def _fmt(value: object) -> str:
    return "unknown" if value is None else str(value)


def evaluate_no_scale_conditions(
    inputs: AssuranceInputs, health: HealthScore
) -> list[NoScaleCondition]:
    """Evaluate all 7 no-scale conditions."""
    conditions: list[NoScaleCondition] = []

    # 1 — Full Ops Health >= 75 with no unknown component.
    if health.unknown_components:
        c1_ok: bool | None = None
        c1_actual = f"{health.total} (incomplete: {len(health.unknown_components)} unknown)"
    else:
        c1_ok = health.total >= 75.0
        c1_actual = str(health.total)
    conditions.append(NoScaleCondition(
        "full_ops_health", "Full Ops Health >= 75", "صحة العمليات >= 75",
        ">= 75", c1_actual, c1_ok,
    ))

    # 2 — Approval compliance = 100%.
    acp = inputs.approval_compliance_pct
    conditions.append(NoScaleCondition(
        "approval_compliance", "Approval compliance = 100%", "الالتزام بالموافقات = 100%",
        "= 100%", _fmt(acp), None if acp is None else acp >= 100.0,
    ))

    # 3 — High-risk auto-send = 0 (read live from the approval store).
    stats = ApprovalAdapter().live_stats()
    if stats.is_known:
        hras = stats.value["high_risk_auto_send"]
        c3_ok: bool | None = hras == 0
        c3_actual = str(hras)
    else:
        c3_ok = None
        c3_actual = "unknown"
    conditions.append(NoScaleCondition(
        "high_risk_auto_send", "High-risk auto-send = 0", "الإرسال الآلي عالي الخطورة = 0",
        "= 0", c3_actual, c3_ok,
    ))

    # 4 — Lead scoring coverage = 100%.
    lsc = inputs.lead_scoring_coverage_pct
    conditions.append(NoScaleCondition(
        "lead_scoring_coverage", "Lead scoring coverage = 100%", "تغطية تقييم العملاء = 100%",
        "= 100%", _fmt(lsc), None if lsc is None else lsc >= 100.0,
    ))

    # 5 — Evidence completeness >= 90%.
    evc = inputs.evidence_completeness_pct
    conditions.append(NoScaleCondition(
        "evidence_completeness", "Evidence completeness >= 90%", "اكتمال الأدلة >= 90%",
        ">= 90%", _fmt(evc), None if evc is None else evc >= 90.0,
    ))

    # 6 — Support high-risk escalation = 100%.
    she = inputs.support_high_risk_escalation_pct
    conditions.append(NoScaleCondition(
        "support_high_risk_escalation", "Support high-risk escalation = 100%",
        "تصعيد الدعم عالي الخطورة = 100%",
        "= 100%", _fmt(she), None if she is None else she >= 100.0,
    ))

    # 7 — Affiliate payout before payment = 0.
    apb = inputs.affiliate_payout_before_payment_count
    conditions.append(NoScaleCondition(
        "affiliate_payout_before_payment", "Affiliate payout before payment = 0",
        "صرف عمولة قبل الدفع = 0",
        "= 0", _fmt(apb), None if apb is None else apb == 0,
    ))

    return conditions
