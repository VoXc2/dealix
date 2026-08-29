"""Legacy proposal-draft compatibility surface.

The current commercial entry motion is a Free Mini Diagnostic. This module may
prepare an internal review draft but never creates quote, send, payment, or
execution authority. Retired catalog tiers may be referenced only as capability
hypotheses and can never inject their historical price/duration into the draft.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

from autonomous_growth.product_catalog import Product, ProductTier
from core.logging import get_logger
from core.utils import generate_id, utcnow

log = get_logger(__name__)

_DEFAULT_QUEUE_PATH = "data/proposal_queue.jsonl"
_QUEUE_ENV_VAR = "DEALIX_PROPOSAL_QUEUE_PATH"


def _queue_path() -> Path:
    return Path(os.environ.get(_QUEUE_ENV_VAR, _DEFAULT_QUEUE_PATH))


ProposalStatus = str


@dataclass
class ProposalDraft:
    """Bilingual internal draft; approval state does not authorize a send."""

    id: str
    product_tier: ProductTier
    lead_name: str
    locale: str
    subject_ar: str
    subject_en: str
    body_ar: str
    body_en: str
    cta_url: str
    status: ProposalStatus = "pending_approval"
    created_at: datetime = field(default_factory=utcnow)
    draft_kind: str = "FREE_MINI_DIAGNOSTIC_INVITE"
    commercial_authority: bool = False
    quote_authority: bool = False
    send_authority: bool = False
    execution_authority: bool = False
    external_effect: bool = False
    price_included: bool = False
    delivery_commitment_included: bool = False
    source_product_authority: str = "UNKNOWN_NOT_EVIDENCE_BACKED"

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "product_tier": self.product_tier.value,
            "lead_name": self.lead_name,
            "locale": self.locale,
            "subject_ar": self.subject_ar,
            "subject_en": self.subject_en,
            "body_ar": self.body_ar,
            "body_en": self.body_en,
            "cta_url": self.cta_url,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
            "draft_kind": self.draft_kind,
            "commercial_authority": self.commercial_authority,
            "quote_authority": self.quote_authority,
            "send_authority": self.send_authority,
            "execution_authority": self.execution_authority,
            "external_effect": self.external_effect,
            "price_included": self.price_included,
            "delivery_commitment_included": self.delivery_commitment_included,
            "source_product_authority": self.source_product_authority,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ProposalDraft":
        created = data.get("created_at")
        if isinstance(created, str):
            created = datetime.fromisoformat(created)
        return cls(
            id=data["id"],
            product_tier=ProductTier(data["product_tier"]),
            lead_name=data.get("lead_name", ""),
            locale=data.get("locale", "ar"),
            subject_ar=data.get("subject_ar", ""),
            subject_en=data.get("subject_en", ""),
            body_ar=data.get("body_ar", ""),
            body_en=data.get("body_en", ""),
            cta_url=data.get("cta_url", ""),
            status=data.get("status", "pending_approval"),
            created_at=created or utcnow(),
            draft_kind=data.get("draft_kind", "FREE_MINI_DIAGNOSTIC_INVITE"),
            commercial_authority=bool(data.get("commercial_authority", False)),
            quote_authority=bool(data.get("quote_authority", False)),
            send_authority=bool(data.get("send_authority", False)),
            execution_authority=bool(data.get("execution_authority", False)),
            external_effect=bool(data.get("external_effect", False)),
            price_included=bool(data.get("price_included", False)),
            delivery_commitment_included=bool(data.get("delivery_commitment_included", False)),
            source_product_authority=data.get("source_product_authority", "UNKNOWN_NOT_EVIDENCE_BACKED"),
        )


def _append_to_queue(draft: ProposalDraft) -> None:
    path = _queue_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(draft.to_dict(), ensure_ascii=False) + "\n")


def _read_queue() -> list[ProposalDraft]:
    path = _queue_path()
    if not path.exists():
        return []
    drafts: list[ProposalDraft] = []
    with path.open("r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                try:
                    drafts.append(ProposalDraft.from_dict(json.loads(line)))
                except Exception as exc:
                    log.warning("proposal_queue_parse_error", error=str(exc))
    return drafts


def _rewrite_queue(drafts: list[ProposalDraft]) -> None:
    path = _queue_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        for draft in drafts:
            fh.write(json.dumps(draft.to_dict(), ensure_ascii=False) + "\n")


from core.agents.base import BaseAgent  # noqa: E402


class ProposalSenderAgent(BaseAgent):
    """Prepare a Free Mini Diagnostic invitation draft for internal review only."""

    name = "proposal_sender"

    async def run(  # type: ignore[override]
        self,
        *,
        product: Product,
        lead_profile: dict[str, Any],
        locale: str = "ar",
        cta_url: str = "",
        **_: Any,
    ) -> ProposalDraft:
        lead_name = lead_profile.get("name") or lead_profile.get("company") or "العميل"
        company = lead_profile.get("company", "")
        pain_points: list[str] = lead_profile.get("pain_points") or []
        pain_text = "، ".join(pain_points[:3]) if pain_points else ""

        subject_ar, subject_en = self._build_subjects(product, lead_name)
        body_ar = self._build_body_ar(product, lead_name, company, pain_text, cta_url)
        body_en = self._build_body_en(product, lead_name, company, pain_text, cta_url)

        draft = ProposalDraft(
            id=generate_id("prop"),
            product_tier=product.tier,
            lead_name=lead_name,
            locale=locale,
            subject_ar=subject_ar,
            subject_en=subject_en,
            body_ar=body_ar,
            body_en=body_en,
            cta_url=cta_url,
            status="pending_approval",
            source_product_authority=product.commercial_authority,
        )
        _append_to_queue(draft)

        self.log.info(
            "diagnostic_draft_queued",
            proposal_id=draft.id,
            capability_hypothesis=product.tier.value,
            lead_name=lead_name,
            status=draft.status,
            send_authority=False,
            quote_authority=False,
        )
        return draft

    @staticmethod
    def _build_subjects(product: Product, lead_name: str) -> tuple[str, str]:
        del product
        return (
            f"تشخيص مصغر مجاني لـ {lead_name}",
            f"Free Mini Diagnostic for {lead_name}",
        )

    @staticmethod
    def _build_body_ar(product: Product, lead_name: str, company: str, pain_text: str, cta_url: str) -> str:
        company_line = f" في {company}" if company else ""
        pain_line = f"\n\nالمشكلات المذكورة حتى الآن: {pain_text}." if pain_text else ""
        capability_note = (
            f"\n\nالتصنيف الداخلي الحالي للقدرة: {product.name_ar}. هذا تصنيف أولي فقط وليس عرضاً أو سعراً أو التزاماً."
            if product.tier != ProductTier.FREE_DIAGNOSTIC else ""
        )
        cta_line = f"\n\nالخطوة المقترحة: تشخيص مصغر مجاني عبر {cta_url}." if cta_url else "\n\nالخطوة المقترحة: تشخيص مصغر مجاني قصير لتحديد المشكلة والأدلة والخطوة التالية."
        return (
            f"السيد/السيدة {lead_name}،\n\n"
            f"أعددنا مسودة داخلية لبدء تشخيص مصغر مجاني{company_line}."
            f"{pain_line}{capability_note}{cta_line}\n\n"
            "لا تتضمن هذه المسودة سعراً أو مدة تسليم أو التزاماً تجارياً، ولا تمنح صلاحية إرسال.\n\n"
            "مع التقدير،\nفريق Dealix"
        )

    @staticmethod
    def _build_body_en(product: Product, lead_name: str, company: str, pain_text: str, cta_url: str) -> str:
        company_line = f" at {company}" if company else ""
        pain_line = f"\n\nProblems stated so far: {pain_text}." if pain_text else ""
        capability_note = (
            f"\n\nCurrent internal capability hypothesis: {product.name_en}. This is a hypothesis only, not an offer, price, or commitment."
            if product.tier != ProductTier.FREE_DIAGNOSTIC else ""
        )
        cta_line = f"\n\nSuggested next step: a Free Mini Diagnostic via {cta_url}." if cta_url else "\n\nSuggested next step: a short Free Mini Diagnostic to clarify the problem, evidence, and next step."
        return (
            f"Dear {lead_name},\n\n"
            f"We prepared an internal draft to start with a Free Mini Diagnostic{company_line}."
            f"{pain_line}{capability_note}{cta_line}\n\n"
            "This draft contains no price, delivery commitment, or binding commercial term, and grants no send authority.\n\n"
            "Best regards,\nDealix Team"
        )
