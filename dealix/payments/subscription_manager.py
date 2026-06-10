"""
Subscription Manager — manages recurring subscription plans for Saudi customers.
مدير الاشتراكات — يدير خطط الاشتراكات المتكررة للعملاء السعوديين.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from decimal import Decimal
from typing import Any

from core.logging import get_logger
from core.utils import generate_id, utcnow

logger = get_logger(__name__)


@dataclass
class SubscriptionStatus:
    active: bool = False
    plan: str = ""
    current_period_start: datetime | None = None
    current_period_end: datetime | None = None
    days_until_renewal: int = 0
    payment_method: str = ""
    auto_renew: bool = True
    cancelled_at: datetime | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "active": self.active,
            "plan": self.plan,
            "current_period_start": self.current_period_start.isoformat() if self.current_period_start else None,
            "current_period_end": self.current_period_end.isoformat() if self.current_period_end else None,
            "days_until_renewal": self.days_until_renewal,
            "payment_method": self.payment_method,
            "auto_renew": self.auto_renew,
            "cancelled_at": self.cancelled_at.isoformat() if self.cancelled_at else None,
        }


@dataclass
class Subscription:
    id: str
    customer_id: str
    plan: str
    price_sar: float
    status: str = "active"
    leads_included: int = 200
    channels_included: int = 2
    sla_hours: float = 1.0
    current_period_start: datetime = field(default_factory=utcnow)
    current_period_end: datetime = field(default_factory=lambda: utcnow() + timedelta(days=30))
    auto_renew: bool = True
    cancelled_at: datetime | None = None
    created_at: datetime = field(default_factory=utcnow)

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "customer_id": self.customer_id,
            "plan": self.plan,
            "price_sar": self.price_sar,
            "status": self.status,
            "leads_included": self.leads_included,
            "channels_included": self.channels_included,
            "sla_hours": self.sla_hours,
            "current_period_start": self.current_period_start.isoformat(),
            "current_period_end": self.current_period_end.isoformat(),
            "auto_renew": self.auto_renew,
            "cancelled_at": self.cancelled_at.isoformat() if self.cancelled_at else None,
            "created_at": self.created_at.isoformat(),
        }


@dataclass
class Invoice:
    id: str
    subscription_id: str
    customer_id: str
    plan: str
    amount_sar: float
    status: str = "pending"
    period_start: datetime = field(default_factory=utcnow)
    period_end: datetime = field(default_factory=lambda: utcnow() + timedelta(days=30))
    paid_at: datetime | None = None
    created_at: datetime = field(default_factory=utcnow)

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "subscription_id": self.subscription_id,
            "customer_id": self.customer_id,
            "plan": self.plan,
            "amount_sar": self.amount_sar,
            "status": self.status,
            "period_start": self.period_start.isoformat(),
            "period_end": self.period_end.isoformat(),
            "paid_at": self.paid_at.isoformat() if self.paid_at else None,
            "created_at": self.created_at.isoformat(),
        }


class SubscriptionManager:
    PLANS = {
        "starter": {"price_sar": 999, "leads": 200, "channels": 2, "sla_hours": 1},
        "growth": {"price_sar": 2999, "leads": 1000, "channels": 4, "sla_hours": 0.5},
        "scale": {"price_sar": 7999, "leads": 5000, "channels": -1, "sla_hours": 0.25},
        "enterprise": {"price_sar": -1, "leads": -1, "channels": -1, "sla_hours": 0.08},
    }

    def __init__(self):
        self._subscriptions: dict[str, Subscription] = {}
        self._invoices: dict[str, Invoice] = {}
        self.log = logger.bind(component="subscription_manager")

    async def create(self, customer_id: str, plan: str) -> Subscription:
        if plan not in self.PLANS:
            raise ValueError(f"Invalid plan: {plan}. Must be one of {list(self.PLANS.keys())}")

        plan_config = self.PLANS[plan]
        now = utcnow()

        subscription = Subscription(
            id=generate_id("sub"),
            customer_id=customer_id,
            plan=plan,
            price_sar=plan_config["price_sar"],
            leads_included=plan_config["leads"],
            channels_included=plan_config["channels"],
            sla_hours=plan_config["sla_hours"],
            status="active",
            current_period_start=now,
            current_period_end=now + timedelta(days=30),
            auto_renew=True,
        )
        self._subscriptions[subscription.id] = subscription
        self.log.info("subscription_created", id=subscription.id, customer=customer_id, plan=plan)
        return subscription

    async def cancel(self, subscription_id: str) -> bool:
        sub = self._subscriptions.get(subscription_id)
        if not sub:
            return False
        sub.status = "cancelled"
        sub.auto_renew = False
        sub.cancelled_at = utcnow()
        self.log.info("subscription_cancelled", id=subscription_id)
        return True

    async def upgrade(self, subscription_id: str, new_plan: str) -> Subscription:
        sub = self._subscriptions.get(subscription_id)
        if not sub:
            raise ValueError(f"Subscription {subscription_id} not found")
        if new_plan not in self.PLANS:
            raise ValueError(f"Invalid plan: {new_plan}")

        plan_config = self.PLANS[new_plan]
        sub.plan = new_plan
        sub.price_sar = plan_config["price_sar"]
        sub.leads_included = plan_config["leads"]
        sub.channels_included = plan_config["channels"]
        sub.sla_hours = plan_config["sla_hours"]

        self.log.info("subscription_upgraded", id=subscription_id, new_plan=new_plan)
        return sub

    async def generate_invoice(self, subscription_id: str) -> Invoice:
        sub = self._subscriptions.get(subscription_id)
        if not sub:
            raise ValueError(f"Subscription {subscription_id} not found")

        now = utcnow()
        invoice = Invoice(
            id=generate_id("inv"),
            subscription_id=subscription_id,
            customer_id=sub.customer_id,
            plan=sub.plan,
            amount_sar=sub.price_sar,
            status="pending",
            period_start=sub.current_period_start,
            period_end=sub.current_period_end,
        )
        self._invoices[invoice.id] = invoice
        self.log.info("invoice_generated", id=invoice.id, subscription_id=subscription_id)
        return invoice

    async def get_status(self, subscription_id: str) -> SubscriptionStatus:
        sub = self._subscriptions.get(subscription_id)
        if not sub:
            return SubscriptionStatus(active=False)

        now = utcnow()
        days_until = (sub.current_period_end - now).days if sub.current_period_end > now else 0

        return SubscriptionStatus(
            active=sub.status == "active",
            plan=sub.plan,
            current_period_start=sub.current_period_start,
            current_period_end=sub.current_period_end,
            days_until_renewal=max(0, days_until),
            payment_method="moyasar",
            auto_renew=sub.auto_renew,
            cancelled_at=sub.cancelled_at,
        )

    def get_subscription(self, subscription_id: str) -> Subscription | None:
        return self._subscriptions.get(subscription_id)

    def list_subscriptions(self, customer_id: str | None = None) -> list[Subscription]:
        if customer_id:
            return [s for s in self._subscriptions.values() if s.customer_id == customer_id]
        return list(self._subscriptions.values())

    def list_invoices(self, subscription_id: str | None = None) -> list[Invoice]:
        if subscription_id:
            return [i for i in self._invoices.values() if i.subscription_id == subscription_id]
        return list(self._invoices.values())

    def get_stats(self) -> dict[str, Any]:
        subs = self._subscriptions.values()
        active = [s for s in subs if s.status == "active"]
        mrr = sum(s.price_sar for s in active)
        return {
            "total_subscriptions": len(subs),
            "active": len(active),
            "cancelled": sum(1 for s in subs if s.status == "cancelled"),
            "mrr_sar": mrr,
            "arr_sar": mrr * 12,
            "by_plan": {
                p: sum(1 for s in subs if s.plan == p)
                for p in self.PLANS
            },
            "total_invoiced": sum(i.amount_sar for i in self._invoices.values()),
            "total_collected": sum(i.amount_sar for i in self._invoices.values() if i.status == "paid"),
        }
