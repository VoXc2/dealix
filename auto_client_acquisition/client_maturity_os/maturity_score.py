"""Client maturity score — seven weighted dimensions (0–100 each)."""

from __future__ import annotations

from dataclasses import dataclass

_WEIGHTS: tuple[int, ...] = (15, 15, 15, 20, 15, 10, 10)


@dataclass(frozen=True, slots=True)
class ClientMaturityDimensions:
    leadership_alignment: int
    data_readiness: int
    workflow_ownership: int
    governance_coverage: int
    proof_discipline: int
    adoption: int
    operating_cadence: int


def _clamp_pct(value: int) -> int:
    if value < 0:
        return 0
    if value > 100:
        return 100
    return value


def client_maturity_score(dimensions: ClientMaturityDimensions) -> int:
    d = dimensions
    values = (
        _clamp_pct(d.leadership_alignment),
        _clamp_pct(d.data_readiness),
        _clamp_pct(d.workflow_ownership),
        _clamp_pct(d.governance_coverage),
        _clamp_pct(d.proof_discipline),
        _clamp_pct(d.adoption),
        _clamp_pct(d.operating_cadence),
    )
    total = sum(v * w for v, w in zip(values, _WEIGHTS, strict=True))
    return min(100, total // 100)


def client_maturity_band(score: int) -> str:
    if score >= 85:
        return "enterprise_expansion_ready"
    if score >= 70:
        return "retainer_workspace_ready"
    if score >= 55:
        return "sprint_enablement"
    if score >= 35:
        return "diagnostic_readiness"
    return "do_not_deploy_ai_workflow"


MATURITY_LADDER_STATES: tuple[str, ...] = (
    "AI Chaos",
    "AI Awareness",
    "Structured Use Case",
    "AI-Assisted Workflow",
    "Governed AI Workflow",
    "Operating AI Capability",
    "Multi-Workflow AI OS",
    "Enterprise AI Control Plane",
)
