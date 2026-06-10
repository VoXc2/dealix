"""
Warm Introduction Pipeline — generates and tracks warm introductions.
خط أنابيب المقدمة الدافئة — يولد ويتتبع المقدمات الدافئة.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from core.logging import get_logger
from core.utils import generate_id, utcnow

logger = get_logger(__name__)


@dataclass
class Prospect:
    id: str
    company_name: str
    sector: str
    contact_name: str = ""
    contact_role: str = ""
    email: str = ""
    phone: str = ""
    mutual_connection: str = ""
    context: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "company_name": self.company_name,
            "sector": self.sector,
            "contact_name": self.contact_name,
            "contact_role": self.contact_role,
            "email": self.email,
            "phone": self.phone,
            "mutual_connection": self.mutual_connection,
            "context": self.context,
        }


@dataclass
class WarmIntro:
    id: str
    prospect_id: str
    mutual_connection: str
    intro_message_ar: str
    intro_message_en: str
    context_notes: str = ""
    status: str = "draft"
    sent_at: datetime | None = None
    response: str = ""
    response_received_at: datetime | None = None
    created_at: datetime = field(default_factory=utcnow)

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "prospect_id": self.prospect_id,
            "mutual_connection": self.mutual_connection,
            "intro_message_ar": self.intro_message_ar,
            "intro_message_en": self.intro_message_en,
            "context_notes": self.context_notes,
            "status": self.status,
            "sent_at": self.sent_at.isoformat() if self.sent_at else None,
            "response": self.response,
            "response_received_at": self.response_received_at.isoformat() if self.response_received_at else None,
            "created_at": self.created_at.isoformat(),
        }


@dataclass
class SendResult:
    success: bool
    intro_id: str
    channel: str = "email"
    message: str = ""
    errors: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "success": self.success,
            "intro_id": self.intro_id,
            "channel": self.channel,
            "message": self.message,
            "errors": self.errors,
        }


@dataclass
class ResponseResult:
    success: bool
    intro_id: str
    response: str
    sentiment: str = "neutral"
    next_action: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "success": self.success,
            "intro_id": self.intro_id,
            "response": self.response,
            "sentiment": self.sentiment,
            "next_action": self.next_action,
        }


class WarmIntroPipeline:
    def __init__(self):
        self._intros: dict[str, WarmIntro] = {}
        self.log = logger.bind(component="warm_intro_pipeline")

    async def generate(self, prospect: Prospect) -> WarmIntro:
        intro_ar = (
            f"السلام عليكم {prospect.mutual_connection}،\n\n"
            f"أتمنى أن تكون بخير. لاحظت أنك على تواصل مع {prospect.contact_name} "
            f"في {prospect.company_name} (قطاع {prospect.sector}).\n\n"
            f"نحن في Dealix نساعد شركات {prospect.sector} في السعودية على "
            f"تسريع نموها الإيرادي باستخدام الذكاء الاصطناعي. "
            f"هل يمكنك تعريفنا؟ سنكون ممتنين جداً.\n\n"
            f"شكراً جزيلاً"
        )

        intro_en = (
            f"Hi {prospect.mutual_connection},\n\n"
            f"I hope you're doing well. I noticed you're connected with "
            f"{prospect.contact_name} at {prospect.company_name} ({prospect.sector} sector).\n\n"
            f"At Dealix, we help Saudi {prospect.sector} companies accelerate "
            f"revenue growth using AI. Would you be open to making an introduction? "
            f"We would greatly appreciate it.\n\n"
            f"Thank you!"
        )

        warm_intro = WarmIntro(
            id=generate_id("wi"),
            prospect_id=prospect.id,
            mutual_connection=prospect.mutual_connection,
            intro_message_ar=intro_ar,
            intro_message_en=intro_en,
            context_notes=prospect.context,
            status="draft",
        )
        self._intros[warm_intro.id] = warm_intro
        self.log.info("warm_intro_generated", id=warm_intro.id, prospect_id=prospect.id)
        return warm_intro

    async def send(self, intro_id: str) -> SendResult:
        intro = self._intros.get(intro_id)
        if not intro:
            return SendResult(success=False, intro_id=intro_id, errors=["Warm intro not found"])

        if intro.status != "draft":
            return SendResult(
                success=False, intro_id=intro_id,
                errors=[f"Invalid status: {intro.status}. Must be draft."],
            )

        intro.status = "sent"
        intro.sent_at = utcnow()

        result = SendResult(
            success=True,
            intro_id=intro_id,
            channel="email",
            message="Warm introduction sent for manual delivery",
        )
        self.log.info("warm_intro_sent", id=intro_id)
        return result

    async def track_response(self, intro_id: str, response: str) -> ResponseResult:
        intro = self._intros.get(intro_id)
        if not intro:
            return ResponseResult(
                success=False, intro_id=intro_id,
                response=response, next_action="none",
            )

        intro.response = response
        intro.response_received_at = utcnow()
        intro.status = "responded"

        positive_keywords = ["نعم", "بكل سرور", "بالتأكيد", "yes", "sure", "absolutely", "happy to"]
        is_positive = any(kw in response.lower() for kw in positive_keywords)

        result = ResponseResult(
            success=True,
            intro_id=intro_id,
            response=response,
            sentiment="positive" if is_positive else "neutral",
            next_action="schedule_meeting" if is_positive else "follow_up",
        )
        self.log.info("warm_intro_response", id=intro_id, sentiment=result.sentiment)
        return result

    def get_intro(self, intro_id: str) -> WarmIntro | None:
        return self._intros.get(intro_id)

    def list_intros(self, status: str | None = None) -> list[WarmIntro]:
        if status:
            return [i for i in self._intros.values() if i.status == status]
        return list(self._intros.values())

    def get_stats(self) -> dict[str, Any]:
        intros = self._intros.values()
        return {
            "total": len(intros),
            "draft": sum(1 for i in intros if i.status == "draft"),
            "sent": sum(1 for i in intros if i.status == "sent"),
            "responded": sum(1 for i in intros if i.status == "responded"),
            "positive_responses": sum(
                1 for i in intros
                if i.response and any(
                    kw in i.response.lower()
                    for kw in ["نعم", "بكل سرور", "yes", "sure", "absolutely"]
                )
            ),
        }
