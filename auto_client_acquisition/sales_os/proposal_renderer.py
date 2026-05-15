"""Proposal renderer — fills a Jinja2-style template (or a plain Python
format-string fallback if Jinja2 isn't installed) with engagement context.

Pattern matches existing repo style: pure-function compose, no I/O.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime, timezone
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
            "proposal_date": self.proposal_date or datetime.now(UTC).strftime("%Y-%m-%d"),
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


__all__ = ["ProposalContext", "render_proposal"]
