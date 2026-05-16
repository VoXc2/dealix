"""Governed Revenue Ops Diagnostic — deterministic diagnostic engine.

Produces the diagnostic deliverables described in
`docs/services/governed_revenue_ops_diagnostic/offer.md`:

    Revenue workflow map · CRM/source quality review · Pipeline risk map ·
    Follow-up gap analysis · Proof-of-value opportunities ·
    Recommended Sprint/Retainer

Pure logic — no sends, no scraping, no guarantee language. Every finding
carries a ``source_ref`` so it can be tied back to a client-supplied input.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

_DISCLAIMER = "Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة"


@dataclass(frozen=True)
class DiagnosticFinding:
    """A single evidence-backed diagnostic finding."""

    area: str
    summary_en: str
    summary_ar: str
    severity: str  # low | medium | high
    source_ref: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "area": self.area,
            "summary_en": self.summary_en,
            "summary_ar": self.summary_ar,
            "severity": self.severity,
            "source_ref": self.source_ref,
        }


@dataclass
class DiagnosticResult:
    """Full Governed Revenue Ops Diagnostic output."""

    engagement_id: str
    crm_quality_score: float
    findings: list[DiagnosticFinding] = field(default_factory=list)
    pipeline_risk_band: str = "unknown"
    followup_gap_pct: float = 0.0
    recommended_next: str = "revenue_intelligence_sprint"
    recommended_next_ar: str = "سبرنت ذكاء الإيراد"

    def to_dict(self) -> dict[str, Any]:
        return {
            "engagement_id": self.engagement_id,
            "crm_quality_score": self.crm_quality_score,
            "pipeline_risk_band": self.pipeline_risk_band,
            "followup_gap_pct": self.followup_gap_pct,
            "findings": [f.to_dict() for f in self.findings],
            "recommended_next": self.recommended_next,
            "recommended_next_ar": self.recommended_next_ar,
            "disclaimer": _DISCLAIMER,
        }


def _crm_quality(rows: list[dict[str, Any]]) -> tuple[float, list[DiagnosticFinding]]:
    """Score CRM/source quality from completeness + duplicates. 0-100."""
    findings: list[DiagnosticFinding] = []
    if not rows:
        return 0.0, [
            DiagnosticFinding(
                area="crm_quality",
                summary_en="No CRM rows supplied — cannot assess data quality.",
                summary_ar="لا توجد صفوف CRM — لا يمكن تقييم جودة البيانات.",
                severity="high",
                source_ref="intake:crm_export",
            )
        ]
    req = ("company_name", "stage", "owner", "amount", "last_activity_at")
    filled = sum(
        1 for r in rows for k in req if str(r.get(k) or "").strip()
    )
    completeness = filled / (len(rows) * len(req))
    names = [str(r.get("company_name") or "").strip().lower() for r in rows]
    non_empty = [n for n in names if n]
    dup_ratio = (
        1.0 - (len(set(non_empty)) / len(non_empty)) if non_empty else 0.0
    )
    score = round(100.0 * (0.7 * completeness + 0.3 * (1.0 - dup_ratio)), 2)
    if completeness < 0.7:
        findings.append(
            DiagnosticFinding(
                area="crm_quality",
                summary_en=f"CRM completeness is {completeness:.0%} — key fields missing.",
                summary_ar=f"اكتمال بيانات الـCRM {completeness:.0%} — حقول أساسية ناقصة.",
                severity="high" if completeness < 0.5 else "medium",
                source_ref="intake:crm_export#completeness",
            )
        )
    if dup_ratio > 0.05:
        findings.append(
            DiagnosticFinding(
                area="crm_quality",
                summary_en=f"Duplicate accounts detected — {dup_ratio:.0%} of rows.",
                summary_ar=f"حسابات مكررة — {dup_ratio:.0%} من الصفوف.",
                severity="medium",
                source_ref="intake:crm_export#duplicates",
            )
        )
    return score, findings


def _pipeline_risk(rows: list[dict[str, Any]]) -> tuple[str, list[DiagnosticFinding]]:
    """Classify pipeline risk from stage spread + stale accounts."""
    findings: list[DiagnosticFinding] = []
    if not rows:
        return "unknown", findings
    no_owner = sum(1 for r in rows if not str(r.get("owner") or "").strip())
    no_stage = sum(1 for r in rows if not str(r.get("stage") or "").strip())
    risk_inputs = (no_owner + no_stage) / (len(rows) * 2)
    band = "high" if risk_inputs > 0.4 else ("medium" if risk_inputs > 0.15 else "low")
    if no_stage:
        findings.append(
            DiagnosticFinding(
                area="pipeline_risk",
                summary_en=f"{no_stage} accounts have no pipeline stage.",
                summary_ar=f"{no_stage} حساب بلا مرحلة في خط الأنابيب.",
                severity="high" if band == "high" else "medium",
                source_ref="intake:crm_export#stage",
            )
        )
    if no_owner:
        findings.append(
            DiagnosticFinding(
                area="pipeline_risk",
                summary_en=f"{no_owner} accounts have no owner — accountability gap.",
                summary_ar=f"{no_owner} حساب بلا مالك — فجوة مسؤولية.",
                severity="medium",
                source_ref="intake:crm_export#owner",
            )
        )
    return band, findings


def _followup_gap(rows: list[dict[str, Any]]) -> tuple[float, list[DiagnosticFinding]]:
    """Percentage of open accounts with no recorded last activity."""
    findings: list[DiagnosticFinding] = []
    if not rows:
        return 0.0, findings
    stale = sum(1 for r in rows if not str(r.get("last_activity_at") or "").strip())
    gap = round(100.0 * stale / len(rows), 2)
    if gap > 25.0:
        findings.append(
            DiagnosticFinding(
                area="followup_gap",
                summary_en=f"{gap:.0f}% of accounts have no recorded follow-up activity.",
                summary_ar=f"{gap:.0f}% من الحسابات بلا نشاط متابعة مُسجّل.",
                severity="high" if gap > 50 else "medium",
                source_ref="intake:crm_export#last_activity",
            )
        )
    return gap, findings


def run_diagnostic(
    engagement_id: str,
    crm_rows: list[dict[str, Any]] | None = None,
    *,
    ai_usage_ungoverned: bool = False,
    has_decision_trail: bool = True,
) -> DiagnosticResult:
    """Run the Governed Revenue Ops Diagnostic over a CRM export.

    Args:
        engagement_id: the engagement this diagnostic belongs to.
        crm_rows: client-supplied CRM rows (company_name, stage, owner,
            amount, last_activity_at).
        ai_usage_ungoverned: founder/intake flag — AI used without approval
            boundaries or source rules.
        has_decision_trail: whether a decision trail currently exists.

    Returns:
        A :class:`DiagnosticResult` with evidence-backed findings and a
        recommended next step. No outcome is promised.
    """
    rows = crm_rows or []
    crm_score, crm_findings = _crm_quality(rows)
    risk_band, risk_findings = _pipeline_risk(rows)
    gap, gap_findings = _followup_gap(rows)

    findings = [*crm_findings, *risk_findings, *gap_findings]

    if ai_usage_ungoverned:
        findings.append(
            DiagnosticFinding(
                area="ai_governance",
                summary_en="AI is used without approval boundaries or source rules.",
                summary_ar="يُستخدم الذكاء الاصطناعي بلا حدود موافقة أو قواعد مصادر.",
                severity="high",
                source_ref="intake:interview#ai_usage",
            )
        )
    if not has_decision_trail:
        findings.append(
            DiagnosticFinding(
                area="decision_trail",
                summary_en="No decision trail — revenue decisions are not auditable.",
                summary_ar="لا يوجد سجل قرارات — قرارات الإيراد غير قابلة للتدقيق.",
                severity="high",
                source_ref="intake:interview#decision_trail",
            )
        )

    # Recommendation: retainer if structurally weak across multiple areas;
    # sprint otherwise. This is a recommendation, not a guaranteed outcome.
    high_count = sum(1 for f in findings if f.severity == "high")
    if high_count >= 3:
        rec, rec_ar = "governed_ops_retainer", "ريتينر التشغيل المحكوم"
    else:
        rec, rec_ar = "revenue_intelligence_sprint", "سبرنت ذكاء الإيراد"

    return DiagnosticResult(
        engagement_id=engagement_id,
        crm_quality_score=crm_score,
        findings=findings,
        pipeline_risk_band=risk_band,
        followup_gap_pct=gap,
        recommended_next=rec,
        recommended_next_ar=rec_ar,
    )
