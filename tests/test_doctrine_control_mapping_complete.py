"""Doctrine-as-code: every commitment in open-doctrine/11_NON_NEGOTIABLES.md
must map to a real, present locking artifact (test file or script).

This test is referenced by the verifier matrix (system 11 — "Evidence
Control Plane"). It is intentionally strict: if a commitment becomes
unmoored from its control, the build fails — not silently rots.
"""
from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
NON_NEG = REPO_ROOT / "open-doctrine" / "11_NON_NEGOTIABLES.md"
MAPPING = REPO_ROOT / "open-doctrine" / "CONTROL_MAPPING.md"

# The commitment → locking artifact map. This matches
# api/routers/dealix_promise.py:COMMITMENT_TO_TEST and is asserted to
# stay in lockstep with it.
COMMITMENT_TO_TEST: dict[int, str] = {
    1: "tests/test_no_source_passport_no_ai.py",
    2: "tests/test_pii_external_requires_approval.py",
    3: "tests/test_output_requires_governance_status.py",
    4: "tests/test_proof_pack_required.py",
    5: "tests/test_no_scraping_engine.py",
    6: "tests/test_no_cold_whatsapp.py",
    7: "tests/test_no_linkedin_automation.py",
    8: "tests/test_no_guaranteed_claims.py",
    9: "tests/test_agent_requires_identity_card.py",
    10: "tests/test_capital_asset_index_valid.py",
    11: "scripts/verify_all_dealix.py",
}


def test_eleven_non_negotiables_file_exists():
    assert NON_NEG.exists(), f"missing public doctrine source: {NON_NEG}"
    text = NON_NEG.read_text(encoding="utf-8")
    # 11 numbered items.
    headings = re.findall(r"^\s*(\d+)\.\s+\*\*", text, flags=re.MULTILINE)
    assert sorted(int(h) for h in headings) == list(range(1, 12)), (
        "11_NON_NEGOTIABLES.md must contain 11 numbered headings 1..11"
    )


def test_control_mapping_file_exists_and_lists_all_eleven():
    assert MAPPING.exists(), f"missing: {MAPPING}"
    text = MAPPING.read_text(encoding="utf-8")
    rows = re.findall(
        r"^\|\s*(\d+)\s*\|", text, flags=re.MULTILINE
    )
    nums = sorted(int(n) for n in rows)
    assert nums == list(range(1, 12)), (
        "CONTROL_MAPPING.md must have a row for every commitment 1..11"
    )


def test_every_commitment_has_a_locking_artifact_on_disk():
    missing = [
        f"{n}:{path}"
        for n, path in COMMITMENT_TO_TEST.items()
        if not (REPO_ROOT / path).exists()
    ]
    assert not missing, f"doctrine commitments without artifacts: {missing}"


def test_locking_artifact_map_matches_router():
    """The router's commitment→test map MUST match this test's map. If they
    drift, the public API will return broken links."""
    # Read the router file directly to avoid importing api (which pulls
    # heavy deps). Parse the COMMITMENT_TO_TEST dict literal out of the
    # source.
    router_path = REPO_ROOT / "api" / "routers" / "dealix_promise.py"
    src = router_path.read_text(encoding="utf-8")
    m = re.search(
        r"COMMITMENT_TO_TEST:\s*dict\[int,\s*str\]\s*=\s*\{(.*?)\}",
        src,
        flags=re.DOTALL,
    )
    assert m, "could not find COMMITMENT_TO_TEST in dealix_promise.py"
    body = m.group(1)
    pairs = re.findall(r"(\d+)\s*:\s*\"([^\"]+)\"", body)
    router_map = {int(k): v for k, v in pairs}
    assert router_map == COMMITMENT_TO_TEST, (
        "router COMMITMENT_TO_TEST does not match the doctrine-as-code test"
    )
