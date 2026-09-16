"""AI Concierge — grounded, safe, Arabic/English, policy-enforced.

Grounded only in PUBLIC_ALLOWLISTED_KNOWLEDGE, never exposes Company Brain secrets.
Supports sector/buyer/problem routing, trust/proof surfacing, diagnostic/qualified routing.
"""

from __future__ import annotations

import re
import time
from datetime import UTC, datetime
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

UNKNOWN = "UNKNOWN"

class ConciergeIntent(StrEnum):
    SECTOR_ROUTER = "sector_router"
    PROBLEM_ROUTER = "problem_router"
    BUYER_ROUTER = "buyer_router"
    OFFER_ROUTER = "offer_router"
    DIAGNOSTIC = "diagnostic"
    TRUST = "trust"
    PROOF = "proof"
    PRICING = "pricing"
    INTEGRATION = "integration"
    HUMAN_HANDOFF = "human_handoff"
    GENERAL = "general"

class ConciergePolicy(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    max_input_chars: int = 2000
    max_output_chars: int = 1500
    rate_limit_per_min: int = 10
    timeout_ms: int = 8000
    blocked_patterns: list[str] = Field(default_factory=lambda: [
        r"system prompt", r"ignore previous", r"expose.*secret", r"private.*api", r"company brain", r"internal prompt"
    ])

    def is_blocked(self, text: str) -> bool:
        low = text.lower()
        for pat in self.blocked_patterns:
            if re.search(pat, low):
                return True
        return False

class ConciergeKnowledge(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    knowledge_id: str
    locale: str  # ar, en
    sector: str = UNKNOWN
    buyer: str = UNKNOWN
    problem: str = UNKNOWN
    title: str
    body: str
    source: str = "public_allowlist"
    proof_ref: str = UNKNOWN
    freshness: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())

PUBLIC_ALLOWLIST: list[ConciergeKnowledge] = [
    ConciergeKnowledge(knowledge_id="k1", locale="ar", sector="government_b2g", title="Dealix تشخيص تنفيذي مجاني", body="تشخيص مجاني ومحكوم بالأدلة؛ أي تدخل مدفوع له نطاق ومدة خاصان بالعميل بعد qualified discovery، ولا إرسال خارجي دون موافقة.", proof_ref="proof_ledger"),
    ConciergeKnowledge(knowledge_id="k2", locale="en", sector="technology_saas_si", title="Dealix Free Execution Diagnostic", body="Free evidence-governed diagnostic; any paid intervention gets customer-specific scope and duration after qualified discovery, with approval-first execution.", proof_ref="proof_ledger"),
    ConciergeKnowledge(knowledge_id="k3", locale="ar", title="ZATCA Wave 25", body="إشارة سوقية للفوترة الإلكترونية — تشخيص جاهزية، لا شهادة رسمية.", proof_ref="zatca_official"),
    ConciergeKnowledge(knowledge_id="k4", locale="en", title="PDPL Governance", body="Dealix never sends cold WhatsApp or scraped outreach. Consent before any external send.", proof_ref="pdpl_policy"),
    ConciergeKnowledge(knowledge_id="k5", locale="ar", title="Approval-First", body="كل إرسال يمر عبر Approval Center. AI يقترح، الإنسان يوافق.", proof_ref="approval_center"),
]

class ConciergeRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    request_id: str
    locale: str = "ar"
    sector: str = UNKNOWN
    buyer: str = UNKNOWN
    problem: str = UNKNOWN
    message: str
    consent: bool = False

class ConciergeResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    request_id: str
    intent: ConciergeIntent
    locale: str
    answer: str
    next_step: str = UNKNOWN
    citations: list[str] = Field(default_factory=list)
    handoff: bool = False
    handoff_reason: str = ""

class AIConcierge:
    def __init__(self, policy: ConciergePolicy | None = None) -> None:
        self.policy = policy or ConciergePolicy()
        self._calls: list[float] = []

    def _rate_limited(self) -> bool:
        now = time.time()
        self._calls = [t for t in self._calls if now - t < 60]
        return len(self._calls) >= self.policy.rate_limit_per_min

    def _classify(self, msg: str) -> ConciergeIntent:
        low = msg.lower()
        if any(k in low for k in ["price", "سعر", "تكلفة"]):
            return ConciergeIntent.PRICING
        if any(k in low for k in ["trust", "ثقة", "أمان", "pdpl", "zcta"]):
            return ConciergeIntent.TRUST
        if any(k in low for k in ["proof", "إثبات", "case"]):
            return ConciergeIntent.PROOF
        if any(k in low for k in ["sector", "قطاع", "b2g", "construction"]):
            return ConciergeIntent.SECTOR_ROUTER
        if any(k in low for k in ["diagnostic", "تشخيص", "assessment"]):
            return ConciergeIntent.DIAGNOSTIC
        if any(k in low for k in ["human", "تواصل", "اجتماع"]):
            return ConciergeIntent.HUMAN_HANDOFF
        return ConciergeIntent.GENERAL

    def _retrieve(self, req: ConciergeRequest) -> list[ConciergeKnowledge]:
        # Simple retrieval by locale + keyword overlap, public only
        candidates = [k for k in PUBLIC_ALLOWLIST if k.locale == req.locale or k.locale == "ar"]
        # rank by overlap
        scored = []
        for k in candidates:
            score = 0
            if req.sector != UNKNOWN and req.sector in k.sector:
                score += 2
            if req.problem != UNKNOWN and req.problem in k.problem:
                score += 2
            if any(w in req.message.lower() for w in k.title.lower().split()):
                score += 1
            scored.append((score, k))
        scored.sort(key=lambda x: -x[0])
        return [k for s,k in scored if s > 0][:2] or candidates[:1]

    def respond(self, req: ConciergeRequest) -> ConciergeResponse:
        if len(req.message) > self.policy.max_input_chars:
            return ConciergeResponse(request_id=req.request_id, intent=ConciergeIntent.GENERAL, locale=req.locale, answer="Input too long. Please shorten.", next_step="shorten_input", handoff=False)
        if self.policy.is_blocked(req.message):
            return ConciergeResponse(request_id=req.request_id, intent=ConciergeIntent.HUMAN_HANDOFF, locale=req.locale, answer="I can help with Dealix capabilities but cannot share internal instructions.", next_step="human_review", handoff=True, handoff_reason="policy_block")
        if self._rate_limited():
            return ConciergeResponse(request_id=req.request_id, intent=ConciergeIntent.GENERAL, locale=req.locale, answer="Rate limit reached. Try again shortly.", next_step="retry", handoff=False)
        self._calls.append(time.time())
        intent = self._classify(req.message)
        if intent == ConciergeIntent.HUMAN_HANDOFF:
            return ConciergeResponse(request_id=req.request_id, intent=intent, locale=req.locale, answer="سأوصلك بفريق Dealix البشري لمتابعة طلبك." if req.locale=="ar" else "I will connect you to Dealix human team.", next_step="human_handoff", handoff=True, handoff_reason="explicit_request")
        know = self._retrieve(req)
        # build answer from allowlisted knowledge only
        body = " | ".join(k.body for k in know)
        citations = [k.proof_ref for k in know]
        # economic purpose: route to diagnostic/next step
        if intent in (ConciergeIntent.DIAGNOSTIC, ConciergeIntent.SECTOR_ROUTER, ConciergeIntent.PROBLEM_ROUTER):
            next_step = "start_diagnostic"
        elif intent == ConciergeIntent.PRICING:
            next_step = "discovery_then_quote"
        else:
            next_step = "explore_proof"
        # Never invent customers/prices/guarantees
        answer = body[: self.policy.max_output_chars]
        if req.locale == "ar":
            answer = f"{answer} — التالي: {next_step}."
        else:
            answer = f"{answer} — Next: {next_step}."
        return ConciergeResponse(request_id=req.request_id, intent=intent, locale=req.locale, answer=answer, next_step=next_step, citations=citations, handoff=False)

__all__ = ["AIConcierge", "ConciergeRequest", "ConciergeResponse", "ConciergeIntent", "ConciergePolicy", "PUBLIC_ALLOWLIST"]
