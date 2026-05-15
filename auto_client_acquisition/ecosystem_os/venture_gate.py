"""Venture gate — ecosystem spinout uses the same proof-backed gate as proof_architecture_os."""

from __future__ import annotations

from auto_client_acquisition.proof_architecture_os.proof_to_retainer import (
    VentureFactoryGateV2Input,
    venture_factory_gate_v2_passes,
)

VentureGateInput = VentureFactoryGateV2Input


def venture_gate_passes(v: VentureGateInput) -> tuple[bool, tuple[str, ...]]:
    """Delegate to canonical venture factory gate (paid clients, proof library, margin, etc.)."""
    return venture_factory_gate_v2_passes(v)
