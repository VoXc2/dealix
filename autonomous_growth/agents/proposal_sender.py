"""
Proposal Sender Agent — generates bilingual proposal drafts and queues them for
founder approval. Nothing is ever sent automatically.

وكيل إرسال العروض — يُنشئ مسوّدات عروض ثنائية اللغة ويضعها في قائمة الانتظار
للموافقة. لا شيء يُرسَل تلقائياً.
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

# JSONL queue path — overridable by environment variable
_DEFAULT_QUEUE_PATH = "data/proposal_queue.jsonl"
_QUEUE_ENV_VAR = "DEALIX_PROPOSAL_QUEUE_PATH"


def _queue_path() -> Path:
    return Path(os.environ.get(_QUEUE_ENV_VAR, _DEFAULT_QUEUE_PATH))


ProposalStatus = str  # "pending_approval" | "approved" | "sent"


@dataclass
class ProposalDraft:
    """A bilingual proposal draft awaiting founder approval."""

    id: str
    product_tier: ProductTier
    lead_name: str
    locale: str                         # primary locale for the proposal
    subject_ar: str
    subject_en: str
    body_ar: str
    body_en: str
    cta_url: str
    status: ProposalStatus = "pending_approval"   # always starts here
    created_at: datetime = field(default_factory=utcnow)

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
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> ProposalDraft:
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
        )


# ---------------------------------------------------------------------------
# Queue helpers (pure I/O; no BaseAgent dependency)
# ---------------------------------------------------------------------------

def _append_to_queue(draft: ProposalDraft) -> None:
    """Append a single ProposalDraft to the JSONL queue file."""
    path = _queue_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(draft.to_dict(), ensure_ascii=False) + "\n")


def _read_queue() -> list[ProposalDraft]:
    """Read all drafts from the JSONL queue file."""
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
    """Overwrite the JSONL queue with the provided list."""
    path = _queue_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        for draft in drafts:
            fh.write(json.dumps(draft.to_dict(), ensure_ascii=False) + "\n")


# ---------------------------------------------------------------------------
# Agent
# ---------------------------------------------------------------------------

# Import BaseAgent only at class definition time — keeps the module importable
# even if the heavy core stack is unavailable during unit tests.
from core.agents.base import BaseAgent  # noqa: E402


class ProposalSenderAgent(BaseAgent):
    """
    Generates a bilingual proposal draft for a given product and lead profile,
    then stores it in the proposal queue with status 'pending_approval'.

    The agent NEVER sends proposals to external parties. Sending is a manual
    founder action after reviewing the draft in the approval queue.

    يُنشئ مسوّدة عرض ثنائية اللغة لمنتج محدد وملف عميل، ثم يحفظها في قائمة
    الانتظار بحالة 'pending_approval'. لا يُرسل شيئاً تلقائياً أبداً.
    """

    name = "proposal_sender"

    async def run(  # type: ignore[override]
        self,
        *,
        product: Product,
        lead_profile: dict[str, Any],
        locale: str = "ar",
        cta_url: str = "https://dealix.ai/book",
        **_: Any,
    ) -> ProposalDraft:
        """
        Generate a bilingual proposal draft and queue it for approval.

        Parameters
        ----------
        product:
            The Product to propose.
        lead_profile:
            Dict containing at minimum ``name`` (str) and optionally
            ``company``, ``sector``, ``pain_points`` (list[str]).
        locale:
            Primary locale for the proposal body. Both languages are always
            generated regardless of this setting.
        cta_url:
            The call-to-action URL to embed in the proposal.
        """
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
        )

        _append_to_queue(draft)

        self.log.info(
            "proposal_draft_queued",
            proposal_id=draft.id,
            product_tier=product.tier.value,
            lead_name=lead_name,
            status=draft.status,
        )
        return draft

    # ── Draft builders ─────────────────────────────────────────────

    @staticmethod
    def _build_subjects(product: Product, lead_name: str) -> tuple[str, str]:
        subject_ar = f"عرض {product.name_ar} لـ {lead_name}"
        subject_en = f"{product.name_en} proposal for {lead_name}"
        return subject_ar, subject_en

    @staticmethod
    def _build_body_ar(
        product: Product,
        lead_name: str,
        company: str,
        pain_text: str,
        cta_url: str,
    ) -> str:
        company_line = f" في {company}" if company else ""
        pain_line = (
            f"\n\nفهمنا أن أبرز التحديات{company_line} تشمل: {pain_text}."
            if pain_text
            else ""
        )
        price_line = (
            f"{product.price_sar:,} ريال"
            if product.price_sar == product.price_max_sar
            else f"{product.price_sar:,} – {product.price_max_sar:,} ريال"
        )
        outcomes = "\n".join(f"- {o}" for o in product.key_outcomes if "Arabic" not in o or True)
        return (
            f"السيد/السيدة {lead_name}،\n\n"
            f"يسعدنا تقديم عرض {product.name_ar}{company_line}.{pain_line}\n\n"
            f"**الوصف:**\n{product.description_ar}\n\n"
            f"**النتائج الرئيسية:**\n{outcomes}\n\n"
            f"**السعر:** {price_line}\n"
            f"**مدة التسليم:** {product.delivery_days} يوم\n\n"
            f"لحجز موعد لمناقشة التفاصيل: {cta_url}\n\n"
            "مع التقدير،\nفريق Dealix"
        )

    @staticmethod
    def _build_body_en(
        product: Product,
        lead_name: str,
        company: str,
        pain_text: str,
        cta_url: str,
    ) -> str:
        company_line = f" at {company}" if company else ""
        pain_line = (
            f"\n\nWe understand that key challenges{company_line} include: {pain_text}."
            if pain_text
            else ""
        )
        price_line = (
            f"{product.price_sar:,} SAR"
            if product.price_sar == product.price_max_sar
            else f"{product.price_sar:,} – {product.price_max_sar:,} SAR"
        )
        outcomes = "\n".join(f"- {o}" for o in product.key_outcomes)
        return (
            f"Dear {lead_name},\n\n"
            f"We are pleased to present our {product.name_en} proposal{company_line}.{pain_line}\n\n"
            f"**Description:**\n{product.description_en}\n\n"
            f"**Key Outcomes:**\n{outcomes}\n\n"
            f"**Price:** {price_line}\n"
            f"**Delivery:** {product.delivery_days} days\n\n"
            f"To schedule a call and discuss the details: {cta_url}\n\n"
            "Best regards,\nDealix Team"
        )
