"""Dealix Partner Network V2 economics and governance.
Pure policy helpers: no payment, messaging, publishing, or production mutation.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from decimal import ROUND_HALF_UP, Decimal
from typing import Mapping

MONEY = Decimal("0.01")
SERVICE_RATES = {
    "scout": Decimal("0.075"),
    "growth_partner": Decimal("0.10"),
    "co_sell_partner": Decimal("0.125"),
    "closer_sector_partner": Decimal("0.15"),
    "strategic_channel": Decimal("0.20"),
}
SAAS_RATES = {
    "scout": Decimal("0.20"),
    "growth_partner": Decimal("0.25"),
    "co_sell_partner": Decimal("0.25"),
    "closer_sector_partner": Decimal("0.30"),
    "strategic_channel": Decimal("0.30"),
}
ATTRIBUTION_PROTECTION_DAYS = 120
ATTRIBUTION_MAX_EXTENSION_DAYS = 180
DEFAULT_CLEARING_DAYS = 30
DEFAULT_SAAS_COMMISSION_MONTHS = 12
NCCR_DEDUCTION_FIELDS = (
    "vat_sar",
    "refunds_sar",
    "credits_sar",
    "chargebacks_sar",
    "pass_through_ad_spend_sar",
    "third_party_licenses_at_cost_sar",
    "pass_through_vendor_costs_sar",
    "government_fees_sar",
)
DEFAULT_SPLIT = {
    "source": Decimal("0.40"),
    "qualification": Decimal("0.20"),
    "close": Decimal("0.40"),
}


def _d(value: Decimal | int | float | str) -> Decimal:
    return Decimal(str(value))


def _money(value: Decimal) -> Decimal:
    return value.quantize(MONEY, rounding=ROUND_HALF_UP)


@dataclass(frozen=True)
class NCCRInputs:
    collected_cash_sar: Decimal
    vat_sar: Decimal = Decimal("0")
    refunds_sar: Decimal = Decimal("0")
    credits_sar: Decimal = Decimal("0")
    chargebacks_sar: Decimal = Decimal("0")
    pass_through_ad_spend_sar: Decimal = Decimal("0")
    third_party_licenses_at_cost_sar: Decimal = Decimal("0")
    pass_through_vendor_costs_sar: Decimal = Decimal("0")
    government_fees_sar: Decimal = Decimal("0")

    @classmethod
    def from_mapping(cls, values: Mapping[str, object]) -> NCCRInputs:
        kwargs = {"collected_cash_sar": _d(values.get("collected_cash_sar", 0))}
        for field_name in NCCR_DEDUCTION_FIELDS:
            kwargs[field_name] = _d(values.get(field_name, 0))
        return cls(**kwargs)


def calculate_nccr(inputs: NCCRInputs | Mapping[str, object]) -> Decimal:
    """Return non-negative Net Commissionable Collected Revenue.

    Financial inputs are fail-closed: negative collected cash or deductions are invalid
    rather than being allowed to inflate commissionable revenue.
    """
    if not isinstance(inputs, NCCRInputs):
        inputs = NCCRInputs.from_mapping(inputs)
    if inputs.collected_cash_sar < 0:
        raise ValueError("collected_cash_sar must be non-negative")
    for field_name in NCCR_DEDUCTION_FIELDS:
        if getattr(inputs, field_name) < 0:
            raise ValueError(f"{field_name} must be non-negative")
    deductions = sum((getattr(inputs, f) for f in NCCR_DEDUCTION_FIELDS), Decimal("0"))
    return _money(max(Decimal("0"), inputs.collected_cash_sar - deductions))


@dataclass(frozen=True)
class CommissionDecision:
    eligible: bool
    status: str
    motion: str
    revenue_type: str
    nccr_sar: Decimal
    rate: Decimal
    commission_sar: Decimal
    clearing_days: int = DEFAULT_CLEARING_DAYS
    recurring_month_limit: int | None = None
    approval_required: bool = False
    reasons: tuple[str, ...] = field(default_factory=tuple)

    def to_dict(self) -> dict[str, object]:
        return {
            "eligible": self.eligible,
            "status": self.status,
            "motion": self.motion,
            "revenue_type": self.revenue_type,
            "nccr_sar": float(self.nccr_sar),
            "rate": float(self.rate),
            "commission_sar": float(self.commission_sar),
            "clearing_days": self.clearing_days,
            "recurring_month_limit": self.recurring_month_limit,
            "approval_required": self.approval_required,
            "reasons": list(self.reasons),
        }


def commission_rate_for(motion: str, revenue_type: str) -> Decimal:
    """Return canonical Partner Network V2 rate for a qualified motion."""
    if revenue_type not in {"services", "saas"}:
        raise ValueError(f"unknown revenue type: {revenue_type}")
    table = SAAS_RATES if revenue_type == "saas" else SERVICE_RATES
    if motion not in table:
        raise ValueError(f"unknown partner motion: {motion}")
    return table[motion]


def calculate_partner_commission(
    *,
    motion: str,
    revenue_type: str,
    economics: NCCRInputs | Mapping[str, object],
    verified_collection: bool,
    partner_active: bool = True,
    duplicate_or_existing_pipeline: bool = False,
    government_or_tender: bool = False,
    margin_approved: bool = False,
    recurring_month_index: int | None = None,
) -> CommissionDecision:
    nccr = calculate_nccr(economics)
    rate = commission_rate_for(motion, revenue_type)
    reasons: list[str] = []
    approval_required = False

    if not partner_active:
        reasons.append("partner_not_active")
    if duplicate_or_existing_pipeline:
        reasons.append("duplicate_or_existing_pipeline")
    if not verified_collection:
        reasons.append("verified_collection_missing")
    if nccr <= 0:
        reasons.append("no_positive_nccr")
    if government_or_tender:
        reasons.append("government_or_tender_compliance_review")
        approval_required = True
    if motion == "strategic_channel" and revenue_type == "services" and not margin_approved:
        reasons.append("strategic_service_margin_approval_required")
        approval_required = True
    if revenue_type == "saas":
        if recurring_month_index is None:
            reasons.append("recurring_month_index_required")
        elif recurring_month_index < 1 or recurring_month_index > DEFAULT_SAAS_COMMISSION_MONTHS:
            reasons.append("outside_saas_commission_window")

    hard_hold = bool(reasons)
    amount = Decimal("0") if hard_hold else _money(nccr * rate)
    status = "compliance_hold" if government_or_tender else ("hold" if hard_hold else "clearing")
    return CommissionDecision(
        eligible=not hard_hold,
        status=status,
        motion=motion,
        revenue_type=revenue_type,
        nccr_sar=nccr,
        rate=rate,
        commission_sar=amount,
        clearing_days=DEFAULT_CLEARING_DAYS,
        recurring_month_limit=(DEFAULT_SAAS_COMMISSION_MONTHS if revenue_type == "saas" else None),
        approval_required=approval_required,
        reasons=tuple(reasons),
    )


def validate_attribution_split(split: Mapping[str, Decimal | int | float | str]) -> dict[str, Decimal]:
    normalized = {role: _d(value) for role, value in split.items()}
    if not normalized:
        raise ValueError("attribution split cannot be empty")
    allowed = set(DEFAULT_SPLIT)
    unknown = set(normalized) - allowed
    if unknown:
        raise ValueError(f"unknown attribution roles: {sorted(unknown)}")
    for role, value in normalized.items():
        if value < 0 or value > 1:
            raise ValueError(f"invalid split for {role}: {value}")
    total = sum(normalized.values(), Decimal("0"))
    if total != Decimal("1"):
        raise ValueError(f"attribution split must total 1.0, got {total}")
    return normalized


def allocate_commission_pool(
    total_commission_sar: Decimal | int | float | str,
    split: Mapping[str, Decimal | int | float | str] = DEFAULT_SPLIT,
) -> dict[str, Decimal]:
    normalized = validate_attribution_split(split)
    total = _money(_d(total_commission_sar))
    if total < 0:
        raise ValueError("total_commission_sar must be non-negative")
    allocated = {role: _money(total * share) for role, share in normalized.items()}
    rounding_delta = total - sum(allocated.values(), Decimal("0"))
    if rounding_delta:
        if "close" in allocated:
            recipient = "close"
        else:
            recipient = max(normalized, key=lambda role: (normalized[role], role))
        allocated[recipient] = _money(allocated[recipient] + rounding_delta)
    return allocated


def attribution_window_days(*, extension_approved: bool = False) -> int:
    return ATTRIBUTION_MAX_EXTENSION_DAYS if extension_approved else ATTRIBUTION_PROTECTION_DAYS


def requires_compliance_hold(
    *,
    government_or_tender: bool = False,
    government_official_or_employee: bool = False,
    influence_based_compensation: bool = False,
    cold_whatsapp: bool = False,
    consent_proven: bool = True,
) -> tuple[bool, tuple[str, ...]]:
    reasons: list[str] = []
    if government_or_tender:
        reasons.append("government_or_tender_review")
    if government_official_or_employee:
        reasons.append("government_official_or_employee")
    if influence_based_compensation:
        reasons.append("influence_based_compensation_prohibited")
    if cold_whatsapp:
        reasons.append("cold_whatsapp_prohibited")
    if not consent_proven:
        reasons.append("marketing_consent_not_proven")
    return bool(reasons), tuple(reasons)
