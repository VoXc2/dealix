"""Expansion readiness — evidence-first, customer-specific commercial authority.

This engine may recommend a scope class for internal review. It never prices an
expansion, fixes duration/session count, sends a proposal, or creates payment.
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
    recommended_tier: str = ""  # compatibility field; value is an unpriced scope class
    proposal_draft_ar: str = ""
    proposal_draft_en: str = ""
    approval_status: str = "approval_required"
    governance_decision: str = "pending"
    price_authority: str = "customer_specific_quote_after_review"
    duration_policy: str = "customer_specific_after_review"

    def to_dict(self) -> dict[str, Any]:
        return json.loads(self.model_dump_json())


_SCOPE_OPTIONS = {
    "managed_ops_core": {
        "name_ar": "Managed Ops — نطاق أساسي",
        "name_en": "Managed Ops — Core Scope",
        "description_ar": "استمرار محكوم للنطاق المثبت مع KPI وProof وموافقات مناسبة للحالة.",
        "description_en": "Governed continuation of the proven scope with case-specific KPI, Proof, and approvals.",
    },
    "managed_ops_expanded": {
        "name_ar": "Managed Ops — نطاق موسع",
        "name_en": "Managed Ops — Expanded Scope",
        "description_ar": "توسعة محكومة فقط لما دعمه Proof واعتمده العميل، بدون باقة أو مدة ثابتة.",
        "description_en": "Governed expansion only for proof-supported, customer-approved work; no fixed package or duration.",
    },
    "executive_ai_partner": {
        "name_ar": "Executive AI Partner — نطاق مخصص",
        "name_en": "Executive AI Partner — Custom Scope",
        "description_ar": "نطاق تنفيذي مخصص يحدد بعد مراجعة الأدلة والقدرة والمتطلبات والموافقات.",
        "description_en": "Custom executive scope defined after evidence, capacity, requirements, and approval review.",
    },
}


class UpsellEngine:
    """Evaluate expansion readiness and draft an unpriced internal scope proposal."""

    def check(self, account_id: str, company_name: str, proof_event_count: int, proof_level: str = "L0", monthly_revenue_sar: float = 0.0) -> UpsellCheckResult:
        eligible = proof_event_count >= 3 and proof_level in ("L1", "L2", "L3")
        if not eligible:
            return UpsellCheckResult(
                account_id=account_id, company_name=company_name, is_eligible=False,
                reason_ar=f"غير مؤهل للتوسع بعد. الأحداث الحالية: {proof_event_count}/3، المستوى: {proof_level}.",
                reason_en=f"Not expansion-eligible yet. Current events: {proof_event_count}/3, level: {proof_level}.",
                proof_event_count=proof_event_count,
            )
        scope_key = "managed_ops_core"
        if monthly_revenue_sar > 100_000 or proof_level == "L3":
            scope_key = "executive_ai_partner"
        elif proof_event_count >= 6 or proof_level == "L2":
            scope_key = "managed_ops_expanded"
        scope = _SCOPE_OPTIONS[scope_key]
        return UpsellCheckResult(
            account_id=account_id, company_name=company_name, is_eligible=True,
            reason_ar=f"مؤهل لمراجعة توسع، لا لعرض تلقائي. {proof_event_count} أحداث موثقة، مستوى {proof_level}.",
            reason_en=f"Eligible for expansion review, not an automatic offer. {proof_event_count} documented events, level {proof_level}.",
            proof_event_count=proof_event_count, recommended_tier=scope_key,
            proposal_draft_ar=self._draft_proposal_ar(company_name, scope, proof_event_count),
            proposal_draft_en=self._draft_proposal_en(company_name, scope, proof_event_count),
        )

    def _draft_proposal_ar(self, company_name: str, scope: dict[str, str], event_count: int) -> str:
        return f"""مسودة مراجعة توسع — {company_name}
التاريخ: {datetime.now(UTC).strftime('%Y-%m-%d')}

بعد {event_count} أحداث موثقة، توجد أهلية لمراجعة نطاق جديد فقط:
## {scope['name_ar']}
{scope['description_ar']}

السعر والمدة وشروط التنفيذ لا يحددها هذا المحرك؛ تُحدد بعد مراجعة خاصة بالعميل وبـquote معتمد.
لا يوجد توسع تلقائي أو live charge أو إرسال خارجي من هذه المسودة.
"""

    def _draft_proposal_en(self, company_name: str, scope: dict[str, str], event_count: int) -> str:
        return f"""Expansion Review Draft — {company_name}
Date: {datetime.now(UTC).strftime('%Y-%m-%d')}

After {event_count} documented events, the account is eligible only for review of a new scope:
## {scope['name_en']}
{scope['description_en']}

Price, duration, and delivery terms are not set by this engine; they require customer-specific review and an approved quote.
No automatic expansion, live charge, or external send is authorized by this draft.
"""
