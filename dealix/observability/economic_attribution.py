"""Internal workload economics and time-to-evidence attribution.

This module is a pure measurement layer over existing runs. It does not persist
events, create a scheduler, call an LLM, infer revenue, or declare customer value.
It can feed the existing CostTracker/OTel integrations when those integrations
are enabled by the host.
"""

from __future__ import annotations

import json
from copy import deepcopy
from datetime import UTC, datetime
from statistics import median
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from dealix.observability.cost_tracker import MODEL_PRICES, estimate_cost_usd

UNKNOWN = "UNKNOWN_NOT_EVIDENCE_BACKED"
SCHEMA_VERSION = "1.0.0"


class WorkloadMeasurement(BaseModel):
    """Read-only facts about one internal workload run."""

    model_config = ConfigDict(extra="forbid")

    run_id: str = Field(..., min_length=1)
    workload_id: str = Field(..., min_length=1)
    agent_id: str = Field(..., min_length=1)
    account_id: str = ""
    started_at: str = Field(..., min_length=1)
    completed_at: str = Field(..., min_length=1)
    status: str = "success"
    input_evidence_refs: list[str] = Field(default_factory=list)
    output_evidence_refs: list[str] = Field(default_factory=list)
    first_evidence_at: str = ""
    founder_minutes: float = Field(default=0.0, ge=0)
    provider: str = ""
    model: str = ""
    input_tokens: int = Field(default=0, ge=0)
    output_tokens: int = Field(default=0, ge=0)
    cached_tokens: int = Field(default=0, ge=0)
    payment_proof_refs: list[str] = Field(default_factory=list)
    synthetic_output: bool = False


class AttributionRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")

    run_id: str
    workload_id: str
    agent_id: str
    account_id: str
    started_at: str
    completed_at: str
    status: str
    duration_ms: float
    founder_minutes: float
    input_evidence_refs: list[str]
    output_evidence_refs: list[str]
    time_to_evidence_ms: float | str = UNKNOWN
    llm_cost_usd: float | str = UNKNOWN
    cost_basis: str = UNKNOWN
    evidence_state: str = UNKNOWN
    payment_proof_state: str = UNKNOWN
    payment_proof_refs: list[str] = Field(default_factory=list)
    customer_value_state: str = UNKNOWN
    verified_revenue: float | str = UNKNOWN

    def to_dict(self) -> dict[str, Any]:
        return self.model_dump(mode="json")

    def to_otel_attributes(self) -> dict[str, str | float | int]:
        """Return bounded scalar attributes safe to attach to an existing span."""

        return {
            "dealix.run_id": self.run_id,
            "dealix.workload_id": self.workload_id,
            "dealix.agent_id": self.agent_id,
            "dealix.account_id": self.account_id,
            "dealix.status": self.status,
            "dealix.duration_ms": self.duration_ms,
            "dealix.founder_minutes": self.founder_minutes,
            "dealix.evidence_state": self.evidence_state,
            "dealix.payment_proof_state": self.payment_proof_state,
        }


class AttributionReport(BaseModel):
    model_config = ConfigDict(extra="forbid")

    schema_version: str = SCHEMA_VERSION
    generated_at: str
    as_of: str
    runs: list[AttributionRecord]
    workload_summaries: list[dict[str, Any]]
    guardrails: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return deepcopy(self.model_dump(mode="json"))

    def semantic_dict(self) -> dict[str, Any]:
        data = self.to_dict()
        data.pop("generated_at", None)
        return data


class WorkloadEconomicsAttribution:
    """Validate and aggregate internal workload economics without value inflation."""

    @staticmethod
    def _parse_timestamp(value: str) -> datetime:
        try:
            parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError as exc:
            raise ValueError(f"timestamp must be ISO-8601: {value}") from exc
        if parsed.tzinfo is None:
            raise ValueError(f"timestamp must include timezone: {value}")
        return parsed.astimezone(UTC)

    @staticmethod
    def _refs(values: list[str]) -> list[str]:
        return sorted({value.strip() for value in values if value.strip()})

    def measure(self, run: WorkloadMeasurement) -> AttributionRecord:
        started = self._parse_timestamp(run.started_at)
        completed = self._parse_timestamp(run.completed_at)
        if completed < started:
            raise ValueError("completed_at cannot precede started_at")

        duration_ms = round((completed - started).total_seconds() * 1000, 3)
        input_refs = self._refs(run.input_evidence_refs)
        output_refs = self._refs(run.output_evidence_refs)
        payment_refs = self._refs(run.payment_proof_refs)

        time_to_evidence: float | str = UNKNOWN
        if run.first_evidence_at:
            first_evidence = self._parse_timestamp(run.first_evidence_at)
            if first_evidence < started or first_evidence > completed:
                raise ValueError("first_evidence_at must fall inside the workload window")
            if not output_refs:
                raise ValueError("time_to_evidence requires output_evidence_refs")
            time_to_evidence = round((first_evidence - started).total_seconds() * 1000, 3)

        llm_cost: float | str = UNKNOWN
        cost_basis = UNKNOWN
        if run.provider and run.model:
            llm_cost = estimate_cost_usd(
                run.model,
                run.input_tokens,
                run.output_tokens,
                run.cached_tokens,
            )
            cost_basis = (
                "MODEL_PRICE_TABLE"
                if run.model in MODEL_PRICES
                else "CONSERVATIVE_FALLBACK_PRICING"
            )

        evidence_state = "RECORDED" if output_refs else UNKNOWN
        payment_state = "VERIFIED" if payment_refs and not run.synthetic_output else UNKNOWN
        return AttributionRecord(
            run_id=run.run_id,
            workload_id=run.workload_id,
            agent_id=run.agent_id,
            account_id=run.account_id,
            started_at=run.started_at,
            completed_at=run.completed_at,
            status=run.status,
            duration_ms=duration_ms,
            founder_minutes=round(run.founder_minutes, 3),
            input_evidence_refs=input_refs,
            output_evidence_refs=output_refs,
            time_to_evidence_ms=time_to_evidence,
            llm_cost_usd=llm_cost,
            cost_basis=cost_basis,
            evidence_state=evidence_state,
            payment_proof_state=payment_state,
            payment_proof_refs=payment_refs if payment_state == "VERIFIED" else [],
        )

    def summarize(self, runs: list[WorkloadMeasurement]) -> AttributionReport:
        if len({run.run_id for run in runs}) != len(runs):
            raise ValueError("run_id must be unique within an attribution report")

        records = sorted(
            (self.measure(run) for run in runs),
            key=lambda record: (record.workload_id, record.run_id),
        )
        summaries: list[dict[str, Any]] = []
        by_workload: dict[str, list[AttributionRecord]] = {}
        for record in records:
            by_workload.setdefault(record.workload_id, []).append(record)

        for workload_id in sorted(by_workload):
            group = by_workload[workload_id]
            known_costs = [
                record.llm_cost_usd
                for record in group
                if isinstance(record.llm_cost_usd, (int, float))
            ]
            known_times = [
                record.time_to_evidence_ms
                for record in group
                if isinstance(record.time_to_evidence_ms, (int, float))
            ]
            output_evidence_runs = sum(1 for record in group if record.output_evidence_refs)
            summaries.append(
                {
                    "workload_id": workload_id,
                    "run_count": len(group),
                    "success_count": sum(1 for record in group if record.status == "success"),
                    "founder_minutes_total": round(
                        sum(record.founder_minutes for record in group), 3
                    ),
                    "llm_cost_usd_total": (
                        round(sum(known_costs), 6)
                        if len(known_costs) == len(group)
                        else UNKNOWN
                    ),
                    "llm_cost_known_runs": len(known_costs),
                    "output_evidence_runs": output_evidence_runs,
                    "output_evidence_count": sum(
                        len(record.output_evidence_refs) for record in group
                    ),
                    "time_to_evidence_ms_p50": (
                        round(float(median(known_times)), 3) if known_times else UNKNOWN
                    ),
                    "time_to_evidence_known_runs": len(known_times),
                }
            )

        as_of = UNKNOWN
        if records:
            latest = max(self._parse_timestamp(record.completed_at) for record in records)
            as_of = latest.isoformat()
        return AttributionReport(
            generated_at=datetime.now(UTC).isoformat(),
            as_of=as_of,
            runs=records,
            workload_summaries=summaries,
            guardrails={
                "verified_revenue": UNKNOWN,
                "customer_value": UNKNOWN,
                "payment_proof_required_for_revenue": True,
                "invoice_is_not_payment": True,
                "synthetic_evidence_is_not_customer_proof": True,
                "measurement_is_internal_attribution_only": True,
            },
        )


__all__ = [
    "AttributionRecord",
    "AttributionReport",
    "UNKNOWN",
    "WorkloadEconomicsAttribution",
    "WorkloadMeasurement",
]
