"""Ultimate Operating Manual — lightweight decision/gate helpers."""

from __future__ import annotations

from auto_client_acquisition.ultimate_manual_os.decision_rule import (
    DealixDecisionTier,
    ultimate_decision_tier,
)
from auto_client_acquisition.ultimate_manual_os.productization_gate import (
    ProductizationGateInput,
    productization_gate_passes,
)
from auto_client_acquisition.ultimate_manual_os.retainer_gate import (
    UltimateRetainerGate,
    ultimate_retainer_gate_passes,
)

__all__ = [
    "DealixDecisionTier",
    "ProductizationGateInput",
    "UltimateRetainerGate",
    "productization_gate_passes",
    "ultimate_decision_tier",
    "ultimate_retainer_gate_passes",
]
