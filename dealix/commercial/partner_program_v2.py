"""Dealix Partner Network V2 economics and governance.
Pure policy helpers: no payment, messaging, publishing, or production mutation.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from decimal import ROUND_HALF_UP, Decimal
from typing import Any, Mapping

MONEY = Decimal("0.01")
PARTNER_POLICY_VERSION = "partner-network-v3-2026-09-17"
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


@dataclass(frozen=True)
class PartnerEligibilityDecision:
    eligible_for_activation: bool
    status: str
    legal_type: str
    policy_version: str = PARTNER_POLICY_VERSION
    reasons: tuple[str, ...] = field(default_factory=tuple)

    def to_dict(self) -> dict[str, object]:
        return {
            "eligible_for_activation": self.eligible_for_activation,
            "status": self.status,
            "legal_type": self.legal_type,
            "policy_version": self.policy_version,
            "reasons": list(self.reasons),
        }


def classify_partner_eligibility(
    *,
    legal_type: str,
    is_saudi_national_or_entity: bool,
    independent_activity_authorized: bool = False,
    employee_like_control: bool = False,
    commercial_agency_claimed: bool = False,
    regulated_brokerage: bool = False,
    terms_accepted: bool = False,
    certification_passed: bool = False,
    tax_profile_recorded: bool = False,
) -> PartnerEligibilityDecision:
    """Fail closed before partner activation; this does not create employment/agency status."""
    reasons: list[str] = []
    if legal_type not in {"individual", "sole_proprietor", "company"}:
        reasons.append("unknown_legal_type")
    if employee_like_control:
        reasons.append("possible_employment_relationship")
    if (not is_saudi_national_or_entity and legal_type in {"individual", "sole_proprietor"}
            and not independent_activity_authorized):
        reasons.append("non_saudi_independent_activity_authorization_required")
    if commercial_agency_claimed:
        reasons.append("commercial_agency_legal_review_required")
    if regulated_brokerage:
        reasons.append("regulated_brokerage_license_review_required")
    if reasons:
        return PartnerEligibilityDecision(False, "legal_hold", legal_type, reasons=tuple(reasons))
    if not tax_profile_recorded:
        return PartnerEligibilityDecision(False, "tax_profile_pending", legal_type, reasons=("tax_profile_not_recorded",))
    if not terms_accepted:
        return PartnerEligibilityDecision(False, "terms_pending", legal_type, reasons=("terms_not_accepted",))
    if not certification_passed:
        return PartnerEligibilityDecision(False, "certification_pending", legal_type, reasons=("certification_not_passed",))
    return PartnerEligibilityDecision(True, "active", legal_type)


def requires_no_mlm_hold(
    *,
    recruitment_only_commission: bool = False,
    downline_override_commission: bool = False,
    multi_partner_split: bool = False,
    same_opportunity_contribution: bool = True,
) -> tuple[bool, tuple[str, ...]]:
    reasons: list[str] = []
    if recruitment_only_commission:
        reasons.append("recruitment_only_commission_prohibited")
    if downline_override_commission:
        reasons.append("downline_override_commission_prohibited")
    if multi_partner_split and not same_opportunity_contribution:
        reasons.append("multi_partner_split_requires_same_opportunity_contribution")
    return bool(reasons), tuple(reasons)


def build_partner_policy_receipt(
    *,
    receipt_type: str,
    entity_id: str,
    state: str,
    policy_version: str = PARTNER_POLICY_VERSION,
    evidence_refs: tuple[str, ...] | list[str] = (),
) -> dict[str, Any]:
    """Build a deterministic receipt payload/hash; storage/immutability belongs to Company Machine."""
    if not receipt_type.strip() or not entity_id.strip() or not state.strip() or not policy_version.strip():
        raise ValueError("receipt_type, entity_id, state and policy_version are required")
    payload: dict[str, Any] = {
        "receipt_type": receipt_type.strip(),
        "entity_id": entity_id.strip(),
        "state": state.strip(),
        "policy_version": policy_version.strip(),
        "evidence_refs": sorted({ref.strip() for ref in evidence_refs if ref and ref.strip()}),
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    payload["content_sha256"] = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    return payload

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
    legal_classification_clear: bool = True,
    mlm_or_downline_violation: bool = False,
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
    if not legal_classification_clear:
        reasons.append("partner_legal_classification_hold")
    if mlm_or_downline_violation:
        reasons.append("mlm_or_downline_commission_prohibited")
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
    misleading_or_guaranteed_claim: bool = False,
    non_saudi_independent_activity: bool = False,
    independent_activity_authorized: bool = False,
    possible_employment_relationship: bool = False,
    mlm_or_downline_commission: bool = False,
    commercial_agency_or_regulated_brokerage: bool = False,
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
    if misleading_or_guaranteed_claim:
        reasons.append("misleading_or_guaranteed_claim")
    if non_saudi_independent_activity and not independent_activity_authorized:
        reasons.append("non_saudi_independent_activity_authorization_required")
    if possible_employment_relationship:
        reasons.append("possible_employment_relationship")
    if mlm_or_downline_commission:
        reasons.append("mlm_or_downline_commission_prohibited")
    if commercial_agency_or_regulated_brokerage:
        reasons.append("regulated_relationship_legal_review_required")
    return bool(reasons), tuple(reasons)
