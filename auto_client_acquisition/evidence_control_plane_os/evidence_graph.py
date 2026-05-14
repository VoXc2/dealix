"""Evidence graph — minimal chain validation for linked artifacts."""

from __future__ import annotations

from collections.abc import Mapping

# Keys for a minimal auditable story (see docs/evidence_control_plane/EVIDENCE_GRAPH.md)
MINI_CHAIN_KEYS: tuple[str, ...] = (
    "source",
    "used_by",
    "produced",
    "governed_by",
    "reviewed_by",
    "supports",
    "created_value",
)


def mini_evidence_chain_complete(chain: Mapping[str, str]) -> tuple[bool, tuple[str, ...]]:
    missing = [k for k in MINI_CHAIN_KEYS if not (chain.get(k) or "").strip()]
    return not missing, tuple(missing)
