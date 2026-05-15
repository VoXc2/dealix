"""The 4-phase AI Company Operating System roadmap and its gates.

Phases 3 and 4 are ``deferred_gated``: the Operating Constitution
(Article 13) forbids activating Build-Order Phase H "Scale" and Waves
2-5 before 3 paid pilots deliver proof. They are scaffolded here, never
activated, until the activation condition holds.
"""

from __future__ import annotations

from typing import Any

from auto_client_acquisition.company_os.schemas import PhaseGate, RoadmapPhase

_REQUIRED_PAID_PILOTS = 3

_GATES: tuple[PhaseGate, ...] = (
    PhaseGate(
        phase=RoadmapPhase.FOUNDATION,
        name_en="Foundation",
        name_ar="التأسيس",
        entry_criteria=("repository live", "canonical modules in place"),
        exit_criteria=(
            "company_os spine shipped",
            "7 systems registered and maturity-scored",
            "read-only company-os API live",
        ),
        deferred_gated=False,
        activation_condition="active_now",
    ),
    PhaseGate(
        phase=RoadmapPhase.DELIVERY_MATURITY,
        name_en="Delivery Maturity",
        name_ar="نضج التسليم",
        entry_criteria=("Foundation exit criteria met", "1 paid pilot delivered"),
        exit_criteria=(
            "repeatable delivery playbooks",
            "QA checklists and ROI reports per service",
            "2 completed pilots with proof packs",
        ),
        deferred_gated=False,
        activation_condition="1_paid_pilot_delivered",
    ),
    PhaseGate(
        phase=RoadmapPhase.AGENTIC_PLATFORM,
        name_en="Agentic Platform",
        name_ar="المنصة الوكيلة",
        entry_criteria=("3 paid pilots delivered", "founder sign-off recorded"),
        exit_criteria=(
            "agent runtime and orchestration live",
            "human-in-the-loop oversight enforced",
        ),
        deferred_gated=True,
        activation_condition="3_paid_pilots_signed",
    ),
    PhaseGate(
        phase=RoadmapPhase.ENTERPRISE_READINESS,
        name_en="Enterprise Readiness",
        name_ar="الجاهزية المؤسسية",
        entry_criteria=("Agentic Platform exit criteria met",),
        exit_criteria=(
            "SSO and advanced governance live",
            "compliance and SLA commitments published",
        ),
        deferred_gated=True,
        activation_condition="3_paid_pilots_signed",
    ),
)


def phase_gates() -> list[PhaseGate]:
    """All 4 roadmap phase gates in order."""
    return list(_GATES)


def get_phase_gate(phase: RoadmapPhase) -> PhaseGate:
    """Return the gate for one phase. Raises KeyError if unknown."""
    for g in _GATES:
        if g.phase == phase:
            return g
    raise KeyError(f"unknown roadmap phase: {phase}")


def is_phase_active(phase: RoadmapPhase, *, paid_pilots: int = 0) -> bool:
    """Whether a phase may be activated given the paid-pilot count.

    Deferred-gated phases activate only once ``paid_pilots`` reaches the
    Constitution's threshold of 3.
    """
    gate = get_phase_gate(phase)
    if not gate.deferred_gated:
        return True
    return paid_pilots >= _REQUIRED_PAID_PILOTS


def roadmap_digest(*, paid_pilots: int = 0) -> dict[str, Any]:
    """Machine-readable roadmap snapshot with live activation status."""
    return {
        "required_paid_pilots": _REQUIRED_PAID_PILOTS,
        "paid_pilots": paid_pilots,
        "phases": [
            {**g.to_dict(), "active": is_phase_active(g.phase, paid_pilots=paid_pilots)}
            for g in _GATES
        ],
    }
