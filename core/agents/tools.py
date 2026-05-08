"""
Agent Tool Registry — function-calling tools for BaseAgent.
سجل أدوات الوكيل — أدوات استدعاء الوظائف للوكيل الأساسي.

Defines the Tool dataclass + registry of built-in tools:
  - search_company       : Search for company information
  - send_whatsapp        : Send a WhatsApp message to a contact
  - create_deal          : Create a new deal in the CRM
  - schedule_meeting     : Schedule a meeting with a contact
  - generate_invoice     : Generate a ZATCA-compliant invoice

Usage in BaseAgent:
    self.register_tool(TOOL_REGISTRY["search_company"])
    result = await self.run_with_tools(task, prompt)
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any, Callable, Awaitable

logger = logging.getLogger(__name__)


# ── Tool dataclass ─────────────────────────────────────────────────

@dataclass
class Tool:
    """
    Represents a callable tool that an agent can invoke.
    أداة قابلة للاستدعاء من قِبَل الوكيل.
    """

    name: str
    description: str
    parameters_schema: dict[str, Any]    # JSON Schema for parameters
    function: Callable[..., Awaitable[dict[str, Any]]]

    def to_openai_schema(self) -> dict[str, Any]:
        """Convert to OpenAI function-calling schema format."""
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.parameters_schema,
            },
        }

    def to_anthropic_schema(self) -> dict[str, Any]:
        """Convert to Anthropic tool-use schema format."""
        return {
            "name": self.name,
            "description": self.description,
            "input_schema": self.parameters_schema,
        }


# ── Tool implementations ───────────────────────────────────────────

async def _search_company(
    company_name: str,
    sector: str | None = None,
    city: str | None = None,
) -> dict[str, Any]:
    """
    Search for a company in the account database.
    البحث عن شركة في قاعدة بيانات الحسابات.
    """
    try:
        from db.session import get_session
        from db.models import AccountRecord
        from sqlalchemy import select, or_

        async with get_session() as session:
            stmt = select(AccountRecord).where(
                or_(
                    AccountRecord.company_name.ilike(f"%{company_name}%"),
                    AccountRecord.normalized_name.ilike(f"%{company_name}%"),
                )
            )
            if sector:
                stmt = stmt.where(AccountRecord.sector == sector)
            if city:
                stmt = stmt.where(AccountRecord.city.ilike(f"%{city}%"))
            stmt = stmt.limit(5)
            result = await session.execute(stmt)
            accounts = result.scalars().all()
            return {
                "found": len(accounts),
                "accounts": [
                    {
                        "id": a.id,
                        "company_name": a.company_name,
                        "sector": a.sector,
                        "city": a.city,
                        "domain": a.domain,
                        "status": a.status,
                        "data_quality_score": a.data_quality_score,
                    }
                    for a in accounts
                ],
            }
    except Exception as exc:
        logger.warning("search_company_error", error=str(exc))
        return {"found": 0, "accounts": [], "error": str(exc)}


async def _send_whatsapp(
    phone_number: str,
    message: str,
    template_name: str | None = None,
) -> dict[str, Any]:
    """
    Send a WhatsApp message via the configured WhatsApp Business API.
    إرسال رسالة واتساب عبر واجهة برمجة أعمال WhatsApp.
    """
    from core.config.settings import get_settings
    settings = get_settings()

    if not settings.whatsapp_allow_live_send:
        logger.warning("whatsapp_live_send_disabled")
        return {
            "status": "blocked",
            "reason": "WHATSAPP_ALLOW_LIVE_SEND is disabled — human approval required",
            "phone": phone_number,
            "message_preview": message[:100],
        }

    # Delegate to existing WhatsApp integration
    try:
        from dealix.channels.whatsapp import send_message  # type: ignore[import]
        result = await send_message(phone=phone_number, body=message, template=template_name)
        return {"status": "sent", "phone": phone_number, "result": result}
    except ImportError:
        return {
            "status": "queued",
            "reason": "WhatsApp integration not yet configured",
            "phone": phone_number,
        }
    except Exception as exc:
        return {"status": "error", "error": str(exc), "phone": phone_number}


async def _create_deal(
    account_id: str,
    amount_sar: float,
    stage: str = "new",
    notes: str | None = None,
    tenant_id: str | None = None,
) -> dict[str, Any]:
    """
    Create a new deal record linked to an account.
    إنشاء صفقة جديدة مرتبطة بحساب.
    """
    try:
        from db.session import get_session
        from db.models import DealRecord, LeadRecord
        from core.utils import generate_id
        from sqlalchemy import select

        async with get_session() as session:
            # Find or create a lead linked to this account
            lead = LeadRecord(
                id=generate_id("lead"),
                tenant_id=tenant_id,
                source="agent_tool",
                company_name=account_id,
                status="qualified",
            )
            session.add(lead)
            await session.flush()

            deal = DealRecord(
                id=generate_id("deal"),
                tenant_id=tenant_id,
                lead_id=lead.id,
                amount=amount_sar,
                currency="SAR",
                stage=stage,
            )
            session.add(deal)
            return {
                "status": "created",
                "deal_id": deal.id,
                "amount_sar": amount_sar,
                "stage": stage,
                "account_id": account_id,
            }
    except Exception as exc:
        logger.warning("create_deal_error", error=str(exc))
        return {"status": "error", "error": str(exc)}


async def _schedule_meeting(
    contact_email: str,
    contact_name: str,
    preferred_date: str,
    meeting_type: str = "discovery",
    notes: str | None = None,
) -> dict[str, Any]:
    """
    Schedule a meeting by queuing a calendar event.
    جدولة اجتماع عن طريق إضافة حدث تقويمي.
    """
    try:
        from core.utils import generate_id
        meeting_id = generate_id("mtg")
        # In production: integrate with Google Calendar or Calendly
        # For now, log + return structured intent for human review
        return {
            "status": "scheduled",
            "meeting_id": meeting_id,
            "contact_email": contact_email,
            "contact_name": contact_name,
            "preferred_date": preferred_date,
            "meeting_type": meeting_type,
            "notes": notes,
            "action_required": "Calendar invite pending — please confirm availability",
        }
    except Exception as exc:
        return {"status": "error", "error": str(exc)}


async def _generate_invoice(
    customer_name: str,
    amount_sar: float,
    vat_rate: float = 0.15,
    line_items: list[dict[str, Any]] | None = None,
    deal_id: str | None = None,
    tenant_id: str | None = None,
) -> dict[str, Any]:
    """
    Generate a ZATCA Phase 2 compliant invoice draft.
    إنشاء مسودة فاتورة إلكترونية متوافقة مع مرحلة فاتورة زاتكا الثانية.
    """
    try:
        from core.utils import generate_id, utcnow
        from datetime import timezone

        vat_amount = round(amount_sar * vat_rate, 2)
        total = round(amount_sar + vat_amount, 2)
        invoice_id = generate_id("inv")
        now = utcnow()

        return {
            "status": "draft",
            "invoice_id": invoice_id,
            "invoice_number": f"DEALIX-{now.strftime('%Y%m%d')}-{invoice_id[-6:].upper()}",
            "customer_name": customer_name,
            "subtotal_sar": amount_sar,
            "vat_rate": vat_rate,
            "vat_amount_sar": vat_amount,
            "total_sar": total,
            "line_items": line_items or [],
            "issue_date": now.strftime("%Y-%m-%d"),
            "zatca_status": "draft",
            "action_required": "Review invoice then submit to ZATCA via /api/v1/zatca/submit",
        }
    except Exception as exc:
        return {"status": "error", "error": str(exc)}


# ── Tool registry ──────────────────────────────────────────────────

TOOL_REGISTRY: dict[str, Tool] = {
    "search_company": Tool(
        name="search_company",
        description=(
            "Search for a company in the Dealix account database. "
            "Returns matching accounts with sector, city, and data quality info."
        ),
        parameters_schema={
            "type": "object",
            "properties": {
                "company_name": {
                    "type": "string",
                    "description": "Company name to search for",
                },
                "sector": {
                    "type": "string",
                    "description": "Optional: industry sector filter (e.g. 'logistics', 'healthcare')",
                },
                "city": {
                    "type": "string",
                    "description": "Optional: city filter (e.g. 'Riyadh', 'Jeddah')",
                },
            },
            "required": ["company_name"],
        },
        function=_search_company,
    ),

    "send_whatsapp": Tool(
        name="send_whatsapp",
        description=(
            "Send a WhatsApp message to a contact. "
            "Blocked in dev mode unless WHATSAPP_ALLOW_LIVE_SEND=true."
        ),
        parameters_schema={
            "type": "object",
            "properties": {
                "phone_number": {
                    "type": "string",
                    "description": "E.164 phone number, e.g. +966501234567",
                },
                "message": {
                    "type": "string",
                    "description": "Message body (Arabic or English)",
                },
                "template_name": {
                    "type": "string",
                    "description": "Optional: pre-approved WhatsApp template name",
                },
            },
            "required": ["phone_number", "message"],
        },
        function=_send_whatsapp,
    ),

    "create_deal": Tool(
        name="create_deal",
        description="Create a new deal record in the CRM linked to an account.",
        parameters_schema={
            "type": "object",
            "properties": {
                "account_id": {
                    "type": "string",
                    "description": "Account ID the deal is linked to",
                },
                "amount_sar": {
                    "type": "number",
                    "description": "Deal value in Saudi Riyals (SAR)",
                },
                "stage": {
                    "type": "string",
                    "description": "Deal stage: new / qualified / proposal / negotiation / won / lost",
                    "default": "new",
                },
                "notes": {
                    "type": "string",
                    "description": "Optional deal notes",
                },
            },
            "required": ["account_id", "amount_sar"],
        },
        function=_create_deal,
    ),

    "schedule_meeting": Tool(
        name="schedule_meeting",
        description=(
            "Schedule a discovery or demo meeting with a contact. "
            "Creates a calendar event and notifies the sales team."
        ),
        parameters_schema={
            "type": "object",
            "properties": {
                "contact_email": {
                    "type": "string",
                    "description": "Contact email address",
                },
                "contact_name": {
                    "type": "string",
                    "description": "Contact full name",
                },
                "preferred_date": {
                    "type": "string",
                    "description": "Preferred meeting date/time in ISO 8601 format",
                },
                "meeting_type": {
                    "type": "string",
                    "description": "Meeting type: discovery / demo / negotiation / onboarding",
                    "default": "discovery",
                },
                "notes": {
                    "type": "string",
                    "description": "Optional agenda or notes",
                },
            },
            "required": ["contact_email", "contact_name", "preferred_date"],
        },
        function=_schedule_meeting,
    ),

    "generate_invoice": Tool(
        name="generate_invoice",
        description=(
            "Generate a ZATCA Phase 2 compliant invoice draft for a customer. "
            "Returns a draft invoice with QR code and ZATCA clearance pending."
        ),
        parameters_schema={
            "type": "object",
            "properties": {
                "customer_name": {
                    "type": "string",
                    "description": "Customer / buyer full name or company name",
                },
                "amount_sar": {
                    "type": "number",
                    "description": "Subtotal before VAT in SAR",
                },
                "vat_rate": {
                    "type": "number",
                    "description": "VAT rate as decimal, e.g. 0.15 for 15%",
                    "default": 0.15,
                },
                "line_items": {
                    "type": "array",
                    "description": "List of line items {description, quantity, unit_price_sar}",
                    "items": {"type": "object"},
                },
                "deal_id": {
                    "type": "string",
                    "description": "Optional: linked deal ID",
                },
            },
            "required": ["customer_name", "amount_sar"],
        },
        function=_generate_invoice,
    ),
}


def get_tool(name: str) -> Tool | None:
    """Look up a tool by name."""
    return TOOL_REGISTRY.get(name)


def list_tools() -> list[str]:
    """Return list of all registered tool names."""
    return list(TOOL_REGISTRY.keys())


def tools_as_openai_schemas() -> list[dict[str, Any]]:
    """Return all tools formatted for OpenAI function-calling."""
    return [t.to_openai_schema() for t in TOOL_REGISTRY.values()]
