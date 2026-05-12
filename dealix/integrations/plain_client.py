"""
Plain.com support ticketing — GraphQL client + Resend-email fallback.

Why Plain: B2B-SaaS-first support tool with GraphQL, multilingual UI,
and modern API. Cheaper than Intercom for our scale. Free tier is
sufficient for the first ~100 customers.

Public surface:
    PlainClient().create_thread(...)
    PlainClient().add_message(thread_id, ...)
    PlainClient().is_configured

Falls back to email-via-Resend (existing integration) when PLAIN_API_KEY
is unset so support never silently 5xx's a paying customer.

Reference: https://www.plain.com/docs/api-reference
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any

import httpx

from core.logging import get_logger

log = get_logger(__name__)

_GRAPHQL_URL = "https://core-api.uk.plain.com/graphql/v1"


@dataclass
class TicketResult:
    success: bool
    transport: str  # "plain" | "resend" | "noop"
    thread_id: str | None = None
    error: str | None = None


class PlainClient:
    def __init__(self, api_key: str | None = None) -> None:
        self.api_key = (api_key or os.getenv("PLAIN_API_KEY", "")).strip()
        self.workspace_id = os.getenv("PLAIN_WORKSPACE_ID", "").strip()

    @property
    def is_configured(self) -> bool:
        return bool(self.api_key)

    def _headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    async def _graphql(
        self, query: str, variables: dict[str, Any]
    ) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=15) as c:
            r = await c.post(
                _GRAPHQL_URL,
                headers=self._headers(),
                json={"query": query, "variables": variables},
            )
            r.raise_for_status()
            data = r.json()
            if data.get("errors"):
                raise RuntimeError(str(data["errors"]))
            return data["data"]

    async def upsert_customer(
        self, *, email: str, full_name: str, tenant_id: str | None = None
    ) -> str:
        """Create or update a Plain customer; returns Plain customer ID."""
        if not self.is_configured:
            raise RuntimeError("plain_not_configured")
        mutation = """
        mutation UpsertCustomer($input: UpsertCustomerInput!) {
          upsertCustomer(input: $input) {
            customer { id }
            error { message }
          }
        }
        """
        variables = {
            "input": {
                "identifier": {"emailAddress": email},
                "onCreate": {
                    "fullName": full_name,
                    "email": {"email": email, "isVerified": False},
                    "externalId": tenant_id or "",
                },
                "onUpdate": {"fullName": {"value": full_name}},
            }
        }
        data = await self._graphql(mutation, variables)
        result = data.get("upsertCustomer") or {}
        if result.get("error"):
            raise RuntimeError(result["error"]["message"])
        return result["customer"]["id"]

    async def create_thread(
        self,
        *,
        customer_email: str,
        customer_name: str,
        title: str,
        body_markdown: str,
        tenant_id: str | None = None,
        labels: list[str] | None = None,
    ) -> TicketResult:
        """Open a new Plain thread; falls back to Resend email if unconfigured."""
        if not self.is_configured:
            return await _fallback_email(
                customer_email=customer_email,
                customer_name=customer_name,
                title=title,
                body=body_markdown,
                tenant_id=tenant_id,
            )
        try:
            customer_id = await self.upsert_customer(
                email=customer_email,
                full_name=customer_name,
                tenant_id=tenant_id,
            )
            mutation = """
            mutation CreateThread($input: CreateThreadInput!) {
              createThread(input: $input) {
                thread { id }
                error { message }
              }
            }
            """
            components = [
                {"componentText": {"text": body_markdown}},
            ]
            variables = {
                "input": {
                    "customerIdentifier": {"customerId": customer_id},
                    "title": title,
                    "components": components,
                    "labelTypeIds": labels or [],
                }
            }
            data = await self._graphql(mutation, variables)
            res = data.get("createThread") or {}
            if res.get("error"):
                raise RuntimeError(res["error"]["message"])
            return TicketResult(
                success=True,
                transport="plain",
                thread_id=res["thread"]["id"],
            )
        except Exception as exc:
            log.exception(
                "plain_create_thread_failed",
                tenant_id=tenant_id,
                email=customer_email,
            )
            # Fall back to email so the customer isn't lost.
            res = await _fallback_email(
                customer_email=customer_email,
                customer_name=customer_name,
                title=title,
                body=body_markdown,
                tenant_id=tenant_id,
            )
            res.error = f"plain_failed_falling_back: {exc}"
            return res


async def _fallback_email(
    *,
    customer_email: str,
    customer_name: str,
    title: str,
    body: str,
    tenant_id: str | None,
) -> TicketResult:
    """Send via Resend (existing integration) when Plain is unconfigured."""
    try:
        from integrations.email import EmailClient
    except Exception:
        return TicketResult(success=False, transport="noop", error="email_unavailable")
    support_to = os.getenv("SUPPORT_INBOX_EMAIL", "support@ai-company.sa").strip()
    full_body = (
        f"New support ticket from {customer_name} <{customer_email}>\n"
        f"Tenant: {tenant_id or '-'}\n"
        f"Subject: {title}\n\n"
        f"{body}\n"
    )
    try:
        client = EmailClient()
        result = await client.send(
            to=support_to,
            subject=f"[Support] {title}",
            body_text=full_body,
            reply_to=customer_email,
        )
        return TicketResult(
            success=bool(getattr(result, "success", True)),
            transport="resend",
            thread_id=getattr(result, "message_id", None),
        )
    except Exception as exc:
        log.exception("support_email_fallback_failed", tenant_id=tenant_id)
        return TicketResult(success=False, transport="noop", error=str(exc))


_singleton: PlainClient | None = None


def get_plain_client() -> PlainClient:
    global _singleton
    if _singleton is None:
        _singleton = PlainClient()
    return _singleton
