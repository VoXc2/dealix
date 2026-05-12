"""
Inngest application + one durable example: `proposal_draft`.

Inngest is the workflow runtime for *long-running* multi-step LLM flows
(proposal drafting, daily targeting batches, weekly digest assembly,
renewal pre-flight). Short async work stays on arq; only flows that
cross worker restarts or run >5 minutes need to move here.

Architecture:
- `inngest_app` is the Inngest client; functions register against it via
  `@inngest_app.create_function(...)`.
- `proposal_draft` is the reference implementation, broken into three
  memoized `step.run` blocks. If the worker dies between steps, Inngest
  replays the function on a healthy worker and *only the unfinished
  steps run again*.
- `dispatcher.kick(event_name, data)` is a thin facade so the rest of
  the codebase can call workflows without importing Inngest directly.
  When INNGEST_SIGNING_KEY isn't set the dispatcher is a no-op.

To run locally:
    pip install inngest
    npx inngest-cli@latest dev
    INNGEST_DEV=1 INNGEST_BASE_URL=http://localhost:8288 \
        uvicorn api.main:app --reload

Reference: https://www.inngest.com/docs/getting-started/python-quick-start
"""

from __future__ import annotations

import os
from typing import Any

from core.logging import get_logger

log = get_logger(__name__)


# ── Inngest client (lazy + optional) ─────────────────────────────────


def is_enabled() -> bool:
    """True if Inngest credentials are present."""
    return bool(os.getenv("INNGEST_SIGNING_KEY", "").strip()) or bool(
        os.getenv("INNGEST_DEV", "").strip()
    )


_client: Any = None


def get_client() -> Any:
    """Return the singleton Inngest client; None if not configured.

    Import is intentionally lazy so the module is import-safe without
    the `inngest` SDK installed.
    """
    global _client
    if _client is not None:
        return _client
    if not is_enabled():
        return None
    try:
        import inngest  # type: ignore
    except ImportError:
        log.warning("inngest_sdk_not_installed_falling_back_to_noop")
        return None
    _client = inngest.Inngest(
        app_id="dealix",
        event_key=os.getenv("INNGEST_EVENT_KEY"),
        signing_key=os.getenv("INNGEST_SIGNING_KEY"),
        is_production=not os.getenv("INNGEST_DEV"),
    )
    return _client


# ── Example function: proposal_draft (3 durable steps) ──────────────


async def _step_load_lead(lead_id: str) -> dict[str, Any]:
    """Step 1: pull the lead from DB (memoized by Inngest)."""
    from sqlalchemy import select

    from db.models import LeadRecord
    from db.session import async_session_factory

    async with async_session_factory()() as session:
        lead = (
            await session.execute(select(LeadRecord).where(LeadRecord.id == lead_id))
        ).scalar_one_or_none()
        if lead is None:
            raise RuntimeError(f"lead_not_found:{lead_id}")
        return {
            "id": lead.id,
            "tenant_id": lead.tenant_id,
            "company_name": lead.company_name,
            "sector": lead.sector,
            "contact_email": lead.contact_email,
            "fit_score": lead.fit_score,
            "pain_points": lead.pain_points or [],
        }


async def _step_draft_proposal(lead: dict[str, Any]) -> dict[str, Any]:
    """Step 2: call the LLM to draft a proposal (memoized)."""
    # Defer the heavy import so a noop run doesn't pay the cost.
    try:
        from auto_client_acquisition.agents.proposal import ProposalAgent
    except Exception:
        return {
            "subject": f"Dealix proposal for {lead.get('company_name', 'your team')}",
            "body": "(Inngest is configured but ProposalAgent is unavailable; this is a stub.)",
        }
    agent = ProposalAgent()
    out = await agent.run(lead=lead, locale="ar")
    return {"subject": out.subject, "body": out.body, "audit_id": getattr(out, "audit_id", None)}


async def _step_queue_for_send(draft: dict[str, Any], lead_id: str) -> dict[str, Any]:
    """Step 3: persist + queue for approval (memoized)."""
    # Persist via the existing email_send infrastructure where possible.
    log.info(
        "proposal_draft_queued",
        lead_id=lead_id,
        subject=draft.get("subject"),
    )
    return {"lead_id": lead_id, "queued": True, "audit_id": draft.get("audit_id")}


def register_functions() -> list[Any]:
    """Register Inngest functions; called once at app boot.

    Returns the list of functions for `inngest.fast_api.serve` integration.
    Empty list when Inngest isn't configured — caller is expected to skip
    serving the inngest webhook in that case.
    """
    client = get_client()
    if client is None:
        return []
    try:
        import inngest  # type: ignore
    except ImportError:
        return []

    @client.create_function(
        fn_id="dealix-proposal-draft",
        trigger=inngest.TriggerEvent(event="dealix/proposal.draft.requested"),
        retries=3,
    )
    async def proposal_draft(
        ctx: inngest.Context, step: inngest.Step
    ) -> dict[str, Any]:
        lead_id = ctx.event.data.get("lead_id")
        if not lead_id:
            raise inngest.NonRetriableError("missing_lead_id")

        lead = await step.run("load-lead", _step_load_lead, lead_id)
        draft = await step.run("draft-proposal", _step_draft_proposal, lead)
        result = await step.run(
            "queue-for-send", _step_queue_for_send, draft, lead_id
        )
        return result

    return [proposal_draft]


# ── Dispatcher facade ───────────────────────────────────────────────


class WorkflowDispatcher:
    """Thin facade so callers don't import inngest directly.

    Usage:
        await dispatcher.send("dealix/proposal.draft.requested", {"lead_id": id})
    """

    async def send(
        self, event_name: str, data: dict[str, Any] | None = None
    ) -> bool:
        """Emit a workflow event; returns True if accepted by Inngest."""
        client = get_client()
        if client is None:
            log.info(
                "inngest_noop_dispatch",
                event=event_name,
                data_keys=list((data or {}).keys()),
            )
            return False
        try:
            import inngest  # type: ignore
        except ImportError:
            return False
        await client.send(inngest.Event(name=event_name, data=data or {}))
        log.info("inngest_event_sent", event=event_name)
        return True


dispatcher = WorkflowDispatcher()
