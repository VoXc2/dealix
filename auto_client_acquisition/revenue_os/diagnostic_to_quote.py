"""
Diagnostic to Quote — converts diagnostic results into quotes and proposals.
من التشخيص إلى العرض — يحول نتائج التشخيص إلى عروض أسعار ومقترحات.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from core.logging import get_logger
from core.utils import generate_id, utcnow

logger = get_logger(__name__)


@dataclass
class Quote:
    id: str
    diagnostic_id: str
    customer_handle: str
    sector: str
    plan_tier: str = "growth"
    base_price_sar: float = 2999.0
    setup_fee_sar: float = 0.0
    discount_sar: float = 0.0
    total_sar: float = 0.0
    line_items: list[dict[str, Any]] = field(default_factory=list)
    status: str = "draft"
    valid_until: str = ""
    created_at: datetime = field(default_factory=utcnow)

    def __post_init__(self):
        if self.total_sar == 0.0:
            self.total_sar = self.base_price_sar + self.setup_fee_sar - self.discount_sar

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "diagnostic_id": self.diagnostic_id,
            "customer_handle": self.customer_handle,
            "sector": self.sector,
            "plan_tier": self.plan_tier,
            "base_price_sar": self.base_price_sar,
            "setup_fee_sar": self.setup_fee_sar,
            "discount_sar": self.discount_sar,
            "total_sar": self.total_sar,
            "line_items": self.line_items,
            "status": self.status,
            "valid_until": self.valid_until,
            "created_at": self.created_at.isoformat(),
        }


@dataclass
class ProposalDocument:
    id: str
    quote_id: str
    customer_handle: str
    title_ar: str
    title_en: str
    executive_summary_ar: str
    executive_summary_en: str
    challenge_analysis_ar: str
    challenge_analysis_en: str
    proposed_solution_ar: str
    proposed_solution_en: str
    pricing_ar: str
    pricing_en: str
    next_steps_ar: str
    next_steps_en: str
    status: str = "draft"
    created_at: datetime = field(default_factory=utcnow)

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "quote_id": self.quote_id,
            "customer_handle": self.customer_handle,
            "title_ar": self.title_ar,
            "title_en": self.title_en,
            "executive_summary_ar": self.executive_summary_ar,
            "executive_summary_en": self.executive_summary_en,
            "challenge_analysis_ar": self.challenge_analysis_ar,
            "challenge_analysis_en": self.challenge_analysis_en,
            "proposed_solution_ar": self.proposed_solution_ar,
            "proposed_solution_en": self.proposed_solution_en,
            "pricing_ar": self.pricing_ar,
            "pricing_en": self.pricing_en,
            "next_steps_ar": self.next_steps_ar,
            "next_steps_en": self.next_steps_en,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
        }


@dataclass
class SendResult:
    success: bool
    target: str = ""
    channel: str = "email"
    message: str = ""
    errors: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "success": self.success,
            "target": self.target,
            "channel": self.channel,
            "message": self.message,
            "errors": self.errors,
        }


PLAN_PRICING = {
    "starter": {"price_sar": 999, "setup_fee_sar": 0, "features": ["AI Diagnostic", "Basic Dashboard", "Email Support"]},
    "growth": {"price_sar": 2999, "setup_fee_sar": 2999, "features": ["AI Diagnostic", "Revenue Dashboard", "Chat Support", "Warm Intro Generator"]},
    "scale": {"price_sar": 7999, "setup_fee_sar": 7999, "features": ["Full AI Stack", "Executive Dashboard", "Priority Support", "API Access", "Partner Portal"]},
    "enterprise": {"price_sar": 24999, "setup_fee_sar": 24999, "features": ["Custom AI Solution", "Dedicated Team", "SLA Guarantee", "White Label", "On-premise Option"]},
}


class DiagnosticToQuote:
    def __init__(self):
        self._quotes: dict[str, Quote] = {}
        self._proposals: dict[str, ProposalDocument] = {}
        self.log = logger.bind(component="diagnostic_to_quote")

    async def convert(self, diagnostic_id: str) -> Quote:
        quote = Quote(
            id=generate_id("qte"),
            diagnostic_id=diagnostic_id,
            customer_handle=f"customer_{diagnostic_id[:8]}",
            sector="general",
            plan_tier="growth",
            base_price_sar=PLAN_PRICING["growth"]["price_sar"],
            setup_fee_sar=PLAN_PRICING["growth"]["setup_fee_sar"],
            total_sar=PLAN_PRICING["growth"]["price_sar"] + PLAN_PRICING["growth"]["setup_fee_sar"],
            line_items=[
                {"description": plan_name, "amount_sar": info["price_sar"]}
                for plan_name, info in PLAN_PRICING.items()
            ],
            status="draft",
            valid_until=utcnow().isoformat(),
        )
        self._quotes[quote.id] = quote
        self.log.info("quote_generated", id=quote.id, diagnostic_id=diagnostic_id)
        return quote

    async def generate_proposal(self, quote_id: str) -> ProposalDocument:
        quote = self._quotes.get(quote_id)
        if not quote:
            raise ValueError(f"Quote {quote_id} not found")

        proposal = ProposalDocument(
            id=generate_id("prp"),
            quote_id=quote_id,
            customer_handle=quote.customer_handle,
            title_ar=f"اقتراح حل Dealix لـ {quote.customer_handle}",
            title_en=f"Dealix Solution Proposal for {quote.customer_handle}",
            executive_summary_ar=(
                f"بناءً على التشخيص الشامل لقطاع {quote.sector} واحتياجات "
                f"{quote.customer_handle}، نقدم حل Dealix المتكامل لتسريع "
                f"النمو الإيرادي باستخدام الذكاء الاصطناعي."
            ),
            executive_summary_en=(
                f"Based on the comprehensive diagnostic of the {quote.sector} sector "
                f"and {quote.customer_handle}'s needs, we present the integrated "
                f"Dealix solution for accelerating revenue growth using AI."
            ),
            challenge_analysis_ar="تم تحديد التحديات الرئيسية خلال جلسة التشخيص.",
            challenge_analysis_en="Key challenges were identified during the diagnostic session.",
            proposed_solution_ar=(
                f"نقترح باقة {quote.plan_tier} التي تتضمن:\n"
                + "\n".join(f"- {f}" for f in PLAN_PRICING[quote.plan_tier]["features"])
            ),
            proposed_solution_en=(
                f"We propose the {quote.plan_tier} plan which includes:\n"
                + "\n".join(f"- {f}" for f in PLAN_PRICING[quote.plan_tier]["features"])
            ),
            pricing_ar=(
                f"السعر الأساسي: {quote.base_price_sar:,.0f} ريال\n"
                f"رسوم التفعيل: {quote.setup_fee_sar:,.0f} ريال\n"
                f"الإجمالي: {quote.total_sar:,.0f} ريال"
            ),
            pricing_en=(
                f"Base Price: SAR {quote.base_price_sar:,.0f}\n"
                f"Setup Fee: SAR {quote.setup_fee_sar:,.0f}\n"
                f"Total: SAR {quote.total_sar:,.0f}"
            ),
            next_steps_ar="1. مراجعة الاقتراح\n2. جدولة جلسة أسئلة وأجوبة\n3. توقيع الاتفاقية",
            next_steps_en="1. Review the proposal\n2. Schedule Q&A session\n3. Sign the agreement",
            status="draft",
        )
        self._proposals[proposal.id] = proposal
        self.log.info("proposal_generated", id=proposal.id, quote_id=quote_id)
        return proposal

    async def send_to_client(self, quote_id: str) -> SendResult:
        quote = self._quotes.get(quote_id)
        if not quote:
            return SendResult(success=False, errors=["Quote not found"])

        quote.status = "sent"

        result = SendResult(
            success=True,
            target=quote.customer_handle,
            channel="email",
            message="Quote and proposal queued for manual review before sending",
        )
        self.log.info("quote_sent", id=quote_id)
        return result

    def get_quote(self, quote_id: str) -> Quote | None:
        return self._quotes.get(quote_id)

    def get_proposal(self, proposal_id: str) -> ProposalDocument | None:
        return self._proposals.get(proposal_id)

    def list_quotes(self, status: str | None = None) -> list[Quote]:
        if status:
            return [q for q in self._quotes.values() if q.status == status]
        return list(self._quotes.values())

    def get_stats(self) -> dict[str, Any]:
        quotes = self._quotes.values()
        return {
            "total_quotes": len(quotes),
            "total_proposals": len(self._proposals),
            "total_value_sar": sum(q.total_sar for q in quotes if q.status == "sent"),
            "by_status": {
                s: sum(1 for q in quotes if q.status == s)
                for s in ["draft", "sent", "accepted", "rejected"]
            },
        }
