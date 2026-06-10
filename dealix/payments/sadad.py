"""
SADAD Client — integrates with SADAD bill presentment and payment (Saudi bank transfer).
عميل سداد — يتكامل مع نظام سداد للفواتير والمدفوعات (تحويل بنكي سعودي).
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Any

from core.logging import get_logger
from core.utils import generate_id, utcnow

logger = get_logger(__name__)


@dataclass
class Bill:
    id: str
    biller_id: str
    customer_id: str
    amount_sar: float
    status: str = "pending"
    sadad_reference: str = ""
    due_date: datetime | None = None
    paid_at: datetime | None = None
    created_at: datetime = field(default_factory=utcnow)

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "biller_id": self.biller_id,
            "customer_id": self.customer_id,
            "amount_sar": self.amount_sar,
            "status": self.status,
            "sadad_reference": self.sadad_reference,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "paid_at": self.paid_at.isoformat() if self.paid_at else None,
            "created_at": self.created_at.isoformat(),
        }


@dataclass
class PaymentStatus:
    bill_id: str
    status: str
    sadad_reference: str = ""
    amount_sar: float = 0.0
    paid_at: datetime | None = None
    error_message: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "bill_id": self.bill_id,
            "status": self.status,
            "sadad_reference": self.sadad_reference,
            "amount_sar": self.amount_sar,
            "paid_at": self.paid_at.isoformat() if self.paid_at else None,
            "error_message": self.error_message,
        }


class SADADClient:
    def __init__(self):
        self._biller_id = os.getenv("SADAD_BILLER_ID", "DEALIX001")
        self._api_key = os.getenv("SADAD_API_KEY", "")
        self._sandbox = os.getenv("SADAD_SANDBOX", "1") == "1"
        self._bills: dict[str, Bill] = {}
        self.log = logger.bind(component="sadad")

        if not self._api_key:
            self.log.warning("sadad_not_configured", message="SADAD_API_KEY not set")

    async def create_bill(self, amount: float, customer_id: str) -> Bill:
        if amount <= 0:
            raise ValueError("Amount must be positive")

        bill = Bill(
            id=generate_id("sad"),
            biller_id=self._biller_id,
            customer_id=customer_id,
            amount_sar=amount,
            status="pending",
            sadad_reference=f"SAD-{generate_id('ref')}",
            due_date=utcnow() + timedelta(days=30),
        )
        self._bills[bill.id] = bill
        self.log.info("sadad_bill_created", id=bill.id, customer=customer_id, amount=amount)
        return bill

    async def check_payment(self, bill_id: str) -> PaymentStatus:
        bill = self._bills.get(bill_id)
        if not bill:
            return PaymentStatus(
                bill_id=bill_id,
                status="not_found",
            )

        return PaymentStatus(
            bill_id=bill_id,
            status=bill.status,
            sadad_reference=bill.sadad_reference,
            amount_sar=bill.amount_sar,
            paid_at=bill.paid_at,
        )

    async def confirm_payment(self, bill_id: str) -> bool:
        bill = self._bills.get(bill_id)
        if not bill:
            return False

        bill.status = "paid"
        bill.paid_at = utcnow()
        self.log.info("sadad_payment_confirmed", bill_id=bill_id)
        return True

    def get_bill(self, bill_id: str) -> Bill | None:
        return self._bills.get(bill_id)

    def get_pending_bills(self) -> list[Bill]:
        return [b for b in self._bills.values() if b.status == "pending"]

    def get_stats(self) -> dict[str, Any]:
        bills = self._bills.values()
        return {
            "total_bills": len(bills),
            "pending": sum(1 for b in bills if b.status == "pending"),
            "paid": sum(1 for b in bills if b.status == "paid"),
            "total_amount_sar": sum(b.amount_sar for b in bills),
            "collected_amount_sar": sum(b.amount_sar for b in bills if b.status == "paid"),
        }
