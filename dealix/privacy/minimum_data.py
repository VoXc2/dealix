"""Typed, fail-closed dataset contract for Dealix's minimum-data first Pilot.

The exact Pilot dataset is intentionally reference-first: it accepts opaque,
pseudonymous identifiers, enums, and aggregate numeric metrics only. It does
not accept arbitrary company notes, contact fields, message bodies, or raw
customer text. Richer context must stay behind separately approved, source-bound
references until its own privacy/data-flow gate is proven.
"""

from __future__ import annotations

import re
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, StringConstraints, field_validator

OpaqueId = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        min_length=1,
        max_length=96,
        pattern=r"^[A-Za-z0-9_.:-]+$",
    ),
]

_EMAIL = re.compile(r"[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}", re.IGNORECASE)
_PHONE = re.compile(r"(?<!\w)(?:\+?966|0)?5\d{8}(?!\w)")
_SECRET_HINT = re.compile(
    r"(?:sk-[A-Za-z0-9_-]{16,}|Bearer\s+[A-Za-z0-9._-]{12,}|AKIA[A-Z0-9]{16})",
    re.IGNORECASE,
)


def _reject_obvious_personal_or_secret(value: str, field_name: str) -> str:
    if _EMAIL.search(value):
        raise ValueError(f"{field_name} must not contain an email address")
    if _PHONE.search(value):
        raise ValueError(f"{field_name} must not contain a Saudi mobile number")
    if _SECRET_HINT.search(value):
        raise ValueError(f"{field_name} must not contain a credential/token pattern")
    return value


class AggregateMetric(BaseModel):
    """Aggregate baseline/outcome metric without arbitrary free text."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    metric_id: OpaqueId
    metric_definition_ref: OpaqueId
    value: float = Field(allow_inf_nan=False)
    unit: Literal["count", "percent", "hours", "days", "ratio"]
    source_ref: OpaqueId
    measurement_window_ref: OpaqueId

    @field_validator(
        "metric_id",
        "metric_definition_ref",
        "source_ref",
        "measurement_window_ref",
    )
    @classmethod
    def ids_must_be_pseudonymous(cls, value: str, info):  # type: ignore[no-untyped-def]
        return _reject_obvious_personal_or_secret(value, info.field_name)


class PseudonymousOpportunity(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    opportunity_id: OpaqueId
    stage: Literal[
        "signal",
        "qualified",
        "discovery",
        "proposal",
        "approval",
        "delivery",
        "won",
        "lost",
        "paused",
    ]
    age_days: int = Field(ge=0, le=3650)
    value_band: Literal["unknown", "low", "medium", "high", "strategic"]
    next_action_status: Literal["missing", "ready", "blocked", "done"]
    owner_role: Literal[
        "founder",
        "sales",
        "sales_manager",
        "revops",
        "finance",
        "operations",
        "customer_success",
        "executive",
    ]
    source_ref: OpaqueId

    @field_validator("opportunity_id", "source_ref")
    @classmethod
    def ids_must_be_pseudonymous(cls, value: str, info):  # type: ignore[no-untyped-def]
        return _reject_obvious_personal_or_secret(value, info.field_name)


class MinimumDataPilotDataset(BaseModel):
    """One structured, non-personal dataset for a bounded Pilot run."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    profile_id: Literal["revenue_command_minimum_data_v1"]
    tenant_id: OpaqueId
    company_id: OpaqueId
    company_context_source_ref: OpaqueId
    icp_id: OpaqueId
    workflow_id: OpaqueId
    acceptance_criteria_ref: OpaqueId
    approval_policy_ref: OpaqueId
    proof_target_id: OpaqueId
    accountable_owner_role: Literal[
        "founder",
        "sales_manager",
        "revops",
        "operations",
        "executive",
    ]
    baseline_metrics: tuple[AggregateMetric, ...] = Field(min_length=1, max_length=50)
    opportunities: tuple[PseudonymousOpportunity, ...] = Field(default=(), max_length=1000)

    @field_validator(
        "tenant_id",
        "company_id",
        "company_context_source_ref",
        "icp_id",
        "workflow_id",
        "acceptance_criteria_ref",
        "approval_policy_ref",
        "proof_target_id",
    )
    @classmethod
    def ids_must_be_pseudonymous(cls, value: str, info):  # type: ignore[no-untyped-def]
        return _reject_obvious_personal_or_secret(value, info.field_name)

    @field_validator("opportunities")
    @classmethod
    def opportunity_ids_must_be_unique(
        cls, value: tuple[PseudonymousOpportunity, ...]
    ) -> tuple[PseudonymousOpportunity, ...]:
        ids = [item.opportunity_id for item in value]
        if len(ids) != len(set(ids)):
            raise ValueError("opportunity_id values must be unique")
        return value

    @field_validator("baseline_metrics")
    @classmethod
    def metric_ids_must_be_unique(
        cls, value: tuple[AggregateMetric, ...]
    ) -> tuple[AggregateMetric, ...]:
        ids = [item.metric_id for item in value]
        if len(ids) != len(set(ids)):
            raise ValueError("metric_id values must be unique")
        return value
