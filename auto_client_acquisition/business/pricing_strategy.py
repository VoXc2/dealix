"""Pricing tiers, plan recommendation, performance fees, ROI estimates."""

from __future__ import annotations

from typing import Any, Literal

PlanKey = Literal[
    "governed_revenue_ai_ops_diagnostic",
    "revenue_intelligence_sprint",
    "governed_ops_retainer",
]


def get_pricing_tiers() -> dict[str, Any]:
    """Governed offers ladder (SAR) aligned with Dealix strategic doctrine."""
    return {
        "currency": "SAR",
        "category_en": "Governed Revenue + AI Workflows Operating Layer",
        "positioning_en": "We do not sell AI automation; we sell governed execution.",
        "entry_offer_en": "7-Day Governed Revenue & AI Ops Diagnostic",
        "tiers": [
            {
                "key": "governed_revenue_ai_ops_diagnostic",
                "name_ar": "تشخيص تشغيل الإيراد والذكاء الاصطناعي المحكوم (7 أيام)",
                "target": "B2B teams with AI/revenue workflow noise",
                "price_packages_sar": {
                    "starter": 4999,
                    "standard": 9999,
                    "executive": 15000,
                    "enterprise": 25000,
                },
                "includes": [
                    "Revenue workflow map",
                    "CRM/source quality review",
                    "approval boundary review",
                    "evidence trail review",
                    "top 3 governed value decisions",
                    "decision passport + proof pack",
                ],
            },
            {
                "key": "revenue_intelligence_sprint",
                "name_ar": "Revenue Intelligence Sprint",
                "target": "Post-diagnostic workflow execution",
                "price_starting_sar": 25000,
                "sell_condition": "Only after paid diagnostic confirms clear workflow opportunity",
                "includes": [
                    "Workflow implementation with controls",
                    "governed AI/revenue execution playbook",
                    "proof of value checkpoint",
                ],
            },
            {
                "key": "governed_ops_retainer",
                "name_ar": "Governed Ops Retainer",
                "target": "Teams with recurring governed workflow needs",
                "price_monthly_sar_range": [4999, 15000],
                "enterprise_monthly_sar_range": [15000, 35000],
                "sell_condition": "Only after repeated monthly workflow evidence",
                "includes": [
                    "approval queue operations",
                    "evidence ledger maintenance",
                    "continuous proof packs",
                    "policy and risk updates",
                ],
            },
        ],
        "discount_policy": {
            "default": "no_discount_without_value_exchange",
            "accepted_exchanges": [
                "testimonial_permission",
                "referral_intro",
                "faster_payment_terms",
                "public_anonymous_case_permission",
                "partner_intro",
            ],
        },
    }


def recommend_plan(
    *,
    company_size: str,
    monthly_budget_sar: float,
    goal: str,
) -> dict[str, Any]:
    """Heuristic recommendation on the governed offer ladder."""
    size = company_size.lower().strip()
    goal_l = goal.lower()
    recommended: PlanKey = "governed_revenue_ai_ops_diagnostic"
    rationale_ar = "نبدأ دائماً بالتشخيص المدفوع قبل أي تنفيذ؛ هذا يحمي الثقة ويمنع بناء حلول بلا دليل."

    if "retainer" in goal_l or "monthly" in goal_l:
        recommended = "governed_ops_retainer"
        rationale_ar = "الهدف تشغيلي شهري؛ المناسب Retainer بشرط وجود أدلة تكرار workflow بعد التشخيص."
    elif monthly_budget_sar >= 25000 or "sprint" in goal_l or "implementation" in goal_l:
        recommended = "revenue_intelligence_sprint"
        rationale_ar = "تتوفر ميزانية تنفيذ؛ Sprint يأتي بعد تشخيص يثبت مسار workflow واضح وقابل للقياس."
    elif monthly_budget_sar >= 4999 or size in ("sme", "medium", "growth", "large", "enterprise", "scale"):
        recommended = "governed_revenue_ai_ops_diagnostic"
        rationale_ar = "أفضل مسار: Diagnostic 7 أيام ثم قرار Sprint/Retainer بناءً على proof."

    tiers = get_pricing_tiers()
    tier = next((t for t in tiers["tiers"] if t["key"] == recommended), tiers["tiers"][0])
    return {
        "recommended_plan": recommended,
        "rationale_ar": rationale_ar,
        "next_step_en": "Sell manually, deliver with evidence, then productize repeated workflows only.",
        "tier_summary": tier,
        "inputs": {"company_size": company_size, "monthly_budget_sar": monthly_budget_sar, "goal": goal},
    }


def calculate_performance_fee(
    *,
    qualified_leads: int,
    booked_meetings: int,
    won_revenue_sar: float,
    lead_fee_sar: float = 40.0,
    meeting_fee_sar: float = 250.0,
    success_fee_pct: float = 5.0,
) -> dict[str, Any]:
    """Demo calculation — real contracts need legal + qualification definitions."""
    lead_component = max(0, qualified_leads) * lead_fee_sar
    meeting_component = max(0, booked_meetings) * meeting_fee_sar
    success_component = max(0.0, won_revenue_sar) * (success_fee_pct / 100.0)
    total = round(lead_component + meeting_component + success_component, 2)
    return {
        "qualified_leads": qualified_leads,
        "booked_meetings": booked_meetings,
        "won_revenue_sar": won_revenue_sar,
        "components_sar": {
            "leads": round(lead_component, 2),
            "meetings": round(meeting_component, 2),
            "success": round(success_component, 2),
        },
        "total_performance_fees_sar": total,
        "disclaimer_ar": "يجب ربط أي رسوم أداء بعقود وتأهيل واضح وتتبع نزاعات قبل الفوترة.",
    }


def estimate_roi(
    *,
    plan_price_sar: float,
    expected_pipeline_sar: float,
    expected_revenue_sar: float,
) -> dict[str, Any]:
    """Simple ROI framing — not financial advice."""
    if plan_price_sar <= 0:
        return {"error": "plan_price_must_be_positive"}
    pipeline_multiple = round(expected_pipeline_sar / plan_price_sar, 2) if plan_price_sar else 0.0
    revenue_multiple = round(expected_revenue_sar / plan_price_sar, 2) if plan_price_sar else 0.0
    return {
        "plan_price_sar": plan_price_sar,
        "expected_pipeline_sar": expected_pipeline_sar,
        "expected_revenue_sar": expected_revenue_sar,
        "pipeline_to_subscription_multiple": pipeline_multiple,
        "revenue_to_subscription_multiple": revenue_multiple,
        "verdict_ar": "إذا تعدت المضاعفات 3–5x على الأنابيب المتوقع، يصير الاشتراك منطقياً مع تتبع أسبوعي.",
    }
