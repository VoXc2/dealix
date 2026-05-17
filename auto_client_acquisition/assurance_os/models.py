"""Data models for the Dealix Assurance System.

The Assurance System is a UNIFICATION LAYER: it reads existing Dealix
infrastructure through pluggable adapters and runs the 7-layer pipeline
(Gate -> Scorecard -> Test -> Evidence -> KPI -> Review -> Improvement).

Doctrine: any business fact that is not available is represented as
``None`` / ``"unknown"`` — never a fabricated number. ``AdapterResult``
with ``Status.UNKNOWN`` is the hinge that keeps this honest.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class Status(str, Enum):
    """Outcome of an adapter read."""

    OK = "ok"            # real value read from a wired source
    UNKNOWN = "unknown"  # source not wired / no data — value is None
    ERROR = "error"      # source wired but the read failed


@dataclass
class AdapterResult:
    """Uniform return type for every adapter read."""

    status: Status
    value: Any
    source: str
    detail: str = ""

    @property
    def is_known(self) -> bool:
        return self.status is Status.OK


# ── Inputs ──────────────────────────────────────────────────────────
@dataclass
class AssuranceInputs:
    """Business facts supplied by the caller (founder / dashboard).

    Anything left empty/None surfaces as ``unknown`` in the report — the
    Assurance System never invents data to fill a gap.
    """

    funnel_counts: dict[str, int] = field(default_factory=dict)
    gate_answers: dict[str, bool] = field(default_factory=dict)
    machine_maturity: dict[str, int] = field(default_factory=dict)
    acceptance_results: dict[str, str] = field(default_factory=dict)
    kpi_values: dict[str, float] = field(default_factory=dict)
    evidence_completeness_pct: float | None = None
    lead_scoring_coverage_pct: float | None = None
    support_high_risk_escalation_pct: float | None = None
    affiliate_payout_before_payment_count: int | None = None
    approval_compliance_pct: float | None = None
    week_of: str = ""
    month: str = ""
    experiments: list[dict[str, Any]] = field(default_factory=list)
    improvement_items: list[dict[str, Any]] = field(default_factory=list)


# ── Layer 1: Gates ──────────────────────────────────────────────────
@dataclass
class GateCriterion:
    id: str
    label_en: str
    label_ar: str
    passed: bool | None = None  # None = unknown


@dataclass
class GateResult:
    gate_id: str
    name_en: str
    name_ar: str
    criteria: list[GateCriterion] = field(default_factory=list)
    passed: bool = False
    unknown_count: int = 0


# ── Layer 2: Scorecards & Health ────────────────────────────────────
@dataclass
class MachineScorecard:
    machine: str
    label_en: str
    label_ar: str
    min_bar: int
    maturity: int | None = None  # 0-5, None = unknown
    met: bool = False


@dataclass
class HealthComponent:
    name: str
    weight: int
    contribution: float | None = None  # 0..weight, None = unknown
    basis: str = ""


@dataclass
class HealthScore:
    components: list[HealthComponent] = field(default_factory=list)
    total: float = 0.0          # sum of KNOWN contributions
    known_weight: int = 0       # sum of weights with known data (max 100)
    unknown_components: list[str] = field(default_factory=list)
    meets_threshold: bool = False  # total >= 75 AND no unknown component


# ── Layer 3: Acceptance Tests ───────────────────────────────────────
@dataclass
class AcceptanceTestResult:
    id: str
    category: str
    name_en: str
    name_ar: str
    expected: str
    result: str = "unknown"  # pass / fail / unknown


# ── Layer 4: Evidence / No-Scale Conditions ─────────────────────────
@dataclass
class NoScaleCondition:
    id: str
    label_en: str
    label_ar: str
    requirement: str
    actual: str
    satisfied: bool | None = None  # None = unknown -> blocks scaling


# ── Layer 5: KPI / Funnel ───────────────────────────────────────────
@dataclass
class FunnelRung:
    key: str
    label_en: str
    label_ar: str
    journey_stages: list[str] = field(default_factory=list)
    count: int | None = None


@dataclass
class FunnelSnapshot:
    rungs: list[FunnelRung] = field(default_factory=list)
    conversion: dict[str, float | None] = field(default_factory=dict)
    north_star: dict[str, Any] = field(default_factory=dict)


# ── Layer 6: Review ─────────────────────────────────────────────────
@dataclass
class OperatingReview:
    week_of: str = ""
    answered_questions: list[dict[str, str]] = field(default_factory=list)
    bottleneck: str = "unknown"
    decisions: list[str] = field(default_factory=list)


@dataclass
class BoardPack:
    month: str = ""
    sections: dict[str, Any] = field(default_factory=dict)


# ── Layer 7: Improvement ────────────────────────────────────────────
@dataclass
class Experiment:
    id: str
    hypothesis: str
    metric: str
    timebox_days: int = 7
    decision: str = "pending"  # keep / kill / iterate / pending


@dataclass
class ImprovementItem:
    id: str
    source: str
    title: str
    recommended_action: str
    status: str = "proposed"  # proposed / approved / done


# ── Composite report ────────────────────────────────────────────────
@dataclass
class AssuranceReport:
    generated_at: str
    layers: list[str]
    gates: list[GateResult] = field(default_factory=list)
    scorecards: list[MachineScorecard] = field(default_factory=list)
    health: HealthScore = field(default_factory=HealthScore)
    acceptance_tests: list[AcceptanceTestResult] = field(default_factory=list)
    no_scale_conditions: list[NoScaleCondition] = field(default_factory=list)
    funnel: FunnelSnapshot = field(default_factory=FunnelSnapshot)
    review: OperatingReview = field(default_factory=OperatingReview)
    experiments: list[Experiment] = field(default_factory=list)
    improvement: list[ImprovementItem] = field(default_factory=list)
    verdict: str = "no_scale"          # scale / no_scale
    verdict_reasons: list[str] = field(default_factory=list)
