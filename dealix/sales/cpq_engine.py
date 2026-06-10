"""
Configure-Price-Quote (CPQ) Engine.
محرك التهيئة والتسعير وعرض الأسعار.

Handles product configuration, pricing calculation, and quote generation
for enterprise AI solutions. Supports Saudi/GCC/global pricing tiers,
custom ML model add-ons, and volume discounting.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime
from decimal import Decimal
from enum import StrEnum
from typing import Any

from core.logging import get_logger

log = get_logger(__name__)


class DeploymentType(StrEnum):
    SAUDI_ONLY = "saudi_only"
    GCC = "gcc"
    GLOBAL = "global"


class ContractTerm(StrEnum):
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    ANNUAL = "annual"
    BIENNIAL = "biennial"


@dataclass
class ClientRequirements:
    company_name: str
    deployment_type: DeploymentType
    expected_leads_per_month: int = 1000
    users: int = 5
    ai_agents: int = 1
    custom_models: bool = False
    integrations: list[str] = field(default_factory=list)
    contract_term: ContractTerm = ContractTerm.ANNUAL
    requires_sla: bool = True
    requires_dedicated_infrastructure: bool = False
    locale: str = "ar"


@dataclass
class LineItem:
    sku: str
    name: str
    description: str
    unit_price: Decimal
    quantity: int
    discount_pct: float = 0.0
    total: Decimal = Decimal("0")
    is_recurring: bool = True
    billing_frequency: str = "monthly"

    def calculate_total(self) -> Decimal:
        discounted = self.unit_price * Decimal(str(1 - self.discount_pct / 100))
        self.total = discounted * self.quantity
        return self.total


@dataclass
class SolutionConfig:
    config_id: str
    requirements: ClientRequirements
    line_items: list[LineItem] = field(default_factory=list)
    setup_fee: Decimal = Decimal("0")
    monthly_total: Decimal = Decimal("0")
    annual_total: Decimal = Decimal("0")
    currency: str = "SAR"
    notes: list[str] = field(default_factory=list)


@dataclass
class PriceQuote:
    quote_id: str
    config: SolutionConfig
    valid_until: str
    status: str = "draft"  # draft / sent / accepted / rejected / expired
    created_at: str = ""
    locale: str = "ar"


@dataclass
class QuoteDocument:
    quote_id: str
    title: str
    html: str
    pdf_bytes: bytes | None = None
    valid_until: str = ""


@dataclass
class Contract:
    contract_id: str
    quote_id: str
    tenant_id: str
    status: str = "draft"  # draft / sent / signed / active / expired / terminated
    signed_at: str | None = None
    expires_at: str | None = None
    content: dict[str, Any] = field(default_factory=dict)


class CPQEngine:
    """Configure-Price-Quote engine for Dealix AI solutions.

    Pricing references:
    - KSA/GCC setup: SAR 12,000 - 50,000
    - KSA/GCC retainer: SAR 3,000 - 15,000/month
    - Global setup: $3,000 - $10,000 USD
    - Global retainer: $800 - $3,000/month
    - AI agent add-on: SAR 2,000/month per agent
    """

    def __init__(self) -> None:
        self._price_book = self._load_price_book()

    async def configure(self, requirements: ClientRequirements) -> SolutionConfig:
        """Transform client requirements into a solution configuration."""
        config_id = f"CFG-{uuid.uuid4().hex[:8].upper()}"
        line_items: list[LineItem] = []

        base_prices = self._get_base_prices(requirements.deployment_type)

        # Platform license
        line_items.append(LineItem(
            sku="PLATFORM-BASE",
            name="منصة Dealix الأساسية" if requirements.locale == "ar" else "Dealix Platform Base",
            description="منصة ذكاء اصطناعي متعددة المستأجرين" if requirements.locale == "ar" else "Multi-tenant AI Platform",
            unit_price=base_prices["platform"],
            quantity=1,
            is_recurring=True,
        ))

        # Per-user license
        line_items.append(LineItem(
            sku="USER-SEAT",
            name="ترخيص مستخدم" if requirements.locale == "ar" else "User License",
            description=f"{requirements.users} users",
            unit_price=base_prices["per_user"],
            quantity=requirements.users,
            is_recurring=True,
        ))

        # AI agents
        if requirements.ai_agents > 0:
            line_items.append(LineItem(
                sku="AI-AGENT",
                name="وكيل ذكاء اصطناعي" if requirements.locale == "ar" else "AI Agent",
                description=f"{requirements.ai_agents} AI agent(s)",
                unit_price=base_prices["per_agent"],
                quantity=requirements.ai_agents,
                is_recurring=True,
            ))

        # Custom models add-on
        if requirements.custom_models:
            line_items.append(LineItem(
                sku="CUSTOM-MODEL",
                name="نموذج مخصص" if requirements.locale == "ar" else "Custom Model",
                description="Fine-tuned custom AI models",
                unit_price=base_prices["custom_model"],
                quantity=1,
                is_recurring=True,
            ))

        # Integrations
        for integration in requirements.integrations:
            if integration in base_prices.get("integrations", {}):
                line_items.append(LineItem(
                    sku=f"INT-{integration.upper()}",
                    name=f"Integration: {integration}",
                    description=f"{integration} integration",
                    unit_price=base_prices["integrations"][integration],
                    quantity=1,
                    is_recurring=True,
                ))

        # SLA
        if requirements.requires_sla:
            line_items.append(LineItem(
                sku="SLA-PREMIUM",
                name="اتفاقية مستوى خدمة ممتازة" if requirements.locale == "ar" else "Premium SLA",
                description="99.9% uptime SLA, 4h response",
                unit_price=base_prices["sla"],
                quantity=1,
                is_recurring=True,
            ))

        # Dedicated infrastructure
        if requirements.requires_dedicated_infrastructure:
            line_items.append(LineItem(
                sku="DEDICATED-INFRA",
                name="بنية تحتية مخصصة" if requirements.locale == "ar" else "Dedicated Infrastructure",
                description="Isolated infrastructure tenant",
                unit_price=base_prices["dedicated_infra"],
                quantity=1,
                is_recurring=True,
            ))

        # Apply volume discounts
        if requirements.expected_leads_per_month > 5000:
            for item in line_items:
                if item.quantity > 10:
                    item.discount_pct = 10

        # Calculate totals
        for item in line_items:
            item.calculate_total()

        monthly = sum(item.total for item in line_items if item.is_recurring)

        config = SolutionConfig(
            config_id=config_id,
            requirements=requirements,
            line_items=line_items,
            setup_fee=base_prices["setup_fee"],
            monthly_total=monthly,
            annual_total=monthly * 12,
            currency="SAR" if requirements.deployment_type in (DeploymentType.SAUDI_ONLY, DeploymentType.GCC) else "USD",
            notes=[f"Valid for {requirements.contract_term.value} contract term"],
        )

        log.info("cpq_config_created", config_id=config_id)
        return config

    async def price(self, config: SolutionConfig) -> PriceQuote:
        """Generate a price quote from a solution configuration."""
        quote_id = f"Q-{uuid.uuid4().hex[:8].upper()}"
        valid_until = ""

        valid_until = datetime.now(UTC).isoformat()

        return PriceQuote(
            quote_id=quote_id,
            config=config,
            valid_until=valid_until,
            status="draft",
            created_at=datetime.now(UTC).isoformat(),
            locale=config.requirements.locale,
        )

    async def quote(self, config: SolutionConfig) -> QuoteDocument:
        """Generate a full quote document from a solution configuration."""
        quote_id = f"Q-{uuid.uuid4().hex[:8].upper()}"
        price_quote = await self.price(config)

        lines_html = ""
        for item in config.line_items:
            lines_html += f"""
            <tr>
                <td style="padding:8px;border-bottom:1px solid #ddd;">{item.name}</td>
                <td style="padding:8px;border-bottom:1px solid #ddd;text-align:center;">{item.quantity}</td>
                <td style="padding:8px;border-bottom:1px solid #ddd;text-align:right;">{config.currency} {item.unit_price:,.2f}</td>
                <td style="padding:8px;border-bottom:1px solid #ddd;text-align:right;">{config.currency} {item.total:,.2f}</td>
            </tr>"""

        html = f"""<!DOCTYPE html>
<html dir="{ 'rtl' if config.requirements.locale == 'ar' else 'ltr' }">
<head><meta charset="utf-8"><title>Quote {quote_id}</title></head>
<body style="font-family: 'IBM Plex Sans Arabic', sans-serif; max-width: 800px; margin: 0 auto; padding: 40px;">
<div style="border: 2px solid #10b981; border-radius: 12px; padding: 32px;">
<div style="text-align: center; margin-bottom: 32px;">
<h1 style="color: #0f172a; margin: 0;">{ 'عرض سعر' if config.requirements.locale == 'ar' else 'Price Quote' }</h1>
<p style="color: #64748b;">{quote_id}</p>
</div>
<div style="margin-bottom: 24px;">
<h3>{config.requirements.company_name}</h3>
<p>{ 'تاريخ الإنشاء:' if config.requirements.locale == 'ar' else 'Created:' } {price_quote.created_at[:10]}</p>
<p>{ 'صالح حتى:' if config.requirements.locale == 'ar' else 'Valid until:' } {price_quote.valid_until[:10]}</p>
</div>
<table style="width:100%;border-collapse:collapse;">
<thead><tr style="background:#f8fafc;">
<th style="padding:8px;text-align:left;border-bottom:2px solid #0f172a;">{'الخدمة' if config.requirements.locale == 'ar' else 'Service'}</th>
<th style="padding:8px;text-align:center;border-bottom:2px solid #0f172a;">{'العدد' if config.requirements.locale == 'ar' else 'Qty'}</th>
<th style="padding:8px;text-align:right;border-bottom:2px solid #0f172a;">{'السعر' if config.requirements.locale == 'ar' else 'Price'}</th>
<th style="padding:8px;text-align:right;border-bottom:2px solid #0f172a;">{'الإجمالي' if config.requirements.locale == 'ar' else 'Total'}</th>
</tr></thead>
<tbody>{lines_html}</tbody>
</table>
<div style="margin-top:24px;border-top:2px solid #0f172a;padding-top:16px;">
<div style="display:flex;justify-content:space-between;">
<span style="font-weight:bold;">{'رسوم التأسيس:' if config.requirements.locale == 'ar' else 'Setup Fee:'}</span>
<span>{config.currency} {config.setup_fee:,.2f}</span>
</div>
<div style="display:flex;justify-content:space-between;font-size:1.2em;font-weight:bold;margin-top:8px;">
<span>{{'الإجمالي الشهري:' if config.requirements.locale == 'ar' else 'Monthly Total:'}}</span>
<span>{config.currency} {config.monthly_total:,.2f}</span>
</div>
<div style="display:flex;justify-content:space-between;font-size:1.4em;color:#10b981;margin-top:8px;">
<span>{{'الإجمالي السنوي:' if config.requirements.locale == 'ar' else 'Annual Total:'}}</span>
<span>{config.currency} {config.annual_total:,.2f}</span>
</div>
</div>
</div>
</body></html>"""

        return QuoteDocument(
            quote_id=quote_id,
            title=f"Quote {quote_id} - {config.requirements.company_name}",
            html=html,
            valid_until=price_quote.valid_until,
        )

    async def generate_contract(self, quote_id: str) -> Contract:
        """Generate a formal contract from an accepted quote."""
        contract_id = f"CTR-{uuid.uuid4().hex[:8].upper()}"
        return Contract(
            contract_id=contract_id,
            quote_id=quote_id,
            tenant_id="",
            status="draft",
            content={
                "quote_id": quote_id,
                "contract_id": contract_id,
                "terms": "Standard Dealix Enterprise Terms",
            },
        )

    def _get_base_prices(self, deployment: DeploymentType) -> dict[str, Any]:
        """Get base prices for the given deployment type."""
        prices: dict[str, Any] = {
            DeploymentType.SAUDI_ONLY: {
                "setup_fee": Decimal("15000"),
                "platform": Decimal("8000"),
                "per_user": Decimal("1000"),
                "per_agent": Decimal("3000"),
                "custom_model": Decimal("5000"),
                "sla": Decimal("2000"),
                "dedicated_infra": Decimal("5000"),
                "integrations": {"hubspot": Decimal("1000"), "zapier": Decimal("500")},
            },
            DeploymentType.GCC: {
                "setup_fee": Decimal("20000"),
                "platform": Decimal("10000"),
                "per_user": Decimal("1200"),
                "per_agent": Decimal("3500"),
                "custom_model": Decimal("6000"),
                "sla": Decimal("2500"),
                "dedicated_infra": Decimal("6000"),
                "integrations": {"hubspot": Decimal("1200"), "zapier": Decimal("500")},
            },
            DeploymentType.GLOBAL: {
                "setup_fee": Decimal("5000"),
                "platform": Decimal("3000"),
                "per_user": Decimal("300"),
                "per_agent": Decimal("1000"),
                "custom_model": Decimal("2000"),
                "sla": Decimal("800"),
                "dedicated_infra": Decimal("2000"),
                "integrations": {"hubspot": Decimal("300"), "zapier": Decimal("100")},
            },
        }
        base = prices.get(deployment, prices[DeploymentType.SAUDI_ONLY])
        return base

    def _load_price_book(self) -> dict[str, Any]:
        """Load price book from configuration (in production, from DB or config)."""
        return {}
