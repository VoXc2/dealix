"""Founder-facing notifications (transactional emails to founder only).

Currently exposes one helper: ``notify_founder_on_intake`` — fires
when a new lead lands in the system. NEVER sends to a customer; the
recipient is always ``Settings.dealix_founder_email``.

This module is the "post-intake hook" missing from the otherwise
fully-implemented intake pipeline. The pipeline (LeadCreateRequest
→ AcquisitionPipeline.run → LeadRecord persistence) used to commit
silently; this hook closes the loop so the founder sees every lead
the moment it arrives.

Hard rules:

  - Recipient is the founder ONLY (read from
    ``Settings.dealix_founder_email``); never a customer.
  - Send failure NEVER fails the underlying intake — caller wraps
    in try/except and logs.
  - Body never reveals secrets / internal API keys.
  - Bilingual subject (Arabic primary, English secondary line).
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from core.config.settings import get_settings
from core.logging import get_logger
from integrations.email import EmailClient, EmailResult

logger = get_logger(__name__)


@dataclass
class FounderAlertPayload:
    """Minimal info needed to render an intake alert."""

    company_name: str
    contact_name: str
    contact_email: str | None
    contact_phone: str | None
    sector: str | None
    region: str | None
    fit_score: float | None
    urgency_score: float | None
    pain_points: list[str]
    locale: str
    source: str
    lead_id: str

    @classmethod
    def from_lead(cls, lead: Any) -> FounderAlertPayload:
        """Build the payload from a LeadRecord (or anything duck-typed similar)."""
        return cls(
            company_name=str(getattr(lead, "company_name", "") or ""),
            contact_name=str(getattr(lead, "contact_name", "") or ""),
            contact_email=getattr(lead, "contact_email", None),
            contact_phone=getattr(lead, "contact_phone", None),
            sector=getattr(lead, "sector", None),
            region=getattr(lead, "region", None),
            fit_score=getattr(lead, "fit_score", None),
            urgency_score=getattr(lead, "urgency_score", None),
            pain_points=list(getattr(lead, "pain_points", None) or []),
            locale=str(getattr(lead, "locale", "ar") or "ar"),
            source=str(getattr(lead, "source", None) or "website"),
            lead_id=str(getattr(lead, "id", "")),
        )


def _format_score(value: float | None) -> str:
    if value is None:
        return "—"
    try:
        return f"{float(value):.2f}"
    except (TypeError, ValueError):
        return "—"


def _build_subject(payload: FounderAlertPayload) -> str:
    sector = payload.sector or "غير محدّد"
    return f"🟢 لِيد جديد · {payload.company_name} ({sector}) — Dealix"


def _build_body_text(payload: FounderAlertPayload) -> str:
    """Render a plain-text body, Arabic primary + English secondary block."""
    fit = _format_score(payload.fit_score)
    urgency = _format_score(payload.urgency_score)
    pain = ", ".join(payload.pain_points[:6]) or "—"

    return f"""لِيد جديد وصل عبر Dealix.

▸ الشركة: {payload.company_name}
▸ جهة التواصل: {payload.contact_name}
▸ البريد: {payload.contact_email or "—"}
▸ الجوال: {payload.contact_phone or "—"}
▸ القطاع: {payload.sector or "—"}
▸ المنطقة: {payload.region or "—"}
▸ Fit Score: {fit}
▸ Urgency Score: {urgency}
▸ Pain points: {pain}
▸ المصدر: {payload.source}
▸ Lead ID: {payload.lead_id}

—

[EN] New lead via Dealix.
  company:    {payload.company_name}
  contact:    {payload.contact_name} <{payload.contact_email or "—"}>
  sector:     {payload.sector or "—"} · region: {payload.region or "—"}
  fit/urgency: {fit} / {urgency}
  source:     {payload.source}
  id:         {payload.lead_id}

Reply to this email to follow up. The lead is already saved in the
Dealix DB — this notification is the founder-only alert.

— Dealix
"""


async def notify_founder_on_intake(lead: Any) -> EmailResult:
    """Send a transactional email to the founder.

    Returns the underlying ``EmailResult`` so the caller can log
    success/failure. Never raises — failures return
    ``EmailResult(success=False, ...)``.
    """
    settings = get_settings()
    recipient = settings.dealix_founder_email
    if not recipient:
        return EmailResult(
            success=False,
            provider=settings.email_provider,
            error="dealix_founder_email_not_configured",
        )

    payload = FounderAlertPayload.from_lead(lead)
    subject = _build_subject(payload)
    body_text = _build_body_text(payload)

    client = EmailClient()
    try:
        result = await client.send(
            to=recipient,
            subject=subject,
            body_text=body_text,
            reply_to=payload.contact_email or None,
        )
        if result.success:
            logger.info(
                "founder_alert_sent",
                lead_id=payload.lead_id,
                recipient=recipient,
                provider=result.provider,
                message_id=result.message_id,
            )
        else:
            logger.warning(
                "founder_alert_send_failed",
                lead_id=payload.lead_id,
                provider=result.provider,
                error=result.error,
            )
        return result
    except Exception as exc:
        logger.exception("founder_alert_exception", lead_id=payload.lead_id)
        return EmailResult(
            success=False,
            provider=settings.email_provider,
            error=f"{type(exc).__name__}: {exc}",
        )


__all__ = [
    "FounderAlertPayload",
    "notify_founder_on_intake",
]
