"""Normalized caller-intent contract; never data, commercial or send authority."""
from __future__ import annotations

import hashlib
import json
import re
from decimal import Decimal
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, StrictBool, field_validator

REQUEST_SCHEMA = "dealix.market-to-delivery.intake-request.v1"


class _StrictBody(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    @field_validator("*", mode="after")
    @classmethod
    def reject_control_characters(cls, value: Any) -> Any:
        if isinstance(value, str) and any(
            ord(char) < 32 and char not in "\n\t" for char in value
        ):
            raise ValueError("control_characters_not_allowed")
        return value


class IntakeEvidenceRef(_StrictBody):
    ref: str = Field(min_length=1, max_length=256)
    sha256: str = Field(pattern=r"^[a-f0-9]{64}$")


class MarketToDeliveryIntakeBody(_StrictBody):
    request_id: str = Field(min_length=1, max_length=80,
                           pattern=r"^[A-Za-z0-9][A-Za-z0-9_.:-]{0,79}$")
    account_id: str = Field(min_length=1, max_length=64)
    company_name: str = Field(min_length=1, max_length=255)
    source_id: str = Field(min_length=1, max_length=64)
    project_id: str = Field(min_length=1, max_length=80,
                           pattern=r"^[A-Za-z0-9][A-Za-z0-9_.:-]{0,79}$")
    problem: str = Field(min_length=1, max_length=4000)
    customer_context: str | None = Field(default=None, max_length=4000)
    current_workflow: str | None = Field(default=None, max_length=4000)
    baseline: str | None = Field(default=None, max_length=4000)
    desired_outcome: str | None = Field(default=None, max_length=4000)
    constraints: str | None = Field(default=None, max_length=4000)
    evidence_refs: list[IntakeEvidenceRef] = Field(default_factory=list, max_length=20)
    data_authorized: StrictBool
    estimated_cost_sar: Decimal | None = Field(
        default=None, ge=0, le=1_000_000_000, decimal_places=2)
    target_margin_pct: Decimal | None = Field(
        default=None, ge=0, le=90, decimal_places=2)

    @field_validator("estimated_cost_sar", "target_margin_pct", mode="before")
    @classmethod
    def reject_boolean_money(cls, value: Any) -> Any:
        if isinstance(value, bool):
            raise ValueError("boolean_is_not_money")
        return value

    @field_validator("customer_context", "current_workflow", "baseline",
                     "desired_outcome", "constraints", mode="after")
    @classmethod
    def optional_empty_is_missing(cls, value: str | None) -> str | None:
        return value or None


def intake_request_fingerprint(body: MarketToDeliveryIntakeBody, tenant_id: str) -> str:
    """Bind all normalized caller fields and the authenticated tenant.

    Independent of generated artifacts, catalogue edits and engine versions.
    The authorization boolean remains an operator attestation, not consent.
    """
    if not isinstance(tenant_id, str) or not re.fullmatch(
        r"[A-Za-z0-9][A-Za-z0-9_.:-]{0,63}", tenant_id
    ):
        raise ValueError("authenticated_tenant_invalid")
    payload = body.model_dump(mode="json")
    payload["evidence_refs"] = [
        {"ref": ref, "sha256": sha}
        for ref, sha in sorted({(item.ref, item.sha256) for item in body.evidence_refs})
    ]
    for field in ("estimated_cost_sar", "target_margin_pct"):
        value = getattr(body, field)
        payload[field] = format(value, ".2f") if value is not None else None
    canonical = json.dumps(
        {"schema_version": REQUEST_SCHEMA, "tenant_id": tenant_id, "input": payload},
        ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False,
    ).encode("utf-8")
    return hashlib.sha256(canonical).hexdigest()
