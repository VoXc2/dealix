"""Definition-of-Done and acceptance-gate evaluation for machines.

A machine is never "done" because it ran once. It is done when its
Definition-of-Done checklist is satisfied and its acceptance gate passes.
These functions are pure and never raise.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from auto_client_acquisition.execution_assurance_os.registry import MachineSpec


@dataclass(frozen=True, slots=True)
class DodResult:
    """Outcome of evaluating a machine's Definition of Done."""

    machine_id: str
    items_met: int
    items_total: int
    pct: float
    blocking_gaps: tuple[str, ...]

    @property
    def complete(self) -> bool:
        return self.items_total > 0 and self.items_met == self.items_total


@dataclass(frozen=True, slots=True)
class GateResult:
    """Outcome of evaluating a machine's acceptance gate."""

    machine_id: str
    passed: bool
    criteria: tuple[str, ...]
    unmet: tuple[str, ...] = field(default_factory=tuple)


def evaluate_dod(spec: MachineSpec) -> DodResult:
    """Compute Definition-of-Done completion for one machine."""
    total = len(spec.definition_of_done)
    met = sum(1 for d in spec.definition_of_done if d.met)
    pct = round((met / total * 100), 1) if total else 0.0
    blocking = tuple(d.text for d in spec.definition_of_done if not d.met)
    return DodResult(
        machine_id=spec.id,
        items_met=met,
        items_total=total,
        pct=pct,
        blocking_gaps=blocking,
    )


def evaluate_acceptance_gate(spec: MachineSpec) -> GateResult:
    """Evaluate a machine's acceptance gate.

    A gate passes only when the machine has reached its target maturity
    AND every Definition-of-Done item is met. Anything less is reported
    with concrete unmet reasons — no fake green.
    """
    dod = evaluate_dod(spec)
    unmet: list[str] = []

    if spec.maturity_score < spec.scorecard_target:
        unmet.append(
            f"maturity {spec.maturity_score} below target "
            f"{spec.scorecard_target}"
        )
    for gap in dod.blocking_gaps:
        unmet.append(f"DoD gap: {gap}")

    return GateResult(
        machine_id=spec.id,
        passed=not unmet,
        criteria=spec.acceptance_gate,
        unmet=tuple(unmet),
    )


__all__ = [
    "DodResult",
    "GateResult",
    "evaluate_acceptance_gate",
    "evaluate_dod",
]
