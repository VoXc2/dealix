"""Upsell Engine — checks eligibility and drafts Managed Ops proposals.

Constitutional gate: NO_LIVE_SEND — proposal drafted only, never auto-sent.
Trigger: account has 3+ proof events at L1 or above.
"""

from __future__ import annotations

import json
from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel


class UpsellCheckResult(BaseModel):
    account_id: str
    company_name: str
    is_eligible: bool
    reason_ar: str
    reason_en: str
    proof_event_count: int
    recommended_tier: str = ""  # "managed_ops_2999" | "managed_ops_4999" | "executive_5k_25k"
    proposal_draft_ar: str = ""
    proposal_draft_en: str = ""
    approval_status: str = "approval_required"
    governance_decision: str = "pending"  # pending | approved | rejected

    def to_dict(self) -> dict[str, Any]:
        return json.loads(self.model_dump_json())


_TIERS = {
    "managed_ops_2999": {
        "price_sar": 2999,
        "name_ar": "Managed Ops الأساسي",
        "name_en": "Managed Ops Basic",
        "sessions": 8,
        "description_ar": "8 جلسات شهرية + لوحة KPI + تقرير إثبات شهري",
        "description_en": "8 monthly sessions + KPI dashboard + monthly proof report",
    },
    "managed_ops_4999": {
        "price_sar": 4999,
        "name_ar": "Managed Ops المتقدم",
        "name_en": "Managed Ops Advanced",
        "sessions": 16,
        "description_ar": "16 جلسة شهرية + KPI حي + طقم إثبات + أولوية الدعم",
        "description_en": "16 monthly sessions + live KPI + proof pack + priority support",
    },
    "executive_5k_25k": {
        "price_sar": 15000,
        "name_ar": "Executive AI Partner",
        "name_en": "Executive AI Partner",
        "sessions": -1,
        "description_ar": "شراكة تنفيذية شاملة — AI agents مخصصة + تكاملات + فريق Dealix",
        "description_en": "Full executive partnership — custom AI agents + integrations + Dealix team",
    },
}


class UpsellEngine:
    """Evaluates upsell readiness and generates proposal drafts."""

    def check(
        self,
        account_id: str,
        company_name: str,
        proof_event_count: int,
        proof_level: str = "L0",
        monthly_revenue_sar: float = 0.0,
    ) -> UpsellCheckResult:

        eligible = proof_event_count >= 3 and proof_level in ("L1", "L2", "L3")
        if not eligible:
            return UpsellCheckResult(
                account_id=account_id,
                company_name=company_name,
                is_eligible=False,
                reason_ar=f"غير مؤهل بعد. الأحداث الحالية: {proof_event_count}/3، المستوى: {proof_level}.",
                reason_en=f"Not eligible yet. Current events: {proof_event_count}/3, level: {proof_level}.",
                proof_event_count=proof_event_count,
            )

        tier = "managed_ops_2999"
        if monthly_revenue_sar > 100_000 or proof_level == "L3":
            tier = "executive_5k_25k"
        elif proof_event_count >= 6 or proof_level == "L2":
            tier = "managed_ops_4999"

        t = _TIERS[tier]
        proposal_ar = self._draft_proposal_ar(company_name, t, proof_event_count)
        proposal_en = self._draft_proposal_en(company_name, t, proof_event_count)

        return UpsellCheckResult(
            account_id=account_id,
            company_name=company_name,
            is_eligible=True,
            reason_ar=f"مؤهل للترقية. {proof_event_count} أحداث موثقة، مستوى {proof_level}.",
            reason_en=f"Eligible for upgrade. {proof_event_count} documented events, level {proof_level}.",
            proof_event_count=proof_event_count,
            recommended_tier=tier,
            proposal_draft_ar=proposal_ar,
            proposal_draft_en=proposal_en,
        )

    def _draft_proposal_ar(self, company_name: str, tier: dict, event_count: int) -> str:
        return f"""عرض Managed Ops — {company_name}
التاريخ: {datetime.now(UTC).strftime('%Y-%m-%d')}

بعد {event_count} نتائج موثقة من برنامج Dealix الأسبوعي، نقترح الانتقال إلى:

## {tier['name_ar']} — {tier['price_sar']:,} ر.س/شهر

### ما يشمله البرنامج:
{tier['description_ar']}

### لماذا الآن؟
الزخم الموجود اليوم في {company_name} يستحق الاستمرار.
التوقف الآن يعني إعادة البناء من الصفر لاحقاً.

### الخطوة التالية:
مكالمة 15 دقيقة لمراجعة شروط العقد والبداية الشهر القادم.

> يتطلب موافقة المؤسس قبل الإرسال.
> **القيمة التقديرية ليست قيمة مُتحقَّقة** — Estimated value is not Verified value.
"""

    def _draft_proposal_en(self, company_name: str, tier: dict, event_count: int) -> str:
        return f"""Managed Ops Proposal — {company_name}
Date: {datetime.now(UTC).strftime('%Y-%m-%d')}

After {event_count} documented results from the Dealix weekly program, we propose upgrading to:

## {tier['name_en']} — {tier['price_sar']:,} SAR/month

### What's included:
{tier['description_en']}

### Why now?
The momentum built at {company_name} deserves continuation.
Stopping now means rebuilding from scratch later.

### Next step:
15-minute call to review contract terms and start next month.

> Requires founder approval before sending.
> **Estimated value is not Verified value** — القيمة التقديرية ليست قيمة مُتحقَّقة.
"""
