"""Customer-facing chat — KB-grounded answers, escalation otherwise."""

from __future__ import annotations

from fastapi import APIRouter
from pydantic import BaseModel

from auto_client_acquisition.chat import respond

router = APIRouter(prefix="/api/v1/chat", tags=["chat"])


class ChatMessage(BaseModel):
    message: str
    customer_id: str | None = None
    tenant_id: str | None = None


@router.get("/status")
async def status() -> dict:
    return {
        "module": "chat",
        "guardrails": {
            "answers_only_from_approved_kb": True,
            "no_kb_match_escalates_to_ticket": True,
            "never_improvises": True,
        },
    }


@router.post("/message")
async def chat_message(body: ChatMessage) -> dict:
    return respond(
        body.message,
        channel="chat_widget",
        customer_id=body.customer_id,
        tenant_id=body.tenant_id,
    )
