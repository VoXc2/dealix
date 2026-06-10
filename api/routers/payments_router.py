"""
Payments Router — all payment and subscription endpoints.
موجه المدفوعات — جميع نقاط نهاية الدفع والاشتراكات.
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, ConfigDict, Field

from dealix.payments.moyasar import MoyasarClient
from dealix.payments.sadad import SADADClient
from dealix.payments.stc_pay import STCPayClient
from dealix.payments.subscription_manager import SubscriptionManager

router = APIRouter(prefix="/api/v1/payments", tags=["payments"])

_subscriptions = SubscriptionManager()
_stc_pay = STCPayClient()
_sadad = SADADClient()
_moyasar = MoyasarClient()

_HARD_GATES = {
    "no_live_charge_without_consent": True,
    "no_auto_renew_without_notice": True,
    "sandbox_mode": True,
}


class CreateSubscriptionRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    customer_id: str = Field(..., min_length=2, max_length=64)
    plan: str = Field(..., pattern=r"^(starter|growth|scale|enterprise)$")


class CancelSubscriptionRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    subscription_id: str


class UpgradeSubscriptionRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    subscription_id: str
    new_plan: str = Field(..., pattern=r"^(starter|growth|scale|enterprise)$")


class GenerateInvoiceRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    subscription_id: str


class STCPayRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    amount_sar: float = Field(..., gt=0, le=1000000)
    description: str = Field(..., min_length=3, max_length=200)


class SADADRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    amount_sar: float = Field(..., gt=0, le=1000000)
    customer_id: str = Field(..., min_length=2, max_length=64)


class MoyasarChargeRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    amount_sar: float = Field(..., gt=0, le=1000000)
    source_id: str = Field(..., min_length=8)
    description: str = "Dealix payment"


@router.get("/subscriptions")
async def list_subscriptions(customer_id: str | None = None) -> dict[str, Any]:
    subs = _subscriptions.list_subscriptions(customer_id)
    return {
        "count": len(subs),
        "subscriptions": [s.to_dict() for s in subs],
        "stats": _subscriptions.get_stats(),
        "hard_gates": _HARD_GATES,
    }


@router.get("/subscriptions/{subscription_id}")
async def get_subscription(subscription_id: str) -> dict[str, Any]:
    sub = _subscriptions.get_subscription(subscription_id)
    if not sub:
        raise HTTPException(status_code=404, detail="Subscription not found")
    status = await _subscriptions.get_status(subscription_id)
    return {
        "subscription": sub.to_dict(),
        "status": status.to_dict(),
        "hard_gates": _HARD_GATES,
    }


@router.post("/subscriptions/create")
async def create_subscription(body: CreateSubscriptionRequest) -> dict[str, Any]:
    try:
        subscription = await _subscriptions.create(body.customer_id, body.plan)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {
        "status": "created",
        "subscription": subscription.to_dict(),
        "hard_gates": _HARD_GATES,
    }


@router.post("/subscriptions/cancel")
async def cancel_subscription(body: CancelSubscriptionRequest) -> dict[str, Any]:
    success = await _subscriptions.cancel(body.subscription_id)
    if not success:
        raise HTTPException(status_code=404, detail="Subscription not found")
    return {"status": "cancelled", "subscription_id": body.subscription_id, "hard_gates": _HARD_GATES}


@router.post("/subscriptions/upgrade")
async def upgrade_subscription(body: UpgradeSubscriptionRequest) -> dict[str, Any]:
    try:
        sub = await _subscriptions.upgrade(body.subscription_id, body.new_plan)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"status": "upgraded", "subscription": sub.to_dict(), "hard_gates": _HARD_GATES}


@router.get("/subscriptions/{subscription_id}/invoices")
async def list_invoices(subscription_id: str) -> dict[str, Any]:
    invoices = _subscriptions.list_invoices(subscription_id)
    return {
        "count": len(invoices),
        "invoices": [i.to_dict() for i in invoices],
        "hard_gates": _HARD_GATES,
    }


@router.post("/invoices/generate")
async def generate_invoice(body: GenerateInvoiceRequest) -> dict[str, Any]:
    try:
        invoice = await _subscriptions.generate_invoice(body.subscription_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"status": "generated", "invoice": invoice.to_dict(), "hard_gates": _HARD_GATES}


@router.get("/plans")
async def list_plans() -> dict[str, Any]:
    plans = {}
    for name, config in _subscriptions.PLANS.items():
        plans[name] = {
            "price_sar": config["price_sar"],
            "leads_per_month": config["leads"] if config["leads"] > 0 else "Unlimited",
            "channels": config["channels"] if config["channels"] > 0 else "Unlimited",
            "sla_response_hours": config["sla_hours"],
        }
    return {"plans": plans, "currency": "SAR", "hard_gates": _HARD_GATES}


@router.post("/stc-pay/create")
async def stc_pay_create(body: STCPayRequest) -> dict[str, Any]:
    try:
        intent = await _stc_pay.create_payment(body.amount_sar, body.description)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"payment": intent.to_dict(), "hard_gates": _HARD_GATES}


@router.get("/stc-pay/{payment_id}/status")
async def stc_pay_status(payment_id: str) -> dict[str, Any]:
    status = await _stc_pay.check_status(payment_id)
    return {"status": status.to_dict(), "hard_gates": _HARD_GATES}


@router.post("/stc-pay/{payment_id}/refund")
async def stc_pay_refund(payment_id: str) -> dict[str, Any]:
    result = await _stc_pay.refund(payment_id)
    return {"refund": result.to_dict(), "hard_gates": _HARD_GATES}


@router.post("/sadad/create-bill")
async def sadad_create_bill(body: SADADRequest) -> dict[str, Any]:
    try:
        bill = await _sadad.create_bill(body.amount_sar, body.customer_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"bill": bill.to_dict(), "hard_gates": _HARD_GATES}


@router.get("/sadad/{bill_id}/status")
async def sadad_status(bill_id: str) -> dict[str, Any]:
    status = await _sadad.check_payment(bill_id)
    return {"status": status.to_dict(), "hard_gates": _HARD_GATES}


@router.post("/sadad/{bill_id}/confirm")
async def sadad_confirm(bill_id: str) -> dict[str, Any]:
    success = await _sadad.confirm_payment(bill_id)
    return {"success": success, "bill_id": bill_id, "hard_gates": _HARD_GATES}


@router.post("/moyasar/charge")
async def moyasar_charge(body: MoyasarChargeRequest) -> dict[str, Any]:
    result = await _moyasar.create_payment(body.amount_sar, body.source_id, body.description)
    return {"payment": result, "hard_gates": _HARD_GATES}


@router.post("/moyasar/webhook")
async def moyasar_webhook(payload: dict[str, Any]) -> dict[str, Any]:
    from dealix.payments.moyasar import verify_webhook
    verified = verify_webhook(payload)
    return {"verified": verified, "status": "received", "hard_gates": _HARD_GATES}


@router.get("/gateways")
async def list_gateways() -> dict[str, Any]:
    from dealix.payments.payment_gateway import PaymentGatewayFactory
    return {
        "gateways": PaymentGatewayFactory.list_gateways(),
        "hard_gates": _HARD_GATES,
    }
