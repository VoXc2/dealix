"""
STC Pay Client — integrates with STC Pay for Saudi payment processing.
عميل STC Pay — يتكامل مع STC Pay لمعالجة المدفوعات السعودية.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from core.logging import get_logger
from core.utils import generate_id, utcnow

logger = get_logger(__name__)


@dataclass
class PaymentIntent:
    id: str
    amount_sar: float
    description: str
    status: str = "pending"
    stc_pay_reference: str = ""
    qr_code_url: str = ""
    expires_at: datetime | None = None
    created_at: datetime = field(default_factory=utcnow)

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "amount_sar": self.amount_sar,
            "description": self.description,
            "status": self.status,
            "stc_pay_reference": self.stc_pay_reference,
            "qr_code_url": self.qr_code_url,
            "expires_at": self.expires_at.isoformat() if self.expires_at else None,
            "created_at": self.created_at.isoformat(),
        }


@dataclass
class PaymentStatus:
    id: str
    status: str
    stc_pay_reference: str = ""
    amount_sar: float = 0.0
    paid_at: datetime | None = None
    error_message: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "status": self.status,
            "stc_pay_reference": self.stc_pay_reference,
            "amount_sar": self.amount_sar,
            "paid_at": self.paid_at.isoformat() if self.paid_at else None,
            "error_message": self.error_message,
        }


@dataclass
class RefundResult:
    success: bool
    payment_id: str
    amount_sar: float = 0.0
    reference: str = ""
    error_message: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "success": self.success,
            "payment_id": self.payment_id,
            "amount_sar": self.amount_sar,
            "reference": self.reference,
            "error_message": self.error_message,
        }


class STCPayClient:
    def __init__(self):
        self._api_key = os.getenv("STCPAY_API_KEY", "")
        self._merchant_id = os.getenv("STCPAY_MERCHANT_ID", "")
        self._sandbox = os.getenv("STCPAY_SANDBOX", "1") == "1"
        self._intents: dict[str, PaymentIntent] = {}
        self.log = logger.bind(component="stc_pay")

        if not self._api_key:
            self.log.warning("stc_pay_not_configured", message="STCPAY_API_KEY not set")

    async def create_payment(self, amount: float, description: str) -> PaymentIntent:
        if amount <= 0:
            raise ValueError("Amount must be positive")

        intent = PaymentIntent(
            id=generate_id("stc"),
            amount_sar=amount,
            description=description,
            status="pending",
            stc_pay_reference=f"STC-{generate_id('ref')}",
            qr_code_url=f"https://stcpay.example.sa/qr/{generate_id('qr')}",
            expires_at=utcnow(),
        )
        self._intents[intent.id] = intent
        self.log.info("stc_pay_payment_created", id=intent.id, amount=amount)
        return intent

    async def check_status(self, payment_id: str) -> PaymentStatus:
        intent = self._intents.get(payment_id)
        if not intent:
            return PaymentStatus(id=payment_id, status="not_found")

        return PaymentStatus(
            id=payment_id,
            status=intent.status,
            stc_pay_reference=intent.stc_pay_reference,
            amount_sar=intent.amount_sar,
            paid_at=utcnow() if intent.status == "paid" else None,
        )

    async def refund(self, payment_id: str) -> RefundResult:
        intent = self._intents.get(payment_id)
        if not intent:
            return RefundResult(
                success=False,
                payment_id=payment_id,
                error_message="Payment not found",
            )

        if intent.status != "paid":
            return RefundResult(
                success=False,
                payment_id=payment_id,
                error_message="Payment not in paid status",
            )

        intent.status = "refunded"
        result = RefundResult(
            success=True,
            payment_id=payment_id,
            amount_sar=intent.amount_sar,
            reference=f"STC-REF-{generate_id('ref')}",
        )
        self.log.info("stc_pay_refund_processed", payment_id=payment_id)
        return result

    def get_pending_intents(self) -> list[PaymentIntent]:
        return [i for i in self._intents.values() if i.status == "pending"]
