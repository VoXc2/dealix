"""Payment Event Handler — governs the complete payment lifecycle.

Triggered by Moyasar webhook after payment confirmation.
Orchestrates: ZATCA invoice → onboarding creation → founder alert.

Constitutional gates:
- APPROVAL_FIRST: founder alert generated (not auto-acted)
- NO_AUTO_ZATCA_BLOCK: payment never blocked by ZATCA failure
- NO_PII_IN_LOGS: customer payment details never logged
"""

from __future__ import annotations

import logging
import uuid
from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, Field

log = logging.getLogger(__name__)


class PaymentEvent(BaseModel):
    """Normalized payment event from Moyasar webhook."""
    event_id: str = Field(default_factory=lambda: f"evt_{uuid.uuid4().hex[:12]}")
    payment_id: str
    invoice_id: str
    status: str  # paid | failed | refunded
    amount_sar: float
    amount_halalas: int
    service_tier: str = ""
    account_id: str = ""
    customer_name: str = ""
    customer_email: str = ""
    metadata: dict[str, str] = Field(default_factory=dict)
    occurred_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    is_live_mode: bool = False


class PaymentEventResult(BaseModel):
    event_id: str
    payment_id: str
    payment_status: str
    zatca_result: dict[str, Any] = Field(default_factory=dict)
    onboarding_created: bool = False
    onboarding_id: str = ""
    founder_alert_generated: bool = False
    founder_alert_ar: str = ""
    processed_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class PaymentEventProcessor:
    """Processes payment events after Moyasar webhook confirmation."""

    async def process(self, event: PaymentEvent) -> PaymentEventResult:
        """Process a confirmed payment event.

        Steps:
        1. Validate event
        2. Issue ZATCA e-invoice (non-blocking)
        3. Create onboarding record
        4. Generate founder alert draft
        """
        result = PaymentEventResult(
            event_id=event.event_id,
            payment_id=event.payment_id,
            payment_status=event.status,
        )

        if event.status != "paid":
            log.info(
                "payment_event_not_paid event_id=%s status=%s",
                event.event_id, event.status,
            )
            return result

        # Step 1: ZATCA e-invoice (non-blocking)
        zatca_result = await self._issue_zatca(event)
        result.zatca_result = zatca_result

        # Step 2: Create onboarding record
        if event.account_id and event.customer_name:
            onboarding_id = await self._create_onboarding(event)
            if onboarding_id:
                result.onboarding_created = True
                result.onboarding_id = onboarding_id

        # Step 3: Generate founder alert
        alert_ar = self._build_founder_alert(event)
        result.founder_alert_generated = bool(alert_ar)
        result.founder_alert_ar = alert_ar

        log.info(
            "payment_processed event_id=%s amount_sar=%.2f zatca=%s onboarding=%s",
            event.event_id,
            event.amount_sar,
            zatca_result.get("status"),
            result.onboarding_id or "skipped",
        )
        return result

    async def _issue_zatca(self, event: PaymentEvent) -> dict[str, Any]:
        try:
            from dealix.commercial.zatca_invoice import issue_zatca_invoice
            payment_dict = {
                "id": event.payment_id,
                "amount": event.amount_halalas,
                "source": {"name": event.customer_name},
            }
            return await issue_zatca_invoice(payment=payment_dict)
        except Exception as exc:
            log.warning("zatca_issue_failed event_id=%s error=%s", event.event_id, exc)
            return {"status": "error", "reason": str(exc)}

    async def _create_onboarding(self, event: PaymentEvent) -> str:
        try:
            from dealix.commercial.onboarding import OnboardingOrchestrator
            orch = OnboardingOrchestrator()
            record = orch.create_onboarding(
                account_id=event.account_id,
                company_name=event.customer_name,
                contact_name=event.metadata.get("contact_name", event.customer_name),
                contact_phone=event.metadata.get("contact_phone", ""),
                service_tier=event.service_tier or "sprint_499",
            )
            return record.onboarding_id
        except Exception as exc:
            log.warning("onboarding_create_failed event_id=%s error=%s", event.event_id, exc)
            return ""

    def _build_founder_alert(self, event: PaymentEvent) -> str:
        tier_names = {
            "sprint_499": "499 SAR Sprint",
            "data_pack_1500": "1,500 SAR Data Pack",
            "managed_ops_2999": "2,999 SAR Managed Ops",
            "managed_ops_4999": "4,999 SAR Managed Ops",
            "custom_ai_15000": "15,000 SAR Custom AI",
        }
        tier_label = tier_names.get(event.service_tier, f"{event.amount_sar} SAR")

        return f"""🎉 دفعة جديدة مؤكدة!

العميل: {event.customer_name}
الباقة: {tier_label}
المبلغ: {event.amount_sar:.0f} ريال
Payment ID: {event.payment_id}

الخطوة التالية:
1. راجع مسودة الترحيب في لوحة التشغيل
2. أرسل بعد الموافقة على رسالة الترحيب
3. حدد موعد جلسة الاستلام خلال 24 ساعة

⚠️ هذا تنبيه للمراجعة — لا إجراء تلقائي"""


def normalize_moyasar_webhook(webhook_body: dict[str, Any]) -> PaymentEvent | None:
    """Convert a raw Moyasar webhook body to a normalized PaymentEvent.

    Returns None if the event is not actionable (e.g., not a payment event).
    """
    event_type = webhook_body.get("type", "")
    if event_type not in ("payment_paid", "payment_failed", "invoice_paid"):
        return None

    payment = webhook_body.get("data", webhook_body)
    amount_halalas = payment.get("amount", 0)
    metadata = payment.get("metadata") or {}

    return PaymentEvent(
        payment_id=str(payment.get("id", "")),
        invoice_id=str(payment.get("invoice_id", payment.get("id", ""))),
        status="paid" if "paid" in event_type else payment.get("status", "unknown"),
        amount_sar=amount_halalas / 100,
        amount_halalas=int(amount_halalas),
        service_tier=metadata.get("service_tier", ""),
        account_id=metadata.get("account_id", ""),
        customer_name=metadata.get("customer_name", ""),
        customer_email=metadata.get("customer_email", ""),
        metadata={k: str(v) for k, v in metadata.items()},
        is_live_mode=bool(webhook_body.get("live_mode", False)),
    )
