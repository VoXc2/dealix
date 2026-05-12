"""
Knock notifications — orchestration layer over email/SMS/in-app/push.

Why Knock: one API for multi-channel transactional notifications with a
hosted preferences center (the customer chooses which workflows email
them vs notify in-app vs SMS them). Replaces ad-hoc Resend calls scattered
across invites, trial, billing.

Public surface:
    KnockClient().is_configured
    await KnockClient().identify(user_id, properties)
    await KnockClient().notify(workflow_key, recipients, data, tenant_id=...)

Falls back to Resend email when KNOCK_API_KEY is unset — every call
must keep working in dev / OSS.

Reference: https://docs.knock.app/reference#trigger-workflow
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any

import httpx

from core.logging import get_logger

log = get_logger(__name__)

_BASE = "https://api.knock.app/v1"


@dataclass
class NotifyResult:
    success: bool
    transport: str
    workflow: str
    error: str | None = None


class KnockClient:
    def __init__(self, api_key: str | None = None) -> None:
        self.api_key = (api_key or os.getenv("KNOCK_API_KEY", "")).strip()

    @property
    def is_configured(self) -> bool:
        return bool(self.api_key)

    def _headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    async def identify(
        self, user_id: str, properties: dict[str, Any]
    ) -> None:
        """Upsert a Knock user record so subsequent notifications resolve recipients."""
        if not self.is_configured:
            return
        async with httpx.AsyncClient(timeout=10) as c:
            await c.put(
                f"{_BASE}/users/{user_id}",
                headers=self._headers(),
                json=properties,
            )

    async def notify(
        self,
        workflow: str,
        recipients: list[str | dict[str, Any]],
        data: dict[str, Any] | None = None,
        *,
        tenant_id: str | None = None,
    ) -> NotifyResult:
        """Trigger a Knock workflow. Falls back to direct email if unconfigured."""
        if not self.is_configured:
            return await _fallback_email(workflow, recipients, data, tenant_id=tenant_id)
        payload: dict[str, Any] = {
            "recipients": recipients,
            "data": data or {},
        }
        if tenant_id:
            payload["actor"] = {"id": f"tenant_{tenant_id}", "collection": "tenants"}
        try:
            async with httpx.AsyncClient(timeout=10) as c:
                r = await c.post(
                    f"{_BASE}/workflows/{workflow}/trigger",
                    headers=self._headers(),
                    json=payload,
                )
                r.raise_for_status()
        except Exception as exc:
            log.exception("knock_trigger_failed", workflow=workflow, tenant_id=tenant_id)
            res = await _fallback_email(
                workflow, recipients, data, tenant_id=tenant_id
            )
            res.error = f"knock_failed: {exc}"
            return res
        log.info(
            "knock_workflow_triggered",
            workflow=workflow,
            tenant_id=tenant_id,
            recipients=len(recipients),
        )
        return NotifyResult(success=True, transport="knock", workflow=workflow)


async def _fallback_email(
    workflow: str,
    recipients: list[str | dict[str, Any]],
    data: dict[str, Any] | None,
    *,
    tenant_id: str | None,
) -> NotifyResult:
    """Send a minimal email via the existing email client."""
    try:
        from integrations.email import EmailClient
    except Exception:
        return NotifyResult(
            success=False,
            transport="noop",
            workflow=workflow,
            error="email_unavailable",
        )
    addresses: list[str] = []
    for r in recipients:
        if isinstance(r, str):
            addresses.append(r)
        elif isinstance(r, dict):
            email = r.get("email") or r.get("id")
            if isinstance(email, str):
                addresses.append(email)
    if not addresses:
        return NotifyResult(
            success=False,
            transport="noop",
            workflow=workflow,
            error="no_recipients",
        )
    body = (
        f"[Knock fallback] workflow={workflow}\n"
        f"tenant_id={tenant_id or '-'}\n\n"
        f"data:\n{data or {}}\n"
    )
    try:
        client = EmailClient()
        await client.send(
            to=addresses[0],
            subject=f"[Dealix] {workflow}",
            body_text=body,
        )
        return NotifyResult(success=True, transport="resend", workflow=workflow)
    except Exception as exc:
        log.exception("knock_fallback_email_failed", workflow=workflow)
        return NotifyResult(
            success=False,
            transport="noop",
            workflow=workflow,
            error=str(exc),
        )


_singleton: KnockClient | None = None


def get_knock_client() -> KnockClient:
    global _singleton
    if _singleton is None:
        _singleton = KnockClient()
    return _singleton
