"""Layer 2b — Full Ops Health Score (out of 100).

Weighted composite across 7 components. Each component's contribution is
``(avg machine maturity / 5) * weight``. If ANY machine feeding a
component has unknown maturity, that component contributes ``None`` and is
listed in ``unknown_components`` — the score is never inflated by guesses.

``meets_threshold`` is True only when total >= 75 AND no component is
unknown — the gate the user defined for "do not scale".
"""
from __future__ import annotations

from auto_client_acquisition.assurance_os.adapters import ScorecardAdapter
from auto_client_acquisition.assurance_os.models import (
    AssuranceInputs,
    HealthComponent,
    HealthScore,
)

# component_name -> (weight, [machine_keys feeding it])
COMPONENTS: dict[str, tuple[int, list[str]]] = {
    "sales": (20, ["sales_autopilot"]),
    "marketing": (15, ["marketing_factory"]),
    "support": (15, ["support_autopilot"]),
    "partner_affiliate": (15, ["partner_machine", "affiliate_machine"]),
    "governance": (20, ["approval_center", "evidence_ledger", "no_build_engine"]),
    "delivery": (10, ["delivery_factory"]),
    "reporting": (5, ["reporting"]),
}

SCALE_THRESHOLD = 75.0


def compute_health(inputs: AssuranceInputs) -> HealthScore:
    """Compute the Full Ops Health Score from machine maturity inputs."""
    adapter = ScorecardAdapter()
    components: list[HealthComponent] = []
    total = 0.0
    known_weight = 0
    unknown: list[str] = []

    for name, (weight, machines) in COMPONENTS.items():
        levels: list[int] = []
        all_known = True
        for machine in machines:
            res = adapter.maturity(machine, inputs)
            if res.is_known:
                levels.append(res.value)
            else:
                all_known = False
        if all_known and levels:
            avg = sum(levels) / len(levels)
            contribution = round((avg / 5.0) * weight, 2)
            total += contribution
            known_weight += weight
            components.append(
                HealthComponent(name, weight, contribution,
                                f"avg maturity {avg:.1f}/5 over {len(machines)} machine(s)")
            )
        else:
            unknown.append(name)
            components.append(
                HealthComponent(name, weight, None, "machine maturity unknown")
            )

    total = round(total, 2)
    meets = not unknown and total >= SCALE_THRESHOLD
    return HealthScore(components, total, known_weight, unknown, meets)
