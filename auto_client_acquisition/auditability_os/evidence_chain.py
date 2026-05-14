"""Evidence chain primitives for auditability (parallel to evidence_control_plane_os)."""

from __future__ import annotations

from auto_client_acquisition.evidence_control_plane_os.evidence_graph import MINI_CHAIN_KEYS

EVIDENCE_CHAIN_STAGES: tuple[str, ...] = MINI_CHAIN_KEYS


def evidence_chain_complete(present: frozenset[str]) -> tuple[bool, tuple[str, ...]]:
    missing = tuple(k for k in EVIDENCE_CHAIN_STAGES if k not in present)
    return not missing, missing


__all__ = ["EVIDENCE_CHAIN_STAGES", "evidence_chain_complete"]
