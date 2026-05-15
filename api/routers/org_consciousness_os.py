"""org_consciousness_os router — Systems 36-45.

Read-only organizational-consciousness synthesis. Every payload carries a
``governance_decision`` per repo convention. The two POST endpoints accept
input-only ledger events / cohort ids — they persist nothing.
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Query
from pydantic import BaseModel, Field

from auto_client_acquisition.capital_os.capital_ledger import CapitalLedgerEvent
from auto_client_acquisition.governance_os.runtime_decision import GovernanceDecision
from auto_client_acquisition.org_consciousness_os.causal import build_causal_report
from auto_client_acquisition.org_consciousness_os.consciousness import (
    synthesize_consciousness,
)
from auto_client_acquisition.org_consciousness_os.learning import (
    detect_learning_patterns,
)
from auto_client_acquisition.org_consciousness_os.meta_orchestration import (
    recommend_meta_orchestration,
)
from auto_client_acquisition.org_consciousness_os.resilience import compute_resilience
from auto_client_acquisition.org_consciousness_os.schemas import DOCTRINE_POSTURE
from auto_client_acquisition.org_consciousness_os.self_evolving import (
    propose_optimizations,
)
from auto_client_acquisition.org_consciousness_os.signals import (
    compute_execution_health,
)
from auto_client_acquisition.org_consciousness_os.strategic import benchmark_customer
from auto_client_acquisition.org_consciousness_os.trust import compute_trust
from auto_client_acquisition.org_consciousness_os.value import (
    compute_operational_value,
)
from auto_client_acquisition.org_consciousness_os.workforce_governance import (
    build_workforce_governance,
)
from auto_client_acquisition.proof_architecture_os.value_ledger import ValueLedgerEvent

router = APIRouter(prefix="/api/v1/org-consciousness", tags=["org-consciousness"])

_ALLOW = GovernanceDecision.ALLOW.value


def _wrap(payload: dict[str, Any]) -> dict[str, Any]:
    payload["governance_decision"] = _ALLOW
    return payload


# ── Request bodies (input-only — never persisted) ────────────────


class ValueEventIn(BaseModel):
    value_event_id: str
    project_id: str
    client_id: str
    value_type: str
    metric: str
    before: int
    after: int
    evidence: str
    confidence: str
    limitations: str


class CapitalEventIn(BaseModel):
    capital_event_id: str
    project_id: str
    client_id: str
    asset_type: str
    title: str
    description: str
    evidence: str


class ValueRequest(BaseModel):
    value_events: list[ValueEventIn] = Field(default_factory=list)
    capital_events: list[CapitalEventIn] = Field(default_factory=list)
    window_days: int = Field(default=30, ge=1, le=365)


class StrategicRequest(BaseModel):
    customer_id: str = Field(..., min_length=1)
    cohort_customer_ids: list[str] = Field(default_factory=list)
    window_days: int = Field(default=30, ge=1, le=365)


# ── Endpoints ────────────────────────────────────────────────────


@router.get("/status")
async def status() -> dict[str, Any]:
    return _wrap({"module": "org_consciousness_os", "guardrails": dict(DOCTRINE_POSTURE)})


@router.get("/{customer_id}")
async def get_snapshot(
    customer_id: str,
    window_days: int = Query(30, ge=1, le=365),
) -> dict[str, Any]:
    snapshot = synthesize_consciousness(customer_id=customer_id, window_days=window_days)
    return _wrap(snapshot.to_dict())


@router.get("/{customer_id}/execution-health")
async def get_execution_health(
    customer_id: str,
    window_days: int = Query(30, ge=1, le=365),
) -> dict[str, Any]:
    signal = compute_execution_health(customer_id=customer_id, window_days=window_days)
    return _wrap(signal.to_dict())


@router.get("/{customer_id}/causal")
async def get_causal(
    customer_id: str,
    window_days: int = Query(30, ge=1, le=365),
) -> dict[str, Any]:
    report = build_causal_report(customer_id=customer_id, window_days=window_days)
    return _wrap(report.to_dict())


@router.get("/{customer_id}/workforce-governance")
async def get_workforce_governance(customer_id: str) -> dict[str, Any]:
    report = build_workforce_governance(customer_id=customer_id)
    return _wrap(report.to_dict())


@router.get("/{customer_id}/resilience")
async def get_resilience(
    customer_id: str,
    window_days: int = Query(30, ge=1, le=365),
) -> dict[str, Any]:
    signal = compute_resilience(customer_id=customer_id, window_days=window_days)
    return _wrap(signal.to_dict())


@router.get("/{customer_id}/trust")
async def get_trust(customer_id: str) -> dict[str, Any]:
    signal = compute_trust(customer_id=customer_id)
    return _wrap(signal.to_dict())


@router.post("/{customer_id}/value")
async def post_value(customer_id: str, body: ValueRequest) -> dict[str, Any]:
    value_events = [ValueLedgerEvent(**e.model_dump()) for e in body.value_events]
    capital_events = [CapitalLedgerEvent(**e.model_dump()) for e in body.capital_events]
    signal = compute_operational_value(
        customer_id=customer_id,
        value_events=value_events,
        capital_events=capital_events,
        friction_window_days=body.window_days,
    )
    return _wrap(signal.to_dict())


@router.get("/{customer_id}/learning")
async def get_learning(
    customer_id: str,
    window_days: int = Query(30, ge=1, le=365),
    lookback_windows: int = Query(4, ge=2, le=12),
) -> dict[str, Any]:
    report = detect_learning_patterns(
        customer_id=customer_id,
        window_days=window_days,
        lookback_windows=lookback_windows,
    )
    return _wrap(report.to_dict())


@router.get("/{customer_id}/meta-orchestration")
async def get_meta_orchestration(
    customer_id: str,
    window_days: int = Query(30, ge=1, le=365),
) -> dict[str, Any]:
    rec = recommend_meta_orchestration(customer_id=customer_id, window_days=window_days)
    return _wrap(rec.to_dict())


@router.post("/strategic")
async def post_strategic(body: StrategicRequest) -> dict[str, Any]:
    ids = {body.customer_id, *body.cohort_customer_ids}
    cohort = {
        cid: compute_execution_health(customer_id=cid, window_days=body.window_days) for cid in ids
    }
    report = benchmark_customer(customer_id=body.customer_id, cohort_signals=cohort)
    return _wrap(report.to_dict())


@router.get("/{customer_id}/evolution-proposals")
async def get_evolution_proposals(
    customer_id: str,
    window_days: int = Query(30, ge=1, le=365),
) -> dict[str, Any]:
    learning = detect_learning_patterns(customer_id=customer_id, window_days=window_days)
    resilience = compute_resilience(customer_id=customer_id, window_days=window_days)
    workforce = build_workforce_governance(customer_id=customer_id)
    proposals = propose_optimizations(
        customer_id=customer_id,
        learning=learning,
        resilience=resilience,
        workforce=workforce,
    )
    return _wrap(
        {
            "customer_id": customer_id,
            "count": len(proposals),
            "proposals": [p.to_dict() for p in proposals],
        }
    )
