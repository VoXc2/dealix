"""Contract: Proof Pack v2 requires all canonical sections populated."""

from __future__ import annotations

from auto_client_acquisition.proof_architecture_os.proof_pack_v2 import (
    PROOF_PACK_V2_SECTIONS,
    proof_pack_v2_sections_complete,
)


def test_proof_pack_required_sections_enforced() -> None:
    ok, missing = proof_pack_v2_sections_complete({})
    assert not ok
    assert set(missing) == set(PROOF_PACK_V2_SECTIONS)
