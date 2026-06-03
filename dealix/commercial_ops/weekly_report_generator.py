"""Weekly Business Report Generator.

Generates a comprehensive weekly business report from operational data.
Output: JSON + Markdown (Arabic + English).

Usage::

    gen = WeeklyReportGenerator()
    report = gen.generate(week_data)
    print(report.as_markdown())
    print(report.to_dict())
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any

# ---------------------------------------------------------------------------
# Data schemas
# ---------------------------------------------------------------------------


@dataclass
class WeeklyReport:
    """A compiled weekly business report."""

    week_label: str
    revenue_summary: dict[str, Any]
    lead_quality: dict[str, Any]
    content_performance: dict[str, Any]
    action_items: list[dict[str, str]]
    risk_flags: list[dict[str, str]]
    governance_decision: str
    generated_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())

    def to_dict(self) -> dict[str, Any]:
        return {
            "week_label": self.week_label,
            "revenue_summary": self.revenue_summary,
            "lead_quality": self.lead_quality,
            "content_performance": self.content_performance,
            "action_items": self.action_items,
            "risk_flags": self.risk_flags,
            "governance_decision": self.governance_decision,
            "generated_at": self.generated_at,
        }

    def as_markdown(self) -> str:
        """Render the report as bilingual Markdown."""
        lines: list[str] = []

        # ── Header ──────────────────────────────────────────────────────
        lines.append(f"# Weekly Report — {self.week_label}")
        lines.append(f"# تقرير الأسبوع — {self.week_label}")
        lines.append(f"\n_Generated: {self.generated_at}_\n")

        # ── Revenue Summary ─────────────────────────────────────────────
        rev = self.revenue_summary
        lines.append("## Revenue Summary / ملخص الإيراد\n")
        lines.append(f"- **MRR:** {rev.get('mrr_sar', 'N/A')} SAR")
        lines.append(f"  - **الإيراد الشهري المتكرر:** {rev.get('mrr_sar', 'N/A')} ريال")
        lines.append(f"- **New Deals:** {rev.get('new_deals', 0)}")
        lines.append(f"  - **صفقات جديدة:** {rev.get('new_deals', 0)}")
        lines.append(f"- **Pipeline Value:** {rev.get('pipeline_value_sar', 'N/A')} SAR")
        lines.append(f"  - **قيمة خط الأنابيب:** {rev.get('pipeline_value_sar', 'N/A')} ريال")
        lines.append(f"- **MRR Growth (WoW):** {rev.get('mrr_growth_pct', 0):.1f}%")
        lines.append(f"  - **نمو الإيراد الأسبوعي:** {rev.get('mrr_growth_pct', 0):.1f}%")
        lines.append("")

        # ── Lead Quality ────────────────────────────────────────────────
        lq = self.lead_quality
        lines.append("## Lead Quality Analysis / تحليل جودة العملاء المحتملين\n")
        lines.append(f"- **Total Leads:** {lq.get('total_leads', 0)}")
        lines.append(f"  - **إجمالي العملاء المحتملين:** {lq.get('total_leads', 0)}")
        lines.append(f"- **HOT:** {lq.get('hot', 0)} | **WARM:** {lq.get('warm', 0)} | **COOL:** {lq.get('cool', 0)} | **COLD:** {lq.get('cold', 0)}")
        lines.append(f"- **Avg Score:** {lq.get('avg_score', 0):.1f}/100")
        lines.append(f"  - **متوسط النقاط:** {lq.get('avg_score', 0):.1f}/100")
        lines.append(f"- **PDPL Compliant:** {lq.get('pdpl_compliant_pct', 0):.0f}%")
        lines.append(f"  - **الامتثال لنظام PDPL:** {lq.get('pdpl_compliant_pct', 0):.0f}%")
        lines.append("")

        # ── Content Performance ─────────────────────────────────────────
        cp = self.content_performance
        lines.append("## Content Performance / أداء المحتوى\n")
        lines.append(f"- **Posts Published:** {cp.get('posts_published', 0)}")
        lines.append(f"  - **مقالات منشورة:** {cp.get('posts_published', 0)}")
        lines.append(f"- **Total Impressions:** {cp.get('total_impressions', 0):,}")
        lines.append(f"  - **إجمالي الظهور:** {cp.get('total_impressions', 0):,}")
        lines.append(f"- **Avg Engagement Rate:** {cp.get('avg_engagement_rate_pct', 0):.1f}%")
        lines.append(f"  - **متوسط معدل التفاعل:** {cp.get('avg_engagement_rate_pct', 0):.1f}%")
        lines.append(f"- **Leads from Content:** {cp.get('leads_from_content', 0)}")
        lines.append(f"  - **عملاء محتملون من المحتوى:** {cp.get('leads_from_content', 0)}")
        lines.append("")

        # ── Action Items ────────────────────────────────────────────────
        if self.action_items:
            lines.append("## Action Items / المهام القادمة\n")
            for item in self.action_items:
                priority = item.get("priority", "medium")
                lines.append(f"- [{priority.upper()}] {item.get('action_en', '')} / {item.get('action_ar', '')}")
                if item.get("owner"):
                    lines.append(f"  - Owner: {item['owner']}")
                if item.get("due"):
                    lines.append(f"  - Due: {item['due']}")
            lines.append("")

        # ── Risk Flags ──────────────────────────────────────────────────
        if self.risk_flags:
            lines.append("## Risk Flags / تحذيرات المخاطر\n")
            for flag in self.risk_flags:
                level = flag.get("level", "medium")
                lines.append(
                    f"- **[{level.upper()}]** {flag.get('risk_en', '')} / {flag.get('risk_ar', '')}"
                )
            lines.append("")

        # ── Footer ──────────────────────────────────────────────────────
        lines.append("---")
        lines.append(f"_Governance: {self.governance_decision}_")
        lines.append("_Estimated outcomes are not guaranteed. / النتائج التقديرية ليست مضمونة._")

        return "\n".join(lines)


# ---------------------------------------------------------------------------
# Generator
# ---------------------------------------------------------------------------


class WeeklyReportGenerator:
    """Generates a WeeklyReport from raw week data dict.

    The ``week_data`` dict supports the following keys (all optional with
    sensible defaults so partial data produces a valid report):

    revenue:
      mrr_sar, mrr_prev_sar, new_deals, pipeline_value_sar

    leads:
      total_leads, hot, warm, cool, cold, avg_score, pdpl_compliant_pct

    content:
      posts_published, total_impressions, avg_engagement_rate_pct,
      leads_from_content

    action_items: list[{action_en, action_ar, priority, owner?, due?}]
    risk_flags: list[{risk_en, risk_ar, level}]
    """

    def generate(self, week_data: dict[str, Any]) -> WeeklyReport:
        """Compile a WeeklyReport from week_data.

        :param week_data: Raw weekly operational data dict.
        :returns: A :class:`WeeklyReport` with bilingual content.
        """
        now = datetime.now(UTC)
        week_label = week_data.get("week_label") or now.strftime("W%V %Y")

        revenue = self._build_revenue(week_data)
        lead_quality = self._build_lead_quality(week_data)
        content = self._build_content(week_data)
        action_items = self._build_action_items(week_data, revenue, lead_quality)
        risk_flags = self._build_risk_flags(week_data, revenue, lead_quality)
        gov = self._governance_decision(risk_flags)

        return WeeklyReport(
            week_label=week_label,
            revenue_summary=revenue,
            lead_quality=lead_quality,
            content_performance=content,
            action_items=action_items,
            risk_flags=risk_flags,
            governance_decision=gov,
        )

    # ── Private builders ────────────────────────────────────────────────────

    def _build_revenue(self, d: dict[str, Any]) -> dict[str, Any]:
        mrr = float(d.get("mrr_sar", 0))
        mrr_prev = float(d.get("mrr_prev_sar", mrr))
        growth_pct = ((mrr - mrr_prev) / mrr_prev * 100) if mrr_prev else 0.0
        return {
            "mrr_sar": mrr,
            "mrr_prev_sar": mrr_prev,
            "mrr_growth_pct": round(growth_pct, 2),
            "new_deals": int(d.get("new_deals", 0)),
            "pipeline_value_sar": float(d.get("pipeline_value_sar", 0)),
            "label_ar": "ملخص الإيراد",
            "label_en": "Revenue Summary",
        }

    def _build_lead_quality(self, d: dict[str, Any]) -> dict[str, Any]:
        hot = int(d.get("hot", 0))
        warm = int(d.get("warm", 0))
        cool = int(d.get("cool", 0))
        cold = int(d.get("cold", 0))
        total = int(d.get("total_leads", hot + warm + cool + cold))
        return {
            "total_leads": total,
            "hot": hot,
            "warm": warm,
            "cool": cool,
            "cold": cold,
            "avg_score": float(d.get("avg_score", 0)),
            "pdpl_compliant_pct": float(d.get("pdpl_compliant_pct", 100)),
            "label_ar": "جودة العملاء المحتملين",
            "label_en": "Lead Quality",
        }

    def _build_content(self, d: dict[str, Any]) -> dict[str, Any]:
        return {
            "posts_published": int(d.get("posts_published", 0)),
            "total_impressions": int(d.get("total_impressions", 0)),
            "avg_engagement_rate_pct": float(d.get("avg_engagement_rate_pct", 0)),
            "leads_from_content": int(d.get("leads_from_content", 0)),
            "label_ar": "أداء المحتوى",
            "label_en": "Content Performance",
        }

    def _build_action_items(
        self,
        d: dict[str, Any],
        revenue: dict[str, Any],
        leads: dict[str, Any],
    ) -> list[dict[str, str]]:
        items: list[dict[str, str]] = list(d.get("action_items", []))

        # Auto-generated action items based on signals.
        if revenue["mrr_growth_pct"] < 5:
            items.append(
                {
                    "action_en": "Review pipeline conversion — MRR growth below 5% target.",
                    "action_ar": "مراجعة تحويل خط الأنابيب — نمو الإيراد دون هدف 5%.",
                    "priority": "high",
                    "owner": "founder",
                }
            )
        if leads["hot"] > 0:
            items.append(
                {
                    "action_en": f"Follow up with {leads['hot']} HOT lead(s) within 24 hours.",
                    "action_ar": f"المتابعة مع {leads['hot']} عميل(عملاء) ساخن خلال 24 ساعة.",
                    "priority": "high",
                    "owner": "founder",
                }
            )
        if leads["pdpl_compliant_pct"] < 90:
            items.append(
                {
                    "action_en": "Collect PDPL consent for leads missing approval.",
                    "action_ar": "جمع موافقة PDPL للعملاء الناقصة موافقتهم.",
                    "priority": "medium",
                    "owner": "ops",
                }
            )
        return items

    def _build_risk_flags(
        self,
        d: dict[str, Any],
        revenue: dict[str, Any],
        leads: dict[str, Any],
    ) -> list[dict[str, str]]:
        flags: list[dict[str, str]] = list(d.get("risk_flags", []))

        if revenue["mrr_growth_pct"] < 0:
            flags.append(
                {
                    "risk_en": "MRR declined week-over-week — investigate churn.",
                    "risk_ar": "انخفض الإيراد الشهري المتكرر — تحقق من الإلغاءات.",
                    "level": "high",
                }
            )
        if leads["pdpl_compliant_pct"] < 80:
            flags.append(
                {
                    "risk_en": "PDPL compliance below 80% — data use restrictions apply.",
                    "risk_ar": "الامتثال لـ PDPL أقل من 80% — قيود استخدام البيانات سارية.",
                    "level": "high",
                }
            )
        if revenue["pipeline_value_sar"] < revenue["mrr_sar"] * 2:
            flags.append(
                {
                    "risk_en": "Pipeline coverage ratio below 2x MRR — prospecting needed.",
                    "risk_ar": "نسبة تغطية خط الأنابيب دون 2x إيراد — يلزم التنقيب.",
                    "level": "medium",
                }
            )
        return flags

    def _governance_decision(self, risk_flags: list[dict[str, str]]) -> str:
        high_risks = [f for f in risk_flags if f.get("level") == "high"]
        if high_risks:
            return "ALLOW_WITH_REVIEW"
        return "ALLOW"


__all__ = ["WeeklyReport", "WeeklyReportGenerator"]
