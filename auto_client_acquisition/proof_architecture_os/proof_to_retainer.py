"""Layer 10 proof-to-retainer alias — re-exports from operating_manual_os."""

from __future__ import annotations

from auto_client_acquisition.operating_manual_os.proof_to_retainer import (
    RETAINER_GATE_THRESHOLDS,
    RetainerGateInputs,
    RetainerGateResult,
    RetainerMotion,
    evaluate_retainer_gate,
)

__all__ = [
    "RETAINER_GATE_THRESHOLDS",
    "RetainerGateInputs",
    "RetainerGateResult",
    "RetainerMotion",
    "evaluate_retainer_gate",
]
