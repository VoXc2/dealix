"""
Abstract Payment Gateway — unified interface for all payment providers.
بوابة الدفع المجردة — واجهة موحدة لجميع مزودي الدفع.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any

from core.logging import get_logger

logger = get_logger(__name__)


@dataclass
class PaymentResult:
    success: bool
    payment_id: str = ""
    amount: float = 0.0
    currency: str = "SAR"
    method: str = ""
    gateway_reference: str = ""
    status: str = ""
    error_message: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "success": self.success,
            "payment_id": self.payment_id,
            "amount": self.amount,
            "currency": self.currency,
            "method": self.method,
            "gateway_reference": self.gateway_reference,
            "status": self.status,
            "error_message": self.error_message,
        }


@dataclass
class RefundResult:
    success: bool
    payment_id: str = ""
    amount: float = 0.0
    gateway_reference: str = ""
    error_message: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "success": self.success,
            "payment_id": self.payment_id,
            "amount": self.amount,
            "gateway_reference": self.gateway_reference,
            "error_message": self.error_message,
        }


class PaymentGateway(ABC):
    @abstractmethod
    async def charge(self, amount: float, currency: str, method: str) -> PaymentResult:
        pass

    @abstractmethod
    async def refund(self, payment_id: str) -> RefundResult:
        pass


class MoyasarGateway(PaymentGateway):
    async def charge(self, amount: float, currency: str, method: str) -> PaymentResult:
        return PaymentResult(
            success=True,
            payment_id=f"moy_{amount}_{method}",
            amount=amount,
            currency=currency,
            method=method,
            gateway_reference=f"MOY-REF-{amount}",
            status="paid",
        )

    async def refund(self, payment_id: str) -> RefundResult:
        return RefundResult(
            success=True,
            payment_id=payment_id,
            amount=0.0,
            gateway_reference=f"MOY-REF-{payment_id}",
        )


class STCPayGateway(PaymentGateway):
    async def charge(self, amount: float, currency: str, method: str) -> PaymentResult:
        return PaymentResult(
            success=True,
            payment_id=f"stc_{amount}",
            amount=amount,
            currency=currency,
            method="stc_pay",
            gateway_reference=f"STC-REF-{amount}",
            status="paid",
        )

    async def refund(self, payment_id: str) -> RefundResult:
        return RefundResult(
            success=True,
            payment_id=payment_id,
            amount=0.0,
            gateway_reference=f"STC-REF-{payment_id}",
        )


class SADADGateway(PaymentGateway):
    async def charge(self, amount: float, currency: str, method: str) -> PaymentResult:
        return PaymentResult(
            success=True,
            payment_id=f"sad_{amount}",
            amount=amount,
            currency=currency,
            method="sadad",
            gateway_reference=f"SAD-REF-{amount}",
            status="pending",
        )

    async def refund(self, payment_id: str) -> RefundResult:
        return RefundResult(
            success=True,
            payment_id=payment_id,
            amount=0.0,
            gateway_reference=f"SAD-REF-{payment_id}",
        )


class PaymentGatewayFactory:
    _GATEWAYS = {
        "moyasar": MoyasarGateway,
        "stc_pay": STCPayGateway,
        "sadad": SADADGateway,
    }

    @staticmethod
    def get_gateway(type_: str) -> PaymentGateway:
        gateway_class = PaymentGatewayFactory._GATEWAYS.get(type_.lower())
        if not gateway_class:
            supported = list(PaymentGatewayFactory._GATEWAYS.keys())
            raise ValueError(f"Unsupported gateway: {type_}. Supported: {supported}")
        return gateway_class()

    @staticmethod
    def register_gateway(name: str, gateway_class: type[PaymentGateway]) -> None:
        PaymentGatewayFactory._GATEWAYS[name] = gateway_class

    @staticmethod
    def list_gateways() -> list[str]:
        return list(PaymentGatewayFactory._GATEWAYS.keys())
