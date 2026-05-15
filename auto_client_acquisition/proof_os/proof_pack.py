"""Proof Pack v2 surface for Revenue / Client OS (canonical sections)."""

from __future__ import annotations

from collections.abc import Mapping

from auto_client_acquisition.proof_architecture_os.proof_pack_v2 import (
    PROOF_PACK_V2_SECTIONS,
    proof_pack_v2_sections_complete,
)


def build_empty_proof_pack_v2() -> dict[str, str]:
    return {k: "" for k in PROOF_PACK_V2_SECTIONS}


def merge_proof_pack_v2(base: Mapping[str, str], updates: Mapping[str, str]) -> dict[str, str]:
    out = build_empty_proof_pack_v2()
    out.update({k: (base.get(k) or "").strip() for k in PROOF_PACK_V2_SECTIONS})
    for k, v in updates.items():
        if k in PROOF_PACK_V2_SECTIONS:
            out[k] = str(v).strip()
    return out


__all__ = [
    "PROOF_PACK_V2_SECTIONS",
    "build_empty_proof_pack_v2",
    "merge_proof_pack_v2",
    "proof_pack_v2_sections_complete",
]
