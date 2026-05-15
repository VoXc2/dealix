"""Proposal renderer — fills a Jinja2-style template (or a plain Python
format-string fallback if Jinja2 isn't installed) with engagement context.

Pattern matches existing repo style: pure-function compose, no I/O.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from string import Template
from typing import Any


_REPO_ROOT = Path(__file__).resolve().parent.parent.parent


@dataclass
class ProposalContext:
    customer_name: str
    customer_handle: str
    sector: str
    city: str
    engagement_id: str
    price_sar: int = 499
    delivery_days: int = 7
    proof_score_target: int = 80
    source_passport_required: bool = True
    exclusions: tuple[str, ...] = (
        "no_scraping",
        "no_cold_whatsapp_automation",
        "no_linkedin_automation",
        "no_fake_proof",
        "no_guaranteed_sales_claims",
        "no_pii_in_logs",
        "no_source_less_answers",
        "no_external_action_without_approval",
        "no_agent_without_identity",
        "no_project_without_proof_pack",
        "no_project_without_capital_asset",
    )
    retainer_offer_after: str = "managed_revenue_ops_2999_sar_per_month"
    proposal_date: str = ""

    def to_mapping(self) -> dict[str, Any]:
        return {
            "customer_name": self.customer_name,
            "customer_handle": self.customer_handle,
            "sector": self.sector,
            "city": self.city,
            "engagement_id": self.engagement_id,
            "price_sar": self.price_sar,
            "delivery_days": self.delivery_days,
            "proof_score_target": self.proof_score_target,
            "source_passport_required": self.source_passport_required,
            "exclusions_list": ", ".join(self.exclusions),
            "retainer_offer_after": self.retainer_offer_after,
            "proposal_date": self.proposal_date or datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        }


_FALLBACK_TEMPLATE = """# Revenue Intelligence Sprint — Proposal

**Customer:** $customer_name ($customer_handle)
**Sector:** $sector | **City:** $city
**Engagement:** $engagement_id
**Date:** $proposal_date

## Scope
- 7-day Revenue Intelligence Sprint
- Source Passport agreed before any AI use
- Data Quality Score + dedupe + account scoring (top 10)
- Bilingual AR + EN draft pack
- Governance Runtime review on every output
- 14-section Proof Pack
- Capital asset registered for reuse

## Price
**$price_sar SAR** — 50% on acceptance, 50% on Proof Pack delivery.

## Delivery
$delivery_days days from kickoff. Proof score target: ≥ $proof_score_target / 100.

## Exclusions (Dealix non-negotiables)
$exclusions_list

## After this sprint
If proof_score ≥ 80 and adoption_score ≥ 70, we offer **$retainer_offer_after**.

---

# عرض مشروع Revenue Intelligence

**العميل:** $customer_name ($customer_handle)
**القطاع:** $sector | **المدينة:** $city
**رقم المشروع:** $engagement_id
**التاريخ:** $proposal_date

## النطاق
- Sprint 7 أيام لذكاء الإيراد
- Source Passport متفق عليه قبل أي استخدام AI
- درجة جودة بيانات + إزالة تكرار + تصنيف 10 حسابات
- مسوّدات ثنائية اللغة (عربي + إنجليزي)
- مراجعة Governance على كل مخرج
- Proof Pack من 14 قسم
- أصل قابل لإعادة الاستخدام يُسجّل في Capital Ledger

## السعر
**$price_sar ريال سعودي** — 50% عند القبول، 50% عند تسليم Proof Pack.

## التسليم
$delivery_days أيام من الانطلاق. الهدف: درجة Proof ≥ $proof_score_target / 100.

## ما لا نقبله (غير قابل للتفاوض)
$exclusions_list

## بعد المشروع
إذا تجاوز proof_score 80 و adoption_score 70، نعرض **$retainer_offer_after**.

---

_Estimated outcomes are not guaranteed outcomes / النتائج التقديرية ليست نتائج مضمونة._
"""


_ENTERPRISE_EXCLUSIONS: tuple[str, ...] = (
    "no_live_send",
    "no_live_charge",
    "no_cold_whatsapp_automation",
    "no_linkedin_automation",
    "no_scraping",
    "no_fake_proof",
    "no_fake_revenue",
    "no_guaranteed_sales_claims",
    "no_pii_in_logs",
    "no_external_action_without_approval",
)


@dataclass
class EnterpriseProposalContext:
    """Context for a tiered enterprise transformation proposal."""

    customer_name: str
    customer_handle: str
    sector: str
    city: str
    engagement_id: str
    offering: Any  # EnterpriseOffering
    recommended_tier_id: str = ""
    proposal_date: str = ""

    def to_mapping(self) -> dict[str, Any]:
        o = self.offering
        return {
            "customer_name": self.customer_name,
            "customer_handle": self.customer_handle,
            "sector": self.sector,
            "city": self.city,
            "engagement_id": self.engagement_id,
            "offering_name_ar": o.name_ar,
            "offering_name_en": o.name_en,
            "offering_summary_ar": o.summary_ar,
            "offering_summary_en": o.summary_en,
            "workstreams": list(o.workstreams),
            "tiers": [t.model_dump() for t in o.tiers],
            "recommended_tier_id": self.recommended_tier_id,
            "exclusions": list(_ENTERPRISE_EXCLUSIONS),
            "proposal_date": self.proposal_date
            or datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        }


def render_enterprise_proposal(
    context: EnterpriseProposalContext, template_path: Path | None = None
) -> str:
    """Render a tiered enterprise transformation proposal as markdown.

    Uses `templates/PROPOSAL_ENTERPRISE_TRANSFORMATION.md.j2` (Jinja2 — loops
    over the pricing tiers). Falls back to a Python-composed proposal if the
    template or Jinja2 is unavailable.
    """
    mapping = context.to_mapping()
    path = template_path or (
        _REPO_ROOT / "templates" / "PROPOSAL_ENTERPRISE_TRANSFORMATION.md.j2"
    )
    if path.exists():
        try:
            import jinja2

            env = jinja2.Environment(
                autoescape=False, keep_trailing_newline=True, trim_blocks=True
            )
            return env.from_string(path.read_text(encoding="utf-8")).render(**mapping)
        except ImportError:
            pass
    return _compose_enterprise_fallback(mapping)


def _compose_enterprise_fallback(m: dict[str, Any]) -> str:
    lines: list[str] = [
        f"# {m['offering_name_en']} — Enterprise Proposal",
        "",
        f"**Customer:** {m['customer_name']} ({m['customer_handle']})",
        f"**Sector:** {m['sector']} | **City:** {m['city']}",
        f"**Engagement:** {m['engagement_id']} | **Date:** {m['proposal_date']}",
        "",
        m["offering_summary_en"],
        "",
        "Dealix does not sell a chatbot — we build a governed AI operating layer.",
        "",
        "## Workstreams in scope",
    ]
    lines += [f"- {ws}" for ws in m["workstreams"]]
    lines += ["", "## Pricing tiers (estimates)", ""]
    for tier in m["tiers"]:
        rec = " — recommended" if tier["id"] == m["recommended_tier_id"] else ""
        lines.append(f"### {tier['name_en']}{rec}")
        lines.append(f"- Setup: {tier['setup_sar']:,.0f} SAR (one-time)")
        lines.append(f"- Retainer: {tier['monthly_sar']:,.0f} SAR / month")
        lines.append(f"- Minimum engagement: {tier['min_duration_days']} days")
        lines += [f"  - {d}" for d in tier["deliverables"]]
        lines.append(f"- Commitment: {tier['kpi_commitment_en']}")
        lines.append("")
    lines.append("## Governance — Dealix non-negotiables")
    lines += [f"- {ex}" for ex in m["exclusions"]]
    lines += [
        "",
        "_Estimated outcomes are not guaranteed outcomes /"
        " النتائج التقديرية ليست نتائج مضمونة._",
    ]
    return "\n".join(lines)


def render_proposal(context: ProposalContext, template_path: Path | None = None) -> str:
    """Render proposal markdown. Reads `templates/PROPOSAL_REVENUE_INTELLIGENCE_SPRINT.md.j2`
    if present; otherwise falls back to the inline template above.

    The Jinja2 template uses `{{ var }}` syntax. For portability we accept
    both Jinja2 (when available) and Python Template ($var) substitution.
    """
    mapping = context.to_mapping()
    path = template_path or (_REPO_ROOT / "templates" / "PROPOSAL_REVENUE_INTELLIGENCE_SPRINT.md.j2")
    if path.exists():
        raw = path.read_text(encoding="utf-8")
        try:
            import jinja2
            env = jinja2.Environment(
                autoescape=False, keep_trailing_newline=True, trim_blocks=True
            )
            return env.from_string(raw).render(**mapping)
        except ImportError:
            # Jinja2 not installed — convert {{ var }} to $var for Template.
            converted = raw
            for key in mapping:
                converted = converted.replace("{{ " + key + " }}", "$" + key)
                converted = converted.replace("{{" + key + "}}", "$" + key)
            return Template(converted).safe_substitute(mapping)

    return Template(_FALLBACK_TEMPLATE).safe_substitute(mapping)


__all__ = [
    "EnterpriseProposalContext",
    "ProposalContext",
    "render_enterprise_proposal",
    "render_proposal",
]
