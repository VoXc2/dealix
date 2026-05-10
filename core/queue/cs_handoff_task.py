"""CS handoff task — queued from Moyasar reconciliation.

Track C5 of 30-day plan. Triggered when a payment is confirmed:

1. Send welcome email (via Resend) — NOT a marketing message;
   transactional, account confirmation only.
2. Bootstrap Customer Brain entry with paid status.
3. Notify founder via WhatsApp Decision card (if configured).

Hard rules:
  - Welcome email = transactional only (PDPL allows post-consent)
  - NO_FAKE_REVENUE — only fires when reconcile_payment returned a
    valid invoice_id + evidence_ref
  - Founder notification is informational — NOT an external send
"""

from __future__ import annotations

import logging
from datetime import UTC, datetime
from typing import Any

logger = logging.getLogger(__name__)


def enqueue_cs_handoff(
    customer_handle: str,
    invoice_id: str,
    amount_sar: float,
) -> str:
    """Enqueue a CS handoff job.

    Falls back to synchronous logging when ARQ Redis isn't reachable.
    Returns a logical job_id for the audit trail.
    """
    job_id = f"cs_{customer_handle}_{int(datetime.now(UTC).timestamp())}"
    payload = {
        "customer_handle": customer_handle,
        "invoice_id": invoice_id,
        "amount_sar": amount_sar,
        "queued_at": datetime.now(UTC).isoformat(),
    }
    try:
        from core.queue.tasks import enqueue_task  # type: ignore

        enqueue_task("cs_handoff", payload)
        return job_id
    except (ImportError, AttributeError):
        # ARQ isn't wired up in this env (test, smoke, no Redis) — log
        # the handoff so it can be replayed manually.
        logger.info(
            "cs_handoff_synchronous_fallback: %s",
            payload,
        )
        return job_id


async def cs_handoff_handler(
    ctx: dict[str, Any],
    customer_handle: str,
    invoice_id: str,
    amount_sar: float,
    **kwargs: Any,
) -> dict[str, Any]:
    """ARQ task handler. Idempotent.

    Returns a dict the worker can log. Never raises — failures are
    surfaced as `errors: [...]` so the founder gets a Slack ping
    rather than a silent crash.
    """
    started = datetime.now(UTC)
    errors: list[str] = []

    # Step 1 — welcome email (transactional)
    welcome_sent = False
    try:
        from auto_client_acquisition.email.transactional_send import (  # type: ignore
            send_welcome_email,
        )
    except ImportError:
        logger.info("cs_handoff: email module not available — skipping welcome email")
    else:
        try:
            send_welcome_email(
                customer_handle=customer_handle,
                amount_sar=amount_sar,
                invoice_id=invoice_id,
            )
            welcome_sent = True
        except Exception as exc:  # noqa: BLE001
            errors.append(f"welcome_email: {exc}")

    # Step 2 — Customer Brain bootstrap
    brain_bootstrapped = False
    try:
        from auto_client_acquisition.customer_brain import (  # type: ignore
            mark_paid,
        )
    except ImportError:
        logger.info("cs_handoff: customer_brain not available — skipping bootstrap")
    else:
        try:
            mark_paid(
                customer_handle=customer_handle,
                amount_sar=amount_sar,
                invoice_id=invoice_id,
            )
            brain_bootstrapped = True
        except Exception as exc:  # noqa: BLE001
            errors.append(f"customer_brain: {exc}")

    # Step 3 — founder WhatsApp notification (informational, NOT external send)
    founder_notified = False
    try:
        from auto_client_acquisition.personal_operator.whatsapp_cards import (  # type: ignore
            queue_founder_notification,
        )
    except ImportError:
        logger.info("cs_handoff: whatsapp_cards not available — skipping notification")
    else:
        try:
            queue_founder_notification(
                title="✓ Payment confirmed",
                body=(
                    f"{customer_handle} دفع {amount_sar:,.0f} SAR · "
                    f"invoice {invoice_id}. CS handoff started."
                ),
            )
            founder_notified = True
        except Exception as exc:  # noqa: BLE001
            errors.append(f"founder_notification: {exc}")

    return {
        "job": "cs_handoff",
        "customer_handle": customer_handle,
        "invoice_id": invoice_id,
        "amount_sar": amount_sar,
        "welcome_sent": welcome_sent,
        "brain_bootstrapped": brain_bootstrapped,
        "founder_notified": founder_notified,
        "errors": errors,
        "started_at": started.isoformat(),
        "duration_ms": int((datetime.now(UTC) - started).total_seconds() * 1000),
    }
