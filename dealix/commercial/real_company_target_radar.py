"""Truth-safe real-company research radar for Dealix.

This module stores public/authoritative company evidence only. A discovered
company is not a relationship, consent record, opportunity, pipeline, or revenue.
"""
from __future__ import annotations

import re
from datetime import UTC, datetime
from typing import Iterable
from urllib.parse import urlparse

from pydantic import BaseModel, ConfigDict, Field, field_validator

RESEARCH_ONLY = "RESEARCH_ONLY"
UNKNOWN = "UNKNOWN"


def _slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


class RealCompanyRecord(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    company_id: str
    display_name: str
    ar_name: str = UNKNOWN
    en_name: str = UNKNOWN
    source_url: str
    source_authority: str
    source_external_id: str = UNKNOWN
    observed_at: str
    sector_id: str
    buyer_role_hypotheses: list[str] = Field(default_factory=list)
    public_evidence: list[str] = Field(default_factory=list)
    problem_hypotheses: list[str] = Field(default_factory=list)
    diagnostic_families: list[str] = Field(default_factory=list)
    offer_match_candidates: list[str] = Field(default_factory=list)
    procurement_partner_path: str = UNKNOWN
    truth_class: str = RESEARCH_ONLY
    relationship: bool = False
    consent: bool = False
    pipeline: bool = False
    revenue: bool = False

    @field_validator("source_url")
    @classmethod
    def _authoritative_url(cls, value: str) -> str:
        parsed = urlparse(value)
        if parsed.scheme != "https" or not parsed.netloc:
            raise ValueError("source_url must be an absolute https URL")
        return value

    @field_validator("relationship", "consent", "pipeline", "revenue")
    @classmethod
    def _research_flags_fail_closed(cls, value: bool) -> bool:
        if value:
            raise ValueError("research-only company records cannot grant authority")
        return value


class InternalAccountPlan(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    company_id: str
    company_name: str
    sector_id: str
    evidence_refs: list[str]
    buyer_role_hypotheses: list[str]
    problem_hypotheses: list[str]
    diagnostic_families: list[str]
    offer_match_candidates: list[str]
    truth_class: str = "INTERNAL_HYPOTHESIS"
    customer_fact_claims_allowed: bool = False
    external_send_allowed: bool = False
    proposal_state: str = "ACCOUNT_PLAN_ONLY"


class RealCompanyTargetRadar:
    """Deterministic, persistence-neutral company research index."""

    def __init__(self, records: Iterable[RealCompanyRecord] = ()) -> None:
        self._records: dict[str, RealCompanyRecord] = {}
        for record in records:
            self.add(record)

    @staticmethod
    def identity_key(record: RealCompanyRecord) -> str:
        external = record.source_external_id
        if external and external != UNKNOWN:
            return f"{_slug(record.source_authority)}::{_slug(external)}"
        return f"{_slug(record.source_authority)}::{_slug(record.display_name)}"

    def add(self, record: RealCompanyRecord) -> str:
        key = self.identity_key(record)
        self._records[key] = record
        return key

    def records(self) -> list[RealCompanyRecord]:
        return sorted(self._records.values(), key=lambda item: item.company_id)

    def build_account_plan(self, company_id: str) -> InternalAccountPlan:
        record = next(item for item in self._records.values() if item.company_id == company_id)
        return InternalAccountPlan(
            company_id=record.company_id,
            company_name=record.display_name,
            sector_id=record.sector_id,
            evidence_refs=[record.source_url, *record.public_evidence],
            buyer_role_hypotheses=record.buyer_role_hypotheses,
            problem_hypotheses=record.problem_hypotheses,
            diagnostic_families=record.diagnostic_families,
            offer_match_candidates=record.offer_match_candidates,
        )

    def receipt(self) -> dict[str, object]:
        return {
            "schema": "dealix.real-company-target-radar.v1",
            "generated_at": datetime.now(UTC).isoformat(),
            "company_count": len(self._records),
            "truth_policy": "RESEARCH_ONLY_NO_RELATIONSHIP_NO_CONSENT_NO_PIPELINE_NO_REVENUE",
            "records": [item.model_dump() for item in self.records()],
        }


def customer_specific_proposal_allowed(*, qualified_problem_ref: str = "", explicit_request_ref: str = "", evidence_resolver=None) -> bool:
    """Fail closed unless canonical evidence validates both truth class and real interaction."""
    if evidence_resolver is None:
        return False
    candidates = (
        (qualified_problem_ref.strip(), "QUALIFIED_PROBLEM"),
        (explicit_request_ref.strip(), "EXPLICIT_CUSTOMER_REQUEST"),
    )
    for ref, expected_class in candidates:
        if not ref:
            continue
        evidence = evidence_resolver(ref)
        if (
            isinstance(evidence, dict)
            and evidence.get("truth_class") == expected_class
            and evidence.get("real_interaction") is True
        ):
            return True
    return False


__all__ = [
    "InternalAccountPlan",
    "RealCompanyRecord",
    "RealCompanyTargetRadar",
    "customer_specific_proposal_allowed",
]
