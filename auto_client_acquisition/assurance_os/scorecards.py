"""Layer 2a — per-machine maturity scorecards.

Each machine is scored 0-5:
  0 absent | 1 fully manual | 2 templates only | 3 internally automated
  4 automated + measured + has approvals | 5 + governed + improves weekly

A machine "meets bar" when its maturity >= its minimum bar. Unknown
maturity never counts as met.
"""
from __future__ import annotations

from auto_client_acquisition.assurance_os.adapters import ScorecardAdapter
from auto_client_acquisition.assurance_os.models import (
    AssuranceInputs,
    MachineScorecard,
)

# (machine_key, label_en, label_ar, min_bar)
MACHINE_SPECS: list[tuple[str, str, str, int]] = [
    ("sales_autopilot", "Sales Autopilot", "أتمتة المبيعات", 4),
    ("marketing_factory", "Marketing Factory", "مصنع التسويق", 3),
    ("support_autopilot", "Support Autopilot", "أتمتة الدعم", 4),
    ("delivery_factory", "Delivery Factory", "مصنع التسليم", 4),
    ("partner_machine", "Partner Machine", "ماكينة الشركاء", 3),
    ("affiliate_machine", "Affiliate Machine", "ماكينة المسوّقين", 4),
    ("approval_center", "Approval Center", "مركز الموافقات", 5),
    ("evidence_ledger", "Evidence Ledger", "سجل الأدلة", 5),
    ("no_build_engine", "No-Build Engine", "محرك عدم البناء", 4),
]


def evaluate_scorecards(inputs: AssuranceInputs) -> list[MachineScorecard]:
    """Score all 9 machines from supplied maturity observations."""
    adapter = ScorecardAdapter()
    cards: list[MachineScorecard] = []
    for machine, label_en, label_ar, min_bar in MACHINE_SPECS:
        res = adapter.maturity(machine, inputs)
        maturity = res.value if res.is_known else None
        met = maturity is not None and maturity >= min_bar
        cards.append(
            MachineScorecard(machine, label_en, label_ar, min_bar, maturity, met)
        )
    return cards
