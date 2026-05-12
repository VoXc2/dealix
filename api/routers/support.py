"""
Customer support tickets — Plain first, Resend email fallback.

Endpoints:
    POST /api/v1/support/tickets   — open a new thread
    GET  /api/v1/support/health    — surfaces which transport is active

Validation: full Pydantic input on the public surface; tenant id resolved
from the auth middleware where possible, otherwise free-form so the
landing-page contact form can also hit this endpoint anonymously.
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Request
from pydantic import BaseModel, EmailStr, Field

from core.logging import get_logger
from dealix.integrations.plain_client import get_plain_client

router = APIRouter(prefix="/api/v1/support", tags=["support"])
log = get_logger(__name__)


class SupportTicketIn(BaseModel):
    email: EmailStr
    name: str = Field(..., min_length=1, max_length=120)
    subject: str = Field(..., min_length=2, max_length=200)
    body: str = Field(..., min_length=2, max_length=10_000)
    tenant_id: str | None = Field(default=None, max_length=64)
    priority: str = Field(default="normal", max_length=16)
    labels: list[str] = Field(default_factory=list, max_length=10)


@router.get("/health")
async def support_health() -> dict[str, Any]:
    client = get_plain_client()
    return {
        "plain_configured": client.is_configured,
        "fallback": "resend_email" if not client.is_configured else None,
    }


@router.post("/tickets")
async def create_support_ticket(
    payload: SupportTicketIn, request: Request
) -> dict[str, Any]:
    """Open a support ticket. Plain when configured, else fall back to email."""
    tenant_id = payload.tenant_id or getattr(request.state, "tenant_id", None)
    client = get_plain_client()
    result = await client.create_thread(
        customer_email=payload.email,
        customer_name=payload.name,
        title=payload.subject,
        body_markdown=payload.body,
        tenant_id=tenant_id,
        labels=payload.labels,
    )
    # Audit ticket creation; tenant_id may be None for anonymous landing
    # submissions — store "anonymous" sentinel so the row still lands.
    try:
        from api.security.audit_writer import audit
        from db.session import async_session_factory

        async with async_session_factory()() as session:
            await audit(
                session,
                action="support.ticket.create",
                entity_type="support_ticket",
                entity_id=result.thread_id,
                tenant_id=tenant_id or "anonymous",
                user_id=getattr(request.state, "user_id", None),
                status="ok" if result.success else "error",
                diff={"subject": payload.subject, "transport": result.transport},
            )
    except Exception:
        log.exception("support_audit_failed")

    log.info(
        "support_ticket_created",
        tenant_id=tenant_id,
        transport=result.transport,
        success=result.success,
        thread_id=result.thread_id,
    )
    return {
        "ok": result.success,
        "transport": result.transport,
        "thread_id": result.thread_id,
        "next_step": (
            "expect_reply_within_one_business_day"
            if result.success
            else "support@ai-company.sa is the human escalation address"
        ),
    }
